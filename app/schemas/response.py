from typing import List, Literal
from pydantic import BaseModel, Field


class AnalyzeTicketResponse(BaseModel):
    ticket_id: str = Field(..., example="TKT-001")

    relevant_transaction_id: str = Field(
        ...,
        example="TXN-9101"
    )

    evidence_verdict: Literal[
        "consistent",
        "inconsistent",
        "insufficient_evidence"
    ] = Field(
        ...,
        example="consistent"
    )

    case_type: str = Field(
        ...,
        example="wrong_transfer"
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ] = Field(
        ...,
        example="high"
    )

    department: str = Field(
        ...,
        example="dispute_resolution"
    )

    agent_summary: str = Field(
        ...,
        example="Customer reports sending 5000 BDT via transaction TXN-9101 to the wrong recipient."
    )

    recommended_next_action: str = Field(
        ...,
        example="Verify TXN-9101 details with the customer and initiate the dispute workflow."
    )

    customer_reply: str = Field(
        ...,
        example="We have noted your concern regarding transaction TXN-9101. Our team is reviewing the issue and will update you shortly."
    )

    human_review_required: bool = Field(
        ...,
        example=True
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        example=0.90
    )

    reason_codes: List[str] = Field(
        default_factory=list,
        example=[
            "wrong_transfer",
            "transaction_match"
        ]
    )