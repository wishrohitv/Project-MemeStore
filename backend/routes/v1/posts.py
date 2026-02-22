from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import (
    ALLOWED_POST_FILE_MIMETYPE,
    ALLOWED_POST_FILE_SIZE,
    PUBLIC_DIRECTORY_POSTS,
    USE_CLOUDINARY_STORAGE,
    Blueprint,
    make_response,
    os,
    request,
    secure_filename,
    uuid,
)
from backend.repository.postRepository import (
    _createPost,
    _deletePost,
    _getPostByIDorReplies,
    _postToggleBookmark,
    _postToggleLike,
    _reportPost,
    _updatePost,
    _userPosts,
)
from backend.utils import Log, LoggedUser, uploadMedia

postsBlueprint = Blueprint("posts", __name__)

route = API_ENDPOINTS()


# /posts
# Unlogged user can access public posts
@postsBlueprint.route(
    f"{route.posts.routeName}/<string:userName>", methods=route.posts.methods
)
@verifyRequestMiddleware(route.posts.routeName)
def posts(loggedUser: LoggedUser | None, *args, **kwargs):
    userName = kwargs.get("userName")
    orderBy = request.args.get("orderBy")
    category = request.args.get("category")
    limit = request.args.get("limit", type=int, default=10)
    offset = request.args.get("offset", type=int, default=0)
    template = str(request.args.get("template", default="False")).lower() == "true"
    bookmark = str(request.args.get("bookmark", default="False")).lower() == "true"
    sessionUserID: int | None = None if loggedUser is None else loggedUser.userID
    if not userName:
        return make_response({"error": "Invalid username"}, 400)
    try:
        return _userPosts(
            userName=userName,
            sessionUserID=sessionUserID,
            limit=limit,
            offset=offset,
            fetchTemplate=template,
            fetchBookmarked=bookmark,
        )
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/upload
@postsBlueprint.route(route.uploadPosts.routeName, methods=route.uploadPosts.methods)
@verifyRequestMiddleware(route.uploadPosts.routeName)
def uploadPosts(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID

    isReplie = (
        str(request.args.get("isReplie", default="False", type=str)).lower() == "true"
    )
    parentPostID = request.args.get("parentPostID", default=None, type=int)

    if isReplie and not parentPostID:
        return make_response(
            {
                "error": "Parent post ID is required for replie to a post",
                "message": "Bad request",
            },
            400,
        )
    try:
        # Handle files
        file = request.files.get(
            "files"
        )  # i.e. <FileStorage: 'mario-removebg-preview.png' ('image/png')>
        _mediaPublicID = str(
            uuid.uuid4()
        )  # Initially any random id otherwise None if file not found
        _fileType = None  # i.e "image/jpeg"
        _fileExtension = None
        _mediaUrl = None

        pForm = request.form
        postVisibility = pForm.get("postVisibility")
        postTitle = pForm.get("postTitle")
        postTags = pForm.get("postTags")
        postVisibility = (
            True if not postVisibility else postVisibility.lower() == "true"
        )
        postAgeRating = (pForm.get("ageRating") or "pg13").lower()

        if file:
            fileMimeType = file.mimetype
            _fileType = fileMimeType.split("/")[0]
            if fileMimeType in ALLOWED_POST_FILE_MIMETYPE:
                _fileExtension = ALLOWED_POST_FILE_MIMETYPE.get(fileMimeType)

            else:
                return make_response(
                    {"error": f"unsupported file type {fileMimeType}"}, 401
                )
            fileSize = file.stream.seek(0, os.SEEK_END)

            allowedFileSize = ALLOWED_POST_FILE_SIZE.get(fileMimeType)
            if not (fileSize <= allowedFileSize):
                return make_response(
                    {
                        "error": "File size exceeded",
                        "message": f"File size must not exceed {allowedFileSize / 1024 / 1024} MB",
                    },
                    406,
                )
            # Move pointer to Zero
            file.stream.seek(0)  # Moves the file pointer back to the beginning

            if USE_CLOUDINARY_STORAGE:
                cloudResponse = uploadMedia(file=file.stream, public_id=_mediaPublicID)
                if not (cloudResponse):
                    return make_response({"error": "Failed to upload media"}, 500)
                _mediaUrl = cloudResponse.get("url")
                _mediaPublicID = cloudResponse.get("public_id")
            else:
                file.save(
                    os.path.join(
                        PUBLIC_DIRECTORY_POSTS,
                        secure_filename(f"{_mediaPublicID}.{_fileExtension}"),
                    )
                )
        else:
            _mediaPublicID = None

        # Check if text and file both is not None
        if not postTitle and not _mediaPublicID:
            return make_response({"error": "Text or file is required"}, 400)

        _createPost(
            userID=sessionUserID,
            text=postTitle,
            tags=postTags,
            visibility=postVisibility,
            fileType=_fileType,  # i.e "image/jpeg"
            fileExtension=_fileExtension,
            mediaUrl=_mediaUrl,
            mediaPublicID=_mediaPublicID,
            category=1,
            ageRating=postAgeRating,
            isReplie=isReplie,
            parentPostID=parentPostID,
        )
        return make_response({"message": "post uploaded successfully"}, 201)
    except Exception as e:
        Log.error(f"Failed to upload post: {e}")
        return make_response({"error": f"{e}"}, 500)


# /posts/like
@postsBlueprint.route(
    f"{route.postLike.routeName}/<int:postID>", methods=route.postLike.methods
)
@verifyRequestMiddleware(route.postLike.routeName)
def toggleLike(loggedUser: LoggedUser, *agrs, **kwargs):
    sessionUserID = loggedUser.userID

    postID = kwargs.get("postID")
    if postID is None and not isinstance(postID, int):
        return make_response({"error": "Invalid post ID"}, 400)
    try:
        return _postToggleLike(sessionUserID=sessionUserID, postID=postID)

    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/bookmark
@postsBlueprint.route(
    f"{route.postBookmark.routeName}/<int:postID>", methods=route.postBookmark.methods
)
@verifyRequestMiddleware(route.postBookmark.routeName)
def toggleBookmark(loggedUser: LoggedUser, *agrs, **kwargs):
    sessionUserID = loggedUser.userID

    postID = kwargs.get("postID")
    if postID is None and not isinstance(postID, int):
        return make_response({"error": "Invalid post ID"}, 400)
    try:
        return _postToggleBookmark(sessionUserID=sessionUserID, postID=postID)

    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/delete
@postsBlueprint.route(
    f"{route.deletePost.routeName}/<int:postID>", methods=route.deletePost.methods
)
@verifyRequestMiddleware(route.deletePost.routeName)
def deletePost(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    postID = kwargs.get("postID")
    if postID is None and not isinstance(postID, int):
        return make_response({"error": f"Invalid postID {postID} datatype"}, 400)
    try:
        _deletePost(sessionUserID=sessionUserID, postID=postID)

        return make_response({"message": "Post deleted successfully"}, 201)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/update
@postsBlueprint.route(
    f"{route.updatePost.routeName}/<int:postID>", methods=route.updatePost.methods
)
@verifyRequestMiddleware(route.updatePost.routeName)
def updatePost(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    postID = kwargs.get("postID")
    if postID is None and not isinstance(postID, int):
        return make_response({"error": f"Invalid postID {postID} datatype"}, 400)
    try:
        body = request.json
        title = body.get("title")
        tags = body.get("tags")
        ageRating = body.get("ageRating")
        category = body.get("category")
        visibility = body.get("visibility")

        _updatePost(
            sessionUserID=sessionUserID,
            postID=postID,
            title=title,
            tags=tags,
            ageRating=ageRating,
            category=category,
            visibility=visibility,
        )

        return make_response({"message": "Post updated successfully"}, 201)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts
@postsBlueprint.route(
    f"{route.posts.routeName}/<int:postID>",
    methods=route.posts.methods,
)
@verifyRequestMiddleware(route.posts.routeName)
def postsByID(loggedUser: LoggedUser | None = None, *args, **kwargs):
    postID = kwargs.get("postID")
    sessionUserID: int | None = loggedUser.userID if loggedUser else None
    if not postID or not isinstance(postID, int):
        return make_response({"error": "Missing postID"}, 400)
    try:
        return _getPostByIDorReplies(postID=postID, sessionUserID=sessionUserID)
    except Exception as e:
        print(e)
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/replies
@postsBlueprint.route(
    f"{route.postReplies.routeName}/<int:postID>",
    methods=route.postReplies.methods,
)
@verifyRequestMiddleware(route.postReplies.routeName)
def postsReplies(loggedUser: LoggedUser | None = None, *args, **kwargs):
    postID: int | None = kwargs.get("postID")
    if not postID:
        return make_response({"error": f"Invalid post id {postID}"}, 400)
    try:
        return _getPostByIDorReplies(postID=postID, fetchReplies=True)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/report
@postsBlueprint.route(
    f"{route.reportPost.routeName}/<int:postID>",
    methods=route.reportPost.methods,
)
@verifyRequestMiddleware(route.reportPost.routeName)
def reportPost(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    postID: int | None = kwargs.get("postID")
    if not postID:
        return make_response({"error": f"Invalid post id {postID}"}, 400)
    try:
        reason = request.get_json().get("reason")
        return _reportPost(sessionUserID=sessionUserID, postID=postID, reason=reason)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)
