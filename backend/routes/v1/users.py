from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import (
    ALLOWED_PROFILE_FILE_MIMETYPE,
    ALLOWED_PROFILE_FILE_SIZE,
    PUBLIC_DIRECTORY_PROFILES,
    USE_CLOUDINARY_STORAGE,
    Blueprint,
    make_response,
    os,
    request,
    secure_filename,
    uuid,
)
from backend.repository.userRespository import (
    _addFollower,
    _blockUser,
    _removeFollower,
    _reportUser,
    _unblockUser,
    getUserProfile,
    updateProfileImg,
    updateUser,
)
from backend.utils import LoggedUser, uploadMedia

usersBlueprint = Blueprint("users", __name__)

route = API_ENDPOINTS()


# /user/auth sessionUser only
@usersBlueprint.route(
    f"{route.userInSession.routeName}", methods=route.userInSession.methods
)
@verifyRequestMiddleware(route.userInSession.routeName)
def userSessionInfo(loggedUser: LoggedUser, *args, **kwargs):
    try:
        userID = loggedUser.userID
        return getUserProfile(
            _userID=userID,
        )
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /user/<string:userName>
@usersBlueprint.route(
    f"{route.user.routeName}/<string:userName>", methods=route.user.methods
)
@verifyRequestMiddleware(route.user.routeName)
def usersGetInfo(loggedUser: LoggedUser | None = None, *args, **kwargs):
    userName: str | None = kwargs.get("userName") or request.args.get("userName")
    userID = request.args.get("userID")
    userEmail: str | None = request.args.get("emailID")
    if not (userName or userID or userEmail):
        return make_response({"error": "Expect any value of userName, userID, emailID"})

    if userID:
        if not isinstance(userID, int):
            return make_response({"error": f"Invalid id {userID} datatype"}, 400)

    try:
        return getUserProfile(
            _userID=userID,
            _userName=userName,
            _email=userEmail,
            sessionUserID=loggedUser.userID if loggedUser else None,
        )
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /user/update
@usersBlueprint.route(route.userUpdate.routeName, methods=route.userUpdate.methods)
@verifyRequestMiddleware(route.userUpdate.routeName)
def usersUpdateInfo(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    try:
        body = request.get_json()
        if not body:
            return make_response({"error": "Invalid request body"}, 400)

        name = body.get("name")
        bio = body.get("bio")
        country = body.get("country")
        age = body.get("age")

        return updateUser(
            sessionUserID=sessionUserID, name=name, bio=bio, country=country, age=age
        )
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /user/profileImg/update
@usersBlueprint.route(
    route.userChangeProfile.routeName, methods=route.userChangeProfile.methods
)
@verifyRequestMiddleware(route.userChangeProfile.routeName)
def usersUpdateProfileImg(loggedUser: LoggedUser, *args, **kwargs):
    try:
        profileMediaUid = str(uuid.uuid4())
        sessionUserID = loggedUser.userID

        file = request.files["file"]
        file.seek(0, 2)  # move to end of file
        size = file.tell()  # get current position, which is file size in bytes
        file.seek(0)  # reset file pointer
        print(f"Actual file size: {(size / 1020) / 1024} MB")
        if file.mimetype not in ALLOWED_PROFILE_FILE_MIMETYPE:
            return make_response({"error": "Invalid file type"}, 400)
        if size > ALLOWED_PROFILE_FILE_SIZE.get(file.mimetype):
            return make_response(
                {
                    "error": f"File size exceeds limit, Please upload a smaller file below {ALLOWED_PROFILE_FILE_SIZE.get(file.mimetype) / 1024 / 1024} MB."
                },
                400,
            )

        fileExtension = file.filename.split(".")[-1]
        _mediaUrl = None
        _mediaPublicID = None
        if USE_CLOUDINARY_STORAGE:
            cloudResponse = uploadMedia(file=file.stream, public_id=profileMediaUid)
            _mediaUrl = cloudResponse.get("url")
            _mediaPublicID = cloudResponse.get("public_id")
        else:
            file.save(
                os.path.join(
                    PUBLIC_DIRECTORY_PROFILES,
                    secure_filename(f"{profileMediaUid}.{fileExtension}"),
                )
            )
            _mediaPublicID = profileMediaUid
        return updateProfileImg(
            sessionUserID=sessionUserID,
            mediaPublicID=_mediaPublicID,
            fileExtension=fileExtension,
            fileType=file.mimetype.split("/")[0],
        )
    except Exception as e:
        return make_response({"error": f"{e}"}, 500)


# /user/delete
@usersBlueprint.route(route.deleteUser.routeName, methods=route.deleteUser.methods)
@verifyRequestMiddleware(route.deleteUser.routeName)
def usersDelete():
    raise NotImplementedError()


# /user/unfollow
@usersBlueprint.route(
    route.userRemoveFollower.routeName, methods=route.userRemoveFollower.methods
)
@verifyRequestMiddleware(route.userRemoveFollower.routeName)
def removeFollower(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    body = request.get_json()
    if isinstance(body, dict):
        targetUserID = body.get("userID")
        if not isinstance(targetUserID, int):
            return make_response({"error": f"Invalid {targetUserID} datatype"})
        if targetUserID == sessionUserID:
            return make_response({"error": "user can't unfollow himself"}, 409)
        else:
            return _removeFollower(sessionUserID, targetUserID)

    else:
        return make_response({"error": "Expect json body"}, 401)


# /user/follow
@usersBlueprint.route(
    route.userAddFollower.routeName, methods=route.userAddFollower.methods
)
@verifyRequestMiddleware(route.userAddFollower.routeName)
def addFollower(loggedUser: LoggedUser, *agrs, **kwargs):
    sessionUserID = loggedUser.userID
    body = request.get_json()
    if isinstance(body, dict):
        targetUserID = body.get("userID")
        if not isinstance(targetUserID, int):
            return make_response({"error": f"Invalid {targetUserID} datatype"})
        if targetUserID == sessionUserID:
            return make_response({"error": "user can't follow himself"}, 409)
        else:
            return _addFollower(sessionUserID, targetUserID)

    else:
        return make_response({"error": "Expect json body"}, 401)


@usersBlueprint.route(
    f"{route.userBlock.routeName}/<int:userID>", methods=route.userBlock.methods
)
@verifyRequestMiddleware(route.userBlock.routeName)
def blockUser(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    userID = kwargs.get("userID")
    if not userID or not isinstance(userID, int):
        return make_response({"error": f"Invalid userID {userID} dataype"}, 400)
    return _blockUser(sessionUserID, userID)


@usersBlueprint.route(
    f"{route.userUnblock.routeName}/<int:userID>", methods=route.userUnblock.methods
)
@verifyRequestMiddleware(route.userUnblock.routeName)
def unblockUser(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    userID = kwargs.get("userID")
    if not userID or not isinstance(userID, int):
        return make_response({"error": f"Invalid userID {userID} dataype"}, 400)
    return _unblockUser(sessionUserID, userID)


@usersBlueprint.route(
    f"{route.userReport.routeName}/<int:userID>", methods=route.userReport.methods
)
@verifyRequestMiddleware(route.userReport.routeName)
def reportUser(loggedUser: LoggedUser, *args, **kwargs):
    sessionUserID = loggedUser.userID
    userID = kwargs.get("userID")
    if not userID or not isinstance(userID, int):
        return make_response({"error": f"Invalid userID {userID} dataype"}, 400)
    reason = request.get_json().get("reason")
    return _reportUser(sessionUserID, userID, reason or "")
