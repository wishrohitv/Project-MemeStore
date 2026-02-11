from backend.config import API_ENDPOINTS, ROLE
from backend.modules import functools, make_response, re, request
from backend.repository.checkUserRole import getUserRole
from backend.utils import LoggedUser, decodeJwtToken

apiEndpointsPartialAccess = API_ENDPOINTS().apiEndpointsPartialAccess


def verifyRequestMiddleware(endpoint: str):
    # below decorator
    def verifyClientRequest(func):
        @functools.wraps(func)
        def checkClientRequest(*args, **kwargs):
            # before main function runs
            accessToken = None
            authorization = request.headers.get("authorization")
            refreshToken = request.headers.get("refreshToken")
            # Check request medium if mobile
            if authorization is not None and re.match(
                "^Bearer *([^ ]+)", authorization, flags=0
            ):
                accessToken = authorization.split(" ")[1]
            else:
                # Check of web
                accessToken = request.cookies.get("accessToken")
                refreshToken = request.cookies.get("refreshToken")

            if accessToken:
                try:
                    decodedToken = decodeJwtToken(accessToken)
                    if decodedToken:
                        # Match the user id and role for this endpoint
                        result = getUserRole(endpoint, decodedToken["payload"]["role"])
                        if result:
                            return func(
                                loggedUser=LoggedUser(
                                    userID=decodedToken["payload"]["id"],
                                    roleID=decodedToken["payload"]["role"],
                                    roleName=ROLE().rolesIds[
                                        decodedToken["payload"]["role"]
                                    ],
                                    accessToken=accessToken,
                                    refreshToken=refreshToken,
                                ),
                                *args,
                                **kwargs,
                            )
                        else:
                            # Either user role or endpoint not found
                            return make_response(
                                {"message": "Invalid user role or route"}, 401
                            )

                    else:
                        return make_response({"error": "Token expired"}, 401)
                except Exception as e:
                    return make_response(
                        {"error": f"{e}", "message": "Provide valid token"}, 401
                    )

            elif apiEndpointsPartialAccess.get(endpoint):
                # Give user partial access
                return func(
                    loggedUser=None,
                    *args,
                    **kwargs,
                )
            else:
                return make_response(
                    {"error": "Invalid token", "message": "No auth token found"}, 401
                )

            # after main function run

        # Renaming the function name:
        # checkClientRequest.__name__ = func.__name__
        return checkClientRequest

    return verifyClientRequest
