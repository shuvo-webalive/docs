"""The Ecommerce settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Ecommerce settings"
SLUG = "ecommerce-settings"
BASE = "/admin/settings/ecommerce_settings"
ICON = "cart-shopping"

GET_PAGE = "/api-reference/ecommerce-settings/get-ecommerce-settings"
UPDATE_PAGE = "/api-reference/ecommerce-settings/update-ecommerce-settings"

SECTIONS = ["continue_shopping", "product_inventory", "pricing", "product_restriction", "order_filters", "location_settings"]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `continue_shopping`, `product_inventory`, `pricing`, `product_restriction`, `order_filters` or `location_settings`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "order_filters"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field of the six sections, keyed by section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_CONTINUE_SHOPPING = {
    "enable_continue_shopping": True,
    "continue_shopping_target": "specified",
    "continue_shopping_specified_target": "home",
}

SAMPLE_PRODUCT_INVENTORY = {
    "show_out_of_stock_products": False,
    "low_stock_notification": False,
    "out_of_stock_notification": False,
    "hide_on_sale_tag_for_out_of_stock_product": False,
    "order_quantity_over_stock": "do_not_sell",
    "update_stock": "after_shipment",
}

SAMPLE_PRICING = {
    "update_price_range": False,
    "enable_minimum_purchase_amount": True,
    "minimum_purchase_amount": 1,
    "enable_minimum_purchase_amount_in_cart": True,
    "minimum_purchase_amount_in_cart": 2,
    "enable_on_account_purchase": False,
    "assign_credit_limit_per_order": False,
    "credit_limit_per_order": None,
    "enable_payment_terms": True,
    "payment_terms": "NET_30",
    "enable_customer_price_restriction": True,
}

SAMPLE_PRODUCT_RESTRICTION = {"enable_product_restriction_based_on_parent_category": False}

SAMPLE_ORDER_FILTERS = {
    "default_order_status": None,
    "default_payment_status": None,
    "default_shipment_status": "shipped",
}

SAMPLE_LOCATION_SETTINGS = {
    "enable_multi_location": False,
    "locations": [
        {"id": 1, "name": "Main Warehouse", "address": "1 Example Street, Sydney NSW 2000", "is_active": True,
         "is_default": True, "created": "2026-07-16T06:24:24", "updated": "2026-08-25T05:00:56"},
        {"id": 4, "name": "Second Warehouse", "address": "2 Example Street, Sydney NSW 2000", "is_active": True,
         "is_default": False, "created": "2026-07-16T06:58:32", "updated": "2026-08-16T14:19:49"},
    ],
}

SAMPLE_ORDER_FLAGS = [
    {"id": 2, "name": "Partial Shipment", "color": "#4FD9FC", "description": None, "type": "order"},
    {"id": 1, "name": "Payment Failed", "color": "#FF6868", "description": None, "type": "order"},
    {"id": 3, "name": "Payment Pending", "color": "#FFA959", "description": None, "type": "order"},
]

SAMPLE_GROUP_META = dict(
    {section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section} for section in SECTIONS},
    order_flags={"kind": "collection", "writable": False, "href": "/api/v4/admin/order_flags"},
)
SAMPLE_GROUP_META["location_settings"]["locations_href"] = "/api/v4/admin/inventory_locations"

SAMPLE_ECOMMERCE_SETTINGS = {
    "ecommerce_settings": {
        "continue_shopping": SAMPLE_CONTINUE_SHOPPING,
        "product_inventory": SAMPLE_PRODUCT_INVENTORY,
        "pricing": SAMPLE_PRICING,
        "product_restriction": SAMPLE_PRODUCT_RESTRICTION,
        "order_filters": SAMPLE_ORDER_FILTERS,
        "location_settings": SAMPLE_LOCATION_SETTINGS,
        "order_flags": SAMPLE_ORDER_FLAGS,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_ECOMMERCE_SETTINGS = copy.deepcopy(SAMPLE_ECOMMERCE_SETTINGS)
PATCHED_ECOMMERCE_SETTINGS["ecommerce_settings"]["continue_shopping"]["continue_shopping_target"] = "previous"
PATCHED_ECOMMERCE_SETTINGS["ecommerce_settings"]["order_filters"]["default_payment_status"] = "unpaid"

PATCHED_ORDER_FILTERS = dict(SAMPLE_ORDER_FILTERS, default_shipment_status="unshipped")


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

ECOMMERCE_SETTINGS_RESPONSE = {"type": "object", "properties": {
    "ecommerce_settings": ref("EcommerceSettings"),
    "group_meta": ref("EcommerceSettingsGroupMeta"),
}}

SECTION_RECORDS = {
    "continue_shopping": ref("ContinueShoppingSettings"),
    "product_inventory": ref("ProductInventorySettings"),
    "pricing": ref("PricingSettings"),
    "product_restriction": ref("ProductRestrictionSettings"),
    "order_filters": ref("OrderFilterSettings"),
    "location_settings": ref("LocationSettings"),
}

SECTION_INPUTS = dict(SECTION_RECORDS, location_settings=ref("LocationSettingsInput"))

ENDPOINTS = [
    {
        "key": "get_ecommerce_settings",
        "slug": "get-ecommerce-settings",
        "title": "Get ecommerce settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all six settings sections and the store's order flags, with a `group_meta` entry for each.",
        "description": "Returns every ecommerce setting under `ecommerce_settings`, with the six sections in full and the store's order flags as a list under `order_flags`. Beside it, `group_meta` gives each key's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section. The response has an `ETag` header.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All six sections, the order flags and `group_meta`.",
                "schema": {"type": "object", "properties": dict(ECOMMERCE_SETTINGS_RESPONSE["properties"], field_metadata=dict(
                    ref("EcommerceSettingsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section, with no entry for `order_flags`.",
                ))},
                "example": SAMPLE_ECOMMERCE_SETTINGS,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_ecommerce_settings",
        "slug": "update-ecommerce-settings",
        "title": "Update ecommerce settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change inside `ecommerce_settings`, grouped by section name; one body can change several sections. Only the fields you send change: other fields, and sections you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get ecommerce settings](" + GET_PAGE + ") does. A body not wrapped in `ecommerce_settings` is rejected with `400`, and so is a section name the store does not have.",
        "body": {
            "schema": {"type": "object", "required": ["ecommerce_settings"], "properties": {
                "ecommerce_settings": dict(ref("EcommerceSettingsInput"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"ecommerce_settings": {
                "continue_shopping": {"continue_shopping_target": "previous"},
                "order_filters": {"default_payment_status": "unpaid"},
            }},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": ECOMMERCE_SETTINGS_RESPONSE, "example": PATCHED_ECOMMERCE_SETTINGS},
            "400": {
                "description": "The body is not wrapped in `ecommerce_settings` (`request body must be wrapped in a 'ecommerce_settings' object`), or names a section the store does not have (`<name>: not a recognized section`, with `details[0].code` set to `unknown_field`).",
                "schema": ERROR,
                "example": error_example("invalid_request", "not_a_section: not a recognized section",
                                         [{"field": "not_a_section", "code": "unknown_field", "message": "not a recognized section"}],
                                         "43172b74-5301-49b0-bd09-b766034162f3"),
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_ecommerce_settings",
        "slug": "get-ecommerce-settings-headers",
        "title": "Get ecommerce settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the ecommerce settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and the same `ETag` that [Get ecommerce settings](" + GET_PAGE + ") returns. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_ecommerce_settings_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `pricing`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `ecommerce_settings`, and without `group_meta`. The values are the same ones [Get ecommerce settings](" + GET_PAGE + ") returns for that section, and the response has an `ETag` header. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section, and `order_flags`, return `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": dict(
                    SECTION_RECORDS,
                    field_metadata=dict(ref("EcommerceSettingsFieldMetadata"), description="Only when you send `field_metadata=true`. Keyed by field name."),
                )},
                "example": {"order_filters": SAMPLE_ORDER_FILTERS},
            },
            "404": {
                "description": "No section has that name. `order_flags` returns this too, because it is not a section.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown settings path: ecommerce_settings/order_flags", [],
                                         "085b1f0c-82ee-4ffc-a5da-c31269ddf632"),
            },
        },
        "example_call": {"path": {"section": "order_filters"}},
    },
    {
        "key": "patch_ecommerce_settings_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change wrapped in the section's own name, such as `order_filters`, or send them unwrapped. A body wrapped in `ecommerce_settings` is rejected with `400`, and so is a field the section does not have, even beside fields it does have. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under its own key and without `group_meta`.",
        "parameters": [SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the name of the section in the path, or send the fields unwrapped. The `ecommerce_settings` wrapper is not accepted here.", "properties": SECTION_INPUTS},
            "example": {"order_filters": {"default_shipment_status": "unshipped"}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": {"type": "object", "properties": SECTION_RECORDS},
                    "example": {"order_filters": PATCHED_ORDER_FILTERS}},
            "400": {
                "description": "The body is wrapped in `ecommerce_settings` (`<section>.ecommerce_settings: not a recognized field`), or names a field the section does not have (`<section>.<field>: not a recognized field`). A value is also rejected when it is not one of an `enum` field's `allowed_values` (`invalid_enum`), is not a boolean for a boolean field (`invalid_boolean`, `must be a boolean (true/false or 0/1)`), or is a `continue_shopping_specified_target` that names no page (`invalid_reference`, `not a known page slug`). While `enable_minimum_purchase_amount` is on, a `minimum_purchase_amount` of `0` is rejected with `must be a number greater than 0 when enable_minimum_purchase_amount is on`. After this `400`, the next read on the same client returns the wrong section, so create a new client first.",
                "schema": ERROR,
                "example": error_example("invalid_request", "default_order_status: must be one of [all, paused, in_progress, completed, reopened] (or empty to clear)",
                                         [{"field": "default_order_status", "code": "invalid_enum", "message": "must be one of [all, paused, in_progress, completed, reopened] (or empty to clear)", "value": " completed"}],
                                         "182b77d5-aa71-447b-9e18-c2da1ea8d936"),
            },
        },
        "example_call": {"path": {"section": "order_filters"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def amount(description, nullable=False):
    return {"type": ["number", "null"] if nullable else "number", "description": description}


def choice(values, description, nullable=False):
    if nullable:
        return {"type": ["string", "null"], "enum": values + [None], "description": description}
    return {"type": "string", "enum": values, "description": description}


SCHEMAS = {
    "EcommerceSettings": {"type": "object", "properties": dict(
        SECTION_RECORDS,
        order_flags={"type": "array", "items": ref("EcommerceSettingsOrderFlag"), "description": "The store's order flags. Read-only here: manage them through `/api/v4/admin/order_flags`."},
    )},
    "EcommerceSettingsInput": {"type": "object", "description": "The fields to change, grouped by section. `order_flags` cannot be written here.", "properties": SECTION_INPUTS},
    "ContinueShoppingSettings": {"type": "object", "description": "The `continue_shopping` section: where the continue shopping link leads.", "properties": {
        "enable_continue_shopping": flag("Turn continue shopping on or off."),
        "continue_shopping_target": choice(["home", "previous", "specified"], "Where continue shopping leads: `home`, `previous` or `specified`. With `specified`, `continue_shopping_specified_target` names the page."),
        "continue_shopping_specified_target": {"type": "string", "description": "The slug of the page to link to. Required when `continue_shopping_target` is `specified`. `field_metadata` lists every page slug in your store under `options`, and a slug that names no page is rejected with `400 invalid_reference` and the message `not a known page slug`."},
    }},
    "ProductInventorySettings": {"type": "object", "description": "The `product_inventory` section: out-of-stock handling and when a sale reduces stock.", "properties": {
        "show_out_of_stock_products": flag("Display out of stock products."),
        "low_stock_notification": flag("Get a low stock notification by email."),
        "out_of_stock_notification": flag("Get an out of stock notification by email."),
        "hide_on_sale_tag_for_out_of_stock_product": flag("Do not display the \"On Sale\" tag on a sold out product."),
        "order_quantity_over_stock": choice(["add_available", "sell_away", "allow_admin_only_to_add_out_of_stock_products", "do_not_sell"],
                                            "The stock rule when an order quantity is more than the stock: `add_available`, `sell_away`, `allow_admin_only_to_add_out_of_stock_products` or `do_not_sell`."),
        "update_stock": choice(["after_order", "after_payment", "after_shipment"], "When stock is updated: `after_order`, `after_payment` or `after_shipment`."),
    }},
    "PricingSettings": {"type": "object", "description": "The `pricing` section: minimum purchase amounts, on account purchase, credit limit and payment terms.", "properties": {
        "update_price_range": flag("Adjust the price range for the product."),
        "enable_minimum_purchase_amount": flag("Turn on the minimum purchase amount."),
        "minimum_purchase_amount": amount("The minimum purchase amount. Depends on `enable_minimum_purchase_amount`, and is required and greater than `0` while it is on."),
        "enable_minimum_purchase_amount_in_cart": flag("Turn on the minimum purchase amount in cart details."),
        "minimum_purchase_amount_in_cart": amount("The minimum purchase amount in cart details. Depends on `enable_minimum_purchase_amount_in_cart`, and is required and greater than `0` while it is on."),
        "enable_on_account_purchase": flag("Turn on on account purchase."),
        "assign_credit_limit_per_order": flag("Set a credit limit for the account. Depends on `enable_on_account_purchase`."),
        "credit_limit_per_order": amount("The credit limit. Depends on `assign_credit_limit_per_order`, and is required while it is on. `0` is allowed and grants no credit. Can be `null`.", nullable=True),
        "enable_payment_terms": flag("Turn on payment terms."),
        "payment_terms": choice(["NET_30", "NET_60", "NET_90"], "The net payment term: `NET_30`, `NET_60` or `NET_90`, written and returned as that string. Depends on `enable_payment_terms`. Can be `null`.", nullable=True),
        "enable_customer_price_restriction": flag("Allow customer-specific price restriction."),
    }},
    "ProductRestrictionSettings": {"type": "object", "description": "The `product_restriction` section: one switch for product restriction based on the parent category.", "properties": {
        "enable_product_restriction_based_on_parent_category": flag("Allow product restriction based on the parent category."),
    }},
    "OrderFilterSettings": {"type": "object", "description": "The `order_filters` section: the status each admin order list opens on. A field is `null` when no default is set.", "properties": {
        "default_order_status": choice(["all", "paused", "in_progress", "completed", "reopened"], "The default order status: `all`, `paused`, `in_progress`, `completed` or `reopened`, or `null` when unset.", nullable=True),
        "default_payment_status": choice(["all", "paid", "unpaid", "partially_paid"], "The default payment status: `all`, `paid`, `unpaid` or `partially_paid`, or `null` when unset.", nullable=True),
        "default_shipment_status": choice(["all", "unshipped", "shipped", "returned", "partial"], "The default shipment status: `all`, `unshipped`, `shipped`, `returned` or `partial`, or `null` when unset.", nullable=True),
    }},
    "LocationSettings": {"type": "object", "description": "The `location_settings` section. Only `enable_multi_location` can be written.", "properties": {
        "enable_multi_location": flag("Turn on multiple stock locations."),
        "locations": {"type": "array", "readOnly": True, "items": ref("EcommerceSettingsLocation"),
                      "description": "A read-only list of your stock locations. Manage them through `/api/v4/admin/inventory_locations`. A body that sends `locations` is rejected with `400 invalid_request` and the message `no recognized ecommerce_settings fields in body`."},
    }},
    "LocationSettingsInput": {"type": "object", "description": "The `location_settings` fields you can write. `locations` is read-only.", "properties": {
        "enable_multi_location": flag("Turn on multiple stock locations."),
    }},
    "EcommerceSettingsLocation": {"type": "object", "description": "One stock location, as `location_settings.locations` lists it.", "properties": {
        "id": {"type": "integer", "description": "The stock location's `id`, which `/api/v4/admin/inventory_locations/{inventory_location_id}` takes as `inventory_location_id`."},
        "name": {"type": "string", "description": "The location's name."},
        "address": {"type": "string", "description": "The location's address."},
        "is_active": {"type": "boolean", "description": "Whether the location is active."},
        "is_default": {"type": "boolean", "description": "`true` on the store's default location."},
        "created": {"type": "string", "description": "When the location was created, such as `2026-07-16T06:24:24`."},
        "updated": {"type": "string", "description": "When the location was last changed."},
    }},
    "EcommerceSettingsOrderFlag": {"type": "object", "description": "One order flag, as `order_flags` lists it.", "properties": {
        "id": {"type": "integer", "description": "The order flag's `id`, which `/api/v4/admin/order_flags/{order_flag_id}` takes as `order_flag_id`."},
        "name": {"type": "string", "description": "The flag's name."},
        "color": {"type": "string", "description": "The flag's colour as a hex code, such as `#FF6868`."},
        "description": {"type": ["string", "null"], "description": "The flag's description, or `null`."},
        "type": {"type": "string", "description": "The flag's type, such as `order`."},
    }},
    "EcommerceSettingsGroupMeta": {"type": "object", "description": "One entry per key under `ecommerce_settings`. Only [Get ecommerce settings](" + GET_PAGE + ") and [Update ecommerce settings](" + UPDATE_PAGE + ") return it.", "properties": dict(
        {section: ref("EcommerceSettingsSectionMeta") for section in SECTIONS},
        order_flags=ref("EcommerceSettingsSectionMeta"),
    )},
    "EcommerceSettingsSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "`setting` for the six sections, `collection` for `order_flags`."},
        "writable": {"type": "boolean", "description": "`true` for the six sections, `false` for `order_flags`."},
        "href": {"type": "string", "description": "The key's own path, such as `/api/v4/admin/settings/ecommerce_settings/pricing`. For `order_flags` it is `/api/v4/admin/order_flags`."},
        "locations_href": {"type": "string", "description": "Only on `location_settings`: `/api/v4/admin/inventory_locations`, where you manage the stock locations."},
    }},
    "EcommerceSettingsFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Describes each field with an `EcommerceSettingsFieldMetadataEntry`. On `/ecommerce_settings` it is keyed by section and then by field name; on a section it is keyed by field name."},
    "EcommerceSettingsFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes: `boolean`, `enum`, `decimal`, `reference` or `collection`."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "default": {"description": "The field's default value, when it has one."},
        "allowed_values": {"type": "array", "items": {"type": "string"}, "description": "The values an `enum` field accepts."},
        "nullable": {"type": "boolean", "description": "`true` when the field can be empty."},
        "depends_on": {"type": "string", "description": "The field this one depends on, such as `enable_minimum_purchase_amount`."},
        "description": {"type": "string", "description": "A note about the field's values, on some fields, such as `Empty = unset.`"},
        "references": {"type": "string", "description": "What a `reference` field points to: `page` for `continue_shopping_specified_target`."},
        "options": {"type": "array", "items": {"type": "string"}, "description": "For `continue_shopping_specified_target`, every page slug in your store."},
        "writable": {"type": "boolean", "description": "`false` on `locations`, which you cannot write."},
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
            "request_id": {"type": "string", "description": "The identifier of this request."},
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Read and change your store's continue shopping, stock, pricing, product restriction, order list and stock location settings."
INTRO = "The Ecommerce settings API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/ecommerce_settings`."
WARNING = (
    "**After a section write is rejected with `400`, the next request on the same client returns the wrong section.**\n"
    "  For example, after `PATCH /ecommerce_settings/pricing` returns `400`, a\n"
    "  `GET /ecommerce_settings/continue_shopping` on the same client returns `200` with the `pricing`\n"
    "  section in its body. Create a new client after such a `400` before you make another call. A\n"
    "  successful write does not cause this."
)
NOTES = [
    "**Six sections hold the settings, and `order_flags` is not one of them.** The sections are\n"
    "  `continue_shopping`, `product_inventory`, `pricing`, `product_restriction`, `order_filters` and\n"
    "  `location_settings`. [Get ecommerce settings](" + GET_PAGE + ") also lists the store's order flags\n"
    "  under `order_flags`, but you cannot read them as a section (`404`) or write them here: manage them\n"
    "  through `/api/v4/admin/order_flags`. In the same way, `location_settings.locations` is a read-only\n"
    "  list of your stock locations, managed through `/api/v4/admin/inventory_locations`.",
    "**The wrapper a write needs depends on the path.** On `/ecommerce_settings`, wrap the fields in\n"
    "  `ecommerce_settings` and then in the section name: a bare section or a loose field is rejected\n"
    "  with `400` and the message `request body must be wrapped in a 'ecommerce_settings' object`. On\n"
    "  `/ecommerce_settings/{section}`, wrap the fields in the section's own name or send them\n"
    "  unwrapped: the `ecommerce_settings` wrapper is rejected there with `400`.",
    "**`PATCH` changes only the fields you send, and checks the values you send.** A value outside an\n"
    "  `enum` field's `allowed_values`, a non-boolean for a boolean field, and a\n"
    "  `continue_shopping_specified_target` that is not a page slug in your store are each rejected with\n"
    "  `400`. On `/ecommerce_settings/{section}`, a field the section does not have is rejected too, even\n"
    "  beside fields it does have. `PUT`, `POST` and `DELETE` are rejected on both paths with\n"
    "  `405 method_not_allowed`.",
    "**Five `pricing` fields depend on a switch.** `minimum_purchase_amount` depends on\n"
    "  `enable_minimum_purchase_amount`, `minimum_purchase_amount_in_cart` on\n"
    "  `enable_minimum_purchase_amount_in_cart`, `assign_credit_limit_per_order` on\n"
    "  `enable_on_account_purchase`, `credit_limit_per_order` on `assign_credit_limit_per_order`, and\n"
    "  `payment_terms` on `enable_payment_terms`. While `enable_minimum_purchase_amount` is on,\n"
    "  `minimum_purchase_amount: 0` is rejected with `400` and the message\n"
    "  `must be a number greater than 0 when enable_minimum_purchase_amount is on`. Turning\n"
    "  `enable_minimum_purchase_amount` off does not clear `minimum_purchase_amount`, and you can still\n"
    "  write `minimum_purchase_amount` while the switch is off.",
    "**Add `field_metadata=true` to a read to get a description of every field.** Each entry gives the\n"
    "  field's `type` and `ui_label`, and where they apply its `default`, `allowed_values`, `nullable`,\n"
    "  `depends_on` and `description`. For `continue_shopping_specified_target`, `options` lists every\n"
    "  page slug in your store. On `/ecommerce_settings` the block is keyed by section; on a section it is\n"
    "  keyed by field name.",
]
