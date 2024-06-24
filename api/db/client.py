from supabase import Client, create_client
from api.config import get_settings

settings = get_settings()


def create_supabase_client():
    supabase: Client = create_client(settings.supabase_url, settings.supabase_key)
    return supabase
