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
    "**Replacing a location resets every field you leave out of the body.** `PUT` on a location does\n"
    "  not merge: `address` becomes `\"\"`, and `is_active` and `is_default` become `false`. If you\n"
    "  replace the default location and leave out `is_default`, the store has no default location\n"
    "  until you give the flag back with [Set the default inventory location](" + DEFAULT_PAGE + ").\n"
    "  Send every field you want to keep, `is_default` included."
)

NOTES = [
    "**Send the fields at the top level of the body, not inside `inventory_location`.** Create and\n"
    "  replace both read `name`, `address`, `is_active` and `is_default` from the top level. A create\n"
    "  wrapped in `{\"inventory_location\": {...}}` is rejected with `400` and the message\n"
    "  `name is required`. Responses return the location inside `inventory_location`.",
    "**At most one location is the default.**\n"
    "  [Set the default inventory location](" + DEFAULT_PAGE + ") gives the flag to the location you name and\n"
    "  takes it from the location that had it. A create with `\"is_default\": true` takes the flag the same\n"
    "  way, and a replace that leaves out `is_default` clears it. You cannot delete the default location:\n"
    "  make another location the default first, or the delete is rejected with `409`.",
    "**A listing returns at most 20 locations per call, whatever `limit` you send.** The store checks\n"
    "  `limit` but does not apply it: `pagination.limit` always shows `20`, and `limit=0` is rejected\n"
    "  with `400`. To get more, send a higher `offset`, or a `page` (read as `offset = (page - 1) * 20`),\n"
    "  while `pagination.has_next` is `true`. The stock listing pages the same way, 20 products at a\n"
    "  time. Unknown query parameters are ignored, not rejected.",
    "**A `200` does not prove a write worked.** For a method these paths do not support, such as\n"
    "  `PATCH` on a location or any write to `/stock`, the store returns `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and stores nothing. Use `PUT` to\n"
    "  replace a location, and [Activate or deactivate an inventory location](" + STATUS_PAGE + ") to change\n"
    "  only `is_active`. No call changes stock.",
]

INVENTORY_LOCATION_ID = {
    "name": "inventory_location_id",
    "in": "path",
    "required": True,
    "description": "The inventory location's `id`, from a listing or from the response to creating the location.",
    "schema": {"type": "integer", "example": 4},
}

