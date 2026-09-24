"""The Country taxes endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Country taxes"
SLUG = "country-taxes"
BASE = "/admin/tax/country_taxes"
ICON = "globe"

OVERVIEW_DESCRIPTION = "List, create, update and delete your store's country taxes, and read the state rules of each one."
INTRO = "The Country taxes API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax/country_taxes`."

RETRIEVE_PAGE = "/api-reference/country-taxes/retrieve-a-country-tax"

WARNING = (
    "**After a request is rejected, the store handles your next request on the same client with the rejected value.**\n"
    "  This applies to the id in the path, such as a `country_tax_id`, and to a query parameter such as `limit`, and\n"
    "  it lasts for one request. After `GET /admin/tax/country_taxes/99999999` returns `404`, your next request for\n"
    "  one record, such as `GET /admin/tax/country_taxes/4` or `GET /admin/tax/custom_profiles/1`, also returns `404`,\n"
    "  even though that record exists. After `limit=0` is rejected, your next listing call is rejected with the same\n"
    "  message, even with `limit=1`. A request that takes neither value runs normally, and a request from a new client\n"
    "  is not affected. A delete sent straight after a rejected `country_tax_id` is handled with that id, so it returns\n"
    "  `404` and removes nothing. Confirm a delete by reading the country tax back with\n"
    "  [Retrieve a country tax](" + RETRIEVE_PAGE + ")."
)

NOTES = [
    "**Wrap every create and update in `country_tax`, and send `country_code` when you create.** A bare\n"
    "  record, or the plural `country_taxes` key, is rejected with `400` and the message `country_tax missing`.\n"
    "  A create without `country_code` is rejected with `400 invalid_request` and the message\n"
    "  `Invalid country_code`. The store fills `country` and `code` from `country_code` and works out\n"
    "  `rate_display` from `tax_rate`, but no response includes `country_code` itself.",
    "**An update changes only the fields you send.** Fields you leave out keep their values, so you do not\n"
    "  send `country_code` again. When you change `tax_rate`, `rate_display` changes with it.",
    "**A listing returns at most 20 country taxes per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To read every country tax, add `pagination.count` to `offset` after each\n"
    "  page until `offset` reaches `pagination.total`. `q` and `field_metadata` are accepted and ignored.",
    "**Read `country.code` to find the country a country tax covers.** On older country taxes, `code` is free\n"
    "  text such as `GST`, `NO_TAX`, `Tax` or `VAT` rather than the country's code. The store's rest-of-the-world\n"
    "  country tax has `country` set to `null`, and `special_key` names it instead. Several country taxes can\n"
    "  have `is_default` set to `true` at the same time.",
    "**There is no `HEAD` call for country taxes, and a `200` does not prove a write was stored.** A `HEAD` or\n"
    "  `OPTIONS` request on the listing is rejected with `404`. A `HEAD` on one country tax returns `200` whether\n"
    "  or not a country tax has that `country_tax_id`, so it cannot tell you the country tax exists. A method the\n"
    "  store has no handler for returns `200` with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}`\n"
    "  and stores nothing, so read the country tax back after a write. Neither path sends an `ETag` or\n"
    "  `Last-Modified` header.",
]

COUNTRY_TAX_ID = {
    "name": "country_tax_id",
    "in": "path",
    "required": True,
    "description": "The country tax's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 42},
}

LIMIT = {"name": "limit", "in": "query", "description": "Country taxes per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of country taxes to skip before this page.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`. `limit=2&page=2` skips 2 country taxes.", "schema": {"type": "integer", "example": 1}}
SEARCH = {"name": "q", "in": "query", "description": "Accepted and ignored: it does not filter the listing.", "schema": {"type": "string"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: it adds nothing to the response.", "schema": {"type": "boolean"}}


REQUEST_ID = "3c9a7e21-6b4d-4f8a-a1e5-2d7c9b0f4e18"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Country tax not found")
INVALID_COUNTRY_CODE = error("invalid_request", "Invalid country_code")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR_REF = ref("CountryTaxError")
ROW_RESPONSE = {"type": "object", "properties": {"country_tax": ref("CountryTax")}}


def country_tax(**fields):
    row = {
        "id": 42,
        "name": "New Zealand",
        "country": {"id": 160, "name": "New Zealand", "code": "NZ"},
        "code": "NZ",
        "tax_rate": 4.5,
        "tax_method": "FIXED_RATE",
        "is_default": False,
        "special_key": None,
        "state_rules_count": 0,
        "rate_display": "4.5%",
        "transaction_no": None,
        "created_at": "2026-09-24T10:00:00",
        "updated_at": "2026-09-24T10:00:00",
    }
    row.update(fields)
    return row


def with_state_rules(row, rules):
    return dict(row, state_rules=rules)


CREATED = country_tax()
UPDATED = country_tax(tax_rate=6.25, rate_display="6.25%", updated_at="2026-09-24T10:05:00")

RETRIEVED = with_state_rules(
    country_tax(id=4, code="GST", tax_rate=15.0, rate_display="15.0%", state_rules_count=1,
                created_at="2026-03-08T12:17:43", updated_at="2026-03-08T12:17:43"),
    [{
        "id": 4, "name": None, "state": None, "state_name": None, "address_line_1": None, "address_line_2": None,
        "city": None, "post_code": None, "tax_rate": 0.0, "tax_rule": "USE_COUNTRY_TAX", "effective_tax_rate": 15.0,
        "is_default": False, "transaction_no": None,
        "created_at": "2026-03-08T12:17:43", "updated_at": "2026-03-08T12:17:43",
    }],
)

SAMPLE_ROWS = [
    country_tax(id=5, name="United Kingdom VAT", country={"id": 235, "name": "United Kingdom", "code": "GB"},
                code="VAT", tax_rate=17.5, rate_display="17.5%", is_default=True,
                created_at="2025-03-10T09:15:00", updated_at="2025-03-10T09:15:00"),
    country_tax(id=12, name="Japan", country={"id": 110, "name": "Japan", "code": "JP"},
                code="JP", created_at="2026-05-04T08:20:00", updated_at="2026-05-04T08:20:00"),
    country_tax(id=13, name="Singapore", country={"id": 201, "name": "Singapore", "code": "SG"},
                code="SG", tax_rate=6.25, rate_display="6.25%",
                created_at="2026-06-18T14:45:00", updated_at="2026-06-18T14:45:00"),
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

WRAPPER_400 = "The body is not wrapped in `country_tax`: a bare record, or the plural `country_taxes` key, is rejected with the message `country_tax missing`."

ENDPOINTS = [
    {
        "key": "list_tax_country_taxes",
        "slug": "list-country-taxes",
        "title": "List country taxes",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 country taxes under `country_taxes`, and how many exist in `pagination.total`.",
        "description": "Returns your store's country taxes under `country_taxes`, up to 20 per call, and a `pagination` object with the total and this page's `offset`. Each country tax has thirteen fields, including `state_rules_count`, the number of its state rules; only [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns the rules themselves. To read every country tax, add `pagination.count` to `offset` after each page until `offset` reaches `pagination.total`. `q` and `field_metadata` are accepted and ignored.",
        "parameters": [LIMIT, OFFSET, PAGE, SEARCH, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "Up to 20 country taxes under `country_taxes`, and a `pagination` object with the number of country taxes in the store and this page's position.",
                "schema": {"type": "object", "properties": {
                    "country_taxes": {"type": "array", "items": ref("CountryTax")},
                    "pagination": ref("CountryTaxPagination"),
                }},
                "example": {"country_taxes": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
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
        "description": "Creates a country tax and returns it with the `id` the store assigned, which the other calls take as `country_tax_id`. Wrap the record in `country_tax` and include `country_code`: the store fills `country` and `code` from it and works out `rate_display` from `tax_rate`, but no response includes `country_code` itself. Fields the store does not know are dropped, and you can create a second country tax for a country that already has one. The response has the same thirteen fields as a country tax in the listing.",
        "body": {
            "schema": {"type": "object", "required": ["country_tax"], "properties": {
                "country_tax": dict(ref("CountryTaxInput"), description="The new country tax. `country_code` is required."),
            }},
            "example": {"country_tax": {"country_code": "NZ", "name": "New Zealand", "tax_rate": 4.5, "tax_method": "FIXED_RATE", "is_default": False}},
        },
        "responses": {
            "201": {
                "description": "The new country tax. Its `id` is the `country_tax_id` the other calls take.",
                "schema": ROW_RESPONSE,
                "example": {"country_tax": CREATED},
            },
            "400": {
                "description": "The body has no `country_code`: the code is `invalid_request` and the message is `Invalid country_code`. Or the body is not wrapped in `country_tax`: the message is `country_tax missing`.",
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
        "summary": "Returns the country tax whose `id` you pass as `country_tax_id`, including its state rules.",
        "description": "Returns one country tax under the `country_tax` key. It has the thirteen fields the listing returns plus `state_rules`, the list of the country tax's state rules, which no other call returns. A country tax with no state rules has an empty `state_rules` list.",
        "parameters": [COUNTRY_TAX_ID],
        "responses": {
            "200": {
                "description": "The country tax, with its `state_rules`.",
                "schema": {"type": "object", "properties": {"country_tax": ref("CountryTaxDetail")}},
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
        "summary": "Changes only the fields you send and returns the updated country tax.",
        "description": "Changes the fields you send inside `country_tax` and returns the updated country tax. Fields you leave out keep their values, so you do not send `country_code` again. When you change `tax_rate`, `rate_display` changes with it. The response has the same thirteen fields as a country tax in the listing, without `state_rules`.",
        "parameters": [COUNTRY_TAX_ID],
        "body": {
            "schema": {"type": "object", "required": ["country_tax"], "properties": {
                "country_tax": dict(ref("CountryTaxInput"), description="The fields to change. Fields you leave out keep their values."),
            }},
            "example": {"country_tax": {"tax_rate": 6.25}},
        },
        "responses": {
            "200": {
                "description": "The updated country tax.",
                "schema": ROW_RESPONSE,
                "example": {"country_tax": UPDATED},
            },
            "400": {
                "description": WRAPPER_400,
                "schema": ERROR_REF,
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
        "description": "Deletes the country tax permanently and returns `204` with no body. The country tax leaves the listing, `pagination.total` goes down by one, and retrieving it returns `404`. If the request just before this one on the same client was rejected with `404` for an id in its path that no record has, such as a `country_tax_id` that no country tax has, the store handles the delete with that rejected value: it returns `404` and removes nothing. Retrieve the country tax afterwards to confirm it is gone.",
        "parameters": [COUNTRY_TAX_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
        },
        "example_call": {"path": {"country_tax_id": 42}},
    },
]

COUNTRY_TAX_FIELDS = {
    "id": {"type": "integer", "description": "The country tax's `id`, assigned by the store. The other calls take it as `country_tax_id`."},
    "name": {"type": ["string", "null"], "description": "The country tax's name. Can be `null`."},
    "country": {"anyOf": [ref("CountryTaxCountry"), {"type": "null"}], "description": "The country this country tax covers. `null` on the store's rest-of-the-world country tax."},
    "code": {"type": "string", "description": "On a country tax you create, the same as `country.code`. On older country taxes it can be free text such as `GST`, `NO_TAX`, `Tax` or `VAT`, so read `country.code` to find the country."},
    "tax_rate": {"type": "number", "description": "The rate as a number, such as `4.5` for 4.5%."},
    "tax_method": {"type": "string", "description": "The tax method, such as `FIXED_RATE`."},
    "is_default": {"type": "boolean", "description": "The country tax's default flag. Several country taxes can have `true` at the same time."},
    "special_key": {"type": ["string", "null"], "description": "A key the store sets on some of its own country taxes: `rest_of_world` on the rest-of-the-world country tax, which has `country` set to `null`, and `usa_based` on the United States country tax. `null` on the others, including every country tax you create."},
    "state_rules_count": {"type": "integer", "description": "The number of state rules the country tax has. Only [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns the rules themselves, as `state_rules`."},
    "rate_display": {"type": "string", "description": "The rate as text, worked out by the store. Usually `tax_rate` with a percent sign, such as `4.5%`. A country tax whose `tax_rate` is `0` shows `No Tax`, and one whose state rules set different rates shows `Varies`."},
    "transaction_no": {"type": ["string", "null"]},
    "created_at": {"type": "string", "description": "When the country tax was created."},
    "updated_at": {"type": "string", "description": "When the country tax was last changed."},
}

SCHEMAS = {
    "CountryTax": {"type": "object", "properties": COUNTRY_TAX_FIELDS},
    "CountryTaxDetail": {"type": "object", "description": "A country tax as [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns it: the thirteen fields the listing returns, plus `state_rules`.", "properties": with_state_rules(
        COUNTRY_TAX_FIELDS,
        {"type": "array", "items": ref("CountryTaxStateRule"), "description": "The country tax's state rules, or an empty list when it has none."},
    )},
    "CountryTaxCountry": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The country's own `id`. It is not a `country_tax_id`."},
        "name": {"type": "string", "description": "The country's name."},
        "code": {"type": "string", "description": "The country's code, such as `NZ`. Send this value as `country_code` to create a country tax for the country."},
    }},
    "CountryTaxStateRule": {"type": "object", "description": "One state rule of a country tax. Only [Retrieve a country tax](" + RETRIEVE_PAGE + ") returns state rules.", "properties": {
        "id": {"type": "integer", "description": "The state rule's own `id`. No call on these pages takes it."},
        "name": {"type": ["string", "null"]},
        "state": {"type": ["string", "null"]},
        "state_name": {"type": ["string", "null"]},
        "address_line_1": {"type": ["string", "null"]},
        "address_line_2": {"type": ["string", "null"]},
        "city": {"type": ["string", "null"]},
        "post_code": {"type": ["string", "null"]},
        "tax_rate": {"type": "number"},
        "tax_rule": {"type": "string"},
        "effective_tax_rate": {"type": "number"},
        "is_default": {"type": "boolean"},
        "transaction_no": {"type": ["string", "null"]},
        "created_at": {"type": "string"},
        "updated_at": {"type": "string"},
    }},
    "CountryTaxInput": {"type": "object", "description": "The fields a create or an update can send, wrapped in `country_tax`.", "properties": {
        "country_code": {"type": "string", "description": "Required when you create a country tax. The country's code, such as `NZ`. No response includes it: the store fills `country` and `code` from it."},
        "name": {"type": "string", "description": "The country tax's name."},
        "tax_rate": {"type": "number", "description": "The rate as a number, such as `4.5` for 4.5%. The store sets `rate_display` from it."},
        "tax_method": {"type": "string", "description": "The tax method, such as `FIXED_RATE`."},
        "is_default": {"type": "boolean", "description": "The country tax's default flag. Several country taxes can have `true` at the same time."},
    }},
    "CountryTaxPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of country taxes in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
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
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string", "description": "What went wrong, such as `Country tax not found` or `Invalid country_code`."},
        "details": {"type": "array", "items": {"type": "object"}, "description": "Extra detail, or an empty list."},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
