# app/users/limits.py
from app.users.db import get_user, update_user

DAILY_LIMIT = 10
MONTHLY_LIMIT = 200

def check_limits(uid):
    u = get_user(uid)
    if u["sub_active"] or u["vip"]:
        return True
    if u["files_today"] >= DAILY_LIMIT: return False
    if u["files_month"] >= MONTHLY_LIMIT: return False
    return True

def increase_usage(uid):
    u = get_user(uid)
    u["files_today"] += 1
    u["files_month"] += 1
    update_user(uid, u)