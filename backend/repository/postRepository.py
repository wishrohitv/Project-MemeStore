from backend.database import engine
from backend.models import (
    AgeRating,
    Bookmark,
    Likes,
    Posts,
    Profile,
    ReportedPosts,
    Reposts,
    Users,
)
from backend.modules import (
    API_ROOT_URL,
    PUBLIC_DIRECTORY_POSTS,
    USE_CLOUDINARY_STORAGE,
    aliased,
    delete,
    exists,
    func,
    make_response,
    or_,
    os,
    select,
    sessionmaker,
    update,
    url_for,
)
from backend.utils import Log, deleteMedia

from .feedRepository import queryPosts

Session = sessionmaker(bind=engine)
session = Session()


def _createPost(
    userID: int,
    text: str | None,
    tags: str | None,
    mediaUrl: str | None,
    mediaPublicID: str | None,
    fileType: str | None,
    fileExtension: str | None,
    ageRating: str,
    category: int,
    parentPostID: int | None = None,
    isReplie: bool = False,
    visibility: bool = True,
):
    try:
        newPost = Posts(
            userID=userID,
            text=text,
            tags=tags,
            mediaUrl=mediaUrl,
            mediaPublicID=mediaPublicID,
            fileType=fileType,
            fileExtension=fileExtension,
            visibility=visibility,
            ageRating=ageRating,
            category=category,
            isReplie=isReplie,
            parentPostID=parentPostID,
        )
        session.add(newPost)
        session.commit()
        session.close()
        Log.info("post added to table successfully")
        return make_response({"message": "post upload successfully"}, 200)
    except Exception as e:
        session.rollback()
        Log.critical(str(e))
        raise Exception(str(e))


def _postToggleLike(sessionUserID: int, postID: int):
    try:
        isAlreadyLiked = (
            session.query(Likes)
            .filter(Likes.userID == sessionUserID, Likes.postID == postID)
            .first()
        )
        if not isAlreadyLiked:
            # add like to post
            likePost = Likes(postID=postID, userID=sessionUserID)
            session.add(likePost)
            session.commit()
            session.close()
            return make_response(
                {"isLiked": True, "message": "Post liked successfully"}, 201
            )
        else:
            # remove like from post
            deLike = delete(Likes).filter(
                Likes.userID == sessionUserID, Likes.postID == postID
            )
            session.execute(deLike)
            session.commit()
            return make_response(
                {"isLiked": False, "message": "Post like removed successfully"}, 201
            )
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def _postToggleBookmark(sessionUserID: int, postID: int):
    try:
        isAlreadyBookmarked = (
            session.query(Bookmark)
            .filter(Bookmark.userID == sessionUserID, Bookmark.postID == postID)
            .first()
        )
        if not isAlreadyBookmarked:
            # Add bookmark to user
            bookmarkPost = Bookmark(postID=postID, userID=sessionUserID)
            session.add(bookmarkPost)
            session.commit()
            session.close()
            return make_response(
                {"isBookmarked": True, "message": "Post bookmark successfully"}, 201
            )
        else:
            # Remove row from Bookmark
            deLike = delete(Bookmark).filter(
                Bookmark.userID == sessionUserID, Bookmark.postID == postID
            )
            session.execute(deLike)
            session.commit()
            return make_response(
                {
                    "isBookmarked": False,
                    "message": "Post bookmark removed successfully",
                },
                201,
            )
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def _deletePost(postID: int, sessionUserID: int):
    try:
        result = session.query(Posts).filter_by(id=postID, userID=sessionUserID).first()
        # Check ownership of the post
        if not result:
            raise Exception("You do not have permission to delete this post")
        # Delete the media
        if USE_CLOUDINARY_STORAGE:
            deleteMedia([result.mediaPublicID])
        else:
            filepath = os.path.join(
                PUBLIC_DIRECTORY_POSTS, f"{result.mediaPublicID}.{result.fileType}"
            )
            if os.path.exists(filepath):
                os.remove(filepath)
        session.delete(result)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def _repostPost(postID: int, sessionUserID: int):
    # Toggle repost
    try:
        isRepost = (
            session.query(Reposts)
            .filter_by(postID=postID, userID=sessionUserID)
            .first()
        )
        if isRepost:
            stmt = delete(Reposts).where(
                Reposts.postID == postID, Reposts.userID == sessionUserID
            )
            session.execute(stmt)
            session.commit()
            return make_response(
                {"message": "Post repost removed successfully", "isReposted": False},
                201,
            )
        else:
            repost = Reposts(postID=postID, userID=sessionUserID)
            session.add(repost)
            session.commit()
            return make_response(
                {"message": "Post reposted successfully", "isReposted": True}, 201
            )
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def _updatePost(
    postID: int,
    sessionUserID: int,
    title: str | None = None,
    tags: str | None = None,
    ageRating: AgeRating | None = None,
    category: int | None = None,
    visibility: bool | None = None,
):
    try:
        updateValue = {}
        if title:
            updateValue["title"] = title
        if tags:
            updateValue["tags"] = tags
        if ageRating:
            updateValue["ageRating"] = ageRating
        if category:
            updateValue["category"] = category
        if visibility is not None:
            updateValue["visibility"] = visibility

        stmt = update(Posts).where(Posts.id == postID).values(updateValue)
        session.execute(stmt)
        session.commit()
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def _userPosts(
    userName: str,
    sessionUserID: int | None = None,
    category: int | None = None,
    orderBy="recent",
    fetchTemplate: bool = False,
    fetchBookmarked: bool = False,
    limit: int = 10,
    offset: int = 0,
):
    """
    Check if user is logged and sessionUserID = userName then fetch private posts too
    if user is logged but sessionUserID != userName then fetch public posts only
    else fetch public posts only
    """

    conditions = []
    if fetchTemplate:
        conditions.append(Posts.isTemplate)

    if not sessionUserID:
        conditions.append(Posts.visibility)

    conditions.append(Users.userName == userName)

    user = session.query(Users).where(Users.userName == userName).first()
    if not user:
        return make_response({"error": "User not found"}, 404)
    if user.accountStatus == "suspended":
        return make_response({"error": "Account is suspended"}, 404)
    if user.accountStatus == "deleted":
        return make_response({"error": "Account is deleted"}, 404)
    if user.accountStatus == "banned":
        return make_response({"error": "Account is banned"}, 404)

    if fetchBookmarked:
        conditions.append(Bookmark.userID == user.id)

    posts = queryPosts(
        conditions=conditions, offset=offset, limit=limit, sessionUserID=sessionUserID
    )
    if len(posts) > 0:
        return make_response({"payload": posts}, 200)
    else:
        return make_response({"payload": []}, 200)


