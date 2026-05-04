import streamlit as st
from supabase import create_client

# -------- TEMP CONFIG (replace later with st.secrets) --------
SUPABASE_URL = "https://qaxczmnhygjrletdookk.supabase.co"
SUPABASE_KEY = "sb_publishable_BpjumdKuYgahI261RSlPcw_5ATBrq6f"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_client()