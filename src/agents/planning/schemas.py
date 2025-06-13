from pydantic import BaseModel, Field
from typing import List, Optional


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: Optional[List[str]] = Field(
        None, description="different steps to follow, should be in sorted order"
    )
