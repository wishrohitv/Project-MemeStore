class RouteAccess:
    def __init__(
        self,
        routeName: str,
        rolePermission: list[int],
        methods: list[str],
        partialAccess: bool = False,  # anyone can access partial public data of user
    ) -> None:
        self.routeName = routeName
        self.rolePermission = rolePermission
        self.partialAccess = partialAccess
        self.methods = methods
