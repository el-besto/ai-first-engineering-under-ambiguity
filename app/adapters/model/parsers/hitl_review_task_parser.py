from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class HITLReviewTaskSchema(BaseModel):
    reasoning: str = Field(
        description=(
            "A 1-2 sentence chain of thought about what a human reviewer needs to do "
            "to resolve the ambiguity or review the claim."
        )
    )
    task_description: str = Field(
        description=("A clear, operational task description dictating what the human reviewer must check.")
    )


hitl_review_task_parser = PydanticOutputParser(pydantic_object=HITLReviewTaskSchema)
