from frontend.modules import Blueprint, redirect, session

logoutBlueprint = Blueprint("logout", __name__)

@logoutBlueprint.route("/logout")
def logout():
    session.pop("email")
    return redirect("/")