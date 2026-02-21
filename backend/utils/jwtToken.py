from typing import Any

from backend.modules import JWT_HASH_KEY, datetime, jwt, timedelta


def decodeJwtToken(clientToken):
    try:
        data = jwt.decode(jwt=clientToken, key=JWT_HASH_KEY, algorithms="HS256")
        return data
    except jwt.ExpiredSignatureError as e:
        raise jwt.ExpiredSignatureError(e)


def generateJwtToken(userData: dict[str, Any], expireInMinute: int):
    currentTime = datetime.now() + timedelta(minutes=expireInMinute)
    unixTimestamp = currentTime.timestamp()  # expiry time

    payload = {"payload": userData, "exp": int(unixTimestamp)}

    userToken = jwt.encode(payload, JWT_HASH_KEY, algorithm="HS256")
    return userToken
