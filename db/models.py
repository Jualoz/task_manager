# db/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .engine import Base  # Importamos Base para heredar de ella

class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True, index=True)  # ID de usuario
    username = Column(String, unique=True, index=True)  # Nombre de usuario único
    email = Column(String, unique=True, index=True)  # Correo electrónico único
    password = Column(String)  # Contraseña del usuario
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    
    tasks = relationship("Task", back_populates="owner")  # Relación con las tareas

class Task(Base):
    __tablename__ = "tasks"  # Nombre de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True, index=True)  # ID de la tarea
    title = Column(String, index=True)  # Título de la tarea
    description = Column(String)  # Descripción de la tarea
    completed = Column(Boolean, default=False)  # Estado de la tarea
    created_at = Column(DateTime, default=datetime.utcnow)  # Fecha de creación
    user_id = Column(Integer, ForeignKey("users.id"))  # Relación con el usuario
    
    owner = relationship("User", back_populates="tasks")  # Relación inversa con el usuario
