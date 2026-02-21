class LoggedUser:
    def __init__(
        self, userID: int, roleID: str, roleName: str, *args, **kwargs
    ) -> None:
        self.userID = userID
        self.userRoleID = roleID
        self.userRoleName = roleName
        self.args = args
        self.kwargs = kwargs


if __name__ == "__main__":
    user = LoggedUser(3, 5, "admin", "man", "one man army", favorite="Tomato")
    print(user.userID, user.args, user.kwargs)
