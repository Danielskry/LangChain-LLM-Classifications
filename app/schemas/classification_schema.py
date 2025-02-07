from langchain_core.pydantic_v1 import BaseModel, Field

class IncidentClassification(BaseModel):
    language: str = Field(
        ...,
        enum=["english", "norwegian"]
    )
    urgency: str = Field(
        ...,
        enum=["minimal", "low", "moderate", "high"]
    )
    breach: str = Field(
        ...,
        enum=["confidentiality", "integrity", "availability"]
    )
    category: str = Field(
        ...,
        enum=["Organisational", "People", "Physical", "Technology"]
    )
    asset: str = Field(
        ...,
        enum=["Information", "Intangible assets", "People", "Hardware", "Software", "Services", "Offices"]
    )

