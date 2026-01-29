from backend.database import engine
from backend.models import AgeRating, Bookmark, Likes, Posts, Profile, Users
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
    isReposted: bool = False,
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
            isReposted=isReposted,
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


def _posts(
    userName: str,
    sessionUserID: int | None = None,
    category: int | None = None,
    orderBy="recent",
    limit: int = 12,
):
    # Check if user is logged and sessionUserID = userName then fetch private posts too
    # if user is logged but sessionUserID != userName then fetch public posts only
    # else fetch public posts only

    filterObj = {}

    if sessionUserID:
        user = session.query(Users).filter_by(id=sessionUserID).first()
        if not user:
            filterObj["visibility"] = False
        elif user.userName == userName:
            # filterObj["visibility"] = True
            pass
        else:
            filterObj["visibility"] = False
    else:
        # Here more abstraction can be added for unauthorized user
        filterObj["visibility"] = False

    # Get feed data from database alog with userName of author of post
    getFeedData = (
        select(
            Users.userName,
            Posts,
        )
        .join_from(Users, Posts)
        .filter_by(**filterObj)
    ).where(Users.userName == userName)
    # print(getFeedData)
    getFeed = session.execute(getFeedData).all()

    # Close the session
    session.close()
    try:
        if getFeed:
            feedObj = []
            for feed in getFeed:
                data = {
                    "userName": feed[0],
                    "postID": feed[1].id,
                    "userID": feed[1].userID,
                    "title": feed[1].title,
                    "tags": feed[1].tags,
                    "mediaPulicID": feed[1].mediaPublicID,
                    "fileType": feed[1].fileType,
                    "fileExtension": feed[1].fileExtension,
                    "visibility": feed[1].visibility,
                    "ageRating": feed[
                        1
                    ].ageRating.value,  # Return Enum class from db and get its value from 'ageRating': <PostAgeRating.pg13: 'pg13'>,
                    "category": feed[1].category,
                    "postUserPicUrl": f"{API_ROOT_URL}{url_for('profileImage.serveImage', fileName=feed[0])}",
                    "postMediaUrl": feed[1].mediaUrl
                    if USE_CLOUDINARY_STORAGE
                    else f"{API_ROOT_URL}{url_for('postMedia.servePostMedia', fileName=f'{feed[1].mediaPublicID}.{feed[1].fileExtension}')}",
                }
                feedObj.append(data)
            return make_response({"payload": feedObj}, 200)
        else:
            return make_response({"payload": []}, 200)
    except Exception as e:
        return make_response({"error": str(e), "message": "Internal server error"}, 500)


def _getPostMedia(postID: int) -> tuple[str, str, str, str] | None:
    try:
        post = (
            session.query(
                Posts.title,
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
):
    conditions = []
    if fetchReplies:
        conditions.append(Posts.parentPostID == postID)

        conditions.append(
            Posts.isReposted == False
        )  # `not Posts.isReposted` is not working as false
    else:
        conditions.append(Posts.id == postID)
    if sessionUserID is not None:
        # Check owner of the post
        post = session.query(Posts).where(Posts.id == postID).first()
        if not post:
            return make_response({"error": "Post not found"}, 404)

        if post.userID == sessionUserID:
            # Give the access to the private post to owner
            # Note : implement superadmin and moderator can access private post for enquiry
            conditions.append(not Posts.visibility)
        else:
            conditions.append(Posts.visibility)
    # Get feed data from database alog with userName of author of post
    likeCount = aliased(Likes)
    bookmarkCount = aliased(Bookmark)
    getFeedData = (
        select(
            Users.userName,
            Posts,
            Profile.mediaUrl,
            Profile.mediaPublicID,
            Profile.fileExtension,
            func.count(likeCount.userID).label("likeCount"),
            func.count(bookmarkCount.userID).label("bookmarkCount"),
            exists(
                select(Likes).where(
                    Likes.postID == Posts.id, Likes.userID == sessionUserID
                )
            ).label("isLiked"),
            exists(
                select(Bookmark).where(
                    Bookmark.postID == Posts.id, Bookmark.userID == sessionUserID
                )
            ).label("isBookmarked"),
        )
        .join_from(Users, Posts)
        .join_from(Users, Profile)
        .where(*conditions)
        .outerjoin(likeCount, likeCount.postID == Posts.id)
        .outerjoin(bookmarkCount, bookmarkCount.postID == Posts.id)
        .group_by(
            Posts.id,
            Users.userName,
            Profile.mediaUrl,
            Profile.mediaPublicID,
            Profile.fileExtension,
        )
    )
    getFeed = session.execute(getFeedData).all()

    # Close the session
    session.close()
    try:
        if getFeed:
            feedObj = []
            for feed in getFeed:
                data = {
                    "userName": feed[0],
                    "postID": feed[1].id,
                    "userID": feed[1].userID,
                    "title": feed[1].text,
                    "tags": feed[1].tags,
                    "mediaPulicID": feed[1].mediaPublicID,
                    "fileType": feed[1].fileType,
                    "fileExtension": feed[1].fileExtension,
                    "visibility": feed[1].visibility,
                    "parentPostID": feed[1].parentPostID,
                    "ageRating": feed[
                        1
                    ].ageRating.value,  # Return Enum class from db and get its value from 'ageRating': <PostAgeRating.pg13: 'pg13'>,
                    "category": feed[1].category,
                    "postMediaUrl": feed[1].mediaUrl
                    if USE_CLOUDINARY_STORAGE
                    else f"{API_ROOT_URL}{url_for('postMedia.servePostMedia', fileName=f'{feed[1].mediaPublicID}.{feed[1].fileExtension}')}",
                    "profileImgUrl": feed[2]
                    if USE_CLOUDINARY_STORAGE
                    else f"{API_ROOT_URL}{url_for('profileImage.serveImage', fileName=f'{feed[3]}.{feed[4]}')}",
                    "likeCount": feed[5],
                    "bookmarkCount": feed[6],
                    "isLiked": feed[7],
                    "isBookmarked": feed[8],
                }
                feedObj.append(data)
            if len(feedObj) == 0:
                return make_response(
                    {
                        "payload": [],
                        "message": "No replies found or post dosen't exists",
                    },
                    200,
                )
            return make_response({"payload": feedObj}, 200)
        else:
            return make_response({"error": "Post not found"}, 404)

    except Exception as e:
        return make_response({"error": f"{e}"}, 500)
