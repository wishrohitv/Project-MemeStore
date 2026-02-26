def mention(
    mentionedBy: str,
    postID: int,
    text: str,  # title of the post or ""
) -> dict:
    return {
        "postID": postID,
        "mentionedBy": mentionedBy,
        "text": text,
    }


def suggestion(
    postID: int,
    text: str,  # title of the post or ""
) -> dict:
    return {
        "postID": postID,
        "text": text,
    }


def reply(
    perentPostID: int,
    postID: int,
    text: str,  # title of the post or ""
) -> dict:
    return {
        "parentPostID": perentPostID,
        "postID": postID,
        "text": text,
    }


def warning(text: str) -> dict:
    return {
        "text": text,
    }


def danger(text: str) -> dict:
    return {
        "text": text,
    }


def systemUpdate(text: str) -> dict:
    return {
        "text": text,
    }
