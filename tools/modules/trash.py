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
    "**`trash_type` takes a value from [List trash types](" + TYPES_PAGE + ").** `Category`, `category` and\n"
    "  `CATEGORY` all work, in a path and in a bulk item. A two-word type has no snake_case form: send\n"
    "  `BlogPost`, because `blog_post` is rejected with `400` and the message `unknown trash type 'blog_post'`.\n"
    "  Listed items and bulk `errors` entries return the type in PascalCase, whatever case you sent.",
    "**Only an item in the trash can be restored or deleted permanently.** An item that is not in the trash\n"
    "  is rejected with `409` and the message `<Type> with id <id> is not in trash`. After a permanent delete\n"
    "  the item is gone: a restore, a second delete and the item's own resource all return `404`. An item\n"
    "  path accepts only `DELETE` and `OPTIONS`: `GET` on it returns `405`.",
    "**A bulk call returns `201` even when some items fail.** [Restore items in bulk](" + BULK_RESTORE_PAGE + ")\n"
    "  and [Delete items permanently in bulk](" + BULK_DELETE_PAGE + ") return `201` when at least one item\n"
    "  succeeds, and `400` with the same body when every item fails. Check `failed` and `errors` in every\n"
    "  response: each failed item has an `errors` entry with its `type`, its `id` and a `reason`.",
    "**A listing returns 20 items per call unless you send `limit`.** A `limit` above `100` returns `100`\n"
    "  items, and `pagination.limit` shows `100`. Send `limit` once: sending it twice returns `500`. Send\n"
    "  `order` in lower case: `order=DESC` is accepted but sorts in ascending order.",
    "**Many writes in a row can be rejected with `429`.** The error code is `rate_limited` and the\n"
    "  `Retry-After` header gives the seconds to wait before you retry.",
]

TRASH_TYPE = {
    "name": "trash_type",
    "in": "path",
    "required": True,
    "description": "The item's type, as returned by [List trash types](" + TYPES_PAGE + "), such as `Category`, `Customer` or `BlogPost`. Letter case does not matter: `Category`, `category` and `CATEGORY` all work. `blog_post` is rejected with `400`; send `BlogPost`.",
    "schema": {"type": "string", "example": "Category"},
}

TRASH_ITEM_ID = {
    "name": "trash_item_id",
    "in": "path",
    "required": True,
    "description": "The id the item has in its own resource: a category's `id`, or a customer's `customer_id`. The same number is the item's `id` in [List items in the trash](" + LIST_PAGE + ").",
    "schema": {"type": "integer", "example": 1234},
}

