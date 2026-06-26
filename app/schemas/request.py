from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from typing import Dict, Any



class Transaction(BaseModel):
    transaction_id: str = Field(..., example="TXN-9101")
    timestamp: str = Field(..., example="2026-04-14T14:08:22Z")
    type: Literal[
    "transfer",
    "payment",
    "cash_in",
    "cash_out",
    "settlement",
    "refund",
]
    amount: float = Field(..., example=5000)
    counterparty: str = Field(..., example="+8801719876543")
    status: Literal[
    "completed",
    "failed",
    "pending",
    "reversed",
]


class AnalyzeTicketRequest(BaseModel):
    ticket_id: str = Field(..., example="TKT-001")
    complaint: str = Field(
        ...,
        example="I sent 5000 taka to a wrong number around 2pm today."
    )
    language: Literal[
    "en",
    "bn",
    "mixed",
]
    channel: Literal[
    "in_app_chat",
    "call_center",
    "email",
    "merchant_portal",
    "field_agent",
]
    user_type: Literal[
    "customer",
    "merchant",
    "agent",
    "unknown",
]

    campaign_context: Optional[str] = Field(
        default=None,
        example="boishakh_bonanza_day_1"
    )

    transaction_history: List[Transaction] = Field(default_factory=list)


    metadata: Optional[Dict[str, Any]] = None