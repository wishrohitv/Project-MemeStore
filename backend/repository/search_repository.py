from database import SessionLocal
from models import Posts, Profile, Users
from modules import select


def _search_prediction(text: str):
    session = SessionLocal()
    stmt = select(Users.id, Users.name, Users.username)
