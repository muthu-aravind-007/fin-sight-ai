def build_rag_prompt(
    context,
    question
):

    return f"""
You are a professional financial analyst.

Use ONLY the context below to answer
the question.

Context:
{context}

Question:
{question}

Instructions:

1. Answer based only on the context.
2. Do not make up information.
3. If the answer is not present,
   say "Information not found in transcript."
4. Quote important evidence when useful.

Provide:

- Answer
- Key Evidence
- Investment Relevance
"""