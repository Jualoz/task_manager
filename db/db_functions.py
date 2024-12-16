from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import User, Task
import json
import streamlit as st

def create_user(db: Session, username: str, email: str, password: str):
    try:
        db_user = User(username=username, email=email, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"user": db_user}  # Devuelve un diccionario con el usuario creado
    except IntegrityError as e:
        db.rollback()
        if "username" in str(e.orig):
            return {"error": "The username is already taken."}
        elif "email" in str(e.orig):
            return {"error": "The email is already registered."}
        else:
            return {"error": "An unexpected error occurred."}
    except Exception as e:
        db.rollback()
        return {"error": f"An error occurred: {str(e)}"}

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def verify_user_credentials(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return {"status": "user_not_found"}
    elif not user.password == password:
        return {"status": "wrong_password"}
    else:
        return {"status": "success", "user": user}

def create_task(db: Session, user_id: int, title: str, description: str, completed: bool = False):
    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()

def update_task_status(db: Session, task_id: int, completed: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False

# Nueva función para actualizar los detalles de la tarea (título y descripción)
def update_task_details(db: Session, task_id: int, title: str, description: str):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        print(db_task)
        db_task.title = title
        db_task.description = description
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def export_tasks(db: Session, user_id: int):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    
    tasks_data = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "created_at": str(task.created_at),
            "completed": task.completed
        }
        for task in tasks
    ]
    # Convertir a JSON
    return json.dumps(tasks_data, indent=4)

def import_tasks(db: Session, user_id: int, tasks_data: str):
    try:
        tasks_json = json.loads(tasks_data)  # Convertir el archivo JSON en un diccionario
        for task in tasks_json:
            # Verificar si la tarea ya existe (puedes ajustar esta lógica de acuerdo con tus necesidades)
            existing_task = db.query(Task).filter(Task.title == task['title'], Task.user_id == user_id).first()
            
            if existing_task:
                # Si la tarea ya existe, puedes actualizarla o saltarla
                # Por ejemplo, si quieres actualizarla:
                existing_task.description = task['description']
                existing_task.completed = task['completed']
                db.commit()
            else:
                # Si no existe, crearla
                new_task = Task(
                    user_id=user_id,
                    title=task['title'],
                    description=task['description'],
                    completed=task['completed']
                )
                db.add(new_task)
                db.commit()
        
        return {"status": "success"}

    except Exception as e:
        db.rollback()
        return {"error": str(e)}