Q = {"name": "q", "in": "query", "description": "Keeps only locations whose `name` contains this text, in any letter case. It does not search `address`.", "schema": {"type": "string", "example": "Sydney"}}
LIMIT = {"name": "limit", "in": "query", "description": "The store checks `limit` but does not apply it: every page holds up to 20 locations, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`. A value that is not an integer is rejected with `400` and the message `'limit' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 1, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of locations to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * 20` whatever `limit` you send. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 1}}

STOCK_LIMIT = {"name": "limit", "in": "query", "description": "The store does not apply `limit`: every page holds up to 20 products, and `pagination.limit` shows `20`.", "schema": {"type": "integer", "minimum": 1, "example": 20}}
STOCK_OFFSET = {"name": "offset", "in": "query", "description": "Number of products to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 0}}
STOCK_PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * 20` whatever `limit` you send. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 1}}

ERROR_REF = {"$ref": "#/components/schemas/InventoryLocationError"}
NOT_FOUND = {"status": "error", "code": 404, "message": "Inventory location not found"}
DEFAULT_NOT_DELETABLE = {"status": "error", "code": 409, "message": "the default inventory location can not be deleted"}
NOT_FOUND_RESPONSE = {"description": "No inventory location has that `inventory_location_id`. The message is `Inventory location not found`.", "schema": ERROR_REF, "example": NOT_FOUND}

ROW_REF = {"$ref": "#/components/schemas/InventoryLocation"}
PAGINATION_REF = {"$ref": "#/components/schemas/InventoryLocationPagination"}
ROW_RESPONSE = {"type": "object", "properties": {"inventory_location": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 1, "name": "Sydney Warehouse", "address": "1 Example Street, Sydney NSW 2000", "is_active": True, "is_default": True, "created": "2026-07-16T06:24:24", "updated": "2026-08-19T11:14:38"},
    {"id": 4, "name": "Sydney Store Room", "address": "2 Example Road, Sydney NSW 2000", "is_active": True, "is_default": False, "created": "2026-07-17T05:16:21", "updated": "2026-08-16T14:19:53"},
]

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

CREATED_ROW = {"id": 19, "name": "Perth Warehouse", "address": "4 Example Street, Perth WA 6000", "is_active": False, "is_default": False, "created": "2026-09-24T09:15:02", "updated": "2026-09-24T09:15:02"}
REPLACED_ROW = dict(CREATED_ROW, address="10 Example Street, Perth WA 6000", is_active=True, updated="2026-09-24T09:20:41")
ACTIVATED_ROW = dict(CREATED_ROW, is_active=True, updated="2026-09-24T09:18:30")
DEFAULT_ROW = dict(SAMPLE_ROWS[1], is_default=True, updated="2026-09-24T09:25:10")

SAMPLE_PRODUCTS = [
    {"product_id": 101, "name": "Cotton T-Shirt", "sku": "TSHIRT-001", "is_variation": False, "stock": 25, "low_stock_level": 5, "is_default": False},
    {"product_id": 102, "name": "Canvas Tote Bag", "sku": "TOTE-001", "is_variation": False, "stock": 8, "low_stock_level": None, "is_default": False},
]

ENDPOINTS = [
    {
        "key": "list_inventory_locations",
        "slug": "list-inventory-locations",
        "title": "List inventory locations",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 inventory locations per call, default location first, with paging details.",
        "description": "Returns the inventory locations, up to 20 per call, with a `pagination` block. The default location comes first, then the rest, newest `created` first. Send `q` to keep only locations whose `name` contains that text. `field_metadata` and unknown parameters change nothing and are not rejected. After a rejected `limit=0`, the next request on the same client returns that rejection's body instead of its own.",
        "parameters": [Q, LIMIT, OFFSET, PAGE],
        "responses": {
            "200": {
                "description": "Up to 20 inventory locations in `inventory_locations`, and the paging details in `pagination`. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "inventory_locations": {"type": "array", "items": ROW_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"inventory_locations": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "You sent `limit=0`: the message is `'limit' must be a positive integer`. Or you sent a `limit` that is not an integer: the message is `'limit' must be a non-negative integer`."},
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
        "description": "Send the fields at the top level of the body, not wrapped in `inventory_location`; only `name` is required. A new location has `is_active` and `is_default` set to `false` unless you send `true`, and sending `\"is_default\": true` takes the flag from the location that had it. The store sets the location's `id`, `created` and `updated` itself, and ignores any values you send for them and any unknown field. A `name` another location already has is accepted.",
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationInput"}, "example": {"name": "Perth Warehouse", "address": "4 Example Street, Perth WA 6000"}},
        "responses": {
            "201": {
                "description": "The new inventory location, with the location's `id`, which the other calls take as `inventory_location_id`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": CREATED_ROW},
            },
            "400": {"description": "`name` is missing or blank, or the body is wrapped in `inventory_location`. The message is `name is required`."},
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
        "description": "Returns one location under the `inventory_location` key, with the same seven fields a listing entry has: `id`, `name`, `address`, `is_active`, `is_default`, `created` and `updated`. The response has no `ETag` header. Unknown query parameters are ignored.",
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
        "summary": "Replaces the location's `name`, `address`, `is_active` and `is_default` with your body and returns it.",
        "description": "Send every field you want to keep, at the top level of the body. This call replaces the location rather than merging: a field you leave out is reset, so `address` becomes `\"\"` and `is_active` and `is_default` become `false`. Leaving out `is_default` on the default location leaves the store with no default location. `name` is required, and a body without it returns `500`, not `400`.",
        "parameters": [INVENTORY_LOCATION_ID],
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationInput"}, "example": {"name": "Perth Warehouse", "address": "10 Example Street, Perth WA 6000", "is_active": True, "is_default": False}},
        "responses": {
            "200": {
                "description": "The inventory location after the replace, with the values you sent.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": REPLACED_ROW},
            },
            "500": {"description": "The body has no `name`, for example `{}` or a body with only `address`. The message is `Unexpected Error Occurred`."},
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
            "404": {"description": "No inventory location has that `inventory_location_id`, for example because you already deleted it."},
            "409": {"description": "The location is the default. The message is `the default inventory location can not be deleted`.", "schema": ERROR_REF, "example": DEFAULT_NOT_DELETABLE},
        },
        "example_call": {"path": {"inventory_location_id": 19}},
    },
    {
        "key": "get_inventory_location_stock",
        "slug": "list-stock-at-an-inventory-location",
        "title": "List stock at an inventory location",
        "method": "GET",
        "path": BASE + "/{inventory_location_id}/stock",
        "summary": "Returns an inventory location and up to 20 of the products it holds, with paging details.",
        "description": "Returns the location under `inventory_location`, up to 20 of its products under `products`, and a `pagination` block that counts products. A location that holds no products returns an empty `products` list, with `total` and `total_pages` set to `0`. Send `offset` or `page` to get the next products. This call is read-only: no call on this API changes stock.",
        "parameters": [INVENTORY_LOCATION_ID, STOCK_LIMIT, STOCK_OFFSET, STOCK_PAGE],
        "responses": {
            "200": {
                "description": "The inventory location in `inventory_location`, up to 20 of its products in `products`, and the paging details in `pagination`.",
                "schema": {"type": "object", "properties": {
                    "inventory_location": ROW_REF,
                    "products": {"type": "array", "items": {"$ref": "#/components/schemas/InventoryLocationStockItem"}},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"inventory_location": SAMPLE_ROWS[1], "products": SAMPLE_PRODUCTS, "pagination": SAMPLE_PAGINATION},
            },
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
        "description": "Makes this location the default and returns it with `is_default` and `is_active` both `true`. The location that had the flag loses it, so this call also changes a location you did not name. The call reads no body, so anything you send is ignored.",
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
        "summary": "Sets `is_active` on an inventory location and leaves every other field as it is.",
        "description": "Send `{\"is_active\": true}` to activate the location or `{\"is_active\": false}` to deactivate it. The store reads only `is_active`: `name`, `is_default` and any other field stay as they are, even if you send them. A value that is not a boolean is read as true or false, so `1` and `\"yes\"` both activate. You can deactivate the default location with this call.",
        "parameters": [INVENTORY_LOCATION_ID],
        "body": {"schema": {"$ref": "#/components/schemas/InventoryLocationStatusInput"}, "example": {"is_active": True}},
        "responses": {
            "200": {
                "description": "The inventory location with its new `is_active` value.",
                "schema": ROW_RESPONSE,
                "example": {"inventory_location": ACTIVATED_ROW},
            },
            "400": {"description": "`is_active` is missing. The message is `is_active is required`."},
        },
        "example_call": {"path": {"inventory_location_id": 19}},
    },
]

SCHEMAS = {
    "InventoryLocation": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The inventory location's id, assigned by the store. Pass it as `inventory_location_id` in a path."},
        "name": {"type": "string", "description": "The location's name. Two locations can have the same name."},
        "address": {"type": "string", "description": "The location's address, as free text. `\"\"` when none is set."},
        "is_active": {"type": "boolean", "description": "Whether the location is active. `false` on a new location unless you send `true`."},
        "is_default": {"type": "boolean", "description": "`true` on the default location. At most one location has it."},
        "created": {"type": "string", "description": "When the location was created, such as `2026-07-16T06:24:24`."},
        "updated": {"type": "string", "description": "When the location last changed."},
    }},
    "InventoryLocationInput": {"type": "object", "required": ["name"], "description": "Send these fields at the top level of the body. On a replace, a field you leave out is reset.", "properties": {
        "name": {"type": "string", "description": "Required. On create, a blank `name` is rejected with `400`."},
        "address": {"type": "string", "description": "Free text. Defaults to `\"\"`, and a replace without it sets it to `\"\"`. On create, an object here returns `500`."},
        "is_active": {"type": "boolean", "description": "Defaults to `false`, and a replace without it sets it to `false`."},
        "is_default": {"type": "boolean", "description": "On create, send `true` to make the new location the default; the location that had the flag loses it. Defaults to `false`, and a replace without it sets it to `false`."},
    }},
    "InventoryLocationStatusInput": {"type": "object", "required": ["is_active"], "properties": {
        "is_active": {"type": "boolean", "description": "Required. `true` activates the location and `false` deactivates it. Other values are read as true or false: `1` and `\"yes\"` both activate."},
    }},
    "InventoryLocationStockItem": {"type": "object", "description": "One product held at the location.", "properties": {
        "product_id": {"type": "integer", "description": "The product's id."},
        "name": {"type": "string", "description": "The product's name."},
        "sku": {"type": "string", "description": "The product's SKU."},
        "stock": {"type": "integer", "description": "How many of the product this location holds."},
        "low_stock_level": {"type": ["integer", "null"], "description": "The product's low-stock level, or `null`."},
        "is_default": {"type": "boolean", "description": "A flag on the product itself. It does not say whether this location is the default."},
        "is_variation": {"type": "boolean"},
    }},
    "InventoryLocationPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "On the listing, the number of locations that match your request. On the stock listing, the number of products at the location."},
        "limit": {"type": "integer", "description": "The page size the store applied. Always `20`, whatever `limit` you send."},
        "offset": {"type": "integer", "description": "The number of items skipped before this page."},
        "count": {"type": "integer", "description": "The number of items on this page."},
        "current_page": {"type": "integer", "description": "The number of this page, counting from `1`."},
        "total_pages": {"type": "integer", "description": "The number of pages. `0` when nothing matches."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, such as `https://your-store.example.com/api/v4/admin/inventory_locations?limit=20&offset=0`, or `null` when `has_previous` is `false`. It is set whenever `offset` is more than `0`, even when `current_page` is `1`."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` when `has_next` is `false`. Check `has_next` before you request it."},
    }},
    "InventoryLocationError": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`error`."},
        "code": {"type": "integer", "description": "The HTTP status, such as `404` or `409`."},
        "message": {"type": "string", "description": "What went wrong, such as `Inventory location not found`."},
    }},
}
