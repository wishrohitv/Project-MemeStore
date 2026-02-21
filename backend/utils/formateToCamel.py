def formateToCamel(val: str) -> str:
    """
    Args:
        "HELLO_WORLD_what"
    RETURNS:
        "helloWorldWhat"
    """
    listOf = val.lower().split("_")

    if len(listOf) == 1:
        return listOf[0]
    else:
        newList = [
            f"{listOf[i][0].upper()}{listOf[i][1:]}" for i in range(1, len(listOf))
        ]
        return "".join([listOf[0]] + newList)
