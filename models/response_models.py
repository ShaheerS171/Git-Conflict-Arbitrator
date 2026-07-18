from pydantic import BaseModel, Field


class ArbitrationResponse(BaseModel):

    conflict_analysis: str = Field(
        description="Detailed explanation of the conflict."
    )

    security_analysis: str = Field(
        description="Security review of both implementations."
    )

    merged_strategy: str = Field(
        description="How both implementations were merged."
    )

    resolved_code: str = Field(
        description="Production ready merged code."
    )

    architectural_notes: str = Field(
        description="Architecture recommendations."
    )

    risks: str = Field(
        description="Potential remaining risks."
    )

    confidence: str = Field(
        description="High, Medium or Low."
    )