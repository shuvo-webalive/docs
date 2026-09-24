"""The Shopping cart settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Shopping cart"
SLUG = "shopping-cart"
BASE = "/admin/settings/page_settings/shopping_cart"
ICON = "cart-shopping"

GET_PAGE = "/api-reference/shopping-cart/get-shopping-cart-settings"
UPDATE_PAGE = "/api-reference/shopping-cart/update-shopping-cart-settings"

SECTIONS = ["cart_page", "flying_cart"]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `cart_page` for the cart page, or `flying_cart` for the slide-out flying cart.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "cart_page"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in both sections, keyed by section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_CART_PAGE = {"show_product_thumbnail": False, "enable_clear_cart": True, "save_cart": True}
SAMPLE_FLYING_CART = {"enabled": True, "enable_clear_cart": True, "save_cart": False}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_SHOPPING_CART = {
    "shopping_cart": {"cart_page": SAMPLE_CART_PAGE, "flying_cart": SAMPLE_FLYING_CART},
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_SHOPPING_CART = copy.deepcopy(SAMPLE_SHOPPING_CART)
PATCHED_SHOPPING_CART["shopping_cart"]["cart_page"]["show_product_thumbnail"] = True
PATCHED_SHOPPING_CART["shopping_cart"]["flying_cart"]["save_cart"] = True

PATCHED_CART_PAGE = dict(SAMPLE_CART_PAGE, show_product_thumbnail=True)


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


UNKNOWN_SECTION = error_example("not_found", "Unknown page-settings section: shopping_cart/bogus", [],
                                "6a2f9c41-3b7e-4d18-9c05-8e1d4f7a2b63")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

SHOPPING_CART_RESPONSE = {"type": "object", "properties": {
    "shopping_cart": ref("ShoppingCartSettings"),
    "group_meta": ref("ShoppingCartGroupMeta"),
}}

SECTION_BODY = {"type": "object", "properties": {
    "cart_page": ref("CartPage"),
    "flying_cart": ref("FlyingCart"),
}}

REPEATED_REJECTION = "After this rejection, the next write on the same client returns the same rejection under a new `request_id`, even when that write is correct. The write after it succeeds."

RATE_LIMITED = {"description": "Too many writes in a short time. Writes to both sections and to `/shopping_cart` are rejected until the time in the `Retry-After` header has passed. Reads still return `200`."}

UNKNOWN_SECTION_404 = {
    "description": "No section has that name. The error `code` is `not_found` and the message is `Unknown page-settings section: shopping_cart/<section>`.",
    "schema": ERROR,
    "example": UNKNOWN_SECTION,
}

ENDPOINTS = [
    {
        "key": "get_shopping_cart",
        "slug": "get-shopping-cart-settings",
        "title": "Get shopping cart settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns both shopping cart sections and a `group_meta` block describing each one.",
        "description": "Returns every shopping cart setting under `shopping_cart`, with the `cart_page` and `flying_cart` sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "Both sections and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(SHOPPING_CART_RESPONSE["properties"], field_metadata=dict(
                    ref("ShoppingCartFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section, then by field name.",
                ))},
                "example": SAMPLE_SHOPPING_CART,
            },
        },
        "example_call": {},
    },
    {
        "key": "patch_shopping_cart",
        "slug": "update-shopping-cart-settings",
        "title": "Update shopping cart settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or both sections and returns all settings.",
        "description": "Send the fields to change inside `shopping_cart`, grouped by section name. One body can change both sections. Only the fields you send change: other fields in the same section, and a section you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get shopping cart settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "required": ["shopping_cart"], "properties": {
                "shopping_cart": dict(ref("ShoppingCartSettings"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"shopping_cart": {"cart_page": {"show_product_thumbnail": True}, "flying_cart": {"save_cart": True}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": SHOPPING_CART_RESPONSE, "example": PATCHED_SHOPPING_CART},
            "400": {
                "description": "The body is not wrapped in `shopping_cart`. The error `code` is `invalid_request`, and the error names `shopping_cart`. " + REPEATED_REJECTION,
                "schema": ERROR,
            },
            "429": RATE_LIMITED,
        },
        "example_call": {},
    },
    {
        "key": "head_shopping_cart",
        "slug": "check-the-shopping-cart-settings",
        "title": "Check the shopping cart settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the shopping cart settings, including an `ETag`, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {},
    },
    {
        "key": "get_shopping_cart_section",
        "slug": "get-a-shopping-cart-section",
        "title": "Get a shopping cart section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one section, `cart_page` or `flying_cart`, under the section's own key.",
        "description": "Returns one section, wrapped in the section's own name, such as `flying_cart`, rather than in `shopping_cart`. The response has no `group_meta`. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": dict(SECTION_BODY["properties"], field_metadata=dict(
                    ref("ShoppingCartSectionFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by field name.",
                ))},
                "example": {"cart_page": SAMPLE_CART_PAGE},
            },
            "404": UNKNOWN_SECTION_404,
        },
        "example_call": {"path": {"section": "cart_page"}},
    },
    {
        "key": "patch_shopping_cart_section",
        "slug": "update-a-shopping-cart-section",
        "title": "Update a shopping cart section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `cart_page`. That is the only wrapper accepted: a body wrapped in `shopping_cart`, or not wrapped at all, is rejected with `400 invalid_request`. Returns the whole section after the change, under the same key and without `group_meta`.",
        "parameters": [SECTION],
        "body": {
            "schema": dict(SECTION_BODY, description="Wrap the fields in the name of the section in the path. No other wrapper is accepted."),
            "example": {"cart_page": {"show_product_thumbnail": True}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": SECTION_BODY, "example": {"cart_page": PATCHED_CART_PAGE}},
            "400": {
                "description": "The body is wrapped in `shopping_cart` or not wrapped at all, instead of in the section's name. The error `code` is `invalid_request`, `details[0].field` names the section and `details[0].code` is `required`. " + REPEATED_REJECTION,
                "schema": ERROR,
            },
            "404": UNKNOWN_SECTION_404,
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "cart_page"}},
    },
]


def flag(description, default):
    return {"type": "boolean", "description": description + " The store's default is `" + str(default).lower() + "`."}


REQUIRES_ENABLED = " Its `field_metadata` entry has `requires: \"enabled\"`. Setting `enabled` to `false` does not change this field's stored value."

SCHEMAS = {
    "ShoppingCartSettings": {"type": "object", "description": "Both shopping cart sections.", "properties": {
        "cart_page": ref("CartPage"),
        "flying_cart": ref("FlyingCart"),
    }},
    "CartPage": {"type": "object", "description": "What the cart page offers a shopper.", "properties": {
        "show_product_thumbnail": flag("Show product images on the cart page.", True),
        "enable_clear_cart": flag("Show a button that empties the cart.", False),
        "save_cart": flag("Show the Save cart button on the cart page. The button comes from the `save-cart` plugin.", False),
    }},
    "FlyingCart": {"type": "object", "description": "The slide-out flying cart, and what it offers a shopper.", "properties": {
        "enabled": flag("Show the slide-out flying cart.", False),
        "enable_clear_cart": flag("Show the empty cart button inside the flying cart." + REQUIRES_ENABLED, False),
        "save_cart": flag("Show the Save cart action inside the flying cart. The action comes from the `save-cart` plugin." + REQUIRES_ENABLED, False),
    }},
    "ShoppingCartGroupMeta": {"type": "object", "description": "One entry per section. Only [Get shopping cart settings](" + GET_PAGE + ") and [Update shopping cart settings](" + UPDATE_PAGE + ") return it.", "properties": {
        "cart_page": ref("ShoppingCartSectionMeta"),
        "flying_cart": ref("ShoppingCartSectionMeta"),
    }},
    "ShoppingCartSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for both sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for both sections."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/page_settings/shopping_cart/cart_page`."},
    }},
    "ShoppingCartFieldMetadata": {"type": "object", "description": "Describes every field, keyed by section and then by field name.", "properties": {
        "cart_page": ref("ShoppingCartSectionFieldMetadata"),
        "flying_cart": ref("ShoppingCartSectionFieldMetadata"),
    }},
    "ShoppingCartSectionFieldMetadata": {"type": "object", "description": "One entry for each of the section's fields, keyed by field name.", "additionalProperties": ref("ShoppingCartFieldMetadataEntry")},
    "ShoppingCartFieldMetadataEntry": {"type": "object", "properties": {
        "ui_label": {"type": "string", "description": "The field's label, such as `Display Flying Cart`."},
        "description": {"type": "string", "description": "What the field does."},
        "type": {"type": "string", "description": "The kind of value the field takes. `boolean` for every shopping cart field."},
        "default": {"type": "boolean", "description": "The field's default value."},
        "plugin": {"type": "string", "description": "The plugin that provides the feature: `save-cart`. Only the two `save_cart` fields have it."},
        "requires": {"type": "string", "description": "The field of the same section that this one depends on: `enabled`. Only `flying_cart.enable_clear_cart` and `flying_cart.save_cart` have it."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
            "message": {"type": "string", "description": "What went wrong. For an unknown section, it is `Unknown page-settings section: shopping_cart/<section>`."},
            "details": {"type": "array", "description": "More about the rejection. When a section write is not wrapped in the section's name, the first entry's `field` names the section and its `code` is `required`.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The field or wrapper the rejection is about."},
                "code": {"type": "string", "description": "Why it was rejected, such as `required`."},
            }}},
            "request_id": {"type": "string", "description": "Identifies the request. A response that repeats an earlier rejection has a new `request_id`."},
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Read and change what your store's cart page and slide-out flying cart offer shoppers."
INTRO = "The Shopping cart API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/page_settings/shopping_cart`."
WARNING = (
    "Every write body must be wrapped in a key, and the key depends on the path. On `/shopping_cart`,\n"
    "  wrap the fields in `shopping_cart` and then in the section name. On `/shopping_cart/{section}`,\n"
    "  wrap them in the section's own name only, such as `cart_page`: a body wrapped in\n"
    "  `shopping_cart`, or not wrapped at all, is rejected with `400 invalid_request`."
)
NOTES = [
    "**The settings are split into two sections.** `cart_page` controls the cart page: product\n"
    "  images, the empty cart button and the Save cart button. `flying_cart` turns the slide-out flying\n"
    "  cart on or off and controls its empty cart button and Save cart action. Read or write both\n"
    "  through `/shopping_cart`, or one through `/shopping_cart/{section}`. An unknown section returns\n"
    "  `404 not_found`.",
    "**`PATCH` is the only way to write.** `PUT`, `POST` and `DELETE` are rejected on `/shopping_cart`\n"
    "  and on both section paths with `405 method_not_allowed` and an `Allow: GET, HEAD, PATCH, OPTIONS`\n"
    "  header. On `/shopping_cart`, only the fields you send change, and one body can change both\n"
    "  sections.",
    "**Add `field_metadata=true` to a read to get a description of every field.** The settings are\n"
    "  still returned with it. Each entry gives the field's `ui_label`, `description`, `type` and\n"
    "  `default`, and every field is a `boolean`. The two `save_cart` fields also have\n"
    "  `plugin: \"save-cart\"`, and `flying_cart.enable_clear_cart` and `flying_cart.save_cart` have\n"
    "  `requires: \"enabled\"`. Setting `flying_cart.enabled` to `false` leaves those two fields' stored\n"
    "  values as they are. On `/shopping_cart` the block is keyed by section; on a section it is keyed\n"
    "  by field name.",
    "**All shopping cart writes share one rate limit.** If you send eleven writes within about 1.3\n"
    "  seconds, the eleventh is rejected with `429` and a `Retry-After` header that counts down the time\n"
    "  left before writes are accepted again. Until then, writes to either section and to\n"
    "  `/shopping_cart` are all rejected, while reads still return `200`. A retry before then counts as\n"
    "  another write, so wait until `Retry-After` has passed before you write again.",
    "**After a rejected write, the next write on the same client returns that rejection again.** It\n"
    "  comes back under a new `request_id`, even when the second write is correct and goes to the other\n"
    "  section. The write after that succeeds.",
]
