import streamlit as st
from utils import get_habits, add_habit, delete_habit

def show_habit_editor(user_id):
    st.title("Habit Editor")

    st.subheader("Add New Habit")

    with st.form("add_habit"):
        name = st.text_input("Habit Name")
        weight = st.number_input("Weight", min_value=1, value=1)
        reason = st.text_input("Reason")

        if st.form_submit_button("Add Habit"):
            if name:
                add_habit(user_id, name, weight, reason)
                st.success("Habit added")
                st.rerun()

    st.divider()

    st.subheader("Existing Habits")

    habits = get_habits(user_id)

    if not habits:
        st.info("No habits found.")
        return

    for habit in habits:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(f"{habit['habit_name']} (Weight: {habit['weight']})")

        with col2:
            if st.button("Delete", key=habit["id"]):
                delete_habit(habit["id"])
                st.rerun()