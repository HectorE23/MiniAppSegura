# src/utils.py
import hashlib
import os
from datetime import datetime

USERS_FILE = "data/users.txt"
GRADES_FILE = "data/grades.txt"
LOG_FILE = "logs/log.txt"


def ensure_files():
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    for file in [USERS_FILE, GRADES_FILE, LOG_FILE]:
        if not os.path.exists(file):
            open(file, "w", encoding="utf-8").close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def log_action(user: str, action: str):
    ensure_files()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {user} | {action}\n")


def is_safe_input(text: str) -> bool:
    dangerous = [
        ";", "'", '"', "--", "|",
        " or 1=1", " drop ", " delete ", " insert ", " update ",
        "<script", "</script"
    ]

    text_lower = text.lower()
    for d in dangerous:
        if d in text_lower:
            return False
    return True
