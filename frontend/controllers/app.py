from frontend.modules import (
    Constants,
    Flask,
    render_template,
)


def createApp():
    app = Flask(
        __name__,
        static_folder="static/daisyUI",  # static folder of app.py
        template_folder="templates/daisyUI",  # templates folder of app.py
    )

    # App secret key
    app.secret_key = Constants.APP_SECRET_KEY

    ## Context processors
    from frontend.controllers.about.about import aboutBlueprint
    from frontend.controllers.guidelines.guidelines import guidelinesBlueprint

    ## Pages
    from frontend.controllers.index.index import indexBlueprint
    from frontend.controllers.login.login import loginBlueprint
    from frontend.controllers.logout.logout import logoutBlueprint
    from frontend.controllers.posts.posts import postsBlueprint
    from frontend.controllers.privacyPolicy.privacyPolicy import privacyPolicyBlueprint
    from frontend.controllers.profile.profile import profileBlueprint
    from frontend.controllers.signup.signup import signupBlueprint
    from frontend.controllers.termConditions.termConditions import (
        termConditionsBlueprint,
    )
    from frontend.utils.contextProcessors.constants import constants
    from frontend.utils.contextProcessors.dateTime import dateTime

    ## Register context processors
    app.context_processor(dateTime)
    app.context_processor(constants)

    # Register Index page
    app.register_blueprint(indexBlueprint)
    # Register Profile page
    app.register_blueprint(profileBlueprint)
    # Register About page
    app.register_blueprint(aboutBlueprint)
    # Register Signup page
    app.register_blueprint(signupBlueprint)
    # Register Login page
    app.register_blueprint(loginBlueprint)
    # Register Logout page
    app.register_blueprint(logoutBlueprint)
    # Register Posts page
    app.register_blueprint(postsBlueprint)
    # Register PrivacyPolicy page
    app.register_blueprint(privacyPolicyBlueprint)
    # Register Term Conditions page
    app.register_blueprint(termConditionsBlueprint)
    # Register Guidelines page
    app.register_blueprint(guidelinesBlueprint)

    # Error handler
    @app.errorhandler(404)
    # @app.errorhandler(werkzeug.exceptions.BadRequest)
    def handle_bad_request(e):
        return render_template("badRequest.html"), 404

    # app.url_map.strict_slashes=True
    # print(app.url_map)
    return app
