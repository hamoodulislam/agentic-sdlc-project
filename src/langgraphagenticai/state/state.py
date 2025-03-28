from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from typing import TypedDict, Annotated, List
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    """
    Represents the structure of the state used in the graph.
    """
    project_title: str
    project_lang: str
    project_requirements: str
    llm_generated_stories: str
    product_owner_stories_feedback: str
    product_owner_accept_reject_stories: str
    llm_generated_design_docs: str
    llm_design_feedback: str
    llm_accept_reject_design: str
    llm_generated_code: str
    llm_code_feedback: str
    llm_accept_reject_code: str
    llm_security_feedback: str
    llm_accept_reject_security: str
    llm_generated_test_cases: str
    llm_test_cases_feedback: str
    llm_accept_reject_test_cases: str
    llm_qa_feedback: str
    llm_accept_reject_qa: str
    llm_deploy_instructions: str
    llm_monitoring_instructions: str