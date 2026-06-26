import os
from typing import Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq

load_dotenv()

# ==========================================================
# LLM
# ==========================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    groq_api_key=os.getenv("GROQ_API_KEY"),
)

# ==========================================================
# Structured Output
# ==========================================================


class ResponseGenerationOutput(BaseModel):

    agent_summary: str = Field(
        ...,
        description="Short investigation summary for support agent."
    )

    recommended_next_action: str = Field(
        ...,
        description="Recommended next operational step."
    )

    customer_reply: str = Field(
        ...,
        description="Professional customer-facing response."
    )


structured_llm = llm.with_structured_output(
    ResponseGenerationOutput
)

# ==========================================================
# LangGraph Node
# ==========================================================


def response_generator_node(
    state: Dict[str, Any],
) -> Dict[str, Any]:
    """
    LangGraph Node 3

    Responsibilities

    - Generate agent summary

    - Generate recommended next action

    - Generate customer reply

    This node MUST NOT

    - change evidence_verdict

    - change severity

    - change department

    - change case_type

    It only communicates previous decisions.
    """

    prompt = f"""
You are an AI Customer Support Copilot.

The investigation has already been completed.

Your responsibility is ONLY to communicate the findings.

Generate

1. Agent Summary

Write a concise investigation summary for the support agent.

Maximum 3 sentences.

------------------------------------------------

2. Recommended Next Action

Recommend the immediate operational action.

Examples

- Verify recipient details.

- Escalate to Fraud Team.

- Initiate dispute workflow.

- Wait for settlement completion.

- Contact merchant support.

------------------------------------------------

3. Customer Reply

Write a professional, polite reply.

Rules

- Never promise refund.

- Never promise reversal.

- Never request PIN.

- Never request OTP.

- Never request password.

- Never claim investigation is complete.

- Never expose internal reasoning.

- Keep response reassuring.

Maximum 2-3 sentences.

------------------------------------------------

Complaint

{state["complaint"]}

Complaint Analysis

{state["complaint_analysis"]}

Relevant Transaction

{state["matched_transaction"]}

Evidence Verdict

{state["evidence_verdict"]}

Case Type

{state["case_type"]}

Severity

{state["severity"]}

Department

{state["department"]}

Human Review Required

{state["human_review_required"]}

Reason Codes

{state["reason_codes"]}
"""

    result = structured_llm.invoke(prompt)

    # Handle both dict and Pydantic model outputs
    if isinstance(result, BaseModel):
        result = result.model_dump()

    return {
        **state,

        "agent_summary": result["agent_summary"],

        "recommended_next_action": result["recommended_next_action"],

        "customer_reply": result["customer_reply"],
    }