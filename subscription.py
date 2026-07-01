# app/payments/subscription.py
from telegram import LabeledPrice
from app.utils.security import PAYMENT_PROVIDER
from app.users.db import get_user, update_user
from app.payments.db import save_payment

def send_subscription(update, context):
    prices = [LabeledPrice("اشتراک ماهانه", 3000000)]
    update.message.reply_invoice(
        title="اشتراک ماهانه",
        description="پردازش نامحدود + گزارش حرفه‌ای",
        provider_token=PAYMENT_PROVIDER,
        currency="IRR",
        prices=prices,
        start_parameter="monthly_sub",
        payload="subscription_payment"
    )

def subscription_success(update, context):
    u = update.message.from_user
    user = get_user(u.id)
    user["sub_active"] = True
    update_user(u.id, user)
    save_payment({"user": u.id, "amount": 3000000, "type": "subscription"})
    update.message.reply_text("اشتراک فعال شد ✔")