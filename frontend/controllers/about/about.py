from frontend.modules import Blueprint, render_template


aboutBlueprint = Blueprint("about", __name__, template_folder="templates", url_prefix="/more")


@aboutBlueprint.route("/about")
def about():
    return render_template("daisyUI/about.html")