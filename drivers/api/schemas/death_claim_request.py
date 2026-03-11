from pydantic import BaseModel, Field


class DeathClaimRequest(BaseModel):
    policy_number: str = Field(
        ...,
        description=(
            "The policy number for the death claim to be triaged. "
            "Use 'AMBIGUOUS' or 'MISSING' in the string to trigger different test fakes."
        ),
    )
