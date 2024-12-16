from .engine import SessionLocal, engine, Base
from . import models
from . import db_functions


def init_db():
    Base.metadata.create_all(bind=engine)