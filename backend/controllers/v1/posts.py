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
    _posts,
    _postToggleLike,
    _updatePost,
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
    sessionUserID: int | None = None if loggedUser is None else loggedUser.userID
    try:
        return _posts(userName=userName, sessionUserID=sessionUserID)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


# /posts/uploadPosts
@postsBlueprint.route(route.uploadPosts.routeName, methods=route.uploadPosts.methods)
@verifyRequestMiddleware(route.uploadPosts.routeName)
def uploadPosts(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    postMediaUid = str(uuid.uuid4())
    if request.method == "POST":
        # body = request.get_json(force=True)
        # print(request.form.getlist)
        print(request.files["files"])
        print(request.form)
        file = request.files["files"]
        fileMimeType = file.mimetype
        if fileMimeType in ALLOWED_POST_FILE_MIMETYPE:
            fileExtension = ALLOWED_POST_FILE_MIMETYPE.get(fileMimeType)

        else:
            return make_response(
                {"error": f"unsupported file type {fileMimeType}"}, 401
            )
        pForm = request.form
        try:
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
            _mediaUrl = None
            _mediaPublicID = None
            if USE_CLOUDINARY_STORAGE:
                cloudResponse = uploadMedia(file=file.stream, public_id=postMediaUid)
                if not (cloudResponse):
                    return make_response({"error": "Failed to upload media"}, 500)
                _mediaUrl = cloudResponse.get("url")
                _mediaPublicID = cloudResponse.get("public_id")
            else:
                file.save(
                    os.path.join(
                        PUBLIC_DIRECTORY_POSTS,
                        secure_filename(f"{postMediaUid}.{fileExtension}"),
                    )
                )
                _mediaPublicID = postMediaUid
            _createPost(
                userID=sessionUserID,
                title=pForm.get("postTitle"),
                tags=pForm.get("postTags"),
                visibility=pForm.get("postVisibility").lower() == "true",
                fileType=fileMimeType.split("/")[0],  # i.e "image/jpeg"
                fileExtension=fileExtension,
                mediaUrl=_mediaUrl,
                mediaPublicID=_mediaPublicID,
                category=1,
                # category=pForm.get("category"),
                ageRating=(pForm.get("ageRating") or "pg13").lower(),
            )
            return make_response({"message": "post uploaded successfully"}, 200)
        except Exception as e:
            Log.error(f"Failed to upload post: {e}")
            return make_response({"error": f"{e}"}, 401)
    else:
        return make_response({"error": "method upload post not allowed"}, 401)


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
