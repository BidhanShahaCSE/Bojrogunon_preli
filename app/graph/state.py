from typing import TypedDict, Optional, List, Literal, Dict, Any


# ==========================================================
# Transaction History
# ==========================================================

class Transaction(TypedDict):
    transaction_id: str
    timestamp: str

    type: Literal[
        "transfer",
        "payment",
        "cash_in",
        "cash_out",
        "settlement",
        "refund",
    ]

    amount: float

    counterparty: str

    status: Literal[
        "completed",
        "failed",
        "pending",
        "reversed",
    ]


# ==========================================================
# Complaint Analysis (LLM 1)
# ==========================================================

class ComplaintAnalysis(TypedDict):
    intent: str
    summary: str

    amount: Optional[float]

    transaction_type: Optional[
        Literal[
            "transfer",
            "payment",
            "cash_in",
            "cash_out",
            "settlement",
            "refund",
        ]
    ]

    time_reference: Optional[str]

    counterparty: Optional[str]


# ==========================================================
# Graph State
# ==========================================================

class GraphState(TypedDict):

    # ======================================================
    # Request (Input)
    # ======================================================

    ticket_id: str

    complaint: str

    language: Optional[
        Literal[
            "en",
            "bn",
            "mixed",
        ]
    ]

    channel: Optional[
        Literal[
            "in_app_chat",
            "call_center",
            "email",
            "merchant_portal",
            "field_agent",
        ]
    ]

    user_type: Optional[
        Literal[
            "customer",
            "merchant",
            "agent",
            "unknown",
        ]
    ]

    campaign_context: Optional[str]

    transaction_history: List[Transaction]

    metadata: Optional[Dict[str, Any]]

    # ======================================================
    # LLM 1 Output
    # Complaint Analysis + Transaction Matching
    # ======================================================

    complaint_analysis: ComplaintAnalysis

    match_found: bool

    relevant_transaction_id: str | None

    matched_transaction: Optional[Transaction]

    # ======================================================
    # LLM 2 Output
    # Investigation
    # ======================================================

    evidence_verdict: Literal[
    "consistent",
    "inconsistent",
    "insufficient_data",
]

    case_type: Optional[
        Literal[
            "wrong_transfer",
            "payment_failed",
            "refund_request",
            "duplicate_payment",
            "merchant_settlement_delay",
            "agent_cash_in_issue",
            "phishing_or_social_engineering",
            "other",
        ]
    ]

    severity: Optional[
        Literal[
            "low",
            "medium",
            "high",
            "critical",
        ]
    ]

    department: Optional[
        Literal[
            "customer_support",
            "dispute_resolution",
            "payments_ops",
            "merchant_operations",
            "agent_operations",
            "fraud_risk",
        ]
    ]

    human_review_required: bool

    confidence: Optional[float]

    reason_codes: List[str]

    # ======================================================
    # LLM 3 Output
    # Response Generation
    # ======================================================

    agent_summary: Optional[str]

    recommended_next_action: Optional[str]

    customer_reply: Optional[str]

    # ======================================================
    # Internal
    # ======================================================

    errors: List[str]