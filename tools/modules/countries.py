"""The Countries endpoints, written from the SDKs' ENDPOINTS.md."""

TAG = "Countries"
SLUG = "countries"
BASE = "/admin/countries"
ICON = "earth-americas"

OVERVIEW_DESCRIPTION = "List your store's countries and each country's states, and look one up by its `id`, `code` or `name`."
INTRO = "The Countries API has eight endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/countries`."

RETRIEVE_COUNTRY_PAGE = "/api-reference/countries/retrieve-a-country"
LIST_STATES_PAGE = "/api-reference/countries/list-the-states-of-a-country"
RETRIEVE_STATE_PAGE = "/api-reference/countries/retrieve-a-state"
SITE_SETTINGS_SECTION_PAGE = "/api-reference/site-settings/get-a-settings-section"

WARNING = (
    "**Send `order`, not `dir`, to reverse a listing, and `search`, not `q`, to find rows by text.**\n"
    "  Both listings ignore `dir`, `q`, `field_metadata` and any other parameter they do not know,\n"
    "  except `page`: you get `200` and the same rows as without them. `order` takes `asc` or `desc`;\n"
    "  `search` matches part of a `name` or a `code`."
)

NOTES = [
    "**You can only read countries and states.** Every path accepts `GET`, `HEAD` and `OPTIONS`, and\n"
    "  `OPTIONS` returns `204` with `Allow: GET, HEAD, OPTIONS`.\n"
    "  `POST`, `PUT` and `PATCH` are rejected with `405 method_not_allowed`, the message\n"
    "  `HTTP method not allowed for this endpoint.` and the header `Allow: GET, HEAD, OPTIONS`.",
    "**`country_id` and `state_id` each take an `id`, a `code` or a `name`.** `{country_id}` takes the country's\n"
    "  numeric `id`, its two-letter `code` or its `name`. `{state_id}` takes the state's `id`, `code` or\n"
    "  `name` within that country. Letter case does not matter, surrounding spaces are trimmed, and every\n"
    "  form returns the same body and `ETag`. A state's `id` is unique across all countries, but the state path\n"
    "  still returns `404` for a state that belongs to another country.",
    "**Exactly one country has `default` set to `true`.** It is the `default_country` in the\n"
    "  `administration` section of the site settings, which you read with\n"
    "  [Get a settings section](" + SITE_SETTINGS_SECTION_PAGE + "). The state named there as\n"
    "  `default_state`, when one is set, is the only state with `default` set to `true`.",
    "**Send `limit=all` to get every row in one call.** It returns every row from `offset` on. In that\n"
    "  response, `pagination.limit` is the number of rows returned, not the word `all`. Otherwise\n"
    "  `limit` takes `1` to `100` and defaults to `20`. `all` works in any letter case. `page` is\n"
    "  rejected with `400`: use `offset`.",
    "**Every read returns an `ETag`.** Each `GET` response has an `ETag` and\n"
    "  `Cache-Control: private, no-cache`, and no `Last-Modified`. Each `HEAD` returns the same `ETag`\n"
    "  as the matching `GET`. Send that `ETag` in `If-None-Match` on a `GET` or a `HEAD`, and while it\n"
    "  is still current you get `304` with no body. The SDK functions take no headers, so they never\n"
    "  send `If-None-Match`: you get `304` only from your own HTTP calls.",
    "**Errors have one shape.** The body is an `error` object with `code`, `message`, `details` and\n"
    "  `request_id`. A rejected query parameter adds one `details` entry with its `field`, `code`,\n"
    "  `message` and `value`, and `message` counts them, such as `1 parameter failed validation.`.\n"
    "  `details` is empty on a `404` or a `405`.",
]

COUNTRY_ID = {
    "name": "country_id",
    "in": "path",
    "required": True,
    "description": "The country's numeric `id`, its two-letter `code` or its `name`, in any letter case, such as `12`, `AU`, `au` or `Australia`. Surrounding spaces are trimmed. The SDKs encode the spaces in a name such as `New Zealand` for you.",
    "schema": {"type": "string", "example": "AU"},
}

