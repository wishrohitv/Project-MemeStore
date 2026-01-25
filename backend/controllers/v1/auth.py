from backend.config import API_ENDPOINTS, ROLE
from backend.middlewares.verifyClientRequest import verifyRequestMiddleware
from backend.models import AccountStatus
from backend.modules import (
    ACCESS_TOKEN_EXPIRY_MINUTES,
    HTTP_ONLY,
    REFRESH_TOKEN_EXPIRY_MINUTES,
    SECURE_COOKIE,
    Blueprint,
    json,
    make_response,
    request,
)
from backend.repository.userRespository import (
    _authenticateUser,
    _createUser,
    _logout,
    _refreshTokens,
)
from backend.utils import LoggedUser

authBlueprint = Blueprint("auth", __name__)
"""
url_prefix causing confilct
authBlueprint = Blueprint(
    "auth",
    __name__,
    url_prefix = 'auth'
)
"""

route = API_ENDPOINTS()


# auth/signup
@authBlueprint.route(route.signupUser.routeName, methods=route.signupUser.methods)
def signup():
    clientBody = request.get_json()
    if isinstance(clientBody, dict):
        name = clientBody.get("name")
        userName = clientBody.get("userName")
        email = clientBody.get("email")
        password1 = clientBody.get("password1")
        password2 = clientBody.get("password2")
        country = clientBody.get("country") if None else "world"

        if not (userName or email or password1 or password2):
            return make_response(
                {"error": "userName, email and password are required"}, 400
            )
        if password1 != password2:
            return make_response({"error": "Passwords do not match"}, 400)

        return _createUser(
            name=name,
            userName=userName,
            email=email,
            password=password1,
            role=ROLE.USER,  # Defualt role,
            accountStatus=AccountStatus.active,
            country=country,
        )
    else:
        return make_response({"error": "Expect json body"}, 401)


# "/auth/login"
@authBlueprint.route(route.loginUser.routeName, methods=route.loginUser.methods)
def login():
    try:
        clientBody = request.get_json()
        if isinstance(clientBody, dict):
            userName = clientBody.get("userName")
            email = clientBody.get("email")
            password = clientBody.get("password")
            if not (userName or email):
                return make_response({"error": "Username or email is required"}, 400)
            if not password:
                return make_response({"error": "Password is required"}, 400)

            return _authenticateUser(userName=userName, email=email, password=password)
        else:
            return make_response({"error": "Expect json body"}, 401)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# "/auth/logout"
@authBlueprint.route(route.logoutUser.routeName, methods=route.logoutUser.methods)
@verifyRequestMiddleware(route.logoutUser.routeName)
def logout(loggedUser: LoggedUser, *args, **kwargs):
    refreshToken = loggedUser.kwargs.get("refreshToken")
    if not refreshToken:
        return make_response({"error": "refresh token is required"}, 401)
    sessionUserID = loggedUser.userID
    allDevices = str(request.args.get("allDevices", False)).lower() == "true"
    _logout(refreshToken, sessionUserID, allDevices)

    res = make_response({"message": "Logged out successfully"}, 200)
    res.delete_cookie(
        key="accessToken",
    )
    res.delete_cookie(
        key="refreshToken",
    )
    return res


# /auth/refresh
@authBlueprint.route(route.refreshToken.routeName, methods=route.refreshToken.methods)
def refreshToken():
    # for web
    refreshToken = request.cookies.get("refreshToken") or request.headers.get(
        "refreshToken", None
    )
    if not refreshToken:
        return make_response({"error": "Refresh token is required"}, 401)

    # verify refresh token
    try:
        newTokens = _refreshTokens(refreshToken)
        res = make_response(
            {"message": "Token refreshed successfully", "payload": newTokens[0]}, 200
        )
        res.set_cookie(
            key="accessToken",
            value=newTokens[1],
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            max_age=ACCESS_TOKEN_EXPIRY_MINUTES * 60,
        )
        res.set_cookie(
            key="refreshToken",
            value=newTokens[2],
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            samesite=None,
            max_age=REFRESH_TOKEN_EXPIRY_MINUTES * 60,
        )
        return res
    except Exception as e:
        return make_response({"error": str(e)}, 401)


@authBlueprint.route("/auth/verify", methods=["POST"])
def verify():
    raise NotImplementedError()
