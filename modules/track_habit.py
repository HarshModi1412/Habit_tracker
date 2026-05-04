import streamlit as st
from datetime import date
from utils import get_habits, get_daily, upsert_tracking

def show_track_page(user_id):
    st.title("Track Habit")

    selected_date = st.date_input("Select Date", date.today())

    st.divider()

    habits = get_habits(user_id)
    daily = get_daily(user_id, selected_date)

    daily_map = {d["habit_id"]: d["completed"] for d in daily}

    if not habits:
        st.warning("No habits found for this user.")
        return

    for habit in habits:
        habit_id = habit["id"]
        checked = daily_map.get(habit_id, False)

        col1, col2 = st.columns([4, 1])

        with col1:
            new_value = st.checkbox(
                habit["habit_name"],
                value=checked,
                key=f"{habit_id}_{selected_date}"
            )

        with col2:
            if new_value != checked:
                upsert_tracking(user_id, habit_id, selected_date, new_value)