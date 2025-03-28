from pydantic import BaseModel,Field
from typing_extensions import TypedDict,Literal

# Schema for structured output to use in evaluation
class StoryFeedback(BaseModel):
    grade: Literal["Accepted", "Rejected"] = Field(
        description="Decide if user stories are Accepted or Rejected.",
    )
    feedback: str = Field(
        description="If the user stories are not acceptable, provide feedback on how to improve it.",
    )