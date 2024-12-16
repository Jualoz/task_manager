import streamlit as st
from components import auth, tasks
from db import init_db

# Verificar si el usuario está autenticado
def check_if_authenticated():
    if "user_id" not in st.session_state:
        return False
    return True

def main():
    init_db()
    if not check_if_authenticated():
        # Si no está autenticado, mostramos el formulario de login
        if auth.login():
            tasks.show_tasks()
    else:
        # Si está autenticado, mostramos las tareas
        tasks.show_tasks()

if __name__ == "__main__":
    main()
