from database import engine
from models import CollectionData, Collections
from modules import datetime, delete, or_, sessionmaker, update
from utils import RepoError

Session = sessionmaker(bind=engine)
session = Session()


def _collections():
    pass


def _create_collection(
    name: str,
    session_user_id: int,
    description: str | None = None,
):
    try:
        stmt = Collections(name=name, description=description, owner=session_user_id)
        session.add(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise RepoError(500, f"Error while creating collection :{e}")


def _add_post_to_collection(collection_id: int, session_user_id: int, post_id: int):
    try:
        collection = (
            session.query(Collections)
            .where(
                Collections.id == collection_id, Collections.owner == session_user_id
            )
            .first()
        )
        if not collection:
            raise RepoError(404, "Collection not found or unauthorized")
        stmt = CollectionData(collection_id=collection_id, post_id=post_id)
        session.add(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise RepoError(500, f"Error while creating collection :{e}")


def _remove_post_to_collection(collection_id: int, session_user_id: int, post_id: int):
    try:
        collection = (
            session.query(Collections)
            .where(
                Collections.id == collection_id, Collections.owner == session_user_id
            )
            .first()
        )
        if not collection:
            raise RepoError(404, "Collection not found or unauthorized")
        stmt = delete(CollectionData).filter_by(
            collection_id=collection_id, post_id=post_id
        )
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise RepoError(500, f"Error while removing post from collection :{e}")


def _delete_collection(collection_id: int, session_user_id: int):
    try:
        collection = (
            session.query(Collections)
            .where(
                Collections.id == collection_id, Collections.owner == session_user_id
            )
            .first()
        )
        if not collection:
            raise RepoError(404, "Collection not found or unauthorized")
        stmt = delete(CollectionData).filter_by(collection_id=collection_id)
        stmt1 = delete(Collections).filter_by(id=collection_id)
        session.execute(stmt)
        session.execute(stmt1)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise RepoError(500, f"Error while deleting collection :{e}")
