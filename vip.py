# app/payments/vip.py
from telegram import LabeledPrice
from app.utils.security import PAYMENT_PROVIDER
from app.users.db import get_user, update_user
from app.payments.db import save_payment

def send_vip_payment(update, context):
    prices = [LabeledPrice("VIP فایل‌های حجیم", 150000)]
    update.message.reply_invoice(
        title="VIP",
        description="پردازش فایل‌های حجیم تا 500MB",
        provider_token=PAYMENT_PROVIDER,
        currency="IRR",
        prices=prices,
        start_parameter="vip_clean",
        payload="vip_payment"
    )

def vip_payment_success(update, context):
    u = update.message.from_user
    user = get_user(u.id)
    user["vip"] = True
    update_user(u.id, user)
    save_payment({"user": u.id, "amount": 150000, "type": "vip"})
    update.message.reply_text("VIP فعال شد ✔")