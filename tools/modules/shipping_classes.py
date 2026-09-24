"""The Shipping classes endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping classes"
SLUG = "shipping-classes"
BASE = "/admin/shipping_classes"
ICON = "boxes-stacked"

OVERVIEW_DESCRIPTION = "List, count, create, update and delete shipping classes, and choose which one is the default."
INTRO = "The Shipping classes API has nine endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/shipping_classes`."

RETRIEVE_PAGE = "/api-reference/shipping-classes/retrieve-a-shipping-class"
DEFAULT_PAGE = "/api-reference/shipping-classes/set-the-default-shipping-class"

WARNING = (
    "**Updating a shipping class replaces both its `name` and its `description`.** If your `PUT` sends\n"
    "  only `name`, the store sets the class's `description` to `null`. To keep the description, send it\n"
    "  again in the same call: `{\"shipping_class\": {\"name\": \"Bulky Goods\", \"description\": \"Items over 20kg\"}}`."
)

NOTES = [
    "**Create and update wrap the class in `shipping_class`.** Send\n"
    "  `{\"shipping_class\": {\"name\": \"Bulky Goods\", \"description\": \"Items over 20kg\"}}` to create or\n"
    "  update a class. A body that sends the fields without the wrapper, or wraps them in the plural\n"
    "  `shipping_classes` key, is rejected with `400` and the message `shipping_class missing`.",
    "**`name` and `description` are the only fields you can write.** `name` is required, at most 50\n"
    "  characters, and must be unique: a name another class already has is rejected with `409`.\n"
    "  `description` is optional and at most 100 characters. If you leave it out, the store saves\n"
    "  `null`; an empty string is saved as an empty string. The store ignores an `id`, an `is_default`\n"
    "  and any unknown field you send inside `shipping_class`.",
    "**Only one class is the default, and only one call changes it.**\n"
    "  [Set the default shipping class](" + DEFAULT_PAGE + ") sets `is_default` to `true` on the class\n"
    "  whose `shipping_class_id` you pass, and to `false` on the class that was the default. You cannot\n"
    "  delete the default class: make another class the default first, or the delete is rejected with `409`.",
    "**A listing returns at most 20 classes per call, and the classes you create are listed first.** A\n"
    "  larger `limit` is capped at `20`, and `pagination.limit` shows `20`. New classes go ahead of the\n"
    "  classes already there, newest first, so the default class can be past the first page. To get\n"
    "  more, send the next `page` or a higher `offset` while `pagination.has_next` is `true`.",
    "**`PATCH` does not change a class.** A `PATCH` on a class returns `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and changes nothing. Use `PUT` to\n"
    "  update a class.",
]

SHIPPING_CLASS_ID = {
    "name": "shipping_class_id",
    "in": "path",
    "required": True,
    "description": "The shipping class's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 2},
}

LIMIT = {"name": "limit", "in": "query", "description": "Shipping classes per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of shipping classes to skip. When you send both `offset` and `page`, `offset` wins. `-1` is rejected with `400` and the message `'offset' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied. `page=2` alone skips 20 classes; `limit=2&page=2` skips 2.", "schema": {"type": "integer", "example": 1}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key that describes each of the class's four fields, `id`, `name`, `description` and `is_default`: its type, whether you can write it and a short description, and for `name` and `description`, whether it is required and its maximum length.", "schema": {"type": "boolean", "example": True}}

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Shipping class not found")
NAME_REQUIRED = error("invalid_request", "name is required")
DUPLICATE_NAME = error("conflict", "a shipping class named 'Bulky Goods' already exists", [{"code": "duplicate"}])
DEFAULT_IN_USE = error("conflict", "cannot delete the default shipping class; set another as default first", [{"code": "default_in_use"}])
UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): sort", [{"field": "sort", "code": "unknown_parameter", "message": None}])

ERROR_REF = {"$ref": "#/components/schemas/ShippingClassError"}
ROW_REF = {"$ref": "#/components/schemas/ShippingClass"}
FIELD_METADATA_REF = {"$ref": "#/components/schemas/ShippingClassFieldMetadata"}
WRITE_BODY = {"type": "object", "required": ["shipping_class"], "properties": {"shipping_class": {"$ref": "#/components/schemas/ShippingClassInput"}}}
ROW_RESPONSE = {"type": "object", "properties": {"shipping_class": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 3, "name": "Bulky Goods", "description": "Items over 20kg", "is_default": False},
    {"id": 1, "name": "Standard", "description": "Standard", "is_default": True},
    {"id": 2, "name": "Express", "description": "Express", "is_default": False},
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

WRITE_400 = "The body is not wrapped in `shipping_class` (`shipping_class missing`), `name` is missing (`name is required`), `name` is longer than 50 characters (`name must be 50 characters or fewer`), or `description` is longer than 100 characters (`description must be 100 characters or fewer`). The `code` is `invalid_request`."
WRITE_409 = "Another shipping class already has that `name`. The `code` is `conflict`, the message is `a shipping class named '<name>' already exists` and `details[0].code` is `duplicate`."

ENDPOINTS = [
    {
        "key": "list_shipping_classes",
        "slug": "list-shipping-classes",
        "title": "List shipping classes",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 shipping classes per call, with classes you create listed first.",
        "description": "Returns up to 20 shipping classes under `shipping_classes`, and a `pagination` object with the total and whether another page follows. The classes you create are listed ahead of the classes already there, newest first, and the default class is not moved to the top. Only `limit`, `offset`, `page` and `field_metadata` are accepted; any other parameter, such as `sort` or `q`, is rejected with `400`. After a rejected `limit` or `offset`, such as `limit=0`, your next listing call on the same client is rejected the same way, even with `limit=20`. A call that takes no `limit`, such as [Retrieve a shipping class](" + RETRIEVE_PAGE + "), runs normally.",
        "parameters": [LIMIT, OFFSET, PAGE, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The shipping classes on this page under `shipping_classes`, and `pagination` with the total, the page size and whether another page follows. With `field_metadata=true`, the response also has a `field_metadata` key.",
                "schema": {"type": "object", "properties": {
                    "shipping_classes": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/ShippingClassPagination"},
                    "field_metadata": FIELD_METADATA_REF,
                }},
                "example": {"shipping_classes": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a parameter the listing does not accept: the `code` is `invalid_request`, the message is `unknown query parameter(s): <name>`, `details[0].code` is `unknown_parameter` and `details[0].field` names the parameter. Or you sent `limit=0`: the message is `'limit' must be a positive integer` and `details[0].code` is `out_of_range`. Or you sent `offset=-1`: the message is `'offset' must be a non-negative integer` and `details[0].code` is `invalid_integer`. A rejected `sort` still changes the next listing on the same client: after `sort=name` it comes back in descending `name` order, and after `sort=-id`, a sort on the class's `id`, it returns `500`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_shipping_classes",
        "slug": "check-the-shipping-classes-list",
        "title": "Check the shipping classes list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the shipping classes list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. Neither this response nor the listing has an `ETag` or a `Last-Modified` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_shipping_classes",
        "slug": "count-shipping-classes",
        "title": "Count shipping classes",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of shipping classes in the store.",
        "description": "Returns the number of shipping classes as `count`, inside a `shipping_classes` object. The number matches `pagination.total` from the listing. Query parameters are accepted and ignored, so nothing narrows the count, and `field_metadata=true` adds no `field_metadata` key.",
        "responses": {
            "200": {
                "description": "The number of shipping classes.",
                "schema": {"type": "object", "properties": {"shipping_classes": {"type": "object", "properties": {"count": {"type": "integer"}}}}},
                "example": {"shipping_classes": {"count": 3}},
            },
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_class",
        "slug": "create-a-shipping-class",
        "title": "Create a shipping class",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a shipping class and returns it with its `id`, which other calls take as `shipping_class_id`.",
        "description": "Creates a shipping class and returns it with the `id` the store assigned. Pass that `id` as `shipping_class_id` to retrieve, update, delete or make the class the default. Wrap the fields in `shipping_class`; the store reads only `name` and `description`, and saves `null` for a `description` you leave out. A new class has `is_default` set to `false`, and any `id` or `is_default` you send inside `shipping_class` is ignored.",
        "body": {"schema": WRITE_BODY, "example": {"shipping_class": {"name": "Bulky Goods", "description": "Items over 20kg"}}},
        "responses": {
            "201": {
                "description": "The new shipping class under `shipping_class`: its `id`, the `name` and `description` you sent, and `is_default` set to `false`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_class": {"id": 3, "name": "Bulky Goods", "description": "Items over 20kg", "is_default": False}},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NAME_REQUIRED},
            "409": {"description": WRITE_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "get_shipping_class",
        "slug": "retrieve-a-shipping-class",
        "title": "Retrieve a shipping class",
        "method": "GET",
        "path": BASE + "/{shipping_class_id}",
        "summary": "Returns the shipping class whose `id` you pass as `shipping_class_id`.",
        "description": "Returns one shipping class under the `shipping_class` key, with the same four fields a listing row has: `id`, `name`, `description` and `is_default`. Send `field_metadata=true` to add a description of each field beside the class. Unknown query parameters are ignored. The response has no `ETag` header. If the request just before this one on the same client was rejected with `404` for a `shipping_class_id` that no shipping class has, the store handles this call with that rejected `shipping_class_id`: it returns `404` even for a class that exists. Send the call again.",
        "parameters": [SHIPPING_CLASS_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The shipping class under `shipping_class`. With `field_metadata=true`, the response also has a `field_metadata` key beside it.",
                "schema": {"type": "object", "properties": {"shipping_class": ROW_REF, "field_metadata": FIELD_METADATA_REF}},
                "example": {"shipping_class": SAMPLE_ROWS[2]},
            },
            "404": {"description": "No shipping class has the `shipping_class_id` you passed, or it is not a number. The `code` is `not_found` and the message is `Shipping class not found`. You also get this `404` for a class that exists when the request just before it on the same client was rejected with `404` for a `shipping_class_id` that no shipping class has.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"shipping_class_id": 2}},
    },
    {
        "key": "head_shipping_class",
        "slug": "check-a-shipping-class",
        "title": "Check a shipping class",
        "method": "HEAD",
        "path": BASE + "/{shipping_class_id}",
        "summary": "Returns `200` and headers only, even when no class has the `shipping_class_id` you pass.",
        "description": "Returns `200` with headers only: no body and no `ETag`. It returns `200` even when no shipping class has the `shipping_class_id` you pass, so it does not tell you whether the class exists. To check that, use [Retrieve a shipping class](" + RETRIEVE_PAGE + "), which returns `404` when no class has that `shipping_class_id`.",
        "parameters": [SHIPPING_CLASS_ID],
        "responses": {
            "200": {"description": "Headers only, no body. Returned even when no shipping class has the `shipping_class_id` you passed."},
        },
        "example_call": {"path": {"shipping_class_id": 2}},
    },
    {
        "key": "update_shipping_class",
        "slug": "update-a-shipping-class",
        "title": "Update a shipping class",
        "method": "PUT",
        "path": BASE + "/{shipping_class_id}",
        "summary": "Replaces a shipping class's `name` and `description` and returns the updated class.",
        "description": "Replaces the `name` and `description` of the class whose `shipping_class_id` you pass, and returns the class. Wrap the change in `shipping_class`; `name` is required and follows the same rules as on create. A `description` you leave out is saved as `null`, so send it again to keep it. Any `id` or `is_default` you send inside `shipping_class` is ignored: to change the default, use [Set the default shipping class](" + DEFAULT_PAGE + ").",
        "parameters": [SHIPPING_CLASS_ID],
        "body": {"schema": WRITE_BODY, "example": {"shipping_class": {"name": "Bulky Goods", "description": "Items over 25kg"}}},
        "responses": {
            "200": {
                "description": "The updated shipping class under `shipping_class`, with the `name` and `description` you sent.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_class": {"id": 3, "name": "Bulky Goods", "description": "Items over 25kg", "is_default": False}},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NAME_REQUIRED},
            "409": {"description": WRITE_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_class_id": 3}},
    },
    {
        "key": "delete_shipping_class",
        "slug": "delete-a-shipping-class",
        "title": "Delete a shipping class",
        "method": "DELETE",
        "path": BASE + "/{shipping_class_id}",
        "summary": "Deletes a shipping class permanently. You cannot delete the default class.",
        "description": "Deletes the shipping class whose `shipping_class_id` you pass, permanently, and returns `204` with no body. The class leaves the listing and the count goes down by one. You cannot delete the default class: make another class the default first, or the call is rejected with `409`.",
        "parameters": [SHIPPING_CLASS_ID],
        "responses": {
            "204": {"description": "The class is deleted. No body."},
            "404": {"description": "No shipping class has the `shipping_class_id` you passed, including a class you already deleted.", "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {
                "description": "The class is the default. The `code` is `conflict`, the message is `cannot delete the default shipping class; set another as default first` and `details[0].code` is `default_in_use`.",
                "schema": ERROR_REF,
                "example": DEFAULT_IN_USE,
            },
        },
        "example_call": {"path": {"shipping_class_id": 3}},
    },
    {
        "key": "set_shipping_class_default",
        "slug": "set-the-default-shipping-class",
        "title": "Set the default shipping class",
        "method": "PUT",
        "path": BASE + "/{shipping_class_id}/default",
        "summary": "Makes a shipping class the default and sets `is_default` to `false` on the previous default.",
        "description": "Makes the class whose `shipping_class_id` you pass the default, and returns it with `is_default` set to `true`. The class that was the default now has `is_default` set to `false`. The call reads no body, so anything you send is ignored. Calling it on the class that is already the default also returns `200`.",
        "parameters": [SHIPPING_CLASS_ID],
        "responses": {
            "200": {
                "description": "The shipping class, now the default.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_class": {"id": 2, "name": "Express", "description": "Express", "is_default": True}},
            },
        },
        "example_call": {"path": {"shipping_class_id": 2}},
    },
]

FIELD_DESCRIPTION = {"type": "object", "properties": {
    "type": {"type": "string", "description": "The field's value type: `integer`, `string` or `boolean`."},
    "writable": {"type": "boolean", "description": "Whether a create or update can set this field: `true` for `name` and `description`, `false` for `id` and `is_default`."},
    "read_only": {"type": "boolean", "description": "Only on `id` and `is_default`, where it is `true`. Only `PUT /admin/shipping_classes/{shipping_class_id}/default` changes `is_default`."},
    "required": {"type": "boolean", "description": "Only on `name` and `description`. Whether a create or update must send this field: `true` for `name`, `false` for `description`."},
    "max_length": {"type": "integer", "description": "Only on `name` and `description`. The longest value accepted: `50` for `name`, `100` for `description`."},
    "description": {"type": "string", "description": "A short description of the field."},
}}

SCHEMAS = {
    "ShippingClass": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping class's `id`, assigned by the store. Pass it as `shipping_class_id` in a path."},
        "name": {"type": "string", "maxLength": 50, "description": "Unique across the store's shipping classes. At most 50 characters."},
        "description": {"type": ["string", "null"], "maxLength": 100, "description": "At most 100 characters. `null` when the last create or update left it out."},
        "is_default": {"type": "boolean", "description": "`true` on the one default class. Only `PUT /admin/shipping_classes/{shipping_class_id}/default` changes it."},
    }},
    "ShippingClassInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "maxLength": 50, "description": "Required. At most 50 characters, and no other class may have the same name."},
        "description": {"type": "string", "maxLength": 100, "description": "Optional. At most 100 characters. If you leave it out, the store saves `null`, on an update too. An empty string is saved as an empty string."},
    }},
    "ShippingClassFieldDescription": FIELD_DESCRIPTION,
    "ShippingClassFieldMetadata": {"type": "object", "description": "Describes each of the shipping class's four fields, `id`, `name`, `description` and `is_default`, keyed by field name. Returned only when you send `field_metadata=true`.", "properties": {
        "id": {"$ref": "#/components/schemas/ShippingClassFieldDescription"},
        "name": {"$ref": "#/components/schemas/ShippingClassFieldDescription"},
        "description": {"$ref": "#/components/schemas/ShippingClassFieldDescription"},
        "is_default": {"$ref": "#/components/schemas/ShippingClassFieldDescription"},
    }},
    "ShippingClassPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of shipping classes in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of shipping classes skipped before this page."},
        "count": {"type": "integer", "description": "The number of shipping classes on this page."},
        "current_page": {"type": "integer", "description": "The page that `offset` falls in: `limit=1&offset=1` gives `2`. A `page` past the last class gives `1`."},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` on the last page. Check `has_next` before you request it."},
    }},
    "ShippingClassError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string"},
        "details": {"type": "array", "description": "Extra detail, or an empty list. On some errors the first entry's `code` gives the reason: `duplicate`, `default_in_use`, `unknown_parameter`, `out_of_range` or `invalid_integer`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter that was rejected, such as `sort`, `limit` or `offset`."},
            "code": {"type": "string"},
            "message": {"type": ["string", "null"]},
            "value": {"type": ["integer", "string"], "description": "The value you sent. On the `out_of_range` error for `limit=0` it is the number `0`. On the `invalid_integer` error for `offset=-1` it is the string `\"-1\"`."},
        }}},
        "request_id": {"type": "string"},
    }}}},
}
