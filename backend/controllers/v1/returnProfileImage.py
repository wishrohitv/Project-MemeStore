from backend.modules import (
    Blueprint,
    request,
    make_response,
    send_from_directory,
    PUBLIC_DIRECTORY_PROFILES,
    url_for,
    os,
)
from backend.utils.logger import Log


getProfileImageRouteBlueprint = Blueprint("profileImage", __name__)


@getProfileImageRouteBlueprint.route(
    "/getProfileImage/<string:userName>", methods=["GET"]
)
def getProfileImage(userName):
    return make_response(
        {
            "profileImg": url_for(
                "profileImage.serveImage", fileName=userName, _external=True
            )
        },
        200,
    )


@getProfileImageRouteBlueprint.route("/userProfile/<path:fileName>")
def serveImage(fileName):
    if os.path.exists(os.path.join(PUBLIC_DIRECTORY_PROFILES, fileName)):
        Log.info(f"userProfile {fileName} found")
        return send_from_directory(
            PUBLIC_DIRECTORY_PROFILES.replace("/backend", ""), fileName
        )
    else:
        Log.warning(f"userProfile {fileName} not found, Sending default image")
        return send_from_directory(
            PUBLIC_DIRECTORY_PROFILES.replace("/backend", ""), "icon"
        )
