from backend.modules import Blueprint, make_response
from backend.repository.feedRepository import getHomeFeed, getUsersPostsFeed

feedBlueprint = Blueprint("feed", __name__)


@feedBlueprint.route("/feed", methods=["GET"])
def getFeed():
    """
    Check if user is logged then build home feed based on his interests
    """
    return getHomeFeed()


@feedBlueprint.route("feed/user/<int:userID>", methods=["GET"])
def getUserPost(userID):
    """
    if user is logged then return private and public posts else public
    Args: .
    """
    return getUsersPostsFeed(userID=userID)
