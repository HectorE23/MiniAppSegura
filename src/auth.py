# src/auth.py
from utils import (
    USERS_FILE,
    hash_password,
    log_action,
    ensure_files,
    is_safe_input,
)


def user_exists(username: str) -> bool:
    ensure_files()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 3:
                continue
            if parts[0] == username:
                return True
    return False


def register_user(username: str, password: str, role: str) -> tuple[bool, str]:
    ensure_files()

    # ⚠️ VALIDACIÓN DE SEGURIDAD (PRIMERO)
    if not is_safe_input(username):
        return False, "Entrada de usuario no permitida (posible inyección)."

    # ⚠️ VALIDACIÓN DE FORMATO (DESPUÉS)
    if len(username) < 3 or len(username) > 30:
        return False, "El usuario debe tener entre 3 y 30 caracteres."

    if " " in username:
        return False, "El usuario no puede tener espacios."

    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."

    if role not in ("teacher", "student"):
        return False, "El rol debe ser 'teacher' o 'student'."

    if user_exists(username):
        return False, "Ese usuario ya existe."

    # Guardar usuario
    pwd_hash = hash_password(password)
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username}|{pwd_hash}|{role}\n")

    log_action(username, f"registro como {role}")
    return True, "Usuario registrado correctamente."


def login_user(username: str, password: str):
    ensure_files()

    # Bloquear intentos raros antes de intentar login
    if not is_safe_input(username):
        log_action(username, "login bloqueado (posible inyección)")
        return None

    pwd_hash = hash_password(password)

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 3:
                continue
            stored_username, stored_hash, stored_role = parts

            if stored_username == username and stored_hash == pwd_hash:
                log_action(username, "login exitoso")
                return {"username": stored_username, "role": stored_role}

    log_action(username, "login fallido")
    return None
