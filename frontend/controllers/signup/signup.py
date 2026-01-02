from frontend.modules import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Constants,
    requests,
    json,
)

signupBlueprint = Blueprint(
    "signup",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/auth",
)


# Signup route
@signupBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        userName = request.form["userName"]
        email = request.form["email"]
        password = request.form["password2"]
        print(request.form)

        bodyData = {
            "name": name,
            "userName": userName,
            "email": email,
            "password": password,
            "role": 3,
            "accountStatus": "active",
            "country": "india",
        }

        headers = {"Content-type": "application/json"}
        connection = requests.post(
            url=Constants.apiCreateUser, headers=headers, json=json.dumps(bodyData)
        )

        print(connection.text)
        return redirect(url_for("signup.verifyEmail"))
    return render_template("daisyUI/signup.html")


# Verify email route
@signupBlueprint.route("/verifyEmail", methods=["GET", "POST"])
def verifyEmail():
    return render_template("daisyUI/verifyEmail.html")
