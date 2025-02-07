""" Schemas for reporting incidents """ 
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.classification_schema import IncidentClassification

class WitnessDetail(BaseModel):
    """ Witness schema """
    name: str = Field(
        ...,
        title="Name",
        description="Name of the witness"
    )
    contact: str = Field(
        ...,
        title="Contact",
        description="Contact details of the witness"
    )

class IncidentReport(BaseModel):
    incident_datetime: datetime = Field(
        ...,
        title="Date and Time",
        description="Date and time of the incident"
    )
    location: str = Field(
        ...,
        title="Location",
        description="Location of the incident"
    )
    description: str = Field(
        ...,
        title="Description",
        description="Description of the incident"
    )
    witnesses: Optional[List[WitnessDetail]] = Field(
        None,
        title="Witnesses",
        description="Details of the witnesses, if any"
    )


class IncidentResponse(BaseModel):
    incident_report: IncidentReport = Field(
        ...,
        title="Incident report",
        description="Report on incident"
    )
    incident_classification: IncidentClassification = Field(
        ...,
        title="Incident classification",
        description="Classification based on report of incident"
    )
