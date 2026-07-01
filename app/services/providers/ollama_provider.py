import os
import ollama

client = ollama.Client(
    host=os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
    )
)

MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")


def generate(prompt, comparison_mode=False):

    num_predict = (
        650 if comparison_mode else 700
    )

    response = client.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": num_predict
        }
    )

    return response["message"]["content"]