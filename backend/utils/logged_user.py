class LoggedUser:
    def __init__(
        self, user_id: int, role_id: int, role_name: str, *args, **kwargs
    ) -> None:
        self.user_id = user_id
        self.user_role_id = role_id
        self.user_role_name = role_name
        self.args = args
        self.kwargs = kwargs


if __name__ == "__main__":
    user = LoggedUser(3, 5, "admin", "man", "one man army", favorite="Tomato")
    print(user.user_id, user.args, user.kwargs)
