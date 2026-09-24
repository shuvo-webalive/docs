"""The Customer portal settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Customer portal"
SLUG = "customer-portal"
BASE = "/admin/settings/customer_portal"
ICON = "id-card"

SECTIONS = ["portal", "registration", "login", "sso", "profile_page", "registration_fields"]
WRITABLE_SECTIONS = ["portal", "registration", "login", "sso"]

GET_PAGE = "/api-reference/customer-portal/get-customer-portal-settings"
UPDATE_PAGE = "/api-reference/customer-portal/update-customer-portal-settings"

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read: `portal`, `registration`, `login`, `sso`, `profile_page` or `registration_fields`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "login"},
}

WRITABLE_SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to change: `portal`, `registration`, `login` or `sso`. Do not send `profile_page` or `registration_fields`: `group_meta` marks them `writable: false`.",
    "schema": {"type": "string", "enum": WRITABLE_SECTIONS, "example": "login"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each field of `portal`, `registration`, `login` and `sso`, keyed by section. `profile_page` and `registration_fields` are left out. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name and nested the same way as the section. Works for all six sections. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_PORTAL = {"enabled": True}

SAMPLE_REGISTRATION = {
    "enabled": True,
    "close_registration_message": None,
    "assign_default_group": True,
    "default_groups": [{"id": 4, "name": "MEMBER"}],
    "requires_approval": False,
    "approval_groups": [],
    "terms": {"enabled": False, "text": "By registering, I accept the", "anchor_text": "Terms and Conditions", "type": "text", "reference": None},
    "facebook": {"enabled": False, "app_id": None},
    "google": {"enabled": False, "client_id": None},
    "b2b_configuration": {"enabled": False, "create_as_organisation": False, "create_as_customer": False, "organisation_selected": False},
    "alternate_login": {"enabled": False, "enable_email_field": False},
}

SAMPLE_LOGIN = {
    "enabled": True,
    "login_disabled_message": None,
    "awaiting_approval_message": "<p>Your registration is awaiting for approval</p>",
    "password_recovery": True,
    "registration_link": True,
    "captcha": {"enabled": False, "fail_count": 3},
    "enable_landing_page_after_successful_login": False,
    "landing_page_after_successful_login": None,
}

SAMPLE_SSO = {
    "enabled": False,
    "require_site_access": False,
    "service_provider": None,
    "azure_ad": {
        "data_mapping": {
            "address_line_1": None, "address_line_2": None, "post_code": None, "phone": None,
            "mobile": None, "country_id": 49, "state": None, "city": None,
        },
        "identifier": None,
        "login_url": None,
        "reply_url_postfix": "customer/azureSamlResponse",
    },
    "azure_ad_b2c": {
        "tenant_name": None,
        "policy_name": None,
        "client_id": None,
        "client_secret": None,
        "reply_url_prefix": "https://your-store.example.com/",
        "reply_url_postfix": "customer/azureAdB2CResponse",
    },
}

SAMPLE_PROFILE_PAGE = {
    "page_html": None,
    "tabs": [
        {"key": "welcome_message", "active": True, "order": 1, "label": "Welcome Message"},
        {"key": "overview", "active": True, "order": 2, "label": "Overview"},
        {"key": "manage_my_account", "active": True, "order": 3, "label": "Manage My Account"},
        {"key": "my_eorders", "active": True, "order": 4, "label": "My Orders"},
        {"key": "my_entitlements", "active": True, "order": 5, "label": "My Entitlements"},
    ],
    "overview": [
        {"key": "overview_top_selling_product", "active": True, "order": 1, "label": "Top Selling Product", "show_product_info": True},
        {"key": "overview_onsale_product", "active": True, "order": 3, "label": "On Sale Product"},
        {"key": "overview_last_viewed_product", "active": True, "order": 5, "label": "Last Viewed Product", "show_product_info": False},
    ],
    "manage_my_account": {
        "sections": [
            {"key": "account_information", "active": True, "order": 1, "label": "Account Information"},
            {"key": "billing_address", "active": True, "order": 2, "label": "Billing Address"},
            {"key": "shipping_address", "active": True, "order": 3, "label": "Shipping Address"},
            {"key": "change_password", "active": True, "order": 4, "label": "Change Password"},
        ],
        "account_information": [
            {"key": "first_name", "active": True, "order": 1},
            {"key": "last_name", "active": True, "order": 2},
            {"key": "email", "active": True, "order": 11},
        ],
        "billing_address": [
            {"key": "name_group_field", "active": True, "order": 1},
            {"key": "country", "active": True, "order": 2},
            {"key": "address_line_2", "active": False, "order": 5},
        ],
        "shipping_address": [
            {"key": "name_group_field", "active": True, "order": 1},
            {"key": "country", "active": True, "order": 2},
            {"key": "mobile", "active": True, "order": 7},
        ],
    },
    "my_orders": {
        "flags": {
            "enable_due_payment": False, "show_track_my_orders": False, "display_track_in_column": False,
            "show_order_channel": False, "show_pay_now": True, "allow_order_share": True,
        },
        "sections": [
            {"key": "all_order", "active": True, "order": 3, "label": "Orders"},
            {"key": "preorder", "active": True, "order": 4, "label": "Pre-orders"},
        ],
    },
    "my_entitlements": [
        {"key": "store_credit", "active": True, "order": 1, "label": "My Store Credit"},
        {"key": "gift_card", "active": True, "order": 2, "label": "My Gift Cards"},
        {"key": "loyalty_point", "active": True, "order": 3, "label": "My Loyalty Points"},
    ],
    "assign_to_customer": {
        "items": [
            {"key": "assign_page", "active": True, "order": 1, "label": "Assigned Pages"},
            {"key": "assign_product", "active": True, "order": 2, "label": "Assigned Products"},
            {"key": "assign_category", "active": True, "order": 3, "label": "Assigned Categories"},
        ],
        "show_pagination": None,
        "item_per_page": None,
    },
}

SAMPLE_REGISTRATION_FIELDS = {
    "fields": [
        {"key": "first_name", "label": None, "default_label": "First Name", "active": True, "required": True, "system": True, "order": 1, "placeholder": "Enter your first name"},
        {"key": "last_name", "label": None, "default_label": "Last Name", "active": True, "required": False, "system": False, "order": 2, "placeholder": "Enter your last name"},
        {"key": "email", "label": None, "default_label": "Email", "active": True, "required": True, "system": True, "order": 10, "placeholder": "Enter your email address"},
        {"key": "company_name", "label": None, "default_label": "Company Name", "active": True, "required": False, "system": False, "order": 19, "placeholder": "Enter your company name"},
    ],
}

SAMPLE_GROUP_META = {
    section: {
        "kind": "setting" if section in WRITABLE_SECTIONS else "resource",
        "writable": section in WRITABLE_SECTIONS,
        "href": "/api/v4" + BASE + "/" + section,
    }
    for section in SECTIONS
}

SAMPLE_CUSTOMER_PORTAL = {
    "customer_portal": {
        "portal": SAMPLE_PORTAL,
        "registration": SAMPLE_REGISTRATION,
        "login": SAMPLE_LOGIN,
        "sso": SAMPLE_SSO,
        "profile_page": SAMPLE_PROFILE_PAGE,
        "registration_fields": SAMPLE_REGISTRATION_FIELDS,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_CUSTOMER_PORTAL = copy.deepcopy(SAMPLE_CUSTOMER_PORTAL)
PATCHED_CUSTOMER_PORTAL["customer_portal"]["login"]["registration_link"] = False
PATCHED_CUSTOMER_PORTAL["customer_portal"]["sso"]["azure_ad"]["data_mapping"]["city"] = "city"

PATCHED_LOGIN = dict(copy.deepcopy(SAMPLE_LOGIN), registration_link=False)


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

CUSTOMER_PORTAL_RESPONSE = {"type": "object", "properties": {
    "customer_portal": ref("CustomerPortalSettings"),
    "group_meta": ref("CustomerPortalGroupMeta"),
}}

WRITABLE_SECTION_PROPERTIES = {
    "portal": ref("CustomerPortalPortal"),
    "registration": ref("CustomerPortalRegistration"),
    "login": ref("CustomerPortalLogin"),
    "sso": ref("CustomerPortalSso"),
}

ALL_SECTION_PROPERTIES = dict(WRITABLE_SECTION_PROPERTIES, **{
    "profile_page": ref("CustomerPortalProfilePage"),
    "registration_fields": ref("CustomerPortalRegistrationFields"),
})

RATE_LIMITED = {"description": "You sent more than ten customer portal writes within about 3.25 seconds. The `Retry-After` header gives the time left before writes are accepted again."}

ENDPOINTS = [
    {
        "key": "get_customer_portal",
        "slug": "get-customer-portal-settings",
        "title": "Get customer portal settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all six customer portal sections and a `group_meta` block that says which you can write.",
        "description": "Returns every customer portal setting under `customer_portal`, with all six sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of each field in the four writable sections, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All six sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(CUSTOMER_PORTAL_RESPONSE["properties"], field_metadata=dict(
                    ref("CustomerPortalFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section, and only for `portal`, `registration`, `login` and `sso`.",
                ))},
                "example": SAMPLE_CUSTOMER_PORTAL,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_customer_portal",
        "slug": "update-customer-portal-settings",
        "title": "Update customer portal settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more writable sections and returns all settings.",
        "description": "Send the fields to change inside `customer_portal`, grouped by section name: `portal`, `registration`, `login` or `sso`. One body can change several sections. Only the fields you send change; other fields in the same block, and sections you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get customer portal settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "required": ["customer_portal"], "properties": {
                "customer_portal": dict(ref("CustomerPortalSettingsInput"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"customer_portal": {"login": {"registration_link": False}, "sso": {"azure_ad": {"data_mapping": {"city": "city"}}}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": CUSTOMER_PORTAL_RESPONSE, "example": PATCHED_CUSTOMER_PORTAL},
            "400": {
                "description": "The body is not wrapped in `customer_portal` (`request body must be wrapped in a 'customer_portal' object`), names only `profile_page` or `registration_fields` (`customer_portal body missing`), or is not valid JSON (`Request body is not valid JSON`). Or a field is unknown or has a value it does not accept: `details[].field` names the field and `details[].code` gives the reason, such as `unknown_field` or `invalid_boolean`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "portal.bogus_field: not a recognized field",
                                         [{"field": "portal.bogus_field", "code": "unknown_field", "message": "not a recognized field"}],
                                         "e767f586-f440-4321-9734-dfea31113eb9"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_customer_portal",
        "slug": "get-customer-portal-settings-headers",
        "title": "Get customer portal settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the customer portal settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` but no `ETag`; no customer portal `GET` or `HEAD` returns an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0`. No `ETag` and no body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_customer_portal_section",
        "slug": "get-a-customer-portal-section",
        "title": "Get a customer portal section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one customer portal section under its own key, such as `login`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `customer_portal`, and without `group_meta`. The section is the same as the one [Get customer portal settings](" + GET_PAGE + ") includes. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.",
                           "properties": dict(ALL_SECTION_PROPERTIES, field_metadata=dict(
                               ref("CustomerPortalFieldMetadata"),
                               description="Only when you send `field_metadata=true`. Keyed by field name.",
                           ))},
                "example": {"login": SAMPLE_LOGIN},
            },
            "404": {
                "description": "No section has that name.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown settings path: customer_portal/bogus", [],
                                         "272c25fd-6f8a-4277-b1ee-181ee42f4b92"),
            },
        },
        "example_call": {"path": {"section": "login"}},
    },
    {
        "key": "patch_customer_portal_section",
        "slug": "update-a-customer-portal-section",
        "title": "Update a customer portal section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one writable section and returns that section.",
        "description": "Send the fields to change wrapped in the section's own name, such as `login`, or with no wrapper at all. A body wrapped in `customer_portal` is rejected with `400`. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under its own key and without `group_meta`.",
        "parameters": [WRITABLE_SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path, or send them with no wrapper. A `customer_portal` wrapper is rejected.",
                       "properties": WRITABLE_SECTION_PROPERTIES},
            "example": {"login": {"registration_link": False}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.",
                    "schema": {"type": "object", "properties": WRITABLE_SECTION_PROPERTIES},
                    "example": {"login": PATCHED_LOGIN}},
            "400": {
                "description": "The body is wrapped in `customer_portal` (`<section>.customer_portal: not a recognized field`), or a field is unknown or has a value it does not accept. `details[].field` names the field and `details[].code` gives the reason, such as `unknown_field`, `invalid_boolean`, `constraint_violation` or `required`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "sso.require_site_access: require_site_access can only be enabled when SSO is enabled",
                                         [{"field": "sso.require_site_access", "code": "constraint_violation", "message": "require_site_access can only be enabled when SSO is enabled"}],
                                         "3805edd2-a0ab-4cd1-a72c-3835b0fc6aed"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "login"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def text(description, **extra):
    return dict({"type": ["string", "null"], "description": description}, **extra)


def rows(name, description):
    return {"type": "array", "items": ref(name), "description": description}


SCHEMAS = {
    "CustomerPortalSettings": {"type": "object", "description": "All six sections. `profile_page` and `registration_fields` are read-only.", "properties": ALL_SECTION_PROPERTIES},
    "CustomerPortalSettingsInput": {"type": "object", "description": "The writable sections. Name only these four.", "properties": WRITABLE_SECTION_PROPERTIES},
    "CustomerPortalPortal": {"type": "object", "description": "The switch that turns the customer portal on or off.", "properties": {
        "enabled": flag("Turn the customer portal on. Defaults to `false`."),
    }},
    "CustomerPortalRegistration": {"type": "object", "description": "Who can register, as what, and what they must accept.", "properties": {
        "enabled": flag("Let customers register. Defaults to `false`."),
        "close_registration_message": text("The HTML message shown while registration is closed, or `null`."),
        "assign_default_group": flag("Assign each new registrant to a default customer group, from `default_groups`. Defaults to `false`."),
        "default_groups": {"type": "array", "maxItems": 100, "items": ref("CustomerPortalCustomerGroup"), "description": "The customer groups a new registrant joins. A read returns each customer group as an `{id, name}` object. A write takes the customer groups' `id` values, such as `[4]`, and also accepts the objects from a read. At most 100 entries; duplicates are removed and each customer group must exist."},
        "requires_approval": flag("New customers need admin approval. Defaults to `false`."),
        "approval_groups": {"type": "array", "maxItems": 100, "items": ref("CustomerPortalCustomerGroup"), "description": "Customer groups, read and written the same way as `default_groups`: a read returns each customer group as an `{id, name}` object, and a write takes the customer groups' `id` values, such as `[4]`. At most 100 entries; duplicates are removed and each customer group must exist."},
        "terms": ref("CustomerPortalRegistrationTerms"),
        "facebook": ref("CustomerPortalFacebookLogin"),
        "google": ref("CustomerPortalGoogleLogin"),
        "b2b_configuration": ref("CustomerPortalB2bConfiguration"),
        "alternate_login": ref("CustomerPortalAlternateLogin"),
    }},
    "CustomerPortalCustomerGroup": {"type": "object", "description": "A customer group, as a read returns it.", "properties": {
        "id": {"type": "integer", "description": "The customer group's `id`. A write takes this number on its own."},
        "name": {"type": "string", "description": "The customer group's name."},
    }},
    "CustomerPortalRegistrationTerms": {"type": "object", "description": "Whether a registrant must accept terms, and where the terms are.", "properties": {
        "enabled": flag("Require registrants to accept the terms. Defaults to `false`. You cannot turn it on while `terms.reference` is `null`: the write is rejected with `400` and `a terms reference is required when terms are enabled`."),
        "text": text("The acceptance text, such as `By registering, I accept the`."),
        "anchor_text": text("The link text, such as `Terms and Conditions`. At most 255 characters.", maxLength=255),
        "type": {"type": "string", "enum": ["page", "link", "text"], "description": "Where the terms are: `page`, `link` or `text`. Any other value is rejected with `400`."},
        "reference": text("Depends on `type`: an existing page's `id` when `type` is `page`, a safe `http(s)` or same-site URL when `type` is `link`, or free text when `type` is `text`."),
    }},
    "CustomerPortalFacebookLogin": {"type": "object", "description": "Facebook login.", "properties": {
        "enabled": flag("Turn on Facebook login. Defaults to `false`."),
        "app_id": text("The Facebook app ID. Required when `facebook.enabled` is `true`."),
    }},
    "CustomerPortalGoogleLogin": {"type": "object", "description": "Google login.", "properties": {
        "enabled": flag("Turn on Google login. Defaults to `false`."),
        "client_id": text("The Google client ID. Required when `google.enabled` is `true`."),
    }},
    "CustomerPortalB2bConfiguration": {"type": "object", "description": "What a new registrant is created as.", "properties": {
        "enabled": flag("Turn on the B2B configuration. Defaults to `false`."),
        "create_as_organisation": flag("Create a new registrant as an organisation."),
        "create_as_customer": flag("Create a new registrant as a customer."),
        "organisation_selected": flag("Set organisation as the default."),
    }},
    "CustomerPortalAlternateLogin": {"type": "object", "description": "Third-party login, and whether it offers an email field.", "properties": {
        "enabled": flag("Turn on third-party login. Defaults to `false`."),
        "enable_email_field": flag("Show an email field. Depends on `alternate_login.enabled`. Defaults to `false`."),
    }},
    "CustomerPortalLogin": {"type": "object", "description": "Whether customers can sign in, and what the sign-in page offers.", "properties": {
        "enabled": flag("Let customers sign in. Defaults to `false`."),
        "login_disabled_message": text("The HTML message shown while login is turned off, or `null`."),
        "awaiting_approval_message": text("The HTML message shown to a customer whose registration is awaiting approval."),
        "password_recovery": flag("Show the password recovery link."),
        "registration_link": flag("Show the customer registration link."),
        "captcha": ref("CustomerPortalLoginCaptcha"),
        "enable_landing_page_after_successful_login": flag("Send customers to `landing_page_after_successful_login` after they sign in. While this is `false`, that page is not used. Defaults to `false`."),
        "landing_page_after_successful_login": text("The same-site path or URL customers land on after they sign in, or `null` to clear it. Used only when `enable_landing_page_after_successful_login` is `true`."),
    }},
    "CustomerPortalLoginCaptcha": {"type": "object", "description": "The captcha shown after failed login attempts.", "properties": {
        "enabled": flag("Show a captcha after failed login attempts. Defaults to `false`."),
        "fail_count": {"type": "integer", "minimum": 1, "maximum": 50, "description": "The number of failed attempts before the captcha shows. From `1` to `50`: any other value is rejected with `400` and `must be between 1 and 50`."},
    }},
    "CustomerPortalSso": {"type": "object", "description": "Single sign-on. Setting `enabled` to `true` on its own is rejected with `400`: `tenant_name`, `policy_name`, `client_id` and `client_secret` under `azure_ad_b2c` are each reported as `required`.", "properties": {
        "enabled": flag("Turn on customer SSO. Defaults to `false`."),
        "require_site_access": flag("Turn on the option labelled `Required customer to access site`. It can be `true` only while `sso.enabled` is `true`; otherwise the write is rejected with `400` and `require_site_access can only be enabled when SSO is enabled`. Defaults to `false`."),
        "service_provider": {"type": ["string", "null"], "enum": ["AZURE_AD_B2C", "AZURE_AD", None], "description": "The SSO provider: `AZURE_AD_B2C` or `AZURE_AD`, or `null`."},
        "azure_ad": ref("CustomerPortalAzureAd"),
        "azure_ad_b2c": ref("CustomerPortalAzureAdB2c"),
    }},
    "CustomerPortalAzureAd": {"type": "object", "description": "The Azure AD (SAML) provider. Required when `service_provider` is `AZURE_AD`.", "properties": {
        "data_mapping": ref("CustomerPortalAzureAdDataMapping"),
        "identifier": text("The Azure AD identifier."),
        "login_url": text("The Azure AD login URL."),
        "reply_url_postfix": text("The end of the reply URL, such as `customer/azureSamlResponse`."),
    }},
    "CustomerPortalAzureAdDataMapping": {"type": "object", "description": "The SAML assertion attribute for each customer field.", "properties": {
        "address_line_1": text("The attribute for address line 1."),
        "address_line_2": text("The attribute for address line 2."),
        "post_code": text("The attribute for the post code."),
        "phone": text("The attribute for the phone number."),
        "mobile": text("The attribute for the mobile number."),
        "country_id": {"type": "integer", "description": "A country's `id`, such as `49`."},
        "state": text("The attribute for the state."),
        "city": text("The attribute for the city."),
    }},
    "CustomerPortalAzureAdB2c": {"type": "object", "description": "The Azure AD B2C provider. Required when `service_provider` is `AZURE_AD_B2C`.", "properties": {
        "tenant_name": text("The B2C tenant name."),
        "policy_name": text("The B2C policy name."),
        "client_id": text("The B2C client ID."),
        "client_secret": text("The B2C client secret. `field_metadata` types it as a plain `string`, with no secret or write-only marker."),
        "reply_url_prefix": text("The start of the reply URL: your store's address, such as `https://your-store.example.com/`."),
        "reply_url_postfix": text("The end of the reply URL, such as `customer/azureAdB2CResponse`."),
    }},
    "CustomerPortalProfilePage": {"type": "object", "description": "The customer's profile page. Read-only: `group_meta` marks it `writable: false`.", "properties": {
        "page_html": text("The welcome message, as HTML, or `null`."),
        "tabs": rows("CustomerPortalProfileEntry", "The profile page tabs, including tabs that plugins add."),
        "overview": rows("CustomerPortalProfileOverviewEntry", "The product blocks on the Overview tab, such as `overview_top_selling_product`."),
        "manage_my_account": ref("CustomerPortalManageMyAccount"),
        "my_orders": ref("CustomerPortalMyOrders"),
        "my_entitlements": rows("CustomerPortalProfileEntry", "The entries on the My Entitlements tab, such as `store_credit`, `gift_card` and `loyalty_point`."),
        "assign_to_customer": ref("CustomerPortalAssignToCustomer"),
    }},
    "CustomerPortalProfileField": {"type": "object", "description": "One field of a form on the profile page.", "properties": {
        "key": {"type": "string", "description": "Names the field, such as `first_name`."},
        "active": flag("Show the field."),
        "order": {"type": "integer", "description": "The field's position."},
    }},
    "CustomerPortalProfileEntry": {"type": "object", "description": "One entry of a list on the profile page: a tab, a section or an entitlement.", "properties": {
        "key": {"type": "string", "description": "Names the entry, such as `overview`."},
        "active": flag("Show the entry."),
        "order": {"type": "integer", "description": "The entry's position."},
        "label": {"type": "string", "description": "The entry's label, such as `Overview`."},
    }},
    "CustomerPortalProfileOverviewEntry": {"type": "object", "description": "One product block on the Overview tab.", "properties": {
        "key": {"type": "string", "description": "Names the block, such as `overview_top_selling_product`."},
        "active": flag("Show the block."),
        "order": {"type": "integer", "description": "The block's position."},
        "label": {"type": "string", "description": "The block's label."},
        "show_product_info": flag("Show product information. Only some blocks have this field."),
    }},
    "CustomerPortalManageMyAccount": {"type": "object", "description": "The Manage My Account tab: its sections and form fields.", "properties": {
        "sections": rows("CustomerPortalProfileEntry", "The tab's sections: `account_information`, `billing_address`, `shipping_address` and `change_password`."),
        "account_information": rows("CustomerPortalProfileField", "The fields of the account information form."),
        "billing_address": rows("CustomerPortalProfileField", "The fields of the billing address form."),
        "shipping_address": rows("CustomerPortalProfileField", "The fields of the shipping address form."),
    }},
    "CustomerPortalMyOrders": {"type": "object", "description": "What the My Orders tab shows, and which order lists it offers.", "properties": {
        "flags": ref("CustomerPortalMyOrderFlags"),
        "sections": rows("CustomerPortalProfileEntry", "The order lists, such as `all_order` and `preorder`."),
    }},
    "CustomerPortalMyOrderFlags": {"type": "object", "description": "Six switches for the My Orders tab.", "properties": {
        "enable_due_payment": flag("Turn on due payment."),
        "show_track_my_orders": flag("Show order tracking."),
        "display_track_in_column": flag("Show tracking in a column. Needs `show_track_my_orders` set to `true`."),
        "show_order_channel": flag("Show the order channel."),
        "show_pay_now": flag("Show Pay Now."),
        "allow_order_share": flag("Let customers share an order."),
    }},
    "CustomerPortalAssignToCustomer": {"type": "object", "description": "The assigned pages tab, and how it paginates.", "properties": {
        "items": rows("CustomerPortalProfileEntry", "The entries: `assign_page`, `assign_product` and `assign_category`."),
        "show_pagination": {"type": ["string", "null"], "enum": ["top", "bottom", "top_and_bottom", None], "description": "Where the pagination control shows: `top`, `bottom` or `top_and_bottom`, or `null`."},
        "item_per_page": {"type": ["integer", "null"], "minimum": 1, "maximum": 999999, "description": "Items per page, from `1` to `999999`, or `null`."},
    }},
    "CustomerPortalRegistrationFields": {"type": "object", "description": "The fields of the registration form. Read-only: `group_meta` marks it `writable: false`.", "properties": {
        "fields": rows("CustomerPortalRegistrationField", "One entry per registration form field."),
    }},
    "CustomerPortalRegistrationField": {"type": "object", "description": "One field of the registration form.", "properties": {
        "key": {"type": "string", "description": "Names the field, such as `first_name`."},
        "label": text("The label you set for the field, or `null` when none is set."),
        "default_label": {"type": "string", "description": "The field's default label, such as `First Name`."},
        "active": flag("Show the field on the registration form."),
        "required": flag("The registrant must fill in the field."),
        "system": flag("`true` for a built-in field, whose `active` and `required` cannot be turned off."),
        "order": {"type": "integer", "description": "The field's position on the form."},
        "placeholder": {"type": "string", "description": "The placeholder text. Not every field has one."},
    }},
    "CustomerPortalGroupMeta": {"type": "object", "description": "One entry per section. Only [Get customer portal settings](" + GET_PAGE + ") and [Update customer portal settings](" + UPDATE_PAGE + ") return it.", "properties": {
        section: ref("CustomerPortalSectionMeta") for section in SECTIONS
    }},
    "CustomerPortalSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "enum": ["setting", "resource"], "description": "`setting` for `portal`, `registration`, `login` and `sso`; `resource` for `profile_page` and `registration_fields`."},
        "writable": {"type": "boolean", "description": "Whether you can write the section. `true` for the four `setting` sections and `false` for the two `resource` sections. Trust this field, not the `Allow` header, which lists `PATCH` on all six."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/customer_portal/login`."},
    }},
    "CustomerPortalFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `CustomerPortalFieldMetadataEntry` in place of each value. `sso.azure_ad` and `sso.azure_ad_b2c` also have a `_required_when` entry, which states when the whole block is required, such as `service_provider=AZURE_AD`."},
    "CustomerPortalFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes: `boolean`, `string`, `html`, `integer`, `enum`, `id_list` or `object_list`."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does, or a rule about it."},
        "default": {"description": "The field's default value."},
        "allowed_values": {"type": "array", "items": {"type": "string"}, "description": "The values the field accepts, for an `enum` field."},
        "min": {"type": "integer", "description": "The lowest value, for an `integer` field."},
        "max": {"type": "integer", "description": "The highest value, for an `integer` field."},
        "max_length": {"type": "integer", "description": "The longest text the field accepts."},
        "max_items": {"type": "integer", "description": "The most entries an `id_list` field accepts."},
        "nullable": {"type": "boolean", "description": "`true` when the field accepts `null`."},
        "depends_on": {"type": "string", "description": "The field this one depends on, such as `enabled`."},
        "required_when": {"type": "string", "description": "The field that makes this one required, such as `enabled`."},
        "read_only": {"type": "boolean", "description": "`true` on a field you cannot change, such as a row's `key`."},
        "item": {"type": "object", "additionalProperties": True, "description": "For an `object_list` field, a description of each field of one row."},
        "note": {"type": "string", "description": "A remark about the field."},
        "applies_to": {"type": "string", "description": "The rows the field applies to."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The field that was rejected, such as `portal.enabled`."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `invalid_boolean`, `constraint_violation` or `required`."},
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": {"type": "string", "description": "Identifies this request."},
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Turn the customer portal on or off, change its registration, login and single sign-on settings, and read its profile page and registration form."
INTRO = "The Customer portal API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/customer_portal`."
WARNING = (
    "**After a write is rejected with `400`, the next write on the same client can be rejected too.** For\n"
    "  example, after a `400` at `/customer_portal/login`, a valid `{\"registration\": {...}}` sent to\n"
    "  `/customer_portal/registration` on the same client is rejected with `400` and\n"
    "  `login.registration: not a recognized field`: the store reads the body under the previous request's\n"
    "  section name. The same write from a new client succeeds. After a `400`, send the next write from a new client."
)
NOTES = [
    "**Four sections are writable and two are read-only.** `group_meta` marks `portal`, `registration`,\n"
    "  `login` and `sso` as `kind: \"setting\"`, `writable: true`, and `profile_page` and\n"
    "  `registration_fields` as `kind: \"resource\"`, `writable: false`. Read the two read-only sections,\n"
    "  but do not write them. The `Allow` header lists `PATCH` on all six section paths, so check\n"
    "  `group_meta`, not `Allow`, to see which sections you can write.",
    "**Each write path takes a different wrapper.** On `/customer_portal`, wrap the fields in\n"
    "  `customer_portal` and then in the section name. Any other body is rejected with `400` and the message\n"
    "  `request body must be wrapped in a 'customer_portal' object`. On `/customer_portal/{section}`, wrap\n"
    "  them in the section's own name, such as `login`, or send them with no wrapper. A body wrapped in\n"
    "  `customer_portal` there is rejected with `400` and `<section>.customer_portal: not a recognized field`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Other fields in the\n"
    "  same nested block, and sections you leave out, keep their stored values. `PUT`, `POST` and `DELETE`\n"
    "  are rejected on every path with `405 method_not_allowed` and an `Allow: GET, HEAD, PATCH, OPTIONS`\n"
    "  header.",
    "**Values are validated, and some rules depend on other fields.** `login.captcha.fail_count` must be\n"
    "  from `1` to `50`, `registration.terms.type` must be `page`, `link` or `text`, and a boolean field\n"
    "  rejects a string with `must be a boolean (true/false or 0/1)`. `sso.require_site_access` can be\n"
    "  `true` only while `sso.enabled` is `true`, and `registration.terms.enabled` can be `true` only while\n"
    "  `registration.terms.reference` is set. Setting `sso.enabled` to `true` on its own fails with `4 fields are invalid`,\n"
    "  naming `tenant_name`, `policy_name`, `client_id` and `client_secret` under `sso.azure_ad_b2c`. A\n"
    "  write that breaks any of these rules is rejected with `400`.",
    "**All customer portal writes share one rate limit.** If you send eleven writes within about 3.25\n"
    "  seconds, the eleventh is rejected with `429` and a `Retry-After` header that counts down the time\n"
    "  left before writes are accepted again. Until then, writes to every customer portal path are\n"
    "  rejected, while writes to page settings and animation effects still succeed. Reads did not hit a\n"
    "  limit: forty reads within about 1.5 seconds all succeeded. A retry before `Retry-After` has passed\n"
    "  counts as another write, so wait until it has passed before you write again.",
]
