import streamlit as st
from db import SessionLocal, db_functions
import json

def show_tasks():
    st.header("Task Manager")
    db = SessionLocal()
    
    """Función que muestra las tareas del usuario"""
    tasks = db_functions.get_tasks_by_user(db, st.session_state.user_id)
    
    # Manejador para almacenar la tarea en edición
    if "editing_task" not in st.session_state:
        st.session_state.editing_task = None

    if tasks:
        st.subheader("Pending Tasks")
        for task in tasks:
            if not task.completed:
                # Mostrar información de cada tarea
                task_expander = st.expander(f"Task: {task.title}")
                with task_expander:
                    st.write(f"Description: {task.description}")
                    st.write(f"Created on: {task.created_at}")
                    st.write(f"Status: {'Completed' if task.completed else 'Pending'}")
                    
                    col1, col2, col3 = st.columns(3)
                    # Botón para marcar como completado
                    with col1:
                        if st.button("Mark as Completed", key=f"complete_{task.id}"):
                            db_functions.update_task_status(db, task.id, True)
                            st.rerun()

                    # Botón para eliminar tarea
                    with col2:
                        if st.button("Delete Task", key=f"delete_{task.id}"):
                            db_functions.delete_task(db, task.id)
                            st.rerun()

                    # Botón para activar edición
                    with col3:
                        if st.button("Edit Task", key=f"edit_{task.id}"):
                            st.session_state.editing_task = task.id
                            st.rerun()
                    
                    # Si la tarea actual está en edición
                    if st.session_state.editing_task == task.id:
                        update_task_title = st.text_input("Edit Title", value=task.title, key=f"edit_title_{task.id}")
                        update_task_description = st.text_area("Edit Description", value=task.description, key=f"edit_desc_{task.id}")
                        
                        if st.button("Update Task", key=f"update_{task.id}"):
                            if update_task_title and update_task_description:
                                db_functions.update_task_details(db, task.id, update_task_title, update_task_description)
                                st.success(f"Task '{update_task_title}' updated successfully!")
                                st.session_state.editing_task = None  # Resetear edición
                                st.rerun()
                            else:
                                st.error("Both title and description are required for updating the task.")
        st.subheader("Completed Tasks")
        for task in tasks:
            if task.completed:
                # Mostrar información de cada tarea
                task_expander = st.expander(f"Task: {task.title}")
                with task_expander:
                    st.write(f"Description: {task.description}")
                    st.write(f"Created on: {task.created_at}")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("Mark as Pending", key=f"pending_{task.id}"):
                            db_functions.update_task_status(db, task.id, False)
                            st.rerun()
                    with col2:
                        if st.button("Delete Task", key=f"delete_{task.id}"):
                            db_functions.delete_task(db, task.id)
                            st.rerun()

    else:
        st.write("No tasks available. Create a new task.")

    # Importar los datos
    import_tasks_from_json()

    # Crear una nueva tarea
    st.subheader("Create a New Task")
    task_title = st.text_input("Task Title", key="task_title")
    task_description = st.text_area("Task Description", key="task_description")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        create_task_button = st.button("Create Task")
        if create_task_button:
            if task_title and task_description:
                db_functions.create_task(db, st.session_state.user_id, task_title, task_description)
                st.success(f"Task '{task_title}' created successfully!")
                st.rerun()
            else:
                st.error("Both task title and description are required.")
    with col2:
        export_tasks_to_json()
    with col3:
        if st.button("Logout"):
            # Cerrar sesión eliminando las claves relevantes de `st.session_state`
            st.session_state.clear()
            st.rerun()

def export_tasks_to_json():
    db = SessionLocal()
    tasks_data = db_functions.export_tasks(db, st.session_state.user_id)
    
    st.download_button(
        label="Export Tasks as JSON",
        data=tasks_data,
        file_name="tasks.json",
        mime="application/json"
    )

def import_tasks_from_json():
    db = SessionLocal()
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = []  # Lista de archivos ya procesados

    uploaded_file = st.file_uploader("Sube un archivo JSON", type=["json"], key="file_uploader")
        
    if uploaded_file is not None:
        # Verificar si el archivo ya fue procesado
        if uploaded_file.name not in st.session_state.processed_files:
            try:
                # Cargar y procesar los datos del archivo
                data = json.load(uploaded_file)

                for task_data in data:
                    title = task_data.get("title")
                    description = task_data.get("description")
                    completed = task_data.get("completed", False)

                    if title and description:
                        # Crear una nueva tarea en la base de datos
                        db_functions.create_task(db, st.session_state.user_id, title=title, description=description, completed=completed)
                    
                    st.success(f"Tasks from '{uploaded_file.name}' imported successfully!")

                    # Marcar el archivo como procesado
                    st.session_state.processed_files.append(uploaded_file.name)
                    st.rerun()
            except Exception as e:
                st.error(f"Error processing file '{uploaded_file.name}': {str(e)}")
        else:
            st.warning(f"The file '{uploaded_file.name}' has already been processed.")