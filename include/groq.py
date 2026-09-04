import httpx
import os
from dotenv import load_dotenv
from include.discord import send_to_discord

load_dotenv()

GROQ_API_URL = os.getenv("GROQ_API_URL") or "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("API_KEY")
AI_MODEL = os.getenv("AI_MODEL") or "openai/gpt-oss-120b"

def call_groq(commits: list) -> str:
    url = GROQ_API_URL
    api = API_KEY
    model = AI_MODEL

    if not api:
        err_msg = "API key cannot be found"
        
        send_to_discord(err_msg + ' @everyone')
        raise ValueError(err_msg)

    headers = {
        "Authorization": f"Bearer {api}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Tu es un Manager de stand-up trash et cynique. Sans pitié. Tu veux à tout prix me faire détester mon job, tu n'es pas prédictible, je suis sous payé, et tu es tétu. Tu n'as aucun but particulier, tu veux juste me faire chier. Et tu parles de façon tres courte, 2 lignes max, souvent tu aimes crier et parler comme un alcoolique colérique et tu es explosif de façon unexpected."},
            {"role": "user", "content": f"Roast ces commits : {commits[:5]}. PRECISION: ne roast pas les commits 1 par 1"}
        ]
    }

    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text
        try:
            error_json = e.response.json()
            if "error" in error_json and "message" in error_json["error"]:
                error_detail = error_json["error"]["message"]
        except Exception:
            pass
        raise RuntimeError(f"Erreur API Groq ({e.response.status_code}) pour le modèle '{model}' : {error_detail}") from None

    return response.json()["choices"][0]["message"]["content"]
