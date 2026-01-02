from backend.database import engine
from backend.models import AccountStatus, Follower, Profile, Sessions, Users
from backend.modules import (
    ACCESS_TOKEN_EXPIRY_MINUTES,
    HTTP_ONLY,
    REFRESH_TOKEN_EXPIRY_MINUTES,
    SECURE_COOKIE,
    aliased,
    delete,
    exists,
    func,
    jsonify,
    make_response,
    or_,
    select,
    sessionmaker,
    update,
)
from backend.utils import (
    decodeJwtToken,
    generateJwtToken,
    matchPassword,
    returnHashedBytes,
)

Session = sessionmaker(bind=engine)
session = Session()


def _createUser(
    name: str,
    userName: str,
    email: str,
    password: str,
    # joinDate,
    role: int,
    accountStatus: AccountStatus,
    country,
):
    # Check if user already exist
    user = (
        session.query(Users)
        .filter(or_(Users.userName == userName, Users.email == email))
        .first()
    )
    if user:
        return make_response(jsonify({"message": "User already exists"}), 400)
    # Add a user
    newUser = Users(
        name=name,
        userName=userName,
        email=email,
        password=returnHashedBytes(password.encode("ascii")),
        role=role,
        accountStatus=accountStatus,
        profile=Profile(country=country),
    )
    session.add(newUser)
    session.commit()
    session.refresh(newUser)
    # Close the session
    session.close()
    userObj = {
        "id": newUser.id,
        "name": newUser.name,
        "userName": newUser.userName,
        "email": newUser.email,
        "joinDate": newUser.joinDate,
        "role": newUser.role,
        "accountStatus": newUser.accountStatus.value,
    }
    print(userObj)
    # TODO: Implement email verification
    return jsonify(userObj)


def _authenticateUser(userName, email, password):
    """
    Check user's account status ["active", "suspended", "banned", "deleted"]
    """
    try:
        # Query the user
        users = (
            session.query(Users)
            .where(or_(Users.email == email, Users.userName == userName))
            .first()
        )
        session.close()
        if not users:
            return make_response({"message": "user does not exist"}, 404)
        if users.accountStatus == AccountStatus.suspended:
            return make_response({"message": "user is suspended"}, 403)
        if users.accountStatus == AccountStatus.banned:
            return make_response({"message": "user is banned"}, 403)
        if users.accountStatus == AccountStatus.deleted:
            return make_response({"message": "user is deleted"}, 403)
        if not matchPassword(password.encode("ascii"), users.password):
            return make_response({"error": "Invalid password"}, 401)
        accessObj = {
            "id": users.id,
            "name": users.name,
            "userName": users.userName,
            "email": users.email,
            "joinDate": users.joinDate.strftime("%Y-%m-%d %H:%M:%S"),
            "role": users.role,
            "accountStatus": users.accountStatus.value,
        }
        refreshObj = {
            "id": users.id,
            "name": users.name,
            "userName": users.userName,
        }

        accessToken = generateJwtToken(
            userData=accessObj, expireInMinute=ACCESS_TOKEN_EXPIRY_MINUTES
        )
        refreshToken = generateJwtToken(
            userData=refreshObj, expireInMinute=REFRESH_TOKEN_EXPIRY_MINUTES
        )

        stmt = Sessions(userID=users.id, refreshToken=refreshToken)
        session.add(stmt)
        session.commit()
        # Close the session
        session.close()

        return (
            {"userID": users.id, "userName": users.userName},
            accessToken,
            refreshToken,
        )
    except Exception as e:
        raise Exception(str(e))


def _refreshTokens(refreshToken: str):
    try:
        decodedData = decodeJwtToken(refreshToken)
        if not decodedData:
            raise Exception("Token expired")
        userID = decodedData["payload"]["id"]
        # TODO: check account status too
        # if accountStatus == "active":
        #     pass
        stmt = (
            select(Users, Sessions.refreshToken)
            .join_from(Users, Sessions)
            .where(Sessions.refreshToken == refreshToken)
        )
        userResult = session.execute(stmt).first()
        user: Users = userResult[0]
        storedRefreshToken: str = userResult[1]
        # user = session.scalar(stmt)
        if not userResult or refreshToken != storedRefreshToken:
            raise Exception("Invalid refresh token")

        newAccessToken = generateJwtToken(
            userData={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "userName": user.userName,
                "joinDate": user.joinDate.strftime("%Y-%m-%d %H:%M:%S"),
                "accountStatus": user.accountStatus.value,
            },
            expireInMinute=ACCESS_TOKEN_EXPIRY_MINUTES,
        )
        newRefreshToken = generateJwtToken(
            userData={
                "id": user.id,
                "name": user.name,
                "userName": user.userName,
            },
            expireInMinute=REFRESH_TOKEN_EXPIRY_MINUTES,
        )
        session.close()
        stmt = Sessions(userID=user.id, refreshToken=refreshToken)
        session.add(stmt)
        session.commit()
        session.close()
        return (
            {"userID": user.id, "userName": user.userName},
            newAccessToken,
            newRefreshToken,
        )
    except Exception as e:
        raise Exception(e)


