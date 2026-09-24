"""The Tax codes endpoints, written from the SDKs' ENDPOINTS.md."""

TAG = "Tax codes"
SLUG = "tax-codes"
BASE = "/admin/tax_codes"
ICON = "percent"

RETRIEVE_PAGE = "/api-reference/tax-codes/retrieve-a-tax-code"
UPDATE_PAGE = "/api-reference/tax-codes/update-a-tax-code"

OVERVIEW_DESCRIPTION = "List, create, retrieve, update and delete your store's tax codes."
INTRO = "The Tax codes API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax_codes`."

WARNING = (
    "**An update sets `priority` to `0` and `resolver_type` to `flat` when you leave them out.**\n"
    "  `name`, `label`, `description` and `rate` keep their stored values when you leave them out,\n"
    "  but these two do not. Send the tax code's current `priority` and `resolver_type` in every\n"
    "  [update](" + UPDATE_PAGE + "), even when you only change its name."
)

NOTES = [
    "**Every write wraps the tax code in `tax_code`.** Send `{\"tax_code\": {\"name\": \"LUXURY\", \"rate\": 15.0}}`\n"
    "  to create a tax code. A bare record, or the plural `tax_codes` key, is rejected with `400` and\n"
    "  the message `tax_code missing`. `name` is the only field a create requires: a create without\n"
    "  it is rejected with `500`, not `400`.",
    "**`default` is read-only, and more than one tax code can have it.** `default: true` marks a tax\n"
    "  code the store built. A create or an update that sends `default: true` stores `false`.",
    "**A listing returns at most 20 tax codes per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get every tax code, raise `offset` by the number of tax codes\n"
    "  each page returned until you reach `pagination.total`. `q` and `field_metadata` are accepted\n"
    "  and ignored: `q` does not filter the listing, and `field_metadata` returns no field descriptions.",
    "**A rejected request can make the next request on the same connection fail too.** Straight after\n"
    "  a `404`, the next retrieve returns `404`, even for a tax code that exists. A retrieve from another\n"
    "  tax collection returns `404` with that collection's own message, such as `Profile not found`.\n"
    "  Straight after a `400` `invalid_pagination`, the next listing returns the same `400`, even on\n"
    "  another tax collection. The request after that works normally. A delete sent straight after a\n"
    "  `404` returns that `404` and deletes nothing, so retrieve the tax code afterwards to confirm it is\n"
    "  gone.",
    "**A `200` does not prove that a call did anything.** `PATCH` on a tax code, `POST` to a tax\n"
    "  code's path and `OPTIONS` on the list return `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and change nothing. A `HEAD` returns\n"
    "  `200` even when no tax code has the `tax_code_id` you send. Use `PUT` to update a tax code, and\n"
    "  [Retrieve a tax code](" + RETRIEVE_PAGE + ") to check that one exists.",
]

TAX_CODE_ID = {
    "name": "tax_code_id",
    "in": "path",
    "required": True,
    "description": "The tax code's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 105},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rows per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. A value below `1`, or one that is not a number, is rejected with `400` `invalid_pagination`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rows to skip. A value that is not a number is rejected with `400` `invalid_pagination`.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the `limit` you send with it.", "schema": {"type": "integer", "example": 1}}
