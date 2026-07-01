# app/payments/perfile.py
from telegram import LabeledPrice
from app.utils.security import PAYMENT_PROVIDER
from app.payments.db import save_payment

def send_file_payment(update, context):
    prices = [LabeledPrice("پردازش یک فایل", 50000)]
    update.message.reply_invoice(
        title="پرداخت فایل",
        description="پردازش حرفه‌ای یک فایل",
        provider_token=PAYMENT_PROVIDER,
        currency="IRR",
        prices=prices,
        start_parameter="file_clean",
        payload="file_payment"
    )

def file_payment_success(update, context):
    u = update.message.from_user
    save_payment({"user": u.id, "amount": 50000, "type": "file"})
    context.user_data["paid_once"] = True
    update.message.reply_text("پرداخت موفق بود ✔ فایل را بفرست.")