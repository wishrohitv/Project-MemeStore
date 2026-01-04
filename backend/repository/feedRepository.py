from backend.database import engine
from backend.models import Bookmark, Category, Likes, Posts, Users
from backend.modules import (
    API_ROOT_URL,
    USE_CLOUDINARY_STORAGE,
    aliased,
    exists,
    func,
    json,
    make_response,
    request,
    select,
    sessionmaker,
    url_for,
)

Session = sessionmaker(bind=engine)
session = Session()


def getHomeFeed(
    category: list = [],
    offset: int = 0,
    sessionUserID: int | None = None,
):
    # Get feed data from database alog with userName of author of post
    likeCount = aliased(Likes)
    bookmarkCount = aliased(Bookmark)
    getFeedData = (
        select(
            Users.userName,
            Posts,
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
        .where(Posts.visibility)  # = True
        .outerjoin(likeCount, likeCount.postID == Posts.id)
        .outerjoin(bookmarkCount, bookmarkCount.postID == Posts.id)
        .group_by(Posts.id, Users.userName)
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
                    "likeCount": feed[2],
                    "bookmarkCount": feed[3],
                    "isLiked": feed[4],
                    "isBookmarked": feed[5],
                }
                feedObj.append(data)
            return make_response({"payload": feedObj}, 200)
        else:
            return make_response({"payload": []}, 200)

    except Exception as e:
        return make_response({"error": f"{e}"}, 401)
