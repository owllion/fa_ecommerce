def usersKey(userId: str):
    return f"users#{userId}"


def userLikesKey(userId: str):
    return f"users:likes#{userId}"


# ------
def user_orders_key(user_id: str):
    return f"user:orders#{user_id}"


def products_key(product_id: str):
    return f"products#{product_id}"


def best_selling_products_key():
    return "products:best_selling"


# -----for redisearch---------------
def products_index_key():
    return "idx:products"


# used to create a hash to store each search options which is stored as a json str as key.
def search_options_key(options: str):
    return f"search:options#{options}"


def number_of_search_result_key(options: str):
    return f"number:search_result:#{options}"
