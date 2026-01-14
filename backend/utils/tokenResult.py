class TokenResult:
    def __init__(
        self,
        isLogged: bool = False,
        partialAccess: bool = False,
    ) -> None:
        self.isLogged = isLogged
        self.partialAccess = partialAccess
