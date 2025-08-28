from fastapi import FastAPI, Query
from pymongo import MongoClient
import logging
from .. import config

app = FastAPI(title="data-retrival-service",version="1.0.0")
logger = logging.getLogger(__name__)

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]

def fetch(coll_name: str, limit: int, skip: int):
    coll = db[coll_name]
    docs = list(coll.find().sort("CreateDate", -1).skip(skip).limit(limit))
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "OK", "message": "Data Retrieval Service is running."}

@app.get("/tweets/antisemitic")
async def get_antisemitic_data(limit: int = Query(10, ge=1, le=200), skip: int = Query(0, ge=0)):
    """
    Endpoint to return antisemitic tweets data.
    """
    return fetch(config.MONGODB_COL_ANTISEMITIC, limit, skip)

@app.get("/tweets/not-antisemitic")
async def get_not_antisemitic_data(limit: int = Query(10, ge=1, le=200), skip: int = Query(0, ge=0)):
    """
    Endpoint to return non-antisemitic tweets data.
    """
    return fetch(config.MONGODB_COL_NOT_ANTISEMITIC, limit, skip)
