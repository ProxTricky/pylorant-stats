from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class APICache(BaseModel):
    key: str  # Clé unique pour identifier la donnée en cache
    data: dict  # Données mises en cache
    expires_at: datetime  # Date d'expiration du cache
    last_modified: datetime  # Dernière modification
    
    class Config:
        collection = "cache"

class CacheConfig:
    MATCH_HISTORY_TTL = 300  # 5 minutes
    MATCH_DETAILS_TTL = 3600  # 1 heure
    ACCOUNT_TTL = 3600  # 1 heure
    MMR_TTL = 300  # 5 minutes
