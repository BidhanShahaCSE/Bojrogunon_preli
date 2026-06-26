import os
from typing import Optional, List, Dict, Any

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
# Structured Output Schemas
# ==========================================================


class Transaction(BaseModel):
    transaction_id: str
    timestamp: str
    type: str
    amount: float
    counterparty: str
    status: str


class ComplaintAnalysis(BaseModel):
    intent: str = Field(
        ...,
        description="Primary complaint intent."
    )

    summary: str = Field(
        ...,
        description="Short summary of the complaint."
    )

    amount: Optional[float] = Field(
        default=None,
        description="Mentioned transaction amount."
    )

    transaction_type: Optional[str] = Field(
        default=None,
        description="transfer/payment/cash_in/cash_out/etc."
    )

    time_reference: Optional[str] = Field(
        default=None,
        description="Time mentioned inside complaint."
    )

    counterparty: Optional[str] = Field(
        default=None,
        description="Receiver or merchant mentioned."
    )


class ComplaintAnalysisOutput(BaseModel):
    complaint_analysis: ComplaintAnalysis

    match_found: bool

    relevant_transaction_id: Optional[str] = None

    matched_transaction: Optional[Transaction] = None


# ==========================================================
# Structured LLM
# ==========================================================

structured_llm = llm.with_structured_output(
    ComplaintAnalysisOutput
)

# ==========================================================
# LangGraph Node
# ==========================================================


def complaint_analysis_node(
    state: Dict[str, Any],
) -> Dict[str, Any]:
    """
    LangGraph Node 1

    Responsibilities
    ----------------
    1. Understand customer complaint.
    2. Extract important entities.
    3. Compare complaint with transaction history.
    4. Find the most relevant transaction.
    5. Return structured output.

    This node DOES NOT determine

    - evidence_verdict
    - case_type
    - severity
    - department
    """

    complaint = state["complaint"]

    language = state.get("language", "en")

    transaction_history = state.get(
        "transaction_history",
        [],
    )

    prompt = f"""
You are an AI Complaint Investigation Assistant.

Your ONLY responsibilities are:

1. Read the customer complaint.

2. Understand it.

3. Extract

- complaint intent
- amount
- transaction type
- time reference
- counterparty

4. Compare the complaint with the supplied transaction history.

5. Identify the BEST matching transaction.

Rules

- If a matching transaction exists,
  return it.

- If no transaction matches,
  set

    match_found = false

    relevant_transaction_id = null

    matched_transaction = null

DO NOT

- classify complaint

- determine evidence_verdict

- determine case_type

- determine severity

- determine department

Complaint

{complaint}

Language

{language}

Transaction History

{transaction_history}
"""

    result: ComplaintAnalysisOutput = structured_llm.invoke(
        prompt
    )
    result = structured_llm.invoke(prompt)

    print(type(result))
    print(result)

    return {
        **state,

        "complaint_analysis": result["complaint_analysis"],

        "match_found": result["match_found"],

        "relevant_transaction_id": result["relevant_transaction_id"],

        "matched_transaction": result["matched_transaction"],
    }