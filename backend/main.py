import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from src.api.routes import router

# Charge les variables d'environnement
load_dotenv()

app = FastAPI(title="Valorant Stats API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # A modifier en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration MongoDB
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "valorant_stats")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(MONGODB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    
    # Création des index
    await app.mongodb["matches"].create_index("match_id", unique=True)
    await app.mongodb["cache"].create_index("key", unique=True)
    await app.mongodb["cache"].create_index("expires_at", expireAfterSeconds=0)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Inclusion des routes
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
