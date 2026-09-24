"""The Price display settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Price display settings"
SLUG = "price-display-settings"
BASE = "/admin/settings/price_display_settings"
ICON = "receipt"

SECTIONS = ["order_item", "order_summary"]

GET_PAGE = "/api-reference/price-display-settings/get-price-display-settings"
UPDATE_PAGE = "/api-reference/price-display-settings/update-price-display-settings"

OVERVIEW_DESCRIPTION = "Read and change how prices, tax, discounts and order totals show in the shopping cart, at checkout and on the order success page."
INTRO = "The Price display settings API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/price_display_settings`."

WARNING = (
    "**While a block's `customize` is `false`, its `scopes` follow its `enabled` value, whatever you send in `scopes`.**\n"
    "  Set `enabled` to `true` on such a block and the response shows every surface the block accepts as\n"
    "  `true`, even if your body sent other `scopes` values. Set `enabled` back and the scopes change back\n"
    "  with it. To set the surfaces one by one, send `customize: true` with your `scopes`."
)

NOTES = [
    "**The settings are split into two sections.** `order_item` controls how each line item's own price\n"
    "  shows. `order_summary` controls the lines of the order summary, such as the subtotal, discount,\n"
    "  shipping cost, handling and order total, and what each line includes. Read or write both through\n"
    "  `/price_display_settings`, or one through `/price_display_settings/{section}`. Reading a section\n"
    "  that does not exist returns `404 not_found`.",
    "**The wrapper a write needs depends on the path.** On `/price_display_settings`, wrap the fields in\n"
    "  `price_display_settings` and then in the section name: a body without that wrapper is rejected with\n"
    "  `400 invalid_request`. On `/price_display_settings/{section}`, wrap them in the section's own name,\n"
    "  such as `order_item`, or send them with no wrapper at all. A section body wrapped in\n"
    "  `price_display_settings` is rejected with `400 invalid_request`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values, at every level of nesting and in a section you did not name. One body on\n"
    "  `/price_display_settings` can change both sections. `PUT`, `POST` and `DELETE` are rejected on all\n"
    "  three paths with `405 method_not_allowed` and an `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Add `field_metadata=true` to a read to get a description of every field.** The settings are still\n"
    "  returned with it. Each entry gives the field's `ui_label`, `description` and `type`, which is\n"
    "  `boolean`, `string` or `scope_flags`. A `scope_flags` entry lists the surfaces the block accepts in\n"
    "  `allowed_scopes`, with a label for each in `scope_labels`. A write that sends any other surface is\n"
    "  rejected with `400 invalid_request` and the reason `invalid_enum`. On `/price_display_settings`,\n"
    "  `field_metadata` is keyed by section; on a section path it holds that section under its own name.",
    "**Each block accepts its own set of surfaces.** The three surfaces are `shopping_cart`, `checkout`\n"
    "  and `order_success`. `tax_in_line` and `item_total_including_tax` accept `shopping_cart` and\n"
    "  `order_success` only. `shipping_cost`, `shipping_discount`, `handling` and `payment_surcharge`\n"
    "  accept `checkout` and `order_success` only. A response lists only the surfaces a block accepts.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `order_item` or `order_summary`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "order_item"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in both sections, keyed by section. The settings and `group_meta` are still returned. The value must be `true`/`false` or `1`/`0`.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_FOR_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields under the section's own name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}


def scoped(enabled, surfaces):
    return {"enabled": enabled, "customize": False, "scopes": {surface: enabled for surface in surfaces}}


ALL = ["shopping_cart", "checkout", "order_success"]
CART_AND_SUCCESS = ["shopping_cart", "order_success"]
CHECKOUT_AND_SUCCESS = ["checkout", "order_success"]

SAMPLE_ORDER_ITEM = {
    "price_including_tax": scoped(False, ALL),
    "price_including_discount": scoped(False, ALL),
    "tax_in_line": scoped(False, CART_AND_SUCCESS),
    "discount_in_line_item": scoped(False, ALL),
    "item_total_including_tax": scoped(False, CART_AND_SUCCESS),
}

SAMPLE_ORDER_SUMMARY = {
    "order_total_excluding_tax": scoped(False, ALL),
    "order_total_including_discount": scoped(False, ALL),
    "subtotal": {
        "show": {"shopping_cart": True, "checkout": True, "order_success": True},
        "include_tax": scoped(False, ALL),
        "include_discount": scoped(False, ALL),
    },
    "discount": {
        "show": {"shopping_cart": True, "checkout": True, "order_success": True},
        "hide_if_zero": scoped(False, ALL),
        "include_tax": scoped(False, ALL),
    },
    "subtotal_tax": {"enabled": False},
    "total_tax": {"enabled": False},
    "order_total": {"enabled": True},
    "shipping_cost": {
        "show": {"checkout": True, "order_success": True},
        "include_tax": scoped(False, CHECKOUT_AND_SUCCESS),
        "include_discount": scoped(False, CHECKOUT_AND_SUCCESS),
    },
    "shipping_discount": {
        "show": {"checkout": False, "order_success": False},
        "include_tax": scoped(False, CHECKOUT_AND_SUCCESS),
        "shipping_tax": {"enabled": True},
    },
    "handling": {
        "show_separately": {"checkout": False, "order_success": False},
        "include_tax": scoped(False, CHECKOUT_AND_SUCCESS),
        "handling_tax": scoped(False, CHECKOUT_AND_SUCCESS),
    },
    "payment_surcharge": scoped(False, CHECKOUT_AND_SUCCESS),
    "pricing_info": {
        "enabled": False,
        "text": "",
        "customize": False,
        "scopes": {"shopping_cart": False, "checkout": False, "order_success": False},
        "do_not_show_due_amount": False,
    },
}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_PRICE_DISPLAY_SETTINGS = {
    "price_display_settings": {
        "order_item": SAMPLE_ORDER_ITEM,
        "order_summary": SAMPLE_ORDER_SUMMARY,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_PRICE_DISPLAY_SETTINGS = copy.deepcopy(SAMPLE_PRICE_DISPLAY_SETTINGS)
PATCHED_PRICE_DISPLAY_SETTINGS["price_display_settings"]["order_item"]["price_including_tax"] = scoped(True, ALL)
PATCHED_PRICE_DISPLAY_SETTINGS["price_display_settings"]["order_summary"]["payment_surcharge"] = scoped(True, CHECKOUT_AND_SUCCESS)

PATCHED_ORDER_ITEM = dict(copy.deepcopy(SAMPLE_ORDER_ITEM), price_including_discount=scoped(True, ALL))


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

FACADE_RESPONSE = {"type": "object", "properties": {
    "price_display_settings": ref("PriceDisplaySettings"),
    "group_meta": ref("PriceDisplayGroupMeta"),
}}

SECTION_RESPONSE = {"type": "object", "description": "Holds only the key of the section in the path.", "properties": {
    "order_item": ref("PriceDisplayOrderItem"),
    "order_summary": ref("PriceDisplayOrderSummary"),
}}

ENDPOINTS = [
    {
        "key": "get_price_display_settings",
        "slug": "get-price-display-settings",
        "title": "Get price display settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns both settings sections and a `group_meta` block describing each one.",
        "description": "Returns every price display setting under `price_display_settings`, with both sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "Both sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(FACADE_RESPONSE["properties"], field_metadata=dict(
                    ref("PriceDisplayFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section.",
                ))},
                "example": SAMPLE_PRICE_DISPLAY_SETTINGS,
            },
            "400": {
                "description": "You sent a query parameter the call does not accept: the message is `unknown query parameter(s): <name>` and `details[0].code` is `unknown_parameter`. Or `field_metadata` is not `true`/`false` or `1`/`0`: the message is `field_metadata must be true/false or 0/1` and `details[0].code` is `invalid_boolean`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "unknown query parameter(s): bogus",
                                         [{"field": "bogus", "code": "unknown_parameter", "message": None}],
                                         "5b2e8c41-7d3a-4f6b-9e10-3a8c2d7f4b65"),
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_price_display_settings",
        "slug": "update-price-display-settings",
        "title": "Update price display settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or both sections and returns all settings.",
        "description": "Send the fields to change inside `price_display_settings`, grouped by section name; one body can change both sections. Only the fields you send change, and everything you leave out keeps its stored value. Returns all the settings after the change, with `group_meta`, as [Get price display settings](" + GET_PAGE + ") does. A body not wrapped in `price_display_settings` is rejected with `400 invalid_request`.",
        "body": {
            "schema": {"type": "object", "required": ["price_display_settings"], "properties": {
                "price_display_settings": dict(ref("PriceDisplaySettings"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"price_display_settings": {
                "order_item": {"price_including_tax": {"enabled": True, "customize": False}},
                "order_summary": {"payment_surcharge": {"enabled": True, "customize": False}},
            }},
        },
        "responses": {
            "200": {
                "description": "All the settings after the change, with `group_meta`. While a block's `customize` is `false`, its `scopes` follow its `enabled` value.",
                "schema": FACADE_RESPONSE,
                "example": PATCHED_PRICE_DISPLAY_SETTINGS,
            },
            "400": {
                "description": "The body is not wrapped in `price_display_settings` (`required`), names a section or field that does not exist (`unknown_field`), sends a value other than `true`/`false` or `1`/`0` for a `true`/`false` field (`invalid_boolean`), sends a surface the block does not accept (`invalid_enum`), or sends a `pricing_info.text` longer than 2000 characters (`too_long`). `details` has one entry per rejected field, and each entry's `code` gives the reason. An empty section, such as `\"order_item\": {}`, is rejected too, with the message `no recognized price_display_settings fields in body` and an empty `details`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "request body must be wrapped in a 'price_display_settings' object",
                                         [{"field": "price_display_settings", "code": "required", "message": "the request body must be wrapped in a 'price_display_settings' object"}],
                                         "c47a1e93-2b6d-4f08-8a5c-9d3e7b1f6a20"),
            },
            "415": {
                "description": "The `Content-Type` header is not `application/json`. The message is `Content-Type must be application/json` and `details[0].code` is `unsupported_media_type`.",
                "schema": ERROR,
                "example": error_example("unsupported_media_type", "Content-Type must be application/json",
                                         [{"field": "Content-Type", "code": "unsupported_media_type", "message": None, "value": "text/plain"}],
                                         "3a9f6c12-8e4b-4d27-b5a0-6c1e9d2f7b48"),
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_price_display_settings",
        "slug": "get-price-display-settings-headers",
        "title": "Get price display settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the price display settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_price_display_settings_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `order_item`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `price_display_settings`, and without `group_meta`. Its values are the same as that section's part of [Get price display settings](" + GET_PAGE + "). Add `field_metadata=true` to also get a description of the section's fields, under the section's own name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_FOR_SECTION],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": {
                    "order_item": ref("PriceDisplayOrderItem"),
                    "order_summary": ref("PriceDisplayOrderSummary"),
                    "field_metadata": dict(ref("PriceDisplayFieldMetadata"), description="Only when you send `field_metadata=true`. Holds one key, the section's own name."),
                }},
                "example": {"order_item": SAMPLE_ORDER_ITEM},
            },
            "404": {
                "description": "No section has that name. The message is `Unknown price_display_settings section: <section>`. Right after another settings area rejects a call on its section path with `400`, the next call on the same client can also return this `404` once, naming the last part of that earlier path as the section.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown price_display_settings section: bogus_section", [],
                                         "8d3f5a27-6c1e-4b94-a0d8-2e7b9c4f1a36"),
            },
        },
        "example_call": {"path": {"section": "order_item"}},
    },
    {
        "key": "patch_price_display_settings_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change wrapped in the section's own name, such as `order_item`, or send them with no wrapper at all. A body wrapped in `price_display_settings` is rejected with `400 invalid_request`, and the error names `<section>.price_display_settings` as an unknown field. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under its own key and without `group_meta`.",
        "parameters": [SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the name of the section in the path, or send them with no wrapper. Do not wrap them in `price_display_settings`.", "properties": {
                "order_item": ref("PriceDisplayOrderItem"),
                "order_summary": ref("PriceDisplayOrderSummary"),
            }},
            "example": {"order_item": {"price_including_discount": {"enabled": True}}},
        },
        "responses": {
            "200": {
                "description": "The whole section after the change, under its own key. While a block's `customize` is `false`, its `scopes` follow its `enabled` value.",
                "schema": SECTION_RESPONSE,
                "example": {"order_item": PATCHED_ORDER_ITEM},
            },
            "400": {
                "description": "The body is wrapped in `price_display_settings` or names a field the section does not have, sends a surface the block does not accept (`invalid_enum`), or sends a `pricing_info.text` longer than 2000 characters (`too_long`). `details` has one entry per rejected field, and each entry's `code` gives the reason.",
                "schema": ERROR,
                "example": error_example("invalid_request", "order_summary.pricing_info.text: must be at most 2000 characters",
                                         [{"field": "order_summary.pricing_info.text", "code": "too_long", "message": "must be at most 2000 characters"}],
                                         "1e6b9d42-3f7a-4c85-b2e0-7a4d8c1f5e93"),
            },
        },
        "example_call": {"path": {"section": "order_item"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def block(name, description):
    return dict(ref(name), description=description)


def toggle(description):
    return block("PriceDisplayScopedToggle", description)


def switch(description):
    return block("PriceDisplayPlainToggle", description)


def surfaces(description):
    return block("PriceDisplayScopes", description)


SCHEMAS = {
    "PriceDisplaySettings": {"type": "object", "properties": {
        "order_item": ref("PriceDisplayOrderItem"),
        "order_summary": ref("PriceDisplayOrderSummary"),
    }},
    "PriceDisplayOrderItem": {"type": "object", "description": "The `order_item` section: how each line item's own price shows.", "properties": {
        "price_including_tax": toggle("Show each line item's price with tax included."),
        "price_including_discount": toggle("Show each line item's price with the discount included."),
        "tax_in_line": toggle("Show the tax on each line item. Accepts the `shopping_cart` and `order_success` surfaces only."),
        "discount_in_line_item": toggle("Show the discount on each line item."),
        "item_total_including_tax": toggle("Show each line item's total with tax included. Accepts the `shopping_cart` and `order_success` surfaces only."),
    }},
    "PriceDisplayOrderSummary": {"type": "object", "description": "The `order_summary` section: the lines of the order summary and what each one includes.", "properties": {
        "order_total_excluding_tax": toggle("Show the order total with tax excluded."),
        "order_total_including_discount": toggle("Show the order total with the discount included."),
        "subtotal": ref("PriceDisplaySubtotal"),
        "discount": ref("PriceDisplayDiscount"),
        "subtotal_tax": switch("Show the subtotal tax line. One `enabled` value covers the shopping cart, checkout and the order success page."),
        "total_tax": switch("Show the total tax line. One `enabled` value covers checkout and the order success page."),
        "order_total": switch("Show the order total line. One `enabled` value covers the shopping cart, checkout and the order success page."),
        "shipping_cost": ref("PriceDisplayShippingCost"),
        "shipping_discount": ref("PriceDisplayShippingDiscount"),
        "handling": ref("PriceDisplayHandling"),
        "payment_surcharge": toggle("Show the payment surcharge in the order summary. Accepts the `checkout` and `order_success` surfaces only."),
        "pricing_info": ref("PriceDisplayPricingInfo"),
    }},
    "PriceDisplayScopes": {"type": "object", "description": "The surfaces a setting applies to. A block accepts only the surfaces its `field_metadata` entry lists in `allowed_scopes`. A write that sends any other key is rejected with `400 invalid_request` and the reason `invalid_enum`.", "properties": {
        "shopping_cart": flag("The shopping cart."),
        "checkout": flag("The checkout page."),
        "order_success": flag("The order success page."),
    }},
    "PriceDisplayScopedToggle": {"type": "object", "description": "A setting with a master switch and optional control per surface.", "properties": {
        "enabled": flag("The master switch. While `customize` is `false`, every surface in `scopes` follows it."),
        "customize": flag("Set each surface in `scopes` yourself instead of following `enabled`."),
        "scopes": surfaces("The surfaces this setting applies to when `customize` is `true`."),
    }},
    "PriceDisplayPlainToggle": {"type": "object", "description": "A setting with only a master switch and no control per surface.", "properties": {
        "enabled": flag("Turn the setting on or off."),
    }},
    "PriceDisplaySubtotal": {"type": "object", "description": "The subtotal line: where it shows, and whether it includes tax and discount.", "properties": {
        "show": surfaces("Show the subtotal line on each surface."),
        "include_tax": toggle("Show the subtotal with tax included."),
        "include_discount": toggle("Show the subtotal with the discount included."),
    }},
    "PriceDisplayDiscount": {"type": "object", "description": "The discount line: where it shows, whether it hides when zero, and whether it includes tax.", "properties": {
        "show": surfaces("Show the discount line on each surface."),
        "hide_if_zero": toggle("Hide the discount line when the discount is zero."),
        "include_tax": toggle("Show the discount with tax included."),
    }},
    "PriceDisplayShippingCost": {"type": "object", "description": "The shipping cost line: where it shows, and whether it includes tax and discount. Accepts the `checkout` and `order_success` surfaces only.", "properties": {
        "show": surfaces("Show the shipping cost line on each surface."),
        "include_tax": toggle("Show the shipping cost with tax included."),
        "include_discount": toggle("Show the shipping cost with the discount included."),
    }},
    "PriceDisplayShippingDiscount": {"type": "object", "description": "The shipping discount line and the shipping tax line. Accepts the `checkout` and `order_success` surfaces only.", "properties": {
        "show": surfaces("Show the shipping discount line on each surface."),
        "include_tax": toggle("Show the shipping discount with tax included."),
        "shipping_tax": switch("Show the shipping tax line. One `enabled` value covers checkout and the order success page."),
    }},
    "PriceDisplayHandling": {"type": "object", "description": "The handling cost, shown apart from shipping, and its tax settings. Accepts the `checkout` and `order_success` surfaces only.", "properties": {
        "show_separately": surfaces("Show the handling cost separately from shipping, on each surface."),
        "include_tax": toggle("Show the handling cost with tax included."),
        "handling_tax": toggle("Show the handling tax in the order summary."),
    }},
    "PriceDisplayPricingInfo": {"type": "object", "description": "A pricing information note shown after the total, and whether the order success page hides the due amount.", "properties": {
        "enabled": flag("Show a custom pricing information note after the total."),
        "text": {"type": "string", "maxLength": 2000, "description": "The note's text. At most 2000 characters: a longer value is rejected with `400 invalid_request` and the reason `too_long`."},
        "customize": flag("Set the surfaces in `scopes` yourself instead of following `enabled`."),
        "scopes": surfaces("The surfaces the note shows on."),
        "do_not_show_due_amount": flag("Hide the due amount on the order success page."),
    }},
    "PriceDisplayGroupMeta": {"type": "object", "description": "One entry per section. Only [Get price display settings](" + GET_PAGE + ") and [Update price display settings](" + UPDATE_PAGE + ") return it.", "properties": {
        "order_item": ref("PriceDisplaySectionMeta"),
        "order_summary": ref("PriceDisplaySectionMeta"),
    }},
    "PriceDisplaySectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for both sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for both sections."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/price_display_settings/order_item`."},
    }},
    "PriceDisplayFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `PriceDisplayFieldMetadataEntry` in place of each setting. A `scopes`, `show` or `show_separately` object gets one `scope_flags` entry. On `/price_display_settings` it is keyed by section; on a section path it holds that section under its own name."},
    "PriceDisplayFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "enum": ["boolean", "string", "scope_flags"], "description": "The kind of value the field takes: `boolean`, `string` or `scope_flags`."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does."},
        "default": {"description": "The field's default value, for a `boolean` or `string` field."},
        "allowed_scopes": {"type": "array", "items": {"type": "string"}, "description": "The surfaces the block accepts, for a `scope_flags` field."},
        "scope_labels": {"type": "object", "additionalProperties": {"type": "string"}, "description": "A label for each surface in `allowed_scopes`."},
        "max_length": {"type": "integer", "description": "The longest value accepted, for a `string` field. Only `order_summary.pricing_info.text` has it, set to `2000`."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The field that was rejected."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field` or `invalid_enum`."},
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": {"type": "string", "description": "An id for this request."},
        }},
    }},
}
