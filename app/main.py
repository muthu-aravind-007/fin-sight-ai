from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.api.routes.analysis import router
from app.api.routes.compare import router as compare_router
from app.api.routes.earnings import router as earnings_router
from app.api.routes.portfolio import router as portfolio_router
from app.api.routes.transcript_summary import router as transcript_summary_router
from app.api.routes.multi_rag import router as multi_rag_router

app = FastAPI(title="FinSight AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Local React
        "https://your-vercel-url.vercel.app",  # Replace later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(compare_router)
app.include_router(earnings_router)
app.include_router(portfolio_router)
app.include_router(transcript_summary_router)
app.include_router(multi_rag_router)

@app.get("/")
def home():
    return {"message": "FinSight AI API Running"}