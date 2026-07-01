# app/payments/db.py
import json, os
PAY_DB = "payments.json"

def load_payments():
    if not os.path.exists(PAY_DB): return []
    return json.load(open(PAY_DB))

def save_payment(p):
    pays = load_payments()
    pays.append(p)
    json.dump(pays, open(PAY_DB, "w"), indent=2)