STATE_ID = {
    "name": "state_id",
    "in": "path",
    "required": True,
    "description": "The state's numeric `id`, its `code` or its `name`, in any letter case, such as `72`, `VIC` or `Victoria`. Surrounding spaces are trimmed. The state must belong to the country in `country_id`.",
    "schema": {"type": "string", "example": "VIC"},
}


def limit_parameter(rows):
    return {
        "name": "limit",
        "in": "query",
        "description": "The number of " + rows + " per page, from `1` to `100`, or `all` (in any letter case) for every row from `offset` on. Defaults to `20`. `pagination.limit` shows the page size applied; with `all` it shows the number of rows returned. `0`, `-1`, `101` and text other than `all` are rejected with `400`.",
        "schema": {"oneOf": [{"type": "integer", "minimum": 1, "maximum": 100}, {"type": "string", "enum": ["all"]}], "example": 20},
    }


def offset_parameter(rows):
    return {
        "name": "offset",
        "in": "query",
        "description": "The number of " + rows + " to skip. A negative value is rejected with `400`. An `offset` past the last row returns no rows, the full `total`, `has_previous` set to `true` and `has_next` set to `false`.",
        "schema": {"type": "integer", "minimum": 0, "example": 0},
    }


SORT = {"name": "sort", "in": "query", "description": "The field to sort by: `id`, `name` or `code`. Defaults to `id`. `name` sorts without regard to letter case. Any other value, `state_count` included, is rejected with `400`.", "schema": {"type": "string", "enum": ["id", "name", "code"], "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Defaults to `asc`. `dir` is ignored.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "desc"}}

COUNTRY_QUERY = [
    limit_parameter("countries"),
    offset_parameter("countries"),
    {"name": "code", "in": "query", "description": "Keeps only the country with this two-letter `code`, in any letter case. A value that is not two letters is rejected with `400`.", "schema": {"type": "string", "example": "NZ"}},
    {"name": "name", "in": "query", "description": "Keeps only the country with exactly this `name`, in any letter case. Part of a name matches nothing; use `search` for that.", "schema": {"type": "string", "example": "New Zealand"}},
    {"name": "id", "in": "query", "description": "Keeps only the country whose `id` is this number.", "schema": {"type": "integer", "example": 160}},
    {"name": "search", "in": "query", "description": "Keeps only countries whose `name` or `code` contains this text, in any letter case. `gb` finds United Kingdom by its code. A value of only spaces applies no filter.", "schema": {"type": "string", "example": "zeal"}},
    {"name": "active", "in": "query", "description": "`true` keeps only active countries and `false` only inactive ones, in any letter case. Any other value, `1` included, is rejected with `400`.", "schema": {"type": "boolean", "example": True}},
    SORT,
    ORDER,
]

STATE_QUERY = [
    limit_parameter("states"),
    offset_parameter("states"),
    {"name": "code", "in": "query", "description": "Keeps only the state with this `code`, in any letter case. The code is one to three letters or digits; any other value is rejected with `400`.", "schema": {"type": "string", "example": "VIC"}},
    {"name": "name", "in": "query", "description": "Keeps only the state with exactly this `name`, in any letter case.", "schema": {"type": "string", "example": "Victoria"}},
    {"name": "id", "in": "query", "description": "Keeps only the state whose `id` is this number.", "schema": {"type": "integer", "example": 72}},
    {"name": "search", "in": "query", "description": "Keeps only states whose `name` or `code` contains this text, in any letter case.", "schema": {"type": "string", "example": "south"}},
    {"name": "active", "in": "query", "description": "`true` keeps only active states and `false` only inactive ones. Any other value is rejected with `400`.", "schema": {"type": "boolean", "example": True}},
    SORT,
    ORDER,
]

REQUEST_ID = "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


COUNTRY_NOT_FOUND = error("not_found", "Country not found")
STATE_NOT_FOUND = error("not_found", "State not found")
LIMIT_REJECTED = error("invalid_request", "1 parameter failed validation.", [
    {"field": "limit", "code": "out_of_range", "message": "must be a whole number from 1 to 100, or all", "value": "101"},
])

ERROR_REF = {"$ref": "#/components/schemas/CountryError"}
COUNTRY_REF = {"$ref": "#/components/schemas/Country"}
REFERENCE_REF = {"$ref": "#/components/schemas/CountryReference"}
STATE_REF = {"$ref": "#/components/schemas/CountryState"}
PAGINATION_REF = {"$ref": "#/components/schemas/CountryPagination"}

AUSTRALIA = {"id": 12, "code": "AU", "name": "Australia", "state_count": 8, "active": True, "default": False}
AUSTRIA = {"id": 14, "code": "AT", "name": "Austria", "state_count": 0, "active": True, "default": False}
NEW_ZEALAND = {"id": 160, "code": "NZ", "name": "New Zealand", "state_count": 16, "active": True, "default": True}
AUSTRALIA_REFERENCE = {"id": 12, "code": "AU", "name": "Australia"}

SAMPLE_STATES = [
    {"id": 66, "code": "ACT", "name": "Australian Capital Territory", "active": True, "default": False},
    {"id": 67, "code": "NSW", "name": "New South Wales", "active": True, "default": False},
    {"id": 68, "code": "NT", "name": "Northern Territory", "active": True, "default": False},
]
VICTORIA = {"id": 72, "code": "VIC", "name": "Victoria", "active": True, "default": False}

LIST_400 = "You sent a query parameter value the listing does not accept, such as `limit=101`, or you sent `page`. The `error.code` is `invalid_request`. Each rejected parameter has a `details` entry naming it in `field`. The messages are `must be a whole number from 1 to 100, or all` for `limit`, `must be 0 or more` for `offset`, `must be true or false` for `active`, `must be one of id, name, code` for `sort`, and `is not supported - page with offset and limit` for `page`."
NOT_MODIFIED = {"description": "You sent the current `ETag` in `If-None-Match`. No body."}

ENDPOINTS = [
    {
        "key": "list_countries",
        "slug": "list-countries",
        "title": "List countries",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 countries per call, or the `limit` you send, in `id` order.",
        "description": "Returns your store's countries in ascending `id` order, 20 per call unless you send `limit`. Send `code`, `name` or `id` to find one country by its exact value, or `search` to match part of a `name` or `code`; filters you send together must all match. Send `sort` and `order` to change the order. `dir`, `q`, `field_metadata` and other parameters the listing does not know, except `page`, are ignored.",
        "parameters": COUNTRY_QUERY,
        "responses": {
            "200": {
                "description": "The countries on this page in `countries`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. The response has an `ETag` header and `Cache-Control: private, no-cache`.",
                "schema": {"type": "object", "properties": {
                    "countries": {"type": "array", "items": COUNTRY_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"countries": [AUSTRALIA, AUSTRIA], "pagination": {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}},
            },
            "304": NOT_MODIFIED,
            "400": {
                "description": LIST_400 + " A `code` that is not two letters is rejected with `must be a 2-letter country code`.",
                "schema": ERROR_REF,
                "example": LIMIT_REJECTED,
            },
        },
        "example_call": {"query": {"search": "aus"}},
    },
    {
        "key": "head_countries",
        "slug": "check-the-countries-list",
        "title": "Check the countries list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers of the countries list, including its `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [List countries](/api-reference/countries/list-countries) returns when you send no query parameters. Compare it with the `ETag` you saved to see whether the list changed without downloading it.",
        "responses": {
            "200": {"description": "Headers only, including the list's `ETag`. No body."},
            "304": NOT_MODIFIED,
        },
        "example_call": {},
    },
    {
        "key": "get_country",
        "slug": "retrieve-a-country",
        "title": "Retrieve a country",
        "method": "GET",
        "path": BASE + "/{country_id}",
        "summary": "Returns the country you name in `country_id` by its `id`, `code` or `name`.",
        "description": "Returns one country under the `country` key, with the same six fields a listing row has: `id`, `code`, `name`, `state_count`, `active` and `default`. `AU`, `au`, `Australia` and the country's `id` all return the same body and the same `ETag`. A query parameter you add is ignored.",
        "parameters": [COUNTRY_ID],
        "responses": {
            "200": {
                "description": "The country. The response has an `ETag` header and `Cache-Control: private, no-cache`.",
                "schema": {"type": "object", "properties": {"country": COUNTRY_REF}},
                "example": {"country": AUSTRALIA},
            },
            "304": NOT_MODIFIED,
            "404": {"description": "No country has that `country_id` as its `id`, `code` or `name`. The message is `Country not found`.", "schema": ERROR_REF, "example": COUNTRY_NOT_FOUND},
        },
        "example_call": {"path": {"country_id": "AU"}},
    },
    {
        "key": "head_country",
        "slug": "check-a-country",
        "title": "Check a country",
        "method": "HEAD",
        "path": BASE + "/{country_id}",
        "summary": "Returns the headers of one country, including its `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [Retrieve a country](" + RETRIEVE_COUNTRY_PAGE + ") returns for that country, whichever form of `country_id` you send.",
        "parameters": [COUNTRY_ID],
        "responses": {
            "200": {"description": "Headers only, including the country's `ETag`. No body."},
            "304": NOT_MODIFIED,
        },
        "example_call": {"path": {"country_id": "AU"}},
    },
    {
        "key": "list_country_states",
        "slug": "list-the-states-of-a-country",
        "title": "List the states of a country",
        "method": "GET",
        "path": BASE + "/{country_id}/states",
        "summary": "Returns the country's states, up to 20 per call, with the country's `id`, `code` and `name`.",
        "description": "Returns the states of the country in `country_id`, in ascending `id` order, 20 per call unless you send `limit`. The country's `id`, `code` and `name` come in `country`, next to `states` and `pagination`. The query parameters work as they do on [List countries](/api-reference/countries/list-countries), except that a state `code` is one to three letters or digits. A country with no states returns an empty `states` list and a `total` of `0`.",
        "parameters": [COUNTRY_ID] + STATE_QUERY,
        "responses": {
            "200": {
                "description": "The country's `id`, `code` and `name` in `country`, the states on this page in `states`, and `pagination`. The response has an `ETag` header and `Cache-Control: private, no-cache`.",
                "schema": {"type": "object", "properties": {
                    "country": REFERENCE_REF,
                    "states": {"type": "array", "items": STATE_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"country": AUSTRALIA_REFERENCE, "states": SAMPLE_STATES, "pagination": {"total": 8, "limit": 3, "offset": 0, "has_previous": False, "has_next": True}},
            },
            "304": NOT_MODIFIED,
            "400": {
                "description": LIST_400 + " A state `code` that is not one to three letters or digits is rejected with `must be 1 to 3 letters or digits`.",
                "schema": ERROR_REF,
                "example": LIMIT_REJECTED,
            },
            "404": {"description": "No country has that `country_id` as its `id`, `code` or `name`. The message is `Country not found`.", "schema": ERROR_REF, "example": COUNTRY_NOT_FOUND},
        },
        "example_call": {"path": {"country_id": "AU"}, "query": {"limit": 3}},
    },
    {
        "key": "head_country_states",
        "slug": "check-the-states-of-a-country",
        "title": "Check the states of a country",
        "method": "HEAD",
        "path": BASE + "/{country_id}/states",
        "summary": "Returns the headers of a country's state list, including its `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [List the states of a country](" + LIST_STATES_PAGE + ") returns for that country when you send no query parameters.",
        "parameters": [COUNTRY_ID],
        "responses": {
            "200": {"description": "Headers only, including the state list's `ETag`. No body."},
            "304": NOT_MODIFIED,
        },
        "example_call": {"path": {"country_id": "AU"}},
    },
    {
        "key": "get_country_state",
        "slug": "retrieve-a-state",
        "title": "Retrieve a state",
        "method": "GET",
        "path": BASE + "/{country_id}/states/{state_id}",
        "summary": "Returns one state of a country, with the country's `id`, `code` and `name`.",
        "description": "Returns the state under the `state` key, with the same five fields a state listing row has: `id`, `code`, `name`, `active` and `default`. The country's `id`, `code` and `name` come in `country`, next to `state`. `VIC`, `vic`, `Victoria` and the state's `id` all return the same body and the same `ETag`. A query parameter you add is ignored.",
        "parameters": [COUNTRY_ID, STATE_ID],
        "responses": {
            "200": {
                "description": "The country's `id`, `code` and `name` in `country`, and the state in `state`. The response has an `ETag` header and `Cache-Control: private, no-cache`.",
                "schema": {"type": "object", "properties": {"country": REFERENCE_REF, "state": STATE_REF}},
                "example": {"country": AUSTRALIA_REFERENCE, "state": VICTORIA},
            },
            "304": NOT_MODIFIED,
            "404": {"description": "The country in `country_id` has no state with that `state_id` as its `id`, `code` or `name`. A state that belongs to another country returns this too. The message is `State not found`.", "schema": ERROR_REF, "example": STATE_NOT_FOUND},
        },
        "example_call": {"path": {"country_id": "AU", "state_id": "VIC"}},
    },
    {
        "key": "head_country_state",
        "slug": "check-a-state",
        "title": "Check a state",
        "method": "HEAD",
        "path": BASE + "/{country_id}/states/{state_id}",
        "summary": "Returns the headers of one state, including its `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [Retrieve a state](" + RETRIEVE_STATE_PAGE + ") returns for that state.",
        "parameters": [COUNTRY_ID, STATE_ID],
        "responses": {
            "200": {"description": "Headers only, including the state's `ETag`. No body."},
            "304": NOT_MODIFIED,
        },
        "example_call": {"path": {"country_id": "AU", "state_id": "VIC"}},
    },
]

SCHEMAS = {
    "Country": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The country's numeric `id`. Pass it, the `code` or the `name` as `country_id` in a path."},
        "code": {"type": "string", "description": "The country's code: two upper-case letters, such as `AU`."},
        "name": {"type": "string", "description": "The country's name, such as `Australia`."},
        "state_count": {"type": "integer", "description": "How many states the country has. It equals `pagination.total` from [List the states of a country](" + LIST_STATES_PAGE + ")."},
        "active": {"type": "boolean", "description": "Whether the country is active."},
        "default": {"type": "boolean", "description": "`true` only on the store's default country, the `default_country` in the `administration` site settings section."},
    }},
    "CountryReference": {"type": "object", "description": "The country a state list or a state belongs to.", "properties": {
        "id": {"type": "integer", "description": "The country's numeric `id`."},
        "code": {"type": "string", "description": "The country's two-letter code."},
        "name": {"type": "string", "description": "The country's name."},
    }},
    "CountryState": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The state's numeric `id`. It is unique across all countries. Pass it, the `code` or the `name` as `state_id` in a path."},
        "code": {"type": "string", "description": "The state's code, such as `VIC`."},
        "name": {"type": "string", "description": "The state's name, such as `Victoria`."},
        "active": {"type": "boolean", "description": "Whether the state is active."},
        "default": {"type": "boolean", "description": "`true` only on the store's default state, the `default_state` in the `administration` site settings section. `false` on every other state of every country."},
    }},
    "CountryPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of rows that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`. With `limit=all`, the number of rows returned."},
        "offset": {"type": "integer", "description": "The number of rows skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
    }},
    "CountryError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What went wrong, such as `Country not found` or `1 parameter failed validation.`."},
        "details": {"type": "array", "description": "One entry per rejected query parameter. Empty on a `404` or a `405`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter that was rejected."},
            "code": {"type": "string", "description": "Why the parameter was rejected, such as `out_of_range`, `invalid_enum` or `unsupported_parameter`."},
            "message": {"type": "string", "description": "What the parameter accepts, such as `must be true or false`."},
            "value": {"description": "The value you sent."},
        }}},
        "request_id": {"type": "string", "description": "A 36-character identifier for this request."},
    }}}},
}
