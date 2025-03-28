from pydantic import BaseModel,Field
from typing_extensions import TypedDict,Literal

# Schema for structured output to use in evaluation
class DesignFeedback(BaseModel):
    grade: Literal["Accepted", "Rejected"] = Field(
        description="Decide if detail design of the project is Accepted or Rejected.",
    )
    feedback: str = Field(
        description="If detail design of the project is not acceptable, provide feedback on how to improve it.",
    )