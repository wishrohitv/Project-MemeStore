from backend.database import engine
from backend.models import Bookmark, Category, Likes, Posts, Profile, Users
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
        .where(*[Posts.visibility, Posts.parentPostID.is_(None)])
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
            return make_response({"payload": feedObj}, 200)
        else:
            return make_response({"payload": []}, 200)

    except Exception as e:
        return make_response({"error": f"{e}"}, 500)
