"""The Payment gateways endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Payment gateways"
SLUG = "payment-gateways"
BASE = "/admin/payment_gateways"
ICON = "credit-card"

OVERVIEW_DESCRIPTION = "List, count and retrieve your store's checkout payment gateways, and change their settings with `PUT` or `PATCH`."
INTRO = "The Payment gateways API has eight endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/payment_gateways`."

RETRIEVE_PAGE = "/api-reference/payment-gateways/retrieve-a-payment-gateway"
PUT_PAGE = "/api-reference/payment-gateways/update-a-payment-gateway-with-put"
PATCH_PAGE = "/api-reference/payment-gateways/update-a-payment-gateway"
LIST_CUSTOMERS_PAGE = "/api-reference/customers/list-customers"
LIST_CUSTOMER_GROUPS_PAGE = "/api-reference/customer-groups/list-customer-groups"

WARNING = (
    "**You cannot send a retrieved gateway back unchanged.** A `PUT` or `PATCH` with the body from\n"
    "  [Retrieve a payment gateway](" + RETRIEVE_PAGE + ") is rejected with `400`: `code` and `promotional`\n"
    "  are read-only, and `surcharge: null` is rejected with `must be an object`. Empty `visibility.customers`\n"
    "  and `visibility.customer_groups` lists are accepted under `type` `everyone`. Send only the fields\n"
    "  you want to change."
)

NOTES = [
    "**Send the fields at the top level of the body, not inside `payment_gateway`.** Both writes take\n"
    "  the bare record. A body wrapped in `payment_gateway`, or any field that is not a gateway field, is\n"
    "  rejected with `400`, the reason `unknown_field` and the message `is not a payment gateway field`.\n"
    "  Responses return the gateway inside `payment_gateway`.",
    "**`PUT` and `PATCH` both change only the fields you send.** `PUT` does not replace the gateway: a\n"
    "  field you leave out keeps its value, as it does with `PATCH`. `allowed_for` merges key by key.\n"
    "  An empty body `{}` is rejected with `400` and the message `request body is empty`.",
    "**You cannot create or delete a gateway.** The gateways already exist in your store. `POST` and\n"
    "  `DELETE` on a gateway, `POST` and `PUT` on the list, and `PATCH` on `/count` are rejected with\n"
    "  `405 method_not_allowed`. `OPTIONS` returns `204` with an `Allow` header: `GET, HEAD, OPTIONS` on\n"
    "  the list and on `/count`, and `GET, HEAD, PUT, PATCH, OPTIONS` on a gateway.",
    "**A listing returns 20 gateways per call unless you send `limit`.** `limit` takes `1` to `100`;\n"
    "  `0` or a value above `100` is rejected with `400` and the reason `out_of_range`. To get the next\n"
    "  page, raise `offset` by `limit` while `pagination.has_next` is `true`. A page past the end returns\n"
    "  no gateways, and its `has_previous` is `false` even though `offset` is above `0`.",
    "**`settings` holds different fields for each gateway, and only a single-gateway read or a write returns it.**\n"
    "  Listing rows have no `settings`. Offline gateways return `{}`. A stored secret, such as an API key\n"
    "  or a client secret, reads `********`. No path returns an `ETag` header.",
    "**Errors have one shape.** The body is an `error` object with `code`, `message`, `details` and\n"
    "  `request_id`. Each `details` entry names the rejected `field` and gives its `code` and `message`.\n"
    "  The entry's `message` is `null` when `limit` is `0` or not a whole number, or `offset` is negative or\n"
    "  not a whole number; the top-level `message` then gives the reason.\n"
    "  A read-only field such as `code` gets two entries: `read_only` and `unknown_field`.",
]

PAYMENT_GATEWAY_ID = {
    "name": "payment_gateway_id",
    "in": "path",
    "required": True,
    "description": "The payment gateway's `id`, from a listing. A gateway's `code`, such as `CHQ`, does not work here and returns `404`.",
    "schema": {"type": "integer", "example": 2},
}

LIMIT = {"name": "limit", "in": "query", "description": "The number of gateways per page, from `1` to `100`. Defaults to `20`. `0` is rejected with `400`, the reason `out_of_range` and the message `'limit' must be a positive integer`. A value above `100` is rejected with `400`, the reason `out_of_range` and the message `limit: must be between 1 and 100`. Text such as `all` or `abc` is rejected with `400`, the reason `invalid_integer` and the message `'limit' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of gateways to skip, `0` or more. A negative or non-numeric value is rejected with `400`, the reason `invalid_integer` and the message `'offset' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "The page number, read as `offset = (page - 1) * limit`. `pagination.offset` shows the result.", "schema": {"type": "integer", "minimum": 1, "example": 1}}
SEARCH = {"name": "search", "in": "query", "description": "Keeps only gateways whose `name` contains this text, in any letter case. `searchText` is accepted as another name for `search`.", "schema": {"type": "string", "example": "card"}}
EXCLUDE = {"name": "exclude", "in": "query", "description": "A comma-separated list of gateway `code` values to leave out, such as `PIS,CHQ`. `excluds` is accepted as another name for `exclude`.", "schema": {"type": "string", "example": "PIS,CHQ"}}
PROMOTIONAL = {"name": "promotional", "in": "query", "description": "`true` keeps only promotional gateways and `false` only the others. `notPromotional=true` works the same as `promotional=false`.", "schema": {"type": "boolean", "example": False}}
ADDED = {"name": "added", "in": "query", "description": "`true` keeps only gateways whose `added` is `true`, and `false` only those whose `added` is `false`.", "schema": {"type": "boolean", "example": True}}
COUNT_LIMIT = {"name": "limit", "in": "query", "description": "Has no effect on `total`, but it is validated as on the listing: text such as `abc` is rejected with `400` and the reason `invalid_integer`, and `0` or a value above `100` with `400` and the reason `out_of_range`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}

REQUEST_ID = "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


ERROR_REF = {"$ref": "#/components/schemas/PaymentGatewayError"}
ROW_REF = {"$ref": "#/components/schemas/PaymentGateway"}
PAGINATION_REF = {"$ref": "#/components/schemas/PaymentGatewayPagination"}
ROW_RESPONSE = {"type": "object", "properties": {"payment_gateway": ROW_REF}}

NOT_FOUND = error("not_found", "Payment gateway 999999 was not found.")
NOT_FOUND_RESPONSE = {
    "description": "No listed gateway has that `payment_gateway_id`. A gateway's `code` in the path returns this too. The reason is `not_found`, the message is `Payment gateway <payment_gateway_id> was not found.`, and `details` is empty.",
    "schema": ERROR_REF,
    "example": NOT_FOUND,
}

EVERYONE = {"type": "everyone", "customers": [], "customer_groups": []}
ALL_DELIVERY_TYPES = {"shipping": True, "delivery": True, "store_pickup": True}

PAY_IN_STORE = {
    "id": 1, "code": "PIS", "name": "Pay In Store", "added": True, "enabled": True, "default": True,
    "promotional": False, "zone": None, "information": "Pay at the counter when you collect your order.",
    "visibility": EVERYONE, "allowed_for": ALL_DELIVERY_TYPES, "surcharge": None,
    "messages": {"pending": "Your order is waiting for payment in store.", "completed": None},
}
CHEQUE = {
    "id": 2, "code": "CHQ", "name": "Cheque", "added": True, "enabled": False, "default": False,
    "promotional": False, "zone": None, "information": None,
    "visibility": EVERYONE, "allowed_for": ALL_DELIVERY_TYPES, "surcharge": None,
    "messages": {"pending": None, "completed": None},
}

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CHEQUE_READ = dict(CHEQUE, settings={})
PUT_BODY = {"information": "Make cheques payable to Example Store."}
PUT_ROW = dict(CHEQUE_READ, information=PUT_BODY["information"])
PATCH_BODY = {"allowed_for": {"store_pickup": False}}
PATCH_ROW = dict(CHEQUE_READ, allowed_for={"shipping": True, "delivery": True, "store_pickup": False})

WRITE_400 = (
    "The body is not valid for this gateway. It is `{}` (message `request body is empty`); it is wrapped in `payment_gateway` "
    "or has a field that is not a gateway field (reason `unknown_field`, message `is not a payment gateway field`); "
    "it sends `code` or `promotional`, even unchanged (two entries each, reasons `read_only` and `unknown_field`); "
    "`information` is longer than 2000 characters (reason `too_long`); `zone` names a zone the store does not have "
    "(reason `unknown_reference`, message `no zone exists with id <id>`); or `surcharge` is `null` (reason `invalid_type`, "
    "message `must be an object`). `error.code` is `invalid_request`, and the "
    "reason for each field is in `details[].code`."
)

ENDPOINTS = [
    {
        "key": "list_payment_gateways",
        "slug": "list-payment-gateways",
        "title": "List payment gateways",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 payment gateways per call, or the `limit` you send, in `id` order.",
        "description": "Returns your store's payment gateways in `payment_gateways`, in ascending `id` order, 20 per call unless you send `limit`, and `pagination` with the paging details. Rows have no `settings`; use [Retrieve a payment gateway](" + RETRIEVE_PAGE + ") to read them. Send `search` to match part of a `name`, `exclude` to leave out gateways by `code`, and `promotional` or `added` to filter on those fields. `sort`, `order`, `dir`, `enabled`, `code`, `q`, `field_metadata` and any other parameter the listing does not know are ignored.",
        "parameters": [LIMIT, OFFSET, PAGE, SEARCH, EXCLUDE, PROMOTIONAL, ADDED],
        "responses": {
            "200": {
                "description": "The gateways on this page in `payment_gateways`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "payment_gateways": {"type": "array", "items": ROW_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"payment_gateways": [PAY_IN_STORE, CHEQUE], "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is `0` or above `100` (reason `out_of_range`) or not a number (reason `invalid_integer`, message `'limit' must be a non-negative integer`), or `offset` is negative or not a number (reason `invalid_integer`, message `'offset' must be a non-negative integer`).",
                "schema": ERROR_REF,
                "example": error("invalid_request", "limit: must be between 1 and 100", [
                    {"field": "limit", "code": "out_of_range", "message": "must be between 1 and 100", "value": "150"},
                ]),
            },
        },
        "example_call": {"query": {"limit": 20, "offset": 0, "promotional": "false"}},
    },
    {
        "key": "head_payment_gateways",
        "slug": "check-the-payment-gateways-list",
        "title": "Check the payment gateways list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the payment gateways list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. The SDK functions send no query parameters with this call.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_payment_gateways",
        "slug": "count-payment-gateways",
        "title": "Count payment gateways",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of payment gateways that match your filters, as `total`.",
        "description": "Returns the number of gateways as `total`, at the top level of the body. `search`, `exclude`, `promotional` and `added` narrow the count as they narrow the listing, so `total` matches the listing's `pagination.total` for the same filters. `limit` is checked but does not change the count, and any other parameter the count does not know is ignored.",
        "parameters": [SEARCH, EXCLUDE, PROMOTIONAL, ADDED, COUNT_LIMIT],
        "responses": {
            "200": {
                "description": "The number of matching gateways. The response has no `ETag` header.",
                "schema": {"$ref": "#/components/schemas/PaymentGatewayCount"},
                "example": {"total": 13},
            },
            "400": {"description": "`limit` is not a number (reason `invalid_integer`), or it is `0` or above `100` (reason `out_of_range`).", "schema": ERROR_REF},
        },
        "example_call": {"query": {"exclude": "PIS,CHQ"}},
    },
    {
        "key": "head_payment_gateways_count",
        "slug": "check-the-payment-gateway-count",
        "title": "Check the payment gateway count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Checks that the payment gateway count is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. The SDK functions send no query parameters with this call.",
        "responses": {
            "200": {"description": "The count is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "get_payment_gateway",
        "slug": "retrieve-a-payment-gateway",
        "title": "Retrieve a payment gateway",
        "method": "GET",
        "path": BASE + "/{payment_gateway_id}",
        "summary": "Returns the payment gateway whose `id` you pass as `payment_gateway_id`, with its `settings`.",
        "description": "Returns one gateway under the `payment_gateway` key, with the fields a listing row has plus `settings`. The fields in `settings` depend on the gateway, and offline gateways return `{}`. A stored secret, such as an API key or a client secret, reads `********`. Query parameters, `field_metadata` included, are ignored.",
        "parameters": [PAYMENT_GATEWAY_ID],
        "responses": {
            "200": {
                "description": "The payment gateway, with `settings`. The response has no `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"payment_gateway": CHEQUE_READ},
            },
            "404": NOT_FOUND_RESPONSE,
        },
        "example_call": {"path": {"payment_gateway_id": 2}},
    },
    {
        "key": "head_payment_gateway",
        "slug": "check-a-payment-gateway",
        "title": "Check a payment gateway",
        "method": "HEAD",
        "path": BASE + "/{payment_gateway_id}",
        "summary": "Checks whether a payment gateway exists. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body when a listed gateway has that `payment_gateway_id`, and `404` when none does. To read the gateway's fields, use [Retrieve a payment gateway](" + RETRIEVE_PAGE + ").",
        "parameters": [PAYMENT_GATEWAY_ID],
        "responses": {
            "200": {"description": "The gateway exists. Headers only, no body."},
            "404": {"description": "No listed gateway has that `payment_gateway_id`."},
        },
        "example_call": {"path": {"payment_gateway_id": 2}},
    },
    {
        "key": "update_payment_gateway",
        "slug": "update-a-payment-gateway-with-put",
        "title": "Update a payment gateway with PUT",
        "method": "PUT",
        "path": BASE + "/{payment_gateway_id}",
        "summary": "Changes the fields you send on a payment gateway and returns the whole gateway.",
        "description": "Send the fields you want to change at the top level of the body, not wrapped in `payment_gateway`. This `PUT` does not replace the gateway: every field you leave out keeps its value, as with [Update a payment gateway](" + PATCH_PAGE + "). `information: null` clears the text. `code` and `promotional` are read-only, so a retrieved gateway sent back unchanged is rejected with `400`; send only the fields you change.",
        "parameters": [PAYMENT_GATEWAY_ID],
        "body": {"schema": {"$ref": "#/components/schemas/PaymentGatewayInput"}, "example": PUT_BODY},
        "responses": {
            "200": {
                "description": "The whole gateway after the change, with `settings`. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"payment_gateway": PUT_ROW},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {"path": {"payment_gateway_id": 2}},
    },
    {
        "key": "patch_payment_gateway",
        "slug": "update-a-payment-gateway",
        "title": "Update a payment gateway",
        "method": "PATCH",
        "path": BASE + "/{payment_gateway_id}",
        "summary": "Changes only the fields you send on a payment gateway and returns the whole gateway.",
        "description": "Send only the fields you want to change, at the top level of the body, not wrapped in `payment_gateway`. Fields you leave out keep their values, and `allowed_for` merges key by key, so `{\"allowed_for\": {\"store_pickup\": false}}` leaves `shipping` and `delivery` as they were. `information: null` clears the text, and `zone` takes a zone's `id` or `{\"id\": ...}`. [Update a payment gateway with PUT](" + PUT_PAGE + ") behaves the same way.",
        "parameters": [PAYMENT_GATEWAY_ID],
        "body": {"schema": {"$ref": "#/components/schemas/PaymentGatewayInput"}, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The whole gateway after the change, with `settings`. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"payment_gateway": PATCH_ROW},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {"path": {"payment_gateway_id": 2}},
    },
]

SCHEMAS = {
    "PaymentGateway": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The payment gateway's `id`. Pass it as `payment_gateway_id` in a path."},
        "code": {"type": "string", "description": "The gateway type's fixed code, such as `PIS` or `CHQ`. Read-only. The listing's `exclude` parameter takes these codes."},
        "name": {"type": "string", "description": "The gateway's display name, such as `Cheque`. The listing's `search` parameter matches it."},
        "added": {"type": "boolean", "description": "Whether the gateway is added to the store. The listing's `added` parameter filters on it."},
        "enabled": {"type": "boolean", "description": "Whether the gateway is enabled."},
        "default": {"type": "boolean", "description": "Whether the gateway is the default."},
        "promotional": {"type": "boolean", "description": "Whether the gateway is promotional. Read-only. The listing's `promotional` parameter filters on it."},
        "zone": {"oneOf": [{"$ref": "#/components/schemas/PaymentGatewayReference"}, {"type": "null"}], "description": "The zone's `id` and `name`, or `null` when none is set."},
        "information": {"type": ["string", "null"], "description": "The gateway's information text, at most 2000 characters, or `null`."},
        "visibility": {"$ref": "#/components/schemas/PaymentGatewayVisibility"},
        "allowed_for": {"oneOf": [{"$ref": "#/components/schemas/PaymentGatewayAllowedFor"}, {"type": "null"}], "description": "The delivery types the gateway is offered for, or `null` on a gateway without that choice."},
        "surcharge": {"oneOf": [{"$ref": "#/components/schemas/PaymentGatewaySurcharge"}, {"type": "null"}], "description": "The gateway's surcharge, or `null` on a gateway without one."},
        "messages": {"$ref": "#/components/schemas/PaymentGatewayMessages"},
        "settings": {"allOf": [{"$ref": "#/components/schemas/PaymentGatewaySettings"}], "description": "The gateway's own settings. Returned by a single-gateway read and by both writes; listing rows have no `settings`."},
    }},
    "PaymentGatewayReference": {"type": "object", "description": "An `id` and `name` pair: the gateway's `zone`, or one customer or customer group in `visibility`.", "properties": {
        "id": {"type": "integer", "description": "The zone's, customer's or customer group's `id`."},
        "name": {"type": "string", "description": "The zone's, customer's or customer group's name."},
    }},
    "PaymentGatewayVisibility": {"type": "object", "description": "Who sees the gateway at checkout.", "properties": {
        "type": {"type": "string", "enum": ["everyone", "customer", "selected"], "description": "One of `everyone`, `customer` or `selected`."},
        "customers": {"type": "array", "items": {"$ref": "#/components/schemas/PaymentGatewayReference"}, "description": "The selected customers. Filled only when `type` is `selected`; otherwise an empty list."},
        "customer_groups": {"type": "array", "items": {"$ref": "#/components/schemas/PaymentGatewayReference"}, "description": "The selected customer groups. Filled only when `type` is `selected`; otherwise an empty list."},
    }},
    "PaymentGatewayAllowedFor": {"type": "object", "description": "The delivery types the gateway is offered for. A write merges these keys one by one: a key you leave out keeps its value.", "properties": {
        "shipping": {"type": "boolean"},
        "delivery": {"type": "boolean"},
        "store_pickup": {"type": "boolean"},
    }},
    "PaymentGatewaySurcharge": {"type": "object", "description": "The gateway's surcharge settings. Sending `\"surcharge\": null` is rejected with `400` and the message `must be an object`.", "properties": {
        "type": {"type": "string", "enum": ["no_surcharge", "flat_surcharge", "percent_surcharge", "surcharge_on_amount_range"]},
        "flat_amount": {"type": "number", "description": "The amount of a `flat_surcharge`."},
        "percent_amount": {"type": ["number", "null"], "description": "The percentage of a `percent_surcharge`, or `null` when none is set."},
        "ranges": {"type": "array", "items": {"$ref": "#/components/schemas/PaymentGatewaySurchargeRange"}, "description": "The amount ranges of a `surcharge_on_amount_range`."},
    }},
    "PaymentGatewaySurchargeRange": {"type": "object", "description": "One amount range of a surcharge.", "properties": {
        "id": {"description": "The range's `id`."},
        "from": {"type": "number"},
        "to": {"type": "number"},
        "amount": {"type": "number"},
    }},
    "PaymentGatewayMessages": {"type": "object", "properties": {
        "pending": {"type": ["string", "null"], "description": "The pending message, or `null`. `null` on a gateway that has no pending message."},
        "completed": {"type": ["string", "null"], "description": "The completed message, or `null`. `null` on a gateway that has no completed message."},
    }},
    "PaymentGatewaySettings": {"type": "object", "description": "The gateway's own settings. Each gateway returns only its own few fields, and offline gateways return `{}`: PayPal returns `version`, `mode`, `standard` and `classic`; the card gateway `processor` and `card_logo`; Express Checkout `google_pay`, `apple_pay` and `paypal`; Payright, Zip and Afterpay their `mode`, keys and display switches; Loyalty Point `amount_per_100_points`. A stored secret reads `********`.", "properties": {
        "version": {"type": "string"},
        "mode": {"type": "string"},
        "standard": {"$ref": "#/components/schemas/PaymentGatewayPayPalStandard"},
        "classic": {"$ref": "#/components/schemas/PaymentGatewayPayPalClassic"},
        "processor": {"$ref": "#/components/schemas/PaymentGatewayCardProcessor"},
        "card_logo": {"$ref": "#/components/schemas/PaymentGatewayCardLogo"},
        "google_pay": {"$ref": "#/components/schemas/PaymentGatewayGooglePay"},
        "apple_pay": {"$ref": "#/components/schemas/PaymentGatewayApplePay"},
        "paypal": {"$ref": "#/components/schemas/PaymentGatewayExpressPayPal"},
        "show_installment_amount": {"type": "boolean"},
        "show_in_product_details": {"type": "boolean"},
        "api_key": {"type": "string", "description": "Reads `********` when a key is stored."},
        "default_term": {"type": "integer"},
        "amount_per_100_points": {"type": "number"},
        "merchant_id": {"type": "string"},
        "merchant_secret_key": {"type": "string", "description": "Reads `********` when a key is stored."},
        "image": {"description": "Always `null`."},
    }},
    "PaymentGatewayPayPalStandard": {"type": "object", "description": "PayPal's `standard` credentials.", "properties": {
        "client_id": {"type": "string"},
        "client_secret": {"type": "string", "description": "Reads `********` when a secret is stored."},
    }},
    "PaymentGatewayPayPalClassic": {"type": "object", "description": "PayPal's `classic` account.", "properties": {
        "email_address": {"type": "string", "description": "The account's email address, such as `payments@example.com`."},
    }},
    "PaymentGatewayCardProcessor": {"type": "object", "description": "The card gateway's processor.", "properties": {
        "type": {"type": "string"},
        "mode": {"type": "string"},
        "merchant_code": {"type": "string"},
        "client_id": {"type": "string", "description": "Reads `********` when set."},
        "client_secret": {"type": "string", "description": "Reads `********` when set."},
        "wallet_payment": {"$ref": "#/components/schemas/PaymentGatewayToggle"},
    }},
    "PaymentGatewayToggle": {"type": "object", "description": "A switch with one key.", "properties": {
        "enabled": {"type": "boolean"},
    }},
    "PaymentGatewayCardLogo": {"type": "object", "description": "The card logos shown at checkout.", "properties": {
        "type": {"type": "string"},
        "cards": {"type": "array", "items": {"type": "string"}},
        "custom_image": {"description": "Always `null`."},
    }},
    "PaymentGatewayGooglePay": {"type": "object", "description": "Express Checkout's Google Pay settings.", "properties": {
        "enabled": {"type": "boolean"},
        "payment_mode": {"type": "string"},
        "merchant_name": {"type": "string"},
        "merchant_id": {"type": "string"},
        "processor": {"type": "string"},
        "secret_key": {"type": "string"},
        "public_key": {"type": "string"},
        "free_shipping_condition_amount": {"type": "number"},
        "shipping_cost": {"type": "number"},
    }},
    "PaymentGatewayApplePay": {"type": "object", "description": "Express Checkout's Apple Pay settings.", "properties": {
        "enabled": {"type": "boolean"},
        "payment_mode": {"type": "string"},
        "merchant_identifier": {"type": "string"},
        "domain_name": {"type": "string"},
        "display_name": {"type": "string"},
        "processor": {"type": "string"},
        "secret_key": {"type": "string"},
        "public_key": {"type": "string"},
    }},
    "PaymentGatewayExpressPayPal": {"type": "object", "description": "Express Checkout's PayPal settings.", "properties": {
        "show_installment_amount": {"type": "boolean"},
    }},
    "PaymentGatewayInput": {"type": "object", "minProperties": 1, "description": "Send at least one of these fields, at the top level of the body. Fields you leave out keep their values. `code`, `promotional` and any other field are rejected with `400`. An `id` equal to `payment_gateway_id` is accepted. `availableFor` is accepted as another name for `visibility.type`.", "properties": {
        "name": {"type": "string"},
        "added": {"type": "boolean"},
        "enabled": {"type": "boolean"},
        "default": {"type": "boolean"},
        "zone": {"oneOf": [{"type": "integer"}, {"type": "object", "properties": {"id": {"type": "integer"}}}, {"type": "null"}], "description": "A zone's `id`, or `{\"id\": ...}`. `null` is accepted. An `id` no zone has is rejected with `400` and the message `no zone exists with id <id>`."},
        "information": {"type": ["string", "null"], "maxLength": 2000, "description": "At most 2000 characters. `null` clears it."},
        "visibility": {"$ref": "#/components/schemas/PaymentGatewayVisibilityInput"},
        "allowed_for": {"$ref": "#/components/schemas/PaymentGatewayAllowedFor"},
        "surcharge": {"$ref": "#/components/schemas/PaymentGatewaySurcharge"},
        "messages": {"$ref": "#/components/schemas/PaymentGatewayMessages"},
        "settings": {"$ref": "#/components/schemas/PaymentGatewaySettings"},
    }},
    "PaymentGatewayVisibilityInput": {"type": "object", "description": "Who sees the gateway at checkout. Customers and customer groups are sent as `id` lists.", "properties": {
        "type": {"type": "string", "enum": ["everyone", "customer", "selected"]},
        "customers": {"type": "array", "items": {"type": "integer"}, "description": "Customer `id` values, from [List customers](" + LIST_CUSTOMERS_PAGE + "). Send it with `type` `selected`. With `type` `everyone`, an empty list is accepted."},
        "customer_groups": {"type": "array", "items": {"type": "integer"}, "description": "Customer group `id` values, from [List customer groups](" + LIST_CUSTOMER_GROUPS_PAGE + "). Send it with `type` `selected`. With `type` `everyone`, an empty list is accepted."},
    }},
    "PaymentGatewayCount": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of gateways that match your filters."},
    }},
    "PaymentGatewayPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of gateways that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20` when you send none."},
        "offset": {"type": "integer", "description": "The number of gateways skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` on every page after the first, including `offset=1` and `page=2`. On a page past the end, which returns no gateways, it is `false` even though `offset` is above `0`."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
    }},
    "PaymentGatewayError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What went wrong, such as `Payment gateway 999999 was not found.`."},
        "details": {"type": "array", "description": "One entry per rejected field or query parameter. Empty on a `404`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected, such as `information` or `visibility.customers`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `read_only`, `too_long` or `invalid_type`."},
            "message": {"type": ["string", "null"], "description": "The reason in words, such as `is not a payment gateway field`. `null` when `limit` is `0` or not a whole number, or `offset` is negative or not a whole number; the top-level `message` then gives the reason."},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
