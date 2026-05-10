from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import Blueprint, make_response, request
from backend.repository.notificationRepository import _getNotifications
from backend.utils import Log, LoggedUser
from backend.utils.appError import AppError, RateLimitExceededError
from backend.utils.logger import Logging

notificationBlueprint = Blueprint("notifications", __name__)

route = API_ENDPOINTS()
logger = Logging(__name__)


@notificationBlueprint.route(
    f"{route.getNotifications.routeName}", methods=route.getNotifications.methods
)
@verifyRequestMiddleware(route.getNotifications.routeName)
def getNotifications(loggedUser: LoggedUser, *args, **kwargs):
    try:
        sessionUserID = loggedUser.userID
        mention = str(request.args.get("mention", default=False)).lower() == "true"
        notice = _getNotifications(sessionUserID, mention)
        return notice
    except Exception as e:
        Log.error(e)
        return make_response({"error": str(e)}, 500)


@notificationBlueprint.route(
    route.trackNotifications.routeName, methods=route.trackNotifications.methods
)
@verifyRequestMiddleware(route.trackNotifications.routeName)
def trackNotificationClick():
    # TODO: complete the logic
    logger.error("not fuond")
    raise RateLimitExceededError(description="Bad request")
