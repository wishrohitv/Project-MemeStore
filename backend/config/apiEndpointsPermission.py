from backend.config.roles import ROLE
from backend.utils.routeAccess import RouteAccess


class API_ENDPOINTS:
    """
    Role of users who can access api endpoints based on their role
    defined here
    """

    # Auth
    signupUser = RouteAccess(
        routeName="/auth/signup",
        methods=["POST"],
        rolePermission=[],
    )
    loginUser = RouteAccess(
        routeName="/auth/login",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
        partialAccess=True,
    )
    logoutUser = RouteAccess(
        routeName="/auth/logout",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
    )
    refreshToken = RouteAccess(
        routeName="/auth/refresh",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
    )
    genrateOtp = RouteAccess(
        routeName="/auth/generate-otp",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    verifyUser = RouteAccess(
        routeName="/auth/verify",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
        partialAccess=True,
    )

    # User route
    deleteUser = RouteAccess(
        routeName="/user/delete",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["DELETE"],
    )
    suspendUser = RouteAccess(
        routeName="/user/suspend",
        rolePermission=[ROLE.MODERATOR, ROLE.SUPER_ADMIN],
        methods=["PUT"],
    )
    user = RouteAccess(
        routeName="/user",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    userUpdate = RouteAccess(
        routeName="/user/update",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["PUT"],
    )
    userChangeProfile = RouteAccess(
        routeName="/user/profileImg/update",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["PUT"],
    )
    userInSession = RouteAccess(
        routeName="/user/auth",  # session user only
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
    )
    banUser = RouteAccess(
        routeName="/user/ban",
        rolePermission=[ROLE.SUPER_ADMIN],
        methods=["PUT"],
    )
    userAddFollower = RouteAccess(
        routeName="/user/follow",
        rolePermission=[ROLE.USER],
        methods=["POST"],
    )
    userRemoveFollower = RouteAccess(
        routeName="/user/unfollow",
        rolePermission=[ROLE.USER],
        methods=["DELETE"],
    )
    userBlock = RouteAccess(
        routeName="/user/block",
        rolePermission=[ROLE.USER],
        methods=["PUT"],
    )
    userUnblock = RouteAccess(
        routeName="/user/unblock",
        rolePermission=[ROLE.USER],
        methods=["PUT"],
    )
    userReport = RouteAccess(
        routeName="/user/report",
        rolePermission=[ROLE.USER],
        methods=["POST"],
    )
    userReportInpector = RouteAccess(
        routeName="/user/report-inspector",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR],
        methods=["PUT"],
    )

    # Feed
    feed = RouteAccess(
        routeName="/feed",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    # Profile
    uploadProfileImage = RouteAccess(
        routeName="/users/profile/image",
        methods=["POST"],
        rolePermission=[ROLE.USER],
    )
    getProfileImage = RouteAccess(
        routeName="/users/profile/image",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    updateProfile = RouteAccess(
        routeName="/users/profile/update",
        rolePermission=[ROLE.USER],
        methods=["PUT"],
    )
    deleteProfile = RouteAccess(
        routeName="/users/profile/delete",
        rolePermission=[ROLE.USER],
        methods=["DELETE"],
    )
    # Posts
    posts = RouteAccess(
        routeName="/posts",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    uploadPosts = RouteAccess(
        routeName="/posts/upload",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
    )
    repostPosts = RouteAccess(
        routeName="/posts/repost",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
    )
    postLike = RouteAccess(
        routeName="/posts/like",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["PUT"],
    )
    postBookmark = RouteAccess(
        routeName="/posts/bookmark",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["PUT"],
    )
    deletePost = RouteAccess(
        routeName="/posts/delete",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["DELETE"],
    )
    updatePost = RouteAccess(
        routeName="/posts/update",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
    )
    reportPost = RouteAccess(
        routeName="/posts/report",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["POST"],
    )
    reportPostInspector = RouteAccess(
        routeName="/posts/report-inspector",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR],
        methods=["POST"],
    )
    # Replies
    postReplies = RouteAccess(
        routeName="/posts/replies",
        rolePermission=[ROLE.SUPER_ADMIN, ROLE.MODERATOR, ROLE.USER],
        methods=["GET"],
        partialAccess=True,
    )
    addTemplatePost = RouteAccess(
        routeName="/posts/addTemplate",
        rolePermission=[ROLE.USER],
        methods=["PUT"],
    )
    removeTemplatePost = RouteAccess(
        routeName="/posts/removeTemplate",
        rolePermission=[ROLE.USER],
        methods=["DELETE"],
    )

    # Collection
    collection = RouteAccess(
        routeName="/collections", rolePermission=[ROLE.USER], methods=["GET"]
    )
    createCollection = RouteAccess(
        routeName="/collections/create", rolePermission=[ROLE.USER], methods=["POST"]
    )
    deleteCollection = RouteAccess(
        routeName="/collections/delete", rolePermission=[ROLE.USER], methods=["DELETE"]
    )
    updateCollection = RouteAccess(
        routeName="/collections/update", rolePermission=[ROLE.USER], methods=["PUT"]
    )
    addPostToCollection = RouteAccess(
        routeName="/collections/addPost", rolePermission=[ROLE.USER], methods=["POST"]
    )
    removePostFromCollection = RouteAccess(
        routeName="/collections/removePost",
        rolePermission=[ROLE.USER],
        methods=["DELETE"],
    )

    @property
    def apiEndpoints(self) -> dict[str, RouteAccess]:
        """
        endpoint name : route name
        """
        return {
            v.routeName: v
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, RouteAccess)
        }

    @property
    def apiEndpointsPartialAccess(self) -> dict[str, bool]:
        """
        endpoint name : access rule
        """
        return {
            v.routeName: v.partialAccess
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, RouteAccess)
        }
