from backend.modules import random


def getRandomOTP(length: int = 6) -> int:
    return random.randint(10 ** (length - 1), 10**length - 1)
