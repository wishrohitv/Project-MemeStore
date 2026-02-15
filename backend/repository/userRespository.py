from backend.database import engine, redisClient
from backend.models import (
    AccountStatus,
    BlockedUsers,
    Follower,
    Profile,
    ReportedUsers,
    Sessions,
    Users,
)
from backend.modules import (
    ACCESS_TOKEN_EXPIRY_MINUTES,
    API_ROOT_URL,
    HTTP_ONLY,
    PUBLIC_DIRECTORY_PROFILES,
    REFRESH_TOKEN_EXPIRY_MINUTES,
    SECURE_COOKIE,
    USE_CLOUDINARY_STORAGE,
    USE_EMAIL_SERVICE,
    aliased,
    delete,
    exists,
    func,
    jsonify,
    make_response,
    or_,
    os,
    select,
    sessionmaker,
    update,
    url_for,
)
from backend.services.mailService import sendOTP
from backend.utils import (
    LoggedUser,
    decodeJwtToken,
    deleteMedia,
    generateJwtToken,
    getRandomOTP,
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
        "joinDate": newUser.createdAt,
        "role": newUser.role,
        "accountStatus": newUser.accountStatus.value,
    }

    return make_response(
        {"message": "User created successfully", "payload": userObj}, 201
    )


def _generateOTPforUser(userID: int):
    # TODO: Implement rate limiting, and check email bounce
    try:
        user = session.query(Users).filter(Users.id == userID).first()
        if not user:
            return make_response({"error": "User not found"}, 404)
        if user.isVerified:
            return make_response({"message": "User already verified"}, 400)
        otp = getRandomOTP()
        redisClient.set(f"otp:{userID}", otp, ex=600)
        sendOTP(user.email, str(otp))
        session.close()
        return make_response({"message": "OTP generated successfully"}, 200)

    except Exception as e:
        print(e)
        return make_response({"error": "Internal server error"}, 500)


