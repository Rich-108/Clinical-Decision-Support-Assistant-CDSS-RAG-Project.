import os
from openai import OpenAI
from app.services.prompts import SYSTEM_PROMPT


# Read API key explicitly
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY not found. "
        "Make sure it is set in the .env file and load_dotenv() is called."
    )

# Initialize OpenAI client safely
client = OpenAI(api_key=api_key)


def generate_answer(query: str, evidence_chunks: list) -> str:
    """
    Generate a clinical answer strictly grounded in provided evidence.
    """

    # Evidence may be list of dicts (Phase-2)
    evidence_text = "\n\n".join(
        [e["text"] if isinstance(e, dict) else e for e in evidence_chunks]
    )

    prompt = f"""
CLINICAL EVIDENCE:
{evidence_text}

QUESTION:
{query}

INSTRUCTIONS:
- Answer ONLY using the clinical evidence above.
- Do NOT add external medical knowledge.
- If evidence is insufficient, say:
  "Information not available in the provided clinical guidelines."
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    answer = response.choices[0].message.content

    disclaimer = (
        "\n\n⚠️ Disclaimer: This response is based solely on the provided "
        "clinical guidelines and does not replace professional medical judgment."
    )

    return answer + disclaimer
