"""The Order flags endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Order flags"
SLUG = "order-flags"
BASE = "/admin/order_flags"
ICON = "flag"

OVERVIEW_DESCRIPTION = "List, create, read, replace and delete your store's order flags."
INTRO = "The Order flags API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/order_flags`."

LIST_PAGE = "/api-reference/order-flags/list-order-flags"
RETRIEVE_PAGE = "/api-reference/order-flags/retrieve-an-order-flag"
ECOMMERCE_SETTINGS_PAGE = "/api-reference/ecommerce-settings/get-ecommerce-settings"

WARNING = (
    "**An update replaces the whole order flag, so send every field you want to keep.** `PUT` does not\n"
    "  merge: if you leave `description` out of the body, the store sets it to `null`. `name` and `color`\n"
    "  are required on every update, and `PATCH` is rejected with `405`."
)

NOTES = [
    "**Wrap the flag in `order_flag` on create and on update.** Send\n"
    "  `{\"order_flag\": {\"name\": \"Awaiting Stock\", \"color\": \"#5A7BD4\"}}`. A bare record is rejected\n"
    "  with `400` and the message `order_flag missing`.",
    "**`name` and `color` are required, and `description` is optional.** When you create a flag, a\n"
    "  `color` that is not a hex code such as `#FF6868` is rejected with `400`, and a `name` another order\n"
    "  flag already has is rejected with `409`. A new flag's `description` is `null` unless you send one.",
    "**A `201` does not mean the store kept every field you sent.** Inside `order_flag`, the store ignores\n"
    "  any `id` or `type` you send, and any field it does not know, and still returns `201`. It assigns\n"
    "  the new order flag's `id` itself, and `type` is always `order`.",
    "**A listing returns at most 20 order flags per call, sorted by `name`.** A larger `limit` is capped\n"
    "  at `20`, and `pagination.limit` shows `20`. To get more, send the next `page` or a higher `offset`\n"
    "  while `pagination.has_next` is `true`. The listing accepts only `limit`, `offset`, `page` and\n"
    "  `field_metadata`, and rejects any other parameter with `400`.",
    "**Ecommerce settings shows these flags, but you change them only here.**\n"
    "  [Get ecommerce settings](" + ECOMMERCE_SETTINGS_PAGE + ") lists the store's order flags under\n"
    "  `order_flags`, and its `group_meta` entry for them has `writable` set to `false` and `href` set to\n"
    "  `/api/v4/admin/order_flags`.",
]

ORDER_FLAG_ID = {
    "name": "order_flag_id",
    "in": "path",
    "required": True,
    "description": "The order flag's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 2},
}

LIMIT = {"name": "limit", "in": "query", "description": "Order flags per page, at most `20`. A larger value is capped at `20`, and `pagination.limit` shows `20`. `0` or less is rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of order flags to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`.", "schema": {"type": "integer", "example": 1}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted, but adds nothing: the response still has only `order_flags` and `pagination`.", "schema": {"type": "boolean", "example": True}}

REQUEST_ID = "5c98dbea-ea13-4b77-b0b0-476ad4104429"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


NOT_FOUND = error("not_found", "Order flag not found")
COLOR_REQUIRED = error("invalid_request", "color is required", [{"field": "color", "code": "required", "message": "color is required"}])
DUPLICATE_NAME = error("conflict", "an order flag named 'Awaiting Stock' already exists", [{"field": "name", "code": "duplicate", "message": "name already exists", "value": "Awaiting Stock"}])
UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): sort", [{"field": "sort", "code": "unknown_parameter", "message": None}])

ERROR_REF = ref("OrderFlagError")
ROW_REF = ref("OrderFlag")
WRITE_BODY = {"type": "object", "required": ["order_flag"], "properties": {"order_flag": ref("OrderFlagInput")}}
ROW_RESPONSE = {"type": "object", "properties": {"order_flag": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 2, "name": "Partial Shipment", "color": "#4FD9FC", "description": None, "type": "order"},
    {"id": 1, "name": "Payment Failed", "color": "#FF6868", "description": None, "type": "order"},
    {"id": 3, "name": "Payment Pending", "color": "#FFA959", "description": None, "type": "order"},
]

SAMPLE_PAGINATION = {"total": 3, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"order_flag": {"name": "Awaiting Stock", "color": "#5A7BD4", "description": "Waiting for stock to arrive."}}
CREATED_FLAG = {"id": 4, "name": "Awaiting Stock", "color": "#5A7BD4", "description": "Waiting for stock to arrive.", "type": "order"}

UPDATE_BODY = {"order_flag": {"name": "Awaiting Stock", "color": "#B02E2E", "description": "Waiting for stock from the supplier."}}
UPDATED_FLAG = {"id": 4, "name": "Awaiting Stock", "color": "#B02E2E", "description": "Waiting for stock from the supplier.", "type": "order"}

CREATE_400 = "The body is not wrapped in `order_flag` (`order_flag missing`), `name` or `color` is missing (for example `color is required`), or `color` is not a hex code (`color must be a hex code like #FF6868`)."
UPDATE_400 = "The body is not wrapped in `order_flag` (`order_flag missing`), or `name` or `color` is missing (for example `color is required`)."
CREATE_409 = "Another order flag already has that `name`. The message is `an order flag named '<name>' already exists` and `details[0].code` is `duplicate`."

ENDPOINTS = [
    {
        "key": "list_order_flags",
        "slug": "list-order-flags",
        "title": "List order flags",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 order flags per call, sorted by `name`, with paging details.",
        "description": "Returns the store's order flags under `order_flags`, sorted by `name`, at most 20 per call, and a `pagination` object with the `total` and `has_next`. Only `limit`, `offset`, `page` and `field_metadata` are accepted; any other parameter, such as `sort`, is rejected with `400`. After a rejected `limit=0`, the next request on the same client returns that rejection's body instead of its own. The response has `ETag` and `Last-Modified` headers.",
        "parameters": [LIMIT, OFFSET, PAGE, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The order flags on this page under `order_flags`, sorted by `name`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`.",
                "schema": {"type": "object", "properties": {
                    "order_flags": {"type": "array", "items": ROW_REF},
                    "pagination": ref("OrderFlagPagination"),
                }},
                "example": {"order_flags": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a parameter the listing does not accept: the message is `unknown query parameter(s): <name>` and `details[0].code` is `unknown_parameter`. Or you sent a `limit` of `0` or less.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_order_flags",
        "slug": "check-the-order-flags-list",
        "title": "Check the order flags list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the order flags list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. Unlike [List order flags](" + LIST_PAGE + "), the response has no `ETag` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body, and no `ETag` header."},
        },
        "example_call": {},
    },
    {
        "key": "create_order_flag",
        "slug": "create-an-order-flag",
        "title": "Create an order flag",
        "method": "POST",
        "path": BASE,
        "summary": "Creates an order flag and returns it with its `id`, which other calls take as `order_flag_id`.",
        "description": "Creates an order flag and returns it with the `id` the store assigned. Pass the flag's `id` as `order_flag_id` to retrieve, replace or delete it. Wrap the record in `order_flag`: `name` and `color` are required, and `description` is optional. The store ignores any `id`, `type` or unknown field you send inside `order_flag`, and sets `type` to `order`.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new order flag, with the `id` the store assigned. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"order_flag": CREATED_FLAG},
            },
            "400": {"description": CREATE_400, "schema": ERROR_REF, "example": COLOR_REQUIRED},
            "409": {"description": CREATE_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "get_order_flag",
        "slug": "retrieve-an-order-flag",
        "title": "Retrieve an order flag",
        "method": "GET",
        "path": BASE + "/{order_flag_id}",
        "summary": "Returns the order flag whose `id` you pass as `order_flag_id`.",
        "description": "Returns one order flag under the `order_flag` key, with the same five fields each flag in a listing has: `id`, `name`, `color`, `description` and `type`. Unknown query parameters are ignored. The response has no `ETag` header.",
        "parameters": [ORDER_FLAG_ID],
        "responses": {
            "200": {
                "description": "The order flag, under `order_flag`.",
                "schema": ROW_RESPONSE,
                "example": {"order_flag": SAMPLE_ROWS[0]},
            },
            "404": {"description": "No order flag has that `order_flag_id`, or it is not a number. The message is `Order flag not found`.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"order_flag_id": 2}},
    },
    {
        "key": "head_order_flag",
        "slug": "check-an-order-flag",
        "title": "Check an order flag",
        "method": "HEAD",
        "path": BASE + "/{order_flag_id}",
        "summary": "Returns headers only, with no body, for the order flag you pass as `order_flag_id`.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. It returns `200` even when no order flag has that `order_flag_id`, so it does not tell you whether the flag exists. To read the flag's fields, or to get `404` for a flag that does not exist, use [Retrieve an order flag](" + RETRIEVE_PAGE + ").",
        "parameters": [ORDER_FLAG_ID],
        "responses": {
            "200": {"description": "Headers only, no body, and no `ETag` header. You get `200` for any `order_flag_id`, including one no order flag has."},
        },
        "example_call": {"path": {"order_flag_id": 2}},
    },
    {
        "key": "update_order_flag",
        "slug": "replace-an-order-flag",
        "title": "Replace an order flag",
        "method": "PUT",
        "path": BASE + "/{order_flag_id}",
        "summary": "Replaces an order flag's `name`, `color` and `description` and returns the updated flag.",
        "description": "Replaces the order flag whose `id` you pass as `order_flag_id` with the fields you send, and returns it. This is a replace, not a merge: `name` and `color` are required, and if you leave out `description` it is set to `null`. Wrap the fields in `order_flag`. `PATCH` is rejected with `405 method_not_allowed` and the message `HTTP method not allowed for this endpoint.`",
        "parameters": [ORDER_FLAG_ID],
        "body": {"schema": WRITE_BODY, "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The order flag with the values you sent. If you left out `description`, it is `null`.",
                "schema": ROW_RESPONSE,
                "example": {"order_flag": UPDATED_FLAG},
            },
            "400": {"description": UPDATE_400, "schema": ERROR_REF, "example": COLOR_REQUIRED},
        },
        "example_call": {"path": {"order_flag_id": 4}},
    },
    {
        "key": "delete_order_flag",
        "slug": "delete-an-order-flag",
        "title": "Delete an order flag",
        "method": "DELETE",
        "path": BASE + "/{order_flag_id}",
        "summary": "Permanently deletes the order flag whose `id` you pass as `order_flag_id`. Returns no body.",
        "description": "Deletes the order flag permanently and returns `204` with no body. The flag no longer appears in the listing, and the listing's `pagination.total` goes down by one. Retrieving it or deleting it again returns `404`.",
        "parameters": [ORDER_FLAG_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No order flag has that `order_flag_id`, including a flag you already deleted. The message is `Order flag not found`.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"order_flag_id": 4}},
    },
]

SCHEMAS = {
    "OrderFlag": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The order flag's `id`, assigned by the store. The other calls take it as `order_flag_id`."},
        "name": {"type": "string", "description": "The flag's name. No two order flags have the same name."},
        "color": {"type": "string", "description": "The flag's colour as a hex code, such as `#FF6868`."},
        "description": {"type": ["string", "null"], "description": "The flag's description, or `null` when it has none."},
        "type": {"type": "string", "description": "Always `order`. No write changes it."},
    }},
    "OrderFlagInput": {"type": "object", "required": ["name", "color"], "properties": {
        "name": {"type": "string", "description": "Required. On create, a name another order flag already has is rejected with `409`."},
        "color": {"type": "string", "description": "Required. Send a hex code, such as `#FF6868`: a create with any other value is rejected with `400`."},
        "description": {"type": ["string", "null"], "description": "Optional. `null` when you leave it out, on create and on update."},
    }},
    "OrderFlagPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of order flags in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of order flags skipped before this page."},
        "has_previous": {"type": "boolean", "description": "Whether a page comes before this one."},
        "has_next": {"type": "boolean", "description": "Whether a page comes after this one."},
    }},
    "OrderFlagError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string", "description": "What went wrong, such as `Order flag not found` or `color is required`."},
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list. The first entry's `code` gives the reason, such as `required`, `duplicate` or `unknown_parameter`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected."},
            "message": {"type": ["string", "null"]},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
