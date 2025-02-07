from datetime import datetime
from typing import List, TypedDict
import json

from app.schemas.incident_schema import IncidentReport, WitnessDetail
from app.schemas.classification_schema import IncidentClassification


class Example(TypedDict):
    """A representation of an example consisting of text input and expected tool calls.

    For extraction, the tool calls are represented as instances of pydantic model.
    """

    input: IncidentReport  # Incident report example
    tool_calls: List[IncidentClassification]  # Instances of pydantic model that should be extracted

def serialize_example(example: Example) -> dict:
    """Serialize example to a format suitable for JSON encoding."""
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, IncidentReport):
            return obj.dict()
        if isinstance(obj, IncidentClassification):
            return obj.dict()
        raise TypeError(f"Type {type(obj)} not serializable")

    return json.loads(json.dumps(example, default=default_serializer))

classification_examples: List[Example] = [
    {
        "input": IncidentReport(
            incident_datetime=datetime(2023, 5, 10, 14, 30),
            location="Main Office",
            description="Unauthorized access to the server room.",
            witnesses=[
                WitnessDetail(name="John Doe", contact="john.doe@example.com")
            ]
        ),
        "tool_calls": [
            IncidentClassification(
                language="english",
                urgency="high",
                breach="confidentiality",
                category="Technology",
                asset="Hardware"
            )
        ]
    },
    {
        "input": IncidentReport(
            incident_datetime=datetime(2023, 6, 15, 9, 0),
            location="Branch Office",
            description="Suspicious email received by multiple employees.",
            witnesses=[
                WitnessDetail(name="Jane Smith", contact="jane.smith@example.com")
            ]
        ),
        "tool_calls": [
            IncidentClassification(
                language="english",
                urgency="moderate",
                breach="integrity",
                category="People",
                asset="Information"
            )
        ]
    },
    {
        "input": IncidentReport(
            incident_datetime=datetime(2023, 7, 20, 16, 45),
            location="Headquarters",
            description="Physical break-in detected at the main entrance.",
            witnesses=[
                WitnessDetail(name="Alice Johnson", contact="alice.johnson@example.com"),
                WitnessDetail(name="Bob Lee", contact="bob.lee@example.com")
            ]
        ),
        "tool_calls": [
            IncidentClassification(
                language="english",
                urgency="high",
                breach="availability",
                category="Physical",
                asset="Offices"
            )
        ]
    },
    {
        "input": IncidentReport(
            incident_datetime=datetime(2023, 8, 5, 11, 20),
            location="Data Center",
            description="Power outage affecting the server racks.",
            witnesses=None
        ),
        "tool_calls": [
            IncidentClassification(
                language="english",
                urgency="high",
                breach="availability",
                category="Technology",
                asset="Services"
            )
        ]
    }
]

# Apply serialization to each example
classification_examples_serialized = [serialize_example(example) for example in classification_examples]
