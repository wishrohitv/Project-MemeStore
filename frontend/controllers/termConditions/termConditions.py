from frontend.modules import Blueprint, render_template

termConditionsBlueprint = Blueprint(
    "termConditions",
    __name__,
    template_folder="templates",
    url_prefix="/",
)


@termConditionsBlueprint.route("/termConditions")
def termCondiions():
    return render_template("daisyUI/termConditions.html")
