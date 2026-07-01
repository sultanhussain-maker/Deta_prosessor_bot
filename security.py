# app/utils/security.py
import os

def env(key):
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Missing ENV: {key}")
    return val

TOKEN = env("TELEGRAM_BOT_TOKEN")
PAYMENT_PROVIDER = env("PAYMENT_PROVIDER")
WALLET = env("WALLET_ADDRESS")
SECRET_KEY = env("SECRET_KEY")
MAX_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
LANG_DEFAULT = os.getenv("LANG_DEFAULT", "fa")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")