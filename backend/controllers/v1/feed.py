from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import Blueprint, make_response, request
from backend.repository.feedRepository import getHomeFeed
from backend.utils import LoggedUser

feedBlueprint = Blueprint("feed", __name__)

route = API_ENDPOINTS()


# /feed
@feedBlueprint.route(route.feed.routeName, methods=route.feed.methods)
@verifyRequestMiddleware(route.feed.routeName)
def getFeed(loggedUser: LoggedUser | None = None, *args, **kwargs):
    """
    Check if user is logged then build home feed based on his interests
    """
    offset = request.args.get("offset", type=int, default=0)
    categoryIDs = request.args.get("category", type=list, default=[1])
    sessionUserID: int | None = loggedUser.userID if loggedUser else None
    try:
        return getHomeFeed(
            category=categoryIDs, offset=offset, sessionUserID=sessionUserID
        )
    except Exception as e:
        return make_response({"error": str(e)}, 500)
