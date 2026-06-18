from app.services.yahoo_finance import get_company_data
from app.agents.metrics_agent import evaluate_metrics

data = get_company_data("NVDA")

print(
    evaluate_metrics(data)
)