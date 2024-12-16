
# Task Manager

Un gestor de tareas simple y funcional construido con Streamlit y SQLAlchemy para manejar tareas con soporte de autenticación, exportación/importación de datos y más.
## Características

- Gestión de Usuarios: Registro, inicio de sesión y cierre de sesión.

- Gestión de Tareas: Crear, editar, eliminar y marcar tareas como completadas.

- Exportación/Importación de Tareas: Exporta tareas a un archivo JSON o importa desde uno.

- Autenticación: Sistema de login que asegura que cada usuario gestione solo sus tareas.
## Instalacion

Clonar el repositorio:
```bash
    git clone https://github.com/Jualoz/task_manager.git
    cd gestor-tareas
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar la aplicación: 
```bash
streamlit run app.py
```

## Uso

- Registro: Ingresa tu nombre de usuario, correo electrónico y contraseña para registrarte.
- Inicio de Sesión: Accede con tu usuario y contraseña.
- Gestión de Tareas: 
    - Agrega nuevas tareas, edita o elimina las existentes.
    - Marca tareas como completadas.
- Exportar/Importar Tareas:
    - Exporta las tareas a un archivo JSON.
    - Importa tareas desde un archivo JSON.



## Ver Proyecto

Puedes ver el proyecto en accion en el link:

[Task Manager](https://jualoz-task-manager.streamlit.app)