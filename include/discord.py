import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_to_discord(
    message: str
) -> None:
    webhook_url = WEBHOOK_URL


    payload = {
        "content": message
    }

    try:
        response = httpx.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except httpx.HTTPStatusError as e:
        print(f"[Discord Webhook] HTTP Error {e.response.status_code}: {e.response.text}")
        return False
    except httpx.RequestError as e:
        print(f"[Discord Webhook] Connexion Error: {e}")
        return False

