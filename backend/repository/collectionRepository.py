from typing_extensions import Collection

from backend.database import engine
from backend.models import CollectionData, Collections
from backend.modules import datetime, delete, or_, sessionmaker, update

Session = sessionmaker(bind=engine)
session = Session()


def _collections():
    pass


def _createCollection(
    collectionName: str,
    sessionUserID: int,
    description: str | None = None,
):
    try:
        stmt = Collections(
            collectionName=collectionName, description=description, owner=sessionUserID
        )
        session.add(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error while creating collection :{e}")


def _addPostToCollection(collectionID: int, sessionUserID: int, postID: int):
    try:
        collection = (
            session.query(Collections)
            .where(Collections.id == collectionID, Collections.owner == sessionUserID)
            .first()
        )
        if not collection:
            raise Exception("Collection not found or unauthorized")
        stmt = CollectionData(collectionId=collectionID, postID=postID)
        session.add(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error while creating collection :{e}")


def _removePostToCollection(collectionID: int, sessionUserID: int, postID: int):
    try:
        collection = (
            session.query(Collections)
            .where(Collections.id == collectionID, Collections.owner == sessionUserID)
            .first()
        )
        if not collection:
            raise Exception("Collection not found or unauthorized")
        stmt = delete(CollectionData).filter_by(
            collectionID=collectionID, postID=postID
        )
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error while creating collection :{e}")


def _deleteCollection(collectionID: int, sessionUserID: int):
    try:
        collection = (
            session.query(Collections)
            .where(Collections.id == collectionID, Collections.owner == sessionUserID)
            .first()
        )
        if not collection:
            raise Exception("Collection not found or unauthorized")
        stmt = delete(CollectionData).filter_by(collectionID=collectionID)
        stmt1 = delete(Collections).filter_by(id=collectionID)
        session.execute(stmt)
        session.execute(stmt1)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error while creating collection :{e}")
