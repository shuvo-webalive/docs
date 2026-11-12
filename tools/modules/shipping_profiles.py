"""The Shipping profiles endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping profiles"
SLUG = "shipping-profiles"
BASE = "/admin/shipping_profiles"
ICON = "truck-fast"

OVERVIEW_DESCRIPTION = "List, count, create, replace, update and delete shipping profiles, choose the default profile, and build a profile with its rules and rates in one call."
INTRO = "The Shipping profiles API has eleven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/shipping_profiles`."

LIST_PAGE = "/api-reference/shipping-profiles/list-shipping-profiles"
RETRIEVE_PAGE = "/api-reference/shipping-profiles/retrieve-a-shipping-profile"
REPLACE_PAGE = "/api-reference/shipping-profiles/replace-a-shipping-profile"
UPDATE_PAGE = "/api-reference/shipping-profiles/update-a-shipping-profile"
DELETE_PAGE = "/api-reference/shipping-profiles/delete-a-shipping-profile"
WIZARD_PAGE = "/api-reference/shipping-profiles/create-a-shipping-profile-with-the-wizard"
RATE_CREATE_PAGE = "/api-reference/shipping-rates/create-a-shipping-rate"

WARNING = (
    "**Sending `default` as `true` changes the default shipping profile for the whole store.**\n"
    "  [Create a shipping profile](/api-reference/shipping-profiles/create-a-shipping-profile) or\n"
    "  [Update a shipping profile](" + UPDATE_PAGE + ") with `default` set to `true` makes that profile the\n"
    "  default and sets `default` to `false` on the profile that was the default. Before you call either, find\n"
    "  the current default, the profile in [List shipping profiles](" + LIST_PAGE + ") with `default=true`, so\n"
    "  you can set it back. You cannot set `default` to `false` on the default profile, and you cannot delete\n"
    "  it: both are rejected with `409`. Make another profile the default first."
)

NOTES = [
    "**A new profile is not used until it is the default.** Creating a profile, even with rules for the order's zone, does not\n"
    "  let orders ship. Set it as `default_shipping_profile` with [Update shipping settings](/api-reference/shipping-settings/update-shipping-settings); until then\n"
    "  orders are refused with `400` and the message `We do not ship to your location.`",
    "**Create, replace, update and the wizard wrap the profile in `shipping_profile`.** Send\n"
    "  `{\"shipping_profile\": {...}}`. A body without the wrapper is rejected with `400`. A field the profile\n"
    "  does not have is rejected with `400`, and so is an `id` in the body. Responses return the profile inside\n"
    "  `shipping_profile`.",
    "**`rule_preference` decides which rule applies when several match.** It is `product_assigned_rule`, the\n"
    "  default, `lowest_shipping_cost_rule` or `highest_shipping_cost_rule`. The short codes `hp`, `lsc` and\n"
    "  `hsc` are accepted on a write, and the profile returns the long names. Any other value is rejected\n"
    "  with `400`.",
    "**`shipping_rules` is the whole list of rule `id` values, and each rule appears once.** Send the `id` of\n"
    "  each shipping rule. An unknown `id` or a repeated one is rejected with `400`. An update with\n"
    "  `\"shipping_rules\": []` takes every rule off the profile, and the rules stay in the store. A profile\n"
    "  returns each rule with its `id`, its `name` and its shipping rate, or `null` when the rule has none.",
    "**`PUT` replaces a profile, and `PATCH` changes only the fields you send.**\n"
    "  [Replace a shipping profile](" + REPLACE_PAGE + ") needs `name`, `description`, `rule_preference` and\n"
    "  `shipping_rules`, and names each missing field in the `400` response with the reason `required`.\n"
    "  `description` takes `null`. To change one field, use [Update a shipping profile](" + UPDATE_PAGE + ").",
    "**The wizard creates a profile, its rules and their rates in one call.** [Create a shipping profile with the\n"
    "  wizard](" + WIZARD_PAGE + ") returns `201` for a new profile `name`. When a profile already has that\n"
    "  `name`, it adds the new rules to that profile and returns `200`. Any bad value saves nothing. Only a\n"
    "  `POST` works on the wizard path: a `GET` or `HEAD` is rejected with `405`.",
    "**A listing returns 20 profiles per call unless you send `limit`, and the newest profile comes first.**\n"
    "  `limit` takes `1` to `100`, and `offset` skips profiles. To get more, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. A query parameter the listing does not know is ignored.",
]

SHIPPING_PROFILE_ID = {
    "name": "shipping_profile_id",
    "in": "path",
    "required": True,
    "description": "The shipping profile's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 12},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "required": False,
    "description": "Optional. A transaction number you choose, such as `TXN-IMPORT-0001`. The store files the new profile under it, and the profile returns it as `transaction_no`. You can also send `transaction_no` inside `shipping_profile`: when you send both, the header wins. Another record may use the same number.",
    "schema": {"type": "string", "example": "TXN-IMPORT-0001"},
}

RULE_PREFERENCES = ["product_assigned_rule", "lowest_shipping_cost_rule", "highest_shipping_cost_rule"]
SORT_FIELDS = ["id", "name", "description", "rule_preference", "created_at", "updated_at", "transaction_no"]

SEARCH = {"name": "search", "in": "query", "description": "Keeps only profiles whose `name` contains this text.", "schema": {"type": "string", "example": "metro"}}
DEFAULT_FILTER = {"name": "default", "in": "query", "description": "Send `true` to keep only the default profile, or `false` to keep every other profile, in any letter case. Any other value is rejected with `400` and the reason `invalid_boolean`.", "schema": {"type": "boolean", "example": True}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by. Without it, the newest profile comes first. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of profiles per call, from `1` to `100`. Defaults to `20`. `0` is rejected with `400` and the reason `out_of_range`, a value above `100` with `400` and the message `must be from 1 to 100`, and a value that is not a number, such as `all`, with `400` and the reason `invalid_integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of profiles to skip, `0` or more.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
FILTERS = [SEARCH, DEFAULT_FILTER]

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


NOT_FOUND = error("not_found", "Profile not found")
BAD_LIST = error("invalid_request", "3 fields are invalid", [
    {"field": "sort", "code": "invalid_enum", "message": "must be one of id, name, description, rule_preference, rulePrecedence, created_at, created, updated_at, updated, transaction_no, transactionNo", "value": "zzz"},
    {"field": "order", "code": "invalid_enum", "message": "must be asc or desc", "value": "up"},
    {"field": "default", "code": "invalid_boolean", "message": "must be true or false", "value": "maybe"},
])
NO_WRAPPER = error("invalid_request", "shipping_profile: must be an object", [{"field": "shipping_profile", "code": "required", "message": "must be an object"}])
DUPLICATE_NAME = error("conflict", "A shipping profile with this name already exists.", [{"field": "name", "code": "duplicate"}])
DEFAULT_PROFILE = error("conflict", "Make another profile the default first.", [{"field": "default", "code": "default_profile"}])

ERROR_REF = {"$ref": "#/components/schemas/ShippingProfileError"}
ROW_REF = {"$ref": "#/components/schemas/ShippingProfile"}
ROW_RESPONSE = {"type": "object", "properties": {"shipping_profile": ROW_REF}}
WRITE_BODY = {"type": "object", "required": ["shipping_profile"], "properties": {"shipping_profile": {"$ref": "#/components/schemas/ShippingProfileInput"}}}
WIZARD_BODY = {"type": "object", "required": ["shipping_profile"], "properties": {"shipping_profile": {"$ref": "#/components/schemas/ShippingProfileWizardInput"}}}

METRO_PROFILE = {
    "id": 12, "name": "Metro profile", "description": "Metro deliveries", "rule_preference": "product_assigned_rule",
    "default": False, "rules_count": 1,
    "shipping_rules": [{"id": 31, "name": "Metro", "shipping_rate": {"id": 21, "name": "Flat 10"}}],
    "transaction_no": None, "created_at": "2026-11-05T05:02:55Z", "updated_at": "2026-11-05T05:02:55Z",
}
STORE_DEFAULT_PROFILE = {
    "id": 3, "name": "Standard shipping", "description": None, "rule_preference": "product_assigned_rule",
    "default": True, "rules_count": 0, "shipping_rules": [],
    "transaction_no": None, "created_at": "2026-05-03T08:09:22Z", "updated_at": "2026-05-03T08:09:22Z",
}
SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"shipping_profile": {"name": "Metro profile", "description": "Metro deliveries", "rule_preference": "product_assigned_rule", "shipping_rules": [31]}}
REPLACE_BODY = {"shipping_profile": {"name": "Metro profile", "description": "Metro and inner west deliveries", "rule_preference": "lowest_shipping_cost_rule", "shipping_rules": [31]}}
PATCH_BODY = {"shipping_profile": {"default": True}}
WIZARD_EXAMPLE = {"shipping_profile": {
    "name": "Wizard profile", "description": "Built in one call", "rule_preference": "product_assigned_rule",
    "shipping_rules": [{
        "name": "Metro delivery", "description": "Metro deliveries", "shipping_class": 2,
        "zones": [{"id": 5}, {"name": "Inner West"}],
        "shipping_rate": {"name": "Metro flat rate", "method": "flat_rate", "shipping_cost": {"amount": 10, "type": "fixed"}, "handling_cost": {"amount": 5, "type": "percent"}},
    }],
}}

WRITE_400 = "The body is not wrapped in `shipping_profile`, a field is unknown or an `id` is sent, `name` is missing, `rule_preference` is not one of its values, `default` is not `true` or `false` (reason `invalid_boolean`), or `shipping_rules` holds an unknown or a repeated rule `id`. The `code` is `invalid_request`."
NAME_409 = "Another shipping profile already has that `name`, in any letter case. The `code` is `conflict` and `details[0].code` is `duplicate`."
NOT_FOUND_404 = "No shipping profile has that `shipping_profile_id`, or the value is not a plain whole number. The `code` is `not_found`."
DEFAULT_409 = "You sent `default` as `false` on the default profile. The `code` is `conflict` and `details[0].code` is `default_profile`. Make another profile the default first."

ENDPOINTS = [
    {
        "key": "list_shipping_profiles",
        "slug": "list-shipping-profiles",
        "title": "List shipping profiles",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 shipping profiles per call, newest first, with paging details.",
        "description": "Returns the shipping profiles in `shipping_profiles`, 20 per call unless you send `limit`, and a `pagination` block. The newest profile comes first unless you send `sort` and `order`. Filter with `search` and `default`. A query parameter the listing does not know is ignored. When several parameters are invalid, the `400` response lists each one in `details`.",
        "parameters": FILTERS + [SORT, ORDER, LIMIT, OFFSET],
        "responses": {
            "200": {
                "description": "The profiles on this call in `shipping_profiles`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. Each profile has the same fields [Retrieve a shipping profile](" + RETRIEVE_PAGE + ") returns.",
                "schema": {"type": "object", "properties": {
                    "shipping_profiles": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/ShippingProfilePagination"},
                }},
                "example": {"shipping_profiles": [METRO_PROFILE, STORE_DEFAULT_PROFILE], "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "A parameter has a value the listing rejects: `sort` or `order` is not one of its values, `default` is not `true` or `false`, or `limit` or `offset` is out of range. The `code` is `invalid_request`, and `details` has one entry per rejected parameter with its `field`, `code`, `message` and `value`.", "schema": ERROR_REF, "example": BAD_LIST},
        },
        "example_call": {"query": {"search": "metro", "sort": "name", "order": "asc", "limit": 20}},
    },
    {
        "key": "head_shipping_profiles",
        "slug": "check-the-shipping-profiles-list",
        "title": "Check the shipping profiles list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns `200` and the headers of the shipping profiles listing, with no body.",
        "description": "Returns `200` with headers only and no body. To read the profiles, use [List shipping profiles](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_shipping_profiles",
        "slug": "count-shipping-profiles",
        "title": "Count shipping profiles",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of shipping profiles that match the listing's filters, as `total`.",
        "description": "Returns the number of shipping profiles as `total`, at the top level of the body. The `search` and `default` filters of [List shipping profiles](" + LIST_PAGE + ") narrow the count the same way.",
        "parameters": FILTERS,
        "responses": {
            "200": {
                "description": "The number of matching shipping profiles.",
                "schema": {"$ref": "#/components/schemas/ShippingProfileCount"},
                "example": {"total": 2},
            },
            "400": {"description": "`default` is not `true` or `false`. The `code` is `invalid_request` and the reason is `invalid_boolean`.", "schema": ERROR_REF, "example": BAD_LIST},
        },
        "example_call": {"query": {"default": "true"}},
    },
    {
        "key": "head_shipping_profiles_count",
        "slug": "check-the-shipping-profile-count",
        "title": "Check the shipping profile count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Returns `200` and the headers of the shipping profile count, with no body.",
        "description": "Returns `200` with headers only and no body. To read the number, use [Count shipping profiles](/api-reference/shipping-profiles/count-shipping-profiles).",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_profile",
        "slug": "create-a-shipping-profile",
        "title": "Create a shipping profile",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a shipping profile and returns it with its `id`, which other calls take as `shipping_profile_id`.",
        "description": "Send the fields inside `shipping_profile`; only `name` is required. `rule_preference` defaults to `product_assigned_rule`, and `shipping_rules` lists the `id` of each rule to put on the profile. The response is the new profile, with a `Location` header that holds its URL. Send `default` as `true` to make it the store default. Send `suggest_name` as `true` to get the next free name, such as `Metro profile(1)`, when another profile has the `name`.",
        "parameters": [TRANSACTION_NO],
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new profile under `shipping_profile`, with its `id`, which the other calls take as `shipping_profile_id`. The `Location` header holds the URL of the new profile.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": METRO_PROFILE},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "409": {"description": NAME_409 + " Send `suggest_name` as `true` to get the next free name instead.", "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {},
    },
    {
        "key": "create_shipping_profile_wizard",
        "slug": "create-a-shipping-profile-with-the-wizard",
        "title": "Create a shipping profile with the wizard",
        "method": "POST",
        "path": BASE + "/wizard",
        "summary": "Creates a shipping profile with its rules, rates and zones in one call.",
        "description": "Send the profile inside `shipping_profile`, with `shipping_rules` as a list of rules to create. Each rule needs a `name`, and takes a `description`, a `shipping_class` `id`, `zones` and a `shipping_rate` that has a `name`, a `method` and the cost fields described in [Create a shipping rate](" + RATE_CREATE_PAGE + "). A zone is `{\"id\": 5}` for an existing zone, or `{\"name\": \"Inner West\"}`, which creates a new zone with that name. A new profile `name` returns `201` with a `Location` header. A `name` that a profile already has adds the new rules to that profile, keeps its `id` and returns `200`. If any value is bad, nothing is saved. A body with only `{\"shipping_profile\": {\"name\": \"...\"}}` creates a profile with no rules. The response does not list the zones the call created: read them from the `zones` of each rule, with [Retrieve a shipping rule](/api-reference/shipping-rules/retrieve-a-shipping-rule).",
        "body": {"schema": WIZARD_BODY, "example": WIZARD_EXAMPLE},
        "responses": {
            "201": {
                "description": "A profile with that `name` did not exist, so the call created it, its rules and their rates. The profile comes back under `shipping_profile`, and each entry of `shipping_rules` has the new rule's `id` and `name` and its shipping rate's `id` and `name`. The `Location` header holds the URL of the new profile.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": {
                    "id": 13, "name": "Wizard profile", "description": "Built in one call", "rule_preference": "product_assigned_rule",
                    "default": False, "rules_count": 1,
                    "shipping_rules": [{"id": 33, "name": "Metro delivery", "shipping_rate": {"id": 23, "name": "Metro flat rate"}}],
                    "transaction_no": None, "created_at": "2026-11-05T07:00:00Z", "updated_at": "2026-11-05T07:00:00Z",
                }},
            },
            "200": {
                "description": "A profile already had that `name`, so the call added the new rules to it. The profile keeps its `id`, and `rules_count` includes the new rules. The body has the same fields as the `201` response.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": dict(METRO_PROFILE, id=13, name="Wizard profile", rules_count=2, shipping_rules=[
                    {"id": 33, "name": "Metro delivery", "shipping_rate": {"id": 23, "name": "Metro flat rate"}},
                    {"id": 34, "name": "Metro express", "shipping_rate": {"id": 24, "name": "Metro express rate"}},
                ])},
            },
            "400": {"description": "The body is not wrapped in `shipping_profile`, a profile field is unknown, `rule_preference` is not one of its values, a rule has no `name`, a rate has a bad `method`, cost or `conditions` row, or a class or zone `id` is the `id` of no record. The `code` is `invalid_request`, and nothing is saved.", "schema": ERROR_REF, "example": NO_WRAPPER},
            "405": {"description": "You sent `GET` or `HEAD` to the wizard path. Only `POST` works. The `code` is `method_not_allowed`, and the `Allow` header is `POST, OPTIONS`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_shipping_profile",
        "slug": "retrieve-a-shipping-profile",
        "title": "Retrieve a shipping profile",
        "method": "GET",
        "path": BASE + "/{shipping_profile_id}",
        "summary": "Returns the shipping profile whose `id` you pass as `shipping_profile_id`.",
        "description": "Returns one shipping profile under the `shipping_profile` key, with the same ten fields a listing row has. `shipping_rules` lists the rules on the profile, each with its `id`, its `name` and its shipping rate, or `null` when the rule has none. Query parameters you add are ignored.",
        "parameters": [SHIPPING_PROFILE_ID],
        "responses": {
            "200": {
                "description": "The shipping profile under `shipping_profile`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": METRO_PROFILE},
            },
            "404": {"description": NOT_FOUND_404 + " The message is `Profile not found`, or `No such record: the id must be a plain whole number` for a value that is not a number.", "schema": ERROR_REF, "example": NOT_FOUND},
        },
        "example_call": {"path": {"shipping_profile_id": 12}},
    },
    {
        "key": "head_shipping_profile",
        "slug": "check-a-shipping-profile",
        "title": "Check a shipping profile",
        "method": "HEAD",
        "path": BASE + "/{shipping_profile_id}",
        "summary": "Returns `200` and headers only when the shipping profile exists, and `404` when it does not.",
        "description": "Returns `200` with headers only and no body when a shipping profile has the `shipping_profile_id` you pass, and `404` when none does. To read the profile, use [Retrieve a shipping profile](" + RETRIEVE_PAGE + ").",
        "parameters": [SHIPPING_PROFILE_ID],
        "responses": {
            "200": {"description": "The shipping profile exists. Headers only, no body."},
            "404": {"description": "No shipping profile has that `shipping_profile_id`. Headers only, no body."},
        },
        "example_call": {"path": {"shipping_profile_id": 12}},
    },
    {
        "key": "update_shipping_profile",
        "slug": "replace-a-shipping-profile",
        "title": "Replace a shipping profile",
        "method": "PUT",
        "path": BASE + "/{shipping_profile_id}",
        "summary": "Replaces a shipping profile with the fields you send in `shipping_profile`, and returns it.",
        "description": "Send the whole profile inside `shipping_profile`. `name`, `description`, `rule_preference` and `shipping_rules` are required, and `description` takes `null`. Each required field you leave out is named in the `400` response with the reason `required`. `default` and `transaction_no` are not required. To change only some fields, use [Update a shipping profile](" + UPDATE_PAGE + ").",
        "parameters": [SHIPPING_PROFILE_ID],
        "body": {"schema": WRITE_BODY, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The profile after the replace, under `shipping_profile`.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": dict(METRO_PROFILE, description="Metro and inner west deliveries", rule_preference="lowest_shipping_cost_rule", updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": "A required field is missing: `details` has one entry per missing field, with the reason `required`. Or " + WRITE_400[0].lower() + WRITE_400[1:], "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409 + " Or " + DEFAULT_409[0].lower() + DEFAULT_409[1:], "schema": ERROR_REF, "example": DUPLICATE_NAME},
        },
        "example_call": {"path": {"shipping_profile_id": 12}},
    },
    {
        "key": "patch_shipping_profile",
        "slug": "update-a-shipping-profile",
        "title": "Update a shipping profile",
        "method": "PATCH",
        "path": BASE + "/{shipping_profile_id}",
        "summary": "Changes only the fields you send inside `shipping_profile` and returns the profile.",
        "description": "Send only the fields to change, inside `shipping_profile`; every field you leave out keeps its value. `shipping_rules` is the full new list of rule `id` values, and `[]` takes every rule off the profile. `default` set to `true` makes this profile the store default and sets `default` to `false` on the old one. `default` set to `false` on the default profile is rejected with `409`.",
        "parameters": [SHIPPING_PROFILE_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The profile after the change, under `shipping_profile`. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"shipping_profile": dict(METRO_PROFILE, default=True, updated_at="2026-11-05T06:15:00Z")},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": NO_WRAPPER},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": NAME_409 + " Or " + DEFAULT_409[0].lower() + DEFAULT_409[1:], "schema": ERROR_REF, "example": DEFAULT_PROFILE},
        },
        "example_call": {"path": {"shipping_profile_id": 12}},
    },
    {
        "key": "delete_shipping_profile",
        "slug": "delete-a-shipping-profile",
        "title": "Delete a shipping profile",
        "method": "DELETE",
        "path": BASE + "/{shipping_profile_id}",
        "summary": "Deletes a shipping profile permanently. You cannot delete the default profile.",
        "description": "Deletes the shipping profile whose `shipping_profile_id` you pass, permanently, and returns `204` with no body. The profile's rules and zones stay in the store. You cannot delete the default profile: make another profile the default first, or the call is rejected with `409`. A second delete of the same profile returns `404`.",
        "parameters": [SHIPPING_PROFILE_ID],
        "responses": {
            "204": {"description": "The profile is deleted. No body."},
            "404": {"description": NOT_FOUND_404 + " A profile you already deleted returns it too.", "schema": ERROR_REF, "example": NOT_FOUND},
            "409": {"description": "The profile is the default. The `code` is `conflict` and `details[0].code` is `default_profile`. Make another profile the default first with [Update a shipping profile](" + UPDATE_PAGE + ").", "schema": ERROR_REF, "example": DEFAULT_PROFILE},
        },
        "example_call": {"path": {"shipping_profile_id": 12}},
    },
]

REFERENCE = {"type": "object", "properties": {
    "id": {"type": "integer", "description": "The record's `id`."},
    "name": {"type": "string", "description": "The record's name."},
}}
COST = {"type": "object", "properties": {
    "amount": {"type": "number", "description": "The cost, `0` or more."},
    "type": {"type": "string", "enum": ["fixed", "percent"], "description": "`fixed` is a money amount, and `percent` is a percentage."},
}}

SCHEMAS = {
    "ShippingProfile": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping profile's `id`, assigned by the store. Pass it as `shipping_profile_id` in a path."},
        "name": {"type": "string", "description": "Unique across the store's shipping profiles, in any letter case."},
        "description": {"type": ["string", "null"], "description": "The profile's description, or `null`."},
        "rule_preference": {"type": "string", "enum": RULE_PREFERENCES, "description": "Which rule applies when several match."},
        "default": {"type": "boolean", "description": "`true` on the one default profile of the store."},
        "rules_count": {"type": "integer", "description": "The number of rules on the profile."},
        "shipping_rules": {"type": "array", "description": "The rules on the profile.", "items": {"$ref": "#/components/schemas/ShippingProfileRule"}},
        "transaction_no": {"type": ["string", "null"], "description": "The transaction number the profile was filed under, or `null`."},
        "created_at": {"type": "string", "description": "When the profile was created, in UTC, such as `2026-11-05T05:02:55Z`."},
        "updated_at": {"type": "string", "description": "When the profile last changed, in UTC."},
    }},
    "ShippingProfileRule": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The shipping rule's `id`."},
        "name": {"type": "string", "description": "The shipping rule's name."},
        "shipping_rate": {"oneOf": [REFERENCE, {"type": "null"}], "description": "The `id` and `name` of the rule's shipping rate, or `null` when the rule has none."},
    }},
    "ShippingProfileInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required. Unique across the store's shipping profiles, in any letter case."},
        "description": {"type": ["string", "null"], "description": "The profile's description. Required on a replace, where `null` is allowed."},
        "rule_preference": {"type": "string", "enum": RULE_PREFERENCES, "description": "Defaults to `product_assigned_rule`. Required on a replace. The short codes `hp`, `lsc` and `hsc` are also accepted."},
        "default": {"type": "boolean", "description": "`true` makes the profile the store default. Only `true` or `false` is accepted, not `\"yes\"` or `1`. `false` on the default profile is rejected with `409`."},
        "shipping_rules": {"type": "array", "description": "The whole list of rule `id` values, each rule once. `[]` for none. Required on a replace.", "items": {"type": "integer"}},
        "transaction_no": {"type": "string", "description": "A transaction number. The `X-Transaction-No` header wins when you send both."},
        "suggest_name": {"type": "boolean", "description": "Only on create. `true` saves the next free name, such as `Metro profile(1)`, when another profile has the `name`."},
    }},
    "ShippingProfileWizardInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required. A name that a profile already has adds the rules to that profile."},
        "description": {"type": ["string", "null"], "description": "The profile's description."},
        "rule_preference": {"type": "string", "enum": RULE_PREFERENCES, "description": "Defaults to `product_assigned_rule`."},
        "shipping_rules": {"type": "array", "description": "The rules to create. Leave it out to create a profile with no rules.", "items": {"$ref": "#/components/schemas/ShippingProfileWizardRule"}},
    }},
    "ShippingProfileWizardRule": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required. The new rule's name."},
        "description": {"type": ["string", "null"], "description": "The rule's description."},
        "shipping_class": {"type": "integer", "description": "The `id` of the shipping class."},
        "zones": {"type": "array", "description": "The zones of the rule. Send `{\"id\": 5}` for an existing zone, or `{\"name\": \"Inner West\"}` to create a zone with that name.", "items": REFERENCE},
        "shipping_rate": {"$ref": "#/components/schemas/ShippingProfileWizardRate"},
    }},
    "ShippingProfileWizardRate": {"type": "object", "required": ["name", "method"], "description": "The shipping rate the wizard creates for the rule. It takes the fields of [Create a shipping rate](" + RATE_CREATE_PAGE + ") that describe the rate, but not `shipping_rule_id`.", "properties": {
        "name": {"type": "string", "description": "Required. The new rate's name."},
        "method": {"type": "string", "description": "Required. `flat_rate`, `free_shipping`, `ship_by_price`, `ship_by_quantity`, `ship_by_weight`, `ship_by_variation` or `shipping_variant`."},
        "calculate_for_entire_order": {"type": "boolean"},
        "price_entered_with_tax": {"type": "boolean"},
        "shipping_cost": COST,
        "handling_cost": COST,
        "conditions": {"type": "array", "description": "The rows of a `ship_by_...` rate.", "items": {"type": "object"}},
        "additional_rule": {"type": "object", "description": "`enabled`, `for_each_additional` and `additional_cost`."},
        "transaction_no": {"type": "string", "description": "A transaction number for the rate."},
    }},
    "ShippingProfilePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of shipping profiles that match."},
        "limit": {"type": "integer", "description": "The number of profiles per call the store applied."},
        "offset": {"type": "integer", "description": "The number of profiles skipped before this call's profiles."},
        "has_previous": {"type": "boolean"},
        "has_next": {"type": "boolean", "description": "`true` when a higher `offset` returns more profiles."},
    }},
    "ShippingProfileCount": {"type": "object", "properties": {"total": {"type": "integer", "description": "The number of shipping profiles that match the filters."}}},
    "ShippingProfileError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found`, `conflict` or `method_not_allowed`."},
        "message": {"type": "string"},
        "details": {"type": "array", "description": "Extra detail, or an empty list. Each entry names the `field` and gives a `code` such as `required`, `invalid_enum`, `invalid_boolean`, `out_of_range`, `invalid_integer`, `duplicate` or `default_profile`.", "items": {"type": "object", "properties": {
            "field": {"type": "string"},
            "code": {"type": "string"},
            "message": {"type": ["string", "null"]},
            "value": {"type": ["integer", "string"], "description": "The value you sent."},
        }}},
        "request_id": {"type": "string"},
    }}}},
}
