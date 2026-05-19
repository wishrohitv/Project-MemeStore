class RouteAccess:
    def __init__(
        self,
        route_name: str,
        role_permission: list[int],
        methods: list[str],
        partial_access: bool = False,  # anyone can access partial public data of user
    ) -> None:
        self.route_name = route_name
        self.role_permission = role_permission
        self.partial_access = partial_access
        self.methods = methods
