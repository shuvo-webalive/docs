"""The Shipping rates endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping rates"
SLUG = "shipping-rates"
BASE = "/admin/shipping_rates"
ICON = "money-bill-wave"

OVERVIEW_DESCRIPTION = "List, count, create, replace, update and delete shipping rates: the prices a shipping rule applies, as flat, free, per-price, per-quantity, per-weight or per-variation shipping."
INTRO = "The Shipping rates API has ten endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/shipping_rates`."

LIST_PAGE = "/api-reference/shipping-rates/list-shipping-rates"
RETRIEVE_PAGE = "/api-reference/shipping-rates/retrieve-a-shipping-rate"
REPLACE_PAGE = "/api-reference/shipping-rates/replace-a-shipping-rate"
UPDATE_PAGE = "/api-reference/shipping-rates/update-a-shipping-rate"
DELETE_PAGE = "/api-reference/shipping-rates/delete-a-shipping-rate"

WARNING = (
    "**A shipping rate is deleted permanently, and a rate that a shipping rule uses cannot be deleted.**\n"
    "  [Delete a shipping rate](" + DELETE_PAGE + ") on a rate that a rule uses is rejected with `409`, and the\n"
    "  response names the rule. The rate's `shipping_rules` list shows which rules use it. Delete those rules,\n"
    "  or take the rate off them, first."
)

NOTES = [
    "**Create, replace and update wrap the rate in `shipping_rate`.** Send `{\"shipping_rate\": {...}}`. A body\n"
    "  without the wrapper is rejected with `400`, the reason `required` and the message\n"
    "  `shipping_rate: must be an object`. A field the rate does not have is rejected with `400` and the reason\n"
    "  `unknown_field`, and an `id` in the body with `400` and the reason `not_allowed`. Responses return the\n"
    "  rate inside `shipping_rate`.",
    "**`method` decides which fields a rate takes.** `method` is `flat_rate`, `free_shipping`, `ship_by_price`,\n"
    "  `ship_by_quantity`, `ship_by_weight`, `ship_by_variation` or `shipping_variant`, and it is required. A\n"
    "  `flat_rate` needs `shipping_cost`, and takes `handling_cost` and `additional_rule`. The four `ship_by_...`\n"
    "  methods take their costs per row in `conditions`, and a `shipping_cost` at the top level of the rate is\n"
    "  rejected with `400` and the reason `not_allowed`. `free_shipping` and `shipping_variant` need no cost.\n"
    "  A cost is `{\"amount\": 10, \"type\": \"fixed\"}`, and `type` is `fixed` or `percent`.",
    "**A `conditions` row depends on the method.** A `ship_by_price` or `ship_by_quantity` row has `from`, `to`,\n"
    "  `shipping_cost` and `handling_cost`. A `ship_by_weight` row also has `packet_weight`. A\n"
    "  `ship_by_variation` row has `variation_combination`, a list of `{\"id\": ...}` with a variation's `id`,\n"
    "  instead of `from` and `to`. Rows whose `from` and `to` overlap are rejected with `400` and the reason\n"
    "  `overlapping_range`.",
    "**`free_shipping` always saves `calculate_for_entire_order` as `false`.** The store ignores a `true` you\n"
    "  send. `price_entered_with_tax` keeps the value you send, and the rate's `shipping_cost` and\n"
    "  `additional_rule` read `null`.",
    "**`PUT` replaces a rate, and `PATCH` changes only the fields you send.**\n"
    "  [Replace a shipping rate](" + REPLACE_PAGE + ") needs `name`, `method`, `calculate_for_entire_order` and\n"
    "  `price_entered_with_tax`, the costs the method uses, `handling_cost` and `additional_rule`, and names each\n"
    "  missing field in the `400` response with the reason `required`. `handling_cost` and `additional_rule`\n"
    "  take `null`. To change one field, use [Update a shipping rate](" + UPDATE_PAGE + ").",
    "**A listing returns 20 rates per call unless you send `limit`, and the newest rate comes first.** `limit`\n"
    "  takes `1` to `100`, and `offset` skips rates. To get more, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. A query parameter the listing does not know is ignored.",
    "**A rate created a long time ago can return a `method` other than the seven names.** For example\n"
    "  `FLAT_RATE` or `[sbq, sbq]`, with `shipping_cost` `null` and no rows in `conditions`. Treat any other\n"
    "  value as unknown, and send only the seven names on a write.",
]

SHIPPING_RATE_ID = {
    "name": "shipping_rate_id",
    "in": "path",
    "required": True,
    "description": "The shipping rate's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 21},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "required": False,
    "description": "Optional. A transaction number you choose, such as `TXN-IMPORT-0001`. The store files the new rate under it, and the rate returns it as `transaction_no`. You can also send `transaction_no` inside `shipping_rate`: when you send both, the header wins. Another record may use the same number.",
    "schema": {"type": "string", "example": "TXN-IMPORT-0001"},
}

METHODS = ["flat_rate", "free_shipping", "ship_by_price", "ship_by_quantity", "ship_by_weight", "ship_by_variation", "shipping_variant"]
SORT_FIELDS = ["id", "name", "method", "created_at", "updated_at", "transaction_no"]

SEARCH = {"name": "search", "in": "query", "description": "Keeps only rates whose `name` contains this text.", "schema": {"type": "string", "example": "flat"}}
METHOD_FILTER = {"name": "method", "in": "query", "description": "Keeps only rates with this `method`: `flat_rate`, `free_shipping`, `ship_by_price`, `ship_by_quantity`, `ship_by_weight`, `ship_by_variation` or `shipping_variant`. The old short codes `fs`, `fr`, `sba`, `sbq`, `sbw`, `sbv` and `sv` are also accepted. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": METHODS, "example": "flat_rate"}}
HANDLING_COST = {"name": "handling_cost", "in": "query", "description": "`with_handling` keeps only rates that have a handling cost, and `without_handling` keeps only rates that have none. A `shipping_variant` rate has no costs, so it counts as without. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["with_handling", "without_handling"], "example": "with_handling"}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by. Without it, the newest rate comes first. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of rates per call, from `1` to `100`. Defaults to `20`. `0` is rejected with `400` and the reason `out_of_range`, a value above `100` with `400` and the message `must be from 1 to 100`, and a value that is not a number, such as `all`, with `400` and the reason `invalid_integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of rates to skip, `0` or more.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
FILTERS = [SEARCH, METHOD_FILTER, HANDLING_COST]

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Shipping rate not found")
METHOD_MESSAGE = "must be one of fs, fr, sba, sbq, sbw, sbv, free_shipping, flat_rate, ship_by_price, ship_by_quantity, ship_by_weight, ship_by_variation, sv, shipping_variant, api"
BAD_METHOD = error("invalid_request", "method: " + METHOD_MESSAGE, [{"field": "method", "code": "invalid_enum", "message": METHOD_MESSAGE, "value": "zzz"}])
NO_WRAPPER = error("invalid_request", "shipping_rate: must be an object", [{"field": "shipping_rate", "code": "required", "message": "must be an object"}])
DUPLICATE_NAME = error("conflict", "A shipping rate with this name already exists.", [{"field": "name", "code": "duplicate"}])
IN_USE = error("conflict", "The shipping rate is used by shipping rule 31.", [{"field": "rule", "code": "in_use", "value": 31}])

ERROR_REF = {"$ref": "#/components/schemas/ShippingRateError"}
ROW_REF = {"$ref": "#/components/schemas/ShippingRate"}
ROW_RESPONSE = {"type": "object", "properties": {"shipping_rate": ROW_REF}}
WRITE_BODY = {"type": "object", "required": ["shipping_rate"], "properties": {"shipping_rate": {"$ref": "#/components/schemas/ShippingRateInput"}}}

FLAT_COST = {"amount": 10, "type": "fixed"}
FLAT_HANDLING = {"amount": 5, "type": "percent"}
FLAT_RATE = {
    "id": 21, "name": "Flat 10", "method": "flat_rate", "calculate_for_entire_order": False,
    "price_entered_with_tax": False, "shipping_cost": FLAT_COST, "handling_cost": FLAT_HANDLING,
    "weight_unit": None, "conditions": [],
    "additional_rule": {"enabled": False, "for_each_additional": None, "additional_cost": None},
    "shipping_rules": [{"id": 31, "name": "Metro"}], "transaction_no": None,
    "created_at": "2026-11-05T05:02:55Z", "updated_at": "2026-11-05T05:02:55Z",
}
WEIGHT_RATE = {
    "id": 22, "name": "Weight tiers", "method": "ship_by_weight", "calculate_for_entire_order": False,
    "price_entered_with_tax": False, "shipping_cost": None, "handling_cost": None, "weight_unit": "pounds",
    "conditions": [
        {"from": 0, "to": 5, "shipping_cost": {"amount": 12, "type": "fixed"}, "handling_cost": {"amount": 0, "type": "fixed"}, "packet_weight": 1},
        {"from": 5, "to": 10, "shipping_cost": {"amount": 18, "type": "fixed"}, "handling_cost": {"amount": 0, "type": "fixed"}, "packet_weight": 1},
    ],
    "additional_rule": {"enabled": False, "for_each_additional": None, "additional_cost": None},
    "shipping_rules": [], "transaction_no": None,
    "created_at": "2026-11-05T05:10:11Z", "updated_at": "2026-11-05T05:10:11Z",
}
SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"shipping_rate": {"name": "Flat 10", "method": "flat_rate", "shipping_cost": FLAT_COST, "handling_cost": FLAT_HANDLING}}
REPLACE_BODY = {"shipping_rate": {
    "name": "Flat 12", "method": "flat_rate", "calculate_for_entire_order": False, "price_entered_with_tax": False,
    "shipping_cost": {"amount": 12, "type": "fixed"}, "handling_cost": FLAT_HANDLING,
    "additional_rule": {"enabled": False},
}}
PATCH_BODY = {"shipping_rate": {"shipping_cost": {"amount": 12, "type": "fixed"}}}

WRITE_400 = "The body is not wrapped in `shipping_rate` (reason `required`), a field is unknown (`unknown_field`) or an `id` is sent (`not_allowed`), `method` is missing or not one of the seven names, a `flat_rate` has no `shipping_cost` (`required`), a `ship_by_...` rate has a `shipping_cost` at the top level (`not_allowed`), the `conditions` rows overlap (`overlapping_range`), a cost is negative or not a number, `type` is not `fixed` or `percent`, a weight row has no `packet_weight`, a variation row has no `variation_combination`, a boolean is not `true` or `false`, or `additional_rule.enabled` is `true` without a `for_each_additional` of `1` or more and an `additional_cost` of `0` or more. The `code` is `invalid_request`."
WRITE_409 = "Another shipping rate already has that `name`, in any letter case. The `code` is `conflict`, `details[0].code` is `duplicate` and the message is `A shipping rate with this name already exists.` Send `suggest_name` as `true` to get the next free name, such as `Flat 10(1)`, instead. Or `shipping_rule_id` names a rule that already has a rate: `details[0].code` is `in_use` and the message names the rule and its rate."
NAME_409 = "Another shipping rate already has that `name`, in any letter case. The `code` is `conflict` and `details[0].code` is `duplicate`."
NOT_FOUND_404 = "No shipping rate has that `shipping_rate_id`, or the value is not a plain whole number. The `code` is `not_found`."

ENDPOINTS = [
    {
        "key": "list_shipping_rates",
        "slug": "list-shipping-rates",
        "title": "List shipping rates",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 shipping rates per call, newest first, with paging details.",
        "description": "Returns the shipping rates in `shipping_rates`, 20 per call unless you send `limit`, and a `pagination` block. The newest rate comes first unless you send `sort` and `order`. Filter with `search`, `method` and `handling_cost`. A query parameter the listing does not know is ignored. When several parameters are invalid, the `400` response lists each one in `details`.",
        "parameters": FILTERS + [SORT, ORDER, LIMIT, OFFSET],
        "responses": {
            "200": {
                "description": "The rates on this call in `shipping_rates`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. Each rate has the same fields [Retrieve a shipping rate](" + RETRIEVE_PAGE + ") returns.",
                "schema": {"type": "object", "properties": {
                    "shipping_rates": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/ShippingRatePagination"},
                }},
                "example": {"shipping_rates": [WEIGHT_RATE, FLAT_RATE], "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "A parameter has a value the listing rejects: `method`, `handling_cost`, `sort` or `order` is not one of its values, or `limit` or `offset` is out of range. The `code` is `invalid_request`, and `details` has one entry per rejected parameter with its `field`, `code`, `message` and `value`.", "schema": ERROR_REF, "example": BAD_METHOD},
        },
        "example_call": {"query": {"method": "flat_rate", "handling_cost": "with_handling", "sort": "name", "order": "asc"}},
    },
    {
        "key": "head_shipping_rates",
        "slug": "check-the-shipping-rates-list",
        "title": "Check the shipping rates list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns `200` and the headers of the shipping rates listing, with no body.",
        "description": "Returns `200` with headers only and no body. To read the rates, use [List shipping rates](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_shipping_rates",
        "slug": "count-shipping-rates",
        "title": "Count shipping rates",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of shipping rates that match the listing's filters, as `total`.",
        "description": "Returns the number of shipping rates as `total`, at the top level of the body. The `search`, `method` and `handling_cost` filters of [List shipping rates](" + LIST_PAGE + ") narrow the count the same way.",
        "parameters": FILTERS,
        "responses": {
            "200": {
                "description": "The number of matching shipping rates.",
                "schema": {"$ref": "#/components/schemas/ShippingRateCount"},
                "example": {"total": 2},
            },
            "400": {"description": "`method` or `handling_cost` has a value the filter rejects. The `code` is `invalid_request` and the reason is `invalid_enum`.", "schema": ERROR_REF, "example": BAD_METHOD},
        },
        "example_call": {"query": {"method": "flat_rate"}},
    },
    {
        "key": "head_shipping_rates_count",
        "slug": "check-the-shipping-rate-count",
        "title": "Check the shipping rate count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Returns `200` and the headers of the shipping rate count, with no body.",
        "description": "Returns `200` with headers only and no body. To read the number, use [Count shipping rates](/api-reference/shipping-rates/count-shipping-rates).",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_rate",
        "slug": "create-a-shipping-rate",
        "title": "Create a shipping rate",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a shipping rate and returns it with its `id`, which other calls take as `shipping_rate_id`.",
        "description": "Send the fields inside `shipping_rate`; `name` and `method` are required, and the costs depend on the `method`. The response is the new rate, with a `Location` header that holds its URL. Send `shipping_rule_id` to attach the new rate to a shipping rule that has no rate yet. Send `suggest_name` as `true` to get the next free name, such as `Flat 10(1)`, when another rate has the `name`.",
        "parameters": [TRANSACTION_NO],
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new rate under `shipping_rate`, with its `id`, which the other calls take as `shipping_rate_id`. The `Location` header holds the URL of the new rate.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rate": FLAT_RATE},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "409": {"description": WRITE_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "get_shipping_rate",
        "slug": "retrieve-a-shipping-rate",
        "title": "Retrieve a shipping rate",
        "method": "GET",
        "path": BASE + "/{shipping_rate_id}",
        "summary": "Returns the shipping rate whose `id` you pass as `shipping_rate_id`.",
        "description": "Returns one shipping rate under the `shipping_rate` key, with the same fourteen fields a listing row has. `shipping_rules` lists the rules that use the rate, each with its `id` and `name`. Query parameters you add are ignored.",
        "parameters": [SHIPPING_RATE_ID],
        "responses": {
            "200": {
                "description": "The shipping rate under `shipping_rate`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rate": WEIGHT_RATE},
            },
            "404": {"description": NOT_FOUND_404 + " The message is `Shipping rate not found`, or `No such record: the id must be a plain whole number` for a value that is not a number.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"shipping_rate_id": 21}},
    },
    {
        "key": "head_shipping_rate",
        "slug": "check-a-shipping-rate",
        "title": "Check a shipping rate",
        "method": "HEAD",
        "path": BASE + "/{shipping_rate_id}",
        "summary": "Returns `200` and headers only when the shipping rate exists, and `404` when it does not.",
        "description": "Returns `200` with headers only and no body when a shipping rate has the `shipping_rate_id` you pass, and `404` when none does. To read the rate, use [Retrieve a shipping rate](" + RETRIEVE_PAGE + ").",
        "parameters": [SHIPPING_RATE_ID],
        "responses": {
            "200": {"description": "The shipping rate exists. Headers only, no body."},
            "404": {"description": "No shipping rate has that `shipping_rate_id`. Headers only, no body."},
        },
        "example_call": {"path": {"shipping_rate_id": 21}},
    },
    {
        "key": "update_shipping_rate",
        "slug": "replace-a-shipping-rate",
        "title": "Replace a shipping rate",
        "method": "PUT",
        "path": BASE + "/{shipping_rate_id}",
        "summary": "Replaces a shipping rate with the fields you send in `shipping_rate`, and returns it.",
        "description": "Send the whole rate inside `shipping_rate`. `name`, `method`, `calculate_for_entire_order` and `price_entered_with_tax` are required, with the costs the `method` uses, `handling_cost` and `additional_rule`; `handling_cost` and `additional_rule` take `null`. Each required field you leave out is named in the `400` response with the reason `required` and the message `PUT replaces the whole rate; send every field or use PATCH`. To change only some fields, use [Update a shipping rate](" + UPDATE_PAGE + ").",
        "parameters": [SHIPPING_RATE_ID],
        "body": {"schema": WRITE_BODY, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The rate after the replace, under `shipping_rate`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rate": dict(FLAT_RATE, name="Flat 12", shipping_cost={"amount": 12, "type": "fixed"}, updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": "A required field is missing: `details` has one entry per missing field, with the reason `required`. Or " + WRITE_400[0].lower() + WRITE_400[1:], "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_rate_id": 21}},
    },
    {
        "key": "patch_shipping_rate",
        "slug": "update-a-shipping-rate",
        "title": "Update a shipping rate",
        "method": "PATCH",
        "path": BASE + "/{shipping_rate_id}",
        "summary": "Changes only the fields you send inside `shipping_rate` and returns the rate.",
        "description": "Send only the fields to change, inside `shipping_rate`; every field you leave out keeps its value. An empty `shipping_rate` object returns `200` and changes nothing. An `id` in the body is rejected with `400`.",
        "parameters": [SHIPPING_RATE_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The rate after the change, under `shipping_rate`. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_rate": dict(FLAT_RATE, shipping_cost={"amount": 12, "type": "fixed"}, updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409, "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_rate_id": 21}},
    },
    {
        "key": "delete_shipping_rate",
        "slug": "delete-a-shipping-rate",
        "title": "Delete a shipping rate",
        "method": "DELETE",
        "path": BASE + "/{shipping_rate_id}",
        "summary": "Deletes a shipping rate permanently. You cannot delete a rate that a shipping rule uses.",
        "description": "Deletes the shipping rate whose `shipping_rate_id` you pass, permanently, and returns `204` with no body. A rate that a shipping rule uses is rejected with `409`, and `details[0].field` is `rule`. A second delete of the same rate returns `404`.",
        "parameters": [SHIPPING_RATE_ID],
        "responses": {
            "204": {"description": "The rate is deleted. No body."},
            "404": {"description": NOT_FOUND_404 + " A rate you already deleted returns it too.", "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": "A shipping rule uses the rate. The `code` is `conflict`, `details[0].code` is `in_use`, `details[0].field` is `rule` and `details[0].value` is the rule's `id`. Delete the rule, or take the rate off it, first.", "schema": ERROR_REF, "example": IN_USE},
        },
        "example_call": {"path": {"shipping_rate_id": 21}},
    },
]

COST = {"type": "object", "properties": {
    "amount": {"type": "number", "description": "The cost, `0` or more."},
    "type": {"type": "string", "enum": ["fixed", "percent"], "description": "`fixed` is a money amount, and `percent` is a percentage."},
}}
ADDITIONAL_RULE = {"type": "object", "properties": {
    "enabled": {"type": "boolean", "description": "`true` to charge an extra cost for each further item. Needs `for_each_additional` and `additional_cost`."},
    "for_each_additional": {"type": ["integer", "null"], "description": "The number of further items each extra charge covers, `1` or more. `null` when `enabled` is `false`."},
    "additional_cost": {"type": ["number", "null"], "description": "The extra cost, `0` or more. `null` when `enabled` is `false`."},
}}
CONDITION = {"type": "object", "description": "One row of a `ship_by_...` rate. A `ship_by_price` or `ship_by_quantity` row has `from`, `to`, `shipping_cost` and `handling_cost`. A `ship_by_weight` row also has `packet_weight`. A `ship_by_variation` row has `variation_combination`, a list of `{\"id\": ...}`, instead of `from` and `to`.", "properties": {
    "from": {"type": "number", "description": "The start of the range. Must not be above `to`."},
    "to": {"type": "number", "description": "The end of the range. Rows must not overlap."},
    "packet_weight": {"type": "number", "description": "Only on a `ship_by_weight` row. Required there."},
    "variation_combination": {"type": "array", "description": "Only on a `ship_by_variation` row. Required there. Send each variation as `{\"id\": 1}`; a response also returns its `name`.", "items": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}}}},
    "shipping_cost": COST,
    "handling_cost": COST,
}}

SCHEMAS = {
    "ShippingRate": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping rate's `id`, assigned by the store. Pass it as `shipping_rate_id` in a path."},
        "name": {"type": "string", "description": "Unique across the store's shipping rates, in any letter case."},
        "method": {"type": "string", "description": "`flat_rate`, `free_shipping`, `ship_by_price`, `ship_by_quantity`, `ship_by_weight`, `ship_by_variation` or `shipping_variant`. A rate created long ago can return another value."},
        "calculate_for_entire_order": {"type": "boolean", "description": "`true` to work out the cost for the whole order instead of per item. Always `false` on `free_shipping`."},
        "price_entered_with_tax": {"type": "boolean", "description": "`true` when the costs you entered include tax."},
        "shipping_cost": {"oneOf": [COST, {"type": "null"}], "description": "The shipping cost of a `flat_rate`. `null` on every other method, where the cost is per row in `conditions`."},
        "handling_cost": {"oneOf": [COST, {"type": "null"}], "description": "The handling cost of a `flat_rate`. `null` when none was sent, and on the `ship_by_...` methods, where it is per row."},
        "weight_unit": {"type": ["string", "null"], "description": "The store's weight unit, such as `pounds`, on a `ship_by_weight` rate. `null` on every other method."},
        "conditions": {"type": "array", "description": "The rows of a `ship_by_...` rate. An empty list on the other methods.", "items": CONDITION},
        "additional_rule": {"oneOf": [ADDITIONAL_RULE, {"type": "null"}], "description": "The extra cost for further items. `{\"enabled\": false, ...}` with `null` values on a `flat_rate` when you did not send one, and `null` on `free_shipping` and `shipping_variant`."},
        "shipping_rules": {"type": "array", "description": "The shipping rules that use this rate.", "items": {"$ref": "#/components/schemas/ShippingRateRule"}},
        "transaction_no": {"type": ["string", "null"], "description": "The transaction number the rate was filed under, or `null`."},
        "created_at": {"type": "string", "description": "When the rate was created, in UTC, such as `2026-11-05T05:02:55Z`."},
        "updated_at": {"type": "string", "description": "When the rate last changed, in UTC."},
    }},
    "ShippingRateRule": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping rule's `id`."},
        "name": {"type": "string", "description": "The shipping rule's name."},
    }},
    "ShippingRateInput": {"type": "object", "required": ["name", "method"], "properties": {
        "name": {"type": "string", "description": "Required. Unique across the store's shipping rates, in any letter case."},
        "method": {"type": "string", "enum": METHODS, "description": "Required. Decides which of the other fields the rate takes."},
        "calculate_for_entire_order": {"type": "boolean", "description": "`true` or `false`. Always saved as `false` on `free_shipping`."},
        "price_entered_with_tax": {"type": "boolean", "description": "`true` or `false`."},
        "shipping_cost": dict(COST, description="Required on a `flat_rate`. Rejected on the `ship_by_...` methods, where each row in `conditions` has its own."),
        "handling_cost": dict(COST, description="Optional on a `flat_rate`."),
        "conditions": {"type": "array", "description": "The rows of a `ship_by_...` rate. Rows must not overlap.", "items": CONDITION},
        "additional_rule": dict(ADDITIONAL_RULE, description="The extra cost for further items. When `enabled` is `true`, `for_each_additional` must be `1` or more and `additional_cost` `0` or more."),
        "shipping_rule_id": {"type": "integer", "description": "Only on create. The `id` of a shipping rule that has no rate; the new rate is attached to it."},
        "transaction_no": {"type": "string", "description": "A transaction number. The `X-Transaction-No` header wins when you send both."},
        "suggest_name": {"type": "boolean", "description": "Only on create. `true` saves the next free name, such as `Flat 10(1)`, when another rate has the `name`."},
    }},
    "ShippingRatePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of shipping rates that match."},
        "limit": {"type": "integer", "description": "The number of rates per call the store applied."},
        "offset": {"type": "integer", "description": "The number of rates skipped before this call's rates."},
        "has_previous": {"type": "boolean"},
        "has_next": {"type": "boolean", "description": "`true` when a higher `offset` returns more rates."},
    }},
    "ShippingRateCount": {"type": "object", "properties": {"total": {"type": "integer", "description": "The number of shipping rates that match the filters."}}},
    "ShippingRateError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string"},
        "details": {"type": "array", "description": "Extra detail, or an empty list. Each entry names the `field` and gives a `code` such as `required`, `unknown_field`, `not_allowed`, `overlapping_range`, `invalid_enum`, `out_of_range`, `invalid_integer`, `duplicate` or `in_use`.", "items": {"type": "object", "properties": {
            "field": {"type": "string"},
            "code": {"type": "string"},
            "message": {"type": ["string", "null"]},
            "value": {"type": ["integer", "string"], "description": "The value you sent, or on an `in_use` error the `id` of the rule that uses the rate."},
        }}},
        "request_id": {"type": "string"},
    }}}},
}
