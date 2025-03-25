from fastapi import APIRouter, Depends, HTTPException
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient
from ..services.valorant_api import ValorantAPI
from ..models.match import Match

router = APIRouter()

async def get_valorant_api(db: AsyncIOMotorClient = Depends()):
    return ValorantAPI(db)

@router.get("/matches/{name}/{tag}", response_model=List[Match])
async def get_match_history(
    name: str,
    tag: str,
    valorant_api: ValorantAPI = Depends(get_valorant_api)
):
    """Récupère l'historique des matchs pour un joueur"""
    try:
        matches = await valorant_api.get_match_history(name, tag)
        return matches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matches/{match_id}", response_model=Match)
async def get_match_details(
    match_id: str,
    valorant_api: ValorantAPI = Depends(get_valorant_api)
):
    """Récupère les détails d'un match spécifique"""
    match = await valorant_api.matches_collection.find_one({"match_id": match_id})
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return Match(**match)
