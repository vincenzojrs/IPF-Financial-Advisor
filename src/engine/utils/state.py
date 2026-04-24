from typing import Optional, TypedDict


class AgentState(TypedDict):
    query: str
    route: str

    parameters: Optional[dict]
    province: Optional[str]
    municipality: Optional[str]
    zone: Optional[str]

    answer: Optional[str]
