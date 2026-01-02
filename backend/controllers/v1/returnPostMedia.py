from backend.modules import (
    Blueprint,
    make_response,
    os,
    PUBLIC_DIRECTORY_POSTS,
    send_from_directory,
    send_file,
    url_for,
)

getPostMediaRouteBlueprint = Blueprint("postMedia", __name__)


@getPostMediaRouteBlueprint.route("/getPostMedia/<string:fileName>")
def getPostMedia(fileName):
    print(fileName)
    return make_response(
        {
            "postMediaLink": url_for(
                "postMedia.servePostMedia", fileName=fileName, _external=True
            )
        },
        200,
    )


@getPostMediaRouteBlueprint.route("/postMedia/<path:fileName>")
def servePostMedia(fileName):
    if os.path.exists(os.path.join(PUBLIC_DIRECTORY_POSTS, fileName)):
        return send_from_directory(PUBLIC_DIRECTORY_POSTS, fileName)
    else:
        return send_from_directory(PUBLIC_DIRECTORY_POSTS, "icon")
