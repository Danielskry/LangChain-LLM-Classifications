# LangChain LLM Classifications Demo 

This repository demonstrates how to harness large language models (LLMs) to perform structured classifications on input to the LLM. With this setup, you can easily customize the classification schema to match your specific requirements.

In this demo, the main workflow involves sending an incident report (formatted in `app/schemas/incident_schema.py`) to the LLM. The LLM processes the input and returns a structured classification based on the schema defined in `app/schemas/classification_schema.py`. Note that the project employs a few-shot prompting technique (see `app/schemas/examples/classification_schema.py`) to guide the LLM in generating accurate responses.

### Classification Schema Details (`incident_schema.py`)
When submitting an incident report, include the following fields:

```python
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
```

You may change this schema to something that suits yourself.

#### Example request

```json
{
  "incident_datetime": "2024-06-11T14:30:00Z",
  "location": "Main Office Building, Floor 3",
  "description": "There was a power outage affecting the entire floor.",
  "witnesses": [
    {
      "name": "John Doe",
      "contact": "john.doe@example.com"
    },
    {
      "name": "Jane Smith",
      "contact": "jane.smith@example.com"
    }
  ]
}
```

#### Response

```json
{
    "language": "english",
    "urgency": "high",
    "breach": "availability",
    "category": "Physical",
    "asset": "Offices"
}
```

## Get started

**1. Configure Environment Variables:**

Rename the .env.example file to .env and fill in the required values.


**2. Build application with Docker:**

You can build and run the application using Docker with the command below:
```bash
docker-compose --env-file .env up -d --build
```

Alternatively, run the project locally with Poetry as your dependency manager:
```bash
poetry build
poetry run python3 server.py
```

**3. Access the API Documentation:**

Once the API is up and running, open your browser and navigate to http://localhost:8000/docs to explore the documentation and test the API.
