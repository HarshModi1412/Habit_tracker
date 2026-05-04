from db import supabase


# =========================
# CORE EXECUTOR
# =========================
def execute(query):
    try:
        res = query.execute()
        return res.data if res.data else []
    except Exception as e:
        print("Supabase Error:", e)
        return []


# =========================
# USERS
# =========================
def get_users():
    return execute(
        supabase.table("users").select("*")
    )


# =========================
# HABITS
# =========================
def get_habits(user_id):
    return execute(
        supabase.table("habits")
        .select("*")
        .eq("user_id", user_id)
    )


def add_habit(user_id, name, weight, reason):
    execute(
        supabase.table("habits").insert({
            "user_id": user_id,
            "habit_name": name,
            "weight": weight,
            "reason": reason
        })
    )


def delete_habit(habit_id):
    execute(
        supabase.table("habits")
        .delete()
        .eq("id", habit_id)
    )


# =========================
# DAILY TRACKING
# =========================
def get_daily(user_id, selected_date):
    return execute(
        supabase.table("daily_tracking")
        .select("*")
        .eq("user_id", user_id)
        .eq("date", str(selected_date))
    )


def get_all_daily(user_id):
    return execute(
        supabase.table("daily_tracking")
        .select("*")
        .eq("user_id", user_id)
    )


def upsert_tracking(user_id, habit_id, selected_date, completed):
    execute(
        supabase.table("daily_tracking").upsert(
            {
                "user_id": user_id,
                "habit_id": habit_id,
                "date": str(selected_date),
                "completed": completed
            },
            on_conflict="user_id,habit_id,date"
        )
    )


# =========================
# REWARDS
# =========================
def add_reward(data):
    execute(
        supabase.table("rewards").insert(data)
    )


def get_rewards(user_id):
    return execute(
        supabase.table("rewards")
        .select("*")
        .eq("user_id", user_id)
    )