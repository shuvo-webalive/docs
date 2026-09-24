"""The Tax profiles endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Tax profiles"
SLUG = "tax-profiles"
BASE = "/admin/tax_profiles"
ICON = "percent"

OVERVIEW_DESCRIPTION = "List, create, update and delete tax profiles, and choose which profile is the store's default."
INTRO = "The Tax profiles API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax_profiles`."

RETRIEVE_PAGE = "/api-reference/tax-profiles/retrieve-a-tax-profile"
UPDATE_PAGE = "/api-reference/tax-profiles/update-a-tax-profile"
TAX_SETTINGS_PAGE = "/api-reference/tax-settings/get-tax-settings"
CUSTOM_PROFILES_PAGE = "/custom-tax-profiles"

WARNING = (
    "**When a tax request is rejected, the next request on the same connection can fail too.** Straight after\n"
    "  a `404`, the next retrieve returns `404`, even for a tax profile that exists, and a `DELETE` returns that\n"
    "  `404` and deletes nothing. Straight after a `400` `invalid_pagination`, the next listing returns the same\n"
    "  `400`, even on another tax collection. The request after that one is handled normally. If a call returns\n"
    "  an error you did not expect, read the tax profile back to see whether the change took effect before you\n"
    "  send the call again."
)

NOTES = [
    "**Create and update wrap the profile in `tax_profile`.** Send `{\"tax_profile\": {\"name\": \"Wholesale\"}}`.\n"
    "  A bare record is rejected with `400` (`tax_profile missing`). On create, a `tax_profile` with no\n"
    "  `name` is rejected with `500`, and so is one with an `id` field.",
    "**At most one profile is the default, and you move the flag rather than clear it.** Send `default: true`\n"
    "  in [Update a tax profile](" + UPDATE_PAGE + ") to make a profile the default. The profile that had the\n"
    "  flag loses it, and `default_tax_profile` in the [tax settings](" + TAX_SETTINGS_PAGE + ") changes to\n"
    "  this profile's `id`. `default: false` returns `200` and leaves the flag on. Deleting the default\n"
    "  profile leaves `default_tax_profile` holding the deleted profile's `id`.",
    "**A listing returns at most 20 profiles per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get every profile, step `offset` by the number of profiles each\n"
    "  page returned until you reach `pagination.total`.",
    "**A `200` does not prove that a write took effect.** A method these paths have no handler for, such as\n"
    "  `OPTIONS`, returns `200` with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and stores\n"
    "  nothing. Use `PUT` to update a profile, and read the profile back to confirm the change.",
    "**Tax profiles are not custom tax profiles.** [Custom tax profiles](" + CUSTOM_PROFILES_PAGE + ") live at\n"
    "  `/api/v4/admin/tax/custom_profiles`, a different collection with a similar name.",
]

TAX_PROFILE_ID = {
    "name": "tax_profile_id",
    "in": "path",
    "required": True,
    "description": "The tax profile's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 2},
}

LIMIT = {"name": "limit", "in": "query", "description": "The number of profiles to return. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. A value below `1`, or one that is not a number, is rejected with `400` (`invalid_pagination`).", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of profiles to skip. A value that is not a number is rejected with `400` (`invalid_pagination`).", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the `limit` you send with it.", "schema": {"type": "integer", "example": 1}}
Q = {"name": "q", "in": "query", "description": "Ignored. Sending `q` does not filter the listing.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Ignored. `field_metadata=true` adds no field descriptions to the response.", "schema": {"type": "boolean"}}

ERROR_REF = {"$ref": "#/components/schemas/TaxProfileError"}
ROW_REF = {"$ref": "#/components/schemas/TaxProfile"}
WRITE_BODY = {"type": "object", "required": ["tax_profile"], "properties": {"tax_profile": {"$ref": "#/components/schemas/TaxProfileInput"}}}
ROW_RESPONSE = {"type": "object", "properties": {"tax_profile": ROW_REF}}

SAMPLE_ROWS = [
    {"id": 1, "name": "Standard", "description": "Standard rate for retail customers", "default": True,
     "created_at": "2026-03-02T09:30:00", "updated_at": "2026-03-02T09:30:00"},
    {"id": 2, "name": "Tax exempt", "description": "Profile for tax-exempt customers", "default": False,
     "created_at": "2026-03-02T09:32:00", "updated_at": "2026-05-18T14:05:00"},
    {"id": 3, "name": "Export", "description": "Profile for orders shipped overseas", "default": False,
     "created_at": "2026-04-11T11:20:00", "updated_at": "2026-04-11T11:20:00"},
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

CREATED_ROW = {"id": 4, "name": "Wholesale", "description": "Profile for wholesale customers", "default": False,
               "created_at": "2026-09-22T10:15:00", "updated_at": "2026-09-22T10:15:00"}
UPDATED_ROW = dict(CREATED_ROW, name="Wholesale AU", updated_at="2026-09-22T10:20:00")

WRAPPER_400 = "The body is not wrapped in `tax_profile` (`tax_profile missing`)."

ENDPOINTS = [
    {
        "key": "list_tax_profiles",
        "slug": "list-tax-profiles",
        "title": "List tax profiles",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 tax profiles per call, and a `pagination` object with the total count.",
        "description": "Returns the tax profiles under `tax_profiles`, up to 20 per call, and a `pagination` object with the `total` number of profiles. Each profile has the same six fields that [Retrieve a tax profile](" + RETRIEVE_PAGE + ") returns, and at most one has `default` set to `true`. A `limit` above `20` does not return more. To get every profile, step `offset` by the number of profiles each page returned until you reach `pagination.total`.",
        "parameters": [LIMIT, OFFSET, PAGE, Q, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "Up to 20 tax profiles under `tax_profiles`, and `pagination`, which gives the `total` number of profiles and this page's `offset`.",
                "schema": {"$ref": "#/components/schemas/TaxProfilePage"},
                "example": {"tax_profiles": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is below `1`, or `limit` or `offset` is not a number (`invalid_pagination`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_tax_profiles",
        "slug": "check-the-tax-profiles-list",
        "title": "Check the tax profiles list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the tax profiles list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. Neither this response nor the listing has an `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_tax_profile",
        "slug": "create-a-tax-profile",
        "title": "Create a tax profile",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a tax profile and returns it with its `id`, which other calls take as `tax_profile_id`.",
        "description": "Creates a tax profile and returns it with the `id` the store assigned, which the other calls take as `tax_profile_id`. Wrap the profile in `tax_profile`, with a required `name` and an optional `description`. The store sets `created_at` and `updated_at` itself: it ignores a `created_at` you send and drops fields it does not know. Do not put an `id` field in `tax_profile`: it is rejected with `500`, so remove the profile's `id` before you send back a profile you read.",
        "body": {"schema": WRITE_BODY, "example": {"tax_profile": {"name": "Wholesale", "description": "Profile for wholesale customers"}}},
        "responses": {
            "201": {
                "description": "The new tax profile, with its `id`.",
                "schema": ROW_RESPONSE,
                "example": {"tax_profile": CREATED_ROW},
            },
            "400": {"description": WRAPPER_400, "schema": ERROR_REF},
            "500": {
                "description": "The `tax_profile` object has no `name`, or it has an `id` field. With an `id` field, the response contains `No signature of method: java.lang.Integer.toLong()`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_tax_profile",
        "slug": "retrieve-a-tax-profile",
        "title": "Retrieve a tax profile",
        "method": "GET",
        "path": BASE + "/{tax_profile_id}",
        "summary": "Returns the tax profile whose `id` you pass as `tax_profile_id`.",
        "description": "Returns one tax profile under the `tax_profile` key, with the same six fields a listing row has: `id`, `name`, `description`, `default`, `created_at` and `updated_at`. When no tax profile has that `tax_profile_id`, it returns `404` with `Profile not found`.",
        "parameters": [TAX_PROFILE_ID],
        "responses": {
            "200": {
                "description": "The tax profile.",
                "schema": ROW_RESPONSE,
                "example": {"tax_profile": SAMPLE_ROWS[1]},
            },
            "404": {"description": "No tax profile has that `tax_profile_id` (`Profile not found`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"tax_profile_id": 2}},
    },
    {
        "key": "head_tax_profile",
        "slug": "check-a-tax-profile",
        "title": "Check a tax profile",
        "method": "HEAD",
        "path": BASE + "/{tax_profile_id}",
        "summary": "Returns headers only, and `200` even when no tax profile has that `tax_profile_id`.",
        "description": "Returns `200` with headers only and no body, and no `ETag` or `Last-Modified` header. It returns `200` even when no tax profile has that `tax_profile_id`, so it does not tell you whether the profile exists. To check that, use [Retrieve a tax profile](" + RETRIEVE_PAGE + "), which returns `404` when no tax profile has it.",
        "parameters": [TAX_PROFILE_ID],
        "responses": {
            "200": {"description": "Headers only, no body. Returned even when no tax profile has that `tax_profile_id`."},
        },
        "example_call": {"path": {"tax_profile_id": 2}},
    },
    {
        "key": "update_tax_profile",
        "slug": "update-a-tax-profile",
        "title": "Update a tax profile",
        "method": "PUT",
        "path": BASE + "/{tax_profile_id}",
        "summary": "Changes the fields you send and returns the updated tax profile.",
        "description": "Changes the fields you send, wrapped in `tax_profile`, and returns the whole tax profile. A field you leave out keeps its value. Sending `default: true` makes this profile the default, takes the flag from the profile that had it, and sets `default_tax_profile` in the tax settings to this profile's `id`. Sending `default: false` returns `200` and leaves the flag on, so to move the default, set it on another profile.",
        "parameters": [TAX_PROFILE_ID],
        "body": {"schema": WRITE_BODY, "example": {"tax_profile": {"name": "Wholesale AU"}}},
        "responses": {
            "200": {
                "description": "The tax profile after the change.",
                "schema": ROW_RESPONSE,
                "example": {"tax_profile": UPDATED_ROW},
            },
            "400": {"description": WRAPPER_400, "schema": ERROR_REF},
        },
        "example_call": {"path": {"tax_profile_id": 4}},
    },
    {
        "key": "delete_tax_profile",
        "slug": "delete-a-tax-profile",
        "title": "Delete a tax profile",
        "method": "DELETE",
        "path": BASE + "/{tax_profile_id}",
        "summary": "Deletes a tax profile permanently. The default profile can be deleted too.",
        "description": "Deletes the tax profile permanently and returns `204` with no body. Retrieving it afterwards returns `404` with `Profile not found`. The default profile is deleted like any other, and `default_tax_profile` in the tax settings then still holds the deleted profile's `id`. To keep a default, first make another profile the default with [Update a tax profile](" + UPDATE_PAGE + ").",
        "parameters": [TAX_PROFILE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {
                "description": "The request just before this one to a tax endpoint was rejected with `404`. This call returns that same `404` and deletes nothing. Send the delete again.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"tax_profile_id": 4}},
    },
]

SCHEMAS = {
    "TaxProfile": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The tax profile's `id`, assigned by the store. The other calls take it as `tax_profile_id`."},
        "name": {"type": "string", "description": "The tax profile's name."},
        "description": {"type": "string", "description": "The tax profile's description."},
        "default": {"type": "boolean", "description": "`true` on at most one profile, the store's default. Updating another profile with `default: true` moves the flag there."},
        "created_at": {"type": "string", "description": "Set by the store when the profile is created. A `created_at` you send is ignored."},
        "updated_at": {"type": "string", "description": "Set by the store."},
    }},
    "TaxProfileInput": {"type": "object", "properties": {
        "name": {"type": "string", "description": "Required on create. On an update, send it only to rename the profile."},
        "description": {"type": "string", "description": "Optional. On an update, send it only to change it."},
        "default": {"type": "boolean", "description": "On an update, `true` makes this profile the default and takes the flag from the profile that had it. `false` leaves the flag as it is."},
    }},
    "TaxProfilePage": {"type": "object", "properties": {
        "tax_profiles": {"type": "array", "items": ROW_REF, "description": "Up to 20 tax profiles."},
        "pagination": {"$ref": "#/components/schemas/TaxProfilePagination"},
    }},
    "TaxProfilePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of tax profiles in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied: the `limit` you sent, or `20` when you sent none or more than `20`."},
        "offset": {"type": "integer", "description": "The number of profiles skipped before this page."},
        "count": {"type": "integer", "description": "The number of profiles on this page."},
        "current_page": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "A link to the previous page, or `null` when there is none."},
        "next_page": {"type": ["string", "null"], "description": "A link to the next page, or `null` when there is none. Check `has_next` before you request it."},
    }},
    "TaxProfileError": {"type": "object", "description": "The body of a rejected request. Each error response on these pages gives the message it contains, such as `Profile not found` or `tax_profile missing`."},
}
