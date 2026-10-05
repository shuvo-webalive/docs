"""The Inventory locations endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Inventory locations"
SLUG = "inventory-locations"
BASE = "/admin/inventory_locations"
ICON = "warehouse"

OVERVIEW_DESCRIPTION = "List, create, replace and delete inventory locations, activate or deactivate them, see the products each one holds, and choose the default location."
INTRO = "The Inventory locations API has ten endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/inventory_locations`."

RETRIEVE_PAGE = "/api-reference/inventory-locations/retrieve-an-inventory-location"
DEFAULT_PAGE = "/api-reference/inventory-locations/set-the-default-inventory-location"
STATUS_PAGE = "/api-reference/inventory-locations/activate-or-deactivate-an-inventory-location"

WARNING = (
    "**Replacing a location resets `address` and `active` when you leave them out of the body.** `PUT`\n"
    "  on a location does not merge: `address` becomes `null` and `active` becomes `true`. A `default`\n"
    "  you leave out keeps its value. Send every field you want to keep."
)

NOTES = [
    "**Send the fields at the top level of the body, not inside `inventory_location`.** Create and\n"
    "  replace both accept only `name`, `address`, `active` and `default`, at the top level. Any other\n"
    "  field, including a wrapping `inventory_location`, is rejected with `400`. Responses return the\n"
    "  location inside `inventory_location`.",
    "**`is_active` and `is_default` are still accepted in request bodies.** The store reads them as\n"
    "  `active` and `default` and returns only the new names. If you send both spellings of a field with\n"
    "  different values, the request is rejected with `400` and the reason `conflicting_field`.",
    "**At most one location is the default.**\n"
    "  [Set the default inventory location](" + DEFAULT_PAGE + ") gives the flag to the location you name and\n"
    "  takes it from the location that had it. A create or replace with `\"default\": true` takes the flag\n"
    "  the same way. You cannot take the flag away with `\"default\": false` or delete the default\n"
    "  location: make another location the default first, or the request is rejected with `409`.",
    "**A listing returns 20 locations per call unless you send `limit`.** `limit` takes `1` to `100`,\n"
    "  and `pagination.limit` shows the page size applied. To get more, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. The listing accepts only `q`, `limit` and `offset`, and the stock\n"
    "  listing only `limit` and `offset`: any other query parameter, `page` included, is rejected with\n"
    "  `400`.",
    "**A `200` does not prove a write worked.** For a method these paths do not support, such as\n"
    "  `PATCH` on a location or any write to `/stock`, the store returns `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and stores nothing. Use `PUT` to\n"
    "  replace a location, and [Activate or deactivate an inventory location](" + STATUS_PAGE + ") to change\n"
    "  only `active`. No call changes stock.",
]

INVENTORY_LOCATION_ID = {
    "name": "inventory_location_id",
    "in": "path",
    "required": True,
    "description": "The inventory location's `id`, from a listing or from the response to creating the location.",
    "schema": {"type": "integer", "example": 4},
}

Q = {"name": "q", "in": "query", "description": "Keeps only locations whose `name` contains this text, in any letter case. It does not search `address`.", "schema": {"type": "string", "example": "Sydney"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of locations per page, from `1` to `100`. Defaults to `20`. `pagination.limit` shows the value applied. `0` and values above `100` are rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of locations to skip.", "schema": {"type": "integer", "example": 0}}

STOCK_LIMIT = {"name": "limit", "in": "query", "description": "The number of products per page. Defaults to `20`. `pagination.limit` shows the value applied.", "schema": {"type": "integer", "minimum": 1, "example": 20}}
STOCK_OFFSET = {"name": "offset", "in": "query", "description": "Number of products to skip.", "schema": {"type": "integer", "example": 0}}

ERROR_REF = {"$ref": "#/components/schemas/InventoryLocationError"}
NOT_FOUND_RESPONSE = {"description": "No inventory location has that `inventory_location_id`.", "schema": ERROR_REF}

ROW_REF = {"$ref": "#/components/schemas/InventoryLocation"}
PAGINATION_REF = {"$ref": "#/components/schemas/InventoryLocationPagination"}
ROW_RESPONSE = {"type": "object", "properties": {"inventory_location": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 1, "name": "Sydney Warehouse", "address": "1 Example Street, Sydney NSW 2000", "active": True, "default": True, "created_at": "2026-07-16T06:24:24", "updated_at": "2026-08-19T11:14:38"},
    {"id": 4, "name": "Sydney Store Room", "address": "2 Example Road, Sydney NSW 2000", "active": True, "default": False, "created_at": "2026-07-17T05:16:21", "updated_at": "2026-08-16T14:19:53"},
]

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATED_ROW = {"id": 19, "name": "Perth Warehouse", "address": "4 Example Street, Perth WA 6000", "active": True, "default": False, "created_at": "2026-09-24T09:15:02", "updated_at": "2026-09-24T09:15:02"}
REPLACED_ROW = dict(CREATED_ROW, address="10 Example Street, Perth WA 6000", updated_at="2026-09-24T09:20:41")
DEACTIVATED_ROW = dict(CREATED_ROW, active=False, updated_at="2026-09-24T09:18:30")
DEFAULT_ROW = dict(SAMPLE_ROWS[1], default=True, updated_at="2026-09-24T09:25:10")

SAMPLE_ITEMS = [
    {"product": {"id": 101, "name": "Cotton T-Shirt", "sku": "TSHIRT-001"}, "variation": None, "available_stock": 25, "low_stock_level": 5, "default_for_product": False},
    {"product": {"id": 102, "name": "Canvas Tote Bag", "sku": "TOTE-001"}, "variation": None, "available_stock": 8, "low_stock_level": None, "default_for_product": False},
]

ENDPOINTS = [
    {
        "key": "list_inventory_locations",
        "slug": "list-inventory-locations",
        "title": "List inventory locations",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 inventory locations per call, or the `limit` you send, default location first, with paging details.",
        "description": "Returns the inventory locations, 20 per call unless you send `limit`, with a `pagination` block. The default location comes first, then the rest, newest `created_at` first. Send `q` to keep only locations whose `name` contains that text. Only `q`, `limit` and `offset` are accepted; any other query parameter, such as `page` or `field_metadata`, is rejected with `400`. After a `400`, the next one or two requests on the same connection can return that rejection's body instead of their own.",
        "parameters": [Q, LIMIT, OFFSET],
        "responses": {
            "200": {
                "description": "The inventory locations on this page in `inventory_locations`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "inventory_locations": {"type": "array", "items": ROW_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"inventory_locations": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a query parameter the listing does not accept: the message is `unsupported query parameter '<name>'; supported: q, limit, offset`. Or you sent a `limit` of `0` or more than `100`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "q=Sydney"},
    },
    {
        "key": "head_inventory_locations",
        "slug": "check-the-inventory-locations-list",
        "title": "Check the inventory locations list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the inventory locations list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_inventory_location",
        "slug": "create-an-inventory-location",
        "title": "Create an inventory location",
        "method": "POST",
        "path": BASE,
        "summary": "Creates an inventory location and returns it with its `id`, which other calls take as `inventory_location_id`.",
        "description": "Send the fields at the top level of the body, not wrapped in `inventory_location`; only `name` is required. A new location has `active` set to `true` and `default` set to `false` unless you send otherwise, and sending `\"default\": true` takes the flag from the location that had it. The store sets the location's `id`, `created_at` and `updated_at` itself: sending any of them is rejected with `400` and the reason `read_only_field`. Any field other than `name`, `address`, `active` and `default` is rejected with `400` and the reason `unknown_field`. `is_active` and `is_default` are accepted as other names for `active` and `default`. A `name` another location already has is accepted.",
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationInput"}, "example": {"name": "Perth Warehouse", "address": "4 Example Street, Perth WA 6000"}},
        "responses": {
            "201": {
                "description": "The new inventory location, with the location's `id`, which the other calls take as `inventory_location_id`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": CREATED_ROW},
            },
            "400": {"description": "`name` is missing or blank; the body has a field the store does not accept (reason `unknown_field`, message `accepted fields are: name, address, active, default`) or one it sets itself (reason `read_only_field`); `active` or `default` is not a boolean (reason `invalid_boolean`); or `active` and `is_active`, or `default` and `is_default`, have different values (reason `conflicting_field`).", "schema": ERROR_REF},
            "500": {"description": "`address` is an object instead of a string."},
        },
        "example_call": {},
    },
    {
        "key": "get_inventory_location",
        "slug": "retrieve-an-inventory-location",
        "title": "Retrieve an inventory location",
        "method": "GET",
        "path": BASE + "/{inventory_location_id}",
        "summary": "Returns the inventory location whose `id` you pass as `inventory_location_id`.",
        "description": "Returns one location under the `inventory_location` key, with the same seven fields a listing entry has: `id`, `name`, `address`, `active`, `default`, `created_at` and `updated_at`. The response has no `ETag` header.",
        "parameters": [INVENTORY_LOCATION_ID],
        "responses": {
            "200": {
                "description": "The inventory location.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": SAMPLE_ROWS[1]},
            },
            "404": NOT_FOUND_RESPONSE,
        },
        "example_call": {"path": {"inventory_location_id": 4}},
    },
    {
        "key": "head_inventory_location",
        "slug": "check-an-inventory-location",
        "title": "Check an inventory location",
        "method": "HEAD",
        "path": BASE + "/{inventory_location_id}",
        "summary": "Returns headers only, with no body, for the location you pass as `inventory_location_id`.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. It returns `200` even when no location has that `inventory_location_id`, so it does not tell you whether the location exists. To read the location's fields, or to get `404` for a location that does not exist, use [Retrieve an inventory location](" + RETRIEVE_PAGE + ").",
        "parameters": [INVENTORY_LOCATION_ID],
        "responses": {
            "200": {"description": "Headers only, no body. You get `200` for any `inventory_location_id`, including one no location has."},
        },
        "example_call": {"path": {"inventory_location_id": 4}},
    },
    {
        "key": "update_inventory_location",
        "slug": "replace-an-inventory-location",
        "title": "Replace an inventory location",
        "method": "PUT",
        "path": BASE + "/{inventory_location_id}",
        "summary": "Replaces the location's `name`, `address` and `active` with your body, sets `default` if you send it, and returns the location.",
        "description": "Send every field you want to keep, at the top level of the body. This call replaces the location rather than merging: `address` you leave out becomes `null`, and `active` you leave out becomes `true`. `default` you leave out keeps its value; `\"default\": true` makes this location the default, and `\"default\": false` on the default location is rejected with `409`. `name` is required. The call accepts the same fields as [Create an inventory location](/api-reference/inventory-locations/create-an-inventory-location), including `is_active` and `is_default`, and rejects the same fields.",
        "parameters": [INVENTORY_LOCATION_ID],
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationInput"}, "example": {"name": "Perth Warehouse", "address": "10 Example Street, Perth WA 6000", "active": True}},
        "responses": {
            "200": {
                "description": "The inventory location after the replace, with the values you sent.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": REPLACED_ROW},
            },
            "409": {"description": "You sent `\"default\": false` for the default location. The message is `the default inventory location can not be un-set; make another location the default instead`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"inventory_location_id": 19}},
    },
    {
        "key": "delete_inventory_location",
        "slug": "delete-an-inventory-location",
        "title": "Delete an inventory location",
        "method": "DELETE",
        "path": BASE + "/{inventory_location_id}",
        "summary": "Deletes an inventory location permanently. You cannot delete the default location.",
        "description": "Deletes the location permanently and returns `204` with no body. The location leaves the listing, and retrieving or deleting it again returns `404`. You cannot delete the default location: make another location the default first, or the call is rejected with `409`.",
        "parameters": [INVENTORY_LOCATION_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No inventory location has that `inventory_location_id`, for example because you already deleted it.", "schema": ERROR_REF},
            "409": {"description": "The location is the default. The message is `the default inventory location can not be deleted; make another location the default first`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"inventory_location_id": 19}},
    },
    {
        "key": "get_inventory_location_stock",
        "slug": "list-stock-at-an-inventory-location",
        "title": "List stock at an inventory location",
        "method": "GET",
        "path": BASE + "/{inventory_location_id}/stock",
        "summary": "Returns an inventory location and up to 20 of the products it holds, or the `limit` you send, with paging details.",
        "description": "Returns the location under `inventory_location`, its products under `items`, 20 per call unless you send `limit`, and a `pagination` block that counts products. Each item names the product in `product` and gives its `available_stock` at this location. A location that holds no products returns an empty `items` list, with `total` set to `0`. Send `offset` to get the next products. Only `limit` and `offset` are accepted; `q`, `page` and any other query parameter are rejected with `400`. This call is read-only: no call on this API changes stock.",
        "parameters": [INVENTORY_LOCATION_ID, STOCK_LIMIT, STOCK_OFFSET],
        "responses": {
            "200": {
                "description": "The inventory location in `inventory_location`, its products in `items`, and the paging details in `pagination`.",
                "schema": {"type": "object", "properties": {
                    "inventory_location": ROW_REF,
                    "items": {"type": "array", "items": {"$ref": "#/components/schemas/InventoryLocationStockItem"}},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"inventory_location": SAMPLE_ROWS[1], "items": SAMPLE_ITEMS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "You sent a query parameter other than `limit` and `offset`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"inventory_location_id": 4}},
    },
    {
        "key": "set_inventory_location_default",
        "slug": "set-the-default-inventory-location",
        "title": "Set the default inventory location",
        "method": "PUT",
        "path": BASE + "/{inventory_location_id}/default",
        "summary": "Makes an inventory location the default and removes the flag from the previous one.",
        "description": "Makes this location the default and returns it with `default` and `active` both `true`. The location that had the flag loses it, so this call also changes a location you did not name. Send no body.",
        "parameters": [INVENTORY_LOCATION_ID],
        "responses": {
            "200": {
                "description": "The inventory location, now the default and active.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": DEFAULT_ROW},
            },
            "404": NOT_FOUND_RESPONSE,
        },
        "example_call": {"path": {"inventory_location_id": 4}},
    },
    {
        "key": "update_inventory_location_status",
        "slug": "activate-or-deactivate-an-inventory-location",
        "title": "Activate or deactivate an inventory location",
        "method": "PUT",
        "path": BASE + "/{inventory_location_id}/status",
        "summary": "Sets `active` on an inventory location and leaves every other field as it is.",
        "description": "Send `{\"active\": true}` to activate the location or `{\"active\": false}` to deactivate it. `active` is the only field the body accepts; `is_active` is accepted as another name for it. Any other field, `name` included, is rejected with `400`. You can deactivate the default location with this call: it stays the default.",
        "parameters": [INVENTORY_LOCATION_ID],
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationStatusInput"}, "example": {"active": False}},
        "responses": {
            "200": {
                "description": "The inventory location with its new `active` value.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": DEACTIVATED_ROW},
            },
            "400": {"description": "`active` is missing: the message is `active: is required`. Or the body has another field: the message is `accepted fields are: active`. Or it sends both `active` and `is_active` (reason `conflicting_field`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"inventory_location_id": 19}},
    },
]

SCHEMAS = {
    "InventoryLocation": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The inventory location's id, assigned by the store. Pass it as `inventory_location_id` in a path."},
        "name": {"type": "string", "description": "The location's name. Two locations can have the same name."},
        "address": {"type": ["string", "null"], "description": "The location's address, as free text, or `null` when none is set."},
        "active": {"type": "boolean", "description": "Whether the location is active. `true` on a new location unless you send `false`."},
        "default": {"type": "boolean", "description": "`true` on the default location. At most one location has it."},
        "created_at": {"type": "string", "description": "When the location was created, such as `2026-07-16T06:24:24`."},
        "updated_at": {"type": "string", "description": "When the location last changed."},
    }},
    "InventoryLocationInput": {"type": "object", "required": ["name"], "description": "Send these fields at the top level of the body. Any other field is rejected with `400`. `is_active` and `is_default` are accepted as other names for `active` and `default`.", "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 250, "description": "Required, 1 to 250 characters."},
        "address": {"type": ["string", "null"], "description": "Free text. A replace without it sets it to `null`. On create, an object here returns `500`."},
        "active": {"type": "boolean", "description": "Defaults to `true`, and a replace without it sets it to `true`."},
        "default": {"type": "boolean", "description": "Send `true` to make this location the default; the location that had the flag loses it. Defaults to `false` on create. A replace without it keeps the current value, and `false` on the default location is rejected with `409`."},
    }},
    "InventoryLocationStatusInput": {"type": "object", "required": ["active"], "description": "`active` is the only field accepted. `is_active` is accepted as another name for it.", "properties": {
        "active": {"type": "boolean", "description": "Required. `true` activates the location and `false` deactivates it."},
    }},
    "InventoryLocationStockProduct": {"type": "object", "description": "The product a stock item is for.", "properties": {
        "id": {"type": "integer", "description": "The product's id."},
        "name": {"type": "string", "description": "The product's name."},
        "sku": {"type": "string", "description": "The product's SKU."},
    }},
    "InventoryLocationStockItem": {"type": "object", "description": "One product held at the location.", "properties": {
        "product": {"$ref": "#/components/schemas/InventoryLocationStockProduct"},
        "variation": {"type": ["object", "null"], "description": "The product variation this item is for, or `null` when the item is for the product itself."},
        "available_stock": {"type": "integer", "description": "How many of the product are available at this location."},
        "low_stock_level": {"type": ["integer", "null"], "description": "The product's low-stock level, or `null`."},
        "default_for_product": {"type": "boolean", "description": "Whether this location is the product's default location. It does not say whether this location is the store's default."},
    }},
    "InventoryLocationPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "On the listing, the number of locations that match your request. On the stock listing, the number of products at the location."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of items skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
    }},
    "InventoryLocationError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason for the rejection."},
        "message": {"type": "string", "description": "What went wrong, such as `accepted fields are: name, address, active, default`."},
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected."},
            "message": {"type": ["string", "null"]},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
