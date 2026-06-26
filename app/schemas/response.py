from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class AnalyzeTicketResponse(BaseModel):
    ticket_id: str = Field(
        ...,
        example="TKT-001"
    )

    # Match না পেলে null হবে
    relevant_transaction_id: Optional[str] = Field(
        default=None,
        example="TXN-9101"
    )

    # Hackathon taxonomy
    evidence_verdict: Literal[
        "consistent",
        "inconsistent",
        "insufficient_data",
    ] = Field(
        ...,
        example="consistent"
    )

    case_type: Literal[
        "wrong_transfer",
        "payment_failed",
        "refund_request",
        "duplicate_payment",
        "merchant_settlement_delay",
        "agent_cash_in_issue",
        "phishing_or_social_engineering",
        "other",
    ] = Field(
        ...,
        example="wrong_transfer"
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical",
    ] = Field(
        ...,
        example="high"
    )

    department: Literal[
        "customer_support",
        "dispute_resolution",
        "payments_ops",
        "merchant_operations",
        "agent_operations",
        "fraud_risk",
    ] = Field(
        ...,
        example="dispute_resolution"
    )

    agent_summary: str = Field(
        ...,
        example="Customer reports sending money to the wrong recipient."
    )

    recommended_next_action: str = Field(
        ...,
        example="Verify transaction details and initiate dispute workflow."
    )

    customer_reply: str = Field(
        ...,
        example="We have received your complaint. Our team is reviewing it and will contact you shortly."
    )

    human_review_required: bool = Field(
        ...,
        example=True
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        example=0.91
    )

    reason_codes: List[str] = Field(
        default_factory=list,
        example=[
            "transaction_match",
            "wrong_transfer",
        ]
    )