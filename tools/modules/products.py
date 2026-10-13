"""The Products endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Products"
SLUG = "products"
BASE = "/admin/products"
ICON = "box"

RETRIEVE_PAGE = "/api-reference/products/retrieve-a-product"
UPDATE_PAGE = "/api-reference/products/update-a-product"
STOCK_PAGE = "/api-reference/products/retrieve-a-products-stock"
SET_STOCK_PAGE = "/api-reference/products/set-a-products-stock"
UNASSIGN_PAGE = "/api-reference/products/unassign-an-inventory-location-from-a-product"
LOCATIONS_PAGE = "/api-reference/inventory-locations/list-inventory-locations"
LOCATION_STOCK_PAGE = "/api-reference/inventory-locations/list-stock-at-an-inventory-location"
DELETE_LOCATION_PAGE = "/api-reference/inventory-locations/delete-an-inventory-location"
CATEGORIES_PAGE = "/api-reference/categories/list-categories"

OVERVIEW_DESCRIPTION = "Read and update a product, read and set its stock at each inventory location, and unassign a location from it."
INTRO = "The Products API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/products`."

WARNING = (
    "**Setting a product's stock unassigns every location you leave out, even one that still holds stock.**\n"
    "  [Set a product's stock](" + SET_STOCK_PAGE + ") replaces the product's whole set of locations with the\n"
    "  rows you send in `locations`. Read the rows first with [Retrieve a product's stock](" + STOCK_PAGE + "),\n"
    "  send every row you want to keep, and change only the values you mean to change."
)

NOTES = [
    "**Send product fields at the top level of the body, not inside `product`.** Responses return the\n"
    "  product inside `product`, but a body wrapped in `product` is rejected with `400` and the message\n"
    "  `product: is not a recognised product field`. Send the stock body's `note` and `locations` at the\n"
    "  top level too.",
    "**An update changes only the fields you send, at every level.** `{\"advanced\": {\"advance_information\": {\"mpn\": \"MPN-0001\"}}}`\n"
    "  changes `mpn` and keeps the other eight fields of `advance_information`. A body that changes nothing\n"
    "  returns `200` and leaves `version` and the `ETag` header as they were.",
    "**Some fields you read cannot be written.** A changed `id`, `created_at`, `created_on`, `custom_class`,\n"
    "  `sold_out`, `sold_out_label`, `length`, `width`, `height`, `weight`, `featured`, `new`, `model`, `is_draft`,\n"
    "  `has_variations`, `urls` or `created_by` is rejected with `400` and the reason `read_only_field`; the value\n"
    "  you read is accepted. `status` and `reviews` are rejected with the reason `unknown_field`, so remove them\n"
    "  before you send back a product you read. Write the dimensions in `product_properties`, and `mpn`, `upc`,\n"
    "  `barcode` and `hs_code` in `advanced.advance_information`. `field_metadata` lists these fields as writable\n"
    "  at the top level, but they are rejected there.",
    "**Setting stock changes the product too.** `available_stock` is the sum of the rows' `stock`, and\n"
    "  `product_pricing_and_stock.low_level_stock` takes the `low_stock_level` of the product's default\n"
    "  location. The product's `version`, `updated_at` and `last_updated_by` change when the stock changes.\n"
    "  `product_pricing_and_stock.locations` on [Retrieve a product](" + RETRIEVE_PAGE + ") holds the same rows as\n"
    "  [Retrieve a product's stock](" + STOCK_PAGE + ").",
    "**The first location you assign to a product is missing from the response.** On a product with no\n"
    "  location yet, [Set a product's stock](" + SET_STOCK_PAGE + ") returns `locations: []` and stores the row.\n"
    "  Call [Retrieve a product's stock](" + STOCK_PAGE + ") to see it. A product that already has a location\n"
    "  returns its rows at once.",
    "**Find a `product_id` in an inventory location's stock.** None of these five endpoints lists\n"
    "  products. [List stock at an inventory location](" + LOCATION_STOCK_PAGE + ") returns the\n"
    "  `id` of each product the location holds, as `items[].product.id`.",
]


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def nullable(kind, description=None):
    schema = {"type": [kind, "null"]}
    if description:
        schema["description"] = description
    return schema


def typed(kind, description=None):
    schema = {"type": kind}
    if description:
        schema["description"] = description
    return schema


def array_of(name, description=None):
    schema = {"type": "array", "items": ref(name)}
    if description:
        schema["description"] = description
    return schema


PRODUCT_ID = {
    "name": "product_id",
    "in": "path",
    "required": True,
    "description": "The product's `id`. [List stock at an inventory location](" + LOCATION_STOCK_PAGE + ") returns it as `items[].product.id`.",
    "schema": {"type": "integer", "example": 101},
}

INVENTORY_LOCATION_ID = {
    "name": "inventory_location_id",
    "in": "path",
    "required": True,
    "description": "The inventory location's `id`: the `warehouse` of one of the rows [Retrieve a product's stock](" + STOCK_PAGE + ") returns.",
    "schema": {"type": "integer", "example": 19},
}

FIELD_METADATA = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` or `1` to add `field_metadata` beside `product`, describing the product's fields. `false` or `0` leaves it out. Any other value is rejected with `400`. The product and the `ETag` header are the same either way.",
    "schema": {"type": "boolean", "example": True},
}

REQUEST_ID = "4f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"


def error(code, message, details):
    return {"error": {"code": code, "message": message, "details": details, "request_id": REQUEST_ID}}


UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): limit", [{"field": "limit", "code": "unknown_parameter", "message": None}])
HAS_STOCK = error("conflict", "Product 101 still holds 25 units at this location. Set its stock here to 0 first.", [{"field": "location_id", "code": "has_stock", "message": "25 units held", "value": 4}])

ERROR_REF = ref("ProductError")
PRODUCT_RESPONSE = {"type": "object", "properties": {"product": ref("Product")}}
STOCK_REF = ref("ProductStock")

LOCATION_ROWS = [
    {"warehouse": 1, "warehouse_name": "Sydney Warehouse", "stock": 10, "low_stock_level": 2, "is_default": True},
    {"warehouse": 4, "warehouse_name": "Sydney Store Room", "stock": 25, "low_stock_level": 5, "is_default": False},
]

SAMPLE_PRODUCT = {
    "id": 101,
    "name": "Cotton T-Shirt",
    "sku": "TSHIRT-001",
    "heading": "Cotton T-Shirt",
    "invoice_note": "",
    "available": True,
    "password_protected": False,
    "password": "",
    "base_price": 25.0,
    "cost_price": 12.0,
    "is_on_sale": False,
    "sale_price": 0.0,
    "version": 7,
    "product_pricing_and_stock": {
        "track_inventory": True,
        "available_stock": 35,
        "low_level_stock": 2,
        "warehouses": [{"warehouse": "1", "stock": 10}, {"warehouse": "4", "stock": 25}],
        "is_multi_location_enabled": True,
        "locations": LOCATION_ROWS,
    },
    "advanced": {"advance_information": {"mpn": "", "barcode": "", "hs_code": ""}},
    "product_variation": {},
    "has_variations": False,
}

UPDATED_PRODUCT = copy.deepcopy(SAMPLE_PRODUCT)
UPDATED_PRODUCT["invoice_note"] = "Ships in 2 business days"
UPDATED_PRODUCT["advanced"]["advance_information"]["mpn"] = "MPN-0001"
UPDATED_PRODUCT["version"] = 8

SAMPLE_STOCK = {
    "status": "success",
    "product_id": 101,
    "multi_location_enabled": True,
    "track_inventory": True,
    "available_stock": 35,
    "locations": LOCATION_ROWS,
}

STOCK_BODY = {
    "note": "Restock",
    "locations": [
        {"warehouse": 1, "stock": 10, "low_stock_level": 2, "is_default": True},
        {"warehouse": 4, "stock": 30, "low_stock_level": 5, "is_default": False},
    ],
}

SET_STOCK = dict(SAMPLE_STOCK, available_stock=40, locations=[LOCATION_ROWS[0], dict(LOCATION_ROWS[1], stock=30)])

ENDPOINTS = [
    {
        "key": "get_product",
        "slug": "retrieve-a-product",
        "title": "Retrieve a product",
        "method": "GET",
        "path": BASE + "/{product_id}",
        "summary": "Returns the product whose `id` you pass as `product_id`, with all 69 of its fields.",
        "description": "Returns one product under the `product` key, with its prices, availability, stock, media, tags, reviews and variations. Send `field_metadata=true` to also get a description of each field. `field_metadata` is the only query parameter accepted: any other, such as `limit` or `fields`, is rejected with `400`. `password` reads `***` when the product has a password and `\"\"` when it has none.",
        "parameters": [PRODUCT_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The product. With `field_metadata=true`, a `field_metadata` key is added after it. The response has an `ETag` header and `Cache-Control: no-cache, no-store`. The example shows a selection of the fields.",
                "schema": {"type": "object", "properties": {"product": ref("Product"), "field_metadata": ref("ProductFieldMetadata")}},
                "example": {"product": SAMPLE_PRODUCT},
            },
            "400": {
                "description": "You sent a query parameter other than `field_metadata`: the message is `unknown query parameter(s): <name>` and `details[0].code` is `unknown_parameter`. Or `field_metadata` is not `true`, `false`, `1` or `0`: the message is `field_metadata must be true/false or 0/1` and `details[0].code` is `invalid_boolean`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
            "404": {"description": "No product has that `product_id`. The message is `Product not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "update_product",
        "slug": "update-a-product",
        "title": "Update a product",
        "method": "PUT",
        "path": BASE + "/{product_id}",
        "summary": "Changes the product fields you send, keeps every other field, and returns the product.",
        "description": "Send the fields to change at the top level of the body, not inside `product`. The update merges at every level: a field you leave out keeps its value, inside nested blocks too. Write the dimensions in `product_properties`, and `mpn`, `upc`, `barcode` and `hs_code` in `advanced.advance_information`. You can send back a product you read once you remove `status` and `reviews`.",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductInput"), "example": {"invoice_note": "Ships in 2 business days", "advanced": {"advance_information": {"mpn": "MPN-0001"}}}},
        "responses": {
            "200": {
                "description": "The product after the update, with an `ETag` header. When something changed, `version`, `updated_at`, `last_updated_on` and `last_updated_by` change too. The example shows a selection of the fields.",
                "schema": PRODUCT_RESPONSE,
                "example": {"product": UPDATED_PRODUCT},
            },
            "400": {
                "description": "The body is wrapped in `product` (message `product: is not a recognised product field`), or it has `status`, `reviews`, or a top-level `mpn`, `upc`, `barcode` or `hs_code` (reason `unknown_field`). Or it changes a read-only field such as `id`, `sold_out`, `model` or the top-level `weight` (reason `read_only_field`). Or a field that takes fixed values has another value (reason `invalid_enum`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "get_product_stock",
        "slug": "retrieve-a-products-stock",
        "title": "Retrieve a product's stock",
        "method": "GET",
        "path": BASE + "/{product_id}/stock",
        "summary": "Returns the product's stock at each inventory location it is assigned to, and the total.",
        "description": "Returns one row in `locations` for each inventory location the product is assigned to, with the location's `id` as `warehouse`, its name as `warehouse_name`, the product's `stock` there and the `low_stock_level`, and whether it is the product's default. `available_stock` is the sum of the rows' `stock`, and exactly one row has `is_default` set to `true`. A product with no location returns `multi_location_enabled: false` and `locations: []`, and a product with variations also returns `variations`. Query parameters are ignored.",
        "parameters": [PRODUCT_ID],
        "responses": {
            "200": {
                "description": "The product's stock. `status` is always `success`. The response has no `ETag` header.",
                "schema": STOCK_REF,
                "example": SAMPLE_STOCK,
            },
            "404": {"description": "No product has that `product_id`. The message is `Product not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "update_product_stock",
        "slug": "set-a-products-stock",
        "title": "Set a product's stock",
        "method": "PUT",
        "path": BASE + "/{product_id}/stock",
        "summary": "Sets the product's stock at each location you send and unassigns every location you leave out.",
        "description": "Send `locations` with one row for every location the product keeps; a location you leave out is unassigned, even while it holds stock. Each row takes the location's `id` as `warehouse`, the units as `stock`, and optionally `low_stock_level` and `is_default`. When no row has `is_default: true`, the first row you send becomes the product's default. The rows [Retrieve a product's stock](" + STOCK_PAGE + ") returns can be sent back as they are: `warehouse_name` and other extra keys are ignored.",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductStockInput"), "example": STOCK_BODY},
        "responses": {
            "200": {
                "description": "The product's stock after the write, with the same fields as [Retrieve a product's stock](" + STOCK_PAGE + ") and no `ETag` header. Rows can come back in a different order from the one you sent. On a product that had no location, `locations` is `[]` although the rows are stored: read the stock again to see them.",
                "schema": STOCK_REF,
                "example": SET_STOCK,
            },
            "400": {
                "description": "`locations` is missing or empty (message `locations is required`), a row has a negative `stock` (message `stock can not be a negative number`), or a row has no `warehouse` (message `invalid inventory location: null`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "delete_product_stock_location",
        "slug": "unassign-an-inventory-location-from-a-product",
        "title": "Unassign an inventory location from a product",
        "method": "DELETE",
        "path": BASE + "/{product_id}/stock/locations/{inventory_location_id}",
        "summary": "Unassigns an inventory location that holds `0` units of the product and is not its default.",
        "description": "Removes the location from the product's stock and returns `204` with an empty body. The location must hold `0` units of the product and must not be the product's default, or the call is rejected with `409`: first set its stock to `0`, or make another row the default, with [Set a product's stock](" + SET_STOCK_PAGE + "). Afterwards [List stock at an inventory location](" + LOCATION_STOCK_PAGE + ") no longer lists the product there. Once the location is unassigned from every product, you can delete it with [Delete an inventory location](" + DELETE_LOCATION_PAGE + ").",
        "parameters": [PRODUCT_ID, INVENTORY_LOCATION_ID],
        "responses": {
            "204": {"description": "The location is unassigned from the product. The body is empty, and the `Content-Type` header is `text/html`."},
            "404": {"description": "The location is not assigned to the product, for example because you already unassigned it. The message is `Inventory location <inventory_location_id> is not assigned to product <product_id>.`", "schema": ERROR_REF},
            "409": {
                "description": "The location still holds units of the product: the message is `Product <product_id> still holds <n> units at this location. Set its stock here to 0 first.` and `details[0].code` is `has_stock`. Or the location is the product's default: the message is `This is product <product_id>'s default location. Make another of its locations the default first.` and `details[0].code` is `is_default`.",
                "schema": ERROR_REF,
                "example": HAS_STOCK,
            },
        },
        "example_call": {"path": {"product_id": 101, "inventory_location_id": 19}},
    },
]

READ_ONLY = "Read-only: a changed value is rejected with `400` and the reason `read_only_field`."
DIMENSION = "Read-only here: write it in `product_properties`. A changed value is rejected with `400` and the reason `read_only_field`."
STAMP = "Changes when the product changes. A value you send is ignored."
ADVANCED_CODE = "Write it here: at the top level of the product it is rejected with `400` and the reason `unknown_field`."

SCHEMAS = {
    "Product": {"type": "object", "description": "One product: 69 fields, the same set on every product.", "properties": {
        "id": typed("integer", "The product's `id`. Pass it as `product_id` in a path. " + READ_ONLY),
        "name": typed("string"),
        "sku": typed("string"),
        "status": typed("string", "Read-only: sending it is rejected with `400` and the reason `unknown_field`."),
        "urls": dict(ref("ProductUrls"), description=READ_ONLY),
        "heading": typed("string"),
        "parents": array_of("ProductParent", "The categories the product is filed under. In a write, send their ids as a list of numbers."),
        "created_by": dict(ref("ProductNamedReference"), description="Who created the product. " + READ_ONLY),
        "created_at": typed("string", READ_ONLY),
        "updated_at": typed("string", STAMP),
        "transaction_no": nullable("string"),
        "product_type": typed("string"),
        "custom_type": typed("string"),
        "invoice_note": typed("string"),
        "available": typed("boolean"),
        "product_page": dict(ref("ProductNamedReference"), description="The product's page as `id` and `name`. Some products return `{}` instead."),
        "product_layout": {"description": "`{}` on every product read."},
        "custom_class": typed("string", READ_ONLY),
        "available_on_date_range": typed("boolean"),
        "available_from_date": typed("string"),
        "available_to_date": typed("string"),
        "available_for": typed("string", "Who can buy the product. `selected` limits it to the customers and groups in `selected_customers`."),
        "selected_customers": {"description": "The customers and customer groups the product is available to, as an object with `customers` and `groups`, or `[]` when the product names none.", "anyOf": [ref("ProductSelectedCustomers"), {"type": "array", "maxItems": 0}]},
        "restrict_for_selected_customers": typed("array"),
        "password_protected": typed("boolean"),
        "password": typed("string", "`***` when the product has a password, `\"\"` when it has none. Sending back `***` keeps the stored password."),
        "available_on_weekdays": ref("ProductAvailableOnWeekdays"),
        "base_price": typed("number"),
        "cost_price": typed("number"),
        "compare_at_price": nullable("number"),
        "is_on_sale": typed("boolean"),
        "sale_price": typed("number"),
        "sold_out": typed("boolean", READ_ONLY),
        "length": typed("number", DIMENSION),
        "width": typed("number", DIMENSION),
        "height": typed("number", DIMENSION),
        "weight": typed("number", DIMENSION),
        "sold_out_label": typed("string", READ_ONLY),
        "is_featured": typed("boolean"),
        "featured_label": typed("string"),
        "is_new": typed("boolean"),
        "featured": typed("boolean", READ_ONLY),
        "new": typed("boolean", READ_ONLY),
        "model": typed("string", READ_ONLY),
        "product_properties": ref("ProductProperties"),
        "version": typed("integer", "Changes when the product changes, including when its stock changes. A write that changes nothing keeps it. A value you send is ignored."),
        "created_on": typed("string", READ_ONLY),
        "last_updated_on": typed("string", STAMP),
        "last_updated_by": {"anyOf": [ref("ProductNamedReference"), {"type": "null"}], "description": "Who last changed the product, or `null`. " + STAMP},
        "schedule_type": typed("string"),
        "custom_schedule_option": typed("string"),
        "tax_settings": ref("ProductTaxSettings"),
        "variation_price_display": ref("ProductVariationPriceDisplay"),
        "administrative_status": typed("boolean"),
        "is_draft": typed("boolean", READ_ONLY),
        "product_summary": typed("string"),
        "product_description": typed("string"),
        "product_pricing_and_stock": ref("ProductPricingAndStock"),
        "image_and_video": ref("ProductImageAndVideo"),
        "advanced": ref("ProductAdvanced"),
        "related_products": array_of("ProductLink"),
        "similar_products": array_of("ProductLink"),
        "seo_configs": array_of("ProductSeoConfig"),
        "tags": array_of("ProductTag"),
        "custom_properties": array_of("ProductCustomProperty"),
        "reviews": array_of("ProductReview", "Read-only: sending it is rejected with `400` and the reason `unknown_field`."),
        "product_variation": dict(ref("ProductVariation"), description="The product's variation types and variants, or `{}` on a product with no variations."),
        "preorder_enabled": typed("boolean"),
        "has_variations": typed("boolean", READ_ONLY),
    }},
    "ProductUrls": {"type": "object", "properties": {
        "url": typed("string", "The product's URL slug."),
        "product_url": typed("string", "The product's full storefront address."),
    }},
    "ProductNamedReference": {"type": "object", "description": "A record the product refers to: an author, a page, a customer or a customer group.", "properties": {
        "id": typed("integer", "The `id` of the named person, page, customer or customer group."),
        "name": typed("string"),
    }},
    "ProductParent": {"type": "object", "description": "One category the product is filed under. [List categories](" + CATEGORIES_PAGE + ") returns the store's categories.", "properties": {
        "id": typed("integer", "The category's id."),
        "name": typed("string"),
        "is_in_trash": typed("boolean"),
        "is_parent_in_trash": typed("boolean"),
        "is_disposable": typed("boolean"),
    }},
    "ProductSelectedCustomers": {"type": "object", "properties": {
        "customers": array_of("ProductNamedReference", "The customers the product is available to."),
        "groups": array_of("ProductNamedReference", "The customer groups the product is available to."),
    }},
    "ProductWeekday": {"type": "object", "description": "One day of the weekday schedule.", "properties": {
        "day": typed("string"),
        "start_hour": typed("integer"),
        "start_minute": typed("integer"),
        "end_hour": typed("integer"),
        "end_minute": typed("integer"),
        "is_full_day": typed("boolean"),
        "enabled": typed("boolean"),
    }},
    "ProductAvailableOnWeekdays": {"type": "object", "properties": {
        "enabled": typed("boolean"),
        "weekdays": array_of("ProductWeekday", "One entry per day in the schedule, or `[]` when `enabled` is `false`."),
    }},
    "ProductProperties": {"type": "object", "description": "The product's dimensions. Write them here; the product's top-level `length`, `width`, `height` and `weight` repeat them and are read-only.", "properties": {
        "length": typed("number"),
        "width": typed("number"),
        "height": typed("number"),
        "weight": typed("number"),
        "length_unit": typed("string"),
        "weight_unit": typed("string"),
    }},
    "ProductTaxSettings": {"type": "object", "description": "Tax settings for this product. They apply only when `overwrite_default_config` is `true`.", "properties": {
        "overwrite_default_config": typed("boolean"),
        "is_tax_exempt": typed("boolean"),
        "show_price_with_tax": typed("boolean"),
        "is_price_with_tax": typed("boolean"),
        "system_default_tax": typed("boolean"),
        "tax_message": typed("string"),
        "base_price_rounding": typed("string"),
        "default_tax_code": typed("string"),
        "custom_tax_profile_id": typed("string"),
    }},
    "ProductVariationPriceDisplay": {"type": "object", "description": "Which variant price a listing shows, and its labels.", "properties": {
        "method": typed("string"),
        "label_for_lowest_price": typed("string"),
        "label_for_highest_price": typed("string"),
    }},
    "ProductWarehouseStock": {"type": "object", "description": "One location's units, in an older format.", "properties": {
        "warehouse": typed("string", "The inventory location's id, as text, such as `\"4\"`. Every other location id in these responses is a number."),
        "stock": typed("integer"),
    }},
    "ProductStockLocation": {"type": "object", "description": "One inventory location the product is assigned to.", "properties": {
        "warehouse": typed("integer", "The inventory location's id. Pass it as `inventory_location_id` to unassign the location."),
        "warehouse_name": typed("string", "The inventory location's name."),
        "stock": typed("integer", "The units of the product at this location."),
        "low_stock_level": nullable("integer", "The low-stock level at this location, or `null` when it was set without one."),
        "is_default": typed("boolean", "`true` on the product's default location. Exactly one row has it."),
    }},
    "ProductPricingAndStock": {"type": "object", "description": "The product's pricing and stock settings.", "properties": {
        "track_inventory": typed("boolean"),
        "available_stock": typed("integer", "The sum of `stock` over the product's locations."),
        "low_level_stock": typed("integer", "Takes the `low_stock_level` of the product's default location."),
        "warehouses": array_of("ProductWarehouseStock", "The same units as `locations`, with each location id as text."),
        "minimum_order_quantity": typed("integer"),
        "maximum_order_quantity": typed("integer"),
        "tax_profile": {"description": "`{}` on every product read."},
        "shipping_profile": {"description": "`{}` on every product read."},
        "enable_multiple_order": typed("boolean"),
        "multiple_order_quantity": typed("integer"),
        "on_sale": typed("boolean"),
        "on_sale_price_type": typed("string"),
        "on_sale_price": typed("number"),
        "expected_to_pay": typed("boolean"),
        "expected_to_pay_price": typed("number"),
        "enable_call_for_price": typed("boolean"),
        "restrict_price_for": typed("string"),
        "restrict_price_for_except_customers": typed("array"),
        "restrict_purchase_for": typed("string"),
        "restrict_purchase_for_selected_customers": typed("array"),
        "hide_price": typed("boolean"),
        "enable_combined_stock_selling_limit": typed("boolean"),
        "combined_stock_selling_limit": typed("integer"),
        "enable_advance_pricing": typed("boolean"),
        "suppliers": typed("array"),
        "is_multi_location_enabled": typed("boolean"),
        "locations": array_of("ProductStockLocation", "The same rows as `locations` in [Retrieve a product's stock](" + STOCK_PAGE + ")."),
    }},
    "ProductImage": {"type": "object", "properties": {
        "id": typed("integer", "The image's id."),
        "filename": typed("string"),
        "alt_text": typed("string"),
        "thumbnail": typed("string"),
        "link": typed("string"),
    }},
    "ProductVideo": {"type": "object", "properties": {
        "id": typed("integer", "The video's id."),
        "filename": typed("string"),
        "thumbnail": typed("string"),
        "link": typed("string"),
    }},
    "ProductImageAndVideo": {"type": "object", "properties": {
        "images": array_of("ProductImage"),
        "videos": array_of("ProductVideo"),
        "specs": typed("array"),
    }},
    "ProductAdvanceInformation": {"type": "object", "description": "The product's identifiers and origin. An update that names one of these fields keeps the others.", "properties": {
        "global_trade_item_number": typed("string"),
        "gtin": typed("string"),
        "mpn": typed("string", ADVANCED_CODE),
        "upc": typed("string", ADVANCED_CODE),
        "barcode": typed("string", ADVANCED_CODE),
        "country_of_origin": typed("string"),
        "hs_code": typed("string", ADVANCED_CODE),
        "product_condition": typed("string"),
        "model": typed("string"),
    }},
    "ProductAdvanced": {"type": "object", "properties": {
        "advance_information": ref("ProductAdvanceInformation"),
        "webtool_disable_tracking": typed("boolean"),
        "meta_tags": typed("array"),
    }},
    "ProductLink": {"type": "object", "description": "A related or similar product.", "properties": {
        "id": typed("integer", "The linked product's id."),
        "name": typed("string"),
        "url": typed("string"),
    }},
    "ProductSeoConfig": {"type": "object", "description": "One SEO setting on the product.", "properties": {
        "id": typed("integer", "The SEO setting's id."),
        "value": typed("string"),
        "type": typed("string"),
        "config_key": typed("string"),
        "meta_tags": typed("array"),
    }},
    "ProductTagValue": {"type": "object", "properties": {
        "id": typed("integer", "The tag value's id."),
        "title": typed("string"),
        "value": typed("string"),
        "url": typed("string"),
    }},
    "ProductTag": {"type": "object", "description": "One tag on the product, with its values.", "properties": {
        "id": typed("integer", "The `id` of this entry in the product's `tags`."),
        "tag_id": typed("integer", "The tag's own id."),
        "name": typed("string"),
        "values": array_of("ProductTagValue"),
        "display_in_product_page": typed("boolean"),
        "enable_expanded_view": typed("boolean"),
    }},
    "ProductCustomProperty": {"type": "object", "properties": {
        "id": typed("integer", "The custom property's id."),
        "label": typed("string"),
        "description": typed("string"),
    }},
    "ProductReview": {"type": "object", "description": "One review of the product.", "properties": {
        "id": typed("integer", "The review's id."),
        "productId": typed("integer", "The reviewed product's id. This is the only camelCase field name in the product."),
        "name": typed("string"),
        "email": typed("string"),
        "review": nullable("string"),
        "rating": typed("number"),
        "date": typed("string"),
        "status": typed("string"),
        "files": typed("array"),
    }},
    "ProductVariationTypeOption": {"type": "object", "properties": {
        "id": typed("integer", "The option's id."),
        "label": typed("string"),
        "value": typed("string"),
        "default": typed("boolean"),
    }},
    "ProductVariationType": {"type": "object", "description": "One variation type the product uses, with its options.", "properties": {
        "id": typed("integer", "The variation type's id."),
        "name": typed("string"),
        "standard": typed("string"),
        "options": array_of("ProductVariationTypeOption"),
    }},
    "ProductCombinationOptionType": {"type": "object", "properties": {
        "id": typed("integer", "The variation type's id."),
        "role": typed("string"),
        "name": typed("string"),
        "standard": typed("string"),
        "is_disposable": typed("boolean"),
    }},
    "ProductCombinationOption": {"type": "object", "description": "One option of a variant.", "properties": {
        "id": typed("integer", "The option's id."),
        "index": typed("integer"),
        "type": array_of("ProductCombinationOptionType", "A list of one entry: the variation type the option belongs to."),
        "label": typed("string"),
        "value": typed("string"),
        "color_has_swatch": typed("boolean"),
        "color_swatch_value": typed("string"),
        "image_base_url": typed("string"),
    }},
    "ProductCombinationImage": {"type": "object", "properties": {
        "id": typed("integer", "The image's id."),
        "thumbnail": typed("string"),
        "url": typed("string"),
    }},
    "ProductCombinationPriceAndStock": {"type": "object", "description": "A variant's pricing and stock settings.", "properties": {
        "track_inventory": typed("boolean"),
        "available_stock": typed("integer"),
        "low_level_stock": typed("integer"),
        "minimum_order_quantity": typed("integer"),
        "maximum_order_quantity": typed("integer"),
        "supported_max_order_quantity": typed("integer"),
        "enable_multiple_order": typed("boolean"),
        "multiple_order_quantity": typed("integer"),
        "on_sale": typed("boolean"),
        "sold_out": typed("boolean"),
        "sold_out_label": typed("string"),
        "on_sale_price_type": typed("string"),
        "on_sale_price": typed("number"),
        "expected_to_pay": typed("boolean"),
        "expected_to_pay_price": typed("number"),
        "enable_call_for_price": typed("boolean"),
        "hide_price": typed("boolean"),
    }},
    "ProductCombinationDetails": {"type": "object", "description": "One variant of the product.", "properties": {
        "variation_id": typed("integer", "The variant's id."),
        "available": typed("boolean"),
        "product_name": typed("string"),
        "sku": typed("string"),
        "custom_sku": typed("string"),
        "urls": ref("ProductUrls"),
        "meta_tags": typed("array"),
        "is_inventory_enabled": typed("boolean"),
        "available_stock": typed("integer"),
        "low_stock_level": typed("integer"),
        "spec": typed("string"),
        "is_multiple_order_quantity": typed("boolean"),
        "is_on_sale": typed("boolean"),
        "is_expect_to_pay": typed("boolean"),
        "is_call_for_price_enabled": typed("boolean"),
        "is_new": typed("boolean"),
        "is_featured": typed("boolean"),
        "on_sale_amount_type": typed("string"),
        "title": typed("string"),
        "heading": typed("string"),
        "summary": typed("string"),
        "description": typed("string"),
        "model": typed("string"),
        "product_condition": typed("string"),
        "featured_label": typed("string"),
        "base_price": typed("number"),
        "cost_price": typed("number"),
        "sale_price": typed("number"),
        "expect_to_pay_price": typed("number"),
        "weight": {"type": ["number", "string"], "description": "A number on some products and text on others."},
        "height": {"type": ["number", "string"], "description": "A number on some products and text on others."},
        "length": {"type": ["number", "string"], "description": "A number on some products and text on others."},
        "width": {"type": ["number", "string"], "description": "A number on some products and text on others."},
        "display_price": typed("number"),
        "previous_price": typed("number"),
        "price_and_stock": ref("ProductCombinationPriceAndStock"),
        "images": array_of("ProductCombinationImage"),
        "videos": array_of("ProductVideo"),
        "specs": typed("array"),
        "supported_max_order_quantity": typed("integer"),
        "is_base": typed("boolean"),
        "barcode": typed("string"),
        "country_of_origin": typed("string"),
        "hs_code": typed("string"),
        "tax": typed("number"),
        "tax_message": typed("string"),
    }},
    "ProductCombination": {"type": "object", "description": "One combination of options and the variant it makes.", "properties": {
        "options": array_of("ProductCombinationOption"),
        "details": ref("ProductCombinationDetails"),
    }},
    "ProductVariation": {"type": "object", "description": "`{}` on a product with no variations.", "properties": {
        "types": array_of("ProductVariationType"),
        "available_combinations": array_of("ProductCombination"),
    }},
    "ProductInput": {"type": "object", "description": "Send these fields at the top level of the body, not inside `product`. Only the fields you send change, inside nested blocks too. A read-only field from [Retrieve a product](" + RETRIEVE_PAGE + ") is accepted when its value is unchanged and rejected with `400` and the reason `read_only_field` when it differs. `status` and `reviews` are rejected with the reason `unknown_field`. `updated_at`, `version`, `last_updated_on` and `last_updated_by` are ignored.", "properties": {
        "name": typed("string"),
        "sku": typed("string"),
        "heading": typed("string"),
        "product_type": typed("string"),
        "custom_type": typed("string"),
        "invoice_note": typed("string"),
        "available": typed("boolean"),
        "available_on_date_range": typed("boolean"),
        "available_from_date": typed("string", "Sent on its own, it is ignored."),
        "available_to_date": typed("string", "Sent on its own, it is ignored."),
        "available_for": typed("string"),
        "password_protected": typed("boolean"),
        "password": typed("string", "Send `***` to keep the stored password. Sent on its own, it is ignored."),
        "available_on_weekdays": ref("ProductAvailableOnWeekdays"),
        "base_price": typed("number"),
        "cost_price": typed("number"),
        "compare_at_price": typed("number"),
        "is_on_sale": typed("boolean"),
        "sale_price": typed("number"),
        "is_featured": typed("boolean"),
        "featured_label": typed("string"),
        "is_new": typed("boolean"),
        "product_properties": dict(ref("ProductProperties"), description="Write the dimensions here."),
        "schedule_type": typed("string"),
        "custom_schedule_option": typed("string"),
        "tax_settings": ref("ProductTaxSettings"),
        "variation_price_display": ref("ProductVariationPriceDisplay"),
        "administrative_status": typed("boolean"),
        "product_summary": typed("string"),
        "product_description": typed("string"),
        "product_pricing_and_stock": ref("ProductPricingAndStock"),
        "image_and_video": ref("ProductImageAndVideo"),
        "advanced": dict(ref("ProductAdvanced"), description="Write `mpn`, `upc`, `barcode` and `hs_code` in `advance_information` here."),
        "parents": {"type": "array", "items": {"type": "integer"}, "description": "The ids of the categories to file the product under."},
        "related_products": typed("array"),
        "similar_products": typed("array"),
        "tags": typed("array"),
        "preorder_enabled": typed("boolean"),
    }},
    "ProductStockVariation": {"type": "object", "description": "One variant's stock, on a product with variations.", "properties": {
        "variation_id": typed("integer", "The variant's id."),
        "product_id": typed("integer", "The variant's own product `id`. It differs from the `product_id` in the path."),
        "name": typed("string"),
        "sku": typed("string"),
        "available_stock": typed("integer"),
        "locations": array_of("ProductStockLocation"),
    }},
    "ProductStock": {"type": "object", "description": "A product's stock at each inventory location it is assigned to.", "properties": {
        "status": typed("string", "Always `success`."),
        "product_id": typed("integer", "The product's id, the `product_id` in the path."),
        "multi_location_enabled": typed("boolean", "`false` on a product with no location. Assigning the product's first location sets it to `true`."),
        "track_inventory": typed("boolean"),
        "available_stock": typed("integer", "The sum of `stock` over the rows in `locations`."),
        "locations": array_of("ProductStockLocation", "One row per inventory location the product is assigned to, or `[]` when it has none."),
        "variations": array_of("ProductStockVariation", "Only on a product with variations: one entry per variant."),
    }},
    "ProductStockLocationInput": {"type": "object", "required": ["warehouse"], "description": "One location the product keeps. Other keys, such as `warehouse_name`, are ignored.", "properties": {
        "warehouse": {"type": ["integer", "string"], "description": "Required. The inventory location's id, as a number or as numeric text. [List inventory locations](" + LOCATIONS_PAGE + ") returns the store's locations."},
        "stock": {"type": "integer", "minimum": 0, "description": "The units at this location, `0` or more."},
        "low_stock_level": nullable("integer", "The low-stock level at this location. Left out or `null`, it is stored as `null`."),
        "is_default": typed("boolean", "Send `true` on the row for the product's default location. When no row has it, the first row you send becomes the default."),
    }},
    "ProductStockInput": {"type": "object", "required": ["locations"], "description": "Send these fields at the top level of the body.", "properties": {
        "note": typed("string", "Optional. It changes nothing you can read back in the response or on the product."),
        "locations": {"type": "array", "minItems": 1, "items": ref("ProductStockLocationInput"), "description": "Required and not empty. Replaces the product's whole set of locations: a location you leave out is unassigned, even while it holds stock."},
    }},
    "ProductFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Returned beside `product` when you send `field_metadata=true` or `1`. An object keyed by field name, such as `id`: `{\"type\": \"integer\", \"read_only\": true}`. The `password` entry has `write_only: true`. It lists `mpn`, `upc`, `barcode`, `hs_code`, `length`, `width`, `height`, `weight` and `sold_out_label` as writable at the top level, but an update rejects each of them there."},
    "ProductError": {"type": "object", "description": "Rejections return this shape. A method a path does not support is rejected too: `HEAD` on a product returns `404` although its `Allow` header lists `HEAD`; `HEAD`, `POST`, `PATCH` and `OPTIONS` on a product's `stock` return `404` with the message `No such endpoint: <METHOD> /api/v4/admin/products/<product_id>/stock`; and `GET` on `stock/locations/{inventory_location_id}` returns `405` with the reason `method_not_allowed`.", "properties": {"error": {"type": "object", "properties": {
        "code": typed("string", "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."),
        "message": typed("string", "What went wrong, such as `locations is required`."),
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": typed("string", "The field or query parameter that was rejected."),
            "code": typed("string", "Why it was rejected, such as `unknown_parameter`, `has_stock` or `is_default`."),
            "message": nullable("string"),
            "value": {"description": "The value involved, when the API includes it, such as the inventory location's id on `has_stock`."},
        }}},
        "request_id": typed("string", "Identifies this request."),
    }}}},
}
