"""The Custom tax profiles endpoints, written from the SDKs' ENDPOINTS.md."""

TAG = "Custom tax profiles"
SLUG = "custom-tax-profiles"
BASE = "/admin/tax/custom-profiles"
ICON = "file-invoice-dollar"

LIST_PAGE = "/api-reference/custom-tax-profiles/list-custom-tax-profiles"
RETRIEVE_PAGE = "/api-reference/custom-tax-profiles/retrieve-a-custom-tax-profile"

OVERVIEW_DESCRIPTION = "List, create, retrieve, replace and delete custom tax profiles, and read the rules each profile holds."
INTRO = "The Custom tax profiles API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax/custom-profiles`, with a hyphen, and these profiles are separate from the tax profiles at `/api/v4/admin/tax_profiles`. The old path `/api/v4/admin/tax/custom_profiles`, with an underscore, returns `404` with the message `Unknown tax path`."

WARNING = (
    "**After the store rejects a request, it returns the same rejection to your next request on the same client.**\n"
    "  This happens once, on any tax path. After `GET /admin/tax/custom-profiles/99999999` returns `404`, your next\n"
    "  `GET /admin/tax/custom-profiles/1` also returns `404` with the message `Profile not found`, even though that\n"
    "  profile exists. The request after that runs normally, and a request from a new client is not affected. A\n"
    "  delete sent straight after a `404` returns that `404` and deletes nothing. So after a rejected call, send one\n"
    "  read, such as [List custom tax profiles](" + LIST_PAGE + ") with `limit=1`, and ignore its response before\n"
    "  your next write. To confirm a write, read the profile back."
)

NOTES = [
    "**Every write wraps the profile in `custom_profile`.** Send\n"
    "  `{\"custom_profile\": {\"name\": \"Wholesale customers\", \"description\": \"Rates for wholesale accounts\"}}` to create\n"
    "  or replace a profile. A bare record, or the plural `custom_profiles` key, is rejected with `400` and the message\n"
    "  `custom_profile missing`.",
    "**An update replaces `description` and `tax_code`, so send them every time.** A `description` or `tax_code` you\n"
    "  leave out comes back `null`, so send the current values again to keep them. A `name` you leave out keeps its\n"
    "  value, and an empty `name` is rejected with `400` and the message `Profile name is required`. The updates for\n"
    "  tax profiles, tax rules and country taxes change only the fields you send; this one does not.",
    "**Write `tax_code`, not `code`.** The create accepts a `code` and discards it, so `tax_code` stays `null`.\n"
    "  Send `tax_code` to set the profile's tax code.",
    "**You can file a create under a transaction number.** Send the number in an `X-Transaction-No` header, or as\n"
    "  `transaction_no` at the top level of the body, beside `custom_profile`. The SDKs send it as the header when you\n"
    "  pass `transaction_no` to the create. A `transaction_no` inside `custom_profile` is accepted and files nothing.\n"
    "  If the header and the body name different numbers, the header wins. No response returns the number.\n"
    "  `GET /api/v4/admin/transactions/{transaction_no}` then counts the profile under `custom_tax_profile`. A profile\n"
    "  keeps the first number it is filed under: an update with a number files only a profile that has none yet.",
    "**A listing returns up to 100 profiles per call, newest first.** A larger `limit` is cut to `100`, and\n"
    "  `pagination.limit` shows `100`. To read every profile, add `pagination.count` to `offset` after each page\n"
    "  until `offset` reaches `pagination.total`. `sort` takes `id` or `name`, and sorts in descending order either way.\n"
    "  `q`, `search` and `field_metadata` are accepted and ignored.",
    "**Row reads and updates return an `ETag`; the store never returns `304`.** Retrieve and update return an `ETag`\n"
    "  header. Send it as `If-Match` on an update, and the update is rejected with `409` if the profile changed since\n"
    "  you read it. The SDK functions send no `If-Match`. `If-None-Match` is ignored: a retrieve with the current\n"
    "  `ETag` still returns `200` and the full body. The listing and the create return no `ETag`.",
    "**There is no `HEAD` call for custom tax profiles.** `HEAD` and `OPTIONS` return `404` on the listing and on a\n"
    "  profile, whether or not a profile has that `custom_profile_id`. The profile path also accepts `PATCH`, which\n"
    "  changes only the fields you send and returns `200` with an `ETag`; the SDKs have no function for it. A request\n"
    "  the store has no handler for can return `200` with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}`\n"
    "  and store nothing, so read the profile back to confirm a change.",
]

