# app/payments/analytics.py
from app.payments.db import load_payments

def financial_report():
    pays = load_payments()
    total = sum(p["amount"] for p in pays)
    return {
        "total_revenue": total,
        "payments_count": len(pays),
        "subs": sum(1 for p in pays if p["type"] == "subscription"),
        "vip": sum(1 for p in pays if p["type"] == "vip")
    }