from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import Blueprint, make_response, request
from backend.repository.commentRepository import (
    _createComment,
    _deleteComment,
    _updateComment,
)
from backend.utils.loggedUser import LoggedUser

commentsBlueprint = Blueprint("comments", __name__)

route = API_ENDPOINTS()


# /comments/create"
@commentsBlueprint.route(
    f"{route.createComments.routeName}/<int:postID>",
    methods=route.createComments.methods,
)
@verifyRequestMiddleware(route.createComments.routeName)
def createCommments(loggedUser: LoggedUser, *args, **kwargs):
    postID = kwargs.get("postID")
    sessionUserID = loggedUser.userID
    data = request.get_json()
    parentCommentID = (
        data.get("parentCommentID") or None
    )  # Used to create comment replies
    if not isinstance(postID, int):
        return make_response({"error": f"Invalid postID {postID} datatype"})

    if parentCommentID is not None and not isinstance(parentCommentID, int):
        return make_response({"error": f"Invalid commnetID {postID} datatype"})

    try:
        _createComment(postID, sessionUserID, data.get("content"), parentCommentID)
        return make_response("Comment created successfully")
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /comments/update
@commentsBlueprint.route(
    f"{route.updateComment.routeName}/<int:commentID>",
    methods=route.updateComment.methods,
)
@verifyRequestMiddleware(route.updateComment.routeName)
def updateComments(loggedUser: LoggedUser, *args, **kwargs):
    commentID = kwargs.get("commentID")
    sessionUserID = loggedUser.userID
    data = request.get_json()
    if not isinstance(commentID, int):
        return make_response({"error": f"Invalid comment id {commentID} datatype"})
    try:
        _ = _updateComment(
            commentID=commentID,
            sessionUserID=sessionUserID,
            content=data.get("content"),
        )
        return make_response("Comment updated successfully")
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /comments/delete
@commentsBlueprint.route(
    f"{route.deleteComment.routeName}/<int:commentID>",
    methods=route.deleteComment.methods,
)
@verifyRequestMiddleware(route.deleteComment.routeName)
def deleteComments(loggedUser: LoggedUser, *args, **kwargs):
    commentID = kwargs.get("commentID")
    sessionUserID = loggedUser.userID

    if not isinstance(commentID, int):
        return make_response({"error": f"Invalid comment id {commentID} datatype"})
    try:
        _deleteComment(
            commentID=commentID,
            sessionUserID=sessionUserID,
        )
        return make_response("Comment deleted successfully")
    except Exception as e:
        return make_response({"error": str(e)})
