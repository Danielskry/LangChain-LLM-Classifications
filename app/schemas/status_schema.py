""" Schema for status endpoint """
from pydantic import BaseModel, Field

class Status(BaseModel):
    """ Status message for server. """
    status: str = Field(
        ...,
        title="Status",
        description="Status from endpoint."
    )
    message: str = Field(
        ...,
        title="Message",
        description="Message from endpoint."
    )
