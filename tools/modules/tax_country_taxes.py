"""The Country taxes endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Country taxes"
SLUG = "country-taxes"
BASE = "/admin/tax/country-taxes"
ICON = "globe"

OVERVIEW_DESCRIPTION = "List, create, update and delete your store's country taxes, and read the state rules of each one."
INTRO = "The Country taxes API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax/country-taxes`, with a hyphen. The old path `/api/v4/admin/tax/country_taxes`, with an underscore, returns `404` with the message `Unknown tax path`."

RETRIEVE_PAGE = "/api-reference/country-taxes/retrieve-a-country-tax"

WARNING = (
    "**After the store rejects a request, it returns the same rejection to your next request on the same client.**\n"
    "  This happens once, on any tax path. After `GET /admin/tax/country-taxes/99999999` returns `404`, your next\n"
    "  request, such as `GET /admin/tax/country-taxes/4` or `GET /admin/tax/custom-profiles/1`, also returns that\n"
    "  `404`, even though the record exists. The request after that runs normally, and a request from a new client\n"
    "  is not affected. A delete sent straight after a `404` returns that `404` and removes nothing. Confirm a delete\n"
    "  by reading the country tax back with [Retrieve a country tax](" + RETRIEVE_PAGE + ")."
)

NOTES = [
    "**Wrap every create and update in `country_tax`, and send `country_code` when you create.** A bare\n"
    "  record, or the plural `country_taxes` key, is rejected with `400` and the message `country_tax missing`.\n"
    "  A create without `country_code`, or with a code no country has, is rejected with `400 invalid_request`\n"
    "  and the message `Invalid country_code`. The store fills `country` from `country_code`, and `tax_code`\n"
    "  too unless you send it, but no response includes `country_code` itself.",
    "**An update changes only the fields you send.** Fields you leave out keep their values, so you do not\n"
    "  send `country_code` again. A new `country_code` moves the country tax to that country, and\n"
    "  `\"tax_method\": \"no_tax\"` sets `tax_rate` to `0`.",
    "**You can file a create under a transaction number.** Send the number in an `X-Transaction-No` header,\n"
    "  or as `transaction_no` at the top level of the body, beside `country_tax`. The SDKs send it as the header\n"
    "  when you pass `transaction_no` to the create. A `transaction_no` inside `country_tax` is accepted and\n"
    "  files nothing. If the header and the body name different numbers, the header wins. No response returns\n"
    "  the number. `GET /api/v4/admin/transactions/{transaction_no}` then counts the country tax under\n"
    "  `country_tax`, until you delete it. An update with a number, in the header or beside `country_tax`, files\n"
    "  the country tax under the new number, and the old number then returns `404`. An update without a number\n"
    "  leaves the filing as it was.",
    "**A listing returns up to 100 country taxes per call, newest first.** A larger `limit` is cut to `100`,\n"
    "  and `pagination.limit` shows `100`. To read every country tax, add `pagination.count` to `offset` after\n"
    "  each page until `offset` reaches `pagination.total`. `sort` takes `id` or `name`, and sorts in descending\n"
    "  order either way. `q`, `search`, `country_code`, `is_rest_of_world` and `field_metadata` are accepted and ignored.",
    "**Read `country.code` to find the country a country tax covers.** On older country taxes, `tax_code` is\n"
    "  free text such as `GST`, `NO_TAX`, `Tax` or `VAT` rather than the country's code. The store's\n"
    "  rest-of-the-world country tax has `is_rest_of_world` set to `true` and `country` set to `null`, and its\n"
    "  state rules have `state` set to `null`. Several country taxes can have `is_default` set to `true` at the\n"
    "  same time.",
    "**Row reads and updates return an `ETag`; the store never returns `304`.** Retrieve and update return an\n"
    "  `ETag` header. Send it as `If-Match` on an update, and the update is rejected with `409` if the country tax\n"
    "  changed since you read it. The SDK functions send no `If-Match`. `If-None-Match` is ignored: a retrieve\n"
    "  with the current `ETag` still returns `200` and the full body. The listing and the create return no `ETag`.",
    "**There is no `HEAD` call for country taxes.** `HEAD` and `OPTIONS` return `404` on the listing and on\n"
    "  a country tax, whether or not a country tax has that `country_tax_id`. The country tax path also accepts\n"
    "  `PATCH`, which changes only the fields you send and returns `200` with an `ETag`; the SDKs have no\n"
    "  function for it. A request the store has no handler for can return `200` with\n"
    "  `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and store nothing, so read the country tax\n"
    "  back after a write.",
]

COUNTRY_TAX_ID = {
    "name": "country_tax_id",
    "in": "path",
    "required": True,
    "description": "The country tax's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 42},
}

IF_MATCH = {
    "name": "If-Match",
    "in": "header",
    "description": "Optional. The country tax's current `ETag`, from your last retrieve or update of it. If the country tax changed since then, the update is rejected with `409`. The SDK functions do not send it.",
    "schema": {"type": "string", "example": "\"5d41402abc4b2a76b9719d911017c592\""},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "description": "Optional. A transaction number to file the new country tax under. The SDKs send it when you pass `transaction_no` to the create. It wins over a different `transaction_no` in the body. No response returns it.",
    "schema": {"type": "string", "example": "TXN-IMPORT-0001"},
}

LIMIT = {"name": "limit", "in": "query", "description": "Country taxes per page, from `1` to `100`. A larger value is cut to `100`, and `pagination.limit` shows `100`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of country taxes to skip before this page.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`. `limit=2&page=2` skips 2 country taxes.", "schema": {"type": "integer", "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "Sorts by `id` or `name`, in descending order either way. `order` and `direction` change nothing. Any other value is rejected with `400` and the message `unsupported sort '<value>'`.", "schema": {"type": "string", "enum": ["id", "name"], "example": "name"}}
SEARCH = {"name": "q", "in": "query", "description": "Accepted and ignored: it does not filter the listing. So are `search`, `country_code` and `is_rest_of_world`.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: it adds nothing to the response.", "schema": {"type": "boolean"}}


REQUEST_ID = "3c9a7e21-6b4d-4f8a-a1e5-2d7c9b0f4e18"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Country tax not found")
INVALID_COUNTRY_CODE = error("invalid_request", "Invalid country_code")
CONFLICT = error("conflict", "The country tax changed since it was read - fetch it again and retry.")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR_REF = ref("CountryTaxError")
ROW_RESPONSE = {"type": "object", "properties": {"country_tax": ref("CountryTax")}}
DETAIL_RESPONSE = {"type": "object", "properties": {"country_tax": ref("CountryTaxDetail")}}


def country_tax(**fields):
    row = {
        "id": 42,
        "name": "NZ GST",
        "country": {"id": 160, "name": "New Zealand", "code": "NZ"},
        "tax_code": "NZ",
        "tax_rate": 15.0,
        "tax_method": "fixed_rate",
        "is_default": False,
        "is_rest_of_world": False,
        "state_rules_count": 0,
        "created_on": "2026-09-24T10:00:00Z",
        "last_updated_on": "2026-09-24T10:00:00Z",
        "last_updated_by": None,
    }
    row.update(fields)
    return row


def with_state_rules(row, rules):
    return dict(row, state_rules=rules)


CREATED = country_tax()
UPDATED = with_state_rules(country_tax(tax_rate=12.5, last_updated_on="2026-09-24T10:05:00Z"), [])

RETRIEVED = with_state_rules(
    country_tax(id=4, name="New Zealand", tax_code="GST", state_rules_count=1,
                created_on="2026-03-08T01:17:43Z", last_updated_on="2026-03-08T01:17:43Z"),
    [{
        "id": 4, "name": None, "state": None, "address_line_1": None, "address_line_2": None,
        "city": None, "post_code": None, "tax_rate": 0.0, "tax_rule": "use_country_tax", "effective_tax_rate": 15.0,
        "is_default": False,
        "created_on": "2026-03-08T01:17:43Z", "last_updated_on": "2026-03-08T01:17:43Z", "last_updated_by": None,
    }],
)

SAMPLE_ROWS = [
    country_tax(id=13, name="Singapore", country={"id": 201, "name": "Singapore", "code": "SG"},
                tax_code="SG", tax_rate=6.25,
                created_on="2026-06-18T14:45:00Z", last_updated_on="2026-06-18T14:45:00Z"),
    country_tax(id=12, name="Japan", country={"id": 110, "name": "Japan", "code": "JP"},
                tax_code="JP", tax_rate=4.5, created_on="2026-05-04T08:20:00Z", last_updated_on="2026-05-04T08:20:00Z"),
    country_tax(id=5, name="United Kingdom VAT", country={"id": 235, "name": "United Kingdom", "code": "GB"},
                tax_code="VAT", tax_rate=17.5, is_default=True,
                created_on="2025-03-10T09:15:00Z", last_updated_on="2025-03-10T09:15:00Z"),
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

SAMPLE_GROUP_META = {
    "country_tax": {"kind": "resource", "writable": True, "href": "/api/v4/admin/tax/country-taxes/{id}"},
    "state_rules": {"kind": "collection", "writable": True, "href": "/api/v4/admin/tax/country-taxes/{id}/state-rules"},
}

WRAPPER_400 = "The body is not wrapped in `country_tax`: a bare record, or the plural `country_taxes` key, is rejected with the message `country_tax missing`."

ENDPOINTS = [
    {
        "key": "list_tax_country_taxes",
        "slug": "list-country-taxes",
        "title": "List country taxes",
        "method": "GET",
        "path": BASE,
        "summary": "Returns a page of up to 100 country taxes under `country_taxes`, newest first, and how many exist in `pagination.total`.",
        "description": "Returns your store's country taxes under `country_taxes`, newest first, up to `limit` per call with a maximum of `100`. You also get a `pagination` object with the total and this page's `offset`, and `group_meta`, which describes `country_tax` and `state_rules` with a `kind`, a `writable` flag and an `href` each. Each country tax has twelve fields, including `state_rules_count`, the number of its state rules; [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns the rules themselves. To read every country tax, add `pagination.count` to `offset` after each page until `offset` reaches `pagination.total`. Send `sort=name` to sort by name. `q`, `search`, `country_code`, `is_rest_of_world` and `field_metadata` are accepted and ignored. The response has no `ETag`.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, SEARCH, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The country taxes on this page under `country_taxes`, `group_meta`, and a `pagination` object with the number of country taxes in the store and this page's position.",
                "schema": {"type": "object", "properties": {
                    "country_taxes": {"type": "array", "items": ref("CountryTax")},
                    "group_meta": ref("CountryTaxGroupMeta"),
                    "pagination": ref("CountryTaxPagination"),
                }},
                "example": {"country_taxes": SAMPLE_ROWS, "group_meta": SAMPLE_GROUP_META, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is `0`: the message is `'limit' must be a positive integer`. Or `sort` is not `id` or `name`: the message is `unsupported sort '<value>'`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "create_tax_country_tax",
        "slug": "create-a-country-tax",
        "title": "Create a country tax",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a country tax and returns it with its `id`, which other calls take as `country_tax_id`.",
        "description": "Creates a country tax and returns it with the `id` the store assigned, which the other calls take as `country_tax_id`. Wrap the record in `country_tax` and include `country_code`, in any letter case. The store fills `country` from it, and sets `tax_code` to the country's code unless you send `tax_code`. No response includes `country_code`, and `country_id` is not read. `tax_method` takes `fixed_rate`, `api` or `no_tax` in any letter case and reads back in lower case. `name` is optional and reads `null` when you leave it out. Fields the store does not know are dropped, and you can create a second country tax for a country that already has one. To file the country tax under a transaction number, send an `X-Transaction-No` header, or `transaction_no` at the top level of the body beside `country_tax`. A `transaction_no` inside `country_tax` files nothing. The response has the twelve fields of a listing row, no `state_rules`, and no `ETag` or `Location` header.",
        "parameters": [TRANSACTION_NO],
        "body": {
            "schema": {"type": "object", "required": ["country_tax"], "properties": {
                "country_tax": dict(ref("CountryTaxInput"), description="The new country tax. `country_code` is required."),
                "transaction_no": {"type": "string", "description": "Optional. A transaction number to file the new country tax under. Send it here, beside `country_tax`: inside `country_tax` it files nothing. An `X-Transaction-No` header with a different number wins."},
            }},
            "example": {"country_tax": {"country_code": "NZ", "name": "NZ GST", "tax_rate": 15.0, "tax_method": "fixed_rate"}, "transaction_no": "TXN-IMPORT-0001"},
        },
        "responses": {
            "201": {
                "description": "The new country tax. Its `id` is the `country_tax_id` the other calls take.",
                "schema": ROW_RESPONSE,
                "example": {"country_tax": CREATED},
            },
            "400": {
                "description": "The body has no `country_code`, or a code no country has: the code is `invalid_request` and the message is `Invalid country_code`. Or `tax_method` is not one of the three values: the message is `Invalid tax_method. Must be one of: fixed_rate, api, no_tax`. Or the body is not wrapped in `country_tax`: the message is `country_tax missing`.",
                "schema": ERROR_REF,
                "example": INVALID_COUNTRY_CODE,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_tax_country_tax",
        "slug": "retrieve-a-country-tax",
        "title": "Retrieve a country tax",
        "method": "GET",
        "path": BASE + "/{country_tax_id}",
        "summary": "Returns the country tax whose `id` you pass as `country_tax_id`, with its state rules and an `ETag`.",
        "description": "Returns one country tax under the `country_tax` key. It has the twelve fields of a listing row plus `state_rules`, the list of the country tax's state rules. A country tax with no state rules has an empty `state_rules` list. The response has an `ETag` header, which you can send as `If-Match` on an update. Sending it back in `If-None-Match` still returns `200` and the full body.",
        "parameters": [COUNTRY_TAX_ID],
        "responses": {
            "200": {
                "description": "The country tax, with its `state_rules`. The response has an `ETag` header.",
                "schema": DETAIL_RESPONSE,
                "example": {"country_tax": RETRIEVED},
            },
            "404": {
                "description": "No country tax has that `country_tax_id`, including one you have deleted. The code is `not_found` and the message is `Country tax not found`.",
                "schema": ERROR_REF,
                "example": NOT_FOUND,
            },
        },
        "example_call": {"path": {"country_tax_id": 4}},
    },
    {
        "key": "update_tax_country_tax",
        "slug": "update-a-country-tax",
        "title": "Update a country tax",
        "method": "PUT",
        "path": BASE + "/{country_tax_id}",
        "summary": "Changes only the fields you send and returns the updated country tax with its state rules and an `ETag`.",
        "description": "Changes the fields you send inside `country_tax` and returns the updated country tax. Fields you leave out keep their values, so you do not send `country_code` again. A new `country_code` moves the country tax to that country, and `\"tax_method\": \"no_tax\"` sets `tax_rate` to `0`. Send an `If-Match` header with the `ETag` from your last read if you want the update rejected with `409` when the country tax changed since then. A `transaction_no` at the top level of the body, or in an `X-Transaction-No` header, files the country tax under that number, and its old number then returns `404`. The response has the twelve fields of a listing row plus `state_rules`, and an `ETag` header.",
        "parameters": [COUNTRY_TAX_ID, IF_MATCH],
        "body": {
            "schema": {"type": "object", "required": ["country_tax"], "properties": {
                "country_tax": dict(ref("CountryTaxInput"), description="The fields to change. Fields you leave out keep their values."),
                "transaction_no": {"type": "string", "description": "Optional. Files the country tax under this number, beside `country_tax`. Its old number then returns `404`. Without it, the filing stays as it was."},
            }},
            "example": {"country_tax": {"tax_rate": 12.5}},
        },
        "responses": {
            "200": {
                "description": "The updated country tax, with its `state_rules`. The response has an `ETag` header.",
                "schema": DETAIL_RESPONSE,
                "example": {"country_tax": UPDATED},
            },
            "400": {
                "description": WRAPPER_400,
                "schema": ERROR_REF,
            },
            "409": {
                "description": "Your `If-Match` value is not the country tax's current `ETag`. The code is `conflict` and the message is `The country tax changed since it was read - fetch it again and retry.`",
                "schema": ERROR_REF,
                "example": CONFLICT,
            },
        },
        "example_call": {"path": {"country_tax_id": 42}},
    },
    {
        "key": "delete_tax_country_tax",
        "slug": "delete-a-country-tax",
        "title": "Delete a country tax",
        "method": "DELETE",
        "path": BASE + "/{country_tax_id}",
        "summary": "Deletes a country tax permanently and returns `204` with no body.",
        "description": "Deletes the country tax permanently and returns `204` with no body. Retrieving or deleting it again returns `404`. If the request just before this one on the same client was rejected with `404`, the store returns that `404` for the delete and removes nothing. Retrieve the country tax afterwards to confirm it is gone.",
        "parameters": [COUNTRY_TAX_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {
                "description": "You already deleted the country tax, or the request just before this one on the same client was rejected with `404` and the store returned that `404` again without deleting anything. The code is `not_found` and the message is `Country tax not found`.",
                "schema": ERROR_REF,
                "example": NOT_FOUND,
            },
        },
        "example_call": {"path": {"country_tax_id": 42}},
    },
]

COUNTRY_TAX_FIELDS = {
    "id": {"type": "integer", "description": "The country tax's `id`, assigned by the store. The other calls take it as `country_tax_id`."},
    "name": {"type": ["string", "null"], "description": "The country tax's name. `null` when you create it without one."},
    "country": {"anyOf": [ref("CountryTaxCountry"), {"type": "null"}], "description": "The country this country tax covers. `null` on the store's rest-of-the-world country tax."},
    "tax_code": {"type": ["string", "null"], "description": "On a country tax you create without `tax_code`, the country's code. On older country taxes it can be free text such as `GST`, `NO_TAX`, `Tax` or `VAT`, so read `country.code` to find the country."},
    "tax_rate": {"type": "number", "description": "The rate as a number, such as `15.0` for 15%. `0` after an update sets `tax_method` to `no_tax`."},
    "tax_method": {"type": "string", "description": "The tax method in lower case: `fixed_rate`, `api` or `no_tax`."},
    "is_default": {"type": "boolean", "description": "The country tax's default flag. Several country taxes can have `true` at the same time."},
    "is_rest_of_world": {"type": "boolean", "description": "`true` on the store's rest-of-the-world country tax, which has `country` set to `null`."},
    "state_rules_count": {"type": "integer", "description": "The number of state rules the country tax has. [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns the rules themselves, as `state_rules`."},
    "created_on": {"type": "string", "description": "When the country tax was created."},
    "last_updated_on": {"type": "string", "description": "When the country tax was last changed."},
    "last_updated_by": {"description": "Who last changed the country tax. The store returns `null`."},
}

SCHEMAS = {
    "CountryTax": {"type": "object", "description": "A country tax as the listing and the create return it: twelve fields, without `state_rules`.", "properties": COUNTRY_TAX_FIELDS},
    "CountryTaxDetail": {"type": "object", "description": "A country tax as [Retrieve a country tax](" + RETRIEVE_PAGE + ") and the update return it: the twelve fields of a listing row, plus `state_rules`.", "properties": with_state_rules(
        COUNTRY_TAX_FIELDS,
        {"type": "array", "items": ref("CountryTaxStateRule"), "description": "The country tax's state rules, or an empty list when it has none."},
    )},
    "CountryTaxCountry": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The country's own `id`. It is not a `country_tax_id`."},
        "name": {"type": "string", "description": "The country's name."},
        "code": {"type": "string", "description": "The country's code, such as `NZ`. Send this value as `country_code` to create a country tax for the country."},
    }},
    "CountryTaxState": {"type": "object", "description": "The state a state rule applies to.", "properties": {
        "id": {"type": "integer", "description": "The state's own `id`. It is not a `country_tax_id`."},
        "name": {"type": "string", "description": "The state's name."},
        "code": {"type": "string", "description": "The state's code."},
    }},
    "CountryTaxStateRule": {"type": "object", "description": "One state rule of a country tax. Retrieve and update return state rules; the listing and the create do not.", "properties": {
        "id": {"type": "integer", "description": "The state rule's own `id`. No call on these pages takes it."},
        "name": {"type": ["string", "null"]},
        "state": {"anyOf": [ref("CountryTaxState"), {"type": "null"}], "description": "The state the rule applies to. `null` on the rules of the rest-of-the-world country tax."},
        "address_line_1": {"type": ["string", "null"]},
        "address_line_2": {"type": ["string", "null"]},
        "city": {"type": ["string", "null"]},
        "post_code": {"type": ["string", "null"]},
        "tax_rate": {"type": "number"},
        "tax_rule": {"type": "string"},
        "effective_tax_rate": {"type": "number"},
        "is_default": {"type": "boolean"},
        "created_on": {"type": "string", "description": "When the state rule was created."},
        "last_updated_on": {"type": "string", "description": "When the state rule was last changed."},
        "last_updated_by": {"description": "Who last changed the state rule. The store returns `null`."},
    }},
    "CountryTaxInput": {"type": "object", "description": "The fields a create or an update can send, wrapped in `country_tax`. Send `transaction_no` beside `country_tax`, not inside it.", "properties": {
        "country_code": {"type": "string", "description": "Required when you create a country tax. The country's code, such as `NZ`, in any letter case. On an update, a new code moves the country tax to that country. No response includes it: the store fills `country` from it."},
        "name": {"type": "string", "description": "The country tax's name. Optional."},
        "tax_code": {"type": "string", "description": "Optional. Defaults to the country's code on a create."},
        "tax_rate": {"type": "number", "description": "The rate as a number, such as `15.0` for 15%."},
        "tax_method": {"type": "string", "enum": ["fixed_rate", "api", "no_tax"], "description": "`fixed_rate`, `api` or `no_tax`, in any letter case. On a create, any other value is rejected with `400`. On an update, `no_tax` sets `tax_rate` to `0`."},
        "is_default": {"type": "boolean", "description": "The country tax's default flag. Several country taxes can have `true` at the same time."},
    }},
    "CountryTaxResourceMeta": {"type": "object", "description": "One entry of `group_meta`.", "properties": {
        "kind": {"type": "string", "description": "`resource` for `country_tax`, `collection` for `state_rules`."},
        "writable": {"type": "boolean", "description": "Whether the entry can be written."},
        "href": {"type": "string", "description": "The entry's path, with `{id}` standing for the `country_tax_id`, such as `/api/v4/admin/tax/country-taxes/{id}`."},
    }},
    "CountryTaxGroupMeta": {"type": "object", "description": "Describes the country tax and its state rules. Only the listing returns it.", "properties": {
        "country_tax": ref("CountryTaxResourceMeta"),
        "state_rules": ref("CountryTaxResourceMeta"),
    }},
    "CountryTaxPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of country taxes in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `100`."},
        "offset": {"type": "integer", "description": "The number of country taxes skipped before this page."},
        "count": {"type": "integer", "description": "The number of country taxes on this page."},
        "current_page": {"type": "integer", "description": "The number of this page, starting at `1`."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up."},
        "has_next": {"type": "boolean", "description": "Whether there is a page after this one."},
        "has_previous": {"type": "boolean", "description": "`false` on the first page."},
        "previous_page": {"type": ["string", "null"], "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` on the last page."},
    }},
    "CountryTaxError": {"type": "object", "description": "Why the request was rejected.", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string", "description": "What went wrong, such as `Country tax not found` or `Invalid country_code`."},
        "details": {"type": "array", "items": {"type": "object"}, "description": "Extra detail, or an empty list."},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
