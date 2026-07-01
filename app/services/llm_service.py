import os

from services.providers import (
    ollama_provider,
    groq_provider
)

PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "ollama"
)


def generate_analysis(
    prompt,
    comparison_mode=False
):

    if PROVIDER == "ollama":
        return ollama_provider.generate(
            prompt,
            comparison_mode
        )

    elif PROVIDER == "groq":
        return groq_provider.generate(
            prompt,
            comparison_mode
        )

    else:
        raise ValueError(
            f"Unsupported provider: {PROVIDER}"
        )