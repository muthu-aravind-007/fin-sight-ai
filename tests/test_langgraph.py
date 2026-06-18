from app.graph.workflow import financial_graph

result = financial_graph.invoke(
    {
        "ticker": "NVDA"
    }
)

print(result)