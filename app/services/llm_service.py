
import os
import time
import ollama

MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

client = ollama.Client(
    host=os.getenv("OLLAMA_HOST", "http://localhost:11434")
)


def generate_analysis(
    prompt,
    comparison_mode=False,
    num_predict=None
):
    if num_predict is None:
        num_predict = 1600 if comparison_mode else 1200

    start = time.perf_counter()

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": num_predict,
            "num_ctx": 4096,
        },
    )

    wall_time = time.perf_counter() - start
    message = response["message"]["content"]

    # Ollama reports durations in nanoseconds.
    def seconds(field):
        value = response.get(field, 0) or 0
        return value / 1_000_000_000

    prompt_tokens = response.get("prompt_eval_count", 0) or 0
    output_tokens = response.get("eval_count", 0) or 0
    prompt_time = seconds("prompt_eval_duration")
    generation_time = seconds("eval_duration")

    print("\n========== LLM PERFORMANCE ==========")
    print(f"[LLM] Model: {MODEL_NAME}")
    print(f"[LLM] Prompt characters: {len(prompt):,}")
    print(f"[LLM] Prompt tokens: {prompt_tokens}")
    print(f"[LLM] Output tokens: {output_tokens}")
    print(f"[LLM] Load time: {seconds('load_duration'):.2f}s")
    print(f"[LLM] Prompt evaluation: {prompt_time:.2f}s")
    print(f"[LLM] Token generation: {generation_time:.2f}s")
    print(f"[LLM] Total wall time: {wall_time:.2f}s")
    print(f"[LLM] Finish reason: {response.get('done_reason', 'unknown')}")

    if prompt_time > 0:
        print(f"[LLM] Prompt speed: {prompt_tokens / prompt_time:.2f} tokens/sec")

    if generation_time > 0:
        print(f"[LLM] Generation speed: {output_tokens / generation_time:.2f} tokens/sec")

    print("=====================================\n")

    return message
