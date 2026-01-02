import os
from backend.modules import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{DB_NAME}")
# engine = create_engine(os.environ.get("DB_URL"))


def initializeDb():
    from backend.models import Base

    # Create all tables in the engine
    Base.metadata.create_all(engine)
