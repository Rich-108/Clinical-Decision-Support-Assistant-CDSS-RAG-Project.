import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.2:1b"  # 🚀 Use the 1B model you already have

def generate_answer(question: str, evidence: list) -> str:
    if not evidence:
        return "No clinical evidence available."

    # Combine text from your search results
    context = "\n\n".join([f"Source: {e['text']}" for e in evidence])

    # Llama 3.2 Prompt Format
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
Answer the question strictly using the provided clinical evidence. 
If the information is not there, say "Not found in guidelines."<|eot_id|>
<|start_header_id|>user<|end_header_id|>
Evidence:
{context}

Question:
{question}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_ctx": 2048
            }
        },
        timeout=300
    )

    response.raise_for_status()
    return response.json()["response"].strip()