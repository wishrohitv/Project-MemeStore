from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import Blueprint, make_response, request
from backend.repository.commentRepository import (
    _createComment,
    _deleteComment,
    _getComments,
    _updateComment,
)
from backend.utils.loggedUser import LoggedUser

commentsBlueprint = Blueprint("comments", __name__)

route = API_ENDPOINTS()


# /comments
@commentsBlueprint.route(
    f"{route.comments.routeName}/<int:postID>", methods=route.comments.methods
)
# /comments/postID/parentCommentID to get replies
@commentsBlueprint.route(
    f"{route.comments.routeName}/<int:postID>/<int:parentCommentID>",
    methods=route.comments.methods,
)
def comments(postID: int, parentCommentID: int | None = None):
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=10, type=int)
    try:
        comments = _getComments(postID, parentCommentID, offset, limit)
        return make_response({"payload": comments}, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


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
    content = data.get("content")
    parentCommentID = (
        data.get("parentCommentID") or None
    )  # Used to create comment replies
    if not isinstance(postID, int):
        return make_response({"error": f"Invalid postID {postID} datatype"}, 401)
    if len(content) == 0 or len(content) > 1000:
        return make_response({"error": "Content length exceeds maximum allowed"}, 401)

    if parentCommentID is not None and not isinstance(parentCommentID, int):
        return make_response({"error": f"Invalid commnetID {postID} datatype"}, 401)

    try:
        _createComment(postID, sessionUserID, content, parentCommentID)
        return make_response("Comment created successfully", 201)
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
