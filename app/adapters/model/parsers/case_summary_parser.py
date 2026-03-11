from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from app.entities.case_summary import CaseSummary


class CaseSummarySchema(BaseModel):
    reasoning: str = Field(
        description=(
            "A 2-3 sentence chain of thought explaining your summary. "
            "Identify the key facts of the claim, note any obviously missing context, "
            "and explain why the summary accurately reflects the provided facts."
        )
    )
    summary: str = Field(
        description=(
            "A concise, operational 1-paragraph summary of the death claim. "
            "Do NOT adjudicate the claim. Do NOT state if the claim is approved or denied."
        )
    )


case_summary_parser = PydanticOutputParser(pydantic_object=CaseSummarySchema)


def map_to_case_summary(parsed: CaseSummarySchema) -> CaseSummary:
    """Maps the Pydantic schema from the LLM adapter to the immutable Domain entity."""
    return CaseSummary(summary_text=parsed.summary)
