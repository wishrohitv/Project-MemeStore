from frontend.models.userModel import UserModel
from frontend.modules import (
    Blueprint,
    Constants,
    flash,
    json,
    redirect,
    render_template,
    request,
    requests,
    session,
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
    connection = requests.get(
        f"{Constants.apiUser}/{userName}",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    if connection.status_code == 200:
        userData = json.loads(connection.text)
        flash("User profile showing")
        userProfile = userData["payload"]
        return render_template(
            "daisyUI/profile.html",
            userData=UserModel(
                id=userProfile["id"],
                bio=userProfile["bio"],
                age=userProfile.get("age"),
                followerCount=userProfile["followerCount"],
                followingCount=userProfile["followingCount"],
                name=userProfile["name"],
                userName=userProfile["userName"],
                email=userProfile["email"],
                joinDate=userProfile["joinDate"],
                role=userProfile["role"],
                country=userProfile["country"],
                accountStatus=userProfile["accountStatus"],
            ),
        )
    else:
        return render_template("badRequest.html")


@profileBlueprint.route("/<userName>/edit", methods=["GET", "POST"])
def editProfile(userName):
    if request.method == "POST":
        # if 'file' not in request.files:
        #     print("no file part")
        #     flash("No file part")
        #     return redirect(url_for("profile.editProfile"))
        # profileImg = request.files["selectedProfileImg"]
        # print(profileImg.headers)
        # print(profileImg.content_type)
        # print(profileImg.mimetype)
        # con = requests.post(apiUserProfile, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlkIjoxLCJuYW1lIjoiTmVyZW5kcmEgTW9kaSIsInVzZXJOYW1lIjoicG1tb2RpIiwiZW1haWwiOiJtb2RpQGdtYWlsLmNvbSIsImpvaW5EYXRlIjoiMjAyNS0wNC0wOCAyMjoyMTozNyIsInJvbGUiOjMsImFjY291bnRTdGF0dXMiOiJhY3RpdmUifSwiZXhwIjoxNzQ0MTYyOTYzLjUyMjg4MX0.8IfWvf1jeclI-_MRRCKUED0s0VR22fOvzOD2gRBSJ0k"})
        # print(con.text)
        return redirect(url_for("profile.editProfile"))
    return render_template("daisyUI/editProfile.html")
