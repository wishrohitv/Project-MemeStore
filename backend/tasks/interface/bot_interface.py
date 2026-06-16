from database import SessionLocal, redis_client
from models import Posts, Users
from modules import APP_NAME

# from repository.post_repository import _create_post
from services.bot_service import generate_bot_response
from utils import get_usernames


def process_user_requests(
    parent_post_id: int | None,
    current_post_id: int,
    replying_to: list[str] | None,  # List of username of the user who are in the thread
    text: str = "",
):
    session = SessionLocal()

    if "nara" not in get_usernames(text):
        return

    # Set rate limit
    # TODO: Implement rate limiting
    try:
        parent_post = None
        if parent_post_id:
            parent_post = (
                session.query(Posts, Users.username)
                .join(Users, Posts.user_id == Users.id)
                .filter(
                    Posts.parent_post_id == parent_post_id,
                    Posts.id == current_post_id,
                    Posts.visibility,
                )
                .first()
            )

        current_post = (
            session.query(Posts, Users.username)
            .join(Users, Posts.user_id == Users.id)
            .filter(
                Posts.id == current_post_id,
                Posts.visibility,
            )
            .first()
        )

        if not current_post:
            return

        # query = {
        #     "role": f"Chat bot of {APP_NAME}(similar to x/twitter) and your name is nara, context can be empty, don't mention about yourself unless you are explicitily asked,  don't mention usernames unless it is required",
        #     "context": "user:@anme post:'This is the best movie i have ever seen, avenger is a best movie'",
        #     "task": "user:@john post:'Hi @nara can you explain about the post'",
        # }
        query = {
            "role": f"Chat bot of {APP_NAME}(similar to x/twitter) and your name is nara, context can be empty, don't mention about yourself unless you are explicitily asked,  don't mention usernames unless it is required",
            "task": f"user:{current_post[1]} post:'{current_post[0].text}'",
        }
        if parent_post:
            query["context"] = f"user:{parent_post[1]} post:'{parent_post[0].text}'"
        response = generate_bot_response(str(query))

        # Create post for this response
        from repository.post_repository import _create_post

        if replying_to is None:
            replying_to = [current_post[1]]
        else:
            replying_to = sorted(set(replying_to + [current_post[1]]))

        _create_post(
            user_id=32,  # Default user_id for bot, representing the bot itself
            text=response,
            tags=None,
            media_url=None,
            media_public_id=None,
            file_type=None,
            file_extension=None,
            age_rating="pg13",
            category=1,
            parent_post_id=current_post_id,
            is_reply=True,
            visibility=True,
            replying_to=replying_to,
        )

    except Exception as e:
        raise e
