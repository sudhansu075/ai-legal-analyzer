import os
from diskcache import Cache
from openai import OpenAI
import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
cache = Cache("cache")


def get_similar_safe_clause(clause_text: str):
    embeddings = OpenAIEmbeddings(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    db = Chroma(
        persist_directory="db",
        embedding_function=embeddings
    )

    results = db.similarity_search(clause_text, k=1)

    if not results:
        return None

    return results[0].page_content

def analyze_clause(clause_text: str):

    # 1. Check cache first
    if clause_text in cache:
        print("Returning cached result")
        return cache[clause_text]
    
    safe_clause = get_similar_safe_clause(clause_text)

    prompt = f"""
    You are a senior contract risk analyst.

    Here is a standard balanced clause:
    {safe_clause}

    Compare it with this uploaded clause:
    {clause_text}

    Explain:

    - summary
    - deviations from standard clause
    - risk_level (Low, Medium, High)
    - risk_reason
    - renegotiation_suggestion
    - one_sided (true/false)

    Respond strictly in JSON format.
    """

    try:
      response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
      )
    except Exception as e:
      return {"error": str(e)}  

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Model returned empty response")

    content = content.strip()

    # Remove markdown if present
    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    result = json.loads(content)

    cache[clause_text] = result

    return result