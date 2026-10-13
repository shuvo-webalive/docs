"""The Currencies endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Currencies"
SLUG = "currencies"
BASE = "/admin/currencies"
ICON = "coins"

OVERVIEW_DESCRIPTION = "List, count, create, replace, update and delete currencies, and choose the store's base currency."
INTRO = "The Currencies API has eleven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/currencies`."

RETRIEVE_PAGE = "/api-reference/currencies/retrieve-a-currency"
REPLACE_PAGE = "/api-reference/currencies/replace-a-currency"
UPDATE_PAGE = "/api-reference/currencies/update-a-currency"
BASE_PAGE = "/api-reference/currencies/set-the-base-currency"

WARNING = (
    "**Setting the base currency changes the `conversion_rate` of every currency in the store.**\n"
    "  [Set the base currency](" + BASE_PAGE + ") divides every currency's rate, inactive ones included,\n"
    "  by the new base's old rate, and sets a new `updated_at` on every currency. Rates are kept to 6\n"
    "  decimal places, so switching back does not always restore a rate exactly. Product `base_price` values do not change."
)

NOTES = [
    "**Send the fields at the top level of the body, not inside `currency`.** Create, replace and\n"
    "  update all take the bare record. A body wrapped in `currency` is rejected with `400`: `currency`\n"
    "  is reported as `unknown_field`, and `name`, `code` and `symbol` as `required`. Responses return the\n"
    "  currency inside `currency`.",
    "**`PUT` replaces a currency, and `PATCH` changes only the fields you send.**\n"
    "  [Replace a currency](" + REPLACE_PAGE + ") resets every field you leave out: `conversion_rate` to `1`,\n"
    "  `rounding` to `nearest`, `precision` to `2`, `active` to `true` and `country` to the store's default\n"
    "  country. To change one field, use [Update a currency](" + UPDATE_PAGE + ").",
    "**Exactly one currency is the base, and you cannot replace, update or delete it.** `PUT` and `PATCH` on\n"
    "  the base currency are rejected with `400`, and `DELETE` with `409`. Make another currency the base\n"
    "  first with [Set the base currency](" + BASE_PAGE + "). That call is the only way to move the flag,\n"
    "  and it rejects an inactive currency.",
    "**A listing returns 20 currencies per call unless you send `limit`.** `limit` takes `1` to `100`,\n"
    "  and `pagination.limit` shows the page size applied. To get more, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. `page` is rejected with `400`. `q` does not filter the listing:\n"
    "  the store ignores it and returns every currency, so send `search` instead.",
    "**`code` is any three letters, stored in upper case.** The store does not check it against\n"
    "  ISO 4217, even though `field_metadata` describes it as an ISO 4217 code. `code` and `name` must\n"
    "  each be unique: a taken one is rejected with `409`. `name` is compared without regard to letter case.",
]

CURRENCY_ID = {
    "name": "currency_id",
    "in": "path",
    "required": True,
    "description": "The currency's `id`, from a listing or from the response to creating the currency.",
    "schema": {"type": "integer", "example": 1234},
}

SORT_FIELDS = ["id", "name", "code", "symbol", "precision", "rounding", "conversion_rate", "active", "base", "updated_at"]

SEARCH = {"name": "search", "in": "query", "description": "Keeps only currencies whose `name` or `code` contains this text, in any letter case. It does not search `symbol` or the country.", "schema": {"type": "string", "example": "dollar"}}
ACTIVE = {"name": "active", "in": "query", "description": "Send `true` to keep only active currencies, or `false` to keep only inactive ones. Any other value is rejected with `400`, the reason `invalid_enum` and the message `must be true or false`.", "schema": {"type": "boolean", "example": True}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by. Without it, currencies come in ascending order of the currency's `id`, and the base currency is not moved to the top. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "code"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`. Any other value is rejected with `400`. `order` is accepted as another name for `dir`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "desc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of currencies per page, from `1` to `100`. Defaults to `20`. `pagination.limit` shows the value applied. `0` and values above `100` are rejected with `400` and the message `must be a whole number from 1 to 100`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of currencies to skip, `0` or more. A negative value is rejected with `400`, the reason `out_of_range` and the message `must be 0 or more`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
FIELD_METADATA_LIST = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key beside `currencies` and `pagination`. It describes each currency field: its type, whether you can write it, and its limits and default.", "schema": {"type": "boolean", "example": True}}
FIELD_METADATA_ROW = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key beside `currency`. It describes each currency field: its type, whether you can write it, and its limits and default.", "schema": {"type": "boolean", "example": True}}

ERROR_REF = {"$ref": "#/components/schemas/CurrencyError"}
ROW_REF = {"$ref": "#/components/schemas/Currency"}
PAGINATION_REF = {"$ref": "#/components/schemas/CurrencyPagination"}
FIELD_METADATA_REF = {"$ref": "#/components/schemas/CurrencyFieldMetadata"}
ROW_RESPONSE = {"type": "object", "properties": {"currency": ROW_REF}}
NOT_FOUND_RESPONSE = {"description": "No currency has that `currency_id`. The message is `Currency <currency_id> was not found.` and the reason is `not_found`.", "schema": ERROR_REF}

US = {"id": 236, "code": "US", "name": "United States"}
NZ = {"id": 160, "code": "NZ", "name": "New Zealand"}
GB = {"id": 235, "code": "GB", "name": "United Kingdom"}

SAMPLE_ROWS = [
    {"id": 1, "name": "US Dollar", "code": "USD", "symbol": "$", "country": US, "conversion_rate": 1, "rounding": "nearest", "precision": 2, "active": True, "base": True, "updated_at": "2026-10-11T04:12:09Z"},
    {"id": 4, "name": "Pound Sterling", "code": "GBP", "symbol": "£", "country": GB, "conversion_rate": 0.79, "rounding": "nearest", "precision": 2, "active": True, "base": False, "updated_at": "2026-10-11T04:12:09Z"},
]

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"name": "Example Dollar", "code": "XEX", "symbol": "$", "country": "NZ", "conversion_rate": 1.2345, "precision": 2, "rounding": "nearest", "active": True}
CREATED_ROW = {"id": 1234, "name": "Example Dollar", "code": "XEX", "symbol": "$", "country": NZ, "conversion_rate": 1.2345, "rounding": "nearest", "precision": 2, "active": True, "base": False, "updated_at": "2026-10-11T05:20:41Z"}

REPLACE_BODY = {"name": "Example Dollar", "code": "XEX", "symbol": "$", "country": {"code": "US"}, "conversion_rate": 1.5, "precision": 3, "rounding": "up", "active": False}
REPLACED_ROW = dict(CREATED_ROW, country=US, conversion_rate=1.5, precision=3, rounding="up", active=False, updated_at="2026-10-11T05:24:02Z")

PATCH_BODY = {"conversion_rate": 2.5}
PATCHED_ROW = dict(CREATED_ROW, conversion_rate=2.5, updated_at="2026-10-11T05:26:15Z")

BASE_CHANGE = {
    "currency": {"id": 1234, "name": "Example Dollar", "code": "XEX", "base": True},
    "previous_base": {"id": 1, "code": "USD", "name": "US Dollar"},
}

WRITE_400 = (
    "The body is not valid for a currency. `name`, `code` or `symbol` is missing (reason `required`); "
    "`code` is not three letters (reason `invalid_format`); `symbol` is longer than 3 characters (reason `too_long`); "
    "`precision` is outside `1` to `9` (reason `out_of_range`); `rounding` is not `nearest`, `up` or `down` (reason `invalid_enum`); "
    "`country` is a list (reason `invalid_type`) or names a country the store does not have (reason `unknown_reference`, message `no such country`); "
    "the body has a field that is not a currency field, such as `base`, `updated_at` or a wrapping `currency` (reason `unknown_field`, message `is not a currency field`); "
    "or it sends `id` (reason `unexpected_field`, message `must not be present - the URL names the currency`). "
    "`error.code` is `invalid_request`, and the reason for each field is in `details[].code`."
)
BASE_READ_ONLY_400 = (
    "The currency is the base currency. The message is `The base currency is read-only - make another currency the base first.`, "
    "and `details[0]` has `field` `base` and `code` `base_currency_read_only`."
)

ENDPOINTS = [
    {
        "key": "list_currencies",
        "slug": "list-currencies",
        "title": "List currencies",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 currencies per call, or the `limit` you send, with paging totals.",
        "description": "Returns the currencies in `currencies`, 20 per call unless you send `limit`, and `pagination` with the total and whether more pages follow. Without `sort`, they come in ascending order of the currency's `id`, and the base currency is not moved to the top. Send `search` to find currencies by `name` or `code`, and `active` to keep only active or inactive ones. `page` is rejected with `400`; `q`, `base` and any other unknown query parameter are ignored and do not filter the listing.",
        "parameters": [SEARCH, ACTIVE, SORT, DIR, LIMIT, OFFSET, FIELD_METADATA_LIST],
        "responses": {
            "200": {
                "description": "The currencies on this page in `currencies`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. With `field_metadata=true`, a `field_metadata` key is added beside them. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "currencies": {"type": "array", "items": ROW_REF},
                    "pagination": PAGINATION_REF,
                    "field_metadata": FIELD_METADATA_REF,
                }},
                "example": {"currencies": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "A query parameter has a value the listing does not accept: `active` is not `true` or `false`, `sort` is not one of the ten sort fields (reason `invalid_enum`, and the message lists the ten fields), `dir` is not `asc` or `desc`, `limit` is `0` or more than `100` (reason `out_of_range`), or `offset` is negative. Or you sent `page`: the reason is `unsupported_parameter` and the message is `is not supported - page with offset and limit`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "search=dollar&active=true"},
    },
    {
        "key": "head_currencies",
        "slug": "check-the-currencies-list",
        "title": "Check the currencies list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the currencies list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body: `Content-Length` is `0`. The response has no `ETag` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_currencies",
        "slug": "count-currencies",
        "title": "Count currencies",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of currencies that match `search` and `active`, as `total`.",
        "description": "Returns the number of currencies as `total`, at the top level of the body. `search` and `active` narrow the count as they narrow the listing, so the number matches the listing's `pagination.total` for the same filters. `limit`, `q`, `field_metadata` and unknown query parameters are ignored. A bad `active` or `sort` value is rejected with `400`, as on the listing, even though the count does not sort.",
        "parameters": [SEARCH, ACTIVE],
        "responses": {
            "200": {
                "description": "The number of matching currencies. The response has no `ETag` header.",
                "schema": {"$ref": "#/components/schemas/CurrencyCount"},
                "example": {"total": 2},
            },
            "400": {"description": "`active` is not `true` or `false`, or `sort` is not one of the ten sort fields.", "schema": ERROR_REF},
        },
        "example_call": {"query": "search=dollar&active=true"},
    },
    {
        "key": "head_currencies_count",
        "slug": "check-the-currency-count",
        "title": "Check the currency count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Checks that the currency count is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body: `Content-Length` is `0`. The response has no `ETag` header.",
        "responses": {
            "200": {"description": "The count is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_currency",
        "slug": "create-a-currency",
        "title": "Create a currency",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a currency and returns it with its `id`, which other calls take as `currency_id`.",
        "description": "Send the fields at the top level of the body, not wrapped in `currency`. `name`, `code` and `symbol` are required, and the store trims spaces from all three and stores `code` in upper case. A field you leave out gets its default: `conversion_rate` `1`, `rounding` `nearest`, `precision` `2`, `active` `true` and the store's default country. A new currency always has `base` set to `false`.",
        "body": {"schema": {"$ref": "#/components/schemas/CurrencyInput"}, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new currency, with the currency's `id`, which the other calls take as `currency_id`. The `Location` header holds the full URL of the new currency.",
                "schema": ROW_RESPONSE,
                "example": {"currency": CREATED_ROW},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
            "409": {"description": "Another currency already has that `name`, in any letter case (`A currency with this name already exists.`, `details[0].code` `duplicate`) or that `code` (`A currency with this code already exists.`). The reason is `conflict`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_currency",
        "slug": "retrieve-a-currency",
        "title": "Retrieve a currency",
        "method": "GET",
        "path": BASE + "/{currency_id}",
        "summary": "Returns the currency whose `id` you pass as `currency_id`, with an `ETag` header.",
        "description": "Returns one currency under the `currency` key, with the same eleven fields a listing entry has. The response has an `ETag` header, which changes when the currency changes. Send `field_metadata=true` to add a description of each field beside `currency`.",
        "parameters": [CURRENCY_ID, FIELD_METADATA_ROW],
        "responses": {
            "200": {
                "description": "The currency. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": {"type": "object", "properties": {"currency": ROW_REF, "field_metadata": FIELD_METADATA_REF}},
                "example": {"currency": CREATED_ROW},
            },
            "404": NOT_FOUND_RESPONSE,
        },
        "example_call": {"path": {"currency_id": 1234}, "query": "field_metadata=true"},
    },
    {
        "key": "head_currency",
        "slug": "check-a-currency",
        "title": "Check a currency",
        "method": "HEAD",
        "path": BASE + "/{currency_id}",
        "summary": "Returns headers only for the currency you pass as `currency_id`, including its `ETag`.",
        "description": "Returns `200` with headers only and no body when a currency has that `currency_id`, and `404` when none does. The `ETag` header is the same one [Retrieve a currency](" + RETRIEVE_PAGE + ") returns, so you can check whether the currency changed without reading it.",
        "parameters": [CURRENCY_ID],
        "responses": {
            "200": {"description": "The currency exists. Headers only, no body, with the currency's `ETag`."},
            "404": {"description": "No currency has that `currency_id`. No body."},
        },
        "example_call": {"path": {"currency_id": 1234}},
    },
    {
        "key": "update_currency",
        "slug": "replace-a-currency",
        "title": "Replace a currency",
        "method": "PUT",
        "path": BASE + "/{currency_id}",
        "summary": "Replaces every field of a currency with your body and returns the currency.",
        "description": "Send `name`, `code` and `symbol`, and every other field you want to keep, at the top level of the body. This call replaces the currency rather than merging: a field you leave out goes back to its default, so `conversion_rate` becomes `1`, `rounding` `nearest`, `precision` `2`, `active` `true` and `country` the store's default country. The body follows the same rules as [Create a currency](/api-reference/currencies/create-a-currency). You cannot replace the base currency.",
        "parameters": [CURRENCY_ID],
        "body": {"schema": {"$ref": "#/components/schemas/CurrencyInput"}, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The currency after the replace, with the values you sent and the default for every field you left out.",
                "schema": ROW_RESPONSE,
                "example": {"currency": REPLACED_ROW},
            },
            "400": {"description": BASE_READ_ONLY_400 + " Or the body breaks a rule of [Create a currency](/api-reference/currencies/create-a-currency), such as a missing `name`, `code` or `symbol`, an unknown field or an `id`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"currency_id": 1234}},
    },
    {
        "key": "patch_currency",
        "slug": "update-a-currency",
        "title": "Update a currency",
        "method": "PATCH",
        "path": BASE + "/{currency_id}",
        "summary": "Changes only the fields you send and returns the currency.",
        "description": "Send only the fields to change, at the top level of the body. Every field you leave out keeps its value. The store trims spaces from `name`, `code` and `symbol` as on create. An empty body is rejected with `400`, and so is any change to the base currency.",
        "parameters": [CURRENCY_ID],
        "body": {"schema": {"$ref": "#/components/schemas/CurrencyPatchInput"}, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The currency after the change.",
                "schema": ROW_RESPONSE,
                "example": {"currency": PATCHED_ROW},
            },
            "400": {"description": BASE_READ_ONLY_400 + " Or the body is empty (message `request body is empty`), has a field that is not a currency field, or sends `id`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"currency_id": 1234}},
    },
    {
        "key": "delete_currency",
        "slug": "delete-a-currency",
        "title": "Delete a currency",
        "method": "DELETE",
        "path": BASE + "/{currency_id}",
        "summary": "Deletes a currency permanently. You cannot delete the base currency.",
        "description": "Deletes the currency permanently and returns `204` with no body. The currency leaves the listing, the count goes down by one, and retrieving or deleting it again returns `404`. You cannot delete the base currency: make another currency the base first with [Set the base currency](" + BASE_PAGE + ").",
        "parameters": [CURRENCY_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No currency has that `currency_id`, for example because you already deleted it.", "schema": ERROR_REF},
            "409": {"description": "The currency is the base currency. The message is `The base currency cannot be deleted.` and the reason is `conflict`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"currency_id": 1234}},
    },
    {
        "key": "set_base_currency",
        "slug": "set-the-base-currency",
        "title": "Set the base currency",
        "method": "PUT",
        "path": BASE + "/{currency_id}/base",
        "summary": "Makes an active currency the base and rescales every currency's `conversion_rate` to match.",
        "description": "Makes the currency the base: its `conversion_rate` becomes `1`, the old base loses the flag, and every other currency's rate, inactive ones included, is divided by the new base's old rate. Every currency gets a new `updated_at` and `ETag`. Send no body: any body, `{}` included, is rejected with `400`. The response returns only the new base's `id`, `name`, `code` and `base`, so retrieve the currency for its other fields.",
        "parameters": [CURRENCY_ID],
        "responses": {
            "200": {
                "description": "The new base in `currency`, with `id`, `name`, `code` and `base`. `previous_base` names the currency that was the base, with `id`, `code` and `name`. `previous_base` is `null` when the currency you named was already the base.",
                "schema": {"$ref": "#/components/schemas/CurrencyBaseChange"},
                "example": BASE_CHANGE,
            },
            "400": {"description": "You sent a body (message `This endpoint takes no request body.`), or the currency is inactive (message `An inactive currency cannot be the base currency - activate it first.`, `details[0].code` `inactive_currency`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"currency_id": 1234}},
    },
]

INPUT_PROPERTIES = {
    "name": {"type": "string", "maxLength": 100, "description": "At most 100 characters. No other currency may have the same name in any letter case. Spaces at either end are removed."},
    "code": {"type": "string", "pattern": "^\\s*[A-Za-z]{3}\\s*$", "description": "Three letters, stored in upper case. No other currency may have the same code. The store does not check it against ISO 4217."},
    "symbol": {"type": "string", "maxLength": 3, "description": "At most 3 characters. Spaces at either end are removed."},
    "country": {
        "description": "The country's numeric `id`, its two-letter `code`, its `name`, or an object such as `{\"code\": \"NZ\"}`. Defaults to the store's default country. A country the store does not have is rejected with `400`.",
        "oneOf": [
            {"type": "integer"},
            {"type": "string"},
            {"type": "object", "properties": {"code": {"type": "string"}}},
        ],
    },
    "conversion_rate": {"type": "number", "exclusiveMinimum": 0, "maximum": 999999999, "description": "Above `0` and at most `999999999`. Stored to 6 decimal places, so `1.234567891` is stored as `1.234568`. Defaults to `1`."},
    "rounding": {"type": "string", "enum": ["nearest", "up", "down"], "description": "Defaults to `nearest`."},
    "precision": {"type": "integer", "minimum": 1, "maximum": 9, "description": "From `1` to `9`. Defaults to `2`."},
    "active": {"type": "boolean", "description": "Defaults to `true`. An inactive currency cannot be made the base."},
}

FIELD_DESCRIPTION = {"type": "object", "description": "Describes one currency field. Other keys give the field's limits and default.", "properties": {
    "type": {"type": "string", "description": "The field's value type: `string`, `reference`, `number`, `enum`, `integer`, `boolean` or `datetime`."},
    "required": {"type": "boolean", "description": "On the eight writable fields: `true` on `name`, `code` and `symbol`, and `false` on the others."},
    "unique": {"type": "boolean", "description": "`true` on `name` and `code`."},
    "writable": {"type": "boolean", "description": "`true` on the eight fields a write can set: `name`, `code`, `symbol`, `country`, `conversion_rate`, `rounding`, `precision` and `active`."},
    "read_only": {"type": "boolean", "description": "`true` on `id`, `base` and `updated_at`."},
    "options": {"type": "array", "items": {"type": "string"}, "description": "On `rounding`: `nearest`, `up` and `down`."},
    "accepts": {"type": "array", "items": {"type": "string"}, "description": "On `country`: `id`, `code`, `name` and `object`, the forms a write can send."},
    "pattern": {"type": "string", "description": "On `code`: `3 letters (ISO 4217), stored upper-case`. Any three letters are accepted."},
    "note": {"type": "string", "description": "On `base`: `change with PUT /api/v4/admin/currencies/{id}/base`, where `{id}` is the currency's `currency_id`."},
}}

ROW_FIELDS = ["id", "name", "code", "symbol", "country", "conversion_rate", "rounding", "precision", "active", "base", "updated_at"]

SCHEMAS = {
    "Currency": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The currency's `id`, set by the store. Pass it as `currency_id` in the path of the other calls."},
        "name": {"type": "string", "description": "The currency's name, unique in any letter case."},
        "code": {"type": "string", "description": "Three upper-case letters, unique across the store's currencies."},
        "symbol": {"type": "string", "description": "At most 3 characters."},
        "country": {"$ref": "#/components/schemas/CurrencyCountry"},
        "conversion_rate": {"type": "number", "description": "The currency's rate against the base currency, to at most 6 decimal places. `1` on the base currency. A whole number, such as `1`, is returned without a decimal point."},
        "rounding": {"type": "string", "enum": ["nearest", "up", "down"]},
        "precision": {"type": "integer", "description": "From `1` to `9`."},
        "active": {"type": "boolean", "description": "Whether the currency is active."},
        "base": {"type": "boolean", "description": "`true` on the store's base currency. Exactly one currency has it, and only [Set the base currency](" + BASE_PAGE + ") changes it."},
        "updated_at": {"type": "string", "description": "When the currency last changed, such as `2026-10-11T04:12:09Z`. Setting the base currency changes it on every currency."},
    }},
    "CurrencyCountry": {"type": "object", "description": "The country the currency belongs to.", "properties": {
        "id": {"type": "integer", "description": "The country's numeric `id`. A write can send it as `country`."},
        "code": {"type": "string", "description": "The country's two-letter code."},
        "name": {"type": "string", "description": "The country's name."},
    }},
    "CurrencyInput": {"type": "object", "required": ["name", "code", "symbol"], "description": "Send these fields at the top level of the body. Any other field, `id` included, is rejected with `400`.", "properties": INPUT_PROPERTIES},
    "CurrencyPatchInput": {"type": "object", "minProperties": 1, "description": "Send only the fields to change, at the top level of the body. Any other field, `id` included, is rejected with `400`, and so is an empty body.", "properties": INPUT_PROPERTIES},
    "CurrencyPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of currencies that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of currencies skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is above `0`, even past the last currency."},
        "has_next": {"type": "boolean", "description": "`true` when there are currencies after this page."},
    }},
    "CurrencyCount": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of currencies that match `search` and `active`."},
    }},
    "CurrencyReference": {"type": "object", "description": "The currency that was the base before the change.", "properties": {
        "id": {"type": "integer", "description": "The previous base currency's `id`, which other calls take as `currency_id`."},
        "code": {"type": "string", "description": "The previous base currency's `code`."},
        "name": {"type": "string", "description": "The previous base currency's `name`."},
    }},
    "CurrencyBaseChange": {"type": "object", "properties": {
        "currency": {"type": "object", "description": "The new base currency. Only these four fields are returned.", "properties": {
            "id": {"type": "integer", "description": "The new base currency's `id`, the `currency_id` you sent."},
            "name": {"type": "string"},
            "code": {"type": "string"},
            "base": {"type": "boolean", "description": "Always `true`."},
        }},
        "previous_base": {"oneOf": [{"$ref": "#/components/schemas/CurrencyReference"}, {"type": "null"}], "description": "The currency that was the base, or `null` when the currency you named was already the base."},
    }},
    "CurrencyFieldDescription": FIELD_DESCRIPTION,
    "CurrencyFieldMetadata": {"type": "object", "description": "Describes each currency field, keyed by field name. Returned only when you send `field_metadata=true`.", "properties": {
        field: {"$ref": "#/components/schemas/CurrencyFieldDescription"} for field in ROW_FIELDS
    }},
    "CurrencyError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string", "description": "What went wrong, such as `The base currency cannot be deleted.`"},
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `unknown_field` or `duplicate`."},
            "message": {"type": "string", "description": "The reason in words, such as `is not a currency field`."},
            "value": {"type": "string", "description": "The value you sent for a rejected query parameter, such as `bogus` for `sort=bogus`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
