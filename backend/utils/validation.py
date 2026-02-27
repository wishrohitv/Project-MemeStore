from backend.modules import re


def getUsername(text: str) -> list:
    """
    Extracts all mentioned usernames from the given text.
    Usernames are expected to be prefixed with '@' and
    consist of word characters (letters, digits, and underscores).
    The function returns a list of extracted usernames.
    """
    pattern = r"@(\w+)"
    matches = re.findall(pattern, text)
    return matches


def validateEmail(email: str) -> bool:
    pass


def validatePassword(password: str) -> bool:
    pass


def validateUsername(username: str) -> bool:
    pass
