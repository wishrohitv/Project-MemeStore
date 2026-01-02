class Constants:
    # App name
    APP_NAME = "MemeStore"

    # App version
    APP_VERSION = "1.0.0"

    # Host
    HOST = "0.0.0.0"

    # Port
    PORT = 8000

    APP_SECRET_KEY = "thisIsYourSuperSecretKey"

    # Api for create new user
    apiCreateUser = "http://127.0.0.1:5000/api/v1/createUser"

    apiAuthenticateUser = "http://127.0.0.1:5000/api/v1/authenticateUser"
    apiUploadPosts = "http://127.0.0.1:5000/api/v1/uploadPosts"
    apiUser = "http://127.0.0.1:5000/api/v1/users"

    # Posts age ratings type
    # Posts age ratings
    POSTS_AGE_RATINGS = ["none", "13", "NSFW"]
