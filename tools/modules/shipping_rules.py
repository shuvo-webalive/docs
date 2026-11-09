"""The Shipping rules endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping rules"
SLUG = "shipping-rules"
BASE = "/admin/shipping_rules"
ICON = "route"

OVERVIEW_DESCRIPTION = "List, count, create, replace, update and delete shipping rules: a shipping class, a shipping rate and the zones they apply to, under one name."
INTRO = "The Shipping rules API has ten endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/shipping_rules`."

LIST_PAGE = "/api-reference/shipping-rules/list-shipping-rules"
RETRIEVE_PAGE = "/api-reference/shipping-rules/retrieve-a-shipping-rule"
REPLACE_PAGE = "/api-reference/shipping-rules/replace-a-shipping-rule"
UPDATE_PAGE = "/api-reference/shipping-rules/update-a-shipping-rule"
DELETE_PAGE = "/api-reference/shipping-rules/delete-a-shipping-rule"

WARNING = (
    "**A shipping rule is deleted permanently, and a rule that is on a shipping profile cannot be deleted.**\n"
    "  [Delete a shipping rule](" + DELETE_PAGE + ") on a rule that a profile uses is rejected with `409`, and the\n"
    "  response names the profile. The rule's `profiles` list shows which profiles use it. Take the rule off those\n"
    "  profiles first. Deleting a rule keeps its shipping rate and its zones."
)

NOTES = [
    "**Create, replace and update wrap the rule in `shipping_rule`.** Send `{\"shipping_rule\": {...}}`. A body\n"
    "  without the wrapper is rejected with `400`. A field the rule does not have is rejected with `400` and the\n"
    "  reason `unknown_field`, and an `id` in the body with `400` and the reason `not_allowed`. Responses return\n"
    "  the rule inside `shipping_rule`.",
    "**A rule has a shipping class, a shipping rate and zones, and you send each one by its `id`.**\n"
    "  `shipping_class` and `shipping_rate` take an `id`, either bare as `2` or as `{\"id\": 2}`, or `null`.\n"
    "  `zones` takes the whole list of tax zone `id` values, bare or as `{\"id\": ...}`, each zone once. An\n"
    "  unknown `id`, `0`, a decimal such as `1.5`, text, or a repeated zone is rejected with `400`. A class,\n"
    "  rate or zone you leave out reads `null`, `null` and `[]`.",
    "**`PUT` replaces a rule, and `PATCH` changes only the fields you send.**\n"
    "  [Replace a shipping rule](" + REPLACE_PAGE + ") needs `name`, `description`, `shipping_class`,\n"
    "  `shipping_rate` and `zones`, and names each missing field in the `400` response with the reason\n"
    "  `required`. The first three take `null`, and `zones` takes `[]`. [Update a shipping rule](" + UPDATE_PAGE + ")\n"
    "  changes only what you send: `zones` is the full new list, and a `shipping_rate` or `shipping_class` of\n"
    "  `null` takes it off the rule. The rate and the zones themselves stay in the store.",
    "**Send `profile_id` on a create to put the new rule on a shipping profile.** The profile then lists the\n"
    "  rule in `shipping_rules`. A `profile_id` that no profile has is rejected with `400`.",
    "**Filters on a listing take `id` values, and each rule is listed once.** `shipping_class_id` and\n"
    "  `zone_id` keep the rules that have that class or zone. A class or zone `id` that no record has is\n"
    "  rejected with `400` and the reason `invalid_reference`. `method` and `handling_cost` match the\n"
    "  rule's shipping rate.",
    "**A listing returns 20 rules per call unless you send `limit`, and the newest rule comes first.** `limit`\n"
    "  takes `1` to `100`, and `offset` skips rules. To get more, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. A query parameter the listing does not know is ignored.",
]

SHIPPING_RULE_ID = {
    "name": "shipping_rule_id",
    "in": "path",
    "required": True,
    "description": "The shipping rule's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 31},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "required": False,
    "description": "Optional. A transaction number you choose, such as `TXN-IMPORT-0001`. The store files the new rule under it, and the rule returns it as `transaction_no`. You can also send `transaction_no` inside `shipping_rule`: when you send both, the header wins. Another record may use the same number.",
    "schema": {"type": "string", "example": "TXN-IMPORT-0001"},
}

METHODS = ["flat_rate", "free_shipping", "ship_by_price", "ship_by_quantity", "ship_by_weight", "ship_by_variation", "shipping_variant"]
SORT_FIELDS = ["id", "name", "description", "created_at", "updated_at", "transaction_no"]

SEARCH = {"name": "search", "in": "query", "description": "Keeps only rules whose `name` contains this text.", "schema": {"type": "string", "example": "metro"}}
CLASS_FILTER = {"name": "shipping_class_id", "in": "query", "description": "Keeps only rules that have the shipping class with this `id`. An `id` that no shipping class has is rejected with `400` and the reason `invalid_reference`.", "schema": {"type": "integer", "example": 2}}
ZONE_FILTER = {"name": "zone_id", "in": "query", "description": "Keeps only rules that have the zone with this `id`. An `id` that no zone has is rejected with `400` and the reason `invalid_reference`.", "schema": {"type": "integer", "example": 5}}
METHOD_FILTER = {"name": "method", "in": "query", "description": "Keeps only rules whose shipping rate has this `method`: `flat_rate`, `free_shipping`, `ship_by_price`, `ship_by_quantity`, `ship_by_weight`, `ship_by_variation` or `shipping_variant`. The old short codes `fs`, `fr`, `sba`, `sbq`, `sbw`, `sbv` and `sv` are also accepted. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": METHODS, "example": "flat_rate"}}
HANDLING_COST = {"name": "handling_cost", "in": "query", "description": "`with_handling` keeps only rules whose shipping rate has a handling cost, and `without_handling` keeps only rules whose rate has none. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["with_handling", "without_handling"], "example": "without_handling"}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by. Without it, the newest rule comes first. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of rules per call, from `1` to `100`. Defaults to `20`. `0` is rejected with `400` and the reason `out_of_range`, a value above `100` with `400` and the message `must be from 1 to 100`, and a value that is not a number, such as `all`, with `400` and the reason `invalid_integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of rules to skip, `0` or more.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
FILTERS = [SEARCH, CLASS_FILTER, ZONE_FILTER, METHOD_FILTER, HANDLING_COST]

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Shipping rule not found")
BAD_ZONE = error("invalid_request", "zone_id: must be the id of an existing record", [{"field": "zone_id", "code": "invalid_reference", "message": "must be the id of an existing record", "value": "999999"}])
NO_WRAPPER = error("invalid_request", "shipping_rule: must be an object", [{"field": "shipping_rule", "code": "required", "message": "must be an object"}])
DUPLICATE_NAME = error("conflict", "A shipping rule with this name already exists.", [{"field": "name", "code": "duplicate"}])
IN_USE = error("conflict", "The shipping rule is used by shipping profile 12.", [{"field": "profile", "code": "in_use", "value": 12}])

ERROR_REF = {"$ref": "#/components/schemas/ShippingRuleError"}
ROW_REF = {"$ref": "#/components/schemas/ShippingRule"}
ROW_RESPONSE = {"type": "object", "properties": {"shipping_rule": ROW_REF}}
WRITE_BODY = {"type": "object", "required": ["shipping_rule"], "properties": {"shipping_rule": {"$ref": "#/components/schemas/ShippingRuleInput"}}}

METRO_RULE = {
    "id": 31, "name": "Metro", "description": "Metro deliveries",
    "shipping_class": {"id": 2, "name": "Bulky Goods"}, "shipping_rate": {"id": 21, "name": "Flat 10"},
    "zones": [{"id": 5, "name": "Sydney"}], "profiles": [{"id": 12, "name": "Metro profile"}],
    "transaction_no": None, "created_at": "2026-11-05T05:02:55Z", "updated_at": "2026-11-05T05:02:55Z",
}
BARE_RULE = {
    "id": 32, "name": "Regional", "description": None, "shipping_class": None, "shipping_rate": None,
    "zones": [], "profiles": [], "transaction_no": None,
    "created_at": "2026-11-05T05:10:11Z", "updated_at": "2026-11-05T05:10:11Z",
}
SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"shipping_rule": {"name": "Metro", "description": "Metro deliveries", "shipping_class": 2, "shipping_rate": 21, "zones": [5], "profile_id": 12}}
REPLACE_BODY = {"shipping_rule": {"name": "Metro", "description": "Metro and inner west deliveries", "shipping_class": 2, "shipping_rate": 21, "zones": [5, 6]}}
PATCH_BODY = {"shipping_rule": {"zones": [5, 6]}}

WRITE_400 = "The body is not wrapped in `shipping_rule`, a field is unknown (`unknown_field`) or an `id` is sent (`not_allowed`), `name` is missing, or `shipping_class`, `shipping_rate`, `zones` or `profile_id` holds an `id` that no record has, `0`, a decimal, text or a repeated zone. The `code` is `invalid_request`."
NAME_409 = "Another shipping rule already has that `name`, in any letter case. The `code` is `conflict` and `details[0].code` is `duplicate`. Send `suggest_name` as `true` on a create to get the next free name, such as `Metro(1)`, instead."
NOT_FOUND_404 = "No shipping rule has that `shipping_rule_id`, or the value is not a plain whole number. The `code` is `not_found`."

ENDPOINTS = [
    {
        "key": "list_shipping_rules",
        "slug": "list-shipping-rules",
        "title": "List shipping rules",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 shipping rules per call, newest first, with paging details.",
        "description": "Returns the shipping rules in `shipping_rules`, 20 per call unless you send `limit`, and a `pagination` block. The newest rule comes first unless you send `sort` and `order`. Filter with `search`, `shipping_class_id`, `zone_id`, `method` and `handling_cost`; a rule is listed once even when it matches several zones. A query parameter the listing does not know is ignored. When several parameters are invalid, the `400` response lists each one in `details`.",
        "parameters": FILTERS + [SORT, ORDER, LIMIT, OFFSET],
        "responses": {
            "200": {
                "description": "The rules on this call in `shipping_rules`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. Each rule has the same fields [Retrieve a shipping rule](" + RETRIEVE_PAGE + ") returns.",
                "schema": {"type": "object", "properties": {
                    "shipping_rules": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/ShippingRulePagination"},
                }},
                "example": {"shipping_rules": [BARE_RULE, METRO_RULE], "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "A parameter has a value the listing rejects: `shipping_class_id` or `zone_id` is the `id` of no record (reason `invalid_reference`), `method`, `handling_cost`, `sort` or `order` is not one of its values, or `limit` or `offset` is out of range. The `code` is `invalid_request`, and `details` has one entry per rejected parameter with its `field`, `code`, `message` and `value`.", "schema": ERROR_REF, "example": BAD_ZONE},
        },
        "example_call": {"query": {"zone_id": 5, "method": "flat_rate", "handling_cost": "without_handling", "sort": "name", "order": "asc"}},
    },
    {
        "key": "head_shipping_rules",
        "slug": "check-the-shipping-rules-list",
        "title": "Check the shipping rules list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns `200` and the headers of the shipping rules listing, with no body.",
        "description": "Returns `200` with headers only and no body. To read the rules, use [List shipping rules](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_shipping_rules",
        "slug": "count-shipping-rules",
        "title": "Count shipping rules",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of shipping rules that match the listing's filters, as `total`.",
        "description": "Returns the number of shipping rules as `total`, at the top level of the body. The filters of [List shipping rules](" + LIST_PAGE + ") narrow the count the same way.",
        "parameters": FILTERS,
        "responses": {
            "200": {
                "description": "The number of matching shipping rules.",
                "schema": {"$ref": "#/components/schemas/ShippingRuleCount"},
                "example": {"total": 2},
            },
            "400": {"description": "A filter has a value it rejects, such as a `zone_id` that no zone has (reason `invalid_reference`) or a `method` that is not one of its values (reason `invalid_enum`).", "schema": ERROR_REF, "example": BAD_ZONE},
        },
        "example_call": {"query": {"zone_id": 5}},
    },
    {
        "key": "head_shipping_rules_count",
        "slug": "check-the-shipping-rule-count",
        "title": "Check the shipping rule count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Returns `200` and the headers of the shipping rule count, with no body.",
        "description": "Returns `200` with headers only and no body. To read the number, use [Count shipping rules](/api-reference/shipping-rules/count-shipping-rules).",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_rule",
        "slug": "create-a-shipping-rule",
        "title": "Create a shipping rule",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a shipping rule and returns it with its `id`, which other calls take as `shipping_rule_id`.",
        "description": "Send the fields inside `shipping_rule`; only `name` is required. The response is the new rule, with a `Location` header that holds its URL. Send `profile_id` to put the new rule on a shipping profile. Send `suggest_name` as `true` to get the next free name, such as `Metro(1)`, when another rule has the `name`.",
        "parameters": [TRANSACTION_NO],
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new rule under `shipping_rule`, with its `id`, which the other calls take as `shipping_rule_id`. The `Location` header holds the URL of the new rule.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rule": METRO_RULE},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "409": {"description": NAME_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "get_shipping_rule",
        "slug": "retrieve-a-shipping-rule",
        "title": "Retrieve a shipping rule",
        "method": "GET",
        "path": BASE + "/{shipping_rule_id}",
        "summary": "Returns the shipping rule whose `id` you pass as `shipping_rule_id`.",
        "description": "Returns one shipping rule under the `shipping_rule` key, with the same ten fields a listing row has. `shipping_class` and `shipping_rate` each give an `id` and a `name`, or `null` when the rule has none. `zones` and `profiles` list the zones and shipping profiles of the rule, each with an `id` and a `name`. Query parameters you add are ignored.",
        "parameters": [SHIPPING_RULE_ID],
        "responses": {
            "200": {
                "description": "The shipping rule under `shipping_rule`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rule": METRO_RULE},
            },
            "404": {"description": NOT_FOUND_404 + " The message is `Shipping rule not found`, or `No such record: the id must be a plain whole number` for a value that is not a number.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"shipping_rule_id": 31}},
    },
    {
        "key": "head_shipping_rule",
        "slug": "check-a-shipping-rule",
        "title": "Check a shipping rule",
        "method": "HEAD",
        "path": BASE + "/{shipping_rule_id}",
        "summary": "Returns `200` and headers only when the shipping rule exists, and `404` when it does not.",
        "description": "Returns `200` with headers only and no body when a shipping rule has the `shipping_rule_id` you pass, and `404` when none does. To read the rule, use [Retrieve a shipping rule](" + RETRIEVE_PAGE + ").",
        "parameters": [SHIPPING_RULE_ID],
        "responses": {
            "200": {"description": "The shipping rule exists. Headers only, no body."},
            "404": {"description": "No shipping rule has that `shipping_rule_id`. Headers only, no body."},
        },
        "example_call": {"path": {"shipping_rule_id": 31}},
    },
    {
        "key": "update_shipping_rule",
        "slug": "replace-a-shipping-rule",
        "title": "Replace a shipping rule",
        "method": "PUT",
        "path": BASE + "/{shipping_rule_id}",
        "summary": "Replaces a shipping rule with the fields you send in `shipping_rule`, and returns it.",
        "description": "Send the whole rule inside `shipping_rule`. `name`, `description`, `shipping_class`, `shipping_rate` and `zones` are required; `description`, `shipping_class` and `shipping_rate` take `null`, and `zones` takes `[]`. Each required field you leave out is named in the `400` response with the reason `required`. To change only some fields, use [Update a shipping rule](" + UPDATE_PAGE + ").",
        "parameters": [SHIPPING_RULE_ID],
        "body": {"schema": WRITE_BODY, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The rule after the replace, under `shipping_rule`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rule": dict(METRO_RULE, description="Metro and inner west deliveries", zones=[{"id": 5, "name": "Sydney"}, {"id": 6, "name": "Inner West"}], updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": "A required field is missing: `details` has one entry per missing field, with the reason `required`. Or " + WRITE_400[0].lower() + WRITE_400[1:], "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409.split(" Send ")[0], "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_rule_id": 31}},
    },
    {
        "key": "patch_shipping_rule",
        "slug": "update-a-shipping-rule",
        "title": "Update a shipping rule",
        "method": "PATCH",
        "path": BASE + "/{shipping_rule_id}",
        "summary": "Changes only the fields you send inside `shipping_rule` and returns the rule.",
        "description": "Send only the fields to change, inside `shipping_rule`; every field you leave out keeps its value. `zones` is the full new list of zones, not an addition. A `shipping_rate` or `shipping_class` of `null` takes it off the rule, and the rate or class stays in the store. An `id` in the body is rejected with `400`.",
        "parameters": [SHIPPING_RULE_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The rule after the change, under `shipping_rule`. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rule": dict(METRO_RULE, zones=[{"id": 5, "name": "Sydney"}, {"id": 6, "name": "Inner West"}], updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409.split(" Send ")[0], "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_rule_id": 31}},
    },
    {
        "key": "delete_shipping_rule",
        "slug": "delete-a-shipping-rule",
        "title": "Delete a shipping rule",
        "method": "DELETE",
        "path": BASE + "/{shipping_rule_id}",
        "summary": "Deletes a shipping rule permanently. You cannot delete a rule that is on a shipping profile.",
        "description": "Deletes the shipping rule whose `shipping_rule_id` you pass, permanently, and returns `204` with no body. The rule's shipping rate and zones stay. A rule that is on a shipping profile is rejected with `409`, and `details[0].field` is `profile`. A second delete of the same rule returns `404`.",
        "parameters": [SHIPPING_RULE_ID],
        "responses": {
            "204": {"description": "The rule is deleted. No body."},
            "404": {"description": NOT_FOUND_404 + " A rule you already deleted returns it too.", "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": "A shipping profile uses the rule. The `code` is `conflict`, `details[0].code` is `in_use`, `details[0].field` is `profile` and `details[0].value` is the profile's `id`. Take the rule off the profile first.", "schema": ERROR_REF, "example": IN_USE},
        },
        "example_call": {"path": {"shipping_rule_id": 31}},
    },
]

REFERENCE = {"type": "object", "properties": {
    "id": {"type": "integer", "description": "The record's `id`."},
    "name": {"type": "string", "description": "The record's name."},
}}


def references(description):
    return {"type": "array", "description": description, "items": REFERENCE}


SCHEMAS = {
    "ShippingRule": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping rule's `id`, assigned by the store. Pass it as `shipping_rule_id` in a path."},
        "name": {"type": "string", "description": "Unique across the store's shipping rules, in any letter case."},
        "description": {"type": ["string", "null"], "description": "The rule's description, or `null`."},
        "shipping_class": {"oneOf": [REFERENCE, {"type": "null"}], "description": "The shipping class of the rule, or `null` when it has none."},
        "shipping_rate": {"oneOf": [REFERENCE, {"type": "null"}], "description": "The shipping rate of the rule, or `null` when it has none."},
        "zones": references("The zones the rule applies to. An empty list when it has none."),
        "profiles": references("The shipping profiles the rule is on. An empty list when it is on none."),
        "transaction_no": {"type": ["string", "null"], "description": "The transaction number the rule was filed under, or `null`."},
        "created_at": {"type": "string", "description": "When the rule was created, in UTC, such as `2026-11-05T05:02:55Z`."},
        "updated_at": {"type": "string", "description": "When the rule last changed, in UTC."},
    }},
    "ShippingRuleInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required. Unique across the store's shipping rules, in any letter case."},
        "description": {"type": ["string", "null"], "description": "The rule's description. Required on a replace, where `null` is allowed."},
        "shipping_class": {"description": "The `id` of the shipping class, bare as `2` or as `{\"id\": 2}`, or `null` for none. Required on a replace.", "oneOf": [{"type": "integer"}, REFERENCE, {"type": "null"}]},
        "shipping_rate": {"description": "The `id` of the shipping rate, bare as `21` or as `{\"id\": 21}`, or `null` for none. Required on a replace.", "oneOf": [{"type": "integer"}, REFERENCE, {"type": "null"}]},
        "zones": {"type": "array", "description": "The whole list of zones, each by its `id`, bare or as `{\"id\": 5}`, each zone once. `[]` for none. Required on a replace.", "items": {"oneOf": [{"type": "integer"}, REFERENCE]}},
        "profile_id": {"type": "integer", "description": "Only on create. The `id` of a shipping profile to put the new rule on."},
        "transaction_no": {"type": "string", "description": "A transaction number. The `X-Transaction-No` header wins when you send both."},
        "suggest_name": {"type": "boolean", "description": "Only on create. `true` saves the next free name, such as `Metro(1)`, when another rule has the `name`."},
    }},
    "ShippingRulePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of shipping rules that match."},
        "limit": {"type": "integer", "description": "The number of rules per call the store applied."},
        "offset": {"type": "integer", "description": "The number of rules skipped before this call's rules."},
        "has_previous": {"type": "boolean"},
        "has_next": {"type": "boolean", "description": "`true` when a higher `offset` returns more rules."},
    }},
    "ShippingRuleCount": {"type": "object", "properties": {"total": {"type": "integer", "description": "The number of shipping rules that match the filters."}}},
    "ShippingRuleError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string"},
        "details": {"type": "array", "description": "Extra detail, or an empty list. Each entry names the `field` and gives a `code` such as `required`, `unknown_field`, `not_allowed`, `invalid_reference`, `invalid_enum`, `out_of_range`, `invalid_integer`, `duplicate` or `in_use`.", "items": {"type": "object", "properties": {
            "field": {"type": "string"},
            "code": {"type": "string"},
            "message": {"type": ["string", "null"]},
            "value": {"type": ["integer", "string"], "description": "The value you sent, or on an `in_use` error the `id` of the profile that uses the rule."},
        }}},
        "request_id": {"type": "string"},
    }}}},
}
