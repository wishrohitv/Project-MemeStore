from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import Blueprint, make_response, request
from backend.repository.notificationRepository import _getNotifications
from backend.utils import Log, LoggedUser

notificationBlueprint = Blueprint("notifications", __name__)

route = API_ENDPOINTS()


@notificationBlueprint.route(
    f"{route.getNotifications.routeName}", methods=route.getNotifications.methods
)
@verifyRequestMiddleware(route.getNotifications.routeName)
def get_notifications(loggedUser: LoggedUser, *args, **kwargs):
    try:
        sessionUserID = loggedUser.userID
        mention = str(request.args.get("mention", default=False)).lower() == "true"
        notice = _getNotifications(sessionUserID, mention)
        return notice
    except Exception as e:
        Log.error(e)
        return make_response({"error": str(e)}, 500)
