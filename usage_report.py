# app/users/usage_report.py
from app.users.db import get_user

def usage_report(uid):
    u = get_user(uid)
    status = "معمولی"
    if u["sub_active"]: status = "اشتراک فعال"
    if u["vip"]: status = "VIP"
    return f"📊 وضعیت شما:\nوضعیت: {status}\nامروز: {u['files_today']}\nاین ماه: {u['files_month']}"