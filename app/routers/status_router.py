from fastapi import APIRouter
from app.schemas.status_schema import Status

status_router = APIRouter()

@status_router.get("/status", response_model=Status, tags=["status"])
async def get_status():
    """
    Get system status.

    This endpoint is exposed and used as a health check to ensure the service is up and running.

    Returns:
    - Status: An object containing the status message.
    """
    return {"status": "OK", "message": "Service is up and running."}
