"""The Shipping methods endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping methods"
SLUG = "shipping-methods"
BASE = "/admin/shipping_methods"
ICON = "truck"

OVERVIEW_DESCRIPTION = "List, count, create, rename and delete shipping methods, and choose which one is the default."
INTRO = "The Shipping methods API has nine endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/shipping_methods`."

RETRIEVE_PAGE = "/api-reference/shipping-methods/retrieve-a-shipping-method"
DEFAULT_PAGE = "/api-reference/shipping-methods/set-the-default-shipping-method"

WARNING = (
    "**A `HEAD` request for one shipping method returns `200` even when no method has the `shipping_method_id` you send**,\n"
    "  so it does not tell you whether the method exists. To check that, call\n"
    "  [Retrieve a shipping method](" + RETRIEVE_PAGE + ") instead: it returns `404` when no method\n"
    "  has that `shipping_method_id`."
)

NOTES = [
    "**Create and rename wrap the method in `shipping_method`.** Send `{\"shipping_method\": {\"name\": \"Express Post\"}}`\n"
    "  to create or rename a method. A bare record, or the plural `shipping_methods` key, is rejected\n"
    "  with `400` and the message `shipping_method missing`.",
    "**`name` is the only field you can write.** It is required, at most 100 characters, and must be\n"
    "  unique: a name another method already has is rejected with `409`. The store ignores `id` and\n"
    "  `is_default` if you send them inside `shipping_method`.",
    "**Only one method is the default, and only one call changes it.**\n"
    "  [Set the default shipping method](" + DEFAULT_PAGE + ") gives the flag to the method you name and\n"
    "  takes it from the method that had it. You cannot delete the default method: make another method\n"
    "  the default first, or the delete is rejected with `409`.",
    "**A listing returns at most 20 methods per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get more, send the next `page` or a higher `offset` while\n"
    "  `pagination.has_next` is `true`. The listing accepts only `limit`, `offset`, `page` and\n"
    "  `field_metadata`, and rejects any other parameter with `400`.",
    "**`PATCH` does not change a method.** A `PATCH` on a method returns `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and changes nothing. Use `PUT` to\n"
    "  rename a method.",
]

SHIPPING_METHOD_ID = {
    "name": "shipping_method_id",
    "in": "path",
    "required": True,
    "description": "The shipping method's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 2},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rows per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rows to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied. `page=2` alone skips 20 rows; `limit=2&page=2` skips 2.", "schema": {"type": "integer", "example": 1}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key that describes each field: its type, whether you can write it, whether it is required, its maximum length, and what it holds.", "schema": {"type": "boolean", "example": True}}

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Shipping method not found")
NAME_REQUIRED = error("invalid_request", "name is required")
DUPLICATE_NAME = error("conflict", "a shipping method named 'Express Post' already exists", [{"code": "duplicate"}])
DUPLICATE_RENAME = error("conflict", "a shipping method named 'Express Post Next Day' already exists", [{"code": "duplicate"}])
DEFAULT_IN_USE = error("conflict", "cannot delete the default shipping method; set another as default first", [{"code": "default_in_use"}])
UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): sort", [{"code": "unknown_parameter"}])

ERROR_REF = {"$ref": "#/components/schemas/Error"}
ROW_REF = {"$ref": "#/components/schemas/ShippingMethod"}
WRITE_BODY = {"type": "object", "required": ["shipping_method"], "properties": {"shipping_method": {"$ref": "#/components/schemas/ShippingMethodInput"}}}
ROW_RESPONSE = {"type": "object", "properties": {"shipping_method": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 1, "name": "Standard Shipping", "is_default": True},
    {"id": 2, "name": "Express Shipping", "is_default": False},
    {"id": 3, "name": "Local Pickup", "is_default": False},
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

WRITE_400 = "The body is not wrapped in `shipping_method` (`shipping_method missing`), `name` is missing (`name is required`), or `name` is longer than 100 characters (`name must be 100 characters or fewer`)."
WRITE_409 = "Another method already has that name. The message is `a shipping method named '<name>' already exists` and `details[0].code` is `duplicate`."

ENDPOINTS = [
    {
        "key": "list_shipping_methods",
        "slug": "list-shipping-methods",
        "title": "List shipping methods",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 shipping methods per call, in `id` order, with paging details.",
        "description": "Returns the shipping methods in ascending `id` order, up to 20 per call, with a `pagination` block. The default method is not moved to the top. Only `limit`, `offset`, `page` and `field_metadata` are accepted; any other parameter, such as `sort` or `q`, is rejected with `400`. After a rejected `limit=0`, the next request on the same client returns that rejection's body instead of its own.",
        "parameters": [LIMIT, OFFSET, PAGE, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "A page of shipping methods and the `pagination` block. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": {
                    "shipping_methods": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/Pagination"},
                    "field_metadata": {"$ref": "#/components/schemas/FieldMetadata"},
                }},
                "example": {"shipping_methods": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a parameter the listing does not accept: the message is `unknown query parameter(s): <name>` and `details[0].code` is `unknown_parameter`. Or you sent `limit=0`: the message is `'limit' must be a positive integer`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_shipping_methods",
        "slug": "check-the-shipping-methods-list",
        "title": "Check the shipping methods list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the shipping methods list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. Neither this response nor the listing has an `ETag` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_shipping_methods",
        "slug": "count-shipping-methods",
        "title": "Count shipping methods",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of shipping methods in the store.",
        "description": "Returns the number of shipping methods as `count`, inside a `shipping_methods` object. The number matches `pagination.total` from the listing. Query parameters are accepted and ignored, so nothing narrows the count.",
        "responses": {
            "200": {
                "description": "The number of shipping methods.",
                "schema": {"type": "object", "properties": {"shipping_methods": {"type": "object", "properties": {"count": {"type": "integer"}}}}},
                "example": {"shipping_methods": {"count": 3}},
            },
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_method",
        "slug": "create-a-shipping-method",
        "title": "Create a shipping method",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a shipping method from a `name` and returns it with its `id`, which the other calls take as `shipping_method_id`.",
        "description": "Creates a shipping method and returns it with the `id` the store assigned. Pass that `id` as `shipping_method_id` to retrieve, rename, delete or make the method the default. Wrap the record in `shipping_method`; `name` is the only field the store reads. A new method always has `is_default` set to `false`, and any `id` or `is_default` you send inside `shipping_method` is ignored.",
        "body": {"schema": WRITE_BODY, "example": {"shipping_method": {"name": "Express Post"}}},
        "responses": {
            "201": {
                "description": "The new shipping method.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_method": {"id": 4, "name": "Express Post", "is_default": False}},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NAME_REQUIRED},
            "409": {"description": WRITE_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "get_shipping_method",
        "slug": "retrieve-a-shipping-method",
        "title": "Retrieve a shipping method",
        "method": "GET",
        "path": BASE + "/{shipping_method_id}",
        "summary": "Returns the shipping method whose `id` you pass as `shipping_method_id`.",
        "description": "Returns one shipping method under the `shipping_method` key, with the same three fields a listing row has: `id`, `name` and `is_default`. Send `field_metadata=true` to add a description of each field. Unknown query parameters are ignored.",
        "parameters": [SHIPPING_METHOD_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The shipping method. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": {"type": "object", "properties": {"shipping_method": ROW_REF, "field_metadata": {"$ref": "#/components/schemas/FieldMetadata"}}},
                "example": {"shipping_method": SAMPLE_ROWS[1]},
            },
            "404": {"description": "No method has that `shipping_method_id`, or it is not a number.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"shipping_method_id": 2}},
    },
    {
        "key": "head_shipping_method",
        "slug": "check-a-shipping-method",
        "title": "Check a shipping method",
        "method": "HEAD",
        "path": BASE + "/{shipping_method_id}",
        "summary": "Returns headers only, and `200` even when no method has that `shipping_method_id`.",
        "description": "Returns `200` with headers only and no body. It returns `200` even when no method has that `shipping_method_id`, so it does not tell you whether the method exists. To check that, use [Retrieve a shipping method](" + RETRIEVE_PAGE + "), which returns `404` when no method has it.",
        "parameters": [SHIPPING_METHOD_ID],
        "responses": {
            "200": {"description": "Headers only, no body. Returned even when no method has that `shipping_method_id`."},
        },
        "example_call": {"path": {"shipping_method_id": 2}},
    },
    {
        "key": "update_shipping_method",
        "slug": "rename-a-shipping-method",
        "title": "Rename a shipping method",
        "method": "PUT",
        "path": BASE + "/{shipping_method_id}",
        "summary": "Changes a shipping method's `name` and returns the updated method.",
        "description": "Changes the method's `name` and returns the method. Wrap the change in `shipping_method`; `name` is required and follows the same rules as on create. Any `id` or `is_default` you send inside `shipping_method` is ignored. To change the default, use [Set the default shipping method](" + DEFAULT_PAGE + ").",
        "parameters": [SHIPPING_METHOD_ID],
        "body": {"schema": WRITE_BODY, "example": {"shipping_method": {"name": "Express Post Next Day"}}},
        "responses": {
            "200": {
                "description": "The renamed shipping method.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_method": {"id": 4, "name": "Express Post Next Day", "is_default": False}},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NAME_REQUIRED},
            "409": {"description": WRITE_409, "schema": ERROR_REF, "example": DUPLICATE_RENAME},
        },
        "example_call": {"path": {"shipping_method_id": 4}},
    },
    {
        "key": "delete_shipping_method",
        "slug": "delete-a-shipping-method",
        "title": "Delete a shipping method",
        "method": "DELETE",
        "path": BASE + "/{shipping_method_id}",
        "summary": "Deletes a shipping method permanently. You cannot delete the default method.",
        "description": "Deletes the shipping method permanently and returns `204` with no body. The method leaves the listing and the count goes down by one. You cannot delete the default method: make another method the default first, or the call is rejected with `409`.",
        "parameters": [SHIPPING_METHOD_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No method has that `shipping_method_id`, including a method you already deleted.", "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {
                "description": "The method is the default. The message is `cannot delete the default shipping method; set another as default first` and `details[0].code` is `default_in_use`.",
                "schema": ERROR_REF,
                "example": DEFAULT_IN_USE,
            },
        },
        "example_call": {"path": {"shipping_method_id": 4}},
    },
    {
        "key": "set_shipping_method_default",
        "slug": "set-the-default-shipping-method",
        "title": "Set the default shipping method",
        "method": "PUT",
        "path": BASE + "/{shipping_method_id}/default",
        "summary": "Makes a shipping method the default and removes the flag from the previous one.",
        "description": "Makes this method the default and returns it with `is_default` set to `true`. The method that was the default loses the flag. The call reads no body, so anything you send is ignored. No call clears the flag without giving it to another method.",
        "parameters": [SHIPPING_METHOD_ID],
        "responses": {
            "200": {
                "description": "The shipping method, now the default.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_method": {"id": 2, "name": "Express Shipping", "is_default": True}},
            },
        },
        "example_call": {"path": {"shipping_method_id": 2}},
    },
]

FIELD_DESCRIPTION = {"type": "object", "properties": {
    "type": {"type": "string", "description": "The field's value type: `integer` for `id`, `string` for `name` and `boolean` for `is_default`."},
    "writable": {"type": "boolean", "description": "Whether a write can set this field. `true` only for `name`."},
    "required": {"type": "boolean", "description": "Whether a write must send this field. Only `name` has it, set to `true`."},
    "max_length": {"type": "integer", "description": "The longest value accepted. Only `name` has it, set to `100`."},
    "read_only": {"type": "boolean", "description": "`true` on `id` and `is_default`. Only `PUT /admin/shipping_methods/{shipping_method_id}/default` changes `is_default`."},
    "description": {"type": "string", "description": "What the field holds."},
}}

SCHEMAS = {
    "ShippingMethod": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping method's id, assigned by the store. Pass it as `shipping_method_id` in a path."},
        "name": {"type": "string", "maxLength": 100, "description": "Unique across the store's methods."},
        "is_default": {"type": "boolean", "description": "`true` on the one default method. Only `PUT /admin/shipping_methods/{shipping_method_id}/default` changes it."},
    }},
    "ShippingMethodInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "maxLength": 100, "description": "Required. At most 100 characters, and no other method may have the same name."},
    }},
    "FieldDescription": FIELD_DESCRIPTION,
    "FieldMetadata": {"type": "object", "description": "Describes each field, keyed by field name. Returned only when you send `field_metadata=true`.", "properties": {
        "id": {"$ref": "#/components/schemas/FieldDescription"},
        "name": {"$ref": "#/components/schemas/FieldDescription"},
        "is_default": {"$ref": "#/components/schemas/FieldDescription"},
    }},
    "Pagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of shipping methods in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of rows skipped before this page."},
        "count": {"type": "integer", "description": "The number of rows on this page."},
        "current_page": {"type": "integer", "description": "The page that `offset` falls in, never more than `total_pages`."},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": "string", "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": "string", "description": "The next page, or `null` on the last page. Check `has_next` before you request it."},
    }},
    "Error": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string"},
        "details": {"type": "array", "description": "Extra detail, or an empty list. On some errors the first entry's `code` gives the reason: `duplicate`, `default_in_use` or `unknown_parameter`.", "items": {"type": "object", "properties": {"code": {"type": "string"}}}},
        "request_id": {"type": "string"},
    }}}},
}
