from pydantic import BaseModel, Field, ValidationError
from typing import Union, Any, Optional
from src.agents.planning.schemas import Plan


class Response(BaseModel):
    """Return the answer for the given question."""

    response: Optional[str] = Field(
        None,
        description="Answer for the given question. Please return only answer extracted or calculated from the table without any explaination or reasons. Note that the answer should be in tag <answer></answer>.",
    )


class Act(BaseModel):
    """Act based on the given context (Continue with the plan or respond with the answer)."""

    action: Optional[Union[Plan, Response]] = Field(
        None,
        description="Next action to perform. If you can answer the given question based on the given past_steps please use Response type to answer the question. If you need to further information to get the answer, use Plan.",
    )
