from flask.helpers import make_response

from backend.database import engine
from backend.models import Notifications
from backend.models.enums import NotificationType
from backend.modules import or_, sessionmaker
from backend.utils import Log

Session = sessionmaker(bind=engine)
session = Session()


def _getNotifications(sessionUserID: int, mention: bool = False, offset: int = 0):
    condition = []
    if mention:
        condition.append(Notifications.type == NotificationType.mention)
        condition.append(
            Notifications.userID == sessionUserID,
        )
    else:
        condition.append(
            or_(
                Notifications.userID == sessionUserID,
                Notifications.userID.is_(None),
            )
        )

    try:
        result = (
            session.query(Notifications)
            .filter(*condition)
            .offset(offset)
            .limit(10)
            .all()
        )

        if not result:
            return make_response([], 200)
        notifications = [
            {
                "id": notice.id,
                "type": notice.type.value,
                "notice": notice.notice,
                "createdAt": notice.createdAt,
                "updatedAt": notice.updatedAt,
                "readAt": notice.readAt,
            }
            for notice in result
        ]
        return make_response(notifications, 200)
    except Exception as e:
        Log.error(e)