def _logout(refreshToken: str, userID: int, allDevices=False):
    try:
        user = None
        if allDevices:
            user = session.query(Sessions).filter_by(userID=userID).first()
        else:
            user = session.query(Sessions).filter_by(refreshToken=refreshToken).first()

        if not user:
            raise Exception("User session not found")
        if allDevices:
            stmt = delete(Sessions).where(Sessions.userID == userID)
            session.execute(stmt)
            session.commit()
            session.close()
        else:
            stmt = delete(Sessions).filter_by(refreshToken=refreshToken)
            session.execute(stmt)
            session.commit()
            session.close()
    except Exception as e:
        raise Exception(e)


def addFollower(sessionUserID: int, userID: int):
    try:
        checkIsAlreadyFollow = select(
            exists().where(
                Follower.userID == userID, Follower.followerID == sessionUserID
            )
        )
        isAlreadyFollows = session.scalar(
            checkIsAlreadyFollow
        )  # Scalar select first row from table
        # print(checkIsAlreadyFollow)
        # print(isAlreadyFollows)

        # If isAlreadyFollows
        if not isAlreadyFollows:
            newFollower = Follower(userID=userID, followerID=sessionUserID)
            session.add(newFollower)
            session.commit()
            session.close()
            print(newFollower)
            return make_response({"message": "follower added successfully"}, 201)
        else:
            return make_response(
                {"message": "user already follows requested user"}, 409
            )
    except Exception as e:
        return make_response({"error": f"{e}"}, 500)


def getUserProfile(
    _userName: str | None = None,
    _email: str | None = None,
    _userID: int | None = None,
    _isLogged: bool = False,
):
    """
    Retrieve a user profile based on the input parameters: userName, email, or uid. Only
    one field should be provided to successfully query a user. If no valid argument
    is passed, an error response is returned. The function queries the database, closes
    the session afterward, and fetches details of the user(s). If a user exists, their
    profile details are returned in the response payload; otherwise, an error message
    is provided.

    :param _userName: Username of the user to be queried
    :param _email: Email address of the user to be queried
    :param _userID: Unique identifier of the user to be queried
    :return: JSON response containing the user's data if the user exists or an error
             message
    """

    # User's follower count
    followerCount = aliased(Follower)
    # User's following count
    followingCount = aliased(Follower)

    # Check if any arguments are passed
    if _userID:
        # Query the user
        stmt = (
            select(
                Users,
                Profile.bio,
                Profile.country,
                func.count(followerCount.userID).label("followerCount"),
                func.count(followingCount.followerID).label("followingCount"),
            )
            .select_from(Users)
            .outerjoin(followerCount, followerCount.userID == Users.id)
            .outerjoin(followingCount, followingCount.followerID == Users.id)
            .outerjoin(Profile, Profile.userID == Users.id)
            .where(Users.id == _userID)
            .group_by(Users.id, Profile.id)
        )
        users = session.execute(stmt).all()

    elif _userName:
        # Query the user
        stmt = (
            select(
                Users,
                Profile.bio,
                Profile.country,
                func.count(followerCount.userID).label("followerCount"),
                func.count(followingCount.followerID).label("followingCount"),
            )
            .select_from(Users)
            .outerjoin(followerCount, followerCount.userID == Users.id)
            .outerjoin(followingCount, followingCount.followerID == Users.id)
            .outerjoin(Profile, Profile.userID == Users.id)
            .where(Users.userName == _userName)
            .group_by(Users.id, Profile.id)
        )
        users = session.execute(stmt).all()

    elif _email:
        # Query the user
        stmt = (
            select(
                Users,
                Profile.bio,
                Profile.country,
                func.count(followerCount.userID).label("followerCount"),
                func.count(followingCount.followerID).label("followingCount"),
            )
            .select_from(Users)
            .outerjoin(followerCount, followerCount.userID == Users.id)
            .outerjoin(followingCount, followingCount.followerID == Users.id)
            .outerjoin(Profile, Profile.userID == Users.id)
            .where(Users.email == _email)
            .group_by(Users.id, Profile.id)
        )
        users = session.execute(stmt).all()

    else:
        return make_response({"message": "Invalid argument passed"}, 404)
    # Close the session
    session.close()

    if users:
        usersDict = []
        for user in users:
            userObj = {
                "id": user[0].id,
                "name": user[0].name,
                "userName": user[0].userName,
                "followerCount": user[3],
                "followingCount": user[4],
                "bio": user[1],
                "country": user[2],
                "email": user[0].email,
                "joinDate": user[0].joinDate.strftime("%Y-%m-%d %H:%M:%S"),
                "role": user[0].role,
                "accountStatus": user[0].accountStatus.value,
            }
            usersDict.append(userObj)
            print(usersDict)
        return make_response({"payload": usersDict[0]}, 200)
    else:
        return make_response({"message": "user does not exist"}, 404)
