from frontend.modules import (
    Blueprint,
    Constants,
    json,
    redirect,
    render_template,
    request,
    requests,
    url_for,
)

signupBlueprint = Blueprint(
    "signup",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)


# Signup route
@signupBlueprint.route("/signup")
def signup():
    return render_template("daisyUI/signup.html")


# Verify email route
@signupBlueprint.route("/verifyEmail")
def verifyEmail():
    return render_template("daisyUI/verifyEmail.html")
