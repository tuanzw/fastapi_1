from sqlmodel import create_engine, Session

from .models import SQLModel

db_filename = "fastapi_1.db"
sqlite_url = f"sqlite:///{db_filename}"

connect_args = {"check_same_thread": False}

engine = create_engine(url=sqlite_url, connect_args=connect_args, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
