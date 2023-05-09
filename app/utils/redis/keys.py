def usersKey(userId: str):
    return f"users#{userId}"


def userLikesKey(userId: str):
    return f"users:likes#{userId}"


# ------
def orders_key(order_id: str):
    return f"orders#{order_id}"


def products_key(product_id: str):
    return f"products#{product_id}"


def products_index_key():
    return "idx:products"