CUSTOM_PROFILE_ID = {
    "name": "custom_profile_id",
    "in": "path",
    "required": True,
    "description": "The custom tax profile's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 1},
}

IF_MATCH = {
    "name": "If-Match",
    "in": "header",
    "description": "Optional. The profile's current `ETag`, from your last retrieve or update of it. If the profile changed since then, the update is rejected with `409`. The SDK functions do not send it.",
    "schema": {"type": "string", "example": "\"5d41402abc4b2a76b9719d911017c592\""},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "description": "Optional. A transaction number to file the new profile under. The SDKs send it when you pass `transaction_no` to the create. It wins over a different `transaction_no` in the body. No response returns it.",
    "schema": {"type": "string", "example": "TXN-IMPORT-0001"},
}

LIMIT = {"name": "limit", "in": "query", "description": "Custom tax profiles per page, from `1` to `100`. A larger value is cut to `100`, and `pagination.limit` shows `100`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of custom tax profiles to skip before this page.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`. `limit=2&page=2` skips 2 profiles.", "schema": {"type": "integer", "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "Sorts by `id` or `name`, in descending order either way. `order` and `direction` change nothing. Any other value is rejected with `400` and the message `unsupported sort '<value>'`.", "schema": {"type": "string", "enum": ["id", "name"], "example": "name"}}
SEARCH = {"name": "q", "in": "query", "description": "Accepted and ignored: it does not filter the listing. So is `search`.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: it adds nothing to the response.", "schema": {"type": "boolean"}}

REQUEST_ID = "5b2e8c1d-3f4a-4e6b-9c7d-1a2b3c4d5e6f"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Profile not found")
NAME_REQUIRED = error("invalid_request", "Profile name is required")
CREATE_NAME_REQUIRED = error("invalid_request", "name is required")
DELETE_NOT_FOUND = error("invalid_request", "Profile not found")

ERROR_REF = {"$ref": "#/components/schemas/TaxCustomProfileError"}
ROW_REF = {"$ref": "#/components/schemas/TaxCustomProfile"}
WRITE_BODY = {"type": "object", "required": ["custom_profile"], "properties": {
    "custom_profile": {"$ref": "#/components/schemas/TaxCustomProfileInput"},
    "transaction_no": {"type": "string", "description": "Optional. A transaction number to file the profile under. Send it here, beside `custom_profile`: inside `custom_profile` it files nothing. An `X-Transaction-No` header with a different number wins. On an update, it files only a profile that has no number yet."},
}}
ROW_RESPONSE = {"type": "object", "properties": {"custom_profile": ROW_REF}}

SAMPLE_RATE_RULE = {
    "id": 12,
    "name": "Wholesale rate",
    "description": "Rate for wholesale orders",
    "zones_count": 2,
    "profiles": [{"id": 1, "name": "Wholesale customers"}],
    "created_on": "2026-08-24T10:25:40Z",
    "last_updated_on": "2026-08-24T10:25:40Z",
}

SAMPLE_ROWS = [
    {
        "id": 2, "name": "Export orders", "tax_code": None, "description": None,
        "is_default": False, "rules_count": 0,
        "created_on": "2026-08-31T11:57:23Z", "last_updated_on": "2026-08-31T11:57:23Z",
    },
    {
        "id": 1, "name": "Wholesale customers", "tax_code": "WHOLESALE", "description": "Rates for wholesale accounts",
        "is_default": True, "rules_count": 1,
        "created_on": "2026-08-24T10:21:56Z", "last_updated_on": "2026-08-24T10:21:56Z",
    },
]

SAMPLE_DETAIL = dict(SAMPLE_ROWS[1], rules=[SAMPLE_RATE_RULE])

SAMPLE_CREATED = {
    "id": 7, "name": "Wholesale customers", "tax_code": None, "description": "Rates for wholesale accounts",
    "is_default": False, "rules_count": 0,
    "created_on": "2026-09-22T09:14:05Z", "last_updated_on": "2026-09-22T09:14:05Z",
}

SAMPLE_REPLACED = dict(SAMPLE_CREATED, name="Wholesale and trade customers", description="Rates for wholesale and trade accounts",
                       last_updated_on="2026-09-22T09:20:31Z")

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

SAMPLE_GROUP_META = {
    "custom_profile": {"kind": "resource", "writable": True, "href": "/api/v4/admin/tax/custom-profiles/{id}"},
    "rules": {"kind": "collection", "writable": True, "href": "/api/v4/admin/tax/custom-profiles/{id}/rules"},
}

WRITE_400_WRAPPER = "The body is not wrapped in `custom_profile`, for example a bare record or a body wrapped in the plural `custom_profiles`. The message is `custom_profile missing`."

ENDPOINTS = [
    {
        "key": "list_tax_custom_profiles",
        "slug": "list-custom-tax-profiles",
        "title": "List custom tax profiles",
        "method": "GET",
        "path": BASE,
        "summary": "Returns a page of up to 100 custom tax profiles under `custom_profiles`, newest first, and how many exist in `pagination.total`.",
        "description": "Returns your custom tax profiles under `custom_profiles`, newest first, up to `limit` per call with a maximum of `100`. You also get a `pagination` object with the `total` number of profiles and `has_next`, which says whether more profiles follow, and `group_meta`, which describes `custom_profile` and `rules` with a `kind`, a `writable` flag and an `href` each. Each profile gives its number of rules in `rules_count`; to get the rules themselves, use [Retrieve a custom tax profile](" + RETRIEVE_PAGE + "). Send `sort=name` to sort by name. `q`, `search` and `field_metadata` are accepted and ignored. The response has no `ETag`.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, SEARCH, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The custom tax profiles on this page under `custom_profiles`, each with eight fields, `group_meta`, and `pagination` with the `total` number of profiles, the `offset` and `limit` of this page, and `has_next`.",
                "schema": {"type": "object", "properties": {
                    "custom_profiles": {"type": "array", "items": ROW_REF},
                    "group_meta": {"$ref": "#/components/schemas/TaxCustomProfileGroupMeta"},
                    "pagination": {"$ref": "#/components/schemas/TaxCustomProfilePagination"},
                }},
                "example": {"custom_profiles": SAMPLE_ROWS, "group_meta": SAMPLE_GROUP_META, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is `0`: the message is `'limit' must be a positive integer`. Or `sort` is not `id` or `name`: the message is `unsupported sort '<value>'`.",
                "schema": ERROR_REF,
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
        "description": "Creates a custom tax profile and returns it with the profile's `id`, which the other calls take as `custom_profile_id`. Wrap the record in `custom_profile`; `name` is required, and `description` and `tax_code` are optional. Any `code` you send is discarded, and fields the store does not know are dropped. To file the profile under a transaction number, send an `X-Transaction-No` header, or `transaction_no` at the top level of the body beside `custom_profile`. A `transaction_no` inside `custom_profile` files nothing. The response has the eight fields of a listing row and no `ETag`. A new profile holds no rules, so its `rules_count` is `0`.",
        "parameters": [TRANSACTION_NO],
        "body": {"schema": WRITE_BODY, "example": {"custom_profile": {"name": "Wholesale customers", "description": "Rates for wholesale accounts"}, "transaction_no": "TXN-IMPORT-0001"}},
        "responses": {
            "201": {
                "description": "The new custom tax profile. Its `id` is the `custom_profile_id` the other calls take.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_CREATED},
            },
            "400": {
                "description": "`name` is missing: the code is `invalid_request` and the message is `name is required`. Or " + WRITE_400_WRAPPER[0].lower() + WRITE_400_WRAPPER[1:],
                "schema": ERROR_REF,
                "example": CREATE_NAME_REQUIRED,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_tax_custom_profile",
        "slug": "retrieve-a-custom-tax-profile",
        "title": "Retrieve a custom tax profile",
        "method": "GET",
        "path": BASE + "/{custom_profile_id}",
        "summary": "Returns the custom tax profile whose `id` you pass as `custom_profile_id`, with its rules and an `ETag`.",
        "description": "Returns the profile whose `id` you pass as `custom_profile_id`, under the `custom_profile` key. It has the eight fields of a listing row plus `rules`, the profile's rules, which is an empty list when the profile holds none. Each rule lists in `profiles` the `id` and `name` of every profile it is filed under. No other call returns `rules`. The response has an `ETag` header, which you can send as `If-Match` on an update. Sending it back in `If-None-Match` still returns `200` and the full body.",
        "parameters": [CUSTOM_PROFILE_ID],
        "responses": {
            "200": {
                "description": "The custom tax profile, with its `rules`. The response has an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_DETAIL},
            },
            "404": {"description": "No custom tax profile has that `custom_profile_id`, including a profile you have deleted. The code is `not_found` and the message is `Profile not found`.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"custom_profile_id": 1}},
    },
    {
        "key": "update_tax_custom_profile",
        "slug": "replace-a-custom-tax-profile",
        "title": "Replace a custom tax profile",
        "method": "PUT",
        "path": BASE + "/{custom_profile_id}",
        "summary": "Replaces a profile's `description` and `tax_code`, setting any you leave out to `null`, changes `name` only when you send it, and returns the profile.",
        "description": "Replaces the profile whose `id` you pass as `custom_profile_id`, and returns it under `custom_profile` with the eight fields of a listing row and an `ETag` header. Wrap the record in `custom_profile`. A `description` or `tax_code` you leave out comes back `null`, so send the current values to keep them. A `name` you leave out keeps its value, and an empty `name` is rejected with `400`. Send an `If-Match` header with the `ETag` from your last read if you want the update rejected with `409` when the profile changed since then. A `transaction_no` at the top level of the body, or in an `X-Transaction-No` header, files only a profile that has no number yet.",
        "parameters": [CUSTOM_PROFILE_ID, IF_MATCH],
        "body": {"schema": WRITE_BODY, "example": {"custom_profile": {"name": "Wholesale and trade customers", "description": "Rates for wholesale and trade accounts"}}},
        "responses": {
            "200": {
                "description": "The custom tax profile after the replace, without `rules`. The response has an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"custom_profile": SAMPLE_REPLACED},
            },
            "400": {
                "description": "`name` is empty: `error.code` is `invalid_request` and the message is `Profile name is required`. Or the body is not wrapped in `custom_profile`, and the message is `custom_profile missing`.",
                "schema": ERROR_REF,
                "example": NAME_REQUIRED,
            },
            "409": {
                "description": "Your `If-Match` value is not the profile's current `ETag`. The code is `conflict`.",
                "schema": ERROR_REF,
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
        "description": "Deletes the profile whose `id` you pass as `custom_profile_id` and returns `204` with no body. Retrieving it afterwards returns `404`. Deleting it again returns `400`, not `404`, with the code `invalid_request` and the message `Profile not found`. If the request just before this one on the same client was rejected with `404`, the store returns that `404` for the delete and deletes nothing. Retrieve the profile afterwards to confirm it is gone.",
        "parameters": [CUSTOM_PROFILE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "400": {"description": "You already deleted the profile. The code is `invalid_request` and the message is `Profile not found`.", "schema": ERROR_REF, "example": DELETE_NOT_FOUND},
            "404": {"description": "The request just before this one on the same client was rejected with `404`. The store returns that `404` again and deletes nothing. Retrieve the profile to see whether it still exists.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"custom_profile_id": 7}},
    },
]

TIMESTAMP = {"type": "string"}

SCHEMAS = {
    "TaxCustomProfile": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The custom tax profile's `id`, assigned by the store. The other calls take it as `custom_profile_id`."},
        "name": {"type": "string", "description": "The profile's name. Required on a create; an update that leaves it out keeps it."},
        "tax_code": {"type": ["string", "null"], "description": "The profile's tax code, or `null` when none is set. An update that leaves it out sets it to `null`. A `code` you send does not set it."},
        "description": {"type": ["string", "null"], "description": "The profile's description. `null` after an update that leaves it out."},
        "is_default": {"type": "boolean"},
        "rules_count": {"type": "integer", "description": "The number of rules the profile holds. `0` on a new profile."},
        "created_on": dict(TIMESTAMP, description="When the profile was created."),
        "last_updated_on": dict(TIMESTAMP, description="When the profile was last changed."),
        "rules": {"type": "array", "items": {"$ref": "#/components/schemas/TaxCustomProfileRateRule"}, "description": "Only when you retrieve one profile. The profile's rules, or an empty list when it holds none."},
    }},
    "TaxCustomProfileRateRule": {"type": "object", "description": "One rule a custom tax profile holds.", "properties": {
        "id": {"type": "integer", "description": "The rule's own `id`. No call on these pages takes it."},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "zones_count": {"type": "integer", "description": "The number of zones the rule has."},
        "profiles": {"type": "array", "items": {"$ref": "#/components/schemas/TaxCustomProfileReference"}, "description": "Every profile the rule is filed under."},
        "created_on": TIMESTAMP,
        "last_updated_on": TIMESTAMP,
    }},
    "TaxCustomProfileReference": {"type": "object", "description": "A profile a rule is filed under.", "properties": {
        "id": {"type": "integer", "description": "The profile's `id`, which the other calls take as `custom_profile_id`."},
        "name": {"type": "string", "description": "The profile's name."},
    }},
    "TaxCustomProfileInput": {"type": "object", "description": "The fields a create or an update can send, wrapped in `custom_profile`. `name` is required on a create. Send `transaction_no` beside `custom_profile`, not inside it.", "properties": {
        "name": {"type": "string", "description": "Required on a create. An update that leaves it out keeps the current name; an empty `name` is rejected with `400`."},
        "description": {"type": "string", "description": "Optional. An update that leaves it out sets it to `null`."},
        "tax_code": {"type": "string", "description": "Optional. An update that leaves it out sets it to `null`."},
        "is_default": {"type": "boolean"},
    }},
    "TaxCustomProfileResourceMeta": {"type": "object", "description": "One entry of `group_meta`.", "properties": {
        "kind": {"type": "string", "description": "`resource` for `custom_profile`, `collection` for `rules`."},
        "writable": {"type": "boolean", "description": "Whether the entry can be written."},
        "href": {"type": "string", "description": "The entry's path, with `{id}` standing for the `custom_profile_id`, such as `/api/v4/admin/tax/custom-profiles/{id}`."},
    }},
    "TaxCustomProfileGroupMeta": {"type": "object", "description": "Describes the profile and its rules. Only the listing returns it.", "properties": {
        "custom_profile": {"$ref": "#/components/schemas/TaxCustomProfileResourceMeta"},
        "rules": {"$ref": "#/components/schemas/TaxCustomProfileResourceMeta"},
    }},
    "TaxCustomProfilePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of custom tax profiles in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `100`."},
        "offset": {"type": "integer", "description": "The number of custom tax profiles skipped before this page."},
        "count": {"type": "integer", "description": "The number of custom tax profiles on this page."},
        "current_page": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` on the last page. Check `has_next` before you request it."},
    }},
    "TaxCustomProfileError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string"},
        "details": {"type": "array", "items": {"type": "object"}},
        "request_id": {"type": "string", "description": "The store's identifier for this request."},
    }}}},
}