def _verifyUser(userID: int, enteredOTP: str):
    # TODO: check user's verification state then allow for login
    try:
        user = session.query(Users).filter(Users.id == userID).first()
        if not user:
            return make_response({"error": "User not found"}, 404)
        if user.isVerified:
            return make_response({"message": "User already verified"}, 400)

        storedOTP = redisClient.get(f"otp:{userID}")
        if not storedOTP:
            return make_response({"error": "OTP expired"}, 400)
        if storedOTP != enteredOTP:
            return make_response({"error": "Invalid OTP"}, 400)

        user.isVerified = True
        session.commit()
        session.refresh(user)
        session.close()
        return make_response({"message": "OTP verified successfully"}, 200)
    except Exception as e:
        print(e)
        return make_response({"error": "Internal server error"}, 500)


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
            "joinDate": users.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
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

        res = make_response(
            {
                "message": "Logged in successfully",
                "payload": {"userID": users.id, "userName": users.userName},
            },
            200,
        )
        res.set_cookie(
            key="accessToken",
            value=accessToken,
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            max_age=ACCESS_TOKEN_EXPIRY_MINUTES * 60,
        )
        res.set_cookie(
            key="refreshToken",
            value=refreshToken,
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            samesite=None,
            max_age=REFRESH_TOKEN_EXPIRY_MINUTES * 60,
        )
        return res

    except Exception as e:
        print(e)
        raise Exception(e)


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
        session.close()
        if not userResult or refreshToken != userResult[1]:
            return make_response({"error": "Invalid refresh token"}, 401)
        # Delete previous refresh token of user
        stmt = (
            update(Sessions)
            .where(Sessions.refreshToken == refreshToken)
            .values(refreshToken="")
        )
        session.execute(stmt)
        session.commit()
        session.close()

        user: Users = userResult[0]

        newAccessToken = generateJwtToken(
            userData={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "userName": user.userName,
                "joinDate": user.createdAt.strftime("%Y-%m-%d %H:%M:%S"),
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
        stmt = Sessions(userID=user.id, refreshToken=newRefreshToken)
        session.add(stmt)
        session.commit()
        session.close()

        res = make_response(
            {
                "message": "Token refreshed successfully",
                "payload": {"userID": user.id, "userName": user.userName},
            },
            200,
        )
        res.set_cookie(
            key="accessToken",
            value=newAccessToken,
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            max_age=ACCESS_TOKEN_EXPIRY_MINUTES * 60,
        )
        res.set_cookie(
            key="refreshToken",
            value=newRefreshToken,
            httponly=HTTP_ONLY,
            secure=SECURE_COOKIE,
            samesite=None,
            max_age=REFRESH_TOKEN_EXPIRY_MINUTES * 60,
        )
        return res
    except Exception as e:
        print(e)
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


def _addFollower(sessionUserID: int, userID: int):
    try:
        checkIsAlreadyFollow = select(
            exists().where(
                Follower.userID == userID, Follower.followerID == sessionUserID
            )
        )
        isAlreadyFollows = session.scalar(
            checkIsAlreadyFollow
        )  # Scalar select first row from table
        session.close()
        # If isAlreadyFollows
        if not isAlreadyFollows:
            newFollower = Follower(userID=userID, followerID=sessionUserID)
            session.add(newFollower)
            session.commit()
            session.close()
            return make_response(
                {"message": "follower added successfully", "isFollowing": True}, 201
            )
        else:
            return make_response({"error": "user already follows requested user"}, 409)
    except Exception as e:
        session.rollback()
        print(e)
        return make_response({"error": f"{e}"}, 500)


def _removeFollower(
    sessionUserID: int,
    userID: int,
    userRemoveFollower: bool = False,  # User wants to remove his follower itself
):
    """
    Follower can unfollow user
    User can remove another user from following list
    """
    try:
        if userRemoveFollower:
            checkIsAlreadyFollow = select(
                exists().where(
                    Follower.userID == sessionUserID, Follower.followerID == userID
                )
            )
        else:
            checkIsAlreadyFollow = select(
                exists().where(
                    Follower.userID == userID, Follower.followerID == sessionUserID
                )
            )

        isAlreadyFollows = session.scalar(
            checkIsAlreadyFollow
        )  # Scalar select first row from table

        session.close()
        # If isAlreadyFollows
        if not isAlreadyFollows:
            return make_response({"error": "User is not following requested user"}, 409)

        if userRemoveFollower:
            stmt = delete(Follower).where(
                Follower.userID == sessionUserID, Follower.followerID == userID
            )
        else:
            stmt = delete(Follower).where(
                Follower.userID == userID, Follower.followerID == sessionUserID
            )
        session.execute(stmt)
        session.commit()
        return make_response(
            {"message": "user unfollows requested user", "isFollowing": False}, 200
        )
    except Exception as e:
        print(e)
        return make_response({"error": f"{e}"}, 500)


def getUserProfile(
    _userName: str | None = None,
    _email: str | None = None,
    _userID: int | None = None,
    sessionUserID: int | None = None,
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

    try:
        # User's follower count
        followerCount = aliased(Follower)
        # User's following count
        followingCount = aliased(Follower)

        matchBy = {}
        if _userID:
            matchBy["id"] = _userID
        elif _userName:
            matchBy["userName"] = _userName
        elif _email:
            matchBy["email"] = _email
        if len(matchBy) == 0:
            raise ValueError("No match criteria provided")
        # Query the user
        stmt = (
            select(
                Users,
                Profile.bio,
                Profile.country,
                Profile.mediaUrl,
                Profile.mediaPublicID,
                Profile.fileExtension,
                func.count(followerCount.userID).label("followerCount"),
                func.count(followingCount.followerID).label("followingCount"),
                exists(
                    select(Follower).where(Follower.followerID == sessionUserID)
                ).label(
                    "isFollowing"  # Whether session user follows or not
                ),
            )
            .select_from(Users)
            .filter_by(**matchBy)  # Apply matches to User only while in context
            .outerjoin(followerCount, followerCount.userID == Users.id)
            .outerjoin(followingCount, followingCount.followerID == Users.id)
            .outerjoin(Profile, Profile.userID == Users.id)
            .group_by(Users.id, Profile.id)
        )
        users = session.execute(stmt).all()
        # Close the session
        session.close()
        if users:
            usersDict = []
            for user in users:
                userObj = {
                    "id": user[0].id,
                    "name": user[0].name,
                    "userName": user[0].userName,
                    "email": user[0].email if sessionUserID == user[0].id else "",
                    "joinDate": user[0].createdAt.strftime("%Y-%m-%d %H:%M:%S"),
                    "role": user[0].role,
                    "accountStatus": user[0].accountStatus.value,
                    "bio": user[1],
                    "country": user[2],
                    "profileImgUrl": user[3]
                    if USE_CLOUDINARY_STORAGE
                    else f"{API_ROOT_URL}{url_for('profileImage.serveImage', fileName=f'{user[4]}.{user[5]}')}",
                    "followerCount": user[6],
                    "followingCount": user[7],
                    "isFollowing": user[8],
                }
                usersDict.append(userObj)
            return make_response({"payload": usersDict[0]}, 200)
        else:
            return make_response({"error": "user does not exist"}, 404)
    except Exception as e:
        print(e)
        return make_response({"error": f"{e}"}, 500)


def updateProfileImg(
    sessionUserID: int,
    mediaPublicID: str,
    fileExtension: str,
    fileType: str,
    mediaUrl: str | None = None,
):
    try:
        userProfile = (
            session.query(Profile).where(Profile.userID == sessionUserID).first()
        )
        session.close()
        if not userProfile:
            return make_response({"message": "user does not exist"}, 404)

        # Delete previous profile image if exists
        if userProfile.mediaPublicID:
            if USE_CLOUDINARY_STORAGE:
                deleteMedia([userProfile.mediaPublicID])
            else:
                filepath = os.path.join(
                    PUBLIC_DIRECTORY_PROFILES,
                    f"{userProfile.mediaPublicID}.{userProfile.fileType}",
                )
                if os.path.exists(filepath):
                    os.remove(filepath)

        stmt = (
            update(Profile)
            .where(Profile.userID == sessionUserID)
            .values(
                mediaPublicID=mediaPublicID,
                fileExtension=fileExtension,
                fileType=fileType,
                mediaUrl=mediaUrl,
            )
        )
        session.execute(stmt)
        session.commit()
        session.close()
        return make_response({"message": "profile image updated successfully"}, 201)
    except Exception as e:
        print(f"Error updating profile image: {e}")
        return make_response({"error": f"{e}"}, 500)


def updateUser(
    sessionUserID: int,
    name: str | None,
    bio: str | None,
    age: int | None,
    country: str | None,
):
    try:
        user = session.query(Users).where(Users.id == sessionUserID).first()
        if not user:
            return make_response({"message": "user does not exist"}, 404)

        if name:
            # Update the name
            user.name = name
            session.commit()
            session.close()
        updateObj = {}
        if bio:
            updateObj["bio"] = bio
        if age:
            updateObj["age"] = age
        if country:
            updateObj["country"] = country

        if len(updateObj) > 0:
            stmt = (
                update(Profile)
                .where(Profile.userID == sessionUserID)
                .values(**updateObj)
            )
            session.execute(stmt)
            session.commit()
            session.close()
        return make_response({"message": "user updated successfully"}, 201)
    except Exception as e:
        print(f"Error updating user: {e}")
        return make_response({"message": "failed to update user"}, 500)


def _blockUser(sessionUserID: int, userID: int):
    try:
        # Check has user already blocked or not
        stmt = select(
            exists().where(
                BlockedUsers.blockedBy == sessionUserID, BlockedUsers.userID == userID
            )
        )
        user = session.scalar(stmt)
        session.close()
        if not user:
            blockedUser = BlockedUsers(userID=userID, blockedBy=sessionUserID)
            session.add(blockedUser)
            session.commit()
            session.close()
            return make_response(
                {"message": "User blocked successfully", "isBlocked": True}, 201
            )

        return make_response(
            {"error": "User is already blocked", "isBlocked": True}, 409
        )
    except Exception as e:
        session.rollback()
        session.close()
        print(e)
        return make_response({"error": f"{e}"}, 500)


def _unblockUser(sessionUserID: int, userID: int):
    try:
        # Check has user already blocked or not
        stmt = select(
            exists().where(
                BlockedUsers.blockedBy == sessionUserID, BlockedUsers.userID == userID
            )
        )
        user = session.scalar(stmt)
        session.close()
        # Remove the user from the table
        if user:
            stmt = delete(BlockedUsers).where(
                BlockedUsers.blockedBy == sessionUserID, BlockedUsers.userID == userID
            )
            session.execute(stmt)
            session.commit()
            session.close()
            return make_response(
                {"message": "User unblocked successfully", "isBlocked": False}, 201
            )

        return make_response(
            {"error": "User has already unblocked the person", "isBlocked": False}, 409
        )
    except Exception as e:
        session.rollback()
        session.close()
        print(e)
        return make_response({"error": f"{e}"}, 500)


def _reportUser(sessionUserID: int, userID: int, reason: str):
    try:
        stmt = ReportedUsers(
            reportedBy=sessionUserID, userID=userID, description=reason
        )
        session.add(stmt)
        session.commit()
        session.close()
        return make_response({"message": "User reported successfully"}, 201)
    except Exception as e:
        session.rollback()
        session.close()
        print(e)
        return make_response({"error": f"{e}"}, 500)
