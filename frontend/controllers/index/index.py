from frontend.modules import Blueprint, render_template, session


indexBlueprint = Blueprint(
    "index",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@indexBlueprint.route("/")
def index():
    print(session.get("userName"), session.get("uid"))
    return render_template("daisyUI/index.html")