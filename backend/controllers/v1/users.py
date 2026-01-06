from backend.config import API_ENDPOINTS
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.modules import (
    PUBLIC_DIRECTORY_PROFILES,
    Blueprint,
    make_response,
    os,
    request,
    secure_filename,
)
from backend.repository.userRespository import addFollower, getUserProfile
from backend.utils import LoggedUser

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
def usersUpdateInfo():
    raise NotImplementedError()


# /user/profileImg/update
@usersBlueprint.route(
    route.userChangeProfile.routeName, methods=route.userChangeProfile.methods
)
@verifyRequestMiddleware(route.userChangeProfile.routeName)
def usersUpdateProfileImg():
    try:
        print(request.form)
        userName = request.form.get("userName")
        files = request.files.getlist("files")
        print(files)
        print(request.files)
        file = request.files["files"]
        print(file.mimetype)
        file.seek(0, 2)  # move to end of file
        size = file.tell()  # get current position, which is file size
        file.seek(0)  # reset file pointer
        print(f"Actual file size: {(size / 1020) / 1024} bytes")
        file.save(
            os.path.join(PUBLIC_DIRECTORY_PROFILES, secure_filename(f"{userName}"))
        )
        return make_response({"message": "File uploaded successfully"}, 200)
    except Exception as e:
        return make_response({"error": "Bad request", "message": f"{e}"})


@usersBlueprint.route(route.deleteUser.routeName, methods=route.deleteUser.methods)
@verifyRequestMiddleware(route.deleteUser.routeName)
def usersDelete():
    raise NotImplementedError()


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
