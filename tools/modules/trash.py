"""The Trash endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Trash"
SLUG = "trash"
BASE = "/admin/trash"
ICON = "trash-can"

OVERVIEW_DESCRIPTION = "List the items in your store's trash and the types it holds, and restore items or delete them permanently, one at a time or up to 100 per call."
INTRO = "The Trash API has eight endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/trash`."

LIST_PAGE = "/api-reference/trash/list-items-in-the-trash"
TYPES_PAGE = "/api-reference/trash/list-trash-types"
RESTORE_PAGE = "/api-reference/trash/restore-an-item-from-the-trash"
DELETE_PAGE = "/api-reference/trash/delete-an-item-permanently"
BULK_RESTORE_PAGE = "/api-reference/trash/restore-items-in-bulk"
BULK_DELETE_PAGE = "/api-reference/trash/delete-items-permanently-in-bulk"
DELETE_CATEGORY_PAGE = "/api-reference/categories/delete-a-category"
DELETE_CUSTOMER_PAGE = "/api-reference/customers/delete-a-customer"
DELETE_BLOG_POST_PAGE = "/api-reference/blogs/delete-a-blog-post"

WARNING = (
    "**Send a `type` other than `Customer` on every listing call.** Without `type`, or with\n"
    "  `type=Customer`, [List items in the trash](" + LIST_PAGE + ") can take about 90 to 110 seconds to\n"
    "  return a page, and [Check the trash list](/api-reference/trash/check-the-trash-list) takes as long,\n"
    "  because it runs the same query. With `type=Category`, `type=Product` or `type=BlogPost`, a page\n"
    "  returns in about a second. If you must list customers, set your client's request timeout above 110\n"
    "  seconds."
)

NOTES = [
    "**You name an item by its type and the id it has in its own resource.** The trash has no ids of its\n"
    "  own. A category, customer, blog post or page that you delete through its own resource, such as\n"
    "  [Delete a category](" + DELETE_CATEGORY_PAGE + "), [Delete a customer](" + DELETE_CUSTOMER_PAGE + ") or\n"
    "  [Delete a blog post](" + DELETE_BLOG_POST_PAGE + "), stays in the trash until you restore it or delete it\n"
    "  permanently. A category is named by its `id` and a customer by its `customer_id`.",
    "**`trash_type` takes a value from [List trash types](" + TYPES_PAGE + ").** The values are in snake_case,\n"
    "  such as `category` and `blog_post`. The PascalCase names (`Category`, `BlogPost`) and other letter\n"
    "  cases are accepted too, in a path and in a bulk item, and so is `blogpost`. Listed items return\n"
    "  the type in snake_case, whatever case you sent.",
    "**Only an item in the trash can be restored or deleted permanently.** An item that is not in the trash\n"
    "  is rejected with `409` and the message `<Type> with id <id> is not in trash`. After a permanent delete\n"
    "  the item is gone: a restore, a second delete and the item's own resource all return `404`. An item\n"
    "  path accepts only `DELETE` and `OPTIONS`: `GET` on it returns `405`.",
    "**A bulk call returns `207` when any item fails.** [Restore items in bulk](" + BULK_RESTORE_PAGE + ")\n"
    "  and [Delete items permanently in bulk](" + BULK_DELETE_PAGE + ") return `200` when every item\n"
    "  succeeds, and `207` with the same body when any item fails, even when none succeeds. Check `failed`\n"
    "  in every response: each failed item has an entry with its `type`, its `id`, a `code` and a `message`.",
    "**A listing returns 20 items per call unless you send `limit`.** A `limit` above `100` is rejected\n"
    "  with `400` and the reason `out_of_range`. Send `limit` once: sending it twice returns `500`. Send\n"
    "  `order` in lower case: `order=DESC` is accepted but sorts in ascending order.",
    "**Many writes in a row can be rejected with `429`.** The error code is `rate_limited` and the\n"
    "  `Retry-After` header gives the seconds to wait before you retry.",
]

TRASH_TYPE = {
    "name": "trash_type",
    "in": "path",
    "required": True,
    "description": "The item's type, as returned by [List trash types](" + TYPES_PAGE + "), such as `category`, `customer` or `blog_post`. Letter case does not matter, and the PascalCase names such as `BlogPost` work too.",
    "schema": {"type": "string", "example": "Category"},
}

TRASH_ITEM_ID = {
    "name": "trash_item_id",
    "in": "path",
    "required": True,
    "description": "The id the item has in its own resource: a category's `id`, or a customer's `customer_id`. The same number is the item's `id` in [List items in the trash](" + LIST_PAGE + ").",
    "schema": {"type": "integer", "example": 1234},
}

TYPE = {"name": "type", "in": "query", "description": "Keeps only items of this type, a value from [List trash types](" + TYPES_PAGE + ") in any letter case, or several types separated by commas, such as `Product,Category`. Send it on every call, and not as `Customer` alone: without it, or with `Customer`, a page can take about 90 to 110 seconds. An unknown type is rejected with `400` and the message `unknown trash type '<value>'`.", "schema": {"type": "string", "example": "Category"}}
SEARCH = {"name": "search", "in": "query", "description": "Keeps only items whose `name` contains this text. `searchText` is accepted as another name for `search`.", "schema": {"type": "string", "example": "spring"}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by: `name`, `type`, `updated` or `removed_at`, which sorts by `updated`. Without it, items come newest `updated` first. Any other value is rejected with `400` and the message `unsupported sort '<value>'`.", "schema": {"type": "string", "enum": ["name", "type", "updated", "removed_at"], "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`, in lower case. `order=DESC` in upper case is accepted but sorts in ascending order. Any other value is rejected with `400` and the message `unsupported dir '<value>'`. `dir` is accepted as another name for `order`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of items per page, `1` or more. Defaults to `20`. A value above `100` is rejected with `400` and the reason `out_of_range`, and so is `0`; text such as `all` is rejected with `400` and the reason `invalid_integer`. Send it once: sending `limit` twice returns `500`. `max` is accepted as another name for `limit`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of items to skip, `0` or more. A negative value is rejected with `400`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "The page to return, counting from `1`. The store skips `(page - 1) * limit` items.", "schema": {"type": "integer", "minimum": 1, "example": 2}}
REMOVED_FROM = {"name": "removed_from", "in": "query", "description": "The start date of the range in which the items were trashed, as `yyyy-MM-dd`.", "schema": {"type": "string", "format": "date", "example": "2026-10-01"}}
REMOVED_TO = {"name": "removed_to", "in": "query", "description": "The end date of the range in which the items were trashed, as `yyyy-MM-dd`. A date in another format is rejected with `400`, and the error names the field `deletedTo`.", "schema": {"type": "string", "format": "date", "example": "2026-10-18"}}

LIST_QUERY = [TYPE, SEARCH, SORT, ORDER, LIMIT, OFFSET, PAGE, REMOVED_FROM, REMOVED_TO]

REQUEST_ID = "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"

ERROR_REF = {"$ref": "#/components/schemas/TrashError"}
ITEM_REF = {"$ref": "#/components/schemas/TrashItem"}
PAGINATION_REF = {"$ref": "#/components/schemas/TrashPagination"}
RESTORE_RESULT_REF = {"$ref": "#/components/schemas/TrashBulkRestoreResult"}
DELETE_RESULT_REF = {"$ref": "#/components/schemas/TrashBulkDeleteResult"}
BULK_INPUT_REF = {"$ref": "#/components/schemas/TrashBulkInput"}

SAMPLE_ITEMS = [
    {"type": "category", "id": 1234, "name": "Spring Collection", "removed_at": "2026-10-18T11:16:07", "url": "/api/v4/admin/categories/1234"},
    {"type": "category", "id": 1229, "name": "Spring Sale", "removed_at": "2026-10-17T09:42:51", "url": "/api/v4/admin/categories/1229"},
]

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

TYPE_NAMES = ["album", "article", "blog_post", "category", "customer", "form", "navigation", "operator", "order", "page", "product", "supplier"]

RESTORED_ROW = {"type": "category", "id": 1234, "name": "Spring Collection", "url": "/api/v4/admin/categories/1234"}
FAILED_ROW = {"type": "category", "id": 99, "code": "not_found", "message": "Category with id 99 not found"}

NOT_IN_TRASH = {"error": {"code": "conflict", "message": "Category with id 1234 is not in trash", "details": [], "request_id": REQUEST_ID}}

BULK_BODY_400 = (
    "The body is not valid, and nothing is restored or deleted: `items` is missing, empty or not an array"
    " (message `items array is required in request body`); an item is not an object"
    " (message `items[0] must be an object with type and id`); an item has a field other than `type` and `id`"
    " (message `items[0] has unknown field(s): <name>`, reason `unknown_parameter`); there are more than 100 items"
    " (message `a maximum of 100 items is allowed per call`, reason `out_of_range`); or an item's `type` is not a trash type"
    " (message `unknown trash type '<value>'`)."
)

ENDPOINTS = [
    {
        "key": "list_trash",
        "slug": "list-items-in-the-trash",
        "title": "List items in the trash",
        "method": "GET",
        "path": BASE,
        "summary": "Returns the items in the trash, newest first, 20 per call unless you send `limit`.",
        "description": "Returns the items in the trash in `items`, 20 per call unless you send `limit`, newest `updated` first, and `pagination` with the total, the page size, the offset and whether a previous or next page exists. Send `type` on every call, and not as `Customer` alone: without it, or with `Customer`, a page can take about 90 to 110 seconds. Send `search` to match part of an item's `name`, and `sort` and `order` to change the order. Any query parameter the listing does not accept, such as `q`, is rejected with `400` and the reason `unknown_parameter`.",
        "parameters": LIST_QUERY,
        "responses": {
            "200": {
                "description": "The items on this page in `items`, each with its `type`, `id`, `name`, `removed_at` and `url`, and `pagination` with five keys: `total`, `limit`, `offset`, `has_previous` and `has_next`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "items": {"type": "array", "items": ITEM_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"items": SAMPLE_ITEMS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "A query parameter is not valid: an unknown `type` (message `unknown trash type '<value>'`), an unknown `sort` (message `unsupported sort '<value>'`), an `order` other than `asc` or `desc` (message `unsupported dir '<value>'`), a `limit` of `0` or above `100` (reason `out_of_range`) or one that is not a number (reason `invalid_integer`), a negative `offset`, a `removed_to` that is not a `yyyy-MM-dd` date, or a parameter the listing does not accept (reason `unknown_parameter`).",
                "schema": ERROR_REF,
            },
            "500": {"description": "You sent `limit` more than once, such as `limit=2&limit=3`. Send it once."},
        },
        "example_call": {"query": {"type": "Category", "search": "spring", "sort": "name", "order": "asc", "limit": 20}},
    },
    {
        "key": "head_trash",
        "slug": "check-the-trash-list",
        "title": "Check the trash list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers of the trash list, with no body. Takes the listing's query parameters.",
        "description": "Returns `200` with headers only and no body. It takes the same query parameters as [List items in the trash](" + LIST_PAGE + ") and runs the same query, so send a `type` here too: without it, or with `Customer`, the call can take about 90 to 110 seconds. A query parameter the listing does not accept is rejected with `400` here as well.",
        "parameters": LIST_QUERY,
        "responses": {
            "200": {"description": "Headers only, no body."},
            "400": {"description": "A query parameter is not valid, as on [List items in the trash](" + LIST_PAGE + "). No body."},
        },
        "example_call": {"query": {"type": "Category", "limit": 1}},
    },
    {
        "key": "list_trash_types",
        "slug": "list-trash-types",
        "title": "List trash types",
        "method": "GET",
        "path": BASE + "/types",
        "summary": "Returns every type the trash holds, in alphabetical order, such as `category` and `customer`.",
        "description": "Returns the types in `types`, each as an object with a `type` field, in alphabetical order. Each value is a snake_case name, such as `blog_post`, that you can send as `trash_type` in a path, as `type` in a bulk item and as `type` on [List items in the trash](" + LIST_PAGE + "). The call takes no query parameters: any one you send is rejected with `400`. The response has no `ETag` header.",
        "responses": {
            "200": {
                "description": "The twelve types in `types`.",
                "schema": {"type": "object", "properties": {"types": {"type": "array", "items": {"$ref": "#/components/schemas/TrashType"}}}},
                "example": {"types": [{"type": name} for name in TYPE_NAMES]},
            },
            "400": {"description": "You sent a query parameter. The message is `unknown query parameter(s): <name>`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "head_trash_types",
        "slug": "check-the-trash-types-list",
        "title": "Check the trash types list",
        "method": "HEAD",
        "path": BASE + "/types",
        "summary": "Returns the headers of the trash types list, with no body.",
        "description": "Returns `200` with headers only and no body. To read the types, use [List trash types](" + TYPES_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "restore_trash_item",
        "slug": "restore-an-item-from-the-trash",
        "title": "Restore an item from the trash",
        "method": "POST",
        "path": BASE + "/{trash_type}/{trash_item_id}/restore",
        "summary": "Restores one item from the trash and returns the restored item.",
        "description": "Restores the item you name by `trash_type` and `trash_item_id`, and returns `200` with the restored item under `item`, with its `type`, `id`, `name` and `url`. The item is live again in its own resource. Send no body: one you send is ignored, and so is any query parameter. An item that is not in the trash is rejected with `409`.",
        "parameters": [TRASH_TYPE, TRASH_ITEM_ID],
        "responses": {
            "200": {
                "description": "The item is restored. The body has the restored item under `item`.",
                "schema": {"$ref": "#/components/schemas/TrashRestoreResult"},
                "example": {"item": RESTORED_ROW},
            },
            "400": {"description": "`trash_type` is not a trash type. The message is `unknown trash type '<value>'`.", "schema": ERROR_REF},
            "404": {"description": "No item of that type has that `trash_item_id`, for example because you deleted it permanently. The code is `not_found` and the message is `<Type> with id <id> not found`.", "schema": ERROR_REF},
            "409": {"description": "The item is not in the trash. The code is `conflict`, the message is `<Type> with id <id> is not in trash`, and `details` is empty.", "schema": ERROR_REF, "example": NOT_IN_TRASH},
        },
        "example_call": {"path": {"trash_type": "Category", "trash_item_id": 1234}},
    },
    {
        "key": "delete_trash_item",
        "slug": "delete-an-item-permanently",
        "title": "Delete an item permanently",
        "method": "DELETE",
        "path": BASE + "/{trash_type}/{trash_item_id}",
        "summary": "Deletes one item in the trash permanently. You cannot restore it afterwards.",
        "description": "Deletes the item you name by `trash_type` and `trash_item_id` permanently, and returns `204` with no body. Afterwards the item's own resource returns `404` for it, and a restore or a second delete returns `404`. An item that is not in the trash is rejected with `409`: delete it through its own resource first.",
        "parameters": [TRASH_TYPE, TRASH_ITEM_ID],
        "responses": {
            "204": {"description": "Deleted permanently. No body."},
            "400": {"description": "`trash_type` is not a trash type. The message is `unknown trash type '<value>'`.", "schema": ERROR_REF},
            "404": {"description": "No item of that type has that `trash_item_id`, for example because you already deleted it permanently. The code is `not_found`.", "schema": ERROR_REF},
            "409": {"description": "The item is not in the trash. The code is `conflict` and the message is `<Type> with id <id> is not in trash`.", "schema": ERROR_REF, "example": NOT_IN_TRASH},
        },
        "example_call": {"path": {"trash_type": "Customer", "trash_item_id": 5678}},
    },
    {
        "key": "bulk_restore_trash",
        "slug": "restore-items-in-bulk",
        "title": "Restore items in bulk",
        "method": "POST",
        "path": BASE + "/bulk-restore",
        "summary": "Restores up to 100 trashed items and returns the restored items and the items that failed.",
        "description": "Send `items`, a list of 1 to 100 objects, each with the item's `type` and `id`, at the top level of the body. You get `200` when every item is restored, and `207` with the same body when any item fails, even if none is restored, so check `failed` in every response. `restored` lists each restored item as [Restore an item from the trash](" + RESTORE_PAGE + ") returns it, and `failed` lists each failed item with its `type`, `id`, `code` and `message`. The `code` is `not_in_trash` for an item that is not in the trash and `not_found` for an id the type does not have. An item listed twice is restored once and reported once.",
        "body": {"schema": BULK_INPUT_REF, "example": {"items": [{"type": "Category", "id": 1234}, {"type": "BlogPost", "id": 99}]}},
        "responses": {
            "200": {
                "description": "Every item is restored. `restored` lists the items and `failed` is empty.",
                "schema": RESTORE_RESULT_REF,
                "example": {"restored": [RESTORED_ROW], "failed": []},
            },
            "207": {
                "description": "At least one item failed. The body has the same `restored` and `failed` fields as a `200`; `restored` is empty when none succeeded.",
                "schema": RESTORE_RESULT_REF,
                "example": {"restored": [RESTORED_ROW], "failed": [FAILED_ROW]},
            },
            "400": {
                "description": BULK_BODY_400 + " The body is an `error` object.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
    {
        "key": "bulk_delete_trash",
        "slug": "delete-items-permanently-in-bulk",
        "title": "Delete items permanently in bulk",
        "method": "POST",
        "path": BASE + "/bulk-delete",
        "summary": "Deletes up to 100 trashed items permanently and returns the deleted items and the items that failed.",
        "description": "Send the same body as [Restore items in bulk](" + BULK_RESTORE_PAGE + "): `items`, a list of 1 to 100 objects, each with the item's `type` and `id`. You get `200` when every item is deleted, and `207` with the same body when any item fails, even if none is deleted, so check `failed` in every response. `deleted` lists each deleted item with its `type`, `id` and `name`, and `failed` lists each failed item with its `type`, `id`, `code` and `message`. The `code` is `not_in_trash` for an item that is not in the trash and `not_found` for an id the type does not have. An item listed twice is deleted once and reported once.",
        "body": {"schema": BULK_INPUT_REF, "example": {"items": [{"type": "Category", "id": 1234}, {"type": "Category", "id": 1229}]}},
        "responses": {
            "200": {
                "description": "Every item is deleted permanently. `deleted` lists the items and `failed` is empty.",
                "schema": DELETE_RESULT_REF,
                "example": {"deleted": [{"type": "category", "id": 1234, "name": "Spring Collection"}, {"type": "category", "id": 1229, "name": "Spring Sale"}], "failed": []},
            },
            "207": {
                "description": "At least one item failed. The body has the same `deleted` and `failed` fields as a `200`; `deleted` is empty when none succeeded.",
                "schema": DELETE_RESULT_REF,
                "example": {"deleted": [{"type": "category", "id": 1229, "name": "Spring Sale"}], "failed": [FAILED_ROW]},
            },
            "400": {
                "description": BULK_BODY_400 + " The body is an `error` object.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
]

BULK_ERROR_ITEMS = {"type": "array", "description": "One entry for each item that failed. Empty when every item succeeded.", "items": {"$ref": "#/components/schemas/TrashBulkError"}}
BULK_RESTORED_ITEMS = {"type": "array", "description": "The items restored, each as a restore returns it, with `type`, `id`, `name` and `url`.", "items": {"$ref": "#/components/schemas/TrashItem"}}
BULK_DELETED_ITEMS = {"type": "array", "description": "The items deleted permanently, each with its `type`, `id` and `name`.", "items": {"$ref": "#/components/schemas/TrashItem"}}

SCHEMAS = {
    "TrashItem": {"type": "object", "description": "One item in the trash, and the item a restore returns.", "properties": {
        "id": {"type": "integer", "description": "The id the item has in its own resource, such as a category's `id` or a customer's `customer_id`. Pass it as `trash_item_id` in a path."},
        "type": {"type": "string", "description": "The item's type in snake_case, such as `category`. Pass it as `trash_type` in a path."},
        "name": {"type": "string", "description": "The item's name."},
        "removed_at": {"type": "string", "description": "When the item was moved to the trash, in UTC with no time zone designator, such as `2026-10-18T11:16:07`. Not returned by a restore or a bulk delete."},
        "url": {"type": ["string", "null"], "description": "The path you call to retrieve the item in its own resource, such as `/api/v4/admin/categories/1234`. `null` for a `blog_post`."},
    }},
    "TrashPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of items that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of items skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one. There is no next-page link: call again with the next `offset`."},
    }},
    "TrashType": {"type": "object", "properties": {
        "type": {"type": "string", "description": "A type the trash holds, in snake_case, such as `blog_post`. Send it as `trash_type` in a path or as `type` in a bulk item."},
    }},
    "TrashRestoreResult": {"type": "object", "properties": {
        "item": {"$ref": "#/components/schemas/TrashItem"},
    }},
    "TrashBulkItemInput": {"type": "object", "required": ["type", "id"], "description": "One item to restore or delete. Any other field is rejected with `400`.", "properties": {
        "type": {"type": "string", "description": "The item's type, a value from [List trash types](" + TYPES_PAGE + ") in any letter case, such as `Category`."},
        "id": {"type": "integer", "description": "The id the item has in its own resource, such as a category's `id` or a customer's `customer_id`."},
    }},
    "TrashBulkInput": {"type": "object", "required": ["items"], "description": "Send `items` at the top level of the body. Another top-level field is ignored.", "properties": {
        "items": {"type": "array", "minItems": 1, "maxItems": 100, "description": "1 to 100 items. An empty or missing list, or more than 100 items, is rejected with `400`.", "items": {"$ref": "#/components/schemas/TrashBulkItemInput"}},
    }},
    "TrashBulkError": {"type": "object", "description": "One item a bulk call could not restore or delete.", "properties": {
        "type": {"type": "string", "description": "The item's type."},
        "id": {"type": "integer", "description": "The id the item has in its own resource, as you sent it in the bulk item's `id`."},
        "code": {"type": "string", "description": "Why the item failed: `not_found` when the type has no item with that `id`, or `not_in_trash` when the item is not in the trash."},
        "message": {"type": "string", "description": "The reason in words, such as `Category with id 99 not found`."},
    }},
    "TrashBulkRestoreResult": {"type": "object", "properties": {
        "restored": BULK_RESTORED_ITEMS,
        "failed": BULK_ERROR_ITEMS,
    }},
    "TrashBulkDeleteResult": {"type": "object", "properties": {
        "deleted": BULK_DELETED_ITEMS,
        "failed": BULK_ERROR_ITEMS,
    }},
    "TrashError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found`, `conflict` or `rate_limited`."},
        "message": {"type": "string", "description": "What went wrong, such as `Category with id 1234 is not in trash`."},
        "details": {"type": "array", "description": "One entry per rejected field or query parameter, or an empty list. On a `400`, each entry's `message` is `null`: read `error.message` instead.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_parameter` or `out_of_range`."},
            "message": {"type": ["string", "null"], "description": "`null` on a `400`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
