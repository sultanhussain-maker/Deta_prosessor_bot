from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import InputFile
from io import BytesIO
import pandas as pd

from app.utils.security import TOKEN, MAX_SIZE_MB, LANG_DEFAULT
from app.utils.languages import LANG
from app.core.cleaner import clean_dataframe
from app.core.report import generate_report
from app.core.pdfgen import generate_pdf
from app.core.watermark import add_watermark_excel
from app.users.limits import check_limits, increase_usage
from app.users.usage_report import usage_report
from app.payments.perfile import send_file_payment, file_payment_success
from app.payments.subscription import send_subscription, subscription_success
from app.payments.vip import send_vip_payment, vip_payment_success

def start(update, context):
    update.message.reply_text(LANG[LANG_DEFAULT]["start"])

def usage_cmd(update, context):
    uid = update.message.from_user.id
    update.message.reply_text(usage_report(uid))

def handle_file(update, context):
    uid = update.message.from_user.id
    doc = update.message.document
    file = doc.get_file()
    file_bytes = file.download_as_bytearray()

    if len(file_bytes) > MAX_SIZE_MB * 1024 * 1024:
        update.message.reply_text(LANG[LANG_DEFAULT]["error_size"])
        return

    if not check_limits(uid):
        update.message.reply_text("❌ محدودیت مصرف شما تمام شده است.")
        return

    ext = doc.file_name.split(".")[-1].lower()
    if ext in ["csv", "txt"]:
        df = pd.read_csv(BytesIO(file_bytes))
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(BytesIO(file_bytes))
    else:
        update.message.reply_text(LANG[LANG_DEFAULT]["error_format"])
        return

    df = clean_dataframe(df)
    df = add_watermark_excel(df, "DataCleaner Pro")
    report = generate_report(df)
    pdf_file = generate_pdf(report)

    excel_out = BytesIO()
    df.to_excel(excel_out, index=False)
    excel_out.seek(0)

    increase_usage(uid)

    update.message.reply_text(report)
    update.message.reply_document(InputFile(excel_out, filename="cleaned_" + doc.file_name))
    update.message.reply_document(InputFile(pdf_file, filename="report.pdf"))

def payment_router(update, context):
    payload = update.message.successful_payment.invoice_payload
    if payload == "file_payment":
        file_payment_success(update, context)
    elif payload == "subscription_payment":
        subscription_success(update, context)
    elif payload == "vip_payment":
        vip_payment_success(update, context)

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("usage", usage_cmd))
    dp.add_handler(CommandHandler("buy_file", send_file_payment))
    dp.add_handler(CommandHandler("buy_sub", send_subscription))
    dp.add_handler(CommandHandler("buy_vip", send_vip_payment))

    dp.add_handler(MessageHandler(Filters.successful_payment, payment_router))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()
    updater.idle()