def _getPostMedia(
    postID: int,
    offset: int = 0,
    limit: int = 10,
) -> tuple[str, str, str, str] | None:
    try:
        post = (
            session.query(
                Posts.text,
                Posts.mediaUrl,
                Posts.mediaPublicID,
                Posts.fileExtension,
            )
            .filter(Posts.id == postID)
            .first()
        )
        if not post:
            return None
        return tuple(post)
    except Exception as e:
        print(f"Error fetching post media: {e}")
        return None


def _getPostByIDorReplies(
    postID: int,
    sessionUserID: int | None = None,
    fetchReplies: bool = False,
    limit: int = 10,
    offset: int = 0,
):
    conditions = []
    if fetchReplies:
        conditions.append(Posts.parentPostID == postID)
        conditions.append(
            Posts.isReplie
        )  # `not Posts.isReplie` is not working as false
        conditions.append(Posts.visibility)  # Fetch only public posts
    else:
        #  Fetch post by ID
        conditions.append(Posts.id == postID)

        # Check post visibility
        if sessionUserID:
            # Check owner of the post
            post = session.query(Posts).where(Posts.id == postID).first()
            if not post:
                return make_response({"error": "Post not found"}, 404)

            # Check whether post's visibility is true or false
            if not post.visibility:
                return make_response({"error": "Post is private"}, 403)

            if post.userID == sessionUserID:
                # Give the access to the private post to owner
                # Note : implement superadmin and moderator can access private post for enquiry
                conditions.append(not Posts.visibility)
            else:
                conditions.append(Posts.visibility)
    postsOrReplie = queryPosts(
        conditions=conditions, offset=offset, limit=limit, sessionUserID=sessionUserID
    )
    if postsOrReplie:
        if len(postsOrReplie) == 0:
            return make_response(
                {
                    "payload": [],
                    "message": "No replies found or post dosen't exists",
                },
                200,
            )
        return make_response({"payload": postsOrReplie}, 200)
    else:
        return make_response({"error": "Post not found"}, 404)


def _reportPost(sessionUserID: int, postID: int, reason: str):
    try:
        post = ReportedPosts(
            reportedBy=sessionUserID, postID=postID, description=reason
        )
        session.add(post)
        session.commit()
        session.close()
        return make_response({"message": "Post reported successfully"}, 201)
    except Exception as e:
        session.rollback()
        session.close()
        print(e)
        return make_response({"errror": f"{e}"}, 500)
