from frontend.modules import Blueprint, render_template

privacyPolicyBlueprint = Blueprint(
    "privacyPolicy",
    __name__,
    template_folder="templates",
    url_prefix="/",
)


@privacyPolicyBlueprint.route("/privacyPolicy")
def privacyPolicy():
    return render_template("daisyUI/privacyPolicy.html")
