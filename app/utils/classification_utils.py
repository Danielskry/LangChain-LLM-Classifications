""" Classification utils """

from typing import List
import json
import uuid

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    ToolMessage,
)

from app.core.logger import get_logger
logger = get_logger(__name__)

def tool_example_to_messages(classification_example: dict) -> List[BaseMessage]:
    """
    Converts a classification example into a list of messages suitable for the LLM.
    
    Parameters:
    - classification_example (dict): The example containing input and tool calls.
    
    Returns:
    - List[BaseMessage]: A list of messages derived from the provided example.
    """
    # Initialize the list of messages with the human input message
    messages: List[BaseMessage] = [HumanMessage(content=str(classification_example["input"]))]
    openai_tool_calls = []  # List to store tool call information
    total_length = 0  # Track the cumulative length of tool calls
    max_total_length = 1024  # Maximum allowed length for all tool calls combined
    
    # Iterate over each tool call in the example
    for tool_call in classification_example["tool_calls"]:
        logger.debug(f"Processing tool_call: {tool_call} (type: {type(tool_call)})")

        # Serialize tool call to JSON, handling different possible types
        if hasattr(tool_call, 'json'):
            tool_call_json = tool_call.json()
        else:
            if isinstance(tool_call, dict):
                tool_call_json = json.dumps(tool_call)
            else:
                logger.error(f"tool_call does not have a 'json' method: {tool_call}")
                raise TypeError(f"tool_call of type {type(tool_call)} does not have a 'json' method.")

        # Calculate JSON structure overhead for the tool call
        json_structure_overhead = len(json.dumps({
            "id": str(uuid.uuid4()),
            "type": "function",
            "function": {
                "name": tool_call.__class__.__name__,
                "arguments": ""
            }
        }))

        # Calculate maximum length allowed for the tool call JSON
        max_length = max_total_length - total_length - json_structure_overhead

        # Truncate tool call JSON if it exceeds the maximum allowed length
        if len(tool_call_json) > max_length:
            tool_call_json = tool_call_json[:max_length]
            logger.warning(f"Truncated tool call JSON to fit within max length: {max_length}")

        # Update the total length after considering the current tool call
        total_length += len(tool_call_json) + json_structure_overhead

        # Append the structured tool call information to the list
        openai_tool_calls.append(
            {
                "id": str(uuid.uuid4()),  # Unique identifier for the tool call
                "type": "function",
                "function": {
                    "name": tool_call.__class__.__name__,  # Name of the tool call class
                    "arguments": tool_call_json,  # Serialized tool call arguments
                },
            }
        )
        logger.debug(f"Added tool call with length {len(tool_call_json)}. Total length now {total_length}.")
    
    # Add an AI message with tool calls to the messages list
    messages.append(
        AIMessage(
            content="",
            additional_kwargs={
                "tool_calls": openai_tool_calls
            }
        )
    )

    # Get the tool outputs from the example or use a default message if not provided
    tool_outputs = classification_example.get("tool_outputs") or [
        "You have correctly called this tool."
    ] * len(openai_tool_calls)

    # Append each tool output message linked to its corresponding tool call ID
    for output, tool_call in zip(tool_outputs, openai_tool_calls):
        messages.append(
            ToolMessage(
                content=output, tool_call_id=tool_call["id"]
            )
        )

    # Return the list of constructed messages
    return messages
