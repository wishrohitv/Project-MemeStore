from frontend.modules import Blueprint, render_template, session, request, redirect


postsBlueprint = Blueprint(
    "posts",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/posts"
)

@postsBlueprint.route("/")
def posts():
    return render_template("daisyUI/posts.html")

@postsBlueprint.route("/createPosts", methods=["GET", "POSt"])
def createPosts():
    # if request.method == "POST":
    #     fileObject = request.files
    #     title = request.form.get("title")
    #     tags = request.form.get("tags")
    #     visibility = request.form.get("visibility")
    #     ageRating = request.form.get("ageRating")
    #     category = request.form.get("category")
    #     print(request.form)
    #     print(fileObject, title, tags, visibility, ageRating, category)
    #     return redirect("/")
    return render_template("daisyUI/createPosts.html")