
#user
USER_NOT_FOUND = "user not found"
USER_ALREADY_EXISTS = "user already exists"

#product
PRODUCT_NOT_FOUND = "product not found"
PRODUCT_ALREADY_EXISTS = "product already exists"
PRODUCT_IS_NOT_AVAILABLE_ERROR = "the product is not available"

#review
REVIEW_NOT_FOUND = "review not found"

#order
ORDER_ALREADY_EXISTS = "order already exists"
ORDER_NOT_FOUND = "order not found"

#coupon
COUPON_NOT_FOUND = "coupon not found"
COUPON_EXPIRED = "coupon expired"
MINIMUM_THRESHOLD_NOT_MET = "minimum threshold not met"
COUPON_ALREADY_EXISTS = "coupon already exists"

#cart_item
CART_ITEM_NOT_FOUND = "cart item not found"
CART_ITEM_QUANTITY_LIMITS_ERROR = "cart item quantity should be greater than 1"






#auth/token
INCORRECT_LOGIN_INPUT = "incorrect email or password"

EMAIL_ALREADY_REGISTERED_WITH_GOOGLE = "this email is already registered with google login"

MALFORMED_PAYLOAD = "could not validate credentials"

AUTHENTICATION_REQUIRED = "authentication required"

#response
API_RESPONSES = {
     404: {"description": "Not found"},
     200: {"description": "OK"},
     500: {"description": "Internal Server Error"},
}