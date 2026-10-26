
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, SecretStr

from app.agent.analyst import analyze_question
from app.db.company_connections import test_company_connection


logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Data Analyst API",
    description="API for the AI Data Analyst Agent",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)



class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        description="Business question to ask about the database",
    )


class ConnectionTestRequest(BaseModel):
    host: str = Field(min_length=1, max_length=255)
    port: int = Field(default=5432, ge=1, le=65535)
    database_name: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    password: SecretStr


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "AI Data Analyst API",
    }


@app.post("/api/v1/ask")
def ask_question(request: AskRequest):
    try:
        return analyze_question(request.question)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Question analysis failed")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while analyzing the question.",
        )


@app.post("/api/v1/connections/test")
def test_connection(request: ConnectionTestRequest):
    try:
        connected = test_company_connection(
            username=request.username,
            password=request.password.get_secret_value(),
            host=request.host,
            port=request.port,
            database_name=request.database_name,
        )

        if not connected:
            raise HTTPException(
                status_code=400,
                detail="Database connection failed.",
            )

        return {
            "status": "success",
            "message": "Database connection successful.",
        }

    except HTTPException:
        raise

    except Exception:
        logger.exception("Company database connection test failed")
        raise HTTPException(
            status_code=400,
            detail=(
                "Database connection failed. "
                "Check the server terminal for diagnostic details."
            ),
        )
