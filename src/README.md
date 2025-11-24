# Mini App Segura – Sistema de Calificaciones (CLI)

Aplicación desarrollada para el curso **COMP 2700 – Cybersecurity** con el objetivo de implementar:

- Autenticación básica de usuarios (login & register)
- Manejo seguro de contraseñas usando hashing **SHA-256**
- Validación de entradas y protección contra inyección
- Control de acceso basado en roles (**teacher / student**)
- Operaciones **CRUD** sobre calificaciones (grades)
- Almacenamiento en archivos de texto (`.txt`)
- Registro de auditoría (**logging**)
- Principios de **Security by Design**

---

##  Integrante

- **Héctor Santos Rodríguez** – HSANTOS7789@interbayamon.edu

------------------------------------------------------------------------------------------------------------------------------------------------

##  Estructura del Proyecto

```text
MiniAppSegura/
│
├── src/
│   ├── main.py       # Menú principal y flujo general de la app
│   ├── auth.py       # Registro, login, hashing, validaciones
│   ├── crud.py       # Operaciones CRUD para calificaciones (grades)
│   └── utils.py      # Funciones auxiliares (hashing, logs, validación, paths)
│
├── data/
│   ├── users.txt     # Usuarios registrados: username | password_hash | role
│   └── grades.txt    # Calificaciones: id | student | subject | score
│
├── logs/
│   └── log.txt       # Acciones
│
├── docs/
│   ├── threat_model.pdf        # Diagrama del Threat Model
│   ├── pip_audit_result.pdf    # Resultado del comando `pip-audit`
│   └── informe.pdf             # Informe final
│
└── README.md
