from typing import Any

from modules import JWT_HASH_KEY, datetime, jwt, timedelta


def decode_jwt_token(clientToken):
    try:
        data = jwt.decode(jwt=clientToken, key=JWT_HASH_KEY, algorithms="HS256")
        return data
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError(e)


def generate_jwt_token(userData: dict[str, Any], expireInMinute: int):
    currentTime = datetime.now() + timedelta(minutes=expireInMinute)
    unixTimestamp = currentTime.timestamp()  # expiry time

    payload = {"payload": userData, "exp": int(unixTimestamp)}

    userToken = jwt.encode(payload, JWT_HASH_KEY, algorithm="HS256")
    return userToken
