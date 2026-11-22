import os

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")


def get_supabase_headers(access_token: str) -> dict:
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        raise RuntimeError("Supabase environment variables are missing.")

    return {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def verify_supabase_token(access_token: str) -> dict | None:
    headers = get_supabase_headers(access_token)

    response = requests.get(
        f"{SUPABASE_URL.rstrip('/')}/auth/v1/user",
        headers=headers,
        timeout=15,
    )

    if response.status_code == 401:
        return None

    response.raise_for_status()

    return response.json()
