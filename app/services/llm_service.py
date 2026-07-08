import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")

if LLM_PROVIDER == "groq":
    from groq import Groq

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

else:
    import ollama

    client = ollama.Client(
        host=os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )
    )


def generate_analysis(prompt, comparison_mode=False):

    num_predict = (
        650
        if comparison_mode
        else 700
    )

    if LLM_PROVIDER == "groq":

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=num_predict
        )

        return response.choices[0].message.content

    else:

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