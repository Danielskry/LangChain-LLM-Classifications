from fastapi import status
import json

from langchain_core.prompts import ChatPromptTemplate

from app.core.llm_session import get_llm
from app.core.environment import get_environment
from app.core.exceptions import raise_with_log

from app.utils.classification_utils import tool_example_to_messages
from app.utils.json_utils import convert_datetimes_to_iso

from app.schemas.incident_schema import IncidentReport
from app.schemas.classification_schema import IncidentClassification
from app.schemas.examples.classification_examples import classification_examples_serialized

from app.core.logger import get_logger
logger = get_logger(__name__)

class IncidentService:
    def __init__(self):
        """
        Initialize the IncidentService with environment settings and LLM.
        """
        self.ENVIRONMENT = get_environment()
        self.LLM = get_llm()
        self.PROMPT_TEMPLATE = ChatPromptTemplate.from_template(
            """
            Extract the desired information from the following incident report.

            Only extract the properties mentioned in the 'IncidentClassification' function.

            incident report:
            {input}
            """
        )
        
        if self.LLM is None:
            raise RuntimeError("Failed to retrieve the language model!")

        logger.info(f"Initialized IncidentService with environment: {self.ENVIRONMENT}")
    
    def classify(self, incident: IncidentReport) -> IncidentClassification:
        """
        Classify the given incident report into IncidentClassification.
        """
        try:
            messages = []
            for example in classification_examples_serialized:
                example_messages = tool_example_to_messages(
                    {
                        "input": example["input"],
                        "tool_calls": example["tool_calls"]
                    }
                )
                messages.extend(example_messages)

            # Ensuring that the LLM has structured output capability
            llm_with_structured_output = self.LLM.with_structured_output(schema=IncidentClassification)
            tagging_chain = self.PROMPT_TEMPLATE | llm_with_structured_output

            # Convert the incident to a dictionary before passing it to the LLM
            incident_dict = convert_datetimes_to_iso(incident.dict())

            incident_json = json.dumps(incident_dict)

            # Invoke the LLM with the incident data and examples
            incident_classification = tagging_chain.invoke(
                {
                    "input": incident_json,
                    "examples": messages
                }
            )

            logger.info(f"LLM response: {incident_classification} (type: {type(incident_classification)})")

            if isinstance(incident_classification, str):
                incident_classification = json.loads(incident_classification)
                logger.info(f"Parsed JSON response: {incident_classification} (type: {type(incident_classification)})")

            if not isinstance(incident_classification, IncidentClassification):
                incident_classification = IncidentClassification(**incident_classification)
                logger.info(f"Converted to Classification object: {incident_classification} (type: {type(incident_classification)})")

            return incident_classification
        except Exception as e:
            logger.error(f"Error in classification of incident report: {e}")
            raise_with_log(status.HTTP_422_UNPROCESSABLE_ENTITY, "Could not classify incident report.")
