# src/crud.py
from utils import GRADES_FILE, log_action, ensure_files, is_safe_input


def _load_grades():
    ensure_files()
    grades = []
    with open(GRADES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 4:
                continue
            grade_id, student, subject, score = parts
            try:
                grade_id = int(grade_id)
                score = int(score)
            except ValueError:
                continue
            grades.append({
                "id": grade_id,
                "student": student,
                "subject": subject,
                "score": score
            })
    return grades


def _save_grades(grades):
    ensure_files()
    with open(GRADES_FILE, "w", encoding="utf-8") as f:
        for g in grades:
            f.write(f"{g['id']}|{g['student']}|{g['subject']}|{g['score']}\n")


def _generate_new_id(grades):
    if not grades:
        return 1
    return max(g["id"] for g in grades) + 1


def _input_score():
    value = input("Puntuación (0-100): ").strip()
    if not value.isdigit():
        print("La puntuación debe ser un número entero.")
        return None
    score = int(value)
    if score < 0 or score > 100:
        print("La puntuación debe estar entre 0 y 100.")
        return None
    return score


# --------- Operaciones para TEACHER ---------

def teacher_create_grade(current_user):
    grades = _load_grades()
    student = input("Usuario del estudiante (username): ").strip()
    subject = input("Materia: ").strip()

    # Validar entradas contra inyección o corrupción de archivo
    if not student or not subject:
        print("Campos vacíos no permitidos.")
        return

    if not is_safe_input(student) or not is_safe_input(subject):
        print("❌ Entrada no permitida (posible inyección).")
        return

    score = _input_score()
    if score is None:
        return

    new_id = _generate_new_id(grades)
    grades.append({
        "id": new_id,
        "student": student,
        "subject": subject,
        "score": score
    })
    _save_grades(grades)
    log_action(
        current_user["username"],
        f"creó calificación id={new_id} para {student} en {subject} con score={score}"
    )
    print("✔ Calificación creada correctamente.")


def teacher_view_all_grades(current_user):
    grades = _load_grades()
    if not grades:
        print("No hay calificaciones registradas.")
    else:
        print("\n=== Todas las calificaciones ===")
        for g in grades:
            print(f"ID:{g['id']} | Estudiante:{g['student']} | Materia:{g['subject']} | Score:{g['score']}")
    log_action(current_user["username"], "visualizó todas las calificaciones")


def teacher_update_grade(current_user):
    grades = _load_grades()
    if not grades:
        print("No hay calificaciones para actualizar.")
        return

    raw_id = input("ID de la calificación a actualizar: ").strip()
    if not raw_id.isdigit():
        print("ID inválido.")
        return

    if not is_safe_input(raw_id):
        print("ID no permitido (posible inyección).")
        return

    grade_id = int(raw_id)
    grade = next((g for g in grades if g["id"] == grade_id), None)
    if grade is None:
        print("No se encontró una calificación con ese ID.")
        return

    print(f"Calificación actual: Estudiante:{grade['student']} | Materia:{grade['subject']} | Score:{grade['score']}")
    new_score = _input_score()
    if new_score is None:
        return

    old_score = grade["score"]
    grade["score"] = new_score
    _save_grades(grades)
    log_action(
        current_user["username"],
        f"actualizó calificación id={grade_id} score {old_score} → {new_score}"
    )
    print("✔ Calificación actualizada correctamente.")


def teacher_delete_grade(current_user):
    grades = _load_grades()
    if not grades:
        print("No hay calificaciones para eliminar.")
        return

    raw_id = input("ID de la calificación a eliminar: ").strip()
    if not raw_id.isdigit():
        print("ID inválido.")
        return

    if not is_safe_input(raw_id):
        print("ID no permitido (posible inyección).")
        return

    grade_id = int(raw_id)

    grade = next((g for g in grades if g["id"] == grade_id), None)
    if grade is None:
        print("No se encontró una calificación con ese ID.")
        return

    grades = [g for g in grades if g["id"] != grade_id]
    _save_grades(grades)
    log_action(
        current_user["username"],
        f"eliminó calificación id={grade_id} de {grade['student']} en {grade['subject']}"
    )
    print("✔ Calificación eliminada correctamente.")


# --------- Operaciones para STUDENT ---------

def student_view_own_grades(current_user):
    grades = _load_grades()
    my_grades = [g for g in grades if g["student"] == current_user["username"]]

    if not my_grades:
        print("No tienes calificaciones registradas.")
    else:
        print("\n=== Mis calificaciones ===")
        for g in my_grades:
            print(f"ID:{g['id']} | Materia:{g['subject']} | Score:{g['score']}")

    log_action(current_user["username"], "visualizó sus propias calificaciones")
