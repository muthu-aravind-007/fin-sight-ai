import os
import ollama

client = ollama.Client(
    host=os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
    )
)

def generate_analysis(
    prompt,
    comparison_mode=False
):

    num_predict = (
        650
        if comparison_mode
        else 700
    )

    response = client.chat(
        model="qwen2.5:7b",
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