"""The Tax rules endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Tax rules"
SLUG = "tax-rules"
BASE = "/admin/tax_rules"
ICON = "scale-balanced"

OVERVIEW_DESCRIPTION = "List, create, update and delete tax rules, and read the tax code and tax zones on each rule."
INTRO = "The Tax rules API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax_rules`."

RETRIEVE_PAGE = "/api-reference/tax-rules/retrieve-a-tax-rule"

WARNING = (
    "**`code`, `zones`, `decimal_point` and `rounding_type` cannot be set through this API.** Create and\n"
    "  update accept them and return success, but store none of them. A rule you create has `code: {}`,\n"
    "  `zones: []`, `decimal_point` set to `2` and `rounding_type` set to `nearest`, whatever you send, and\n"
    "  an update leaves these four fields as they were."
)

NOTES = [
    "**Wrap every write in `tax_rule`.** Send `{\"tax_rule\": {\"name\": \"Reduced rate\"}}` to create or\n"
    "  update a rule. A bare record is rejected with `400` and the message `tax_rule missing`. On create,\n"
    "  `name` is required and a body without it fails with `500`; `description` is the only other field\n"
    "  the store reads. An update changes only the fields you send.",
    "**A listing returns at most 20 rules per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To read every rule, step `offset` by the number of rules each page\n"
    "  returned until you reach `pagination.total`. A `limit` below `1`, or a `limit` or `offset` that is\n"
    "  not a number, is rejected with `400` and the error `invalid_pagination`.",
    "**A rejected request can make the next request on the same connection fail too.** Straight after a\n"
    "  `404`, the next retrieve returns `404`, even for a tax rule that exists. A retrieve from another tax\n"
    "  collection returns `404` with that collection's own message, such as `Profile not found`. Straight\n"
    "  after a `400` `invalid_pagination`, the next listing returns the same `400`, even on another tax\n"
    "  collection. The request after that is handled normally. So a delete sent straight after a `404`\n"
    "  returns that `404` and deletes nothing. Check the status of every call, and send the delete again\n"
    "  when it returns the previous call's error.",
    "**A `200` does not always mean the call worked.** A method these paths do not handle, such as\n"
    "  `OPTIONS`, returns `200` with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` instead\n"
    "  of `405`, and stores nothing. A `HEAD` request for one rule returns `200` even when no rule has the\n"
    "  `tax_rule_id` you send; use [Retrieve a tax rule](" + RETRIEVE_PAGE + ") to check that a rule exists.",
    "**Tax rules live at `/admin/tax_rules`, not under `/admin/tax/`.** `/admin/tax/custom_rules`, the\n"
    "  path an older API collection used, returns `404` with the error code `not_found` and a message that\n"
    "  starts `Unknown tax path`.",
]

TAX_RULE_ID = {
    "name": "tax_rule_id",
    "in": "path",
    "required": True,
    "description": "The tax rule's `id`, from a listing or from the response to creating the rule.",
    "schema": {"type": "integer", "example": 42},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rules per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. A value below `1`, or one that is not a number, is rejected with `400` and the error `invalid_pagination`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rules to skip. A value that is not a number is rejected with `400` and the error `invalid_pagination`.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the `limit` you send with it.", "schema": {"type": "integer", "example": 1}}

ROW_REF = {"$ref": "#/components/schemas/TaxRule"}
WRITE_BODY = {"type": "object", "required": ["tax_rule"], "properties": {"tax_rule": {"$ref": "#/components/schemas/TaxRuleInput"}}}
ROW_RESPONSE = {"type": "object", "properties": {"tax_rule": ROW_REF}}
ERROR = {"$ref": "#/components/schemas/TaxRuleError"}

SAMPLE_ROWS = [
    {
        "id": 7,
        "name": "GST",
        "code": {"id": 3, "name": "GST", "is_default": True},
        "description": "Goods and services tax",
        "default": True,
        "rounding_type": "nearest",
        "decimal_point": 2,
        "zones": [{"id": 1, "name": "Australia", "is_system_generated": True, "is_default": True}],
        "created_at": "2026-01-15T09:30:00",
        "updated_at": "2026-01-15T09:30:00",
    },
    {
        "id": 42,
        "name": "Reduced rate",
        "code": {},
        "description": "Rule for reduced-rate goods",
        "default": False,
        "rounding_type": "nearest",
        "decimal_point": 2,
        "zones": [],
        "created_at": "2026-09-21T10:15:00",
        "updated_at": "2026-09-21T10:15:00",
    },
]

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

UPDATED_ROW = dict(SAMPLE_ROWS[1], name="Reduced rate goods", updated_at="2026-09-22T08:40:00")

WRITE_400 = "The body is not wrapped in `tax_rule`. The message is `tax_rule missing`."

ENDPOINTS = [
    {
        "key": "list_tax_rules",
        "slug": "list-tax-rules",
        "title": "List tax rules",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 tax rules per call, each with its tax code and tax zones.",
        "description": "Returns up to 20 tax rules under `tax_rules`, and the rule count and page position under `pagination`. Each rule has ten fields, including its tax code in `code` and its tax zones in `zones`. To read every rule, step `offset` by the number of rules each page returned until you reach `pagination.total`. `q` and `field_metadata` are accepted and ignored: `q` does not filter the rules.",
        "parameters": [LIMIT, OFFSET, PAGE],
        "responses": {
            "200": {
                "description": "Up to 20 tax rules under `tax_rules`. `pagination.total` is the number of rules in the store. No `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "tax_rules": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/TaxRulePagination"},
                }},
                "example": {"tax_rules": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "`limit` is below `1`, or `limit` or `offset` is not a number. The error is `invalid_pagination`, and the `errors` list in the response names the rejected parameter.", "schema": ERROR},
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_tax_rules",
        "slug": "check-the-tax-rules-list",
        "title": "Check the tax rules list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the tax rules path exists. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. A `200` shows only that the path exists: the store also returns `200` for a method it does not handle, and a `HEAD` response has no body to tell the two apart. The response has no `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {"description": "The path exists. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_tax_rule",
        "slug": "create-a-tax-rule",
        "title": "Create a tax rule",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a tax rule and returns the new rule, whose `id` other calls take as `tax_rule_id`.",
        "description": "Creates a tax rule and returns it, with the rule's `id` set by the store. Pass that `id` as `tax_rule_id` to retrieve, update or delete the rule. Wrap the fields in `tax_rule`: `name` is required, and `description` is the only other field the store reads. `code`, `zones`, `decimal_point` and `rounding_type` are accepted and not stored, so the new rule has `code: {}`, `zones: []`, `decimal_point` set to `2` and `rounding_type` set to `nearest`.",
        "body": {"schema": WRITE_BODY, "example": {"tax_rule": {"name": "Reduced rate", "description": "Rule for reduced-rate goods"}}},
        "responses": {
            "201": {
                "description": "The new tax rule.",
                "schema": ROW_RESPONSE,
                "example": {"tax_rule": SAMPLE_ROWS[1]},
            },
            "400": {"description": WRITE_400, "schema": ERROR},
            "500": {"description": "The body has no `name` inside `tax_rule`. The store rejects a create without a `name` with `500`, not `400`.", "schema": ERROR},
        },
        "example_call": {},
    },
    {
        "key": "get_tax_rule",
        "slug": "retrieve-a-tax-rule",
        "title": "Retrieve a tax rule",
        "method": "GET",
        "path": BASE + "/{tax_rule_id}",
        "summary": "Returns the tax rule whose `id` you pass as `tax_rule_id`, with its tax code and zones.",
        "description": "Returns one tax rule under the `tax_rule` key, with the same ten fields a listing row has. `code` holds the rule's tax code and `zones` its tax zones. A rule created through this API has `code: {}` and `zones: []`.",
        "parameters": [TAX_RULE_ID],
        "responses": {
            "200": {
                "description": "The tax rule. No `ETag` or `Last-Modified` header.",
                "schema": ROW_RESPONSE,
                "example": {"tax_rule": SAMPLE_ROWS[0]},
            },
            "404": {"description": "No tax rule has that `tax_rule_id`. The message is `Rule not found`.", "schema": ERROR},
        },
        "example_call": {"path": {"tax_rule_id": 7}},
    },
    {
        "key": "head_tax_rule",
        "slug": "check-a-tax-rule",
        "title": "Check a tax rule",
        "method": "HEAD",
        "path": BASE + "/{tax_rule_id}",
        "summary": "Returns headers only, and `200` even when no tax rule has that `tax_rule_id`.",
        "description": "Returns `200` with headers only and no body. It returns `200` even when no tax rule has that `tax_rule_id`, so it does not tell you whether the rule exists. To check that, use [Retrieve a tax rule](" + RETRIEVE_PAGE + "), which returns `404` with the message `Rule not found`. The response has no `ETag` or `Last-Modified` header.",
        "parameters": [TAX_RULE_ID],
        "responses": {
            "200": {"description": "Headers only, no body. Returned even when no tax rule has that `tax_rule_id`."},
        },
        "example_call": {"path": {"tax_rule_id": 7}},
    },
    {
        "key": "update_tax_rule",
        "slug": "update-a-tax-rule",
        "title": "Update a tax rule",
        "method": "PUT",
        "path": BASE + "/{tax_rule_id}",
        "summary": "Changes a tax rule's `name` or `description` and returns the updated rule.",
        "description": "Changes the fields you send and returns the whole rule; fields you leave out keep their values. Wrap the fields in `tax_rule`. `name` and `description` are the fields you can change: `code`, `zones`, `decimal_point` and `rounding_type` are accepted and left as they were.",
        "parameters": [TAX_RULE_ID],
        "body": {"schema": WRITE_BODY, "example": {"tax_rule": {"name": "Reduced rate goods"}}},
        "responses": {
            "200": {
                "description": "The updated tax rule.",
                "schema": ROW_RESPONSE,
                "example": {"tax_rule": UPDATED_ROW},
            },
            "400": {"description": WRITE_400, "schema": ERROR},
        },
        "example_call": {"path": {"tax_rule_id": 42}},
    },
    {
        "key": "delete_tax_rule",
        "slug": "delete-a-tax-rule",
        "title": "Delete a tax rule",
        "method": "DELETE",
        "path": BASE + "/{tax_rule_id}",
        "summary": "Deletes a tax rule permanently and returns `204` with no body.",
        "description": "Deletes the tax rule permanently and returns `204` with no body. Retrieving it afterwards returns `404` with the message `Rule not found`. If the tax request just before this one was rejected, this call returns that same error instead and deletes nothing, so check the status before you treat the rule as gone.",
        "parameters": [TAX_RULE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "The tax request just before this one was rejected with `404`, so this call returns that same `404` and deletes nothing. The next request is handled normally: send the delete again.", "schema": ERROR},
        },
        "example_call": {"path": {"tax_rule_id": 42}},
    },
]

SCHEMAS = {
    "TaxRule": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The tax rule's `id`, assigned by the store. Pass it as `tax_rule_id` in a path."},
        "name": {"type": "string", "description": "Required on create."},
        "code": {"$ref": "#/components/schemas/TaxRuleCode", "description": "The rule's tax code. No call here sets it: it is `{}` on a rule created through this API."},
        "description": {"type": "string"},
        "default": {"type": "boolean"},
        "rounding_type": {"type": "string", "description": "The rule's rounding type, such as `nearest`. Create and update ignore it: it is `nearest` on a rule created through this API."},
        "decimal_point": {"type": "integer", "description": "Create and update ignore it: it is `2` on a rule created through this API."},
        "zones": {"type": "array", "items": {"$ref": "#/components/schemas/TaxRuleZone"}, "description": "The rule's tax zones. No call here sets them: the list is empty on a rule created through this API."},
        "created_at": {"type": "string", "description": "When the rule was created."},
        "updated_at": {"type": "string", "description": "When the rule was last changed."},
    }},
    "TaxRuleCode": {"type": "object", "description": "The tax code on a rule. On a rule created through this API it is `{}`, with none of these fields.", "properties": {
        "id": {"type": "integer", "description": "The tax code's `id`, which the Tax codes endpoints take as `tax_code_id`."},
        "name": {"type": "string", "description": "The tax code's name."},
        "is_default": {"type": "boolean"},
    }},
    "TaxRuleZone": {"type": "object", "description": "One tax zone on a rule.", "properties": {
        "id": {"type": "integer", "description": "The tax zone's `id`, which the Tax zones endpoints take as `tax_zone_id`."},
        "name": {"type": "string", "description": "The tax zone's name."},
        "is_system_generated": {"type": "boolean"},
        "is_default": {"type": "boolean"},
    }},
    "TaxRuleInput": {"type": "object", "description": "The two fields a create or update stores: `name` and `description`. The store ignores any other field you send.", "properties": {
        "name": {"type": "string", "description": "Required on create. On update, send it only to change it."},
        "description": {"type": "string", "description": "Optional. On update, send it only to change it."},
    }},
    "TaxRulePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of tax rules in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`, even when you send a larger `limit`."},
        "offset": {"type": "integer", "description": "The number of rules skipped before this page."},
        "count": {"type": "integer", "description": "The number of rules on this page."},
        "current_page": {"type": "integer"},
        "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"},
        "has_previous": {"type": "boolean"},
        "previous_page": {"type": ["string", "null"], "description": "The URL of the previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The URL of the next page, or `null` on the last page."},
    }},
    "TaxRuleError": {"type": "object", "additionalProperties": True, "description": "Why the request was rejected. Each error status on these pages gives its message.", "properties": {
        "errors": {"type": "array", "description": "Only on a `400` for a paging parameter: names the rejected parameter, `limit` or `offset`.", "items": {"type": "object"}},
    }},
}
