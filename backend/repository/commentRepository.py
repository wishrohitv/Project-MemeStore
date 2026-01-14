from backend.database import engine
from backend.models import Comments, Posts
from backend.modules import datetime, delete, or_, sessionmaker, update

Session = sessionmaker(bind=engine)
session = Session()


def _createComment(
    postID: int, userID: int, content: str, parentCommentID: int | None = None
) -> None | Exception:
    try:
        stmt = Comments(
            postID=postID,
            userID=userID,
            content=content,
            parentCommentID=parentCommentID,
        )
        session.add(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error creating comment: {e}")


def _updateComment(
    commentID: int, content: str, sessionUserID: int
) -> None | Exception:
    """
    Update a comment's content.

    Args:
        commentID (int): The ID of the comment to update.
        content (str): The new content of the comment.
        authorID (int): The ID of the user who authored the comment.

    Raises:
        Exception: If the comment does not exist or the user is not authorized to update it.
    """
    try:
        # Check comment's author or post's postAuthor is in session
        query = (
            session.query(Comments)
            .filter(
                Comments.id == commentID,
                Comments.userID == sessionUserID,
            )
            .first()
        )
        if not query:
            raise Exception("Unauthorized access")
        stmt = (
            update(Comments)
            .filter_by(
                id=commentID,
            )
            .values(content=content)
        )
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error updating comment: {e}")


def _deleteComment(
    commentID: int,
    sessionUserID: int,
):
    try:
        # Check comment's author or post's postAuthor is in session
        query = (
            session.query(Comments)
            .join(Posts)
            .filter(
                Comments.id == commentID,
                or_(Comments.userID == sessionUserID, Posts.userID == sessionUserID),
            )
            .first()
        )

        if not query:
            raise Exception("Unauthorized access")
        stmt = delete(Comments).filter_by(
            id=commentID,
        )
        session.execute(stmt)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise Exception(f"Error deleting comment: {e}")
