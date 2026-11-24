from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.analysis import router
from app.api.routes.compare import router as compare_router
from app.api.routes.earnings import router as earnings_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.transcript_summary import router as transcript_summary_router
from app.api.routes.reports import router as reports_router

from app.api.routes.multi_rag import (
    router as multi_rag_router
)

app = FastAPI(
    title="FinSight AI"
)

app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://fin-sight-ai-beta.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(compare_router)
app.include_router(earnings_router)
app.include_router(portfolio_router)
app.include_router(transcript_summary_router)
app.include_router(multi_rag_router)
app.include_router(reports_router)


@app.get("/")
def home():
    return {
        "message": "FinSight AI API Running"
    }
