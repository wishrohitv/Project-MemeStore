from backend.database import engine
from backend.models import Category, Posts, Users
from backend.modules import (
    API_ROOT_URL,
    USE_CLOUDINARY_STORAGE,
    json,
    make_response,
    request,
    select,
    sessionmaker,
    url_for,
)

Session = sessionmaker(bind=engine)
session = Session()


def getHomeFeed(category: str = "all", offset: int = 0):
    # Get feed data from database alog with userName of author of post
    getFeedData = (
        select(
            Users.userName,
            Posts,
            # Posts.id,
            # Posts.title,
            # Posts.tags,
            # Posts.mediaUrl,
            # Posts.mediaPublicID,
            # Posts.fileType,
            # Posts.fileExtension,
            # Posts.visibility,
            # Posts.ageRating,
            # Posts.category,
        )
        .join_from(Users, Posts)
        .where(Posts.visibility == True)
    )  # .where(Posts.userID == Users.id)
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
        return make_response({"error": f"{e}"}, 401)


def getUsersPostsFeed(category: str = "all", offset: int = 0, userID: int = None):
    # Get feed data from database alog with userName of author of post
    getFeedData = (
        select(
            Users.userName,
            Posts,
            # Posts.id,
            # Posts.title,
            # Posts.tags,
            # Posts.mediaUrl,
            # Posts.fileType,
            # Posts.fileExtension,
            # Posts.visibility,
            # Posts.ageRating,
            # Posts.category,
        )
        .join_from(Users, Posts)
        .where(Posts.userID == userID)
    )
    # print(getFeedData)
    getFeed = session.execute(getFeedData).all()
    # print(getFeed)
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
                    "mediaPublicID": feed[1].mediaPublicID,
                    "fileType": feed[1].fileType,
                    "fileExtension": feed[1].fileExtension,
                    "visibility": feed[1].visibility,
                    "ageRating": feed[1].ageRating.value,
                    "category": feed[1].category,
                    "postUserPicUrl": f"{API_ROOT_URL}{url_for('profileImage.serveImage', fileName=feed[0])}",
                    "postMediaUrl": feed[1].mediaUrl
                    if USE_CLOUDINARY_STORAGE
                    else f"{API_ROOT_URL}{url_for('postMedia.servePostMedia', fileName=f'{feed[1].postUrl}.{feed[1].fileExtension}')}",
                }
                feedObj.append(data)
            return make_response({"payload": feedObj}, 200)
        else:
            return make_response({"payload": []}, 200)

    except Exception as e:
        return make_response({"error": f"{e}"}, 401)
