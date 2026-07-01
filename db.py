# app/users/db.py
import json, os
DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    return json.load(open(DB_FILE))

def save_db(db):
    json.dump(db, open(DB_FILE, "w"), indent=2)

def get_user(uid):
    db = load_db()
    return db.get(str(uid), {
        "sub_active": False,
        "vip": False,
        "files_today": 0,
        "files_month": 0,
        "admin": False
    })

def update_user(uid, data):
    db = load_db()
    db[str(uid)] = data
    save_db(db)