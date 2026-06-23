def expand_query(question):

    question = question.lower()

    expansions = []

    if "ai" in question:

        expansions.extend([
            "artificial intelligence",
            "machine learning",
            "generative ai",
            "llm",
            "foundation model",
            "agentic ai",
            "copilot",
            "openai",
            "foundry"
        ])

    if any(
        x in question
        for x in [
            "infrastructure",
            "compute",
            "cloud",
            "capacity",
            "datacenter",
            "data center",
            "gpu"
        ]
    ):

        expansions.extend([
            "ai infrastructure",
            "gpu",
            "cpu",
            "compute",
            "capacity",
            "datacenter",
            "cloud",
            "azure",
            "training",
            "inference",
            "silicon",
            "networking"
        ])

    if "investment" in question:

        expansions.extend([
            "capital expenditure",
            "capex",
            "r&d",
            "research and development",
            "infrastructure spending",
            "talent investment"
        ])

    expanded_question = (
        question
        + " "
        + " ".join(expansions)
    )

    return expanded_question