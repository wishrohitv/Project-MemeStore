from frontend.modules import Blueprint, render_template

guidelinesBlueprint = Blueprint(
    "guidelines",
    __name__,
    template_folder="templates",
    url_prefix="/",
)


@guidelinesBlueprint.route("/guidelines")
def guidelines():
    return render_template("daisyUI/guidelines.html")
