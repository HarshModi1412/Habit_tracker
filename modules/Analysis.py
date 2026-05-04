import streamlit as st
import pandas as pd
from utils import get_habits, get_all_daily

def show_summary_page(user_id):
    st.title("Summary")

    # ---------- LOAD DATA ----------
    habits = get_habits(user_id)
    daily = get_all_daily(user_id)

    if not habits or not daily:
        st.warning("Not enough data.")
        return

    habits_df = pd.DataFrame(habits)[["id", "habit_name", "weight"]]
    daily_df = pd.DataFrame(daily)[["habit_id", "date", "completed"]]

    daily_df["completed"] = daily_df["completed"].astype(int)

    # ---------- MERGE ----------
    df = daily_df.merge(habits_df, left_on="habit_id", right_on="id")

    # ---------- SCORE ----------
    df["score"] = df["completed"] * df["weight"]

    # ===============================
    # 📊 1. OVERALL SCORE
    # ===============================
    overall = df.groupby("date")["score"].sum().reset_index()
    overall = overall.sort_values("date")

    st.subheader("Overall Score Trend")
    st.line_chart(overall.set_index("date"))

    st.divider()

    # ===============================
    # 📊 2. HABIT-SPECIFIC TREND
    # ===============================
    habit_list = df["habit_name"].unique().tolist()

    selected_habit = st.selectbox("Select Habit", habit_list)

    habit_df = df[df["habit_name"] == selected_habit]

    habit_summary = habit_df.groupby("date")["score"].sum().reset_index()
    habit_summary = habit_summary.sort_values("date")

    st.subheader(f"{selected_habit} Trend")
    st.line_chart(habit_summary.set_index("date"))

    # ---------- OPTIONAL TABLE ----------
    with st.expander("View Data"):
        st.dataframe(habit_summary, use_container_width=True)