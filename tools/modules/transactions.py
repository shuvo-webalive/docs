"""The Transactions endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Transactions"
SLUG = "transactions"
BASE = "/admin/transactions"
ICON = "receipt"

OVERVIEW_DESCRIPTION = "List the transaction numbers stamped on your store's records, count one number's records by type, and list its records of one type."
INTRO = "The Transactions API has six endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/transactions`."

LIST_PAGE = "/api-reference/transactions/list-transactions"
RETRIEVE_PAGE = "/api-reference/transactions/retrieve-a-transaction"
ITEMS_PAGE = "/api-reference/transactions/list-the-records-of-a-transaction"
DELETE_CATEGORY_PAGE = "/api-reference/categories/delete-a-category"

WARNING = (
    "**Do not follow `url` or `items_url` for a number that contains a space or a `/`.** The store\n"
    "  writes a space in these links as `+` and then reads a `+` in a path as a literal `+`, so the link\n"
    "  returns `404`. Pass `transaction_no` to the SDK function instead: the SDKs percent-encode it, so a\n"
    "  space reaches the store intact. A number that contains `/` cannot be read at all: the request is\n"
    "  rejected with `400` and an HTML page, `Invalid URI: [The encoded slash character is not allowed]`,\n"
    "  before it reaches the API. Do not use `/` in the transaction numbers you send."
)

NOTES = [
    "**You can only read transaction numbers.** A create call that sends a `transaction_no` stamps that\n"
    "  number on the record it creates, and this API reads the numbers back. Every path accepts `GET`,\n"
    "  `HEAD` and `OPTIONS`, and `OPTIONS` returns `204` with `Allow: GET, HEAD, OPTIONS`. `POST`, `PUT`,\n"
    "  `PATCH` and `DELETE` are rejected with `405 method_not_allowed` and the message\n"
    "  `HTTP method not allowed for this endpoint.`",
    "**A record you delete stays counted.** After you delete a category stamped with a number, using\n"
    "  [Delete a category](" + DELETE_CATEGORY_PAGE + "), the number's `total_records`, its `category`\n"
    "  count and the category's row under `items` do not change. The number also stays in the listing.",
    "**`transaction_no` matches exactly, letter case included.** The number in lower case returns\n"
    "  `404` when it was stored in upper case. The store trims surrounding spaces off a number when it\n"
    "  stores one, so send the number without them.",
    "**The two listings handle a large `limit` differently.** [List transactions](" + LIST_PAGE + ")\n"
    "  holds a `limit` above `200` to `200` and shows `200` in `pagination.limit`.\n"
    "  [List the records of a transaction](" + ITEMS_PAGE + ") rejects it with `400` and the message\n"
    "  `max cannot exceed 200`. Both default to `20` and accept `max` as another name for `limit`.",
    "**`pagination` has ten keys.** `total`, `limit`, `offset`, `count`, `current_page`, `total_pages`,\n"
    "  `has_next`, `has_previous`, `previous_page` and `next_page`; the last two are absolute URLs or\n"
    "  `null`. Past the last row, both listings return no rows, `has_previous` set to `false` and\n"
    "  `current_page` equal to `total_pages`. No response here has an `ETag` header, and every one has\n"
    "  `Cache-Control: no-cache, no-store`.",
    "**Errors have one shape.** The body is an `error` object with `code`, `message`, `details` and\n"
    "  `request_id`. A rejected query parameter adds one `details` entry with its `field`, `code`,\n"
    "  `message` and the `value` you sent; `message` can be `null`. On\n"
    "  [List transactions](" + LIST_PAGE + "), a rejected `limit` returns two entries, one for `limit`\n"
    "  and one for `max`. `details` is empty on a `405` and on an unknown path below `/transactions`,\n"
    "  which returns `404` with the message `No such endpoint: GET <path>`.",
]

TYPES = [
    "product", "product_variation", "product_review", "customer", "order", "category", "currency",
    "country_tax", "country_tax_state_rule", "custom_tax_profile", "custom_tax_rule",
    "custom_tax_rule_zone", "shipping_profile", "shipping_rule", "shipping_rate",
]
TYPE_LIST = ", ".join("`%s`" % name for name in TYPES)

TRANSACTION_NO = {
    "name": "transaction_no",
    "in": "path",
    "required": True,
    "description": "The transaction number, exactly as it was sent on the create call that stamped it, in the same letter case, such as `IMPORT-2026-0001`. A listing row returns it in `transaction_no`. The SDKs percent-encode it for you, so `#`, `%`, spaces and non-ASCII letters reach the store intact. A number that contains `/` cannot be read.",
    "schema": {"type": "string", "example": "IMPORT-2026-0001"},
}


def limit_parameter(rows, rules, schema):
    return {
        "name": "limit",
        "in": "query",
        "description": "The number of " + rows + " per page. Defaults to `20`. `max` is accepted as another name for `limit`. " + rules,
        "schema": schema,
    }


def offset_parameter(rows):
    return {
        "name": "offset",
        "in": "query",
        "description": "The number of " + rows + " to skip. A negative value is rejected with `400`.",
        "schema": {"type": "integer", "minimum": 0, "example": 0},
    }


def page_parameter(rows):
    return {
        "name": "page",
        "in": "query",
        "description": "The page of " + rows + " to return, counting from `1`. It sets `offset` to `(page - 1) * limit`. Text such as `abc` is rejected with `400`.",
        "schema": {"type": "integer", "minimum": 1, "example": 2},
    }


LIST_QUERY = [
    limit_parameter("transaction numbers", "Values from `1` up are accepted; a value above `200` is held to `200`, and `pagination.limit` shows `200`. `0` and text such as `abc` or `all` are rejected with `400`.", {"type": "integer", "minimum": 1, "example": 20}),
    offset_parameter("transaction numbers"),
    page_parameter("transaction numbers"),
    {"name": "transaction_no", "in": "query", "description": "Returns only the row for this exact number, matched in the same letter case. The response then has no `pagination` block. An empty value applies no filter.", "schema": {"type": "string", "example": "IMPORT-2026-0001"}},
]

ITEMS_QUERY = [
    {"name": "type", "in": "query", "required": True, "description": "Required. The kind of record to list, one of the 15 `type` names in lower case: " + TYPE_LIST + ". A missing `type` is rejected with `400`. A name in upper case, an unknown name or a comma-separated list is rejected with `400` too.", "schema": {"type": "string", "enum": TYPES, "example": "product"}},
    limit_parameter("records", "Takes `1` to `200`. A value above `200` is rejected with `400` and the message `max cannot exceed 200`.", {"type": "integer", "minimum": 1, "maximum": 200, "example": 20}),
    offset_parameter("records"),
    page_parameter("records"),
    {"name": "detail", "in": "query", "description": "`slim`, the default, returns a short form of each record: its `id` and a few fields that depend on `type`, such as `name`, `sku` and `url` for a product. `full` returns each record as its own retrieve call returns it, without the wrapping key. Any other value, `FULL` included, is rejected with `400` and the message `detail must be 'slim' or 'full'`.", "schema": {"type": "string", "enum": ["slim", "full"], "example": "slim"}},
]

ITEMS_HEAD_QUERY = [
    {"name": "type", "in": "query", "required": True, "description": "Required, as on [List the records of a transaction](" + ITEMS_PAGE + "): one of the 15 `type` names in lower case. Without it the call returns `400`.", "schema": {"type": "string", "enum": TYPES, "example": "product"}},
]

ERROR_REF = {"$ref": "#/components/schemas/TransactionError"}
PAGINATION_REF = {"$ref": "#/components/schemas/TransactionPagination"}

NOT_FOUND = "No record is stamped with that `transaction_no`. A number in a different letter case returns this too. The `error.code` is `not_found`, the message is `transaction not found`, and `details[0].field` is `transaction_no`."


def number_url(number):
    return "/api/v4/admin/transactions/" + number


SAMPLE_ROWS = [
    {"transaction_no": "IMPORT-2026-0001", "total_records": 4, "url": number_url("IMPORT-2026-0001")},
    {"transaction_no": "IMPORT-2026-0002", "total_records": 1, "url": number_url("IMPORT-2026-0002")},
]

LIST_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1, "has_next": False, "has_previous": False, "previous_page": None, "next_page": None}

COUNTS = {"product": 3, "category": 1}


def type_row(name):
    row = {"type": name, "count": COUNTS.get(name, 0)}
    if row["count"]:
        row["items_url"] = number_url("IMPORT-2026-0001") + "/items?type=" + name
    return row


SAMPLE_TRANSACTION = {"transaction_no": "IMPORT-2026-0001", "total_records": 4, "by_type": [type_row(name) for name in TYPES]}

SAMPLE_ITEMS = [
    {"id": 207, "name": "Linen Apron", "sku": "APRON-LIN-01", "url": "/api/v4/admin/products/207"},
    {"id": 206, "name": "Canvas Tote Bag", "sku": "TOTE-CNV-01", "url": "/api/v4/admin/products/206"},
    {"id": 205, "name": "Cotton T-Shirt", "sku": "TEE-COT-01", "url": "/api/v4/admin/products/205"},
]

NOT_FOUND_EXAMPLE = {"error": {"code": "not_found", "message": "transaction not found", "details": [
    {"field": "transaction_no", "code": "not_found", "message": None, "value": "import-2026-0001"},
], "request_id": "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"}}

TYPE_REQUIRED_EXAMPLE = {"error": {"code": "invalid_request", "message": "type query parameter is required", "details": [
    {"field": "type", "code": "required", "message": "type query parameter is required"},
], "request_id": "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"}}

LIMIT_REJECTED_EXAMPLE = {"error": {"code": "invalid_request", "message": "limit is invalid; max is invalid", "details": [
    {"field": "limit", "code": "out_of_range", "message": None, "value": 0},
    {"field": "max", "code": "out_of_range", "message": None, "value": 0},
], "request_id": "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"}}

ITEMS_PAGINATION = {"total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1, "has_next": False, "has_previous": False, "previous_page": None, "next_page": None}

ENDPOINTS = [
    {
        "key": "list_transactions",
        "slug": "list-transactions",
        "title": "List transactions",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 transaction numbers per call, with each number's record count.",
        "description": "Returns the transaction numbers stamped on your store's records, in ascending order of `transaction_no`, 20 per call unless you send `limit`. Each row gives the number, how many records it is stamped on in `total_records`, and its `url`. Send `transaction_no` to get only that number's row; the response then has no `pagination` block. `search`, `q`, `sort`, `order` and parameters the listing does not know are ignored.",
        "parameters": LIST_QUERY,
        "responses": {
            "200": {
                "description": "The numbers on this page in `transactions`, and `pagination` with ten keys. With a `transaction_no` filter, `transactions` alone. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "transactions": {"type": "array", "items": {"$ref": "#/components/schemas/TransactionListEntry"}},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"transactions": SAMPLE_ROWS, "pagination": LIST_PAGINATION},
            },
            "400": {"description": "`limit` or `max` is `0` or not a number, `offset` is negative, or `page` is not a number. The `error.code` is `invalid_request`, and each rejected parameter has a `details` entry naming it in `field`. A rejected `limit` returns two entries, one for `limit` and one for `max`, and the message `limit is invalid; max is invalid`.", "schema": ERROR_REF, "example": LIMIT_REJECTED_EXAMPLE},
        },
        "example_call": {"query": {"limit": 50, "offset": 0}},
    },
    {
        "key": "head_transactions",
        "slug": "check-the-transactions-list",
        "title": "Check the transactions list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the transactions list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "get_transaction",
        "slug": "retrieve-a-transaction",
        "title": "Retrieve a transaction",
        "method": "GET",
        "path": BASE + "/{transaction_no}",
        "summary": "Returns how many records the number in `transaction_no` is stamped on, for each record type.",
        "description": "Returns the number, its `total_records` and `by_type`, at the top level of the body with no wrapping key. `by_type` always has the same 15 rows in the same order, one per record type, each with `type` and `count`. A row has `items_url` only when `count` is above `0`. To list the records of one type, use [List the records of a transaction](" + ITEMS_PAGE + ").",
        "parameters": [TRANSACTION_NO],
        "responses": {
            "200": {
                "description": "The number, its record count and its 15 `by_type` rows. The response has no `ETag` header.",
                "schema": {"$ref": "#/components/schemas/Transaction"},
                "example": SAMPLE_TRANSACTION,
            },
            "400": {"description": "The number in `transaction_no` contains `/`. The web server rejects the request before it reaches the API and returns an HTML page with `Invalid URI: [The encoded slash character is not allowed]`, not a JSON error. A number that contains `/` cannot be read.", "content_type": "text/html", "schema": {"type": "string"}},
            "404": {"description": NOT_FOUND, "schema": ERROR_REF, "example": NOT_FOUND_EXAMPLE},
        },
        "example_call": {"path": {"transaction_no": "IMPORT-2026-0001"}},
    },
    {
        "key": "head_transaction",
        "slug": "check-a-transaction",
        "title": "Check a transaction",
        "method": "HEAD",
        "path": BASE + "/{transaction_no}",
        "summary": "Checks whether any record is stamped with the number in `transaction_no`. Returns headers only.",
        "description": "Returns `200` with headers only and no body when at least one record is stamped with the number, and `404` when none is. The response has no `ETag` header. To read the counts, use [Retrieve a transaction](" + RETRIEVE_PAGE + ").",
        "parameters": [TRANSACTION_NO],
        "responses": {
            "200": {"description": "At least one record is stamped with the number. Headers only, no body."},
            "404": {"description": "No record is stamped with that `transaction_no`. No body."},
        },
        "example_call": {"path": {"transaction_no": "IMPORT-2026-0001"}},
    },
    {
        "key": "list_transaction_items",
        "slug": "list-the-records-of-a-transaction",
        "title": "List the records of a transaction",
        "method": "GET",
        "path": BASE + "/{transaction_no}/items",
        "summary": "Returns the records of one `type` stamped with the number in `transaction_no`, newest first.",
        "description": "Send `type` to choose the kind of record, such as `product` or `category`; the call is rejected with `400` without it. Records come newest first, 20 per call unless you send `limit`, which takes `1` to `200`; `sort` and `order` are ignored. With `detail=slim`, the default, each item has the record's `id` and a few fields that depend on `type`; with `detail=full`, each item is the record as its own retrieve call returns it. A type with no records stamped, or a number no record is stamped with, returns `200` with an empty `items` list and a `total` of `0`, not `404`.",
        "parameters": [TRANSACTION_NO] + ITEMS_QUERY,
        "responses": {
            "200": {
                "description": "The number in `transaction_no`, the `type` you sent, the records on this page in `items`, and `pagination` with ten keys. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "transaction_no": {"type": "string", "description": "The number you sent in the path."},
                    "type": {"type": "string", "description": "The `type` you sent."},
                    "items": {"type": "array", "description": "With `detail=slim`, each item has the record's `id` and the short fields for its `type`. With `detail=full`, each item is the record's full body, which differs by `type`.", "items": {"$ref": "#/components/schemas/TransactionItem"}},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"transaction_no": "IMPORT-2026-0001", "type": "product", "items": SAMPLE_ITEMS, "pagination": ITEMS_PAGINATION},
            },
            "400": {"description": "`type` is missing: the message is `type query parameter is required`. Or `type` is not one of the 15 names in lower case: the message starts `Invalid type '<value>'. Allowed:` and lists the 15 names. Or `detail` is not `slim` or `full`: the message is `detail must be 'slim' or 'full'`. Or `limit` is above `200`: the message is `max cannot exceed 200`, with one `details` entry for `max`. Or `limit`, `offset` or `page` is not accepted, as on [List transactions](" + LIST_PAGE + "). The `error.code` is `invalid_request`.", "schema": ERROR_REF, "example": TYPE_REQUIRED_EXAMPLE},
        },
        "example_call": {"path": {"transaction_no": "IMPORT-2026-0001"}, "query": {"type": "product", "limit": 20, "offset": 0, "detail": "slim"}},
    },
    {
        "key": "head_transaction_items",
        "slug": "check-the-records-of-a-transaction",
        "title": "Check the records of a transaction",
        "method": "HEAD",
        "path": BASE + "/{transaction_no}/items",
        "summary": "Checks that one `type` of records under a number is reachable. Returns headers only.",
        "description": "Send `type` as on [List the records of a transaction](" + ITEMS_PAGE + "): without it the call returns `400`. With it, the call returns `200` with headers only and no body. The response has no `ETag` header.",
        "parameters": [TRANSACTION_NO] + ITEMS_HEAD_QUERY,
        "responses": {
            "200": {"description": "Headers only, no body."},
            "400": {"description": "`type` is missing. No body."},
        },
        "example_call": {"path": {"transaction_no": "IMPORT-2026-0001"}, "query": {"type": "product"}},
    },
]

SCHEMAS = {
    "TransactionListEntry": {"type": "object", "description": "One row of the transactions list.", "properties": {
        "transaction_no": {"type": "string", "description": "The transaction number. Pass it as `transaction_no` in a path."},
        "total_records": {"type": "integer", "description": "How many records are stamped with the number. A record you delete stays counted."},
        "url": {"type": "string", "description": "The path of [Retrieve a transaction](" + RETRIEVE_PAGE + ") for this number. A space in the number appears as `+`, and the link then returns `404`."},
    }},
    "TransactionTypeCount": {"type": "object", "description": "One `by_type` row: the records of one type stamped with the number.", "properties": {
        "type": {"type": "string", "enum": TYPES, "description": "The record type. Pass it as `type` to [List the records of a transaction](" + ITEMS_PAGE + ")."},
        "count": {"type": "integer", "description": "How many records of this type are stamped with the number."},
        "items_url": {"type": "string", "description": "The path of [List the records of a transaction](" + ITEMS_PAGE + ") for this type. Present only when `count` is above `0`. A space in the number appears as `+`, and the link then returns `404`."},
    }},
    "Transaction": {"type": "object", "properties": {
        "transaction_no": {"type": "string", "description": "The transaction number you sent in the path."},
        "total_records": {"type": "integer", "description": "How many records are stamped with the number, across all types."},
        "by_type": {"type": "array", "description": "Always 15 rows in this order: " + TYPE_LIST + ".", "items": {"$ref": "#/components/schemas/TransactionTypeCount"}},
    }},
    "TransactionItem": {"type": "object", "description": "One record stamped with the number, as `detail=slim` returns it. Every item has `id`; the other fields depend on `type`: `category` has `name` and `url`; `product` and `product_variation` have `name`, `sku` and `url`; `product_review` has `name`, `rating` and `url`; `customer` has `email`, `first_name`, `last_name` and `url`; `order` has `order_no`, `grand_total`, `status` and `url`; `currency` has `name`, `code`, `symbol` and `url`; `custom_tax_profile` has `name`, `code` and `url`; `custom_tax_rule` has `name` only; `custom_tax_rule_zone` has `country_code`, `state_name`, `postcode`, `rate` and `priority`; `shipping_profile` has `name`, `description` and `url`; `shipping_rate` has `name`, `policy_type` and `url`. With `detail=full`, the item is the record's full body instead.", "properties": {
        "id": {"type": "integer", "description": "The record's `id`. Where the item has a `url`, the `id` is the last part of it, except for `order`: an order's `url` ends with its `order_no`, the value the orders API takes as `order_id`. For `category`, the `id` is the value [Retrieve a category](/api-reference/categories/retrieve-a-category) takes as `category_id`."},
        "name": {"type": "string", "description": "The record's name. Not returned for `customer`, `order` or `custom_tax_rule_zone`."},
        "sku": {"type": "string", "description": "The SKU of a `product` or `product_variation`."},
        "rating": {"type": "number", "description": "The rating of a `product_review`."},
        "email": {"type": "string", "description": "The email address of a `customer`, such as `jane@example.com`."},
        "first_name": {"type": "string", "description": "The first name of a `customer`."},
        "last_name": {"type": "string", "description": "The last name of a `customer`."},
        "order_no": {"type": "integer", "description": "The order number of an `order`. The order's `url` ends with it."},
        "grand_total": {"type": "number", "description": "The grand total of an `order`."},
        "status": {"type": "string", "description": "The status of an `order`."},
        "code": {"type": "string", "description": "The code of a `currency` or a `custom_tax_profile`."},
        "symbol": {"type": "string", "description": "The symbol of a `currency`."},
        "country_code": {"type": "string", "description": "The country code of a `custom_tax_rule_zone`."},
        "state_name": {"type": ["string", "null"], "description": "The state name of a `custom_tax_rule_zone`, or `null` when the zone has no state."},
        "postcode": {"type": "string", "description": "The post code of a `custom_tax_rule_zone`."},
        "rate": {"type": "number", "description": "The rate of a `custom_tax_rule_zone`."},
        "priority": {"type": "integer", "description": "The priority of a `custom_tax_rule_zone`."},
        "description": {"type": "string", "description": "The description of a `shipping_profile`."},
        "policy_type": {"type": "string", "description": "The policy type of a `shipping_rate`."},
        "url": {"type": "string", "description": "The path you call to retrieve the record, such as `/api/v4/admin/products/207`. Not returned for `custom_tax_rule` or `custom_tax_rule_zone`."},
    }},
    "TransactionPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of rows that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of rows skipped before this page."},
        "count": {"type": "integer", "description": "The number of rows on this page."},
        "current_page": {"type": "integer", "description": "The page number of this page, counting from `1`. Past the last row, it equals `total_pages`."},
        "total_pages": {"type": "integer", "description": "The number of pages at this `limit`."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one. Past the last row it is `false`, even though earlier rows exist."},
        "previous_page": {"type": ["string", "null"], "description": "The absolute URL of the previous page, or `null`."},
        "next_page": {"type": ["string", "null"], "description": "The absolute URL of the next page, or `null`. A space in the number appears as `+`, and the link then returns `404`; call the SDK function with the next `offset` instead."},
    }},
    "TransactionError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What went wrong, such as `transaction not found` or `type query parameter is required`."},
        "details": {"type": "array", "description": "One entry per rejected query parameter or path value. Empty on a `405`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter or path parameter that was rejected, such as `type` or `transaction_no`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `out_of_range`, `invalid_value` or `not_found`."},
            "message": {"type": ["string", "null"], "description": "What the parameter accepts, such as `max cannot exceed 200`, or `null`."},
            "value": {"description": "The value you sent. Not returned when the parameter is missing."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
