from typing import List, Dict, Any
from fastapi import FastAPI, Query
from pymongo import MongoClient
from .. import config

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]

app = FastAPI(title="Tweets Data Retrieval API", version="1.0.0")

def fetch(coll_name: str, limit: int, skip: int) -> List[Dict[str, Any]]:
    coll = db[coll_name]
    docs = list(coll.find().sort("CreateDate", -1).skip(skip).limit(limit))
    for d in docs:
        d["_id"] = str(d.get("_id"))
    return docs

@app.get("/tweets/antisemitic")
def get_antisemitic(limit: int = Query(10, ge=1, le=200), skip: int = Query(0, ge=0)):
    return fetch("tweets_antisemitic", limit, skip)

@app.get("/tweets/not-antisemitic")
def get_not_antisemitic(limit: int = Query(10, ge=1, le=200), skip: int = Query(0, ge=0)):
    return fetch("tweets_not_antisemitic", limit, skip)


@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Data Retrieval Service is running."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)