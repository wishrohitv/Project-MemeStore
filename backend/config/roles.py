from backend.utils.formateToCamel import formateToCamel


# Roles and with id in database
class ROLE:
    SUPER_ADMIN = 1
    MODERATOR = 2
    USER = 3
    GUEST = 4

    @property
    def roles(self) -> dict[str, int]:
        # Iterate over the class's attributes (stored in self.__class__.__dict__)
        # and include only those that are uppercase (which represent the roles)
        return {
            # Convert the role name to lowercase (e.g., 'SUPER_ADMIN' -> 'superAdmin')
            # You might need to adjust the key generation based on your desired output
            formateToCamel(k): v
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, int) and k.isupper()
        }

    @property
    def rolesIds(self) -> dict[int, str]:
        return {
            # Convert the role name to lowercase (e.g., 'SUPER_ADMIN' -> 'superAdmin')
            # You might need to adjust the key generation based on your desired output
            v: formateToCamel(k)
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, int) and k.isupper()
        }
