"""The Site settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Site settings"
SLUG = "site-settings"
BASE = "/admin/settings/site_settings"
ICON = "sliders"

SECTIONS = [
    "administration", "brand_kit", "date_time", "domain_settings",
    "email_settings", "favicon", "store_details", "store_logo",
]
KINDS = {"favicon": "media", "store_logo": "media", "store_details": "resource"}

GET_PAGE = "/api-reference/site-settings/get-site-settings"
UPDATE_PAGE = "/api-reference/site-settings/update-site-settings"
UPDATE_SECTION_PAGE = "/api-reference/site-settings/update-a-settings-section"

OVERVIEW_DESCRIPTION = "Read and change your store's details, logo, favicon, brand colours, date and time formats, units of measure, CAPTCHA, and domain and email settings."
INTRO = "The Site settings API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/site_settings`."

WARNING = (
    "**On `/site_settings`, a key whose value is not an object is ignored, and the call still returns `200`.**\n"
    "  So a field sent outside its section, as in `{\"site_settings\": {\"palette_name\": \"Autumn\"}}` or\n"
    "  `{\"palette_name\": \"Autumn\"}`, returns `200` and changes nothing. Put each field under its section's\n"
    "  name: `{\"site_settings\": {\"brand_kit\": {\"palette_name\": \"Autumn\"}}}`."
)

NOTES = [
    "**The settings are split into eight sections, and each has its own path.** The sections are\n"
    "  `administration`, `brand_kit`, `date_time`, `domain_settings`, `email_settings`, `favicon`,\n"
    "  `store_details` and `store_logo`. Read all eight through `/site_settings`, or one through\n"
    "  `/site_settings/{section}`, which returns exactly what `/site_settings` returns for that section.\n"
    "  An unknown section returns `404 not_found`. In `group_meta`, `favicon` and `store_logo` are\n"
    "  `kind: \"media\"`, `store_details` is `kind: \"resource\"`, the other five are `kind: \"setting\"`, and all\n"
    "  eight are `writable: true`.",
    "**Each write path takes two body shapes.** On `/site_settings`, wrap the sections in `site_settings`,\n"
    "  or send them bare, as in `{\"brand_kit\": {\"palette_name\": \"Autumn\"}}`. On `/site_settings/{section}`,\n"
    "  wrap the fields in the section's own name, or send the fields bare. A section body wrapped in\n"
    "  `site_settings` is rejected with `400 invalid_request`. On `/site_settings/brand_kit` the message\n"
    "  is `no recognized fields for section 'brand_kit': [site_settings]`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields, blocks and\n"
    "  sections you leave out keep their stored values. One body sent to `/site_settings` can name several\n"
    "  sections: if the store rejects a value in one of them, none of the named sections is written.\n"
    "  `PUT`, `POST` and `DELETE` are rejected on both paths with `405 method_not_allowed` and an\n"
    "  `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Secret fields read back as `***`.** `email_settings.smtp.authentication.password`,\n"
    "  `email_settings.sendgrid.api_key`, `domain_settings.security_code.code`,\n"
    "  `administration.captcha.private_key` and `administration.captcha.private_key_v3` are marked\n"
    "  `secret: true` in `field_metadata`, and each reads back as `***` once it is set. Send a new value\n"
    "  to change one, and leave it out to keep it. Send only the fields you change, not a copy of a read.",
    "**Calls to this area are slow.** A read of `/site_settings` takes about fifteen seconds, and a write\n"
    "  takes thirteen to fifteen seconds, whichever section it names. Allow for that in your client's\n"
    "  timeout.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read: `administration`, `brand_kit`, `date_time`, `domain_settings`, `email_settings`, `favicon`, `store_details` or `store_logo`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "brand_kit"},
}

WRITE_SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to write: `administration`, `brand_kit`, `date_time`, `domain_settings`, `email_settings`, `favicon`, `store_details` or `store_logo`. `favicon` takes only an `image_base64` upload or `remove`, and `store_logo` only an `image_base64` upload.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "brand_kit"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in all eight sections, keyed by section. Beside the sections, an `enums` key lists the `time_zone` and `locale` values. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields under the section's own name. For `date_time` it also has an `enums` key that lists the `time_zone` values. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_STATE = {"id": 67, "code": "NSW", "name": "New South Wales"}
SAMPLE_COUNTRY = {"id": 12, "code": "AU", "name": "Australia"}

SAMPLE_ADMINISTRATION = {
    "page_404": "page-404",
    "page_403": None,
    "default_country": SAMPLE_COUNTRY,
    "default_state": SAMPLE_STATE,
    "max_precision": 2,
    "unit_length": "centimeters",
    "unit_weight": "kilograms",
    "ecommerce_enabled": True,
    "captcha": {
        "enabled": False, "version": "V2", "type": "re_captcha", "use_own": False,
        "public_key": None, "private_key": None,
        "public_key_v3": None, "private_key_v3": None,
        "public_key_turnstile": None, "private_key_turnstile": None,
        "minimum_score": 0.5,
    },
    "auto_suggest": {"addresses": {"enabled": False, "validate": True}, "suburbs_cities": True},
}

SAMPLE_BRAND_KIT = {
    "enabled": False,
    "palette_name": "My Palette",
    "colors": {
        "primary": "#1a1a1a", "secondary": "#4d4d4d", "accent": "#808080",
        "background": "#ffffff", "surface": "#f4f4f5", "text": "#111111",
    },
}


def date_time_block(separate=None):
    block = {"date_format": "d/M/yyyy", "time_format": "HH:mm:ss", "time_zone": "Australia/Adelaide"}
    if separate is not None:
        block["separate"] = separate
    return block


SAMPLE_DATE_TIME = {
    "admin": dict(date_time_block(), first_day_of_week="Monday"),
    "email": date_time_block(False),
    "user": date_time_block(False),
    "hide_time_zone": True,
}

SAMPLE_DOMAIN_SETTINGS = {
    "website_address": "https://your-store.example.com/",
    "https_enabled": True,
    "maintenance": {"enabled": False, "message": ""},
    "security_code": {"enabled": False, "code": None, "number_only": False},
    "aliases": [],
    "ssl": {
        "key_file": {"uploaded": True, "file_name": "ssl-private-key.pem"},
        "certificate_file": {"uploaded": True, "file_name": "ssl-certificate.pem", "subject": None, "expires_at": None},
    },
}

SAMPLE_REPLY = {"different": False, "to_name": "Your Store", "to_email": "support@your-store.example.com"}

SAMPLE_EMAIL_SETTINGS = {
    "service_provider": "SMTP",
    "available": [
        {"key": "SMTP", "label": "SMTP", "type": "direct"},
        {"key": "DEFAULT", "label": "Default", "type": "direct"},
        {"key": "GMAIL", "label": "Gmail", "type": "oauth", "connect_url": "/setting/authorizeGmail"},
        {"key": "OFFICE365", "label": "Office 365", "type": "oauth", "connect_url": "/setting/authorizeOffice365"},
        {"key": "SENDGRID", "label": "SendGrid", "type": "direct"},
    ],
    "smtp": {
        "sender_name": "Your Store",
        "sender_email": "orders@your-store.example.com",
        "host": "your-store.example.com",
        "port": 587,
        "encryption": "starttls",
        "authentication": {"enabled": True, "username": "mailer@your-store.example.com", "password": "***"},
    },
    "sendgrid": {
        "api_key": "***",
        "sender_name": "Your Store",
        "sender_email": "orders@your-store.example.com",
        "reply": SAMPLE_REPLY,
    },
    "gmail": {"connect_url": "/setting/authorizeGmail"},
    "office365": {"connect_url": "/setting/authorizeOffice365"},
    "default": {"domains": [
        {"domain": "your-store.example.com", "configure": False, "sender_name": "Your Store", "email_prefix": "orders", "reply": SAMPLE_REPLY},
    ]},
}

SAMPLE_FAVICON = {"enabled": False, "image": None}

SAMPLE_STORE_DETAILS = {
    "company_name": "Your Store Pty Ltd",
    "email": "info@your-store.example.com",
    "address": {
        "address_line_1": "1 Example Street",
        "address_line_2": "Level 4",
        "city": "Sydney",
        "post_code": "2000",
        "state": SAMPLE_STATE,
        "country": SAMPLE_COUNTRY,
    },
    "contact": {"phone": "+61 2 9000 0000", "mobile": "+61 400 000 000", "fax": "+61 2 9000 0001"},
    "abn": "12 345 678 901",
}

SAMPLE_STORE_LOGO = {
    "image": {
        "file_name": "store-logo.png",
        "url": "https://your-store.example.com/store/store-logo.png",
        "content_type": "image/png",
        "size_bytes": 4096,
        "width": 200,
        "height": 60,
    },
}

SAMPLE_SECTIONS = {
    "administration": SAMPLE_ADMINISTRATION,
    "brand_kit": SAMPLE_BRAND_KIT,
    "date_time": SAMPLE_DATE_TIME,
    "domain_settings": SAMPLE_DOMAIN_SETTINGS,
    "email_settings": SAMPLE_EMAIL_SETTINGS,
    "favicon": SAMPLE_FAVICON,
    "store_details": SAMPLE_STORE_DETAILS,
    "store_logo": SAMPLE_STORE_LOGO,
}

SAMPLE_GROUP_META = {
    section: {"kind": KINDS.get(section, "setting"), "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_SITE_SETTINGS = {"site_settings": SAMPLE_SECTIONS, "group_meta": SAMPLE_GROUP_META}

PATCHED_SITE_SETTINGS = copy.deepcopy(SAMPLE_SITE_SETTINGS)
PATCHED_SITE_SETTINGS["site_settings"]["brand_kit"]["palette_name"] = "Autumn"
PATCHED_SITE_SETTINGS["site_settings"]["date_time"]["hide_time_zone"] = False

PATCHED_BRAND_KIT = dict(copy.deepcopy(SAMPLE_BRAND_KIT), palette_name="Autumn")


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


UNKNOWN_SECTION_IN_BODY = error_example(
    "invalid_request", "not_a_section: is not a recognized site-settings section",
    [{"field": "not_a_section", "code": "unknown_section", "message": "is not a recognized site-settings section"}],
    "e1b28569-e2a7-45ba-b4ab-366a340ba1ea",
)
UNKNOWN_SECTION_IN_PATH = error_example(
    "not_found", "Unknown site-settings section: bogus", [], "dc77e68b-d88c-4a3f-b978-31db5ca7b0e8",
)
INVALID_BOOLEAN = error_example(
    "invalid_request", "hide_time_zone: must be a boolean (true/false or 0/1)",
    [{"field": "hide_time_zone", "code": "invalid_boolean", "message": "must be a boolean (true/false or 0/1)", "value": "nope"}],
    "2f0a11e6-2d79-410f-8aea-91b35c7ac12c",
)
WRONG_CONTENT_TYPE = error_example(
    "unsupported_media_type", "Content-Type must be application/json",
    [{"field": "Content-Type", "code": "unsupported_media_type", "message": None, "value": "text/plain"}],
    "4cfb4443-9f34-4e2c-8072-e2b275efbac4",
)


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

SECTION_PROPERTIES = {
    "administration": ref("SiteSettingsAdministration"),
    "brand_kit": ref("SiteSettingsBrandKit"),
    "date_time": ref("SiteSettingsDateTime"),
    "domain_settings": ref("SiteSettingsDomainSettings"),
    "email_settings": ref("SiteSettingsEmailSettings"),
    "favicon": ref("SiteSettingsFavicon"),
    "store_details": ref("SiteSettingsStoreDetails"),
    "store_logo": ref("SiteSettingsStoreLogo"),
}

SITE_SETTINGS_RESPONSE = {"type": "object", "properties": {
    "site_settings": ref("SiteSettings"),
    "group_meta": ref("SiteSettingsGroupMeta"),
}}

VALUE_REASONS = (
    "`out_of_range` (`max_precision` outside `1` to `9`), `invalid_enum` (a value outside the field's `allowed_values`), "
    "`invalid_boolean`, `invalid_color` (a `brand_kit.colors` value that is not a colour), `invalid_page` (a `page_404` "
    "that is not the URL of an existing page), `invalid_abn` (an `abn` that is not 11 digits), `invalid_email` or "
    "`invalid_reference` (a state `id` in `default_state` that matches no state)"
)

ENDPOINTS = [
    {
        "key": "get_site_settings",
        "slug": "get-site-settings",
        "title": "Get site settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all eight settings sections and a `group_meta` block describing each one.",
        "description": "Returns every site setting under `site_settings`, with all eight sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section. The response has no `ETag` header.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All eight sections and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(SITE_SETTINGS_RESPONSE["properties"], field_metadata=dict(
                    ref("SiteSettingsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section, with an `enums` key beside the eight.",
                ))},
                "example": SAMPLE_SITE_SETTINGS,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_site_settings",
        "slug": "update-site-settings",
        "title": "Update site settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change grouped by section name, inside `site_settings` or bare at the top level. One body can name several sections, and only the fields you send change. Returns all the settings after the change, with `group_meta`, as [Get site settings](" + GET_PAGE + ") does. A key whose value is not an object, such as `{\"site_settings\": {\"palette_name\": \"Autumn\"}}`, is ignored and the call still returns `200`.",
        "body": {
            "schema": {"type": "object", "description": "Group the fields by section, inside `site_settings` or bare at the top level, as in `{\"brand_kit\": {\"palette_name\": \"Autumn\"}}`. Put each field under its section's name: a key whose value is not an object is ignored.", "properties": {
                "site_settings": dict(ref("SiteSettings"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"site_settings": {"brand_kit": {"palette_name": "Autumn"}, "date_time": {"hide_time_zone": False}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": SITE_SETTINGS_RESPONSE, "example": PATCHED_SITE_SETTINGS},
            "400": {
                "description": "The body names a section that does not exist: the message is `<name>: is not a recognized site-settings section` and `details[0].code` is `unknown_section`. Or a named section has a value the store does not accept, with the reason in `details[].code`, as on [Update a settings section](" + UPDATE_SECTION_PAGE + "). When one value is rejected, none of the sections named in the body is written.",
                "schema": ERROR,
                "example": UNKNOWN_SECTION_IN_BODY,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_site_settings",
        "slug": "get-site-settings-headers",
        "title": "Get site settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the site settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0`, and there is no `ETag` header. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0`. No `ETag` and no body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_site_settings_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `brand_kit`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `site_settings`, and without `group_meta`. The section is exactly what [Get site settings](" + GET_PAGE + ") returns for it. Add `field_metadata=true` to also get a description of each of the section's fields. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key. The response has no `ETag` header.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": dict(
                    SECTION_PROPERTIES,
                    field_metadata=dict(ref("SiteSettingsFieldMetadata"), description="Only when you send `field_metadata=true`. Holds the section's own name, and an `enums` key for `date_time`."),
                )},
                "example": {"brand_kit": SAMPLE_BRAND_KIT},
            },
            "404": {
                "description": "No section has that name. The message is `Unknown site-settings section: <name>`.",
                "schema": ERROR,
                "example": UNKNOWN_SECTION_IN_PATH,
            },
        },
        "example_call": {"path": {"section": "brand_kit"}},
    },
    {
        "key": "patch_site_settings_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change wrapped in the section's own name, such as `brand_kit`, or bare with no wrapper. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under its own key and without `group_meta`. A body wrapped in `site_settings` is rejected with `400`.",
        "parameters": [WRITE_SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path, or send them bare. Send only the fields that change.", "properties": SECTION_PROPERTIES},
            "example": {"brand_kit": {"palette_name": "Autumn"}},
        },
        "responses": {
            "200": {
                "description": "The whole section after the change, under its own key.",
                "schema": {"type": "object", "properties": SECTION_PROPERTIES},
                "example": {"brand_kit": PATCHED_BRAND_KIT},
            },
            "400": {
                "description": "Every field the body names is unknown or read-only: the message is `no recognized fields for section '<section>': [<names>]` and `details[].code` is `unknown_field`. A body wrapped in `site_settings` gets the same message, naming `[site_settings]`. An unknown or read-only field sent beside fields the store recognises is ignored instead. Or a value is not accepted, with the reason in `details[].code`: " + VALUE_REASONS + ". On `store_logo`, `remove: true` is rejected with `details[0].code` `unsupported`: the logo can only be replaced with a new `image_base64`.",
                "schema": ERROR,
                "example": INVALID_BOOLEAN,
            },
            "415": {
                "description": "The `Content-Type` header is not `application/json`.",
                "schema": ERROR,
                "example": WRONG_CONTENT_TYPE,
            },
        },
        "example_call": {"path": {"section": "brand_kit"}},
    },
]


def flag(description, **extra):
    return dict({"type": "boolean", "description": description}, **extra)


def text(description, **extra):
    return dict({"type": "string", "description": description}, **extra)


def whole(description, **extra):
    return dict({"type": "integer", "description": description}, **extra)


SECRET = "Reads back as `***` once set. Send a new value to change it, or leave it out to keep it."
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PROVIDERS = ["SMTP", "DEFAULT", "GMAIL", "OFFICE365", "SENDGRID"]
REGION_WRITE = "A write can send the {whose} `id`, `code` or `name` alone, or the whole record."

SCHEMAS = {
    "SiteSettings": {"type": "object", "description": "All eight sections, as [Get site settings](" + GET_PAGE + ") returns them. In a write, send only the sections and fields that change.", "properties": SECTION_PROPERTIES},
    "SiteSettingsRegion": {"type": "object", "description": "A country or a state. A read returns this record; a write can send the country's or state's `id`, `code` or `name` alone instead.", "properties": {
        "id": whole("The country's or state's `id`."),
        "code": text("The country's or state's code, such as `AU` or `NSW`."),
        "name": text("The country's or state's name, such as `Australia` or `New South Wales`."),
    }},
    "SiteSettingsAdministration": {"type": "object", "description": "Units of measure, price precision, the default country and state, error pages, CAPTCHA and address suggestions.", "properties": {
        "page_404": text("The URL of the page shown when a page is not found. It must be the URL of an existing page, or empty for the system-defined page: anything else is rejected with `400 invalid_page`."),
        "page_403": text("The URL of the page shown when access is forbidden, or `null`.", type=["string", "null"]),
        "default_country": dict(ref("SiteSettingsRegion"), description="The default country for new records. " + REGION_WRITE.format(whose="country's")),
        "default_state": dict(ref("SiteSettingsRegion"), description="The default state for new records. " + REGION_WRITE.format(whose="state's") + " A state `id` that matches no state is rejected with `400 invalid_reference`."),
        "max_precision": whole("The number of decimal places for prices and amounts. `0` or `10` is rejected with `400 out_of_range`.", minimum=1, maximum=9),
        "unit_length": text("The unit of length. A value outside this list is rejected with `400 invalid_enum`.", enum=["inches", "centimeters", "kilometers", "miles", "millimeters", "feet", "meters"]),
        "unit_weight": text("The unit of weight.", enum=["pounds", "ounces", "grams", "tonnes", "kilograms"]),
        "ecommerce_enabled": flag("Turn the storefront's commerce features on or off."),
        "captcha": ref("SiteSettingsCaptcha"),
        "auto_suggest": ref("SiteSettingsAutoSuggest"),
    }},
    "SiteSettingsCaptcha": {"type": "object", "description": "CAPTCHA protection for the store's forms.", "properties": {
        "enabled": flag("Protect forms with a CAPTCHA."),
        "version": text("The reCAPTCHA version.", enum=["V2", "V3"]),
        "type": text("The CAPTCHA provider, such as `re_captcha`."),
        "use_own": {"type": "boolean"},
        "public_key": text("The CAPTCHA site key, or `null`.", type=["string", "null"]),
        "private_key": text("The CAPTCHA secret key, or `null`. " + SECRET, type=["string", "null"]),
        "public_key_v3": text("The reCAPTCHA v3 site key, or `null`.", type=["string", "null"]),
        "private_key_v3": text("The reCAPTCHA v3 secret key, or `null`. " + SECRET, type=["string", "null"]),
        "public_key_turnstile": text("Returned on reads, as text or `null`. `field_metadata` has no entry for it.", type=["string", "null"]),
        "private_key_turnstile": text("Returned on reads, as text or `null`. `field_metadata` has no entry for it.", type=["string", "null"]),
        "minimum_score": {"type": "number", "description": "The reCAPTCHA v3 minimum passing score, such as `0.5`. A read returns a number, although `field_metadata` types it `string`."},
    }},
    "SiteSettingsAutoSuggest": {"type": "object", "description": "Address and suburb suggestions as the user types.", "properties": {
        "addresses": ref("SiteSettingsAutoSuggestAddresses"),
        "suburbs_cities": flag("Suggest suburbs and cities as the user types."),
    }},
    "SiteSettingsAutoSuggestAddresses": {"type": "object", "description": "Address suggestions.", "properties": {
        "enabled": flag("Suggest addresses as the user types."),
        "validate": flag("Validate the address the user chooses."),
    }},
    "SiteSettingsBrandKit": {"type": "object", "description": "The site-wide colour palette.", "properties": {
        "enabled": flag("Turn the site-wide brand palette on or off."),
        "palette_name": text("The name of the default colour palette."),
        "colors": ref("SiteSettingsBrandColors"),
    }},
    "SiteSettingsBrandColors": {"type": "object", "description": "Six colour roles, each a hex colour such as `#1a1a1a`. A value that is not a colour is rejected with `400 invalid_color`.", "properties": {
        "primary": text("The primary brand colour."),
        "secondary": text("The secondary brand colour."),
        "accent": text("The accent colour."),
        "background": text("The background colour."),
        "surface": text("The surface colour."),
        "text": text("The text colour."),
    }},
    "SiteSettingsDateTime": {"type": "object", "description": "Date and time formats and time zones for the admin area, emails and the storefront.", "properties": {
        "admin": ref("SiteSettingsAdminDateTime"),
        "email": dict(ref("SiteSettingsSeparableDateTime"), description="The date and time settings used in emails."),
        "user": dict(ref("SiteSettingsSeparableDateTime"), description="The date and time settings for the storefront."),
        "hide_time_zone": flag("Hide the time zone label on the storefront."),
        "separate_time_zone_for_email": flag("Use a separate time zone for emails. `field_metadata` lists it as writable, but a read does not return it.", writeOnly=True),
        "separate_time_zone_for_user": flag("Use a separate time zone for the storefront. `field_metadata` lists it as writable, but a read does not return it.", writeOnly=True),
    }},
    "SiteSettingsAdminDateTime": {"type": "object", "description": "The admin area's date and time settings.", "properties": {
        "date_format": text("The date pattern, such as `M/d/yyyy`."),
        "time_format": text("The time pattern, such as `HH:mm:ss`."),
        "time_zone": text("The time zone, such as `Australia/Adelaide`. `field_metadata` lists the accepted values in `enums.time_zone.values`."),
        "first_day_of_week": text("The first day shown in calendars.", enum=DAYS),
    }},
    "SiteSettingsSeparableDateTime": {"type": "object", "description": "The date and time settings for emails or for the storefront.", "properties": {
        "separate": flag("Returned on reads. `field_metadata` has no entry for it. To give emails or the storefront their own time zone, send `separate_time_zone_for_email` or `separate_time_zone_for_user` on `date_time`."),
        "date_format": text("The date pattern, such as `M/d/yyyy`."),
        "time_format": text("The time pattern, such as `HH:mm:ss`."),
        "time_zone": text("The time zone, such as `Australia/Adelaide`. `field_metadata` lists the accepted values in `enums.time_zone.values`."),
    }},
    "SiteSettingsDomainSettings": {"type": "object", "description": "The store's web address, HTTPS, maintenance mode, site lock, domain aliases and SSL files.", "properties": {
        "website_address": text("The public base URL of the store, such as `https://your-store.example.com/`."),
        "https_enabled": flag("Serve the storefront over HTTPS."),
        "maintenance": ref("SiteSettingsMaintenance"),
        "security_code": ref("SiteSettingsSecurityCode"),
        "aliases": {"type": "array", "items": {"type": "string"}, "readOnly": True, "description": "The store's domain aliases. Read-only here: manage them through `/api/v4/admin/aliases`. A write that names only `aliases` is rejected with `400 unknown_field`."},
        "ssl": ref("SiteSettingsSsl"),
    }},
    "SiteSettingsMaintenance": {"type": "object", "description": "Whether the storefront is closed for maintenance, and what it shows.", "properties": {
        "enabled": flag("Put the storefront into maintenance mode."),
        "message": text("The message shown during maintenance."),
    }},
    "SiteSettingsSecurityCode": {"type": "object", "description": "The site lock: a code visitors must enter to view the site.", "properties": {
        "enabled": flag("Require a code to view the site."),
        "code": text("The code visitors must enter, or `null`. " + SECRET, type=["string", "null"]),
        "number_only": flag("Allow only digits in the code."),
    }},
    "SiteSettingsSsl": {"type": "object", "description": "The SSL private key and certificate. A read returns `key_file` and `certificate_file`; a write sends `key_file_base64` and `certificate_file_base64` instead.", "properties": {
        "key_file": dict(ref("SiteSettingsSslKeyFile"), readOnly=True),
        "certificate_file": dict(ref("SiteSettingsSslCertificateFile"), readOnly=True),
        "key_file_base64": text("The private key as a base64 PEM. The store checks it and never returns it. Send it with `certificate_file_base64`.", writeOnly=True),
        "certificate_file_base64": text("The certificate as a base64 PEM. The store checks it and never returns it. Send it with `key_file_base64`.", writeOnly=True),
    }},
    "SiteSettingsSslKeyFile": {"type": "object", "description": "What is stored for the private key. The key itself is never returned.", "properties": {
        "uploaded": flag("Whether a key file is stored."),
        "file_name": text("The stored key file's name."),
    }},
    "SiteSettingsSslCertificateFile": {"type": "object", "description": "What is stored for the certificate.", "properties": {
        "uploaded": flag("Whether a certificate file is stored."),
        "file_name": text("The stored certificate file's name."),
        "subject": text("The certificate's subject, or `null`.", type=["string", "null"]),
        "expires_at": text("When the certificate expires, or `null`.", type=["string", "null"]),
    }},
    "SiteSettingsEmailSettings": {"type": "object", "description": "The provider the store sends email through, and each provider's settings.", "properties": {
        "service_provider": text("The provider the store sends email through.", enum=PROVIDERS),
        "available": {"type": "array", "items": ref("SiteSettingsEmailProvider"), "readOnly": True, "description": "The providers you can choose. Read-only."},
        "smtp": ref("SiteSettingsSmtp"),
        "sendgrid": ref("SiteSettingsSendGrid"),
        "gmail": dict(ref("SiteSettingsOauthProvider"), description="Gmail. Connect it through its interactive flow, not through this API."),
        "office365": dict(ref("SiteSettingsOauthProvider"), description="Office 365. Connect it through its interactive flow, not through this API."),
        "default": ref("SiteSettingsDefaultEmail"),
    }},
    "SiteSettingsEmailProvider": {"type": "object", "description": "A provider the store can send email through.", "properties": {
        "key": text("The provider's key: the value `service_provider` takes.", enum=PROVIDERS),
        "label": text("The provider's display name."),
        "type": text("`direct`, or `oauth` for a provider you connect through `connect_url`.", enum=["direct", "oauth"]),
        "connect_url": text("The path that starts the provider's connect flow. Only on `oauth` providers."),
    }},
    "SiteSettingsOauthProvider": {"type": "object", "properties": {
        "connect_url": text("The path that starts the connect flow, such as `/setting/authorizeGmail`. Read-only.", readOnly=True),
    }},
    "SiteSettingsSmtp": {"type": "object", "description": "The SMTP server the store sends through, and the sender it uses.", "properties": {
        "sender_name": text("The sender's display name."),
        "sender_email": text("The from-address.", format="email"),
        "host": text("The SMTP server's host."),
        "port": whole("The SMTP server's port.", minimum=1, maximum=65535),
        "encryption": text("The connection encryption.", enum=["no", "ssl", "starttls"]),
        "authentication": ref("SiteSettingsSmtpAuthentication"),
    }},
    "SiteSettingsSmtpAuthentication": {"type": "object", "description": "How the store signs in to the SMTP server.", "properties": {
        "enabled": flag("Use SMTP authentication."),
        "username": text("The SMTP user name."),
        "password": text("The SMTP password. " + SECRET),
    }},
    "SiteSettingsSendGrid": {"type": "object", "description": "The SendGrid account the store sends through, and the sender it uses.", "properties": {
        "api_key": text("The SendGrid API key. " + SECRET),
        "sender_name": text("The sender's display name."),
        "sender_email": text("The from-address.", format="email"),
        "reply": ref("SiteSettingsReplyTo"),
    }},
    "SiteSettingsReplyTo": {"type": "object", "description": "Where replies go.", "properties": {
        "different": flag("Send replies to a different address from the sender's."),
        "to_name": text("The reply-to display name."),
        "to_email": text("The reply-to address.", format="email"),
    }},
    "SiteSettingsDefaultEmail": {"type": "object", "description": "The platform's own sending domains.", "properties": {
        "domains": {"type": "array", "items": ref("SiteSettingsDefaultDomain")},
    }},
    "SiteSettingsDefaultDomain": {"type": "object", "description": "One of the platform's sending domains, and the sender used on it.", "properties": {
        "domain": text("The sending domain. Read-only.", readOnly=True),
        "configure": flag("Use custom sender details for this domain."),
        "sender_name": text("The sender's display name on this domain."),
        "email_prefix": text("The part of the sender address before `@` and the domain."),
        "reply": ref("SiteSettingsReplyTo"),
    }},
    "SiteSettingsFavicon": {"type": "object", "description": "The favicon. A read returns `enabled` and `image`; a write sends `image_base64` or `remove`.", "properties": {
        "enabled": flag("`true` when a favicon is set. Read-only: the store sets it from whether an image is stored.", readOnly=True),
        "image": {"anyOf": [ref("SiteSettingsMediaImage"), {"type": "null"}], "readOnly": True, "description": "The stored favicon, or `null` when none is set."},
        "image_base64": text("A new favicon as a data URI, such as `data:image/png;base64,...`: a transparent PNG or JPEG of up to 10 KB and at most 256 x 256 pixels.", writeOnly=True),
        "remove": flag("Send `true` to remove the current favicon.", writeOnly=True),
    }},
    "SiteSettingsStoreLogo": {"type": "object", "description": "The store logo. A read returns `image`; a write sends `image_base64`.", "properties": {
        "image": dict(ref("SiteSettingsMediaImage"), readOnly=True, description="The stored logo."),
        "image_base64": text("A new logo as a data URI, such as `data:image/png;base64,...`: a PNG or JPEG of up to 200 KB.", writeOnly=True),
        "remove": flag("Listed in `field_metadata`, but `remove: true` is rejected with `400`: the logo can only be replaced with a new `image_base64`.", writeOnly=True),
    }},
    "SiteSettingsMediaImage": {"type": "object", "description": "A stored image and where it is served from.", "properties": {
        "file_name": text("The stored file's name."),
        "url": text("The public URL of the image."),
        "content_type": text("The image's media type, such as `image/png`."),
        "size_bytes": whole("The file size in bytes, or `null`.", type=["integer", "null"]),
        "width": whole("The width in pixels, or `null`.", type=["integer", "null"]),
        "height": whole("The height in pixels, or `null`.", type=["integer", "null"]),
    }},
    "SiteSettingsStoreDetails": {"type": "object", "description": "The business's name, contact email, address, phone numbers and ABN. `group_meta` marks it `kind: \"resource\"`, and every field is writable.", "properties": {
        "company_name": text("The registered store or business name. Marked `required` in `field_metadata`; a write that leaves it out keeps the stored value."),
        "email": text("The store's main contact email. A value that is not an email address is rejected with `400 invalid_email`. Marked `required` in `field_metadata`.", format="email"),
        "address": ref("SiteSettingsStoreAddress"),
        "contact": ref("SiteSettingsStoreContact"),
        "abn": text("The Australian Business Number, or a local tax number. It must be 11 digits, with spaces allowed: anything else is rejected with `400 invalid_abn`."),
    }},
    "SiteSettingsStoreAddress": {"type": "object", "description": "Where the business is.", "properties": {
        "address_line_1": text("Street address line 1. Marked `required` in `field_metadata`."),
        "address_line_2": text("Street address line 2."),
        "city": text("The city or suburb."),
        "post_code": text("The postal or ZIP code."),
        "state": dict(ref("SiteSettingsRegion"), description="The state. " + REGION_WRITE.format(whose="state's")),
        "country": dict(ref("SiteSettingsRegion"), description="The country. " + REGION_WRITE.format(whose="country's")),
    }},
    "SiteSettingsStoreContact": {"type": "object", "description": "The store's published phone numbers.", "properties": {
        "phone": text("The landline number."),
        "mobile": text("The mobile number."),
        "fax": text("The fax number."),
    }},
    "SiteSettingsGroupMeta": {"type": "object", "description": "One entry per section. Only [Get site settings](" + GET_PAGE + ") and [Update site settings](" + UPDATE_PAGE + ") return it.", "properties": {
        section: ref("SiteSettingsSectionMeta") for section in SECTIONS
    }},
    "SiteSettingsSectionMeta": {"type": "object", "properties": {
        "kind": text("What the section is: `media` for `favicon` and `store_logo`, `resource` for `store_details`, and `setting` for the other five.", enum=["setting", "media", "resource"]),
        "writable": flag("Whether you can write to the section. `true` for all eight."),
        "href": text("The section's own path, such as `/api/v4/admin/settings/site_settings/brand_kit`."),
    }},
    "SiteSettingsFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Each section is nested like the settings, with a `SiteSettingsFieldMetadataEntry` for each field. A field entry always has `writable`; a block of entries does not. The match with a read is not exact: some entries name a field a read never returns, such as `favicon.image_base64`, and some fields a read returns have no entry, such as `date_time.email.separate`. On `/site_settings` it covers all eight sections, keyed by section, and an `enums` key beside them lists the `time_zone` and `locale` values. On `/site_settings/{section}` it holds the section's own name, and for `date_time` an `enums` key that lists the `time_zone` values. Each list under `enums` has `values`, the accepted values, and `labels`, a display name for each value."},
    "SiteSettingsFieldMetadataEntry": {"type": "object", "properties": {
        "ui_label": text("The field's label."),
        "description": text("What the field holds or does."),
        "type": text("The kind of value the field takes: `boolean`, `string`, `integer`, `enum`, `object` or `array`."),
        "required": flag("`true` on `store_details.company_name`, `store_details.email` and `store_details.address.address_line_1`."),
        "writable": flag("Whether a write can set the field."),
        "read_only": flag("`true` when a write cannot set the field."),
        "write_only": flag("`true` on a field that a read never returns, such as `domain_settings.ssl.key_file_base64`."),
        "secret": flag("`true` on a secret field. A read returns it as `***` once it is set, except `domain_settings.ssl.key_file_base64`, which a read never returns."),
        "note": text("Extra guidance, such as how to keep a secret field's stored value."),
        "format": text("The value's format: `hex-color`, `email` or `java-date-time-pattern`."),
        "allowed_values": {"type": "array", "items": {}, "description": "The values the field accepts, for an `enum` field."},
        "enum_ref": text("The key under `enums` that lists the field's accepted values, such as `time_zone`."),
        "min": whole("The lowest value, for an `integer` field."),
        "max": whole("The highest value, for an `integer` field."),
        "shape": text("The record a read returns, such as `{id,code,name}`."),
        "accepts": text("The forms a write accepts, such as `id | code | name | object`."),
        "accepts_human_value": flag("`true` on the country and state fields, whose `accepts` lists `code` and `name`."),
        "media": flag("`true` on an upload field, such as `image_base64`."),
        "key_path": text("The field's full path, such as `site_settings.brand_kit.palette_name`."),
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": text("A machine-readable reason, such as `invalid_request`, `not_found` or `unsupported_media_type`."),
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": text("The field that was rejected."),
                "code": text("Why it was rejected, such as `unknown_field`, `unknown_section` or `invalid_boolean`."),
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": text("Identifies this request."),
        }},
    }},
}
