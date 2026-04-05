import os
from pathlib import Path
from supabase import create_client, Client

# Load .env only in local development (file won't exist in GitHub Actions)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Safe debug — shows presence only, never leaks values
print(f"DEBUG URL present: {bool(SUPABASE_URL)}")
print(f"DEBUG KEY present: {bool(SUPABASE_KEY)}")


def get_supabase_client() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("❌ Supabase credentials still not loading")

    return create_client(SUPABASE_URL, SUPABASE_KEY)