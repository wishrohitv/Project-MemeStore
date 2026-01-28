from backend.database import engine
from backend.models import Comments, Posts, Profile, Users
from backend.modules import (
    API_ROOT_URL,
    USE_CLOUDINARY_STORAGE,
    datetime,
    delete,
    or_,
    select,
    sessionmaker,
    update,
    url_for,
)

Session = sessionmaker(bind=engine)
session = Session()


def _getComments(
    postID: int,
    parentCommentID: int | None = None,  # Used to fetch related comment's replies
    offset: int = 0,
    limit: int = 10,
):
    try:
        stmt = (
            select(
                Comments,
                Users.userName,
                Users.name,
                Profile.mediaUrl,
                Profile.mediaPublicID,
                Profile.fileExtension,
            )
            .join(
                Users,
                Comments.userID == Users.id,
            )
            .join(
                Profile,
                Users.id == Profile.userID,
            )
            .where(
                Comments.postID == postID,
                Comments.parentCommentID == parentCommentID,
            )
            .offset(offset)
            .limit(limit)
        )
        comments = session.execute(stmt).all()
        session.close()
        commentsData = [
            {
                "id": comment[0].id,
                "userID": comment[0].userID,
                "content": comment[0].content,
                "parentCommentID": comment[0].parentCommentID,
                "createdAt": comment[0].createdAt,
                "updatedAt": comment[0].updatedAt,
                "userName": comment[1],
                "name": comment[2],
                "profileImgUrl": comment[3]
                if USE_CLOUDINARY_STORAGE
                else f"{API_ROOT_URL}{url_for('profileImage.serveImage', fileName=f'{comment[4]}.{comment[5]}')}",
            }
            for comment in comments
        ]
        return commentsData
    except Exception as e:
        print(e)
        raise Exception(f"Error getting comments: {e}")


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
