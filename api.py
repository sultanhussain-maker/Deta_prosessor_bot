from flask import Flask, request, jsonify
from io import BytesIO
import pandas as pd

from app.core.cleaner import clean_dataframe
from app.core.report import generate_report
from app.cache.redis_cache import get_cached_report, set_cached_report
from app.monitoring.metrics import track_request, metrics_response

app = Flask(__name__)

@app.route("/api/process", methods=["POST"])
@track_request
def api_process():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "فایل ارسال نشده"}), 400

    ext = file.filename.split(".")[-1].lower()
    content = file.read()

    cached = get_cached_report(content)
    if cached:
        return jsonify({"status": "ok", "cached": True, "report": cached})

    if ext in ["csv", "txt"]:
        df = pd.read_csv(BytesIO(content))
    elif ext in ["xls", "xlsx"]:
        df = pd.read_excel(BytesIO(content))
    else:
        return jsonify({"error": "فرمت پشتیبانی نمی‌شود"}), 400

    df = clean_dataframe(df)
    report = generate_report(df)
    set_cached_report(content, report)

    return jsonify({"status": "ok", "cached": False, "report": report})

@app.route("/metrics")
def metrics():
    return metrics_response()