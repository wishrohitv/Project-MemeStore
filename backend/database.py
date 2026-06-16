import sys

import redis
from dotenv import load_dotenv
from modules import create_engine, os, sessionmaker
from redis import RedisError

load_dotenv()

try:
    # Initialize database engine
    engine = create_engine(os.environ.get("DB_URL") or "", pool_pre_ping=True)

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    # Initialize Redis client
    redis_client = redis.Redis.from_url(
        os.environ.get("REDIS_URL") or "", decode_responses=True
    )
except RedisError as e:
    print(f"Failed to initialize Redis client: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Failed to initialize database client: {e}")
    sys.exit(1)


def initialize_db():
    from models import Base

    # Create all tables in the engine
    Base.metadata.create_all(engine)
