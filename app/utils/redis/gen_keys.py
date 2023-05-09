def usersKey(userId: str) -> str:
    return f"users#{userId}"


def userLikesKey(userId: str) -> str:
    return f"users:likes#{userId}"


def usernamesKey() -> str:
    return "usernames"


def itemKey(itemId: str) -> str:
    return f"items#{itemId}"


def itemsIndexKey() -> str:
    return "idx:items"
