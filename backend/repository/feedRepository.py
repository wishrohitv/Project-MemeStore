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
    limit: int = 10,
    fetchTemplate: bool = False,
    sessionUserID: int | None = None,
):
    # Fetch only public posts and isReplie false
    conditions = [Posts.visibility, Posts.isReplie.is_(False)]
    feed = queryPosts(conditions, category, offset, limit, sessionUserID)
    if feed and len(feed) >= 0:
        return make_response({"payload": feed}, 200)
    else:
        return make_response({"payload": []}, 200)


def queryPosts(
    conditions,
    category: list = [],
    offset: int = 0,
    limit: int = 10,
    sessionUserID: int | None = None,
):
    """
    Global feed and post and replie query function
    """
    # Get feed data from database alog with userName of author of post
    like = aliased(Likes)
    likeCount = (
        select(func.count(like.userID))
        .where(like.postID == Posts.id)
        .correlate(Posts)
        .scalar_subquery()
    )
    bookmark = aliased(Bookmark)
    bookmarkCount = (
        select(func.count(bookmark.userID))
        .where(bookmark.postID == Posts.id)
        .correlate(Posts)
        .scalar_subquery()
    )

    reply = aliased(Posts)
    repliesCount = (
        select(func.count(reply.id))
        .where(reply.parentPostID == Posts.id, reply.isReplie.is_(True))
        .scalar_subquery()
    )
    getFeedData = (
        select(
            Users.userName,
            Posts,
            Profile.mediaUrl,
            Profile.mediaPublicID,
            Profile.fileExtension,
            likeCount.label("likeCount"),
            bookmarkCount.label("bookmarkCount"),
            repliesCount.label("replieCount"),
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
        .limit(limit)
        .offset(offset)
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
                    "parentPostID": feed[1].parentPostID
                    if not feed[1].isReplie
                    else None,  # Check if post's 'isReplie=True' send None because
                    "createdAt": feed[1].createdAt,
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
                    "replieCount": feed[7],
                    "isLiked": feed[8],
                    "isBookmarked": feed[9],
                }
                feedObj.append(data)

            return feedObj
        else:
            return []

    except Exception as e:
        raise Exception(e)
