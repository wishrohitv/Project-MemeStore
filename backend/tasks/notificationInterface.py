from .notifications import createNotification
from backend.models import Users
from backend.models.enums import NotificationType
from backend.modules import sessionmaker
from backend.database import engine
from backend.utils import getUsername, Log

Session = sessionmaker(bind=engine)
session = Session()


def mention(
    mentionedByUserID: int,
    postID: int,
    text: str,
) -> None:
    try:
        # Extract mentioned usernames from the text
        mentionedUsernames = getUsername(text)

        # Get the username of the user who mentioned others
        result = (
            session.query(Users.userName).filter(Users.id == mentionedByUserID).first()
        )
        # Get the username of the user who mentioned others
        mentionedBy = result[0] if result else None

        # If the user who mentioned others is not found, we can't create notifications
        if not mentionedBy:
            return

        # Create notifications for each mentioned user
        for mentionedUsername in mentionedUsernames:
            # Find the user ID of the mentioned username
            result = (
                session.query(Users.id)
                .filter(Users.userName == mentionedUsername)
                .first()
            )
            # User iD of the mentioned user, if found, else None
            userID = result[0] if result else None

            # If the mentioned user is found, create a notification for them
            if userID:
                notice = {
                    # Post ID where the user was mentioned
                    "postID": postID,
                    # Username of the user who mentioned them
                    "mentionedBy": mentionedBy,
                    # Text of the notification, e.g., "Alice mentioned you in a post."
                    "alert": f"{mentionedBy} mentioned you in a post.",
                    "text": text[150] if len(text) > 150 else text,  # Short preview of the text

                }
                # Create the notification using the createNotification function
                createNotification(
                    userID=userID,
                    notice=notice,
                    type=NotificationType.mention,
                )
    except Exception as e:
        session.close()
        Log.critical(str(e))
        raise Exception(str(e))


def suggestion(
    postID: int,
    text: str,  # title of the post or ""
) -> dict:
    notice = {
        "postID": postID,
        "text": text,
    }


def reply(
    perentPostID: int,
    postID: int,
    text: str,  # title of the post or ""
) -> dict:
    try:
        mentionedUsernames = getUsername(text)
        for mentionedUsername in mentionedUsernames:
            userID = (
                session.query(Users.id)
                .filter(Users.username == mentionedUsername)
                .first()
            )
            if not userID:
                notice = {
                    "parentPostID": perentPostID,
                    "postID": postID,
                    "text": text,
                }
                createNotification(
                    userID=userID,
                    notice=notice,
                    type=NotificationType.mention,
                )
    except Exception as e:
        session.close()
        Log.critical(str(e))
        raise Exception(str(e))


def warning(text: str) -> dict:
    notice = {
        "text": text,
    }


def danger(text: str) -> dict:
    notice = {
        "text": text,
    }


def systemUpdate(text: str) -> dict:
    notice = {
        "text": text,
    }
