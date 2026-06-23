import ollama

def generate_analysis(
    prompt,
    comparison_mode=False
):

    if comparison_mode:
        num_predict = 650
    else:
        num_predict = 700

    response = ollama.chat(
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