"""The Cities endpoints, written from the SDKs' ENDPOINTS.md and checked against a live store."""

TAG = "Cities"
SLUG = "cities"
BASE = "/app/cities"
ICON = "city"

OVERVIEW_DESCRIPTION = "Look up cities and their post codes, filtered by country, state, post code or part of the city name."
INTRO = "The Cities API has two endpoints, and you can call both from all seven SDKs. Both use the path `/api/v4/app/cities`."

LIST_PAGE = "/api-reference/cities/list-cities"
LIST_COUNTRIES_PAGE = "/api-reference/countries/list-countries"
LIST_STATES_PAGE = "/api-reference/countries/list-the-states-of-a-country"
SITE_SETTINGS_SECTION_PAGE = "/api-reference/site-settings/get-a-settings-section"

WARNING = (
    "**Send `country` with a state code.** `state=VIC` on its own is rejected with `400` and the detail code\n"
    "  `country_required`, because codes such as `WA` repeat across countries. Send `country=AU&state=VIC`, or send\n"
    "  the state's numeric `id`, such as `state=72`, which works without `country`. A state name such as `Victoria`\n"
    "  matches no cities."
)

NOTES = [
    "**You can only read cities.** `OPTIONS` on `/api/v4/app/cities` returns `204` with\n"
    "  `Allow: GET, HEAD, OPTIONS`, and `POST`, `PUT`, `PATCH` and `DELETE` are rejected with `405`. There is no path\n"
    "  for a single city: `GET /api/v4/app/cities/{city_id}` returns `404` with the error code `not_found`.",
    "**Take the `country` and `state` values from the Countries API.** A city's `country.id` is the country's `id`\n"
    "  from [List countries](" + LIST_COUNTRIES_PAGE + "), and its `state.id` is the state's `id` from\n"
    "  [List the states of a country](" + LIST_STATES_PAGE + ").",
    "**Older parameter names still work.** `max` is the same as `limit`, `countryId` as `country`, `stateId` as\n"
    "  `state`, `postCode` as `post_code`, and `searchText` and `name` as `search`. Send one name for each: a name\n"
    "  sent twice, or sent together with its other name, is rejected with `400` and the detail code\n"
    "  `duplicate_parameter`. `q`, `dir`, `page`, `field_metadata` and any other name the listing does not know\n"
    "  are ignored: you get `200` and the same cities as without them.",
    "**`state.default` follows the store's default state.** A state has `default` set to `true` while it is the\n"
    "  `default_state` in the `administration` section of the site settings, which you read with\n"
    "  [Get a settings section](" + SITE_SETTINGS_SECTION_PAGE + "). The default country does not filter the listing.",
    "**Every read returns an `ETag`.** Each `GET` and `HEAD` response has an `ETag` and\n"
    "  `Cache-Control: private, max-age=3600`. Send that `ETag` in `If-None-Match` on a `GET` or a `HEAD`, and while\n"
    "  it is still current you get `304` with no body. The SDK functions take no headers, so they never send\n"
    "  `If-None-Match`: you get `304` only from your own HTTP calls.",
    "**The cities list has a read limit.** You can make 20 calls within about 10 seconds, `GET` and `HEAD`\n"
    "  counted together. The next call is rejected with `429` and the error code `rate_limited`, and the\n"
    "  `Retry-After` header says how many seconds to wait.",
]

