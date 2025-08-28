from fastapi import FastAPI
import logging

app = FastAPI(title="data-retrival-service",version="1.0.0")
logger = logging.getLogger(__name__)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "OK", "message": "Data Retrieval Service is running."}

@app.get("/antishemic")
async def antishemic_data():
    """
    Endpoint to retrun the antishemic functionality.
    """
