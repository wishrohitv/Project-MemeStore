from backend.config import API_ENDPOINTS
from backend.constant import ALLOWED_POST_FILE_SIZE
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
    addFollower,
    getUserProfile,
    updateProfileImg,
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
    raise NotImplementedError()


# /user/profileImg/update
@usersBlueprint.route(
    route.userChangeProfile.routeName, methods=route.userChangeProfile.methods
)
@verifyRequestMiddleware(route.userChangeProfile.routeName)
def usersUpdateProfileImg(loggedUser: LoggedUser, *args, **kwargs):
    try:
        profileMediaUid = str(uuid.uuid4())
        sessionUserID = loggedUser.userID
        # files = request.files.getlist("file")
        # print(files)
        # print(request.files)
        file = request.files["file"]
        print(file)
        print(file.mimetype)
        file.seek(0, 2)  # move to end of file
        size = file.tell()  # get current position, which is file size
        file.seek(0)  # reset file pointer
        print(size)
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
        return make_response({"error": "Bad request", "message": f"{e}"})


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
def toggleFollower():
    raise NotImplementedError()


@usersBlueprint.route(
    route.userAddFollower.routeName, methods=route.userAddFollower.methods
)
@verifyRequestMiddleware(route.userAddFollower.routeName)
def addFollwer(loggedUser: LoggedUser, *agrs, **kwargs):
    sessionUserID = loggedUser.userID
    body = request.get_json()
    if isinstance(body, dict):
        targetUserID = body.get("userID")
        if not isinstance(targetUserID, int):
            return make_response({"error": f"Invalid {targetUserID} datatype"})
        if targetUserID == sessionUserID:
            return make_response({"error": "user can't follow himself"}, 409)
        else:
            return addFollower(sessionUserID, targetUserID)

    else:
        return make_response({"error": "Expect json body"}, 401)
