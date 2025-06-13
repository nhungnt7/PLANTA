from typing import Optional
from pydantic import BaseModel, Field

class Exception_Output(BaseModel):
    answer: Optional[str] = Field(
        description="answer to the question"
    )
    reason: Optional[str] = Field(
        description="reason for the answer"
    )