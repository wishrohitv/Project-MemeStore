from frontend.modules import (
    Blueprint,
    Constants,
    flash,
    json,
    redirect,
    render_template,
    request,
    url_for,
)

profileBlueprint = Blueprint(
    "user",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/user",
)


@profileBlueprint.route("/<string:userName>")
def profile(userName):
    return render_template("daisyUI/profile.html")


@profileBlueprint.route("/<userName>/edit")
def editProfile(userName):
    return render_template("daisyUI/editProfile.html")
