from app.services.llm_service import generate_analysis
from app.prompts.earnings_prompt import build_earnings_prompt


def analyze_earnings(transcript):

    prompt = build_earnings_prompt(
        transcript
    )

    analysis = generate_analysis(
        prompt
    )

    return {
        "analysis": analysis
    }