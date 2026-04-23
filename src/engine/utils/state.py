from typing import Union, Optional, TypedDict
from src.engine.workflows.RAG.Generator import AnswerWithCitations


class AgentState(TypedDict):
    query: str
    route: str

    parameters: Optional[dict]
    province: Optional[str]
    municipality: Optional[str]
    zone: Optional[str]

    answer: Optional[Union [AnswerWithCitations, dict]]
