from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path='.env')
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)  


def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine) 
