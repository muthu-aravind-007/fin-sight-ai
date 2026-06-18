from fastapi import FastAPI

from app.api.routes.analysis import router
from app.api.routes.compare import router as compare_router
from app.api.routes.earnings import router as earnings_router
from app.api.routes.portfolio import router as portfolio_router

app = FastAPI(
    title="FinSight AI"
)

app.include_router(router)

app.include_router(compare_router)

app.include_router(earnings_router)

app.include_router(portfolio_router)


@app.get("/")
def home():
    return {
        "message": "FinSight AI API Running"
    }