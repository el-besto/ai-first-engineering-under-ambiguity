from enum import StrEnum

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class QualityMarker(StrEnum):
    # Tone and Policy (Required baselines)
    EMPATHETIC = "empathetic"
    CLEAR = "clear"
    NON_ADJUDICATIVE = "non-adjudicative"
    RESPECTFUL = "respectful"

    # Observability / Human Review Flags (Optional insights)
    URGENT = "urgent"  # The LLM felt the claimant's situation sounded time-sensitive
    SENSITIVE = "sensitive"  # The claim facts involve a particularly tragic or delicate situation
    COMPLEX = "complex"  # The missing requirements are unusually complicated to explain
    FRUSTRATED = "frustrated"  # The LLM detected frustration in the claimant's prior context


class FollowUpMessageSchema(BaseModel):
    reasoning: str = Field(
        description=(
            "A 1-2 sentence chain of thought about how to ask for the missing items. "
            "Discuss the tone that is appropriate (empathetic and clear) and "
            "note any terms to avoid (e.g., 'denied', 'investigating')."
        )
    )
    message: str = Field(
        description=(
            "The exact text of the message to send to the claimant or beneficiary. "
            "It must be empathetic, clear, and request the missing items."
        )
    )
    quality_markers: list[QualityMarker] = Field(
        description=(
            "A list of keywords validating the message's properties. You must select from "
            "the provided allowed enum values."
        )
    )


follow_up_message_parser = PydanticOutputParser(pydantic_object=FollowUpMessageSchema)
