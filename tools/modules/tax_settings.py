"""The Tax settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Tax settings"
SLUG = "tax-settings"
BASE = "/admin/settings/tax"
ICON = "file-invoice-dollar"

GET_PAGE = "/api-reference/tax-settings/get-tax-settings"

OVERVIEW_DESCRIPTION = "Read and change your store's tax settings, such as the tax rate for customers, the tax region, whether prices show with tax and the tax message."
INTRO = "The Tax settings API has three endpoints, and you can call every one from all seven SDKs. All three use the path `/api/v4/admin/settings/tax`."

WARNING = (
    "**Wrap a write in `tax_settings`.** The store also accepts `tax` as the wrapper. A body wrapped in\n"
    "  `settings` and a body with no wrapper are each rejected with `400`."
)

NOTES = [
    "**A write changes only the fields you send.** `PUT` and `PATCH` both merge: every field you leave\n"
    "  out keeps its stored value.",
    "**Write the custom tax profile as `custom_tax_profile_id`.** The read returns the profile as\n"
    "  `custom_tax_profile`, but a write that contains `custom_tax_profile` or `calculated_by` is rejected\n"
    "  with `400 unknown_field`.",
    "**Write `tax_region` as an object.** `{\"country_code\": \"AU\"}` sets the region. `{\"country_tax_id\": 1}`\n"
    "  is accepted but leaves `tax_region` as `null`. A bare id is rejected with `400`.",
    "**The `group_meta` links for tax profiles and tax rules return `404`.** `group_meta` names\n"
    "  `/api/v4/admin/tax/profiles` and `/api/v4/admin/tax/rules`. Read the tax profiles at\n"
    "  `/admin/tax_profiles` and the tax rules at `/admin/tax_rules` instead.",
    "**The old path `/admin/tax/settings` returns `404` with the message `Unknown tax path`.** Add\n"
    "  `field_metadata=true` to a read to also get `field_metadata`, a description of each field.",
]

ERROR_REF = {"$ref": "#/components/schemas/Error"}
SETTINGS_RESPONSE = {"type": "object", "properties": {
    "tax_settings": {"$ref": "#/components/schemas/TaxSettings"},
}}
WRITE_BODY = {"type": "object", "required": ["tax_settings"], "properties": {
    "tax_settings": {"$ref": "#/components/schemas/TaxSettingsInput"},
}}

FIELD_METADATA = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each field.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_SETTINGS = {
    "tax_rate_for_customers": "system_default",
    "tax_region": {"country_tax_id": 1, "country_code": "AU", "country_name": "Australia"},
    "custom_tax_profile": {"id": 1, "name": "Standard tax"},
    "is_price_shown_with_tax": True,
    "prices_in_catalog": "excluding_tax",
    "calculated_by": "store_region",
    "is_out_of_region_tax_free": False,
    "tax_message": "All prices include GST",
    "base_price_rounding": "nearest",
    "group_meta": {
        "tax_settings": {"kind": "setting", "writable": True, "href": "/api/v4/admin/settings/tax"},
        "tax_profiles": {"kind": "resource", "writable": True, "href": "/api/v4/admin/tax/profiles"},
        "tax_rules": {"kind": "resource", "writable": True, "href": "/api/v4/admin/tax/rules"},
    },
}

WRITE_400 = (
    "The body is wrapped in `settings` or has no wrapper. Or it contains `custom_tax_profile` or `calculated_by`, "
    "which are `unknown_field` in a write. Or `tax_region` is a bare id, not an object."
)

ENDPOINTS = [
    {
        "key": "get_tax_settings",
        "slug": "get-tax-settings",
        "title": "Get tax settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns the nine tax settings in one `tax_settings` object, and `group_meta`.",
        "description": "Returns the store's tax settings as nine fields in one flat `tax_settings` object, with no sections. `group_meta` names the settings, the tax profiles and the tax rules. Send `field_metadata=true` to also get `field_metadata`, a description of each field.",
        "parameters": [FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The nine tax settings under `tax_settings`, with `group_meta`. With `field_metadata=true`, a `field_metadata` key is added.",
                "schema": SETTINGS_RESPONSE,
                "example": {"tax_settings": SAMPLE_SETTINGS},
            },
        },
        "example_call": {},
    },
    {
        "key": "put_tax_settings",
        "slug": "update-tax-settings",
        "title": "Update tax settings",
        "method": "PUT",
        "path": BASE,
        "summary": "Changes the tax settings you send inside `tax_settings` and returns all nine.",
        "description": "Send the fields to change inside a `tax_settings` object. Only those fields change; the others keep their stored values. Returns all nine settings under `tax_settings`, in the same shape as [Get tax settings](" + GET_PAGE + "). A body wrapped in `settings`, or with no wrapper, is rejected with `400`.",
        "body": {"schema": WRITE_BODY, "example": {"tax_settings": {"tax_message": "All prices include GST"}}},
        "responses": {
            "200": {
                "description": "All nine tax settings after the change, under `tax_settings`.",
                "schema": SETTINGS_RESPONSE,
                "example": {"tax_settings": SAMPLE_SETTINGS},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "patch_tax_settings",
        "slug": "patch-tax-settings",
        "title": "Patch tax settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the tax settings you send inside `tax_settings` and returns all nine.",
        "description": "Send the fields to change inside a `tax_settings` object. Like `PUT`, `PATCH` merges: only the fields you send change. Returns all nine settings under `tax_settings`, in the same shape as [Get tax settings](" + GET_PAGE + "). A body wrapped in `settings`, or with no wrapper, is rejected with `400`.",
        "body": {"schema": WRITE_BODY, "example": {"tax_settings": {"is_price_shown_with_tax": True}}},
        "responses": {
            "200": {
                "description": "All nine tax settings after the change, under `tax_settings`.",
                "schema": SETTINGS_RESPONSE,
                "example": {"tax_settings": SAMPLE_SETTINGS},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {},
    },
]

REFERENCE = {"anyOf": [{"type": "object", "properties": {
    "id": {"type": "integer", "description": "The custom tax profile's `id`."},
    "name": {"type": "string", "description": "The custom tax profile's name."},
}}, {"type": "null"}], "description": "The custom tax profile: its `id` and name, or `null` when none is set."}

SCHEMAS = {
    "TaxSettings": {"type": "object", "description": "The store's tax settings: nine fields at one level, with no sections, and `group_meta`.", "properties": {
        "tax_rate_for_customers": {"type": "string", "enum": ["system_default", "custom_tax_profile"], "description": "Which tax rate customers are charged: `system_default` or `custom_tax_profile`."},
        "tax_region": {"anyOf": [{"type": "object", "properties": {
            "country_tax_id": {"type": "integer", "description": "The country tax's `id`."},
            "country_code": {"type": "string", "description": "The country code, such as `AU`."},
            "country_name": {"type": "string", "description": "The country's name."},
        }}, {"type": "null"}], "description": "The store's tax region, or `null` when none is set."},
        "custom_tax_profile": REFERENCE,
        "is_price_shown_with_tax": {"type": "boolean", "description": "`true` shows prices with tax."},
        "prices_in_catalog": {"type": "string", "enum": ["excluding_tax", "including_tax"], "description": "Whether the prices in your catalog are `excluding_tax` or `including_tax`."},
        "calculated_by": {"type": "string", "enum": ["store_region"], "description": "Read-only: `store_region`. A write that contains it is rejected with `400 unknown_field`."},
        "is_out_of_region_tax_free": {"type": "boolean", "description": "`true` charges no tax outside the tax region."},
        "tax_message": {"type": "string", "description": "Free text, such as `All prices include GST`."},
        "base_price_rounding": {"type": "string", "enum": ["nearest", "up", "down"], "description": "How base prices are rounded: `nearest`, `up` or `down`."},
        "group_meta": {"$ref": "#/components/schemas/TaxSettingsGroupMeta"},
        "field_metadata": {"description": "Only when you send `field_metadata=true`: a description of each field."},
    }},
    "TaxSettingsGroupMeta": {"type": "object", "description": "The settings area, the tax profiles and the tax rules.", "properties": {
        "tax_settings": {"$ref": "#/components/schemas/TaxSettingsAreaMeta"},
        "tax_profiles": {"$ref": "#/components/schemas/TaxSettingsAreaMeta"},
        "tax_rules": {"$ref": "#/components/schemas/TaxSettingsAreaMeta"},
    }},
    "TaxSettingsAreaMeta": {"type": "object", "description": "One `group_meta` entry: what the area is, whether it can be written, and its path. The `href` of `tax_profiles` and `tax_rules` returns `404`.", "properties": {
        "kind": {"type": "string", "description": "What the area is: `setting` for `tax_settings`, `resource` for `tax_profiles` and `tax_rules`."},
        "writable": {"type": "boolean", "description": "Whether you can write the area: `true` for all three."},
        "href": {"type": "string", "description": "The area's path."},
    }},
    "TaxSettingsInput": {"type": "object", "description": "Send only the fields you want to change. Every field you leave out keeps its stored value.", "properties": {
        "tax_rate_for_customers": {"type": "string", "enum": ["system_default", "custom_tax_profile"], "description": "`system_default` or `custom_tax_profile`."},
        "tax_region": {"$ref": "#/components/schemas/TaxRegionInput"},
        "custom_tax_profile_id": {"type": "integer", "description": "The `id` of the custom tax profile. The read returns it as `custom_tax_profile`."},
        "is_price_shown_with_tax": {"type": "boolean", "description": "`true` shows prices with tax."},
        "prices_in_catalog": {"type": "string", "enum": ["excluding_tax", "including_tax"], "description": "`excluding_tax` or `including_tax`."},
        "is_out_of_region_tax_free": {"type": "boolean", "description": "`true` charges no tax outside the tax region."},
        "tax_message": {"type": "string", "description": "Free text."},
        "base_price_rounding": {"type": "string", "enum": ["nearest", "up", "down"], "description": "`nearest`, `up` or `down`."},
    }},
    "TaxRegionInput": {"type": "object", "description": "The tax region to set. `{\"country_code\": \"AU\"}` sets it. `{\"country_tax_id\": 1}` is accepted but leaves `tax_region` as `null`. A bare id is rejected with `400`.", "properties": {
        "country_code": {"type": "string", "description": "The country code, such as `AU`."},
        "state_code": {"type": "string", "description": "An optional state code to send with `country_code`."},
        "country_tax_id": {"type": "integer", "description": "A country tax's `id`. The store accepts it but leaves `tax_region` as `null`."},
    }},
    "Error": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `unknown_field`."},
        "message": {"type": "string", "description": "What was wrong."},
        "details": {"type": "array", "items": {"type": "object"}, "description": "Extra detail, or an empty list."},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
