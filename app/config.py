import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing environment variables: SUPABASE_URL, SUPABASE_KEY"
    )
    
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) # shared client across the app