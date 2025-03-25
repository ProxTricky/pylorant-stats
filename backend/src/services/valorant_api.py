import os
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.cache import APICache, CacheConfig
from ..models.match import Match, MatchStats

class ValorantAPI:
    def __init__(self, db: AsyncIOMotorClient):
        self.base_url = "https://api.henrikdev.xyz/valorant/v3"
        self.headers = {"Authorization": os.getenv("HENRIK_API_KEY")}
        self.db = db
        self.cache_collection = db[APICache.Config.collection]
        self.matches_collection = db[Match.Config.collection]

    async def get_cached_data(self, cache_key: str) -> Optional[dict]:
        """Récupère les données en cache si elles existent et sont valides"""
        cache = await self.cache_collection.find_one({"key": cache_key})
        if cache and datetime.utcnow() < cache["expires_at"]:
            return cache["data"]
        return None

    async def set_cached_data(self, cache_key: str, data: dict, ttl: int):
        """Met en cache les données avec une durée de vie (TTL)"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        await self.cache_collection.update_one(
            {"key": cache_key},
            {
                "$set": {
                    "data": data,
                    "expires_at": expires_at,
                    "last_modified": datetime.utcnow()
                }
            },
            upsert=True
        )

    async def get_match_history(self, name: str, tag: str) -> List[Match]:
        """Récupère l'historique des matchs avec gestion du cache"""
        cache_key = f"history:{name}#{tag}"
        
        # Vérifie le cache
        cached_data = await self.get_cached_data(cache_key)
        if cached_data:
            return [Match(**match) for match in cached_data]

        # Appel API si pas en cache
        response = requests.get(
            f"{self.base_url}/matches/{name}/{tag}",
            headers=self.headers
        )
        response.raise_for_status()
        matches_data = response.json()["data"]

        # Traite et sauvegarde chaque match
        processed_matches = []
        for match_data in matches_data:
            match = await self.process_match(match_data)
            if match:
                processed_matches.append(match)

        # Met en cache les résultats
        await self.set_cached_data(
            cache_key,
            [match.dict() for match in processed_matches],
            CacheConfig.MATCH_HISTORY_TTL
        )

        return processed_matches

    async def process_match(self, match_data: dict) -> Optional[Match]:
        """Traite et sauvegarde un match si pas déjà en base"""
        match_id = match_data["metadata"]["matchid"]

        # Vérifie si le match existe déjà
        existing_match = await self.matches_collection.find_one({"match_id": match_id})
        if existing_match:
            return Match(**existing_match)

        # Crée l'objet Match
        try:
            match = Match(
                match_id=match_id,
                map_id=match_data["metadata"]["map"],
                game_start=datetime.fromtimestamp(match_data["metadata"]["game_start"]),
                game_length=match_data["metadata"]["game_length"],
                game_mode=match_data["metadata"]["mode"],
                rounds_played=match_data["metadata"]["rounds_played"],
                rounds_won=match_data["teams"]["red"]["rounds_won"],
                rounds_lost=match_data["teams"]["blue"]["rounds_won"],
                agent=match_data["players"]["all_players"][0]["character"],
                stats=MatchStats(
                    kills=match_data["players"]["all_players"][0]["stats"]["kills"],
                    deaths=match_data["players"]["all_players"][0]["stats"]["deaths"],
                    assists=match_data["players"]["all_players"][0]["stats"]["assists"],
                    score=match_data["players"]["all_players"][0]["stats"]["score"],
                    headshots=match_data["players"]["all_players"][0]["stats"]["headshots"],
                    bodyshots=match_data["players"]["all_players"][0]["stats"]["bodyshots"],
                    legshots=match_data["players"]["all_players"][0]["stats"]["legshots"],
                    ability_casts=match_data["players"]["all_players"][0]["ability_casts"],
                    damage_made=match_data["players"]["all_players"][0]["damage_made"],
                    damage_received=match_data["players"]["all_players"][0]["damage_received"]
                ),
                team_score=match_data["teams"]["red"]["rounds_won"],
                opponent_score=match_data["teams"]["blue"]["rounds_won"],
                rank_rating_change=match_data.get("mmr_change", None),
                current_tier=match_data.get("currenttier", None)
            )

            # Sauvegarde le match en base
            await self.matches_collection.insert_one(match.dict())
            return match

        except KeyError as e:
            print(f"Erreur lors du traitement du match {match_id}: {e}")
            return None
