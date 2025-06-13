import operator
from typing import Annotated, List, Tuple
from typing_extensions import TypedDict


class GraphState(TypedDict):
    question: str
    table_id: str
    table_cap: str
    table: List[List[str]]
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    next_requirement_type: int
    response: str
