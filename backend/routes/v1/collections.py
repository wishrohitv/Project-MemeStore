from config import API_ENDPOINTS
from middlewares.verify_client_request import verify_request_middleware
from modules import Blueprint, make_response, request
from repository.collection_repository import (
    _add_post_to_collection,
    _create_collection,
    _delete_collection,
    _remove_post_to_collection,
)
from utils import LoggedUser

collection_blueprint = Blueprint("collections", __name__)


route = API_ENDPOINTS()


@collection_blueprint.route(
    route.collection.route_name, methods=route.collection.methods
)
@verify_request_middleware(route.collection.route_name)
def collection(logged_user: LoggedUser, *args, **kwargs):
    return make_response({}, 201)


# /collections
@collection_blueprint.route(
    route.collection.route_name, methods=route.collection.methods
)
@verify_request_middleware(route.collection.route_name)
def create_collection(logged_user: LoggedUser, *args, **kwargs):
    session_user_id = logged_user.user_id
    body = request.get_json()
    name = body.get("name")
    description = body.get("description")
    if not name:
        return make_response({"error": "Collection name is required"}, 400)
    try:
        _create_collection(name, session_user_id, description)
        return make_response({"message": "Collection created successfully"}, 201)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /collections/<int:collectionID>/<int:postID>
@collection_blueprint.route(
    route.collection_add_post.route_name,
    methods=route.collection_add_post.methods,
)
@verify_request_middleware(route.collection_add_post.route_name)
def addPost(logged_user: LoggedUser, *args, **kwargs):
    session_user_id = logged_user.user_id
    collectionID = kwargs.get("collectionID")
    postID = kwargs.get("postID")
    if not collectionID or not postID:
        return make_response({"error": "Collection ID and Post ID are required"}, 400)
    try:
        _add_post_to_collection(collectionID, session_user_id, postID)
        return make_response({"message": "Post added to collection successfully"}, 201)
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /collections/<int:collection_id>/<int:post_id>
@collection_blueprint.route(
    f"{route.collection_remove_post.route_name}",
    methods=route.collection_remove_post.methods,
)
@verify_request_middleware(route.collection_remove_post.route_name)
def removePosts(logged_user: LoggedUser, *args, **kwargs):
    session_user_id = logged_user.user_id
    collectionID = kwargs.get("collection_id")
    postID = kwargs.get("post_id")
    if not collectionID or not postID:
        return make_response({"error": "Collection ID and Post ID are required"}, 400)
    try:
        _remove_post_to_collection(collectionID, session_user_id, postID)
        return make_response(
            {"message": "Post removed from collection successfully"}, 200
        )
    except Exception as e:
        return make_response({"error": str(e)}, 500)


# /collections DELETE
@collection_blueprint.route(
    route.collection_delete.route_name,
    methods=route.collection_delete.methods,
)
@verify_request_middleware(route.collection_delete.route_name)
def delete_collection(logged_user: LoggedUser, *args, **kwargs):
    session_user_id = logged_user.user_id
    collectionID = kwargs.get("collectionID")
    if not collectionID:
        return make_response({"error": "Collection ID is required"}, 400)
    try:
        _delete_collection(collectionID, session_user_id)
        return make_response({"message": "Collection deleted successfully"}, 200)
    except Exception as e:
        return make_response({"error": str(e)}, 500)
