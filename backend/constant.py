# App name
APP_NAME: str = "Meme Store"

# App version
APP_VERSION: str = "1.0.0"

# Media storage
USE_CLOUDINARY_STORAGE: bool = False  # If true then cloudinary service will be used for storing user uploaded media file, else local computer storage will be used to store media files


USER_ACCOUNT_STATUS: list[str] = ["active", "suspended", "banned", "deleted"]

ALLOWED_FILE_MIMETYPE_FOR_POST: dict = {
    # mimeType : extension
    "image/jpeg": "jpeg",
    "image/png": "png",
    "image/webp": "webp",
    "video/mp4": "mp4",
}
SEREVR_ALLOWED_UPLOAD_FILE_SIZE: int = 20 * 1024 * 1024  # 20 MB
ALLOWED_IMG_FILE_SIZE: int = 5 * 1024 * 1024  # 5 MB
ALLOWED_VID_FILE_SIZE: int = SEREVR_ALLOWED_UPLOAD_FILE_SIZE  # 20 MB

ALLOWED_FILE_SIZE: dict = {
    "image/jpeg": ALLOWED_IMG_FILE_SIZE,
    "image/png": ALLOWED_IMG_FILE_SIZE,
    "image/webp": ALLOWED_IMG_FILE_SIZE,
    "video/mp4": ALLOWED_VID_FILE_SIZE,
}

PASS_HASH_KEY: bytes = b"hellofromjapan"

JWT_HASH_KEY: str = "YourSuperSecreteJwtHashKsy"

PORT: int = 5000
HOST: str = "0.0.0.0"

# Public directory to store clients media data
PUBLIC_DIRECTORY_PROFILES: str = "./backend/public/profiles"
PUBLIC_DIRECTORY_POSTS: str = "./backend/public/posts"

API_ROOT_URL: str = "http://127.0.0.1:5000"

LOGGING_PATH: str = "./backend/logs"

ACCESS_TOKEN_EXPIRY_MINUTES: int = 30  # Minute

REFRESH_TOKEN_EXPIRY_MINUTES: int = 60 * 24 * 10  # 10 days

SECURE_COOKIE: bool = False  # Set always true

HTTP_ONLY: bool = True  # Set always true
