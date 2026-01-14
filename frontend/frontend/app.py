from frontend.modules import (
    Constants,
    Flask,
    render_template,
)


def createApp():
    app = Flask(
        __name__,
        static_folder="static/",  # static folder of app.py
        template_folder="templates/daisyUI",  # templates folder of app.py
    )

    # App secret key
    app.secret_key = Constants.APP_SECRET_KEY

    ## Context processors
    from frontend.utils.contextProcessors.constants import constants
    from frontend.utils.contextProcessors.dateTime import dateTime

    ## Pages

    ## Register context processors
    app.context_processor(dateTime)
    app.context_processor(constants)

    # Register Index page
    @app.route("/*")
    def index():
        return render_template("base.html")

    # Error handler
    @app.errorhandler(404)
    # @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return render_template("badRequest.html"), 404

    # app.url_map.strict_slashes=True
    # print(app.url_map)
    return app
