from frontend.modules import (
    Blueprint,
    Constants,
    json,
    redirect,
    render_template,
    request,
    requests,
    session,
    url_for,
)

loginBlueprint = Blueprint(
    "login", __name__, template_folder="templates", url_prefix="/auth"
)


@loginBlueprint.route("/login")
def login():
    return render_template("daisyUI/login.html")
