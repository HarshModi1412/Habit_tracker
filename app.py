import streamlit as st
from utils import get_users

# Import pages
from modules.summary import show_summary_page   # ✅ NEW (correct import)
from modules.track_habit import show_track_page
from modules.habit_editor import show_habit_editor
from modules.Analysis import show_summary_page as show_analysis_page
from modules.rewards import show_rewards_page

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Habit Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ LOAD USERS ------------------
users = get_users()

if not users:
    st.error("No users found in database.")
    st.stop()

user_dict = {u["name"]: u["id"] for u in users}

# ------------------ SIDEBAR ------------------
st.sidebar.title("Settings")

selected_user_name = st.sidebar.selectbox(
    "Select User",
    list(user_dict.keys())
)

user_id = user_dict[selected_user_name]

st.sidebar.divider()

# Navigation (Summary added at top)
page = st.sidebar.radio(
    "Navigation",
    ["Summary", "Track Habit", "Habit Editor", "Analysis", "Rewards"]
)

# ------------------ ROUTING ------------------
if page == "Summary":
    show_summary_page(user_id)

elif page == "Track Habit":
    show_track_page(user_id)

elif page == "Habit Editor":
    show_habit_editor(user_id)

elif page == "Analysis":
    show_analysis_page(user_id)

elif page == "Rewards":
    show_rewards_page(user_id)