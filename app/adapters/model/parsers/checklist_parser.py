from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class ChecklistSchema(BaseModel):
    reasoning: str = Field(
        description=(
            "A 1-2 sentence chain of thought explaining your assessment of the missing items. "
            "Identify exactly what documents are needed based on the logic facts provided."
        )
    )
    missing_items: list[str] = Field(
        description=(
            "A list of clearly named documents or information needed to complete the claim. "
            "Each item should be a short, actionable directive (e.g., 'A certified copy of the death certificate')."
        )
    )


checklist_parser = PydanticOutputParser(pydantic_object=ChecklistSchema)


def map_to_requirements_checklist_string(parsed: ChecklistSchema) -> str:
    """Maps the Pydantic schema to a bulleted markdown string for the graph state."""
    if not parsed.missing_items:
        return ""
    return "\n".join(f"- {item}" for item in parsed.missing_items)
