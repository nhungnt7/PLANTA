from pydantic import BaseModel, Field


class QuestionType(BaseModel):
    """Return enum for different types of questions
    1: search in the table
    2: calculation
    3: comparison
    """

    question_type: int = Field(
        description="Type of question to be answered. 1 if the question need a search in the table, 2 if the question need a calculation, 3 if the question need a comparison"
    )
