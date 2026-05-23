from config import API_ENDPOINTS
from modules import Blueprint, request
from repository.search_repository import _search_prediction
from utils import BadRequestError, SuccessResponse

search_blueprint = Blueprint("search", __name__)

route = API_ENDPOINTS()


@search_blueprint.route("/", methods=["GET"])
def search():
    query = request.args.get("q")
    limit = request.args.get("limit", default=10)
    offset = request.args.get("offset", default=0)
    filter_by = request.args.get("filter_by", default="all")

    if filter_by not in ["people", "post", "all"]:
        raise BadRequestError("Invalid filter flag")
    if int(limit) > 15 or int(offset) > 10:
        raise BadRequestError("Invalid limit or offset")

    return SuccessResponse(data={}, message="Fetch data successfully", status_code=200)


@search_blueprint.route("/predict", methods=["GET"])
def search_predict():
    query = request.args.get("q")
    if not query:
        raise BadRequestError("No search query found")
    _search_prediction(query)
    return SuccessResponse(data={}, message="Fetch data successfully", status_code=200)


@search_blueprint.route("/trending", methods=["GET"])
def trending():
    """
    Trending hashtags
    Fetch trending hashtags by filtering post text
    """
    return SuccessResponse(data={}, message="Fetch data successfully", status_code=200)


@search_blueprint.route("/trending/<string:hash_tag>/post", methods=["GET"])
def trending_posts(hash_tag: str):
    """
    Trending posts
    Fetch post by filtering post text
    """
    limit = request.args.get("limit", default=10)
    offset = request.args.get("offset", default=0)

    if int(limit) > 15 or int(offset) > 10:
        raise BadRequestError("Invalid limit or offset")

    return SuccessResponse(data={}, message="Fetch data successfully", status_code=200)
