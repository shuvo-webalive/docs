"""The Custom tax profiles endpoints, written from the SDKs' ENDPOINTS.md."""

TAG = "Custom tax profiles"
SLUG = "custom-tax-profiles"
BASE = "/admin/tax/custom_profiles"
ICON = "file-invoice-dollar"

LIST_PAGE = "/api-reference/custom-tax-profiles/list-custom-tax-profiles"
RETRIEVE_PAGE = "/api-reference/custom-tax-profiles/retrieve-a-custom-tax-profile"

OVERVIEW_DESCRIPTION = "List, create, retrieve, replace and delete custom tax profiles, and read the rate rules each profile holds."
INTRO = "The Custom tax profiles API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax/custom_profiles`, and these profiles are separate from the tax profiles at `/api/v4/admin/tax_profiles`."

WARNING = (
    "**After a request is rejected, the store handles your next request on the same client with the rejected value.**\n"
    "  This applies to the id in the path, such as a `custom_profile_id`, and to a query parameter such as `limit`, and\n"
    "  it lasts for one request. After `GET /admin/tax/custom_profiles/99999999` returns `404`, your next\n"
    "  `GET /admin/tax/custom_profiles/1` also returns `404` with the message `Profile not found`, even though that\n"
    "  profile exists. After `limit=0` is rejected, your next listing call is rejected with the same message, even with\n"
    "  `limit=1`. A request that takes neither value runs normally. So after a rejected call, send one read, such as\n"
    "  [List custom tax profiles](" + LIST_PAGE + ") with `limit=1`, and ignore its response before your next write.\n"
    "  To confirm a write, read the profile back."
)

NOTES = [
    "**Every write wraps the profile in `custom_profile`.** Send\n"
    "  `{\"custom_profile\": {\"name\": \"Wholesale customers\", \"description\": \"Rates for wholesale accounts\"}}` to create\n"
    "  or replace a profile. A bare record, or the plural `custom_profiles` key, is rejected with `400` and the message\n"
    "  `custom_profile missing`.",
    "**An update sets `name` and `description` together, so send both.** A `PUT` without `name` is rejected with `400`\n"
    "  and the message `Profile name is required`. A `description` you leave out comes back `null`, so send the current\n"
    "  `description` again to keep it. The updates for tax profiles, tax rules and country taxes change only the fields\n"
    "  you send; this one does not.",
    "**You cannot set `code`.** Create and update accept a `code` and discard it, so a profile you create has `code`\n"
    "  set to `null`. Only a profile that already had a `code` in the store shows one.",
    "**A listing returns at most 20 profiles per call.** A larger `limit` is capped at `20`, and `pagination.limit` shows\n"
    "  `20`. To read every profile, raise `offset` by the number of rows each page returned until you reach\n"
    "  `pagination.total`. Only `limit`, `offset` and `page` change the listing; `q` and `field_metadata` are accepted\n"
    "  and ignored.",
    "**Some requests return `200` without doing anything.** A `HEAD` on one profile returns `200` whether or not a\n"
    "  profile has that `custom_profile_id`. Some methods these paths do not handle return `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` instead of `405`, and store nothing. Neither path sends\n"
    "  an `ETag` or `Last-Modified` header, so read the profile back to confirm a change.",
]

CUSTOM_PROFILE_ID = {
    "name": "custom_profile_id",
    "in": "path",
    "required": True,
    "description": "The custom tax profile's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 1},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rows per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rows to skip.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`. `limit=2&page=2` skips 2 rows.", "schema": {"type": "integer", "example": 1}}
SEARCH = {"name": "q", "in": "query", "description": "Accepted and ignored: it does not filter the listing.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: it adds nothing to the response.", "schema": {"type": "boolean"}}

REQUEST_ID = "5b2e8c1d-3f4a-4e6b-9c7d-1a2b3c4d5e6f"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Profile not found")
NAME_REQUIRED = error("invalid_request", "Profile name is required")

ERROR_REF = {"$ref": "#/components/schemas/TaxCustomProfileError"}
ROW_REF = {"$ref": "#/components/schemas/TaxCustomProfile"}
WRITE_BODY = {"type": "object", "required": ["custom_profile"], "properties": {"custom_profile": {"$ref": "#/components/schemas/TaxCustomProfileInput"}}}
ROW_RESPONSE = {"type": "object", "properties": {"custom_profile": ROW_REF}}

SAMPLE_RATE_RULE = {
    "id": 12,
    "name": "Wholesale rate",
    "description": "Rate for wholesale orders",
    "zones_count": 2,
    "transaction_no": None,
    "created_at": "2026-08-24T10:25:40",
    "updated_at": "2026-08-24T10:25:40",
}

