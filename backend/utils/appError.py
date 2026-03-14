from werkzeug.exceptions import HTTPException


class AppError(HTTPException):
    def __init__(self, code=500, error="AppError", description="Something went wrong"):
        super().__init__(description=description)
        self.code = code
        self.error = error
        self.description = description


class ResourceNotFoundError(AppError):
    def __init__(
        self, code=404, error="ResourceNotFoundError", description="Resource not found"
    ):
        super().__init__(code=code, error=error, description=description)


class InvalidCredentialsError(AppError):
    def __init__(
        self,
        code=401,
        error="InvalidCredentialsError",
        description="Invalid credentials",
    ):
        super().__init__(code=code, error=error, description=description)


class TokenExpiredError(AppError):
    def __init__(
        self,
        code=401,
        error="TokenExpiredError",
        description="Token has expired",
    ):
        super().__init__(code=code, error=error, description=description)


class RateLimitExceededError(AppError):
    def __init__(
        self,
        code=429,
        error="RateLimitExceededError",
        description="Rate limit exceeded",
    ):
        super().__init__(code=code, error=error, description=description)


class ConflictError(AppError):
    def __init__(
        self,
        code=409,
        error="ConflictError",
        description="Conflict",
    ):
        super().__init__(code=code, error=error, description=description)
