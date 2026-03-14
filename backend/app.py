from dotenv import load_dotenv

from backend.database import initializeDb
from backend.modules import (
    CORS,
    HOST,
    PORT,
    SEREVR_ALLOWED_UPLOAD_FILE_SIZE,
    Flask,
    jsonify,
    os,
)
from backend.repository.getReadyRole import getReadyRole
from backend.tasks import startWorker
from backend.utils import AppError

load_dotenv()


def runApp():
    # Initialize database
    initializeDb()

    app = Flask(__name__)
    app.secret_key = os.environ.get("APP_SECRET_KEY") or "default_secret_key"
    CORS(
        app,
        supports_credentials=True,
        origins=os.environ.get("ORIGINS").split(",") or ["*"],
    )

    app.config["path"] = "backend/public"
    app.config["MAX_CONTENT_LENGTH"] = SEREVR_ALLOWED_UPLOAD_FILE_SIZE

    # Blueprint for auth
    from backend.routes.v1.auth import authBlueprint

    # Blueprint for post collection of posts
    from backend.routes.v1.collections import (
        collectionBlueprint,
    )

    # Register Bluprint for homeFeed endpoint
    from backend.routes.v1.feed import feedBlueprint

    # Blueprint for notifications
    from backend.routes.v1.notifications import notificationBlueprint

    # Blueprint for posts
    from backend.routes.v1.posts import postsBlueprint

    # Blueprint for posts media content of user
    from backend.routes.v1.returnPostMedia import getPostMediaRouteBlueprint

    # Blueprint for profile image fetch of user
    from backend.routes.v1.returnProfileImage import (
        getProfileImageRouteBlueprint,
    )

    # Blueprint for user profile data
    from backend.routes.v1.users import usersBlueprint

    app.register_blueprint(authBlueprint, url_prefix="/api/v1")
    app.register_blueprint(getProfileImageRouteBlueprint, url_prefix="/api/v1")
    app.register_blueprint(getPostMediaRouteBlueprint, url_prefix="/api/v1")
    app.register_blueprint(postsBlueprint, url_prefix="/api/v1")
    app.register_blueprint(usersBlueprint, url_prefix="/api/v1")
    app.register_blueprint(feedBlueprint, url_prefix="/api/v1")
    app.register_blueprint(collectionBlueprint, url_prefix="/api/v1")
    app.register_blueprint(notificationBlueprint, url_prefix="/api/v1")

    # Register handler for the custom exception

    @app.errorhandler(AppError)
    def handle_custom_error(error: AppError):
        # Log the error, return a custom JSON response or render a custom template
        response = jsonify(
            {
                "code": error.code,
                "error": error.error,
                "description": error.description,
            }
        )
        response.status_code = error.code
        return response

    # getReadyRole
    getReadyRole()
    # Start background worker
    startWorker()

    return app


if __name__ == "__main__":
    app = runApp()
    app.run(debug=True, host=HOST, port=PORT)