SAMPLE_ROWS = [
    {
        "id": 1, "name": "Wholesale customers", "code": "WHOLESALE", "description": "Rates for wholesale accounts",
        "is_default": True, "rate_rules_count": 1, "transaction_no": None,
        "created_at": "2026-08-24T10:21:56", "updated_at": "2026-08-24T10:21:56",
    },
    {
        "id": 2, "name": "Export orders", "code": None, "description": None,
        "is_default": False, "rate_rules_count": 0, "transaction_no": None,
        "created_at": "2026-08-31T11:57:23", "updated_at": "2026-08-31T11:57:23",
    },
]

SAMPLE_DETAIL = {
    "id": 1, "name": "Wholesale customers", "code": "WHOLESALE", "description": "Rates for wholesale accounts",
    "is_default": True, "rate_rules_count": 1, "transaction_no": None,
    "created_at": "2026-08-24T10:21:56", "updated_at": "2026-08-24T10:21:56", "rate_rules": [SAMPLE_RATE_RULE],
}

SAMPLE_CREATED = {
    "id": 7, "name": "Wholesale customers", "code": None, "description": "Rates for wholesale accounts",
    "is_default": False, "rate_rules_count": 0, "transaction_no": None,
    "created_at": "2026-09-22T09:14:05", "updated_at": "2026-09-22T09:14:05",
}

SAMPLE_REPLACED = dict(SAMPLE_CREATED, name="Wholesale and trade customers", description="Rates for wholesale and trade accounts",
                       updated_at="2026-09-22T09:20:31")

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

WRITE_400_WRAPPER = "The body is not wrapped in `custom_profile`, for example a bare record or a body wrapped in the plural `custom_profiles`. The message is `custom_profile missing`."

