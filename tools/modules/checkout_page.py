"""The Checkout page settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Checkout page"
SLUG = "checkout-page"
BASE = "/admin/settings/page_settings/checkout_page"
ICON = "cash-register"

SECTIONS = ["billing_address", "shipping_address", "customer_checkout", "delivery_options", "order_summary", "others"]
WRITABLE_SECTIONS = ["customer_checkout", "delivery_options", "order_summary", "others"]

GET_PAGE = "/api-reference/checkout-page/get-checkout-page-settings"
UPDATE_PAGE = "/api-reference/checkout-page/update-checkout-page-settings"
SECTION_PAGE = "/api-reference/checkout-page/get-a-settings-section"

OVERVIEW_DESCRIPTION = "Read your checkout page's address forms, and read and change its sign-in, delivery, order summary and other settings."
INTRO = "The Checkout page API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/page_settings/checkout_page`."

WARNING = (
    "**After a `400`, the next call on the same client gets the wrong response.** That call returns the\n"
    "  previous call's response instead of its own: the same `400` again, or a `200` with the body of the\n"
    "  path you called before. The request you sent never reaches the store, so a write in it is not saved.\n"
    "  The call after that works normally. After a `400`, make your next call from a new client."
)

NOTES = [
    "**The settings are split into six sections, and two of them are read-only.** The sections are\n"
    "  `billing_address`, `shipping_address`, `customer_checkout`, `delivery_options`, `order_summary` and\n"
    "  `others`. `group_meta` marks `billing_address` and `shipping_address` `writable: false`, so write only\n"
    "  the other four. Read all six through `/checkout_page`, or one through `/checkout_page/{section}`.",
    "**Every write body must be wrapped, and the wrapper depends on the path.** On `/checkout_page`, wrap\n"
    "  the fields in `checkout_page` and then in the section name. On `/checkout_page/{section}`, wrap them\n"
    "  in the section's own name only, such as `order_summary`. A body without the right wrapper is\n"
    "  rejected with `400 invalid_request`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values, including other fields in the same block and sections you did not name.\n"
    "  `PUT`, `POST` and `DELETE` are rejected on every path with `405 method_not_allowed` and an\n"
    "  `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Some combinations of settings are rejected.** In `customer_checkout`, at least one of `allow_sign_in`,\n"
    "  `allow_sign_up` and `checkout_as_guest` must stay on. In `delivery_options`, at least one of the four\n"
    "  delivery options must stay on. A body that breaks a rule is rejected with `400 invalid_request`, and\n"
    "  `details[0].code` is `constraint_violation`. Read the section with `field_metadata=true` to get its\n"
    "  rules in `_rules`.",
    "**Writes and reads are rate limited.** The eleventh write in a short window is rejected with\n"
    "  `429 rate_limited` and the message `Too many writes to this resource`. Until the window ends, writes\n"
    "  to `/checkout_page`, to other sections and to the product page settings are rejected too, while\n"
    "  reads still return `200`. The `Retry-After` header counts down the seconds left, so wait that long before you\n"
    "  write again. Reads have their own limit: the twenty-first read in about one second is rejected, with\n"
    "  `Retry-After: 10`.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read: `billing_address`, `shipping_address`, `customer_checkout`, `delivery_options`, `order_summary` or `others`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "order_summary"},
}

WRITABLE_SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to write: `customer_checkout`, `delivery_options`, `order_summary` or `others`. `group_meta` marks `billing_address` and `shipping_address` `writable: false`, so they are not listed.",
    "schema": {"type": "string", "enum": WRITABLE_SECTIONS, "example": "order_summary"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, keyed by section. It describes the fields of the four writable sections one by one, and each address section as a single `resource` entry with `read_only: true`. It also has a `_legacy_field_map` entry, which gives the flat name the older admin save uses for twelve of the fields. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. For `customer_checkout` and `delivery_options` it also has `_rules`, the list of rules the store enforces: a write that breaks one is rejected with `400`. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_ACTIVE_FIELDS = ["first_name", "last_name", "country", "address_line_1", "post_code", "city", "phone", "email"]


def address_field(key, active, required, order, group):
    return {"key": key, "label": None, "active": active, "required": required, "order": order, "group": group}


SAMPLE_ADDRESS_FIELDS = [
    address_field("first_name", True, True, 1, "name"),
    address_field("last_name", True, False, 2, "name"),
    address_field("country", True, True, 2, ""),
    address_field("address_line_1", True, True, 3, ""),
    address_field("post_code", True, True, 1, "postcity"),
    address_field("city", True, True, 2, "postcity"),
    address_field("address_line_2", False, False, 5, ""),
    address_field("phone", True, False, 6, ""),
    address_field("mobile", False, False, 7, ""),
    address_field("fax", False, False, 8, ""),
    address_field("email", True, True, 9, ""),
    address_field("confirm_email", False, False, 10, ""),
    address_field("company_name", False, False, 11, ""),
]

SAMPLE_CUSTOMER_CHECKOUT = {
    "allow_sign_in": True,
    "allow_sign_up": {"enabled": True, "required": False},
    "checkout_as_guest": {"enabled": True, "quick_signup": False},
    "newsletter_subscription": True,
    "multiple_shipping_methods": False,
}

SAMPLE_DELIVERY_OPTIONS = {
    "enable_shipping": True,
    "enable_store_pickup": True,
    "enable_shipping_quote": True,
    "enable_delivery_service": True,
}

SAMPLE_ORDER_SUMMARY = {
    "show_product_thumbnail": True,
    "show_quantity": True,
    "enable_payment_expand_view": True,
    "order_confirm_captcha": False,
}

SAMPLE_OTHERS = {
    "show_logo": False,
    "login_url": "https://your-store.example.com/customer/login?referer=/shop/checkout",
    "custom_html": "<div class=\"help-policy\"><p>Need help? <a href=\"/contact-us\">Contact Us</a></p></div>",
    "comment": {"enabled": False, "send_notification": False},
    "terms_and_condition": {
        "enabled": True,
        "text": "By placing this order, I agree to be bound by the ",
        "link_label": "Terms and Conditions.",
        "type": "link",
        "ref": {"link": "https://your-store.example.com/terms-and-conditions"},
    },
}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": section in WRITABLE_SECTIONS, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_CHECKOUT_PAGE = {
    "checkout_page": {
        "billing_address": {"active_fields": SAMPLE_ACTIVE_FIELDS},
        "shipping_address": {"active_fields": SAMPLE_ACTIVE_FIELDS},
        "customer_checkout": SAMPLE_CUSTOMER_CHECKOUT,
        "delivery_options": SAMPLE_DELIVERY_OPTIONS,
        "order_summary": SAMPLE_ORDER_SUMMARY,
        "others": SAMPLE_OTHERS,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_CHECKOUT_PAGE = copy.deepcopy(SAMPLE_CHECKOUT_PAGE)
PATCHED_CHECKOUT_PAGE["checkout_page"]["order_summary"]["enable_payment_expand_view"] = False
PATCHED_CHECKOUT_PAGE["checkout_page"]["customer_checkout"]["multiple_shipping_methods"] = True

PATCHED_ORDER_SUMMARY = dict(copy.deepcopy(SAMPLE_ORDER_SUMMARY), show_product_thumbnail=False)


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

RATE_LIMITED = {"description": "Too many writes in a short time. The error code is `rate_limited`, the message is `Too many writes to this resource`, and the `Retry-After` header counts down the seconds until you can write again."}

CHECKOUT_PAGE_RESPONSE = {"type": "object", "properties": {
    "checkout_page": ref("CheckoutPageSettings"),
    "group_meta": ref("CheckoutGroupMeta"),
}}

SECTION_PROPERTIES = {
    "billing_address": ref("CheckoutAddressForm"),
    "shipping_address": ref("CheckoutAddressForm"),
    "customer_checkout": ref("CheckoutCustomerCheckout"),
    "delivery_options": ref("CheckoutDeliveryOptions"),
    "order_summary": ref("CheckoutOrderSummary"),
    "others": ref("CheckoutOthers"),
}

WRITABLE_PROPERTIES = {section: SECTION_PROPERTIES[section] for section in WRITABLE_SECTIONS}

ENDPOINTS = [
    {
        "key": "get_checkout_page",
        "slug": "get-checkout-page-settings",
        "title": "Get checkout page settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all six checkout page settings sections, and a `group_meta` block describing each one.",
        "description": "Returns all six sections under `checkout_page`. The two address sections list only their active field keys, in `active_fields`; [Get a settings section](" + SECTION_PAGE + ") returns their full field list. Beside the settings, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of each section's fields, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All six sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(CHECKOUT_PAGE_RESPONSE["properties"], field_metadata=dict(
                    ref("CheckoutFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section, with a `_legacy_field_map` entry beside the six.",
                ))},
                "example": SAMPLE_CHECKOUT_PAGE,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_checkout_page",
        "slug": "update-checkout-page-settings",
        "title": "Update checkout page settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change inside `checkout_page`, grouped by section name; one body can name several sections. Only the fields you send change: other fields in the same block, and sections you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get checkout page settings](" + GET_PAGE + ") does. A body that is not wrapped in `checkout_page` is rejected with `400 invalid_request`.",
        "body": {
            "schema": {"type": "object", "required": ["checkout_page"], "properties": {
                "checkout_page": {
                    "type": "object",
                    "description": "The fields to change, grouped by section. Send only the fields that change. Only the four sections `group_meta` marks `writable: true` can be written.",
                    "properties": WRITABLE_PROPERTIES,
                },
            }},
            "example": {"checkout_page": {"order_summary": {"enable_payment_expand_view": False}, "customer_checkout": {"multiple_shipping_methods": True}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": CHECKOUT_PAGE_RESPONSE, "example": PATCHED_CHECKOUT_PAGE},
            "400": {
                "description": "The body is not wrapped in `checkout_page`: `details[0].field` is `checkout_page` and `details[0].code` is `required`. Or the body breaks one of the rules listed under `_rules` in `field_metadata`: `details[0].code` is `constraint_violation` and the message quotes the rule.",
                "schema": ERROR,
                "example": error_example("invalid_request", "request body must be wrapped in a 'checkout_page' object",
                                         [{"field": "checkout_page", "code": "required", "message": "the request body must be wrapped in a 'checkout_page' object"}],
                                         "552dcbb3-a758-48e5-bff8-3df2225d3b69"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_checkout_page",
        "slug": "get-checkout-page-settings-headers",
        "title": "Get checkout page settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the checkout page settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_checkout_page_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `order_summary`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `checkout_page`, and without `group_meta`. For `billing_address` and `shipping_address` it returns `fields`: each form field with its `key`, `label`, `active`, `required`, `order` and `group`, inactive fields included. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": dict(
                    SECTION_PROPERTIES,
                    field_metadata=dict(ref("CheckoutFieldMetadata"), description="Only when you send `field_metadata=true`. Keyed by field name, with a `_rules` entry for `customer_checkout` and `delivery_options`."),
                )},
                "example": {"order_summary": SAMPLE_ORDER_SUMMARY},
            },
            "404": {
                "description": "No section has that name. The error `code` is `not_found` and the message is `Unknown page-settings section: checkout_page/<section>`.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown page-settings section: checkout_page/bogus", [], "4d7a2c18-9e3b-4f65-b1d0-6a8e5c2f7b39"),
            },
        },
        "example_call": {"path": {"section": "order_summary"}},
    },
    {
        "key": "patch_checkout_page_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `order_summary`. That is the only wrapper accepted: a body wrapped in `checkout_page`, or not wrapped at all, is rejected with `400 invalid_request`, and `details[0].field` names the section. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under the same key and without `group_meta`.",
        "parameters": [WRITABLE_SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path. No other wrapper is accepted.", "properties": WRITABLE_PROPERTIES},
            "example": {"order_summary": {"show_product_thumbnail": False}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": {"type": "object", "properties": WRITABLE_PROPERTIES}, "example": {"order_summary": PATCHED_ORDER_SUMMARY}},
            "400": {
                "description": "The body is not wrapped in the section's own name: `details[0].field` names the section and `details[0].code` is `required`. Or the body breaks one of the section's `_rules`: `details[0].code` is `constraint_violation` and the message quotes the rule.",
                "schema": ERROR,
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "order_summary"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def text(description, **extra):
    return dict({"type": "string", "description": description}, **extra)


ADDRESS_KEYS = [
    "first_name", "last_name", "country", "address_line_1", "address_line_2", "post_code", "city",
    "state", "phone", "mobile", "fax", "email", "confirm_email", "company_name",
]

SCHEMAS = {
    "CheckoutPageSettings": {"type": "object", "description": "All six sections, as [Get checkout page settings](" + GET_PAGE + ") returns them.", "properties": {
        "billing_address": dict(ref("CheckoutAddressFieldKeys"), description="The billing address form's active field keys. Read-only."),
        "shipping_address": dict(ref("CheckoutAddressFieldKeys"), description="The shipping address form's active field keys. Read-only."),
        "customer_checkout": ref("CheckoutCustomerCheckout"),
        "delivery_options": ref("CheckoutDeliveryOptions"),
        "order_summary": ref("CheckoutOrderSummary"),
        "others": ref("CheckoutOthers"),
    }},
    "CheckoutAddressFieldKeys": {"type": "object", "description": "An address section as `/checkout_page` returns it.", "properties": {
        "active_fields": {"type": "array", "items": {"type": "string", "enum": ADDRESS_KEYS}, "description": "The keys of the fields that show on the form, such as `first_name` and `post_code`."},
    }},
    "CheckoutAddressForm": {"type": "object", "description": "An address section as `/checkout_page/{section}` returns it. Read-only: `group_meta` marks it `writable: false`.", "properties": {
        "fields": {"type": "array", "items": ref("CheckoutAddressField"), "description": "Each form field, inactive fields included."},
    }},
    "CheckoutAddressField": {"type": "object", "description": "One field of an address form, and how it shows.", "properties": {
        "key": text("The field's key.", enum=ADDRESS_KEYS),
        "label": text("The label shown for the field. `null` means the field's default label.", type=["string", "null"]),
        "active": flag("Whether the field shows on the form."),
        "required": flag("Whether the customer must fill in the field."),
        "order": {"type": "integer", "minimum": 1, "maximum": 99, "description": "The field's position on the form."},
        "group": text("The layout group the field belongs to: `name`, `postcity`, or an empty string for none. The store sets it from its field catalog, and `field_metadata` marks it `read_only`.", enum=["name", "postcity", ""]),
    }},
    "CheckoutCustomerCheckout": {"type": "object", "description": "How customers sign in, sign up or check out as a guest. At least one of `allow_sign_in`, `allow_sign_up` and `checkout_as_guest` must stay on.", "properties": {
        "allow_sign_in": flag("Let returning customers sign in during checkout."),
        "allow_sign_up": ref("CheckoutSignUp"),
        "checkout_as_guest": ref("CheckoutGuestCheckout"),
        "newsletter_subscription": flag("Show a newsletter opt-in on the checkout page."),
        "multiple_shipping_methods": flag("Show only multi-select options."),
    }},
    "CheckoutSignUp": {"type": "object", "description": "Whether customers can, or must, create an account during checkout.", "properties": {
        "enabled": flag("Let customers create an account during checkout."),
        "required": flag("Make customers create an account to place an order."),
    }},
    "CheckoutGuestCheckout": {"type": "object", "description": "Whether customers can order without an account.", "properties": {
        "enabled": flag("Let customers order without an account."),
        "quick_signup": flag("Offer guests a one-click account creation."),
    }},
    "CheckoutDeliveryOptions": {"type": "object", "description": "The delivery options offered at checkout. At least one of the four must stay on.", "properties": {
        "enable_shipping": flag("Offer shipping."),
        "enable_store_pickup": flag("Offer in-store pickup."),
        "enable_shipping_quote": flag("Offer a request-a-shipping-quote option."),
        "enable_delivery_service": flag("Offer on-demand delivery: a delivery date picker shows at checkout."),
    }},
    "CheckoutOrderSummary": {"type": "object", "description": "What the checkout's order summary shows.", "properties": {
        "show_product_thumbnail": flag("Show product images in the order summary."),
        "show_quantity": flag("Show the quantity column or label."),
        "enable_payment_expand_view": flag("Expand the payment section by default."),
        "order_confirm_captcha": flag("Ask for a CAPTCHA before the order is confirmed."),
    }},
    "CheckoutOthers": {"type": "object", "description": "The checkout page's logo, login link, custom HTML, order comments and terms and conditions.", "properties": {
        "show_logo": flag("Show the store logo on the checkout page."),
        "login_url": text("The URL of the customer login page. When it is not set, the store returns the login URL it works out itself. It cannot be cleared.", maxLength=255),
        "custom_html": text("Custom HTML shown on the checkout page.", maxLength=65535),
        "comment": ref("CheckoutOrderComment"),
        "terms_and_condition": ref("CheckoutTermsAndCondition"),
    }},
    "CheckoutOrderComment": {"type": "object", "description": "Whether customers can add a comment to an order, and whether staff get an email about it.", "properties": {
        "enabled": flag("Let customers add a comment to their order."),
        "send_notification": flag("Email staff when an order comment is added. Reads `false` while `enabled` is `false`."),
    }},
    "CheckoutTermsAndCondition": {"type": "object", "description": "Whether customers must accept terms and conditions before ordering, and where the terms are.", "properties": {
        "enabled": flag("Make customers accept the terms and conditions before ordering."),
        "text": text("The text shown before the terms link."),
        "link_label": text("The text of the terms link."),
        "type": text("Where the terms come from: `page`, `link` or `text`.", enum=["page", "link", "text"]),
        "ref": ref("CheckoutTermsReference"),
    }},
    "CheckoutTermsReference": {"type": "object", "description": "Where the terms are. Holds only the one key that matches `type`.", "properties": {
        "page": {"description": "The terms page, when `type` is `page`: an object with the page's `id` and the page's `name`."},
        "link": text("The URL of the terms, when `type` is `link`."),
        "text": text("The terms text, when `type` is `text`."),
    }},
    "CheckoutGroupMeta": {"type": "object", "description": "One entry per section. Only [Get checkout page settings](" + GET_PAGE + ") and [Update checkout page settings](" + UPDATE_PAGE + ") return it.", "properties": {
        section: ref("CheckoutSectionMeta") for section in SECTIONS
    }},
    "CheckoutSectionMeta": {"type": "object", "properties": {
        "kind": text("What the section is. `setting` for all six sections."),
        "writable": flag("Whether you can write to the section. `false` for `billing_address` and `shipping_address`, `true` for the other four."),
        "href": text("The section's own path, such as `/api/v4/admin/settings/page_settings/checkout_page/order_summary`."),
    }},
    "CheckoutFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `CheckoutFieldMetadataEntry` in place of each value. On `/checkout_page` it also has `_legacy_field_map`, and it describes each address section as one `resource` entry with `read_only: true`. On `customer_checkout` and `delivery_options` it also has `_rules`, the list of rules the store enforces on a write."},
    "CheckoutFieldMetadataEntry": {"type": "object", "properties": {
        "ui_label": text("The field's label."),
        "description": text("What the field does."),
        "type": text("The kind of value the field takes: `boolean`, `string`, `enum`, `array` for an address section's `fields`, or `resource` for an address section on `/checkout_page`."),
        "default": {"description": "The field's default value."},
        "allowed_values": {"type": "array", "items": {}, "description": "The values the field accepts. `others.terms_and_condition.type` is the one `enum` field and lists `page`, `link` and `text`."},
        "max_length": {"type": "integer", "description": "The longest value accepted, for a `string` field."},
        "required": flag("`true` when the field must have a value. On `/checkout_page`, `others.login_url` is the one field marked required."),
        "read_only": flag("`true` when you cannot write the field or section."),
        "href": text("For an address section on `/checkout_page`: the section's own path, such as `/api/v4/admin/settings/page_settings/checkout_page/billing_address`."),
        "item_schema": {"type": "object", "description": "For an address section's `fields`: a description of each of the six keys of a field record."},
        "catalog": {"type": "array", "items": {"type": "object"}, "description": "For an address section's `fields`: every field key the form can use."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": text("A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."),
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": text("The field that was rejected."),
                "code": text("Why it was rejected, such as `required` or `constraint_violation`."),
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": text("The id the store gave this request."),
        }},
    }},
}
