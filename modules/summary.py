import streamlit as st
import pandas as pd
from datetime import date
from utils import get_habits, get_all_daily, get_rewards

from PIL import Image, ImageOps
import requests
from io import BytesIO


# =========================
# IMAGE PROGRESS FUNCTION
# =========================
from PIL import ImageFilter

def get_progress_image(image_url, progress):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # Create blurred version
        blurred = img.filter(ImageFilter.GaussianBlur(radius=10))

        w, h = img.size
        reveal_h = int(h * progress)

        # Take sharp (original) bottom part
        clear_part = img.crop((0, h - reveal_h, w, h))

        # Paste sharp part onto blurred image
        blurred.paste(clear_part, (0, h - reveal_h))

        return blurred

    except Exception as e:
        print("Image error:", e)
        return None


# =========================
# CUSTOM PROGRESS BAR
# =========================
def render_progress_bar(progress, width=250):
    percent = int(progress * 100)

    color = (
        "#4CAF50" if progress > 0.7
        else "#FFA500" if progress > 0.3
        else "#FF4B4B"
    )

    st.markdown(
        f"""
        <div style="width:{width}px">
            <div style="background-color:#2e2e2e; border-radius:8px;">
                <div style="
                    width:{percent}%;
                    background-color:{color};
                    height:10px;
                    border-radius:8px;">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# MAIN SUMMARY PAGE
# =========================
def show_summary_page(user_id):
    st.title("Summary")

    habits = get_habits(user_id)
    daily = get_all_daily(user_id)
    rewards = get_rewards(user_id)

    if not habits:
        st.warning("No habits found.")
        return

    habits_df = pd.DataFrame(habits)[["id", "habit_name", "weight", "reason"]]

    # ---------- DAILY DATA ----------
    if daily:
        daily_df = pd.DataFrame(daily)[["habit_id", "date", "completed"]]
        daily_df["date"] = pd.to_datetime(daily_df["date"])
        daily_df["completed"] = daily_df["completed"].astype(int)

        df = daily_df.merge(habits_df, left_on="habit_id", right_on="id")
        df["score"] = df["completed"] * df["weight"]
    else:
        df = pd.DataFrame()

    today = pd.to_datetime(date.today())

    # =========================
    # 🎯 REWARDS
    # =========================
    st.subheader("🎯 Rewards")

    if rewards and not df.empty:
        rewards_df = pd.DataFrame(rewards)

        cols = st.columns(4)  # 🔥 balanced for 250px

        for i, r in enumerate(rewards_df.itertuples()):
            col = cols[i % 4]

            start_date = pd.to_datetime(r.start_date)
            target = r.value

            temp_df = df[df["date"] >= start_date]

            # Habit-specific vs Overall
            if pd.notna(r.habit_id):
                temp_df = temp_df[temp_df["habit_id"] == r.habit_id]

            current_score = temp_df["score"].sum()
            progress = min(current_score / target, 1.0) if target else 0

            with col:
                if r.image_url:
                    img = get_progress_image(r.image_url, progress)
                    if img:
                        st.image(img, width=250)

                st.caption(r.reward_name)

                # 🔥 Custom aligned progress bar
                render_progress_bar(progress, width=250)

                st.caption(f"{int(progress * 100)}% complete")

    else:
        st.info("No rewards available.")

    st.divider()

    # =========================
    # ⚠️ FOCUS INSIGHT
    # =========================
    st.subheader("⚠️ Focus")

    issue_found = False

    if not df.empty:
        for habit in habits_df.itertuples():
            h_df = df[df["habit_id"] == habit.id]

            if h_df.empty:
                continue

            last_done = h_df[h_df["completed"] == 1]["date"]

            if last_done.empty:
                days_missed = 999
            else:
                days_missed = (today - last_done.max()).days

            if days_missed >= 3:
                st.warning(
                    f"You are not focusing on ***{habit.habit_name}***.\n\n"
                    f"Because I remember you said:\n\n"
                    f"***{habit.reason}***"
                )
                issue_found = True
                break

    if not issue_found:
        st.success("You are doing good. Keep it up.")

    st.divider()

    # =========================
    # 📊 OVERALL TREND
    # =========================
    st.subheader("📊 Overall Trend")

    if not df.empty:
        overall = df.groupby("date")["score"].sum().reset_index()
        overall = overall.sort_values("date")

        st.line_chart(overall.set_index("date"))
    else:
        st.info("No data yet.")
