from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.schemas import (
    AnalyzeTicketRequest,
    AnalyzeTicketResponse,
)

from app.graph.workflow import graph


app = FastAPI(
    title="QueueStorm Investigator",
    description="AI-powered investigation API",
    version="1.0.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post(
    "/analyze-ticket",
    response_model=AnalyzeTicketResponse,
    status_code=200,
)
async def analyze_ticket(request: AnalyzeTicketRequest):
    try:

        # Run LangGraph
        result = graph.invoke(
            request.model_dump()
        )

        # Return only the response schema
        return AnalyzeTicketResponse(
            ticket_id=result["ticket_id"],
            relevant_transaction_id=result["relevant_transaction_id"],
            evidence_verdict=result["evidence_verdict"],
            case_type=result["case_type"],
            severity=result["severity"],
            department=result["department"],
            agent_summary=result["agent_summary"],
            recommended_next_action=result["recommended_next_action"],
            customer_reply=result["customer_reply"],
            human_review_required=result["human_review_required"],
            confidence=result["confidence"],
            reason_codes=result["reason_codes"],
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
            },
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )