import os
from typing import Optional, List, Dict, Any, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

load_dotenv()

# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# ==========================================================
# Structured Output
# ==========================================================


class InvestigationOutput(BaseModel):

    evidence_verdict: Literal[
        "consistent",
        "inconsistent",
        "insufficient_data"
    ] = Field(
        ...,
        description="Whether transaction history supports the complaint."
    )

    case_type: str = Field(
        ...,
        description="Complaint category."
    )

    severity: Literal[
        "low",
        "medium",
        "high",
        "critical"
    ] = Field(
        ...,
        description="Case severity."
    )

    department: str = Field(
        ...,
        description="Department responsible for handling the complaint."
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Confidence score."
    )

    human_review_required: bool = Field(
        ...,
        description="Whether a human agent should review the case."
    )

    reason_codes: List[str] = Field(
        ...,
        description="Short machine-readable reasoning codes."
    )


structured_llm = llm.with_structured_output(
    InvestigationOutput
)

# ==========================================================
# LangGraph Node
# ==========================================================


def investigation_node(
    state: Dict[str, Any],
) -> Dict[str, Any]:
    """
    LangGraph Node 2

    Responsibilities

    - Determine evidence_verdict

    - Determine case_type

    - Determine severity

    - Determine department

    - Determine confidence

    - Determine reason_codes

    - Determine human_review_required
    """

    prompt = f"""
You are an AI Complaint Investigation Expert.

Your task is to investigate the complaint using the output from
the previous investigation stage.

You MUST determine

1. evidence_verdict

Allowed values

- consistent
- inconsistent
- insufficient_data

Definitions

consistent
The available transaction supports the customer's complaint.

inconsistent
The available transaction contradicts the customer's complaint.

insufficient_data
There is not enough information to determine whether
the complaint is true.

------------------------------------------------

2. case_type

Examples

wrong_transfer

failed_transaction

merchant_settlement

refund_request

balance_deduction

fraud

cash_in_issue

cash_out_issue

payment_issue

other

------------------------------------------------

3. severity

Allowed

low

medium

high

critical

------------------------------------------------

4. department

Examples

dispute_resolution

fraud_team

merchant_support

payment_operations

customer_support

technical_support

------------------------------------------------

5. confidence

Return a value between 0 and 1.

------------------------------------------------

6. human_review_required

Return true if

- fraud suspected

- insufficient evidence

- high severity

- ambiguous complaint

Otherwise false.

------------------------------------------------

7. reason_codes

Return short codes explaining the decision.

Example

[
    "transaction_match",
    "amount_match",
    "completed_transfer"
]

------------------------------------------------

Customer Complaint

{state["complaint"]}

Complaint Analysis

{state["complaint_analysis"]}

Match Found

{state["match_found"]}

Relevant Transaction ID

{state["relevant_transaction_id"]}

Matched Transaction

{state["matched_transaction"]}

User Type

{state.get("user_type")}

Channel

{state.get("channel")}
"""

    result = structured_llm.invoke(prompt)

    if isinstance(result, BaseModel):
        result = result.model_dump()

    return {
        **state,

        "evidence_verdict": result["evidence_verdict"],

        "case_type": result["case_type"],

        "severity": result["severity"],

        "department": result["department"],

        "confidence": result["confidence"],

        "human_review_required": result["human_review_required"],

        "reason_codes": result["reason_codes"],
    }