from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db, init_db
from .llm_agent import LLMAgent
from .query_runner import QueryRunner

app = FastAPI(title="BI Query Bot")

# Initialize LLM agent
llm_agent = LLMAgent()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/query", response_model=QueryResponse)
async def query_data(
    request: QueryRequest,
    session: AsyncSession = Depends(get_db)
):
    try:
        # Generate SQL query from natural language
        sql_query = await llm_agent.generate_sql_query(request.question)

        # Initialize query runner
        runner = QueryRunner(session)

        # Validate query
        if not runner.validate_query(sql_query):
            raise HTTPException(
                status_code=400,
                detail="Generated query contains unsafe operations"
            )

        # Execute query
        results = await runner.execute_safe_query(sql_query)

        return QueryResponse(
            sql_query=sql_query,
            results=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 