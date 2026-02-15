import redis
from dotenv import load_dotenv

from backend.modules import create_engine, os

load_dotenv()

# Initialize database engine
engine = create_engine(os.environ.get("DB_URL") or "", pool_pre_ping=True)

# Initialize Redis client
redisClient = redis.Redis.from_url(
    os.environ.get("REDIS_URL") or "", decode_responses=True
)


def initializeDb():
    from backend.models import Base

    # Create all tables in the engine
    Base.metadata.create_all(engine)
