import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env explicitly
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG URL:", SUPABASE_URL)
print("DEBUG KEY:", SUPABASE_KEY)


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("❌ Supabase credentials still not loading")

    return create_client(SUPABASE_URL, SUPABASE_KEY)