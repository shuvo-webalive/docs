"""The Common settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Common settings"
SLUG = "common-settings"
BASE = "/settings"
ICON = "sliders"

OVERVIEW_DESCRIPTION = "Read and change the store's settings by group and key, and read the fields of the customer registration form."
INTRO = "The Common settings API has six endpoints, and you can call every one from all seven SDKs. The paths start with `/api/v4/settings` and `/api/v4/create-customer-fields`, directly under `/api/v4` and not under `/api/v4/admin`."

GET_PAGE = "/api-reference/common-settings/get-settings"
UPDATE_PAGE = "/api-reference/common-settings/update-settings"
FIELDS_PAGE = "/api-reference/common-settings/get-the-customer-registration-fields"

WARNING = (
    "**A write changes settings for the whole store and returns every settings group.** Only the keys you\n"
    "  send change, but one entry that is not valid rejects the whole request with `400` and nothing is saved.\n"
    "  The response is about 2 MB, and a write can take from 5 to more than 50 seconds, longer than the\n"
    "  SDKs' default timeout of 30 seconds: build the client with a longer timeout, such as 120 seconds.\n"
    "  Never send a `***` value back: it is the mask a read returns for a secret, not the stored value."
)

NOTES = [
    "**Send `type` on every read.** Without it, [Get settings](" + GET_PAGE + ") returns every group,\n"
    "  about 2 MB, and can take 30 seconds or more. `type` names one group, such as `general`, `locale`,\n"
    "  `email`, `e_commerce` or `customer_registration_field`. An unknown group, or a comma list of groups\n"
    "  such as `general,locale`, is rejected with `404`.",
    "**Read one key per call with `config_key`.** A comma list such as `abn_label,abn_placeholder` matches\n"
    "  nothing and returns `{\"settings\": {}}` with `200`. Send one call per key, or read the whole group\n"
    "  with `type` alone.",
    "**Every value is text, except in the `notifications` group.** Values come back as strings, such as\n"
    "  `\"true\"` or `\"18\"`, and a number you write is stored as its text: `5` becomes `\"5\"`. The\n"
    "  `notifications` group is an object of names to `true` or `false`, such as\n"
    "  `{\"order_emails_enabled\": true, \"customer_emails_enabled\": true}`, not a list.",
    "**Passwords, keys and tokens read as `***`.** This includes `smtp_password` in the `email` group and\n"
    "  the `password_*` and `retype_password_*` keys in `customer_registration_field`. Write only the keys\n"
    "  you change, so you never send a `***` value back.",
    "**The registration form returns booleans where the settings read returns text.**\n"
    "  [Get the customer registration fields](" + FIELDS_PAGE + ") returns each field's `_active` and\n"
    "  `_required` as `true` or `false`. Reading the same keys from the `customer_registration_field` group\n"
    "  returns them as text, such as `\"true\"`. `_order` is text in both.",
    "**`/settings` accepts `GET`, `HEAD`, `PUT` and `POST`; `/create-customer-fields` accepts only `GET` and `HEAD`.**\n"
    "  An `OPTIONS` request returns these methods in its `Allow` header. Neither path sends an `ETag`\n"
    "  header.",
]

TYPE = {
    "name": "type",
    "in": "query",
    "description": "The settings group to return, such as `general`, `locale`, `email`, `e_commerce`, `notifications` or `customer_registration_field`. Send it on every call: without it, the call returns every group, about 2 MB, and can take 30 seconds or more. An unknown group, or a comma list of groups, is rejected with `404` and the detail code `unknown_type`. An empty `type=` counts as no `type`, so the call returns every group.",
    "schema": {"type": "string", "example": "customer_registration_field"},
}

CONFIG_KEY = {
    "name": "config_key",
    "in": "query",
    "description": "The one setting to return, such as `abn_placeholder`. It works with or without `type`; without `type`, the response places the key under the group it belongs to. A comma list of keys matches nothing and returns `{\"settings\": {}}`. An empty `config_key=` counts as no `config_key`.",
    "schema": {"type": "string", "example": "abn_placeholder"},
}

ERROR_REF = {"$ref": "#/components/schemas/CommonSettingError"}
GROUPS_REF = {"$ref": "#/components/schemas/CommonSettingGroups"}
INPUT_REF = {"$ref": "#/components/schemas/CommonSettingInput"}
FIELDS_REF = {"$ref": "#/components/schemas/CommonSettingCustomerFields"}

READ_400 = (
    "You sent a query parameter other than `type` and `config_key`, such as `limit` or `offset`: the message is "
    "`unknown query parameter(s): <name>` and the detail code `unknown_parameter`. Or you sent `type` or "
    "`config_key` twice: the message is `Send each query parameter once: <name>` and the detail code "
    "`duplicate_parameter`."
)
READ_404 = (
    "No settings group has the name you sent in `type`. The message is `Unknown settings type: <type>` and the "
    "detail code `unknown_type`."
)
WRITE_400 = (
    "The body is not valid, and nothing is saved. The groups are not inside `settings` (each group is reported as "
    "`unknown_field` and `settings` as `required`); the body is `{}` (the message is `request body is empty`); "
    "an entry names a group the store does not have (detail code `unknown_group`); or an entry names a key the "
    "group does not have (detail code `unknown_key`). One entry that is not valid rejects every entry in the request."
)

LIST_BODY = {"settings": {"customer_registration_field": [{"config_key": "abn_placeholder", "value": "Enter your ABN"}]}}
MAP_BODY = {"settings": {"customer_registration_field": {"abn_placeholder": "Enter your ABN"}}}

READ_EXAMPLE = {"settings": {"customer_registration_field": [{"config_key": "abn_placeholder", "value": "Enter your ABN"}]}}
WRITE_EXAMPLE = {"settings": {
    "customer_registration_field": [{"config_key": "abn_placeholder", "value": "Enter your ABN"}],
    "general": [{"config_key": "unit_weight", "value": "pounds"}],
    "notifications": {"order_emails_enabled": True, "customer_emails_enabled": True},
}}

REGISTRATION_FIELDS = [
    ("first_name", "First Name"), ("last_name", "Last Name"), ("address_line_1", "Address Line 1"),
    ("address_line_2", "Address Line 2"), ("post_code", "Post Code"), ("city", "City"), ("phone", "Phone"),
    ("mobile", "Mobile"), ("fax", "Fax"), ("email", "Email"), ("confirm_email", "Confirm Email"),
    ("password", "Password"), ("retype_password", "Retype Password"), ("country", "Country"),
    ("customer_type", "Customer Type"), ("sex", "Sex"), ("abn", "ABN"), ("abn_branch", "ABN Branch"),
    ("company_name", "Company Name"), ("date_of_birth", "Date of Birth"),
]
SAMPLE_ACTIVE = ["first_name", "last_name", "address_line_1", "post_code", "city", "phone", "email", "password", "retype_password", "country"]
SAMPLE_REQUIRED = ["first_name", "last_name", "email", "password", "retype_password"]
SAMPLE_PLACEHOLDERS = {"first_name": "Enter your first name", "abn": "Enter your ABN"}

SAMPLE_FIELD_CONFIGS = {}
for position, (field, label) in enumerate(REGISTRATION_FIELDS, start=1):
    SAMPLE_FIELD_CONFIGS[field + "_order"] = str(position)
    SAMPLE_FIELD_CONFIGS[field + "_key"] = field
    SAMPLE_FIELD_CONFIGS[field + "_label"] = label
    SAMPLE_FIELD_CONFIGS[field + "_placeholder"] = SAMPLE_PLACEHOLDERS.get(field, "")
    SAMPLE_FIELD_CONFIGS[field + "_active"] = field in SAMPLE_ACTIVE
    SAMPLE_FIELD_CONFIGS[field + "_required"] = field in SAMPLE_REQUIRED

FIELD_CONFIG_PROPERTIES = {}
for field, label in REGISTRATION_FIELDS:
    FIELD_CONFIG_PROPERTIES[field + "_order"] = {"type": "string", "description": "The position of the " + label + " field on the form, as text, such as `\"1\"`."}
    FIELD_CONFIG_PROPERTIES[field + "_key"] = {"type": "string", "description": "The " + label + " field's key, `" + field + "`."}
    FIELD_CONFIG_PROPERTIES[field + "_label"] = {"type": "string", "description": "The label the form shows for the " + label + " field."}
    FIELD_CONFIG_PROPERTIES[field + "_placeholder"] = {"type": "string", "description": "The placeholder text in the " + label + " field, or an empty string."}
    FIELD_CONFIG_PROPERTIES[field + "_active"] = {"type": "boolean", "description": "`true` when the form shows the " + label + " field."}
    FIELD_CONFIG_PROPERTIES[field + "_required"] = {"type": "boolean", "description": "`true` when the " + label + " field must be filled in."}

ENDPOINTS = [
    {
        "key": "get_settings",
        "slug": "get-settings",
        "title": "Get settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns the settings in the group you name with `type`, as `config_key` and `value` pairs.",
        "description": "Returns `settings`, an object keyed by group name, where each group is a list of `config_key` and `value` pairs. Send `type` to get one group and `config_key` to get one key; without `type`, the call returns every group, about 2 MB, and can take 30 seconds or more. Every value is text, except in the `notifications` group, and passwords, keys and tokens read as `***`. Only `type` and `config_key` are accepted: any other query parameter, `limit` and `offset` included, is rejected with `400`.",
        "parameters": [TYPE, CONFIG_KEY],
        "responses": {
            "200": {
                "description": "The settings you asked for in `settings`, keyed by group name. A `config_key` that matches nothing, or a comma list of keys, returns `{\"settings\": {}}`. The response is not paginated and has no `ETag` header.",
                "schema": GROUPS_REF,
                "example": READ_EXAMPLE,
            },
            "400": {"description": READ_400, "schema": ERROR_REF},
            "404": {"description": READ_404, "schema": ERROR_REF},
        },
        "example_call": {"query": "type=customer_registration_field&config_key=abn_placeholder"},
    },
    {
        "key": "head_settings",
        "slug": "check-settings",
        "title": "Check settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that a settings group can be read. Returns headers only, with no body.",
        "description": "Runs the same query as [Get settings](" + GET_PAGE + ") and returns `200` with headers only and no body. Send `type`: an unknown group returns `404`, and a query parameter other than `type` and `config_key` returns `400`. Without `type`, the call still reads every group and can take about 6 seconds. The response has no `ETag` header.",
        "parameters": [TYPE, CONFIG_KEY],
        "responses": {
            "200": {"description": "The group can be read. Headers only, no body."},
            "400": {"description": "You sent a query parameter other than `type` and `config_key`. Headers only, no body."},
            "404": {"description": "No settings group has the name you sent in `type`. Headers only, no body."},
        },
        "example_call": {"query": "type=general"},
    },
    {
        "key": "update_settings",
        "slug": "update-settings",
        "title": "Update settings",
        "method": "PUT",
        "path": BASE,
        "summary": "Changes only the settings you send with `PUT` and returns every settings group of the store.",
        "description": "Saves the settings you send inside `settings`, keyed by group name, and returns every settings group of the store, about 2 MB. Each group is a list of `config_key` and `value` pairs, an object of `config_key` to value, or an object of any names to `config_key` and `value` pairs. Only the keys you send change, and one entry that is not valid, such as an unknown group or key, rejects the whole request with `400` and saves nothing. The call can take from 5 to more than 50 seconds, longer than the default timeout of 30 seconds: build the client with a longer timeout, such as 120 seconds.",
        "body": {"schema": INPUT_REF, "example": LIST_BODY},
        "responses": {
            "200": {
                "description": "Every settings group of the store in `settings`, about 2 MB, with your changes saved. The example is cut down to one entry in each of three groups.",
                "schema": GROUPS_REF,
                "example": WRITE_EXAMPLE,
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {"body": LIST_BODY},
    },
    {
        "key": "save_settings",
        "slug": "save-settings",
        "title": "Save settings",
        "method": "POST",
        "path": BASE,
        "summary": "Changes only the settings you send with `POST`, and returns `201` and every settings group.",
        "description": "Takes the same body as [Update settings](" + UPDATE_PAGE + ") and saves it the same way: only the keys you send change, and one entry that is not valid rejects the whole request with `400`. It returns `201` instead of `200`, with every group of the store, and can take from 5 to more than 50 seconds. If the call times out, read the keys back with [Get settings](" + GET_PAGE + ") before you send it again.",
        "body": {"schema": INPUT_REF, "example": MAP_BODY},
        "responses": {
            "201": {
                "description": "Every settings group of the store in `settings`, about 2 MB, with your changes saved. The example is cut down to one entry in each of three groups.",
                "schema": GROUPS_REF,
                "example": WRITE_EXAMPLE,
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {"body": MAP_BODY},
    },
    {
        "key": "get_create_customer_fields",
        "slug": "get-the-customer-registration-fields",
        "title": "Get the customer registration fields",
        "method": "GET",
        "path": "/create-customer-fields",
        "summary": "Returns the customer registration form: the active fields in order and every field's settings.",
        "description": "Returns `fields`, the keys of the active registration fields in their `_order`, and `fields_configs`, six settings for each of the store's 20 registration fields, inactive ones included. Each field has `_order`, `_key`, `_label`, `_placeholder`, `_active` and `_required`, such as `first_name_label`; `_order` is text, and `_active` and `_required` are booleans. The form follows the `customer_registration_field` settings group, which you change with [Update settings](" + UPDATE_PAGE + "). The call takes no query parameters: any query parameter is rejected with `400`.",
        "responses": {
            "200": {
                "description": "The active fields' keys in `fields`, and the settings of all 20 fields in `fields_configs`. The response has no `ETag` header.",
                "schema": FIELDS_REF,
                "example": {"fields": SAMPLE_ACTIVE, "fields_configs": SAMPLE_FIELD_CONFIGS},
            },
            "400": {"description": "You sent a query parameter. The message is `unknown query parameter(s): <name>` and the detail code `unknown_parameter`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "head_create_customer_fields",
        "slug": "check-the-customer-registration-fields",
        "title": "Check the customer registration fields",
        "method": "HEAD",
        "path": "/create-customer-fields",
        "summary": "Checks that the customer registration form can be read. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. To read the fields, use [Get the customer registration fields](" + FIELDS_PAGE + ").",
        "responses": {
            "200": {"description": "The registration form can be read. Headers only, no body."},
        },
        "example_call": {},
    },
]

SCHEMAS = {
    "CommonSetting": {"type": "object", "description": "One setting in a group.", "properties": {
        "config_key": {"type": "string", "description": "The setting's key, such as `abn_placeholder`."},
        "value": {"type": "string", "description": "The setting's value, always as text, such as `\"true\"` or `\"18\"`. Passwords, keys and tokens read as `***`."},
    }},
    "CommonSettingNotifications": {"type": "object", "description": "The `notifications` group. Unlike every other group, it is an object of names to booleans, not a list.", "properties": {
        "order_emails_enabled": {"type": "boolean", "description": "Whether order emails are on."},
        "customer_emails_enabled": {"type": "boolean", "description": "Whether customer emails are on."},
    }},
    "CommonSettingGroups": {"type": "object", "properties": {
        "settings": {
            "type": "object",
            "description": "The settings, keyed by group name, such as `general` or `customer_registration_field`. Each group is a list of `config_key` and `value` pairs, except `notifications`, which is an object of names to booleans.",
            "additionalProperties": {"oneOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/CommonSetting"}},
                {"$ref": "#/components/schemas/CommonSettingNotifications"},
            ]},
        },
    }},
    "CommonSettingInput": {"type": "object", "required": ["settings"], "description": "The settings to change, inside `settings`. A body without the `settings` wrapper, or `{}`, is rejected with `400`.", "properties": {
        "settings": {
            "type": "object",
            "description": "The groups to change, keyed by group name. Each group is a list of `config_key` and `value` pairs, an object of `config_key` to value, or an object of any names to `config_key` and `value` pairs. Only the keys you send change. An unknown group is rejected with `400 unknown_group` and an unknown key with `400 unknown_key`. A number you send as a value is stored as its text.",
            "additionalProperties": {"oneOf": [
                {"type": "array", "items": {"$ref": "#/components/schemas/CommonSetting"}},
                {"type": "object", "additionalProperties": {"type": "string"}},
                {"type": "object", "additionalProperties": {"$ref": "#/components/schemas/CommonSetting"}},
            ]},
        },
    }},
    "CommonSettingCustomerFields": {"type": "object", "properties": {
        "fields": {"type": "array", "items": {"type": "string"}, "description": "The keys of the active registration fields, in their `_order`, such as `first_name`."},
        "fields_configs": {"$ref": "#/components/schemas/CommonSettingCustomerFieldConfigs"},
    }},
    "CommonSettingCustomerFieldConfigs": {"type": "object", "description": "Six settings for each of the 20 registration fields, inactive ones included: `<field>_order`, `<field>_key`, `<field>_label`, `<field>_placeholder`, `<field>_active` and `<field>_required`. `_active` and `_required` are booleans here, though the settings read returns them as text.", "properties": FIELD_CONFIG_PROPERTIES},
    "CommonSettingError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "`invalid_request` on a `400` and `not_found` on a `404`."},
        "message": {"type": "string", "description": "What went wrong, such as `Unknown settings type: <type>`."},
        "details": {"type": "array", "description": "One entry per rejected parameter or entry.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter or body entry that was rejected, such as `type`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_parameter`, `duplicate_parameter`, `unknown_type`, `unknown_field`, `required`, `unknown_group` or `unknown_key`."},
            "message": {"type": ["string", "null"], "description": "More detail, such as `no settings group has this name`, or `null`."},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