ENDPOINTS = [
    {
        "key": "list_tax_custom_profiles",
        "slug": "list-custom-tax-profiles",
        "title": "List custom tax profiles",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 custom tax profiles per call, with the total in `pagination`.",
        "description": "Returns up to 20 custom tax profiles under `custom_profiles`, and a `pagination` object with the `total` number of profiles and `has_next`, which says whether more rows follow. Each row gives its number of rate rules in `rate_rules_count`; to get the rules themselves, use [Retrieve a custom tax profile](" + RETRIEVE_PAGE + "). Only `limit`, `offset` and `page` change the result; `q` and `field_metadata` are ignored. A `HEAD` or `OPTIONS` request on this path returns `404`.",
        "parameters": [LIMIT, OFFSET, PAGE, SEARCH, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "Up to 20 custom tax profiles under `custom_profiles`, each with nine fields, and `pagination` with the `total` number of profiles, the `offset` and `limit` of this page, and `has_next`.",
                "schema": {"type": "object", "properties": {
                    "custom_profiles": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/TaxCustomProfilePagination"},
                }},
                "example": {"custom_profiles": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "create_tax_custom_profile",
        "slug": "create-a-custom-tax-profile",
        "title": "Create a custom tax profile",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a custom tax profile and returns it; other calls take its `id` as `custom_profile_id`.",
        "description": "Creates a custom tax profile and returns it with the profile's `id`, which the other calls take as `custom_profile_id`. Wrap the record in `custom_profile`; `name` is required and `description` is optional. Any `code` you send is discarded, so the new profile's `code` is `null`. The response has the nine fields of a listing row, and a new profile holds no rate rules, so its `rate_rules_count` is `0`.",
        "body": {"schema": WRITE_BODY, "example": {"custom_profile": {"name": "Wholesale customers", "description": "Rates for wholesale accounts"}}},
        "responses": {
            "201": {
                "description": "The new custom tax profile. Its `id` is the `custom_profile_id` the other calls take.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_CREATED},
            },
            "400": {"description": WRITE_400_WRAPPER, "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_tax_custom_profile",
        "slug": "retrieve-a-custom-tax-profile",
        "title": "Retrieve a custom tax profile",
        "method": "GET",
        "path": BASE + "/{custom_profile_id}",
        "summary": "Returns the custom tax profile whose `id` you pass as `custom_profile_id`, with its rate rules.",
        "description": "Returns the profile whose `id` you pass as `custom_profile_id`, under the `custom_profile` key. It has the nine fields of a listing row plus `rate_rules`, the profile's rate rules, which is an empty list when the profile holds none. No other call returns `rate_rules`. A `HEAD` request on this path returns `200` whether or not a profile has that `custom_profile_id`, so use this call to check that a profile exists.",
        "parameters": [CUSTOM_PROFILE_ID],
        "responses": {
            "200": {
                "description": "The custom tax profile, with its `rate_rules`.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_DETAIL},
            },
            "404": {"description": "No custom tax profile has that `custom_profile_id`, including a profile you have deleted. The message is `Profile not found`.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"custom_profile_id": 1}},
    },
    {
        "key": "update_tax_custom_profile",
        "slug": "replace-a-custom-tax-profile",
        "title": "Replace a custom tax profile",
        "method": "PUT",
        "path": BASE + "/{custom_profile_id}",
        "summary": "Replaces a profile's `name` and `description`; a `description` you leave out becomes `null`.",
        "description": "Replaces the `name` and `description` of the profile whose `id` you pass as `custom_profile_id`, and returns the profile under `custom_profile` with the nine fields of a listing row. Wrap the record in `custom_profile` and send `name` every time, or the call is rejected with `400`. A `description` you leave out comes back `null`, so send the current `description` to keep it. Any `code` you send is discarded.",
        "parameters": [CUSTOM_PROFILE_ID],
        "body": {"schema": WRITE_BODY, "example": {"custom_profile": {"name": "Wholesale and trade customers", "description": "Rates for wholesale and trade accounts"}}},
        "responses": {
            "200": {
                "description": "The custom tax profile with its new `name` and `description`.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_REPLACED},
            },
            "400": {
                "description": "`name` is missing: `error.code` is `invalid_request` and the message is `Profile name is required`. Or the body is not wrapped in `custom_profile`, and the message is `custom_profile missing`.",
                "schema": ERROR_REF,
                "example": NAME_REQUIRED,
            },
        },
        "example_call": {"path": {"custom_profile_id": 7}},
    },
    {
        "key": "delete_tax_custom_profile",
        "slug": "delete-a-custom-tax-profile",
        "title": "Delete a custom tax profile",
        "method": "DELETE",
        "path": BASE + "/{custom_profile_id}",
        "summary": "Deletes a custom tax profile permanently. Returns `204` with no body.",
        "description": "Deletes the profile whose `id` you pass as `custom_profile_id` and returns `204` with no body. The profile leaves the listing, and retrieving it afterwards returns `404`. If the request just before this one on the same client was rejected with `404` for an id in its path that no record has, such as a `custom_profile_id` that no profile has, the store handles this call with that rejected value: it returns `404` and deletes nothing. Retrieve the profile afterwards to confirm it is gone.",
        "parameters": [CUSTOM_PROFILE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
        },
        "example_call": {"path": {"custom_profile_id": 7}},
    },
]

TIMESTAMP = {"type": "string"}

SCHEMAS = {
    "TaxCustomProfile": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The custom tax profile's `id`, assigned by the store. The other calls take it as `custom_profile_id`."},
        "name": {"type": "string", "description": "The profile's name. Required on every write."},
        "code": {"type": ["string", "null"], "description": "Read-only. Create and update discard any `code` you send, so a profile you create has `code` set to `null`. Only a profile that already had a `code` in the store shows one."},
        "description": {"type": ["string", "null"], "description": "The profile's description. `null` after an update that leaves it out."},
        "is_default": {"type": "boolean"},
        "rate_rules_count": {"type": "integer", "description": "The number of rate rules the profile holds. `0` on a new profile."},
        "transaction_no": {"type": ["string", "null"]},
        "created_at": dict(TIMESTAMP, description="When the profile was created."),
        "updated_at": dict(TIMESTAMP, description="When the profile was last changed."),
        "rate_rules": {"type": "array", "items": {"$ref": "#/components/schemas/TaxCustomProfileRateRule"}, "description": "Only when you retrieve one profile. The profile's rate rules, or an empty list when it holds none."},
    }},
    "TaxCustomProfileRateRule": {"type": "object", "description": "One rate rule a custom tax profile holds.", "properties": {
        "id": {"type": "integer", "description": "The rate rule's `id`."},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "zones_count": {"type": "integer", "description": "The number of zones the rate rule has."},
        "transaction_no": {"type": ["string", "null"]},
        "created_at": TIMESTAMP,
        "updated_at": TIMESTAMP,
    }},
    "TaxCustomProfileInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required on create and on update."},
        "description": {"type": "string", "description": "Optional. An update that leaves it out sets it to `null`."},
    }},
    "TaxCustomProfilePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of custom tax profiles in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of rows skipped before this page."},
        "count": {"type": "integer", "description": "The number of rows on this page."},
        "current_page": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` on the last page. Check `has_next` before you request it."},
    }},
    "TaxCustomProfileError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string"},
        "details": {"type": "array", "items": {"type": "object"}},
        "request_id": {"type": "string", "description": "The store's identifier for this request."},
    }}}},
}