TYPE = {"name": "type", "in": "query", "description": "Keeps only items of this type, a value from [List trash types](" + TYPES_PAGE + ") in any letter case, or several types separated by commas, such as `Product,Category`. Send it on every call, and not as `Customer` alone: without it, or with `Customer`, a page can take about 90 to 110 seconds. An unknown type, `blog_post` included, is rejected with `400` and the message `unknown trash type '<value>'`.", "schema": {"type": "string", "example": "Category"}}
SEARCH = {"name": "search", "in": "query", "description": "Keeps only items whose `name` contains this text. `searchText` is accepted as another name for `search`.", "schema": {"type": "string", "example": "spring"}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by: `name`, `type`, `updated` or `removed_at`, which sorts by `updated`. Without it, items come newest `updated` first. Any other value is rejected with `400` and the message `unsupported sort '<value>'`.", "schema": {"type": "string", "enum": ["name", "type", "updated", "removed_at"], "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`, in lower case. `order=DESC` in upper case is accepted but sorts in ascending order. Any other value is rejected with `400` and the message `unsupported dir '<value>'`. `dir` is accepted as another name for `order`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of items per page, `1` or more. Defaults to `20`. A value above `100` returns `100` items, and `pagination.limit` shows the value applied. `0` is rejected with `400` and the reason `out_of_range`; text such as `all` with `400` and the reason `invalid_integer`. Send it once: sending `limit` twice returns `500`. `max` is accepted as another name for `limit`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
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
    {"id": 1234, "type": "Category", "name": "Spring Collection", "updated": "2026-10-18T11:16:07"},
    {"id": 1229, "type": "Category", "name": "Spring Sale", "updated": "2026-10-17T09:42:51"},
]

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

TYPE_NAMES = ["Album", "Article", "BlogPost", "Category", "Customer", "Form", "Navigation", "Operator", "Order", "Page", "Product", "Supplier"]

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
        "description": "Returns the items in the trash in `items`, 20 per call unless you send `limit`, newest `updated` first, and `pagination` with the total and the URLs of the next and previous pages. Send `type` on every call, and not as `Customer` alone: without it, or with `Customer`, a page can take about 90 to 110 seconds. Send `search` to match part of an item's `name`, and `sort` and `order` to change the order. Any query parameter the listing does not accept, such as `q`, is rejected with `400` and the reason `unknown_parameter`.",
        "parameters": LIST_QUERY,
        "responses": {
            "200": {
                "description": "The items on this page in `items`, each with its `id`, `type`, `name` and `updated`, and `pagination` with the total, the page size, the page number and the URLs of the next and previous pages. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "items": {"type": "array", "items": ITEM_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"items": SAMPLE_ITEMS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "A query parameter is not valid: an unknown `type` (message `unknown trash type '<value>'`), an unknown `sort` (message `unsupported sort '<value>'`), an `order` other than `asc` or `desc` (message `unsupported dir '<value>'`), a `limit` of `0` (reason `out_of_range`) or one that is not a number (reason `invalid_integer`), a negative `offset`, a `removed_to` that is not a `yyyy-MM-dd` date, or a parameter the listing does not accept (reason `unknown_parameter`).",
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
        "summary": "Returns every type the trash holds, in alphabetical order, such as `Category` and `Customer`.",
        "description": "Returns the types in `types`, each as an object with a `type` field, in alphabetical order. Each value is a PascalCase name, such as `BlogPost`, that you can send as `trash_type` in a path, as `type` in a bulk item and as `type` on [List items in the trash](" + LIST_PAGE + "). The call takes no query parameters: any one you send is rejected with `400`. The response has no `ETag` header.",
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
        "summary": "Restores one item from the trash and returns a success message, not the item.",
        "description": "Restores the item you name by `trash_type` and `trash_item_id`, and returns `201` with `status` and `message`. The item is live again in its own resource; read it there to get its fields. Send no body: one you send is ignored, and so is any query parameter. An item that is not in the trash is rejected with `409`.",
        "parameters": [TRASH_TYPE, TRASH_ITEM_ID],
        "responses": {
            "201": {
                "description": "The item is restored. The body has `status` set to `success` and a `message` such as `Category restored successfully`.",
                "schema": {"$ref": "#/components/schemas/TrashRestoreResult"},
                "example": {"status": "success", "message": "Category restored successfully"},
            },
            "400": {"description": "`trash_type` is not a trash type, such as `blog_post`. The message is `unknown trash type '<value>'`.", "schema": ERROR_REF},
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
            "400": {"description": "`trash_type` is not a trash type, such as `blog_post`. The message is `unknown trash type '<value>'`.", "schema": ERROR_REF},
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
        "summary": "Restores up to 100 trashed items and returns how many were restored and which failed.",
        "description": "Send `items`, a list of 1 to 100 objects, each with the item's `type` and `id`, at the top level of the body. You get `201` when at least one item is restored, even if others fail, and `400` with the same body when none is, so check `failed` and `errors` in every response. An item that is not in the trash fails with the reason `<Type> with id <id> is not in trash`, and an id the type does not have fails with `<Type> with id <id> not found`. An item listed twice is restored once, and the second copy fails.",
        "body": {"schema": BULK_INPUT_REF, "example": {"items": [{"type": "Category", "id": 1234}, {"type": "BlogPost", "id": 99}]}},
        "responses": {
            "201": {
                "description": "At least one item is restored. `restored` and `failed` count the items, and `errors` has one entry for each item that failed.",
                "schema": RESTORE_RESULT_REF,
                "example": {"restored": 1, "failed": 1, "errors": [{"type": "BlogPost", "id": 99, "reason": "BlogPost with id 99 not found"}]},
            },
            "400": {
                "description": "No item is restored. The body has the same `restored`, `failed` and `errors` fields as a `201`. Or: " + BULK_BODY_400 + " In that case the body is an `error` object.",
                "schema": {"oneOf": [RESTORE_RESULT_REF, ERROR_REF]},
                "example": {"restored": 0, "failed": 1, "errors": [{"type": "Category", "id": 1234, "reason": "Category with id 1234 is not in trash"}]},
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
        "summary": "Deletes up to 100 trashed items permanently and returns counts and the items that failed.",
        "description": "Send the same body as [Restore items in bulk](" + BULK_RESTORE_PAGE + "): `items`, a list of 1 to 100 objects, each with the item's `type` and `id`. You get `201` when at least one item is deleted, even if others fail, and `400` with the same body when none is, so check `failed` and `errors` in every response. An item that is not in the trash fails with the reason `<Type> with id <id> is not in trash`, and an id the type does not have fails with `<Type> with id <id> not found`. An item listed twice is deleted once, and the second copy fails with `not found`.",
        "body": {"schema": BULK_INPUT_REF, "example": {"items": [{"type": "Category", "id": 1234}, {"type": "Category", "id": 1229}]}},
        "responses": {
            "201": {
                "description": "At least one item is deleted permanently. `deleted` and `failed` count the items, and `errors` has one entry for each item that failed.",
                "schema": DELETE_RESULT_REF,
                "example": {"deleted": 2, "failed": 0, "errors": []},
            },
            "400": {
                "description": "No item is deleted. The body has the same `deleted`, `failed` and `errors` fields as a `201`. Or: " + BULK_BODY_400 + " In that case the body is an `error` object.",
                "schema": {"oneOf": [DELETE_RESULT_REF, ERROR_REF]},
                "example": {"deleted": 0, "failed": 1, "errors": [{"type": "Category", "id": 1234, "reason": "Category with id 1234 not found"}]},
            },
        },
        "example_call": {},
    },
]

BULK_ERROR_ITEMS = {"type": "array", "description": "One entry for each item that failed. Empty when every item succeeded.", "items": {"$ref": "#/components/schemas/TrashBulkError"}}

SCHEMAS = {
    "TrashItem": {"type": "object", "description": "One item in the trash.", "properties": {
        "id": {"type": "integer", "description": "The id the item has in its own resource, such as a category's `id` or a customer's `customer_id`. Pass it as `trash_item_id` in a path."},
        "type": {"type": "string", "description": "The item's type in PascalCase, such as `Category`. Pass it as `trash_type` in a path."},
        "name": {"type": "string", "description": "The item's name."},
        "updated": {"type": "string", "description": "When the item was moved to the trash, in UTC with no time zone designator, such as `2026-10-18T11:16:07`."},
    }},
    "TrashPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of items that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, `100` when you sent more, or `20`."},
        "offset": {"type": "integer", "description": "The number of items skipped before this page."},
        "count": {"type": "integer", "description": "The number of items on this page."},
        "current_page": {"type": "integer", "description": "The number of this page, counting from `1`."},
        "total_pages": {"type": "integer", "description": "The number of pages at this page size."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The full URL of the next page, or `null` on the last page."},
    }},
    "TrashType": {"type": "object", "properties": {
        "type": {"type": "string", "description": "A type the trash holds, in PascalCase, such as `BlogPost`. Send it as `trash_type` in a path or as `type` in a bulk item."},
    }},
    "TrashRestoreResult": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "message": {"type": "string", "description": "`<Type> restored successfully`, such as `Category restored successfully`."},
    }},
    "TrashBulkItemInput": {"type": "object", "required": ["type", "id"], "description": "One item to restore or delete. Any other field is rejected with `400`.", "properties": {
        "type": {"type": "string", "description": "The item's type, a value from [List trash types](" + TYPES_PAGE + ") in any letter case, such as `Category`."},
        "id": {"type": "integer", "description": "The id the item has in its own resource, such as a category's `id` or a customer's `customer_id`."},
    }},
    "TrashBulkInput": {"type": "object", "required": ["items"], "description": "Send `items` at the top level of the body. Another top-level field is ignored.", "properties": {
        "items": {"type": "array", "minItems": 1, "maxItems": 100, "description": "1 to 100 items. An empty or missing list, or more than 100 items, is rejected with `400`.", "items": {"$ref": "#/components/schemas/TrashBulkItemInput"}},
    }},
    "TrashBulkError": {"type": "object", "description": "One item a bulk call could not restore or delete.", "properties": {
        "type": {"type": "string", "description": "The item's type, in PascalCase."},
        "id": {"type": "integer", "description": "The id the item has in its own resource, as you sent it in the bulk item's `id`."},
        "reason": {"type": "string", "description": "Why the item failed, such as `Category with id 1234 is not in trash` or `Category with id 1234 not found`."},
    }},
    "TrashBulkRestoreResult": {"type": "object", "properties": {
        "restored": {"type": "integer", "description": "The number of items restored."},
        "failed": {"type": "integer", "description": "The number of items not restored."},
        "errors": BULK_ERROR_ITEMS,
    }},
    "TrashBulkDeleteResult": {"type": "object", "properties": {
        "deleted": {"type": "integer", "description": "The number of items deleted permanently."},
        "failed": {"type": "integer", "description": "The number of items not deleted."},
        "errors": BULK_ERROR_ITEMS,
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