LIMIT = {"name": "limit", "in": "query", "description": "The number of cities per page, from `1` to `100`. Defaults to `100`. `pagination.limit` shows the page size applied. `0`, a negative value, a value above `100`, `all` and a value that is not a whole number are rejected with `400`. `max` is another name for `limit`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of cities to skip. Defaults to `0`. A negative value or a value that is not a whole number is rejected with `400`. An `offset` past the last city returns no cities, the full `total`, `has_previous` set to `true` and `has_next` set to `false`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
COUNTRY = {"name": "country", "in": "query", "description": "Keeps only cities in this country. Send the country's numeric `id` from [List countries](" + LIST_COUNTRIES_PAGE + ") or its two-letter `code` in any letter case, such as `12`, `AU` or `au`. A country name such as `Australia`, or other text, is rejected with `400`. A country with no cities, an `id` no country has and `0` all return no cities. `countryId` is another name for `country`.", "schema": {"type": "string", "example": "AU"}}
STATE = {"name": "state", "in": "query", "description": "Keeps only cities in this state. Send the state's numeric `id` from [List the states of a country](" + LIST_STATES_PAGE + "), such as `72`, or its `code` in any letter case, such as `VIC`, together with `country`. A code without `country` is rejected with `400`, and so is a number with a decimal point. An `id` no state has, a code the country does not have, and a state name all return no cities. `stateId` is another name for `state`.", "schema": {"type": "string", "example": "VIC"}}
POST_CODE = {"name": "post_code", "in": "query", "description": "Keeps only cities with exactly this post code. Surrounding spaces are trimmed. Part of a post code, such as `300`, returns no cities. A blank value applies no filter, and a value longer than 10 characters is rejected with `400`. `postCode` is another name for `post_code`.", "schema": {"type": "string", "maxLength": 10, "example": "3000"}}
SEARCH = {"name": "search", "in": "query", "description": "Keeps only cities whose `name` contains this text, in any letter case. It does not match post codes. `%` and `_` match only themselves. A blank value applies no filter. Broken percent-encoding, such as `%zz`, is rejected with `400`. `name` and `searchText` are other names for `search`.", "schema": {"type": "string", "example": "melb"}}
SORT = {"name": "sort", "in": "query", "description": "The order of the cities: `state`, `name` or `post_code`. Defaults to `state`, which sorts by state, then post code, then city name. `name` sorts by city name across all states, and `post_code` by post code. Any other value, such as `id` or `-name`, is rejected with `400`.", "schema": {"type": "string", "enum": ["state", "name", "post_code"], "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Defaults to `asc`. Any other value is rejected with `400`. `dir` is ignored.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "desc"}}

REQUEST_ID = "3d8f1a62-7b4c-4e19-9a05-c2e6b7d41f83"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


STATE_CODE_REJECTED = error("invalid_request", "1 parameter failed validation.", [
    {"field": "state", "code": "country_required", "message": "a state code needs country, because codes such as WA repeat across countries", "value": "VIC"},
])
RATE_LIMITED_EXAMPLE = error("rate_limited", "Too many reads to this resource — retry after 8s.")

ERROR_REF = {"$ref": "#/components/schemas/CityError"}
CITY_REF = {"$ref": "#/components/schemas/City"}
PAGINATION_REF = {"$ref": "#/components/schemas/CityPagination"}

VICTORIA = {"id": 72, "code": "VIC", "name": "Victoria", "active": True, "default": False}
AUSTRALIA = {"id": 12, "code": "AU", "name": "Australia"}

SAMPLE_CITIES = [
    {"id": 1001, "name": "Melbourne", "post_code": "3000", "state": VICTORIA, "country": AUSTRALIA},
    {"id": 1002, "name": "East Melbourne", "post_code": "3002", "state": VICTORIA, "country": AUSTRALIA},
]

CACHE_HEADERS = "The response has an `ETag` header and `Cache-Control: private, max-age=3600`."

LIST_400 = (
    "You sent a query parameter value the listing does not accept, such as `limit=101` or `state=VIC` without `country`. "
    "The `error.code` is `invalid_request`, and each rejected parameter has a `details` entry naming it in `field`, "
    "so `message` counts them, such as `2 parameters failed validation.`. "
    "The messages are `must be a whole number from 1 to 100` for `limit`, `must be 0 or more` for a negative `offset`, "
    "`must be a country id or a 2-letter ISO code` for `country`, "
    "`a state code needs country, because codes such as WA repeat across countries` for a state code without `country`, "
    "`must be at most 10 characters, as the address form` for `post_code`, "
    "`must be one of state, name, post_code` for `sort` and `must be asc or desc` for `order`. "
    "A parameter sent twice, or sent together with its other name, has the detail code `duplicate_parameter` and a message such as `send limit or max once`."
)
NOT_MODIFIED = {"description": "You sent the current `ETag` in `If-None-Match`. No body."}
RATE_LIMITED = {
    "description": "You made more than 20 calls to the cities list, `GET` and `HEAD` counted together, within about 10 seconds. The `error.code` is `rate_limited`, and the message starts with `Too many reads to this resource` and says how many seconds to wait. The `Retry-After` header gives the same number of seconds.",
    "schema": ERROR_REF,
    "example": RATE_LIMITED_EXAMPLE,
}

ENDPOINTS = [
    {
        "key": "list_cities",
        "slug": "list-cities",
        "title": "List cities",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 100 cities per call, sorted by state, post code and name.",
        "description": "Returns the cities in `cities`, 100 per call unless you send a smaller `limit`, sorted by state, then post code, then city name. Send `country` and `state` to keep only the cities of one country or state, `post_code` to find the cities with an exact post code, and `search` to match part of a city name; filters you send together must all match. Send `sort` and `order` to change the order. Each city includes its `state` and its `country`.",
        "parameters": [LIMIT, OFFSET, COUNTRY, STATE, POST_CODE, SEARCH, SORT, ORDER],
        "responses": {
            "200": {
                "description": "The cities on this page in `cities`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. " + CACHE_HEADERS,
                "schema": {"type": "object", "properties": {
                    "cities": {"type": "array", "items": CITY_REF},
                    "pagination": PAGINATION_REF,
                }},
                "example": {"cities": SAMPLE_CITIES, "pagination": {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}},
            },
            "304": NOT_MODIFIED,
            "400": {
                "description": LIST_400,
                "schema": ERROR_REF,
                "example": STATE_CODE_REJECTED,
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"query": {"country": "AU", "state": "VIC", "limit": 20}},
    },
    {
        "key": "head_cities",
        "slug": "check-the-cities-list",
        "title": "Check the cities list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers of the cities list, including its `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [List cities](" + LIST_PAGE + ") returns when you send no query parameters, and the SDK functions send none. Compare it with the `ETag` you saved to see whether the list changed without downloading it. It counts toward the same read limit as [List cities](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, including the list's `ETag` and `Cache-Control: private, max-age=3600`. No body."},
            "304": NOT_MODIFIED,
            "429": RATE_LIMITED,
        },
        "example_call": {},
    },
]

SCHEMAS = {
    "City": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The city's numeric `id`. No endpoint takes it as a path parameter."},
        "name": {"type": "string", "description": "The city's name, such as `Melbourne`."},
        "post_code": {"type": "string", "description": "The city's post code, such as `3000`."},
        "state": {"$ref": "#/components/schemas/CityState"},
        "country": {"$ref": "#/components/schemas/CityCountry"},
    }},
    "CityState": {"type": "object", "description": "The state the city is in.", "properties": {
        "id": {"type": "integer", "description": "The state's numeric `id`, the same `id` that [List the states of a country](" + LIST_STATES_PAGE + ") returns. Send it as `state` to filter the listing."},
        "code": {"type": "string", "description": "The state's code, such as `VIC`."},
        "name": {"type": "string", "description": "The state's name, such as `Victoria`."},
        "active": {"type": "boolean", "description": "Whether the state is active."},
        "default": {"type": "boolean", "description": "`true` while the state is the `default_state` in the `administration` site settings section, and `false` otherwise."},
    }},
    "CityCountry": {"type": "object", "description": "The country the city is in.", "properties": {
        "id": {"type": "integer", "description": "The country's numeric `id`, the same `id` that [List countries](" + LIST_COUNTRIES_PAGE + ") returns. Send it, or the `code`, as `country` to filter the listing."},
        "code": {"type": "string", "description": "The country's two-letter code, such as `AU`."},
        "name": {"type": "string", "description": "The country's name, such as `Australia`."},
    }},
    "CityPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of cities that match your filters, across all pages."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `100` when you sent none."},
        "offset": {"type": "integer", "description": "The number of cities skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is above `0`."},
        "has_next": {"type": "boolean", "description": "`true` when more cities follow this page."},
    }},
    "CityError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `rate_limited`."},
        "message": {"type": "string", "description": "What went wrong, such as `1 parameter failed validation.`."},
        "details": {"type": "array", "description": "One entry per rejected query parameter. Empty on a `404` or a `429`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter that was rejected, such as `limit`."},
            "code": {"type": "string", "description": "Why the parameter was rejected, such as `out_of_range`, `invalid_integer`, `invalid_value`, `country_required`, `too_long`, `invalid_enum` or `duplicate_parameter`."},
            "message": {"type": "string", "description": "What the parameter accepts, such as `must be a whole number from 1 to 100`."},
            "value": {"type": "string", "description": "The value you sent. For a parameter sent twice, both values separated by a comma, such as `1, 2`."},
        }}},
        "request_id": {"type": "string", "description": "A 36-character identifier for this request."},
    }}}},
}
