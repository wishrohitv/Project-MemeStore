from dotenv import load_dotenv

from backend.modules import create_engine, os

load_dotenv()

engine = create_engine(os.environ.get("DB_URL") or "")


def initializeDb():
    from backend.models import Base

    # Create all tables in the engine
    Base.metadata.create_all(engine)
