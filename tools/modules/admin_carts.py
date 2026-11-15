"""The Admin cart and checkout endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Admin cart and checkout"
SLUG = "admin-cart-and-checkout"
BASE = "/admin/orders"
ICON = "cart-plus"

CREATE_PAGE = "/api-reference/admin-cart-and-checkout/create-an-admin-cart"
RETRIEVE_PAGE = "/api-reference/admin-cart-and-checkout/retrieve-an-admin-cart"
REPLACE_PAGE = "/api-reference/admin-cart-and-checkout/replace-an-admin-cart"
UPDATE_PAGE = "/api-reference/admin-cart-and-checkout/change-an-admin-carts-customer"
DELETE_PAGE = "/api-reference/admin-cart-and-checkout/delete-an-admin-cart"
ADD_ITEMS_PAGE = "/api-reference/admin-cart-and-checkout/add-products-to-an-admin-cart"
CLEAR_ITEMS_PAGE = "/api-reference/admin-cart-and-checkout/remove-every-line-from-an-admin-cart"
UPDATE_ITEM_PAGE = "/api-reference/admin-cart-and-checkout/change-the-quantity-of-a-cart-line"
DELETE_ITEM_PAGE = "/api-reference/admin-cart-and-checkout/remove-a-cart-line"
CHECKOUT_PAGE = "/api-reference/admin-cart-and-checkout/retrieve-a-checkout"
UPDATE_CHECKOUT_PAGE = "/api-reference/admin-cart-and-checkout/update-a-checkout"
CONFIRM_PAGE = "/api-reference/admin-cart-and-checkout/place-the-order-from-a-checkout"
APPLY_COUPON_PAGE = "/api-reference/admin-cart-and-checkout/apply-a-coupon-to-a-checkout"
REMOVE_COUPON_PAGE = "/api-reference/admin-cart-and-checkout/remove-the-coupon-from-a-checkout"
APPLY_GIFT_CARD_PAGE = "/api-reference/admin-cart-and-checkout/apply-a-gift-card-to-a-checkout"
REMOVE_GIFT_CARD_PAGE = "/api-reference/admin-cart-and-checkout/remove-the-gift-card-from-a-checkout"
SCHEDULES_PAGE = "/api-reference/admin-cart-and-checkout/retrieve-a-checkouts-delivery-schedule"
SET_SCHEDULE_PAGE = "/api-reference/admin-cart-and-checkout/set-a-checkouts-delivery-schedule"
CLEAR_SCHEDULE_PAGE = "/api-reference/admin-cart-and-checkout/clear-a-checkouts-delivery-schedule"
CREATE_ORDER_PAGE = "/api-reference/orders/create-an-order"
DELETE_ORDER_PAGE = "/api-reference/orders/delete-an-order"
GIFT_CARDS_PAGE = "/api-reference/gift-cards/list-gift-cards"
SHIPPING_SETTINGS_PAGE = "/api-reference/shipping-settings/update-shipping-settings"
RETRIEVE_CUSTOMER_PAGE = "/api-reference/customers/retrieve-a-customer"

OVERVIEW_DESCRIPTION = "Build a cart for a customer, set its delivery and addresses, apply a coupon, a gift card and a delivery date, and place the order."
INTRO = (
    "The Admin cart and checkout API has 19 endpoints, and you can call every one from all seven SDKs. Every path"
    " starts with `/api/v4/admin/orders/carts` or `/api/v4/admin/orders/checkout`. You create a cart for a customer,"
    " change its lines, set the delivery and the addresses on its checkout, apply a coupon, a gift card and a delivery"
    " date, and place the order. A cart and its checkout are one session, and every call reaches it by its `session_id`."
    " The storefront's carts are in the [Carts](/carts) API."
)

WARNING = (
    "**[Place the order from a checkout](" + CONFIRM_PAGE + ") creates a real order.**\n"
    "  It closes the session, and every later call on the cart or the checkout, a second confirm included, is rejected\n"
    "  with `410` and the code `session_confirmed`. A session also ends on its own: it is held for 30 minutes from its\n"
    "  last write. Create a new cart when you need one again."
)

NOTES = [
    "**Every call takes the cart's `session_id`.** [Create an admin cart](" + CREATE_PAGE + ") returns it as\n"
    "  `cart.session.session_id`, a value such as `PRV-3f2a9c41b7d80e65`. Every other call takes it as `session_id` in the\n"
    "  path, and the two line calls also take the line's `cart_item_id` from `cart.items`. Send `session_id` in the\n"
    "  create body to name the session yourself, in the same `PRV-` form.",
    "**Bodies are bare, and `customer_id` is the customer's own `customer_id`.** Send the fields at the top level, with\n"
    "  no wrapper. A field a call does not accept is rejected with `400` and the code `unknown_field`. Find the\n"
    "  `customer_id` with [Retrieve a customer](" + RETRIEVE_CUSTOMER_PAGE + ") or a customer listing.",
    "**Every cart call returns the whole cart, except the delete.** [Delete an admin cart](" + DELETE_PAGE + ") returns\n"
    "  `204` with no body. [Replace an admin cart](" + REPLACE_PAGE + ") puts the lines on again, so each gets a new\n"
    "  `cart_item_id`. [Change an admin cart's customer](" + UPDATE_PAGE + ") takes only `customer_id`: sending\n"
    "  `products` there is rejected with `400`. [Add products to an admin cart](" + ADD_ITEMS_PAGE + ") raises the\n"
    "  quantity of a product that is already on the cart.",
    "**A closed session returns `410`.** After [Place the order from a checkout](" + CONFIRM_PAGE + ") every call on it\n"
    "  returns `410` with the code `session_confirmed`, and the detail on `order_id` holds the new order. After\n"
    "  [Delete an admin cart](" + DELETE_PAGE + ") every call on it, a second delete included, returns `410` with the code\n"
    "  `session_deleted`. A `cart_item_id` the cart does not hold returns `404`.",
    "**The checkout lists what blocks the order in `issues`.** [Retrieve a checkout](" + CHECKOUT_PAGE + ") returns\n"
    "  `issues` with `delivery_type` `required` until you set a delivery type with\n"
    "  [Update a checkout](" + UPDATE_CHECKOUT_PAGE + "). While `issues` is not empty,\n"
    "  [Place the order from a checkout](" + CONFIRM_PAGE + ") is rejected with `422` and the code `checkout_incomplete`.",
    "**An address you send replaces the whole address.** `delivery_type` is `shipping`, `delivery`, `others_shipping` or\n"
    "  `store_pickup`. The checkout starts with the customer's addresses. A field you leave out of an address you send\n"
    "  reads `\"\"`. Shipping and handling follow the shipping address, so send it with `delivery_type`; a `store_pickup`\n"
    "  has no shipping cost.",
    "**A `shipping` or `delivery` checkout needs a default shipping profile.** A new store has none. Create a shipping\n"
    "  profile, then make it the store's `default_shipping_profile` with\n"
    "  [Update shipping settings](" + SHIPPING_SETTINGS_PAGE + "): creating the profile alone is not enough.",
    "**A checkout takes one coupon and one gift card.** A second coupon, or a second gift card, is rejected with `409`.\n"
    "  A code the store does not accept, or a coupon or gift card that is not active, is rejected with `422`: the\n"
    "  code is `invalid_coupon` or `invalid_gift_card` on `code`. A missing `code` is `400`. A coupon lowers\n"
    "  `totals.total_discount` and `totals.grand_total`, and `discounts.coupon.applied_amount` is what it takes off.\n"
    "  A gift card leaves `grand_total` as it was, sets `totals.gift_card_applied` and lowers `totals.due`, and pays\n"
    "  only for the cart's own customer; find a customer's cards with [List gift cards](" + GIFT_CARDS_PAGE + ").\n"
    "  The two remove calls return `404` when nothing is applied.",
    "**A delivery date needs `delivery_type` `delivery`.** [Set a checkout's delivery schedule](" + SET_SCHEDULE_PAGE + ")\n"
    "  needs the schedule `id` and a `date`. With another delivery type it is rejected with `422` and the code\n"
    "  `delivery_type_not_supported`. A schedule that does not apply to the order is rejected with `422` and the code\n"
    "  `schedule_not_applicable`, an unknown `id` with `404`, and a `date` that is not a date with `400`.\n"
    "  [Clear a checkout's delivery schedule](" + CLEAR_SCHEDULE_PAGE + ") returns `204`, also when none was set.",
    "**The transaction number can go in the body or in a header.** Send `transaction_no` in the confirm body, or send it\n"
    "  as the `X-Transaction-No` header, which the SDKs send for you. The store files the order under that number. When\n"
    "  both are present and differ, the call is rejected with `400` and the code `header_body_mismatch`.",
]

DELIVERY_TYPES = ["delivery", "others_shipping", "shipping", "store_pickup"]


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def text(description):
    return {"type": "string", "description": description}


def nullable_text(description):
    return {"type": ["string", "null"], "description": description}


def number(description):
    return {"type": "number", "description": description}


def whole(description):
    return {"type": "integer", "description": description}


def nullable_whole(description):
    return {"type": ["integer", "null"], "description": description}


def flag(description):
    return {"type": "boolean", "description": description}


SESSION_ID = "PRV-3f2a9c41b7d80e65"

SESSION_ID_PARAMETER = {
    "name": "session_id",
    "in": "path",
    "required": True,
    "description": "The cart's `session_id`, from `cart.session.session_id` in the response to [Create an admin cart](" + CREATE_PAGE + "). It looks like `PRV-3f2a9c41b7d80e65`.",
    "schema": {"type": "string", "example": SESSION_ID},
}

CART_ITEM_ID_PARAMETER = {
    "name": "cart_item_id",
    "in": "path",
    "required": True,
    "description": "The line's `cart_item_id`, from `cart.items` in any cart response. A replace of the cart numbers its lines again.",
    "schema": {"type": "integer", "example": 1},
}

ERROR_REF = ref("AdminCartError")

SESSION = {"session_id": SESSION_ID, "status": "active", "created_at": "2026-11-12T10:34:55Z", "expires_at": "2026-11-12T11:04:55Z"}
LATER_SESSION = dict(SESSION, expires_at="2026-11-12T11:05:01Z")
CUSTOMER = {"customer_id": 512, "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com"}
ITEM = {
    "cart_item_id": 1, "product_id": 101, "product_name": "Cotton T-Shirt", "variation_id": None, "variation_name": None,
    "sku": "TSHIRT-001", "price": 8.0, "quantity": 2, "discount": 0.0, "tax": 1.6, "total_amount": 17.6,
    "taxable": True, "shippable": True,
}
CART_TOTALS = {"sub_total": 16.0, "total_discount": 0.0, "total_tax": 1.6, "grand_total": 17.6}
CART = {"session": SESSION, "customer": CUSTOMER, "currency_code": "AUD", "items": [ITEM], "totals": CART_TOTALS}
EMPTY_CART = dict(CART, items=[], totals={"sub_total": 0.0, "total_discount": 0.0, "total_tax": 0.0, "grand_total": 0.0})

COUNTRY = {"id": 12, "name": "Australia", "code": "AU"}
STATE = {"id": 72, "name": "Victoria", "code": "VIC"}
ADDRESS = {
    "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "company_name": "", "address_line_1": "1 Example Street",
    "address_line_2": "", "country": COUNTRY, "state": STATE, "city": "Melbourne", "post_code": "3000", "mobile": "", "phone": "0300000000", "fax": "",
}
ADDRESS_INPUT = {
    "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "address_line_1": "1 Example Street",
    "city": "Melbourne", "post_code": "3000", "phone": "0300000000", "country_code": "AU", "state_code": "VIC",
}
NO_DISCOUNTS = {"coupon": None, "gift_card": None}
SHIPPING = {"delivery_type": "shipping", "shipping_type": "flat_rate", "shipping_cost": 100.0, "shipping_tax": 10.0}
TOTALS = {
    "sub_total": 16.0, "total_discount": 0.0, "total_tax": 1.6, "shipping_cost": 100.0, "handling_cost": 10.0,
    "total_surcharge": 0.0, "gift_card_applied": 0.0, "grand_total": 137.6, "due": 137.6,
}
OPEN_CHECKOUT = {
    "session": SESSION, "customer": CUSTOMER, "delivery_type": None, "currency_code": "AUD", "items": [ITEM],
    "billing_address": dict(ADDRESS, address_line_1="", city="", post_code="", phone="", state={}),
    "shipping_address": dict(ADDRESS, address_line_1="", city="", post_code="", phone="", state={}),
    "shipping": {"delivery_type": None, "shipping_type": "", "shipping_cost": 0.0, "shipping_tax": 0.0},
    "discounts": NO_DISCOUNTS, "delivery_schedule": None,
    "totals": dict(TOTALS, shipping_cost=0.0, handling_cost=0.0, grand_total=17.6, due=17.6),
    "issues": [{"field": "delivery_type", "code": "required", "message": "is required"}],
}
READY_CHECKOUT = dict(
    OPEN_CHECKOUT, session=LATER_SESSION, delivery_type="shipping", billing_address=ADDRESS, shipping_address=ADDRESS,
    shipping=SHIPPING, totals=TOTALS, issues=[],
)
COUPON_DISCOUNTS = {"coupon": {"code": "SAVE10", "status": "applied", "applied_amount": 1.6}, "gift_card": None}
COUPON_TOTALS = dict(TOTALS, total_discount=1.6, total_tax=1.44, grand_total=135.84, due=135.84)
GIFT_CARD_DISCOUNTS = {"coupon": None, "gift_card": {"code": "GIFT-0001", "status": "applied", "applied_amount": 10.0, "remaining_balance": None}}
GIFT_CARD_TOTALS = dict(TOTALS, gift_card_applied=10.0, due=127.6)

CONFIRMED_ORDER = {
    "order_id": 1043, "order_no": 1043, "internal_id": 2187, "uuid": "3f2b8c1e-6d4a-4e7b-9a15-0c8d2e6f7a41",
    "transaction_no": "TXN-ORDER-0001", "currency_code": "AUD", "order_status": "in_progress",
    "payment_status": "unpaid", "shipping_status": "unshipped", "sub_total": 16.0, "shipping_cost": 100.0,
    "shipping_tax": 10.0, "handling_cost": 10.0, "total_surcharge": 0.0, "total_discount": 0.0, "total_tax": 1.6,
    "grand_total": 137.6, "paid": 0.0, "due": 137.6, "items_total": 2,
    "customer_summary": {"first_name": "Jane", "last_name": "Doe", "customer_id": 512, "internal_id": 2204, "email": "jane.doe@example.com"},
    "order_line_details": [{"product_id": 101, "product_name": "Cotton T-Shirt", "sku": "TSHIRT-001", "quantity": 2, "price": 8.0, "total_amount": 16.0, "cart_item_id": 1}],
    "payments": [],
}

CLOSED_410 = "The session is closed. The code is `gone`, and `details` has an entry on `session_id` or `order_id` with the code `session_deleted` (the cart was deleted) or `session_confirmed` (an order was placed from it, and `value` holds the order's `order_id`)."
NO_LINE_404 = "The cart does not hold that `cart_item_id`. The code is `not_found`, and `details` names `cart_item_id`."
UNKNOWN_FIELD_400 = "the body has a field the call does not accept (the code `unknown_field`)"

CART_RESPONSE = {"type": "object", "properties": {"cart": ref("AdminCart")}}
CHECKOUT_RESPONSE = {"type": "object", "properties": {"checkout": ref("AdminCheckout")}}
DISCOUNT_RESPONSE = {"type": "object", "properties": {"checkout": ref("AdminCheckoutDiscountResult")}}

PRODUCTS_BODY = {"products": [{"product_id": 101, "quantity": 2}]}

ENDPOINTS = [
    {
        "key": "create_admin_cart",
        "slug": "create-an-admin-cart",
        "title": "Create an admin cart",
        "method": "POST",
        "path": BASE + "/carts",
        "summary": "Creates a cart for a customer with the products you send and returns it with its `session_id`.",
        "description": "Send `customer_id` and `products` at the top level of the body; each product has a `product_id` and a `quantity`, and a `variation_id` for a variation. The store prices the lines and returns the cart under `cart`, with `cart.session.session_id`, which every other call takes as `session_id`. The session is held for 30 minutes from its last write. Send `session_id` in the body, in the `PRV-` form, to name the session yourself.",
        "body": {"schema": ref("AdminCartInput"), "example": dict({"customer_id": 512}, **PRODUCTS_BODY)},
        "responses": {
            "201": {
                "description": "The new cart under `cart`: `session`, `customer`, `currency_code`, `items` and `totals`.",
                "schema": CART_RESPONSE,
                "example": {"cart": CART},
            },
            "400": {"description": "`customer_id` or `products` is missing, a product line has no `product_id` or `quantity`, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_admin_cart",
        "slug": "retrieve-an-admin-cart",
        "title": "Retrieve an admin cart",
        "method": "GET",
        "path": BASE + "/carts/{session_id}",
        "summary": "Returns the cart whose `session_id` you pass, with its lines and totals.",
        "description": "Returns the cart in the same shape as [Create an admin cart](" + CREATE_PAGE + "). A cart that was deleted, or that an order was placed from, returns `410`.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "The cart under `cart`.", "schema": CART_RESPONSE, "example": {"cart": CART}},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "replace_admin_cart",
        "slug": "replace-an-admin-cart",
        "title": "Replace an admin cart",
        "method": "PUT",
        "path": BASE + "/carts/{session_id}",
        "summary": "Replaces the cart's customer and lines with the ones you send and returns the cart.",
        "description": "Send `customer_id` and `products` at the top level of the body. The lines you send take the place of the cart's lines, so each gets a new `cart_item_id`. To change only the customer, use [Change an admin cart's customer](" + UPDATE_PAGE + ").",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCartInput"), "example": {"customer_id": 512, "products": [{"product_id": 101, "variation_id": 2011, "quantity": 1}]}},
        "responses": {
            "200": {"description": "The cart under `cart`, with the new lines.", "schema": CART_RESPONSE, "example": {"cart": dict(CART, items=[dict(ITEM, cart_item_id=2, variation_id=2011, variation_name="Medium", quantity=1, tax=0.8, total_amount=8.8)], totals={"sub_total": 8.0, "total_discount": 0.0, "total_tax": 0.8, "grand_total": 8.8})}},
            "400": {"description": "`customer_id` or `products` is missing, a product line is not valid, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "update_admin_cart",
        "slug": "change-an-admin-carts-customer",
        "title": "Change an admin cart's customer",
        "method": "PATCH",
        "path": BASE + "/carts/{session_id}",
        "summary": "Moves the cart to another customer and returns the cart.",
        "description": "Send only `customer_id` at the top level of the body. This call changes nothing else: sending `products` is rejected with `400`. To change the lines, use [Replace an admin cart](" + REPLACE_PAGE + "), [Add products to an admin cart](" + ADD_ITEMS_PAGE + ") or the line calls.",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCartCustomerInput"), "example": {"customer_id": 513}},
        "responses": {
            "200": {"description": "The cart under `cart`, for the new customer.", "schema": CART_RESPONSE, "example": {"cart": dict(CART, customer=dict(CUSTOMER, customer_id=513, first_name="John", email="john.doe@example.com"))}},
            "400": {"description": "`customer_id` is missing, or the body has another field, `products` included (the code `unknown_field`).", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "delete_admin_cart",
        "slug": "delete-an-admin-cart",
        "title": "Delete an admin cart",
        "method": "DELETE",
        "path": BASE + "/carts/{session_id}",
        "summary": "Deletes the cart and its checkout, returning `204` with no body.",
        "description": "Deletes the cart. Every later call on the cart or its checkout, a second delete included, returns `410` with the code `session_deleted`.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "204": {"description": "The cart is deleted. No body."},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "add_admin_cart_items",
        "slug": "add-products-to-an-admin-cart",
        "title": "Add products to an admin cart",
        "method": "POST",
        "path": BASE + "/carts/{session_id}/cart_items",
        "summary": "Adds the products you send to the cart and returns the cart.",
        "description": "Send `products` at the top level of the body. A product that is not on the cart gets a new line with its own `cart_item_id`. A product that is already on the cart raises that line's `quantity` instead.",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCartItemsInput"), "example": {"products": [{"product_id": 102, "quantity": 1}]}},
        "responses": {
            "201": {"description": "The cart under `cart`, with the added lines.", "schema": CART_RESPONSE, "example": {"cart": dict(CART, items=[ITEM, dict(ITEM, cart_item_id=2, product_id=102, product_name="Canvas Tote Bag", sku="TOTE-001", price=12.0, quantity=1, tax=1.2, total_amount=13.2)], totals={"sub_total": 28.0, "total_discount": 0.0, "total_tax": 2.8, "grand_total": 30.8})}},
            "400": {"description": "`products` is missing, a product line is not valid, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "clear_admin_cart_items",
        "slug": "remove-every-line-from-an-admin-cart",
        "title": "Remove every line from an admin cart",
        "method": "DELETE",
        "path": BASE + "/carts/{session_id}/cart_items",
        "summary": "Removes every line from the cart and returns the empty cart.",
        "description": "Removes all the cart's lines and keeps the cart and its customer. The response is the cart with an empty `items` list and totals of `0`. To delete the cart itself, use [Delete an admin cart](" + DELETE_PAGE + ").",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "The cart under `cart`, with no lines.", "schema": CART_RESPONSE, "example": {"cart": EMPTY_CART}},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "update_admin_cart_item",
        "slug": "change-the-quantity-of-a-cart-line",
        "title": "Change the quantity of a cart line",
        "method": "PATCH",
        "path": BASE + "/carts/{session_id}/cart_items/{cart_item_id}",
        "summary": "Sets the quantity of one cart line and returns the cart.",
        "description": "Send the new `quantity` at the top level of the body. The line is the one whose `cart_item_id` you pass in the path. The response is the whole cart, repriced.",
        "parameters": [SESSION_ID_PARAMETER, CART_ITEM_ID_PARAMETER],
        "body": {"schema": ref("AdminCartItemUpdateInput"), "example": {"quantity": 3}},
        "responses": {
            "200": {"description": "The cart under `cart`, with the new quantity.", "schema": CART_RESPONSE, "example": {"cart": dict(CART, items=[dict(ITEM, quantity=3, tax=2.4, total_amount=26.4)], totals={"sub_total": 24.0, "total_discount": 0.0, "total_tax": 2.4, "grand_total": 26.4})}},
            "400": {"description": "`quantity` is missing, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "404": {"description": NO_LINE_404, "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID, "cart_item_id": 1}},
    },
    {
        "key": "delete_admin_cart_item",
        "slug": "remove-a-cart-line",
        "title": "Remove a cart line",
        "method": "DELETE",
        "path": BASE + "/carts/{session_id}/cart_items/{cart_item_id}",
        "summary": "Removes one line from the cart and returns the cart.",
        "description": "Removes the line whose `cart_item_id` you pass in the path. The response is the whole cart without that line, not `204`.",
        "parameters": [SESSION_ID_PARAMETER, CART_ITEM_ID_PARAMETER],
        "responses": {
            "200": {"description": "The cart under `cart`, without the removed line.", "schema": CART_RESPONSE, "example": {"cart": EMPTY_CART}},
            "404": {"description": NO_LINE_404, "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID, "cart_item_id": 1}},
    },
    {
        "key": "get_checkout",
        "slug": "retrieve-a-checkout",
        "title": "Retrieve a checkout",
        "method": "GET",
        "path": BASE + "/checkout/{session_id}",
        "summary": "Returns the cart's checkout: totals, delivery, addresses and what still blocks the order.",
        "description": "Returns the checkout for the cart whose `session_id` you pass. `issues` lists what still blocks [Place the order from a checkout](" + CONFIRM_PAGE + "): it holds `delivery_type` `required` until you set a delivery type, and it is empty when the order can be placed. The addresses start as the customer's.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "The checkout under `checkout`: `session`, `customer`, `delivery_type`, `currency_code`, `items`, `billing_address`, `shipping_address`, `shipping`, `discounts`, `delivery_schedule`, `totals` and `issues`.", "schema": CHECKOUT_RESPONSE, "example": {"checkout": OPEN_CHECKOUT}},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "update_checkout",
        "slug": "update-a-checkout",
        "title": "Update a checkout",
        "method": "PATCH",
        "path": BASE + "/checkout/{session_id}",
        "summary": "Sets the delivery type and the billing and shipping addresses and returns the priced checkout.",
        "description": "Send `delivery_type`, `billing_address` and `shipping_address` at the top level of the body; no other field is taken. Each address you send replaces the whole address, and a field you leave out reads `\"\"`. Shipping and handling follow the shipping address, so send it with `delivery_type`. A `store_pickup` has no shipping cost. A `shipping` or `delivery` checkout needs the store to have a default shipping profile; see [Update shipping settings](" + SHIPPING_SETTINGS_PAGE + ").",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCheckoutInput"), "example": {"delivery_type": "shipping", "billing_address": ADDRESS_INPUT, "shipping_address": ADDRESS_INPUT}},
        "responses": {
            "200": {"description": "The priced checkout under `checkout`, in the same shape as [Retrieve a checkout](" + CHECKOUT_PAGE + "). `issues` is empty once the delivery type is set.", "schema": CHECKOUT_RESPONSE, "example": {"checkout": READY_CHECKOUT}},
            "400": {"description": "`delivery_type` is not one of the four values, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "confirm_checkout",
        "slug": "place-the-order-from-a-checkout",
        "title": "Place the order from a checkout",
        "method": "POST",
        "path": BASE + "/checkout/{session_id}/confirm",
        "summary": "Places a real order from the checkout and closes the session.",
        "description": "This creates an order and closes the session. The body is optional. With no `payment`, or with `payment_gateway` `PIS`, the order is unpaid. To record a payment, send `payment` with an `amount` and a `payment_method`; an `amount` above what is due is rejected. The call returns `422` with the code `checkout_incomplete` while the checkout's `issues` is not empty. Send `transaction_no` in the body, or as the `X-Transaction-No` header, to file the order under that number; a header that differs from the body's `transaction_no` is rejected with `400`.",
        "parameters": [
            SESSION_ID_PARAMETER,
            {
                "name": "X-Transaction-No",
                "in": "header",
                "required": False,
                "description": "A transaction number to file the order under. The SDKs send it from their `transaction_no` argument. If the body also has a `transaction_no` that differs, the call is rejected with `400` and the code `header_body_mismatch`.",
                "schema": {"type": "string", "example": "TXN-ORDER-0001"},
            },
        ],
        "body": {"schema": ref("AdminCheckoutConfirmInput"), "example": {"send_email": False, "payment_gateway": "PIS"}},
        "responses": {
            "201": {
                "description": "The new order under `order`, in the same flat shape as the response to [Create an order](" + CREATE_ORDER_PAGE + "): `order_id`, `transaction_no`, the totals, `customer_summary`, `order_line_details`, `payments` and the addresses. To remove a test order, use [Delete an order](" + DELETE_ORDER_PAGE + ").",
                "schema": {"type": "object", "properties": {"order": ref("OrderFlat")}},
                "example": {"order": CONFIRMED_ORDER},
            },
            "400": {"description": "`transaction_no` in the body differs from the `X-Transaction-No` header (the code `header_body_mismatch`), the `payment` is missing its `amount` or `payment_method`, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "The checkout is not ready: `issues` is not empty. The code is `checkout_incomplete`. No order is created.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "apply_checkout_coupon",
        "slug": "apply-a-coupon-to-a-checkout",
        "title": "Apply a coupon to a checkout",
        "method": "POST",
        "path": BASE + "/checkout/{session_id}/coupon",
        "summary": "Applies a coupon code to the checkout and returns the lower totals.",
        "description": "Send the coupon's `code` at the top level of the body. The response returns `discounts.coupon` with the `applied_amount` the coupon takes off, and `totals` with the new `total_discount` and `grand_total`. A checkout takes one coupon: a second call is rejected with `409`. A code the store does not accept, or a coupon that is not active, is rejected with `422`.",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCheckoutCodeInput"), "example": {"code": "SAVE10"}},
        "responses": {
            "200": {"description": "Only `session`, `discounts` and `totals` under `checkout`. `discounts.coupon` has the `code`, the `status` and the `applied_amount`.", "schema": DISCOUNT_RESPONSE, "example": {"checkout": {"session": LATER_SESSION, "discounts": COUPON_DISCOUNTS, "totals": COUPON_TOTALS}}},
            "400": {"description": "`code` is missing, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "409": {"description": "A coupon is already applied. Remove it first with [Remove the coupon from a checkout](" + REMOVE_COUPON_PAGE + ").", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "The store does not accept the code, or the coupon is not active. The code is `unprocessable`, and `details` has an entry on `code` with the code `invalid_coupon`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "remove_checkout_coupon",
        "slug": "remove-the-coupon-from-a-checkout",
        "title": "Remove the coupon from a checkout",
        "method": "DELETE",
        "path": BASE + "/checkout/{session_id}/coupon",
        "summary": "Removes the applied coupon, so the totals return to what they were before it.",
        "description": "Removes the coupon and returns `200`. With no coupon applied, the call returns `404`.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "The coupon is removed. Only `session`, `discounts` and `totals` under `checkout`.", "schema": DISCOUNT_RESPONSE, "example": {"checkout": {"session": LATER_SESSION, "discounts": NO_DISCOUNTS, "totals": TOTALS}}},
            "404": {"description": "No coupon is applied. The code is `not_found`, and `details` has an entry on `code` with the code `coupon_not_applied`.", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "apply_checkout_gift_card",
        "slug": "apply-a-gift-card-to-a-checkout",
        "title": "Apply a gift card to a checkout",
        "method": "POST",
        "path": BASE + "/checkout/{session_id}/gift_card",
        "summary": "Applies a gift card to the checkout, lowering the amount due.",
        "description": "Send the card's `code` at the top level of the body. The card pays up to its balance: `discounts.gift_card.applied_amount` is the lesser of the card's balance and `grand_total`, `totals.gift_card_applied` equals it, `grand_total` does not change and `due` is lower by that amount. The card pays only for the cart's own customer, and nothing is spent from it until an order is placed. A checkout takes one gift card: a second call is rejected with `409`. A code the store does not accept, or a card that is not active, is rejected with `422`.",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCheckoutCodeInput"), "example": {"code": "GIFT-0001"}},
        "responses": {
            "200": {"description": "Only `session`, `discounts` and `totals` under `checkout`. `discounts.gift_card` has the `code`, the `status`, the `applied_amount` and the `remaining_balance`.", "schema": DISCOUNT_RESPONSE, "example": {"checkout": {"session": LATER_SESSION, "discounts": GIFT_CARD_DISCOUNTS, "totals": GIFT_CARD_TOTALS}}},
            "400": {"description": "`code` is missing, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "409": {"description": "A gift card is already applied. Remove it first with [Remove the gift card from a checkout](" + REMOVE_GIFT_CARD_PAGE + ").", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "The store does not accept the code, the card is not active, or the cart's customer cannot use it. The code is `unprocessable`, and `details` has an entry on `code` with the code `invalid_gift_card`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "remove_checkout_gift_card",
        "slug": "remove-the-gift-card-from-a-checkout",
        "title": "Remove the gift card from a checkout",
        "method": "DELETE",
        "path": BASE + "/checkout/{session_id}/gift_card",
        "summary": "Removes the applied gift card, so `due` returns to the grand total.",
        "description": "Removes the gift card and returns `200`. With no gift card applied, the call returns `404`.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "The gift card is removed. Only `session`, `discounts` and `totals` under `checkout`.", "schema": DISCOUNT_RESPONSE, "example": {"checkout": {"session": LATER_SESSION, "discounts": NO_DISCOUNTS, "totals": TOTALS}}},
            "404": {"description": "No gift card is applied. The code is `not_found`, and `details` has an entry on `code` with the code `gift_card_not_applied`.", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "get_checkout_delivery_schedules",
        "slug": "retrieve-a-checkouts-delivery-schedule",
        "title": "Retrieve a checkout's delivery schedule",
        "method": "GET",
        "path": BASE + "/checkout/{session_id}/delivery_schedules",
        "summary": "Returns the delivery schedule chosen for the checkout, or `null` when none is set.",
        "description": "Returns `session` and `delivery_schedule` under `checkout`. `delivery_schedule` is `null` until you choose one with [Set a checkout's delivery schedule](" + SET_SCHEDULE_PAGE + ").",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "200": {"description": "`session` and `delivery_schedule` under `checkout`.", "schema": {"type": "object", "properties": {"checkout": ref("AdminCheckoutScheduleResult")}}, "example": {"checkout": {"session": LATER_SESSION, "delivery_schedule": None}}},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "set_checkout_delivery_schedule",
        "slug": "set-a-checkouts-delivery-schedule",
        "title": "Set a checkout's delivery schedule",
        "method": "PUT",
        "path": BASE + "/checkout/{session_id}/delivery_schedules",
        "summary": "Chooses a delivery schedule and date for the checkout.",
        "description": "Send the schedule's `id` and the `date` you want at the top level of the body; both are required. Only a checkout whose `delivery_type` is `delivery` takes a schedule: with another delivery type the call is rejected with `422` and the code `delivery_type_not_supported`. A schedule that does not apply to the order is rejected with `422` and the code `schedule_not_applicable`.",
        "parameters": [SESSION_ID_PARAMETER],
        "body": {"schema": ref("AdminCheckoutDeliveryScheduleInput"), "example": {"id": 1, "date": "2026-11-20"}},
        "responses": {
            "200": {"description": "The schedule is set on the checkout."},
            "400": {"description": "`id` or `date` is missing, `date` is not a date, or " + UNKNOWN_FIELD_400 + ".", "schema": ERROR_REF},
            "404": {"description": "No delivery schedule has that `id`.", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "The checkout's `delivery_type` is not `delivery` (the code `delivery_type_not_supported`), or the schedule does not apply to the order (the code `schedule_not_applicable`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
    {
        "key": "clear_checkout_delivery_schedule",
        "slug": "clear-a-checkouts-delivery-schedule",
        "title": "Clear a checkout's delivery schedule",
        "method": "DELETE",
        "path": BASE + "/checkout/{session_id}/delivery_schedules",
        "summary": "Clears the checkout's delivery schedule, returning `204` with no body.",
        "description": "Clears the delivery schedule and returns `204` with no body. The call also returns `204` when no schedule was set.",
        "parameters": [SESSION_ID_PARAMETER],
        "responses": {
            "204": {"description": "The schedule is cleared. No body."},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"session_id": SESSION_ID}},
    },
]

SCHEMAS = {
    "AdminCart": {"type": "object", "description": "A cart, with its lines priced by the store.", "properties": {
        "session": ref("AdminCartSession"),
        "customer": ref("AdminCartCustomer"),
        "currency_code": text("The store's currency, such as `AUD`."),
        "items": {"type": "array", "items": ref("AdminCartItem"), "description": "One entry for each line."},
        "totals": ref("AdminCartTotals"),
    }},
    "AdminCartSession": {"type": "object", "properties": {
        "session_id": text("The cart's `session_id`, such as `PRV-3f2a9c41b7d80e65`. Pass it as `session_id` in the path of every other call."),
        "status": text("`active`."),
        "created_at": text("When the cart was created, in UTC, such as `2026-11-12T10:34:55Z`."),
        "expires_at": text("When the session ends: 30 minutes after the last write."),
    }},
    "AdminCartCustomer": {"type": "object", "description": "The customer the cart is for.", "properties": {
        "customer_id": whole("The customer's `customer_id`."),
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": nullable_text("The email address, or `null`."),
    }},
    "AdminCartItem": {"type": "object", "properties": {
        "cart_item_id": whole("The line's `cart_item_id`. The line calls take it in the path. A replace of the cart numbers the lines again."),
        "product_id": whole("The product's `product_id`."),
        "product_name": text("The product's name."),
        "variation_id": nullable_whole("The variation's `variation_id`, or `null` for a product with no variation."),
        "variation_name": nullable_text("The variation's name, or `null`."),
        "sku": text("The SKU."),
        "price": number("The unit price the store charges."),
        "quantity": whole("The quantity on the line."),
        "discount": number("The discount on this line."),
        "tax": number("The tax on this line."),
        "total_amount": number("The line's total."),
        "taxable": flag("Whether the product is taxed."),
        "shippable": flag("Whether the product ships."),
    }},
    "AdminCartTotals": {"type": "object", "description": "The cart's money, before shipping.", "properties": {
        "sub_total": number("The total of the lines, before discounts and tax."),
        "total_discount": number("The discounts on the lines."),
        "total_tax": number("The tax on the lines."),
        "grand_total": number("The cart's total."),
    }},
    "AdminCheckout": {"type": "object", "description": "A cart's checkout. Retrieve and update return every field; the coupon, gift card and delivery schedule calls return only the parts they change.", "properties": {
        "session": ref("AdminCartSession"),
        "customer": ref("AdminCartCustomer"),
        "delivery_type": nullable_text("`delivery`, `others_shipping`, `shipping` or `store_pickup`, or `null` until you set one."),
        "currency_code": text("The store's currency, such as `AUD`."),
        "items": {"type": "array", "items": ref("AdminCartItem"), "description": "One entry for each line."},
        "billing_address": ref("AdminCheckoutAddress"),
        "shipping_address": ref("AdminCheckoutAddress"),
        "shipping": ref("AdminCheckoutShipping"),
        "discounts": ref("AdminCheckoutDiscounts"),
        "delivery_schedule": {"type": ["object", "null"], "description": "The chosen delivery schedule, or `null` until you set one."},
        "totals": ref("AdminCheckoutTotals"),
        "issues": {"type": "array", "items": ref("AdminCheckoutIssue"), "description": "What still blocks the order. Empty when the order can be placed."},
    }},
    "AdminCheckoutDiscountResult": {"type": "object", "description": "What the coupon and gift card calls return: only these three fields of the checkout.", "properties": {
        "session": ref("AdminCartSession"),
        "discounts": ref("AdminCheckoutDiscounts"),
        "totals": ref("AdminCheckoutTotals"),
    }},
    "AdminCheckoutScheduleResult": {"type": "object", "description": "What the delivery schedule read returns: only these two fields of the checkout.", "properties": {
        "session": ref("AdminCartSession"),
        "delivery_schedule": {"type": ["object", "null"], "description": "The chosen delivery schedule, or `null` until you set one."},
    }},
    "AdminCheckoutAddress": {"type": "object", "description": "A billing or shipping address as the checkout returns it. `state` is `{}` when the address has none.", "properties": {
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": text("The email address."),
        "company_name": text("The company name."),
        "address_line_1": text("The first address line."),
        "address_line_2": text("The second address line."),
        "country": {"type": "object", "description": "The country, with its `id`, `name` and `code`."},
        "state": {"type": "object", "description": "The state, with its `id`, `name` and `code`, or `{}`."},
        "city": text("The city."),
        "post_code": text("The post code."),
        "mobile": text("The mobile number."),
        "phone": text("The phone number."),
        "fax": text("The fax number."),
    }},
    "AdminCheckoutShipping": {"type": "object", "description": "The delivery the checkout was priced for. Empty until you set a delivery type.", "properties": {
        "delivery_type": nullable_text("The delivery type, or `null`."),
        "shipping_type": nullable_text("The shipping type the store chose, or an empty string."),
        "shipping_cost": number("The shipping cost. `0` for `store_pickup`."),
        "shipping_tax": number("The tax on shipping. It is part of `totals.grand_total`."),
    }},
    "AdminCheckoutCoupon": {"type": "object", "properties": {
        "code": text("The coupon code."),
        "status": text("The coupon's status, such as `applied`."),
        "applied_amount": number("The amount the coupon takes off."),
    }},
    "AdminCheckoutGiftCard": {"type": "object", "properties": {
        "code": text("The gift card's code."),
        "status": text("The card's status, such as `applied`."),
        "applied_amount": number("The lesser of the card's balance and `totals.grand_total`."),
        "remaining_balance": {"type": ["number", "null"], "description": "The card's remaining balance, or `null`."},
    }},
    "AdminCheckoutDiscounts": {"type": "object", "properties": {
        "coupon": {"oneOf": [ref("AdminCheckoutCoupon"), {"type": "null"}], "description": "The applied coupon, or `null`."},
        "gift_card": {"oneOf": [ref("AdminCheckoutGiftCard"), {"type": "null"}], "description": "The applied gift card, or `null`."},
    }},
    "AdminCheckoutTotals": {"type": "object", "properties": {
        "sub_total": number("The total of the lines, before discounts and tax."),
        "total_discount": number("The coupon's discount."),
        "total_tax": number("The tax on the lines."),
        "shipping_cost": number("The shipping cost."),
        "handling_cost": number("The handling cost."),
        "total_surcharge": number("The surcharge."),
        "gift_card_applied": number("The amount the gift card pays. `0` with no gift card."),
        "grand_total": number("The order's total, with shipping, handling and tax."),
        "due": number("`grand_total` minus `gift_card_applied`."),
    }},
    "AdminCheckoutIssue": {"type": "object", "properties": {
        "field": text("The field that blocks the order, such as `delivery_type`."),
        "code": text("Why, such as `required`."),
        "message": text("The reason, such as `is required`."),
    }},
    "AdminCartProductInput": {"type": "object", "required": ["product_id", "quantity"], "properties": {
        "product_id": whole("The product's `product_id`."),
        "variation_id": whole("The variation's `variation_id`, for a product with variations."),
        "quantity": whole("The quantity to add."),
    }},
    "AdminCartInput": {"type": "object", "required": ["customer_id", "products"], "description": "Send these fields at the top level of the body. A field the call does not accept is rejected with `400` and the code `unknown_field`.", "properties": {
        "customer_id": whole("The customer's `customer_id`, from [Retrieve a customer](" + RETRIEVE_CUSTOMER_PAGE + ") or a listing."),
        "session_id": text("Only for a create: a name for the session, in the `PRV-` form. Leave it out and the store names it."),
        "products": {"type": "array", "items": ref("AdminCartProductInput"), "description": "The products to put on the cart. At least one."},
    }},
    "AdminCartCustomerInput": {"type": "object", "required": ["customer_id"], "properties": {
        "customer_id": whole("The `customer_id` of the customer to move the cart to."),
    }},
    "AdminCartItemsInput": {"type": "object", "required": ["products"], "properties": {
        "products": {"type": "array", "items": ref("AdminCartProductInput"), "description": "The products to add. A product already on the cart raises that line's quantity."},
    }},
    "AdminCartItemUpdateInput": {"type": "object", "required": ["quantity"], "properties": {
        "quantity": whole("The new quantity."),
    }},
    "AdminCheckoutAddressInput": {"type": "object", "description": "An address. It replaces the whole stored address, and a field you leave out reads `\"\"`.", "properties": {
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": text("The email address."),
        "company_name": text("The company name."),
        "address_line_1": text("The first address line."),
        "address_line_2": text("The second address line."),
        "city": text("The city."),
        "post_code": text("The post code."),
        "phone": text("The phone number."),
        "mobile": text("The mobile number."),
        "country_code": text("The country's code, such as `AU`."),
        "state_code": text("The state's code, such as `VIC`."),
    }},
    "AdminCheckoutInput": {"type": "object", "description": "Send these fields at the top level of the body. No other field is taken.", "properties": {
        "delivery_type": {"type": "string", "enum": DELIVERY_TYPES, "description": "How the order is delivered. A `shipping` or `delivery` checkout needs a default shipping profile."},
        "billing_address": ref("AdminCheckoutAddressInput"),
        "shipping_address": ref("AdminCheckoutAddressInput"),
    }},
    "AdminCheckoutCodeInput": {"type": "object", "required": ["code"], "properties": {
        "code": text("The coupon code or the gift card's code."),
    }},
    "AdminCheckoutDeliveryScheduleInput": {"type": "object", "required": ["id", "date"], "properties": {
        "id": whole("The delivery schedule's `id`."),
        "date": text("The delivery date you want, such as `2026-11-20`."),
    }},
    "AdminCheckoutPaymentInput": {"type": "object", "required": ["amount", "payment_method"], "properties": {
        "amount": number("The amount paid. More than the amount due is rejected."),
        "payment_status": text("The payment's status, such as `success`."),
        "payment_method": text("The payment method, such as `manual`."),
        "transaction_reference": text("Your reference for the payment."),
        "transaction_date": text("When the payment was made."),
    }},
    "AdminCheckoutConfirmInput": {"type": "object", "description": "Every field is optional, and the body can be left out. A field the call does not accept is rejected with `400`.", "properties": {
        "payment_gateway": text("The payment gateway's code, such as `PIS`. `PIS` leaves the order unpaid."),
        "transaction_no": text("A transaction number you choose. The store files the order under it. It must match the `X-Transaction-No` header when you send both."),
        "send_email": flag("Whether the store emails the customer."),
        "payment": ref("AdminCheckoutPaymentInput"),
    }},
    "AdminCartError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": text("A machine-readable reason, such as `invalid_request`, `not_found`, `conflict`, `gone` or `unprocessable`."),
        "message": text("What went wrong."),
        "details": {"type": "array", "description": "One entry for each problem, or an empty list.", "items": {"type": "object", "properties": {
            "field": text("The field, such as `code`, `session_id`, `cart_item_id` or `delivery_type`."),
            "code": text("Why it was rejected, such as `unknown_field`, `invalid_coupon`, `session_confirmed` or `session_deleted`."),
            "message": nullable_text("The rule that failed, or `null`."),
            "value": {"description": "The value involved, such as the `order_id` of the order placed from the cart."},
        }}},
        "request_id": text("Identifies this request."),
    }}}},
}
