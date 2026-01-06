from backend.modules import (
    PUBLIC_DIRECTORY_POSTS,
    Blueprint,
    make_response,
    os,
    send_file,
    send_from_directory,
    url_for,
)

getPostMediaRouteBlueprint = Blueprint("postMedia", __name__)


@getPostMediaRouteBlueprint.route("/getPostMedia/<string:fileName>")
def getPostMedia(fileName):
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
        # return send_from_directory(PUBLIC_DIRECTORY_POSTS, fileName)

        return send_file(
            f"{PUBLIC_DIRECTORY_POSTS.replace('./backend/', '')}/{fileName}"
        )
    else:
        return send_from_directory(PUBLIC_DIRECTORY_POSTS, "icon")
