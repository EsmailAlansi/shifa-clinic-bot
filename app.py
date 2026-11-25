"""FastAPI Web Application for Al-Shifa Clinic AI Assistant."""
import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from openai import APIError, RateLimitError
from pydantic import BaseModel, Field

from bot import CONTACT, MODEL, ask

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Al-Shifa Clinic AI Assistant",
    description="Interactive AI Assistant answering patient inquiries for Al-Shifa Clinic",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    answer: str
    model: str


@app.get("/")
async def index():
    """Serve the web chat interface."""
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
async def health():
    """Health check endpoint returning service status and model."""
    return {"status": "ok", "model": MODEL}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Receive patient questions and return bot answers."""
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Please enter a valid question.")

    try:
        answer, _ = await asyncio.to_thread(ask, question)
        if not answer:
            answer = f"عذراً، لم أتمكن من توليد إجابة الآن. يمكنك التواصل معنا على {CONTACT}."
        return ChatResponse(answer=answer, model=MODEL)
    except RateLimitError:
        logger.warning("OpenRouter rate limit reached")
        raise HTTPException(
            status_code=429,
            detail="Rate limit reached on the free tier. Please wait a moment and try again.",
        )
    except APIError as exc:
        logger.error("OpenRouter API error: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Unable to reach AI service at this moment. Please try again shortly.",
        )
    except Exception as exc:
        logger.exception("Unexpected error in /api/chat: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
