from app.services.llm_service import generate_analysis

response = generate_analysis(
    "Give a short analysis of NVIDIA."
)

print(response)