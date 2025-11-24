# src/main.py
from auth import register_user, login_user
from utils import ensure_files
from crud import (
    teacher_create_grade,
    teacher_view_all_grades,
    teacher_update_grade,
    teacher_delete_grade,
    student_view_own_grades,
)

def show_main_menu():
    print("\n=== Mini App Segura - Calificaciones ===")
    print("1) Registrarse")
    print("2) Iniciar sesión")
    print("3) Salir")

def teacher_menu(current_user):
    while True:
        print("\n=== Menú Teacher ===")
        print("1) Crear calificación")
        print("2) Ver todas las calificaciones")
        print("3) Actualizar calificación")
        print("4) Eliminar calificación")
        print("5) Cerrar sesión")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            teacher_create_grade(current_user)
        elif opcion == "2":
            teacher_view_all_grades(current_user)
        elif opcion == "3":
            teacher_update_grade(current_user)
        elif opcion == "4":
            teacher_delete_grade(current_user)
        elif opcion == "5":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida.")

def student_menu(current_user):
    while True:
        print("\n=== Menú Student ===")
        print("1) Ver mis calificaciones")
        print("2) Cerrar sesión")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            student_view_own_grades(current_user)
        elif opcion == "2":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida.")

def main():
    ensure_files()

    while True:
        show_main_menu()
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            username = input("Nuevo usuario: ").strip()
            password = input("Nueva contraseña: ").strip()
            print("Rol disponible: teacher / student")
            role = input("Rol: ").strip().lower()

            ok, msg = register_user(username, password, role)
            print(msg)

        elif opcion == "2":
            username = input("Usuario: ").strip()
            password = input("Contraseña: ").strip()

            user = login_user(username, password)
            if user is None:
                print("Usuario o contraseña incorrectos.")
            else:
                print(f"\nBienvenido, {user['username']} ({user['role']})")
                if user["role"] == "teacher":
                    teacher_menu(user)
                else:
                    student_menu(user)

        elif opcion == "3":
            print("Saliendo de la aplicación...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
