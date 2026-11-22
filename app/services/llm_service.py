import os
import time
from groq import Groq

MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_analysis(
    prompt,
    comparison_mode=False,
    num_predict=None
):
    if num_predict is None:
        num_predict = 1600 if comparison_mode else 1200

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=num_predict,
        temperature=0.2,
    )

    wall_time = time.perf_counter() - start

    message = response.choices[0].message.content or ""

    prompt_tokens = response.usage.prompt_tokens if response.usage else 0
    output_tokens = response.usage.completion_tokens if response.usage else 0

    print("\n========== LLM PERFORMANCE ==========")
    print(f"[LLM] Provider: Groq")
    print(f"[LLM] Model: {MODEL_NAME}")
    print(f"[LLM] Prompt characters: {len(prompt):,}")
    print(f"[LLM] Prompt tokens: {prompt_tokens}")
    print(f"[LLM] Output tokens: {output_tokens}")
    print(f"[LLM] Total wall time: {wall_time:.2f}s")

    if wall_time > 0:
        print(f"[LLM] Overall speed: {(prompt_tokens + output_tokens) / wall_time:.2f} tokens/sec")

    print("=====================================\n")

    return message