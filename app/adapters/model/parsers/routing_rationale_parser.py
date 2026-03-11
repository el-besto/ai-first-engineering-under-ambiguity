from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class RoutingRationaleSchema(BaseModel):
    reasoning: str = Field(
        description=(
            "A 1-2 sentence chain of thought about why this claim is being escalated. "
            "Discuss the provided escalation reasons."
        )
    )
    rationale: str = Field(
        description=(
            "A 1-paragraph explanation of why the claim is being routed to human review, "
            "suitable for internal reviewers. Synthesize the ambiguous or complex facts."
        )
    )


routing_rationale_parser = PydanticOutputParser(pydantic_object=RoutingRationaleSchema)
