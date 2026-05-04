import streamlit as st
import uuid
from datetime import date
from db import supabase
from utils import get_habits, add_reward

def show_rewards_page(user_id):
    st.title("Rewards Setup")

    # ---------- LOAD HABITS ----------
    habits = get_habits(user_id)

    if not habits:
        st.warning("No habits found. Create habits first.")
        return

    habit_map = {h["habit_name"]: h["id"] for h in habits}

    # Add Overall option
    options = ["Overall"] + list(habit_map.keys())

    # ---------- FORM ----------
    with st.form("reward_form"):

        reward_name = st.text_input("Reward Name")

        duration = st.number_input("Duration (days)", min_value=1, value=7)

        target_value = st.number_input("Target Score", min_value=1, value=10)

        selected_option = st.selectbox("Select Category", options)

        uploaded_file = st.file_uploader(
            "Upload Reward Image",
            type=["png", "jpg", "jpeg"]
        )

        submit = st.form_submit_button("Save Reward")

        if submit:
            if not reward_name:
                st.error("Reward name required")
                return

            # ---------- MAP HABIT ----------
            if selected_option == "Overall":
                habit_id = None
            else:
                habit_id = habit_map[selected_option]

            image_url = None

            # ---------- IMAGE UPLOAD ----------
            if uploaded_file:
                file_bytes = uploaded_file.read()
                file_name = f"{uuid.uuid4()}_{uploaded_file.name}"

                supabase.storage.from_("habit-images").upload(
                    file_name,
                    file_bytes
                )

                image_url = supabase.storage.from_("habit-images").get_public_url(file_name)

            # ---------- INSERT ----------
            add_reward({
                "reward_name": reward_name,
                "duration": duration,
                "value": target_value,     # mapped to your DB
                "habit_id": habit_id,      # NULL = Overall
                "user_id": user_id,
                "image_url": image_url,
                "start_date": str(date.today())
            })

            st.success("Reward saved successfully")
            st.rerun()