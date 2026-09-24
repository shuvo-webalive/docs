"""The Shipping settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Shipping settings"
SLUG = "shipping-settings"
BASE = "/admin/settings/shipping_settings"
ICON = "truck-fast"

GET_PAGE = "/api-reference/shipping-settings/get-shipping-settings"

OVERVIEW_DESCRIPTION = "Read and change your store's default shipping, delivery and shipping tax profiles, its default tax switches for shipping and delivery, and its shipping class switches."
INTRO = "The Shipping settings API has three endpoints, and you can call every one from all seven SDKs. All three use one path, `/api/v4/admin/settings/shipping_settings`."

WARNING = (
    "**Turning `enable_shipping_class` off also turns `enable_flat_view_class` off.** While\n"
    "  `enable_shipping_class` is `false`, a write of `\"enable_flat_view_class\": true` returns `200`,\n"
    "  but the value stays `false`, so check the value in the response. Turning `enable_shipping_class`\n"
    "  back on does not turn `enable_flat_view_class` back on: write `enable_flat_view_class` as well,\n"
    "  or it stays `false`."
)

NOTES = [
    "**The seven settings have no paths of their own.** Read and write all seven at\n"
    "  `/admin/settings/shipping_settings`. A path such as\n"
    "  `/admin/settings/shipping_settings/enable_shipping_class` returns `404 not_found` with the message\n"
    "  `Unknown settings path: shipping_settings/enable_shipping_class`, whatever the method. `group_meta`\n"
    "  has a single entry, `shipping_settings`, with `kind` and `writable` and no `href`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send, with one exception.**\n"
    "  Wrap the fields in `shipping_settings` or send them bare at the top level: both are accepted.\n"
    "  Fields you leave out keep their stored values, except `enable_flat_view_class`, which turns off\n"
    "  when you turn `enable_shipping_class` off. You can send the settings from a read straight back as a\n"
    "  write, profile records included. `PUT`, `POST` and `DELETE` are rejected with\n"
    "  `405 method_not_allowed` and an `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**A profile field takes the profile's `id`, not a bare name.** `default_shipping_profile`,\n"
    "  `default_delivery_profile` and `shipping_tax_profile` each read back as `{\"id\": …, \"name\": …}` or as\n"
    "  `null`. To change one, send the profile's `id` as a number or as a numeric string such as `\"1\"`, an\n"
    "  `{\"id\": …}` or `{\"name\": …}` record, or `null` for the `No Shipping` or `No Tax` option. A bare name\n"
    "  string is rejected with `400` and `id must be an integer`, even though `field_metadata` lists `name`\n"
    "  under `accepts`. Each profile field's `options` in `field_metadata` lists the profiles you can\n"
    "  choose, with their `id`s.",
    "**Add `field_metadata=true` to a read to get a description of each field.** The settings and\n"
    "  `group_meta` are still returned. `field_metadata` is keyed by field name and covers exactly the\n"
    "  seven fields. Every entry has `type`, `ui_label`, `description`, `required`, `writable`, `read_only`\n"
    "  and a `key_path` such as `shipping_settings.enable_shipping_class`. A boolean field's entry adds\n"
    "  `default`, and the `enable_flat_view_class` entry also adds `depends_on`, which names\n"
    "  `enable_shipping_class`. A profile field's entry adds `nullable`, `references`, `accepts`, `write_key`\n"
    "  and `options`, a list of `{id, name}` records for the profiles you can choose. The first option is\n"
    "  `No Shipping`, or `No Tax` on `shipping_tax_profile`, and its `id` is `null`.",
    "**`400`, `404` and `405` responses share one shape:** an `error` object with `code`, `message`,\n"
    "  `details` and `request_id`.",
]

FIELD_METADATA = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the seven fields, keyed by field name. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


SAMPLE_PROFILE = {"id": 4, "name": "Standard shipping"}

SAMPLE_SETTINGS = {
    "default_shipping_profile": SAMPLE_PROFILE,
    "enable_shipping_default_tax": True,
    "default_delivery_profile": SAMPLE_PROFILE,
    "enable_delivery_default_tax": True,
    "shipping_tax_profile": None,
    "enable_shipping_class": True,
    "enable_flat_view_class": True,
}

SAMPLE_GROUP_META = {"shipping_settings": {"kind": "setting", "writable": True}}

SAMPLE_RESPONSE = {"shipping_settings": SAMPLE_SETTINGS, "group_meta": SAMPLE_GROUP_META}

SETTINGS_RESPONSE = {"type": "object", "properties": {
    "shipping_settings": ref("ShippingSettings"),
    "group_meta": ref("ShippingSettingsGroupMeta"),
}}

ERROR_REF = ref("Error")

WRITE_400 = (
    "The write was rejected. A field outside the seven, or a second `shipping_settings` inside the wrapper, "
    "returns `invalid_request` with the message `<name>: not a recognized field`. An empty wrapper returns "
    "`invalid_request` with `shipping_settings body missing`. A string for a boolean field returns "
    "`must be a boolean (true/false or 0/1)`. A name string for a profile field returns `invalid_request` with "
    "`id must be an integer`. A profile `id` that none of the field's `options` has, or a `{\"code\": …}` record "
    "that matches no profile, returns `invalid_reference`, such as `no tax profile with id <n>`."
)

ENDPOINTS = [
    {
        "key": "get_shipping_settings",
        "slug": "get-shipping-settings",
        "title": "Get shipping settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all seven shipping settings, and `group_meta` saying whether you can write them.",
        "description": "Returns the seven shipping settings under `shipping_settings`, with `group_meta` beside them. The three profile fields each hold the profile's `{id, name}` record or `null`, and the other four are `true` or `false`. Send `field_metadata=true` to also get a description of each field, keyed by field name. The response has no `ETag` header.",
        "parameters": [FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The seven settings under `shipping_settings`, and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(SETTINGS_RESPONSE["properties"], field_metadata=dict(
                    ref("ShippingSettingsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by field name.",
                ))},
                "example": SAMPLE_RESPONSE,
            },
        },
        "example_call": {},
    },
    {
        "key": "patch_shipping_settings",
        "slug": "update-shipping-settings",
        "title": "Update shipping settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the shipping settings you send and returns all seven after the change.",
        "description": "Send the fields to change, wrapped in `shipping_settings` or bare at the top level: both are accepted. Fields you leave out keep their stored values, except `enable_flat_view_class`, which turns off when you turn `enable_shipping_class` off. Set a profile field with the profile's `id`; a bare name string is rejected. Returns all seven settings after the change, with `group_meta`, as [Get shipping settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in `shipping_settings`, or send them bare at the top level. Send only the fields that change.", "properties": {
                "shipping_settings": ref("ShippingSettingsInput"),
            }},
            "example": {"shipping_settings": {"enable_shipping_default_tax": True}},
        },
        "responses": {
            "200": {
                "description": "All seven settings after the change, with `group_meta`.",
                "schema": SETTINGS_RESPONSE,
                "example": SAMPLE_RESPONSE,
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "head_shipping_settings",
        "slug": "check-the-shipping-settings",
        "title": "Check the shipping settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the shipping settings are reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0`, and there is no `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0`. No body and no `ETag`."},
        },
        "example_call": {},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def profile_or_null(description):
    return {"anyOf": [ref("ShippingSettingsProfile"), {"type": "null"}], "description": description}


SHIPPING_DEFAULT_TAX = "`true` turns on the default tax for shipping. Changing it changes no other field."
DELIVERY_DEFAULT_TAX = "`true` turns on the default tax for delivery."
SHIPPING_CLASS = "`true` turns on shipping classes. Turning it off also turns `enable_flat_view_class` off."
FLAT_VIEW_CLASS = "Depends on `enable_shipping_class`: it stays `false` while `enable_shipping_class` is `false`, even when you write `true`."
BOOLEAN_INPUT = " A string is rejected with `400`."

SCHEMAS = {
    "ShippingSettings": {"type": "object", "description": "The seven shipping settings. None of them has a path of its own.", "properties": {
        "default_shipping_profile": profile_or_null("The default shipping profile, as the profile's `{id, name}` record, or `null` for `No Shipping`."),
        "enable_shipping_default_tax": flag(SHIPPING_DEFAULT_TAX),
        "default_delivery_profile": profile_or_null("The default delivery profile, as the profile's `{id, name}` record, or `null` for `No Shipping`."),
        "enable_delivery_default_tax": flag(DELIVERY_DEFAULT_TAX),
        "shipping_tax_profile": profile_or_null("The shipping tax profile, as the profile's `{id, name}` record, or `null` for `No Tax`."),
        "enable_shipping_class": flag(SHIPPING_CLASS),
        "enable_flat_view_class": flag(FLAT_VIEW_CLASS),
    }},
    "ShippingSettingsProfile": {"type": "object", "description": "The profile a profile field points at.", "properties": {
        "id": {"type": "integer", "description": "The profile's `id`. Send it in a write to choose this profile."},
        "name": {"type": "string", "description": "The profile's name."},
    }},
    "ShippingSettingsInput": {"type": "object", "description": "The fields to change. Every field is optional; send only the ones that change.", "properties": {
        "default_shipping_profile": dict(ref("ShippingSettingsProfileInput"), description="The profile to choose as the default shipping profile."),
        "enable_shipping_default_tax": flag(SHIPPING_DEFAULT_TAX + BOOLEAN_INPUT),
        "default_delivery_profile": dict(ref("ShippingSettingsProfileInput"), description="The profile to choose as the default delivery profile."),
        "enable_delivery_default_tax": flag(DELIVERY_DEFAULT_TAX + BOOLEAN_INPUT),
        "shipping_tax_profile": dict(ref("ShippingSettingsProfileInput"), description="The profile to choose as the shipping tax profile."),
        "enable_shipping_class": flag(SHIPPING_CLASS + " When you turn it back on, write `enable_flat_view_class` as well." + BOOLEAN_INPUT),
        "enable_flat_view_class": flag(FLAT_VIEW_CLASS + BOOLEAN_INPUT),
    }},
    "ShippingSettingsProfileInput": {
        "description": "The profile to choose, by its `id`. The profile `id`s you can send are in the field's `options` under `field_metadata`. A profile `id` that none of the `options` has is rejected with `400 invalid_reference`, and a bare name string with `400` and `id must be an integer`. A `{\"code\": …}` record is looked up by code, and is rejected with `400 invalid_reference` when no profile matches.",
        "anyOf": [
            {"type": "integer", "description": "The profile's `id`, such as `4`."},
            {"type": "string", "description": "The profile's `id` as a numeric string, such as `\"1\"`. A name is rejected."},
            {"type": "object", "required": ["id"], "description": "A record with the profile's `id`. The `{id, name}` record a read returns is accepted as it is.", "properties": {"id": {"type": "integer", "description": "The profile's `id`."}}},
            {"type": "object", "required": ["name"], "description": "A record with the profile's name.", "properties": {"name": {"type": "string", "description": "The profile's name."}}},
            {"type": "null", "description": "The `No Shipping` or `No Tax` option."},
        ],
    },
    "ShippingSettingsGroupMeta": {"type": "object", "description": "A single entry, `shipping_settings`.", "properties": {
        "shipping_settings": ref("ShippingSettingsAreaMeta"),
    }},
    "ShippingSettingsAreaMeta": {"type": "object", "description": "What the settings group is and whether you can write it. There is no `href`.", "properties": {
        "kind": {"type": "string", "description": "The kind of group: `setting`."},
        "writable": {"type": "boolean", "description": "Whether you can write these settings: `true`."},
    }},
    "ShippingSettingsFieldMetadata": {"type": "object", "description": "Describes each of the seven fields, keyed by field name. Returned only when you send `field_metadata=true`.", "properties": {
        name: ref("ShippingSettingsFieldDescription") for name in (
            "default_shipping_profile", "enable_shipping_default_tax", "default_delivery_profile",
            "enable_delivery_default_tax", "shipping_tax_profile", "enable_shipping_class", "enable_flat_view_class",
        )
    }},
    "ShippingSettingsFieldOption": {"type": "object", "description": "One profile you can choose for a profile field.", "properties": {
        "id": {"type": ["integer", "null"], "description": "The profile's `id`. Send it in a write to choose this profile. `null` on the `No Shipping` or `No Tax` option: send `null` to choose it."},
        "name": {"type": "string", "description": "The profile's name, or `No Shipping` or `No Tax`."},
    }},
    "ShippingSettingsFieldDescription": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes: `reference` for the three profile fields, `boolean` for the other four."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does."},
        "required": {"type": "boolean", "description": "Whether the field is required."},
        "writable": {"type": "boolean", "description": "Whether a write can set the field."},
        "read_only": {"type": "boolean", "description": "Whether the field is read-only."},
        "key_path": {"type": "string", "description": "Where the field sits in the body, such as `shipping_settings.enable_shipping_class`."},
        "default": {"description": "The field's default value. Only on the four boolean fields."},
        "depends_on": {"type": "string", "description": "Only on `enable_flat_view_class`: `enable_shipping_class`, the field it depends on."},
        "nullable": {"type": "boolean", "description": "Whether the field can be `null`. Only on the three profile fields, where it is `true`."},
        "references": {"type": "string", "description": "Only on the three profile fields: the kind of profile the field points at. `shipping_profile` on `default_shipping_profile` and `default_delivery_profile`, `custom_tax_profile` on `shipping_tax_profile`."},
        "accepts": {"type": "array", "items": {"type": "string"}, "description": "Only on the three profile fields: `id` and `name`, and also `code` on `shipping_tax_profile`. A bare name string is still rejected with `400`: send `{\"name\": …}` or the profile's `id` instead."},
        "write_key": {"type": "string", "description": "Only on the three profile fields: `id`."},
        "options": {"type": "array", "description": "Only on the three profile fields: the profiles you can choose, starting with the `No Shipping` or `No Tax` option, whose `id` is `null`. Send an option's `id` to choose that profile.", "items": ref("ShippingSettingsFieldOption")},
    }},
    "Error": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `invalid_reference`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What was wrong, such as `shipping_settings body missing`."},
        "details": {"type": "array", "description": "Extra detail about the error, or an empty list.", "items": {"type": "object"}},
        "request_id": {"type": "string", "description": "The request's id."},
    }}}},
}
