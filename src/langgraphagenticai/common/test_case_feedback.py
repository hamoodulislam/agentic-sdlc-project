from pydantic import BaseModel,Field
from typing_extensions import TypedDict,Literal

# Schema for structured output to use in evaluation
class TestCaseFeedback(BaseModel):
    grade: Literal["Accepted", "Rejected"] = Field(
        description="Decide if test cases of project are Accepted or Rejected.",
    )
    feedback: str = Field(
        description="If test cases review of the project is not acceptable, provide feedback on how to improve it.",
    )