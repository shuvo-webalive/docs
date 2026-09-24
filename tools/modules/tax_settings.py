"""The Tax settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Tax settings"
SLUG = "tax-settings"
BASE = "/admin/tax/settings"
ICON = "file-invoice-dollar"

GET_PAGE = "/api-reference/tax-settings/get-tax-settings"

OVERVIEW_DESCRIPTION = "Read and change your store's tax settings, such as the default country, the default tax code and the tax message."
INTRO = "The Tax settings API has two endpoints, and you can call both from all seven SDKs. Both use the path `/api/v4/admin/tax/settings`."

WARNING = (
    "**Wrap a write in `settings`, not in `tax_settings`.** The read returns the settings under\n"
    "  `tax_settings`, but the write takes them under `settings`. A body wrapped in `tax_settings`,\n"
    "  a body with no wrapper and an empty `settings` object are each rejected with\n"
    "  `400 invalid_request` and the message `settings missing`."
)

NOTES = [
    "**A write changes only the fields you send.** Every field you leave out keeps its stored value,\n"
    "  and the response returns all nine settings. A field the store does not know is ignored, and a\n"
    "  body in which every field is ignored is rejected with `400` and the message\n"
    "  `No settings provided to update`.",
    "**Only `default_tax_profile` and `configuration_type` are checked.** If no tax profile has the\n"
    "  `tax_profile_id` you send as `default_tax_profile`, or the store does not know the\n"
    "  `configuration_type` you send, the write is rejected with `400 invalid_request` and the stored\n"
    "  value stays as it was. `default_country`, `default_tax_code` and `custom_tax_profile_id` are\n"
    "  stored without a check: `default_country: \"ZZ\"`, a `default_tax_code` that matches no tax code\n"
    "  and `custom_tax_profile_id: 99999999` are each accepted with `200`. Check these three values\n"
    "  yourself before you send them.",
    "**`default_tax_profile` follows the default tax profile.** It holds the `id` of the tax profile\n"
    "  whose `default` is `true`, which the tax profile calls take as `tax_profile_id`, and it changes\n"
    "  when another tax profile becomes the default. If the default tax profile is deleted,\n"
    "  `default_tax_profile` keeps the deleted profile's `tax_profile_id`, and a write cannot send that\n"
    "  value back: it is rejected with `400`. Leave `default_tax_profile` out of a write unless you are\n"
    "  changing it.",
    "**After a rejected request, the store handles your next request on the same client with the rejected\n"
    "  value.** This applies to the id in the path, such as a `country_tax_id`, and to a query parameter\n"
    "  such as `limit`, and it lasts for one request. After `GET /admin/tax/country_taxes/99999999`\n"
    "  returns `404`, a `GET /admin/tax/custom_profiles/1` sent next also returns `404`, even though that\n"
    "  profile exists. [Get tax settings](" + GET_PAGE + ") takes neither value, so it returns the settings\n"
    "  as usual straight after a rejected request. If a call fails straight after another call failed,\n"
    "  send it again.",
    "**Only `GET` and `PUT` exist, on one flat path.** There is no `HEAD` endpoint: `HEAD`, `POST`,\n"
    "  `PATCH` and `OPTIONS` on `/admin/tax/settings` return `404`. The settings have no sections, so\n"
    "  a path below it, such as `/admin/tax/settings/bogus`, returns `404 not_found` with the message\n"
    "  `Unknown tax path: /api/v4/admin/tax/settings/bogus`. Responses have no `ETag` or\n"
    "  `Last-Modified` header, and `field_metadata=true` changes nothing.",
]

REQUEST_ID = "7d2e4a91-3b6c-4f0e-9a58-1c2b3d4e5f60"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


SETTINGS_MISSING = error("invalid_request", "settings missing")

ERROR_REF = {"$ref": "#/components/schemas/Error"}
SETTINGS_RESPONSE = {"type": "object", "properties": {"tax_settings": {"$ref": "#/components/schemas/TaxSettings"}}}
WRITE_BODY = {"type": "object", "required": ["settings"], "properties": {
    "settings": {"$ref": "#/components/schemas/TaxSettingsInput"},
}}

SAMPLE_SETTINGS = {
    "configuration_type": "DEFAULT",
    "system_default_tax": True,
    "default_country": "AU",
    "custom_tax_profile_id": 1,
    "default_tax_profile": 3,
    "show_price_with_tax": True,
    "is_price_with_tax": False,
    "default_tax_code": "GST",
    "tax_message": "All prices include GST",
}

WRITE_400 = (
    "The body is not wrapped in `settings`, or `settings` is empty: the message is `settings missing`. "
    "Or every field in `settings` is one the store does not know: the message is `No settings provided to update`. "
    "Or no tax profile has the `tax_profile_id` you sent as `default_tax_profile`, or `configuration_type` is a type "
    "the store does not know: the stored value stays as it was."
)

ENDPOINTS = [
    {
        "key": "get_tax_settings",
        "slug": "get-tax-settings",
        "title": "Get tax settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all nine tax settings in one `tax_settings` object.",
        "description": "Returns the store's tax settings as nine fields in one flat `tax_settings` object, with no sections. Query parameters have no effect: `field_metadata=true` returns the same body and no field descriptions. The response has no `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {
                "description": "The nine tax settings under `tax_settings`.",
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
        "summary": "Changes the tax settings you send inside `settings` and returns all nine.",
        "description": "Send the fields to change inside a `settings` object. Only those fields change; the others keep their stored values. Returns all nine settings under `tax_settings`, in the same shape as [Get tax settings](" + GET_PAGE + "). A body wrapped in `tax_settings`, the key the read returns, is rejected with `400` and the message `settings missing`.",
        "body": {"schema": WRITE_BODY, "example": {"settings": {"tax_message": "All prices include GST"}}},
        "responses": {
            "200": {
                "description": "All nine tax settings after the change, under `tax_settings`.",
                "schema": SETTINGS_RESPONSE,
                "example": {"tax_settings": SAMPLE_SETTINGS},
            },
            "400": {"description": WRITE_400, "schema": ERROR_REF, "example": SETTINGS_MISSING},
        },
        "example_call": {},
    },
]

SCHEMAS = {
    "TaxSettings": {"type": "object", "description": "The store's tax settings: nine fields at one level, with no sections.", "properties": {
        "configuration_type": {"type": "string", "description": "The tax configuration type, such as `DEFAULT`."},
        "system_default_tax": {"type": "boolean"},
        "default_country": {"type": "string", "description": "The default country, such as `AU`. The store does not check this value."},
        "custom_tax_profile_id": {"type": "integer", "description": "A custom tax profile's `id`, such as `1`. The store does not check this value."},
        "default_tax_profile": {"type": "integer", "description": "The `id` of the default tax profile, the one whose `default` is `true`. The tax profile calls take it as `tax_profile_id`. It changes when another tax profile becomes the default, and after the default tax profile is deleted it still holds that profile's `tax_profile_id`."},
        "show_price_with_tax": {"type": "boolean"},
        "is_price_with_tax": {"type": "boolean"},
        "default_tax_code": {"type": "string", "description": "The default tax code, such as `GST`. The store does not check this value."},
        "tax_message": {"type": "string", "description": "Free text, such as `All prices include GST`."},
    }},
    "TaxSettingsInput": {"type": "object", "description": "Send only the fields you want to change. Every field you leave out keeps its stored value, and a field the store does not know is ignored.", "properties": {
        "configuration_type": {"type": "string", "description": "Must be a type the store knows, such as `DEFAULT`. Any other value is rejected with `400 invalid_request`."},
        "system_default_tax": {"type": "boolean"},
        "default_country": {"type": "string", "description": "Stored as you send it: `ZZ` is accepted."},
        "custom_tax_profile_id": {"type": "integer", "description": "A custom tax profile's `id`. Stored as you send it, without a check: `99999999` is accepted."},
        "default_tax_profile": {"type": "integer", "description": "Must be the `tax_profile_id` of an existing tax profile. Any other value is rejected with `400 invalid_request`, including the `tax_profile_id` of a deleted default profile that the read still returns, and the stored value stays as it was."},
        "show_price_with_tax": {"type": "boolean"},
        "is_price_with_tax": {"type": "boolean"},
        "default_tax_code": {"type": "string", "description": "Stored as you send it, including a tax code that does not exist."},
        "tax_message": {"type": "string", "description": "Free text."},
    }},
    "Error": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string", "description": "What was wrong, such as `settings missing`."},
        "details": {"type": "array", "items": {"type": "object"}, "description": "Extra detail, or an empty list."},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
