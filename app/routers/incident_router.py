from fastapi import APIRouter

from app.services.incident_service import IncidentService
from app.schemas.incident_schema import IncidentReport, IncidentResponse

incident_router = APIRouter()

from app.core.logger import get_logger
logger = get_logger(__name__)

@incident_router.post("/report-incident")
async def report_incident(incident: IncidentReport):
    """
    Endpoint for reporting an incident.

    Parameters:
    - incident (IncidentReport): The incident report details.

    Returns:
    - response (IncidentResponse): based on the reported incident and its classification.
    """
    incident_classification = IncidentService().classify(incident)

    return incident_classification
