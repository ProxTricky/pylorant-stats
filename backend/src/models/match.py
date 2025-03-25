from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class MatchStats(BaseModel):
    kills: int
    deaths: int
    assists: int
    score: int
    headshots: int
    bodyshots: int
    legshots: int
    ability_casts: dict
    damage_made: int
    damage_received: int

class Match(BaseModel):
    match_id: str
    map_id: str
    game_start: datetime
    game_length: int
    game_mode: str
    rounds_played: int
    rounds_won: int
    rounds_lost: int
    agent: str
    stats: MatchStats
    team_score: int
    opponent_score: int
    rank_rating_change: Optional[int]
    current_tier: Optional[int]
    
    class Config:
        collection = "matches"
