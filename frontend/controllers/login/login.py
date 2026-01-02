from frontend.modules import (
    Blueprint,
    render_template,
    redirect,
    request,
    Constants,
    requests,
    json,
    url_for,
    session,
)

loginBlueprint = Blueprint(
    "login", __name__, template_folder="templates", url_prefix="/auth"
)


@loginBlueprint.route("/login", methods=["GET", "POST"])
def login():
    #     if request.method == "POST":
    # #         print(request.form)
    # #
    # #         bodyData = {
    # #             "email": request.form.get("email"),
    # #             "userName": request.form.get("userName"),
    # #             "password": request.form.get("password")
    # #         }
    # #         headers = {'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlkIjoyLCJuYW1lIjoiS3Agb2xpIiwidXNlck5hbWUiOiJvbGkiLCJlbWFpbCI6Im9saUBnbWFpbC5jb20iLCJqb2luRGF0ZSI6IjIwMjUtMDQtMDcgMjM6MDI6MDciLCJyb2xlIjozLCJhY2NvdW50U3RhdHVzIjoiYWN0aXZlIn0sImV4cCI6MTc0NDA3NzUyNy44MDc0OTR9.7kvbaK1epSxqcZJRv88psYlkkD8_nn8a0JW0FCyQtiY'
    # # ,                   'Content-type': 'application/json'}
    # #         connection = requests.post(apiAuthenticateUser, headers=headers, json=bodyData)
    # #         print(connection.text)
    # #         session["email"] = request.form.get("email")
    #         return redirect(url_for("index.index"))
    return render_template("daisyUI/login.html")