QUERY = {"name": "q", "in": "query", "description": "Accepted and ignored: the listing is not filtered.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: the rows are the same with or without it, and no field descriptions are returned.", "schema": {"type": "boolean"}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("TaxCodeError")
ROW_RESPONSE = {"type": "object", "properties": {"tax_code": ref("TaxCode")}}
WRITE_BODY = {"type": "object", "required": ["tax_code"], "properties": {"tax_code": ref("TaxCodeInput")}}

SAMPLE_ROWS = [
    {"id": 1, "name": "STANDARD", "label": "Standard rate", "description": "Standard rate for most goods", "rate": 10.0, "resolver_type": "flat", "priority": 0, "default": True},
    {"id": 2, "name": "REDUCED", "label": "Reduced rate", "description": "Reduced rate for essential goods", "rate": 5.0, "resolver_type": "flat", "priority": 0, "default": True},
    {"id": 3, "name": "ZERO", "label": "Zero rate", "description": "Goods with no tax", "rate": 0.0, "resolver_type": "flat", "priority": 0, "default": True},
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

CREATED_ROW = {"id": 105, "name": "LUXURY", "label": "Luxury goods", "description": "Higher rate for luxury goods", "rate": 15.0, "resolver_type": "flat", "priority": 1, "default": False}
UPDATED_ROW = dict(CREATED_ROW, label="Luxury items")

WRAPPER_400 = "The body is not wrapped in `tax_code`. A bare record, or one wrapped in the plural `tax_codes`, is rejected with the message `tax_code missing`."

ENDPOINTS = [
    {
        "key": "list_tax_codes",
        "slug": "list-tax-codes",
        "title": "List tax codes",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 tax codes per call, and how many the store has in `pagination.total`.",
        "description": "Returns the store's tax codes under `tax_codes`, up to 20 per call, with a `pagination` block. Each tax code has the same eight fields that [Retrieve a tax code](" + RETRIEVE_PAGE + ") returns. A larger `limit` still returns 20, so to get every tax code, raise `offset` by the number of tax codes each page returned until you reach `pagination.total`. `q` and `field_metadata` are accepted and ignored.",
        "parameters": [LIMIT, OFFSET, PAGE, QUERY, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "A page of tax codes and the `pagination` block. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "tax_codes": {"type": "array", "items": ref("TaxCode")},
                    "pagination": ref("TaxCodePagination"),
                }},
                "example": {"tax_codes": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is below `1`, or `limit` or `offset` is not a number. The error is `invalid_pagination`, and its `errors` list names the parameter. After this rejection, the next listing you send on the same connection returns the same `400`, even from another tax collection; the request after that is handled normally.",
                "schema": ERROR,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_tax_codes",
        "slug": "check-the-tax-codes-list",
        "title": "Check the tax codes list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the tax codes list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. A `200` tells you only that the path is reachable. Neither this response nor the listing has an `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_tax_code",
        "slug": "create-a-tax-code",
        "title": "Create a tax code",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a tax code and returns it with its `id`, which other calls take as `tax_code_id`.",
        "description": "Creates a tax code and returns it with the `id` the store assigned. Pass that `id` as `tax_code_id` to retrieve, update or delete the tax code. Wrap the fields in `tax_code`; `name` is the only required field. The store ignores a tax code `id`, a `default` or an unknown field inside `tax_code`, and stores `resolver_type` exactly as you send it, without checking the value.",
        "body": {"schema": WRITE_BODY, "example": {"tax_code": {"name": "LUXURY", "label": "Luxury goods", "description": "Higher rate for luxury goods", "rate": 15.0, "resolver_type": "flat", "priority": 1}}},
        "responses": {
            "201": {
                "description": "The new tax code, under `tax_code`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"tax_code": CREATED_ROW},
            },
            "400": {"description": WRAPPER_400, "schema": ERROR},
            "500": {"description": "The body has no `name`. The store rejects a create without a `name` with `500`, not `400`.", "schema": ERROR},
        },
        "example_call": {},
    },
    {
        "key": "get_tax_code",
        "slug": "retrieve-a-tax-code",
        "title": "Retrieve a tax code",
        "method": "GET",
        "path": BASE + "/{tax_code_id}",
        "summary": "Returns the tax code whose `id` you pass as `tax_code_id`.",
        "description": "Returns one tax code under the `tax_code` key, with the same eight fields a listing row has: `id`, `name`, `label`, `description`, `rate`, `resolver_type`, `priority` and `default`. The response has no `ETag` or `Last-Modified` header.",
        "parameters": [TAX_CODE_ID],
        "responses": {
            "200": {
                "description": "The tax code.",
                "schema": ROW_RESPONSE,
                "example": {"tax_code": SAMPLE_ROWS[1]},
            },
            "404": {"description": "No tax code has that `tax_code_id`. The message is `Tax code not found`.", "schema": ERROR},
        },
        "example_call": {"path": {"tax_code_id": 2}},
    },
    {
        "key": "head_tax_code",
        "slug": "check-a-tax-code",
        "title": "Check a tax code",
        "method": "HEAD",
        "path": BASE + "/{tax_code_id}",
        "summary": "Returns headers only, with `200` even when no tax code has the `tax_code_id` you send.",
        "description": "Returns `200` with headers only and no body. It returns `200` even when no tax code has the `tax_code_id` you send, or when `tax_code_id` is not a number, so it does not tell you whether the tax code exists. To check that, use [Retrieve a tax code](" + RETRIEVE_PAGE + "), which returns `404` when no tax code has that `tax_code_id`.",
        "parameters": [TAX_CODE_ID],
        "responses": {
            "200": {"description": "Headers only, no body, and no `ETag` or `Last-Modified` header. Returned even when no tax code has the `tax_code_id` you send."},
        },
        "example_call": {"path": {"tax_code_id": 2}},
    },
    {
        "key": "update_tax_code",
        "slug": "update-a-tax-code",
        "title": "Update a tax code",
        "method": "PUT",
        "path": BASE + "/{tax_code_id}",
        "summary": "Changes a tax code and returns it. Send `priority` and `resolver_type` every time.",
        "description": "Changes the fields you send and returns the tax code. Wrap the fields in `tax_code`; you can leave out `name`. `name`, `label`, `description` and `rate` keep their stored values when you leave them out, but `priority` is set to `0` and `resolver_type` to `flat`, so send both in every update. A `default: true` in the body is stored as `false`.",
        "parameters": [TAX_CODE_ID],
        "body": {"schema": WRITE_BODY, "example": {"tax_code": {"label": "Luxury items", "priority": 1, "resolver_type": "flat"}}},
        "responses": {
            "200": {
                "description": "The updated tax code.",
                "schema": ROW_RESPONSE,
                "example": {"tax_code": UPDATED_ROW},
            },
            "400": {"description": WRAPPER_400, "schema": ERROR},
        },
        "example_call": {"path": {"tax_code_id": 105}},
    },
    {
        "key": "delete_tax_code",
        "slug": "delete-a-tax-code",
        "title": "Delete a tax code",
        "method": "DELETE",
        "path": BASE + "/{tax_code_id}",
        "summary": "Deletes a tax code permanently and returns `204` with no body.",
        "description": "Deletes the tax code permanently and returns `204` with no body. The tax code leaves the listing, and retrieving it returns `404`. If the request just before the delete was rejected, the delete returns that same rejection and deletes nothing, so retrieve the tax code afterwards to confirm it is gone.",
        "parameters": [TAX_CODE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No tax code has that `tax_code_id`. The message is `Code not found`. You also get a `404` when the request just before the delete returned one: the delete returns that earlier `404` and deletes nothing.", "schema": ERROR},
        },
        "example_call": {"path": {"tax_code_id": 105}},
    },
]

SCHEMAS = {
    "TaxCode": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The tax code's `id`, assigned by the store. Pass it as `tax_code_id` in a path. A create ignores any tax code `id` you send inside `tax_code`."},
        "name": {"type": "string", "description": "The tax code's name. Required when you create a tax code. An update that leaves it out keeps the stored name."},
        "label": {"type": ["string", "null"], "description": "The tax code's label, or `null` when the tax code has none. An update that leaves it out keeps the stored label."},
        "description": {"type": ["string", "null"], "description": "The tax code's description, or `null` when the tax code has none. An update that leaves it out keeps the stored description."},
        "rate": {"type": "number", "description": "The tax code's rate. An update that leaves it out keeps the stored rate."},
        "resolver_type": {"type": "string", "description": "The tax code's resolver type, such as `flat`. The store keeps any value you send without checking it. An update that leaves it out sets it to `flat`."},
        "priority": {"type": "integer", "description": "The tax code's priority. An update that leaves it out sets it to `0`."},
        "default": {"type": "boolean", "description": "`true` marks a tax code the store built. More than one tax code can have it. Read-only: a create or an update that sends `default: true` stores `false`."},
    }},
    "TaxCodeInput": {"type": "object", "description": "The fields you can write. A create needs `name`; an update can leave it out.", "properties": {
        "name": {"type": "string", "description": "Required when you create a tax code."},
        "label": {"type": "string"},
        "description": {"type": "string"},
        "rate": {"type": "number"},
        "resolver_type": {"type": "string", "description": "Stored exactly as you send it. An update that leaves it out sets it to `flat`."},
        "priority": {"type": "integer", "description": "An update that leaves it out sets it to `0`."},
    }},
    "TaxCodePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of tax codes in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of tax codes skipped before this page."},
        "count": {"type": "integer", "description": "The number of tax codes on this page."},
        "current_page": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "The URL of the previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The URL of the next page, or `null` on the last page."},
    }},
    "TaxCodeError": {"type": "object", "additionalProperties": True, "description": "What the store returns when it rejects a request.", "properties": {
        "errors": {"type": "array", "description": "On a `400` `invalid_pagination`, names the rejected parameter: `limit` or `offset`.", "items": {"type": "object"}},
    }},
}
