from backend.models import Notifications
from backend.models.enums import NotificationType
from backend.modules import sessionmaker
from backend.database import engine
from backend.utils import Log

Session = sessionmaker(bind=engine)
session = Session()


def createNotification(
    userID: int | None,
    notice: dict,
    type: NotificationType,
):
    try:
        notification = Notifications(
            userID=userID,
            notice=notice,
            type=type,
        )
        session.add(notification)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        Log.critical(f"Error creating notification: {str(e)}")
        raise Exception(str(e))
