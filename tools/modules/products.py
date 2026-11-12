"""The Products endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Products"
SLUG = "products"
BASE = "/admin/products"
ICON = "box"

LIST_PAGE = "/api-reference/products/list-products"
CREATE_PAGE = "/api-reference/products/create-a-product"
RETRIEVE_PAGE = "/api-reference/products/retrieve-a-product"
UPDATE_PAGE = "/api-reference/products/update-a-product"
PATCH_PAGE = "/api-reference/products/patch-a-product"
DELETE_PAGE = "/api-reference/products/delete-a-product"
REVIEWS_PAGE = "/api-reference/products/import-a-products-reviews"
IMPORT_VARIANTS_PAGE = "/api-reference/variations/import-a-products-variants"
STOCK_PAGE = "/api-reference/products/retrieve-a-products-stock"
SET_STOCK_PAGE = "/api-reference/products/set-a-products-stock"
UNASSIGN_PAGE = "/api-reference/products/unassign-an-inventory-location-from-a-product"
LOCATIONS_PAGE = "/api-reference/inventory-locations/list-inventory-locations"
LOCATION_STOCK_PAGE = "/api-reference/inventory-locations/list-stock-at-an-inventory-location"
DELETE_LOCATION_PAGE = "/api-reference/inventory-locations/delete-an-inventory-location"
CATEGORIES_PAGE = "/api-reference/categories/list-categories"
COUNT_PAGE = "/api-reference/products/count-products"
CHECK_SKU_PAGE = "/api-reference/products/check-a-product-sku"
SPECIAL_PAGE = "/api-reference/products/list-special-products"
BULK_DELETE_PAGE = "/api-reference/products/delete-several-products"
LIST_REVIEWS_PAGE = "/api-reference/products/list-a-products-reviews"
RETRIEVE_REVIEW_PAGE = "/api-reference/products/retrieve-a-products-review"
PATCH_REVIEW_PAGE = "/api-reference/products/patch-a-products-review"
DELETE_REVIEW_PAGE = "/api-reference/products/delete-a-products-review"
INVENTORY_PAGE = "/api-reference/products/update-a-products-inventory"
UPLOAD_IMAGES_PAGE = "/api-reference/products/upload-images-to-a-product"
ADD_MEDIA_PAGE = "/api-reference/products/add-an-image-to-a-products-media"
DELETE_IMAGE_PAGE = "/api-reference/products/delete-a-products-image"
MEDIA_ORDER_PAGE = "/api-reference/products/set-the-order-of-a-products-images"
MOVE_IMAGE_PAGE = "/api-reference/products/move-a-products-image"
SEO_PAGE = "/api-reference/products/retrieve-a-products-seo-settings"
PATCH_STOCK_PAGE = "/api-reference/products/change-a-products-stock"
ADJUSTMENTS_PAGE = "/api-reference/products/list-a-products-stock-adjustments"

OVERVIEW_DESCRIPTION = "List, count, create, read, update and delete products, check a SKU, list special products, delete several products at once, import, list, read, change and delete a product's reviews, upload, reorder, move and delete its images, read its SEO settings, set its inventory, read, set and change its stock at each inventory location, list its stock adjustments, and unassign a location from it."
INTRO = "The Products API has twenty-seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/products`."

WARNING = (
    "**Setting a product's stock unassigns every location you leave out, even one that still holds stock.**\n"
    "  [Set a product's stock](" + SET_STOCK_PAGE + ") replaces the product's whole set of locations with the\n"
    "  rows you send in `locations`. Read the rows first with [Retrieve a product's stock](" + STOCK_PAGE + "),\n"
    "  send every row you want to keep, and change only the values you mean to change."
)

NOTES = [
    "**Turn stock tracking on before you sync stock.** A product that does not track its stock reads `available_stock: 0`, refuses a new\n"
    "  figure with `409` and the reason `tracking_disabled`, and keeps its stock when an order ships. Check `track_inventory` with\n"
    "  [Retrieve a product's stock](" + STOCK_PAGE + "), then send `{\"tracking\": {\"enabled\": true, \"available_stock\": 25}}` to\n"
    "  [Change a product's stock](" + PATCH_STOCK_PAGE + ") to turn tracking on and set the figure in one call. Creating an order does not\n"
    "  lower stock; [creating a shipment](/api-reference/orders/create-a-shipment) does, for products that track it.",
    "**Send product fields at the top level of the body, not inside `product`.** Responses return the\n"
    "  product inside `product`, but a create or `PUT` body wrapped in `product` is rejected with `400` and\n"
    "  the message `product: is not a recognised product field`. A `PATCH` body wrapped in `product` is\n"
    "  rejected with `400` in a different error shape, with `code` set to `validation_error` and the rejected\n"
    "  fields in `errors`. Send the stock body's `note` and `locations` at the top level too.\n"
    "  [Import a product's reviews](" + REVIEWS_PAGE + ") is the exception: wrap its reviews in `product`.",
    "**`PUT` and `PATCH` both change only the fields you send, at every level.** `{\"advanced\": {\"advance_information\": {\"mpn\": \"MPN-0001\"}}}`\n"
    "  changes `mpn` and keeps the other eight fields of `advance_information`. A body that changes nothing,\n"
    "  `{}` included, returns `200` and leaves `version` and the `ETag` header as they were.",
    "**Deleting a product moves it to the trash.** [Delete a product](" + DELETE_PAGE + ") returns `204`, but\n"
    "  [Retrieve a product](" + RETRIEVE_PAGE + ") still returns the product, with `status` set to `trashed`.\n"
    "  Every write to a product in the trash, including `PUT`, `PATCH` and importing reviews, is rejected with\n"
    "  `409`, and deleting it again returns `404` with the message `Product already in trash`.",
    "**Tag a create with a transaction number in the `X-Transaction-No` header or the body.** [Create a product](" + CREATE_PAGE + "),\n"
    "  [Import a product's reviews](" + REVIEWS_PAGE + ") and [Import a product's variants](" + IMPORT_VARIANTS_PAGE + ")\n"
    "  take an optional `X-Transaction-No` header; in the SDKs, pass `transaction_no`. You can send\n"
    "  `transaction_no` in the body instead. When you send both with different values, the header's value is\n"
    "  stored and the body's is lost, with no error. On `PUT` and `PATCH` the header is ignored, and a body\n"
    "  `transaction_no` is stored only on a product that has none: a product that has one keeps it.",
    "**Some fields cannot be written.** A changed `id`, `created_at`, `created_on`, `custom_class`,\n"
    "  `sold_out`, `sold_out_label`, `length`, `width`, `height`, `weight`, `featured`, `new`, `model`, `is_draft`,\n"
    "  `has_variations`, `urls` or `created_by` is rejected with `400` and the reason `read_only_field`; the value\n"
    "  you read is accepted. `status` and `reviews` are rejected with the reason `unknown_field`, so remove them\n"
    "  before you send back a product you read. Write the dimensions in `product_properties`, and `mpn`, `upc`,\n"
    "  `barcode` and `hs_code` in `advanced.advance_information`. `field_metadata` lists these fields as writable\n"
    "  at the top level, but they are rejected there.",
    "**Setting stock changes the product too.** `available_stock` is the sum of the rows' `stock`, and\n"
    "  `product_pricing_and_stock.low_level_stock` takes the `low_stock_level` of the product's default\n"
    "  location. The product's `version`, `updated_at` and `updated_by` change when the stock changes.\n"
    "  `product_pricing_and_stock.locations` on [Retrieve a product](" + RETRIEVE_PAGE + ") holds the same rows as\n"
    "  [Retrieve a product's stock](" + STOCK_PAGE + ").",
    "**The first location you assign to a product is missing from the response.** On a product with no\n"
    "  location yet, [Set a product's stock](" + SET_STOCK_PAGE + ") returns `locations: []` and stores the row.\n"
    "  Call [Retrieve a product's stock](" + STOCK_PAGE + ") to see it. A product that already has a location\n"
    "  returns its rows at once.",
    "**Find a `product_id` in the product list, a create response or an inventory location's stock.**\n"
    "  [List products](" + LIST_PAGE + ") returns every product with its `id`. [Create a product](" + CREATE_PAGE + ") returns the new product's `id` as\n"
    "  `product.id`. [List stock at an inventory location](" + LOCATION_STOCK_PAGE + ")\n"
    "  returns the `id` of each product the location holds, as `items[].product.id`.",
    "**A `PUT` must include ten fields.** [Update a product](" + UPDATE_PAGE + ") rejects a body that leaves out `name`, `sku`,\n"
    "  `base_price`, `product_type`, `available`, `is_on_sale`, `available_on_date_range`, `available_on_weekdays`,\n"
    "  `available_for` or `selected_customers` with `400` and the reason `required`. Every other field you leave out\n"
    "  keeps its value. [Patch a product](" + PATCH_PAGE + ") has no required fields.",
    "**A product returns its prices, flags and availability inside blocks, not as flat fields.** A product returns 46 fields, among them `pricing`, `inventory`, `ordering`,\n"
    "  `restrictions`, `tax`, `shipping`, `available_for_purchase`, `media`, `categories`, `up_sell_products`, `summary`, `description`, `virtual`, `product_url`, `updated_by` and `links`,\n"
    "  and `advanced` holds `product_flags`, `product_dimension`, `product_identifiers` and `webtool`. Read the base price from `pricing.base_price` and the featured flag from\n"
    "  `advanced.product_flags.featured.enabled`: the flat fields `base_price`, `is_featured` and the others that moved into blocks are not returned. A create and a `PATCH` still accept the flat\n"
    "  names, so `{\"base_price\": 3.5}` changes `pricing.base_price`.\n"
    "  These block fields are read-only: `product_url`, `links`, `restrictions.enabled`, `restrictions.display_only`,\n"
    "  `restrictions.price.enabled`, `restrictions.purchase.enabled`, `shipping.enabled`, the two units in\n"
    "  `advanced.product_dimension`, `advanced.product_flags.sold_out` and `advanced.webtool`. A value you send in\n"
    "  `updated_by`, `restrictions.price.customers` or `restrictions.purchase.customers` returns `200` and is not kept.",
    "**Some block fields behave differently from the flat ones.** `up_sell_products` takes `{\"id\": ...}` records: a list\n"
    "  of bare ids returns `200` and leaves `up_sell_products` empty. `categories` takes category ids or\n"
    "  `{\"id\": ...}` records, and `[]` changes nothing. `media` names files the product already holds. `shipping.profile`\n"
    "  (an id or `{\"id\": ...}`) is kept by an update and dropped by a create. `tax.custom_tax_profile` takes the id of a\n"
    "  custom tax profile. While `available_for_purchase.enabled` is `false`, a value you write in its `who_can_view`,\n"
    "  `schedule` or `password_protection` returns `200` and is not kept.",
    "**`selected_customers` and `restrict_for_selected_customers` are objects.** Each reads\n"
    "  `{\"customers\": [], \"groups\": []}` when nobody is named. To write `selected_customers`, send the customer ids in\n"
    "  `customers` and the customer group ids in `groups`; a group sent as `{\"id\": ...}` is rejected with `400`.\n"
    "  `restrict_for_selected_customers` is read-only.",
    "**Upload images as JSON with the file base64-encoded.** [Upload images to a product](" + UPLOAD_IMAGES_PAGE + ") and [Add an image to a product's media](" + ADD_MEDIA_PAGE + ") reject a multipart body\n"
    "  with `415`, the message `Content-Type must be application/json` and `details[0].field` set to `Content-Type`. Send the file's bytes as base64 text. Only images are accepted: a `type` of `videos` or\n"
    "  `specification_file` on [Add an image to a product's media](" + ADD_MEDIA_PAGE + ") is rejected with `400` and the reason `not_supported`. The store keeps the file under your `filename` with a UUID and `_`\n"
    "  in front, such as `<uuid>_front.png`, so compare the end of the name.",
    "**The two upload calls take different bodies and return different shapes.** [Upload images to a product](" + UPLOAD_IMAGES_PAGE + ") takes `{\"product\": {\"image_and_video\": {\"images\": [{\"filename\": ..., \"base64\": ...}]}}}`,\n"
    "  stores one or more files, and returns `201` with only the files it just stored in `product.images`, and no `Location` header. [Add an image to a product's media](" + ADD_MEDIA_PAGE + ") takes one file as\n"
    "  `{\"type\": \"images\", \"filename\": ..., \"content\": ...}` at the top level, where `content` is base64 text or a `data:image/png;base64,...` address, and returns `201` with a `Location` header and the stored image\n"
    "  as one flat row: `id`, `filename`, `position`, `primary`, `alt_text`, `url` and `thumbnail_url`. `position` is optional. A field named `base64` on that call is rejected with `400` and the reason `unknown_field`.\n"
    "  Pass the image's `id` as `image_id` to [Delete a product's image](" + DELETE_IMAGE_PAGE + "). Deleting it again returns `404`.",
    "**Delete several products moves them to the trash and returns `200` even when some fail.** Send `{\"ids\": [...]}` to [Delete several products](" + BULK_DELETE_PAGE + "); `product_ids` is rejected with `400` and the reason `required`,\n"
    "  and so is an empty list. `deleted` counts the products moved to the trash, `failed` counts the others, and `errors` lists each failure with its `id` and a `reason` such as `not_found`. A product in the trash\n"
    "  still holds its SKU, which [Check a product SKU](" + CHECK_SKU_PAGE + ") reports with `status` set to `trashed`, and neither [Count products](" + COUNT_PAGE + ") nor [List products](" + LIST_PAGE + ") includes it.",
    "**Count products takes the list's filters, but not its paging or sorting.** [Count products](" + COUNT_PAGE + ") returns `total` and `count`, which hold the same number, for the same filters as [List products](" + LIST_PAGE + "),\n"
    "  so the count equals `pagination.total` of the list with the same filters. `limit`, `offset` and `sortBy` are rejected with `400` and the reason `unknown_parameter`. `status` takes `active`, `inactive` or `draft`,\n"
    "  and `product_type` takes `physical`, `downloadable`, `gift_card` or `bundle`; any other value is rejected with `400` and the reason `invalid_enum`. `category` is accepted and filters nothing. A list or a count without `status` includes draft products.",
    "**List special products needs `type`, and two types need a customer.** Send `type` set to `onSale`, `featured`, `new`, `topSelling`, `lastBought` or `lastViewed`, in that letter case, to [List special products](" + SPECIAL_PAGE + ").\n"
    "  `max` is `1` to `100` and defaults to `10`, and `offset` is `0` or more. `lastBought` and `lastViewed` are per customer: send `customerId` (the customer's `customer_id`) or `customer_email`.\n"
    "  `customer_id` is not read, and a `customerId` no customer has is rejected with `400` and the reason `unknown_reference`. A per-customer list with no products also returns `\"status\": \"success\"`.",
    "**Check a product SKU also sees trashed products and variants.** [Check a product SKU](" + CHECK_SKU_PAGE + ") ignores letter case. A SKU held by a variant is reported under the variant's own product `id`, not the `id` of the parent\n"
    "  product, and a SKU held by a product in the trash is reported with `status` set to `trashed`. Send `exclude_product_id` with the `id` of the product you are editing to treat its own SKU as free.",
    "**A review's `status` is `pending` or `approved`, and the review list pages.** [Patch a product's review](" + PATCH_REVIEW_PAGE + ") takes `status`, `rating` and `comment`, and a `status` of `rejected` is rejected with `400` and the reason `invalid_enum`.\n"
    "  [List a product's reviews](" + LIST_REVIEWS_PAGE + ") takes `limit` (`1` to `100`, default `20`) and `offset` and returns a `pagination` block. It ignores `status` and `page`: a list sent with `status=pending` still returns approved reviews.\n"
    "  [Retrieve a product's review](" + RETRIEVE_REVIEW_PAGE + ") returns `404` with the message `Review not found` when no review has that `review_id`, and `400` when the review belongs to another product.",
    "**Updating a product's inventory sets the stock figure, and a variant keeps its own.** [Update a product's inventory](" + INVENTORY_PAGE + ") takes `track_inventory`, `available_stock` and `low_level_stock` inside\n"
    "  `product.product_pricing_and_stock` and returns `201`. Read the new stock with [Retrieve a product's stock](" + STOCK_PAGE + "). The stock of a product's variants does not change. The call takes the optional `X-Transaction-No` header:\n"
    "  the number is stored when the product has none, but the response to that first write shows the earlier value, `null`.",
    "**Set the order of all images, or move one.** [Set the order of a product's images](" + MEDIA_ORDER_PAGE + ") takes `{\"type\": \"images\", \"ids\": [...]}` and must name every image of the product exactly once, otherwise it is rejected with `400`\n"
    "  and the reason `invalid_set`. The first `id` becomes the `primary` image. [Move a product's image](" + MOVE_IMAGE_PAGE + ") takes only `{\"position\": n}`, counted from `1`; any other body, `alt_text` and a wrapper included, is rejected with `400` and the reason `invalid_body`.\n"
    "  Both send their fields at the top level of the body, with no wrapper.",
    "**Change stock with a `PATCH`, and expect `null` transaction numbers in the history.** [Change a product's stock](" + PATCH_STOCK_PAGE + ") takes `tracking`, `locations`, `note` and `transaction_no` at the top level of the body, and at least one of them.\n"
    "  A wrapper, or `available_stock` outside `tracking`, is rejected with `400` and the reason `unknown_field`. It returns `adjustment` as `null` when the stock figure did not change, and the adjustment's `note` is `via API` unless you send one.\n"
    "  [List a product's stock adjustments](" + ADJUSTMENTS_PAGE + ") returns every row with `transaction_no` set to `null`, also for a change you sent with a `transaction_no`, so do not look a change up by its transaction number.",
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
    "description": "The product's `id`. [Create a product](" + CREATE_PAGE + ") returns it as `product.id`, and [List stock at an inventory location](" + LOCATION_STOCK_PAGE + ") returns it as `items[].product.id`.",
    "schema": {"type": "integer", "example": 101},
}

TRANSACTION_NO = {
    "name": "X-Transaction-No",
    "in": "header",
    "description": "Optional. A transaction number to tag this create with, such as `IMPORT-2026-10-18`. In the SDKs, pass it as `transaction_no`. You can send `transaction_no` in the body instead. When you send both with different values, the header's value is stored and the body's is lost, with no error.",
    "schema": {"type": "string", "example": "IMPORT-2026-10-18"},
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
    "password_protected": False,
    "password": "",
    "pricing": {"base_price": 25.0, "cost_price": 12.0, "rrp_price": None, "on_sale": {"enabled": False, "discounted_price": None, "amount_type": "flat"}},
    "available_for_purchase": {"enabled": True, "active": True, "who_can_view": "all"},
    "version": 7,
    "product_pricing_and_stock": {
        "track_inventory": True,
        "available_stock": 35,
        "low_level_stock": 2,
        "warehouses": [{"warehouse": "1", "stock": 10}, {"warehouse": "4", "stock": 25}],
        "is_multi_location_enabled": True,
        "locations": LOCATION_ROWS,
    },
    "advanced": {"advance_information": {"mpn": "", "barcode": "", "hs_code": ""}, "product_flags": {"featured": {"enabled": False, "label": None}, "new_product": False}},
    "product_variation": {},
    "has_variations": False,
}

UPDATE_BODY = {
    "name": "Cotton T-Shirt",
    "sku": "TSHIRT-001",
    "base_price": 25.0,
    "product_type": "physical",
    "available": True,
    "is_on_sale": False,
    "available_on_date_range": False,
    "available_on_weekdays": {"enabled": False, "weekdays": []},
    "available_for": "all",
    "selected_customers": {"customers": [], "groups": []},
    "invoice_note": "Ships in 2 business days",
    "advanced": {"advance_information": {"mpn": "MPN-0001"}},
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

CREATE_BODY = {"name": "Blue Mug", "sku": "MUG-BLUE", "base_price": 12.5, "transaction_no": "IMPORT-2026-10-18"}
CREATED_PRODUCT = {
    "id": 102,
    "name": "Blue Mug",
    "sku": "MUG-BLUE",
    "status": "active",
    "transaction_no": "IMPORT-2026-10-18",
    "product_type": "physical",
    "pricing": {"base_price": 12.5, "cost_price": 0.0},
}

PATCHED_PRODUCT = copy.deepcopy(SAMPLE_PRODUCT)
PATCHED_PRODUCT["pricing"] = dict(PATCHED_PRODUCT["pricing"], base_price=27.5)
PATCHED_PRODUCT["version"] = 8

REVIEWS_BODY = {"product": {"reviews": [{"name": "Sam Lee", "email": "sam@example.com", "rating": 5, "review": "Great shirt", "status": "approved"}]}}
REVIEWS_RESULT = {"product": {"reviews": [
    {"id": 31, "productId": 101, "name": "Alex Kim", "email": "alex@example.com", "review": None, "rating": 4.0, "status": "pending", "files": []},
    {"id": 32, "productId": 101, "name": "Sam Lee", "email": "sam@example.com", "review": "Great shirt", "rating": 5.0, "status": "approved", "files": []},
]}}

LIST_PARAMETERS = [
    {"name": "limit", "in": "query", "description": "The number of products to return, from `1` to `100`. The default is `20`. `0` or a number above `100` is rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}},
    {"name": "offset", "in": "query", "description": "The number of products to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "minimum": 0, "example": 0}},
    {"name": "page", "in": "query", "description": "The page number, counted from `1`.", "schema": {"type": "integer", "minimum": 1, "example": 1}},
    {"name": "search_text", "in": "query", "description": "Returns the products whose `name` or `sku` contains this text. `searchText` works too.", "schema": {"type": "string", "example": "shirt"}},
    {"name": "name", "in": "query", "description": "Filters by product `name`.", "schema": {"type": "string"}},
    {"name": "sku", "in": "query", "description": "Filters by product `sku`.", "schema": {"type": "string"}},
    {"name": "ids", "in": "query", "description": "Returns the products with these `id` values. Repeat the name for several products, such as `ids=101&ids=102`. A comma-separated list is rejected with `500`.", "schema": {"type": "integer", "example": 101}},
    {"name": "parent", "in": "query", "description": "A category's `id`. [List categories](" + CATEGORIES_PAGE + ") returns it. Returns the products filed under that category.", "schema": {"type": "integer"}},
    {"name": "product_type", "in": "query", "description": "Returns one type of product: `physical`, `downloadable`, `gift_card` or `bundle`. `productType` works too.", "schema": {"type": "string", "enum": ["physical", "downloadable", "gift_card", "bundle"]}},
    {"name": "status", "in": "query", "description": "Returns the products with this status: `active`, `inactive` or `draft`. Any other value is rejected with `400` and the reason `invalid_enum`. Without it, the list includes draft products.", "schema": {"type": "string", "enum": ["active", "inactive", "draft"]}},
    {"name": "stock", "in": "query", "description": "Filters by stock level: `in`, `out` or `low`.", "schema": {"type": "string", "enum": ["in", "out", "low"]}},
    {"name": "is_available", "in": "query", "description": "Filters by whether the product is available.", "schema": {"type": "boolean"}},
    {"name": "is_inventory_enabled", "in": "query", "description": "Filters by whether the product tracks inventory.", "schema": {"type": "boolean"}},
    {"name": "created_by", "in": "query", "description": "Filters by who created the product.", "schema": {"type": "string"}},
    {"name": "price_from", "in": "query", "description": "Returns products priced from this amount.", "schema": {"type": "number"}},
    {"name": "price_to", "in": "query", "description": "Returns products priced up to this amount.", "schema": {"type": "number"}},
    {"name": "created_from", "in": "query", "description": "Returns products created from this date. Send `yyyy-MM-dd` or an ISO instant.", "schema": {"type": "string", "example": "2026-10-01"}},
    {"name": "created_to", "in": "query", "description": "Returns products created up to this date. Send `yyyy-MM-dd` or an ISO instant.", "schema": {"type": "string"}},
    {"name": "updated_from", "in": "query", "description": "Returns products updated from this date. Send `yyyy-MM-dd` or an ISO instant.", "schema": {"type": "string"}},
    {"name": "updated_to", "in": "query", "description": "Returns products updated up to this date. Send `yyyy-MM-dd` or an ISO instant.", "schema": {"type": "string"}},
    {"name": "sort", "in": "query", "description": "The field to sort by: `name`, `isAvailable`, `sku`, `parent`, `basePrice`, `isInventoryEnabled`, `createdBy`, `created`, `updated` or `id`.", "schema": {"type": "string", "example": "name"}},
    {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`.", "schema": {"type": "string", "enum": ["asc", "desc"]}},
    {"name": "category", "in": "query", "description": "The store accepts it and filters nothing. Use `parent` to filter by category.", "schema": {"type": "string"}},
    {"name": "field_metadata", "in": "query", "description": "Send `true` to add `field_metadata` beside `products`, a schema of the product fields.", "schema": {"type": "boolean", "example": True}},
]

COUNT_EXCLUDED = ("limit", "offset", "page", "sort", "dir", "field_metadata")


def count_parameter(parameter):
    description = parameter["description"]
    if parameter["name"] == "status":
        description = "Counts the products with this status: `active`, `inactive` or `draft`. Any other value is rejected with `400` and the reason `invalid_enum`. Without it, the count includes draft products."
    else:
        description = description.replace("Returns the products", "Counts the products").replace("Returns products", "Counts the products").replace("Returns one type of product", "Counts one type of product")
    return dict(parameter, description=description)


COUNT_PARAMETERS = [count_parameter(p) for p in LIST_PARAMETERS if p["name"] not in COUNT_EXCLUDED]

SKU_PARAMETERS = [
    {"name": "sku", "in": "query", "required": True, "description": "The SKU to look up. The match ignores letter case. `SKU` in capital letters is rejected with `400` and the reason `unknown_parameter`.", "schema": {"type": "string", "example": "TSHIRT-001"}},
    {"name": "exclude_product_id", "in": "query", "description": "A product's `id`. When that product holds the SKU, the SKU counts as free, so you can check a SKU while you edit the product that has it. Another product's `id` changes nothing.", "schema": {"type": "integer", "example": 101}},
]

SPECIAL_PARAMETERS = [
    {"name": "type", "in": "query", "required": True, "description": "Which selection to return: `onSale`, `featured`, `new`, `topSelling`, `lastBought` or `lastViewed`, in this letter case. A missing `type` is rejected with `400` and the reason `required`, and another value with the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["onSale", "featured", "new", "topSelling", "lastBought", "lastViewed"], "example": "featured"}},
    {"name": "max", "in": "query", "description": "The number of products to return, from `1` to `100`. The default is `10`. `0` or a negative number is rejected with `400` and the reason `out_of_range`, and so is a number above `100`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 10}},
    {"name": "offset", "in": "query", "description": "The number of products to skip, `0` or more. A negative number is rejected with `400` and the reason `out_of_range`. `page` is ignored.", "schema": {"type": "integer", "minimum": 0, "example": 0}},
    {"name": "customerId", "in": "query", "description": "A customer's `customer_id`. `lastBought` and `lastViewed` need it or `customer_email`. A `customerId` that no customer has is rejected with `400` and the reason `unknown_reference`. `customer_id` is not read.", "schema": {"type": "integer", "example": 74479}},
    {"name": "customer_email", "in": "query", "description": "A customer's email address. `lastBought` and `lastViewed` need it or `customerId`.", "schema": {"type": "string", "example": "alex@example.com"}},
]

REVIEW_ID = {
    "name": "review_id",
    "in": "path",
    "required": True,
    "description": "The review's `id`. [List a product's reviews](" + LIST_REVIEWS_PAGE + ") returns it as `reviews[].id`, and [Import a product's reviews](" + REVIEWS_PAGE + ") as `product.reviews[].id`. The review must belong to the product you pass as `product_id`.",
    "schema": {"type": "integer", "example": 31},
}

IMAGE_ID = {
    "name": "image_id",
    "in": "path",
    "required": True,
    "description": "The image's `id`. [Add an image to a product's media](" + ADD_MEDIA_PAGE + ") returns it as `id`, [Upload images to a product](" + UPLOAD_IMAGES_PAGE + ") as `product.images[].id`, and [Retrieve a product](" + RETRIEVE_PAGE + ") as `media.images[].id`.",
    "schema": {"type": "integer", "example": 1876},
}

REVIEW_LIMIT = {"name": "limit", "in": "query", "description": "The number of reviews per page, from `1` to `100`. The default is `20`. `0`, a number above `100` and text such as `abc` are rejected with `400`, the message `limit: must be a whole number from 1 to 100` and the reason `out_of_range`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
REVIEW_OFFSET = {"name": "offset", "in": "query", "description": "The number of reviews to skip, `0` or more. A negative number is rejected with `400` and the reason `out_of_range`. `page` and `status` are ignored.", "schema": {"type": "integer", "minimum": 0, "example": 0}}

INVENTORY_TRANSACTION_NO = dict(TRANSACTION_NO, description="Optional. A transaction number, such as `IMPORT-2026-10-18`. In the SDKs, pass it as `transaction_no`. The store stores it as the product's `transaction_no` when the product has none. The response to that first write shows `null`, the value from before the write.")

PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGNgAAIAAAUAAen63NgAAAAASUVORK5CYII="
IMAGE_UUID = "6f1c2d3e-5a6b-4c7d-8e9f-0a1b2c3d4e5f"

COUNT_RESULT = {"total": 117, "count": 117}
SKU_FREE = {"available": True, "is_exist": False, "product": None}
SKU_HELD = {"available": False, "is_exist": True, "product": {"id": 101, "name": "Cotton T-Shirt", "status": "active"}, "id": 101}

SPECIAL_ROW = {
    "id": 101,
    "sku": "TSHIRT-001",
    "name": "Cotton T-Shirt",
    "image": "https://your-store.example.com/resources/product/101/150-tshirt.png",
    "base_price": 27.5,
    "is_on_sale": False,
    "on_sale_amount_type": "flat",
    "effective_price": 25.0,
    "actual_base_price": 25.0,
    "on_sale_amount": 0.0,
    "expect_to_pay_price": 0.0,
    "expect_to_pay_price_with_tax": 27.5,
    "tax_exclusive_base_price": 25.0,
    "tax_exclusive_sale_price": 0.0,
    "tax": 2.5,
    "previous_price_to_display": None,
    "actual_price_to_display": 27.5,
    "sale_price": 0.0,
    "updated": "2026-10-10T10:42:00",
    "url": "https://your-store.example.com/product/cotton-t-shirt",
    "summary": "<p>Everyday cotton t-shirt.</p>",
    "description": "<p>Soft cotton.</p>",
}
SPECIAL_RESULT = {"total": 1, "max": 10, "offset": 0, "products": [SPECIAL_ROW], "pagination": {"total": 1, "limit": 10, "offset": 0, "has_previous": False, "has_next": False}}

BULK_DELETE_BODY = {"ids": [102, 103]}
BULK_DELETE_RESULT = {"deleted": 2, "failed": 0, "errors": []}

REVIEW_ROW = {"id": 31, "productId": 101, "name": "Alex Kim", "email": "alex@example.com", "review": "Great shirt", "rating": 4.0, "date": "2026-10-18T09:30:00", "status": "approved", "files": [], "product_id": 101, "reviewer": {"name": "Alex Kim", "email": "alex@example.com"}, "comment": "Great shirt", "created_at": "2026-10-18T09:30:00Z"}
REVIEW_LIST = {"reviews": [REVIEW_ROW], "pagination": {"total": 1, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}}
REVIEW_PATCH_BODY = {"status": "approved", "rating": 2, "comment": "Runs small"}
REVIEW_PATCHED = {"review": dict(REVIEW_ROW, rating=2.0, review="Runs small", comment="Runs small")}

INVENTORY_BODY = {"product": {"product_pricing_and_stock": {"track_inventory": True, "available_stock": 12, "low_level_stock": 3}}}
INVENTORY_RESULT = {"status": "success", "message": "Inventory has been updated successfully", "transaction_no": None}

IMAGE_BODY = {"product": {"image_and_video": {"images": [{"filename": "front.png", "base64": PNG_BASE64}]}}}
IMAGE_RESULT = {"product": {"images": [{"id": 1876, "filename": IMAGE_UUID + "_front.png", "alt_text": "", "thumbnail": "https://your-store.example.com/resources/product/101/150-" + IMAGE_UUID + "_front.png", "link": "https://your-store.example.com/resources/product/101/" + IMAGE_UUID + "_front.png"}], "videos": [], "specs": []}, "transaction_no": None}

MEDIA_BODY = {"type": "images", "filename": "side.png", "content": PNG_BASE64}
MEDIA_RESULT = {"id": 1877, "filename": IMAGE_UUID + "_side.png", "position": 2, "primary": False, "alt_text": "", "url": "https://your-store.example.com/resources/product/101/" + IMAGE_UUID + "_side.png", "thumbnail_url": "https://your-store.example.com/resources/product/101/150-" + IMAGE_UUID + "_side.png"}

IMAGE_ORDER_BODY = {"type": "images", "ids": [1877, 1876]}
IMAGE_ORDER_RESULT = {"images": [
    {"id": 1877, "filename": IMAGE_UUID + "_side.png", "position": 1, "primary": True, "alt_text": "", "url": "https://your-store.example.com/resources/product/101/" + IMAGE_UUID + "_side.png", "thumbnail_url": "https://your-store.example.com/resources/product/101/150-" + IMAGE_UUID + "_side.png"},
    {"id": 1876, "filename": IMAGE_UUID + "_front.png", "position": 2, "primary": False, "alt_text": "", "url": "https://your-store.example.com/resources/product/101/" + IMAGE_UUID + "_front.png", "thumbnail_url": "https://your-store.example.com/resources/product/101/150-" + IMAGE_UUID + "_front.png"},
]}
IMAGE_MOVE_BODY = {"position": 1}
IMAGE_MOVED = IMAGE_ORDER_RESULT["images"][0]

SEO_CARD = {"title": None, "description": None, "image_url": None}
SEO_RESULT = {"seo": {
    "url_handle": "blue-cotton-shirt",
    "title": None,
    "description": None,
    "advanced_settings": {"enabled": False, "robots_meta": "index", "canonical_url": None},
    "analytics": {
        "enabled": False,
        "platform": "google_analytics",
        "google_analytics": {"enabled": False, "measurement_id": None, "events": {"enabled": False, "view_item": False, "view_item_list": False, "view_cart": False, "add_to_wish_list": False, "remove_from_cart": False, "begin_checkout": False, "add_shipping_info": False, "add_payment_info": False, "purchase": False}},
        "facebook_pixel": {"enabled": False, "pixel_id": None, "events": {"enabled": False, "search": False, "add_to_cart": False, "add_to_wish_list": False, "initiate_checkout": False, "add_payment_info": False, "purchase": False}},
        "google_ads": {"conversion_id": None, "conversion_label": None},
    },
    "custom_code": {"header": {"enabled": False, "code": None}, "footer": {"enabled": False, "code": None}},
    "social": dict(SEO_CARD, facebook=dict(SEO_CARD), twitter=dict(SEO_CARD), linkedin=dict(SEO_CARD)),
    "ai_visibility": {"structured_attributes": None, "product_faq": None, "citability_score": None, "json_ld": None},
}}

STOCK_PATCH_BODY = {
    "tracking": {"enabled": True, "available_stock": 40},
    "note": "Restock",
}
ADJUSTMENT_ROW = {"id": 9001, "delta": 5, "note": "Restock", "transaction_no": None, "created_by": {"id": 12, "name": "Alex Kim"}, "created_at": "2026-11-11T09:30:00Z"}
STOCK_PATCH_RESULT = {
    "stock": {
        "tracking": {"enabled": True, "available_stock": 40, "low_stock_level": 5},
        "multi_location_enabled": False,
        "locations": [],
        "variations": [],
    },
    "adjustment": ADJUSTMENT_ROW,
}
ADJUSTMENTS_RESULT = {"adjustments": [ADJUSTMENT_ROW], "pagination": {"total": 1, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}}

ADJUSTMENT_PARAMETERS = [
    {"name": "limit", "in": "query", "description": "The number of adjustments to return. The default is `20`.", "schema": {"type": "integer", "minimum": 1, "example": 20}},
    {"name": "offset", "in": "query", "description": "The number of adjustments to skip.", "schema": {"type": "integer", "minimum": 0, "example": 0}},
]


LIST_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

ENDPOINTS = [
    {
        "key": "list_products",
        "slug": "list-products",
        "title": "List products",
        "method": "GET",
        "path": BASE,
        "summary": "Returns the store's products, 20 per call by default and up to 100, each as the full product record, with paging details.",
        "description": "Returns your store's products under `products`, the most recently updated first, with a `pagination` block. Each row is the full record [Retrieve a product](" + RETRIEVE_PAGE + ") returns, and a product in the trash is not listed. [Count products](" + COUNT_PAGE + ") counts the same products. `limit` is `1` to `100` and defaults to `20`. Page with `offset`, or with `page` counted from `1`; `offset` wins when you send both. Filter with `search_text`, `name`, `sku`, `ids`, `parent`, `product_type`, `status`, `stock`, `is_available`, `is_inventory_enabled`, `created_by`, `price_from`, `price_to`, `created_from`, `created_to`, `updated_from` and `updated_to`. Sort with `sort` and `dir`. `category` is accepted and filters nothing. Any other parameter is rejected with `400` and the reason `unknown_parameter`. `HEAD` on this path returns `404`.",
        "parameters": LIST_PARAMETERS,
        "responses": {
            "200": {
                "description": "`products` holds the products on this page, each with all 46 fields that [Retrieve a product](" + RETRIEVE_PAGE + ") returns. `pagination` has five keys: `total`, `limit`, `offset`, `has_previous` and `has_next`. With `field_metadata=true`, a `field_metadata` key is added beside `products`. The example shows a selection of the fields.",
                "schema": ref("ProductPage"),
                "example": {"products": [SAMPLE_PRODUCT, CREATED_PRODUCT], "pagination": LIST_PAGINATION},
            },
            "400": {
                "description": "`limit` is `0` or above `100`, or you sent a parameter the listing does not accept: `details[0].code` is `unknown_parameter`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
            "500": {"description": "`ids` is a comma-separated list. Repeat `ids` for each product instead.", "schema": ERROR_REF},
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "create_product",
        "slug": "create-a-product",
        "title": "Create a product",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a product and returns it with its `id`, which the other calls take as `product_id`.",
        "description": "Send the fields at the top level of the body, not inside `product`. `name` and `base_price` are required. `sku` must not belong to another product; leave it out and the store gives the product an `sku` made of `PRODUCT-` and 12 hexadecimal characters. `name` does not have to be unique: a product with a name another product has gets a different `urls.url`. `product_type` defaults to `physical`. `parents` takes the `id` of each category to file the product under, as a number or as `{\"id\": <category id>}`; [List categories](" + CATEGORIES_PAGE + ") returns each category's `id`. The body takes the same fields as [Update a product](" + UPDATE_PAGE + "). To tag the product with a transaction number, send the `X-Transaction-No` header (in the SDKs, `transaction_no`) or `transaction_no` in the body.",
        "parameters": [TRANSACTION_NO],
        "body": {"schema": ref("ProductCreateInput"), "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new product, with all 46 fields that [Retrieve a product](" + RETRIEVE_PAGE + ") returns. `status` is `active`, and `id` is the value the other calls take as `product_id`. `transaction_no` holds the number you sent, or `null` when you sent none. The example shows a selection of the fields.",
                "schema": PRODUCT_RESPONSE,
                "example": {"product": CREATED_PRODUCT},
            },
            "400": {
                "description": "`name` is missing (message `Product name is required`), `base_price` is missing (message `Product base price is required`), or the body is wrapped in `product` (message `product: is not a recognised product field`).",
                "schema": ERROR_REF,
            },
            "409": {"description": "Another product already has that `sku`. The message is `Product SKU already exists in another product`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_product",
        "slug": "retrieve-a-product",
        "title": "Retrieve a product",
        "method": "GET",
        "path": BASE + "/{product_id}",
        "summary": "Returns the product whose `id` you pass as `product_id`, with all 46 of its fields.",
        "description": "Returns one product under the `product` key, with its prices, availability, stock, media, tags, reviews and variations. Prices are in `pricing` and the flags in `advanced.product_flags`: flat fields such as `base_price` and `is_featured` are not returned. Send `field_metadata=true` to also get a description of each field. `field_metadata` is the only query parameter accepted: any other, such as `limit` or `fields`, is rejected with `400`. `password` reads `***` when the product has a password and `\"\"` when it has none. A product you deleted is still returned, with `status` set to `trashed`.",
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
        "summary": "Changes the product fields you send, keeps every other field, and returns the product. The body must include ten required fields.",
        "description": "Send the fields to change at the top level of the body, not inside `product`. The body must include `name`, `sku`, `base_price`, `product_type`, `available`, `is_on_sale`, `available_on_date_range`, `available_on_weekdays`, `available_for` and `selected_customers`; a missing one is rejected with `400` and the reason `required`. Apart from those, the update merges at every level: a field you leave out keeps its value, inside nested blocks too. Write the dimensions in `product_properties`, and `mpn`, `upc`, `barcode` and `hs_code` in `advanced.advance_information`. You can send back a product you read once you remove `status` and `reviews`.",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductInput"), "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The product after the update, with an `ETag` header. When something changed, `version`, `updated_at` and `updated_by` change too. The example shows a selection of the fields.",
                "schema": PRODUCT_RESPONSE,
                "example": {"product": UPDATED_PRODUCT},
            },
            "400": {
                "description": "One of the ten required fields is missing (reason `required`). Or the body is wrapped in `product` (message `product: is not a recognised product field`), or it has `status`, `reviews`, or a top-level `mpn`, `upc`, `barcode` or `hs_code` (reason `unknown_field`). Or it changes a read-only field such as `id`, `sold_out`, `model` or the top-level `weight` (reason `read_only_field`). Or a field that takes fixed values has another value (reason `invalid_enum`).",
                "schema": ERROR_REF,
            },
            "409": {"description": "The product is in the trash. The message is `cannot modify a product in the trash`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "patch_product",
        "slug": "patch-a-product",
        "title": "Patch a product",
        "method": "PATCH",
        "path": BASE + "/{product_id}",
        "summary": "Changes the product fields you send, keeps every other field, and returns the product, the same way `PUT` does.",
        "description": "Send the fields to change at the top level of the body, not inside `product`. This call takes the same body as [Update a product](" + UPDATE_PAGE + ") and merges it the same way: a field you leave out keeps its value, inside nested blocks too. A body that changes nothing, `{}` included, returns `200` with the product unchanged. The flat names such as `base_price` and `is_featured` are still accepted; the response shows the changed values in `pricing.base_price` and `advanced.product_flags.featured.enabled`. A product in the trash is rejected with `409`.",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductInput"), "example": {"base_price": 27.5}},
        "responses": {
            "200": {
                "description": "The product after the change. When something changed, `version`, `updated_at` and `updated_by` change too. The example shows a selection of the fields.",
                "schema": PRODUCT_RESPONSE,
                "example": {"product": PATCHED_PRODUCT},
            },
            "400": {
                "description": "The body is wrapped in `product`. This rejection has its own shape: `request_id`, `status` set to `400`, `code` set to `validation_error`, `message`, and an `errors` list in which each entry gives a `field` and a `code` such as `unknown_field`. Every other rejection returns the usual `error` object.",
                "schema": {"anyOf": [ERROR_REF, ref("ProductValidationError")]},
            },
            "409": {"description": "The product is in the trash. The message is `cannot modify a product in the trash`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "delete_product",
        "slug": "delete-a-product",
        "title": "Delete a product",
        "method": "DELETE",
        "path": BASE + "/{product_id}",
        "summary": "Moves the product to the trash. The product still reads back, with `status` set to `trashed`.",
        "description": "Moves the product to the trash and returns `204` with no body. The product is not deleted permanently: [Retrieve a product](" + RETRIEVE_PAGE + ") still returns it, with `status` set to `trashed`. Every write to it is then rejected with `409`, including [Update a product](" + UPDATE_PAGE + "), [Patch a product](" + PATCH_PAGE + ") and [Import a product's reviews](" + REVIEWS_PAGE + "). Deleting it again returns `404`. Query parameters are ignored, `permanent` included.",
        "parameters": [PRODUCT_ID],
        "responses": {
            "204": {"description": "The product is in the trash. No body."},
            "404": {"description": "The product is already in the trash, for example because you already deleted it. The message is `Product already in trash`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "import_product_reviews",
        "slug": "import-a-products-reviews",
        "title": "Import a product's reviews",
        "method": "POST",
        "path": BASE + "/{product_id}/reviews",
        "summary": "Adds the reviews you send to the product and returns every review the product now has.",
        "description": "Wrap the reviews in `product`: `{\"product\": {\"reviews\": [...]}}`. Each review needs `name`, `email` and a `rating` from `1` to `5`. Send the text as `review` or `comment`; it reads back as `review`. `status` `approved` is kept, and any other value, or none, is stored as `pending`. To set the review's date, send `dateCreated` as `yyyy-MM-ddTHH:mm:ss`: `date`, the key the response uses, is rejected. A review with an `email` the product already has a review from replaces that review: it keeps the earlier review's `id` and takes the new text and `rating`, with the same `201` and nothing in the response to show it. `title` and other unknown keys are accepted and dropped. To tag the reviews with a transaction number, send the `X-Transaction-No` header (in the SDKs, `transaction_no`) or `transaction_no` beside `product`, not inside it. A product in the trash is rejected with `409`.",
        "parameters": [PRODUCT_ID, dict(TRANSACTION_NO, description="Optional. A transaction number to tag the imported reviews with, such as `IMPORT-2026-10-18`. In the SDKs, pass it as `transaction_no`. You can send `transaction_no` in the body beside `product` instead. When you send both with different values, the header's value is stored and the body's is lost, with no error.")],
        "body": {"schema": ref("ProductReviewsImportInput"), "example": REVIEWS_BODY},
        "responses": {
            "201": {
                "description": "Every review the product has, oldest first, in `product.reviews`, not only the ones you sent. The reviews you added are last. A review that replaced an earlier one adds no entry: it shows under the earlier review's `id`, with the new text and `rating`. `rating` reads back as a decimal number, such as `5.0`. In the raw response text, the `@` in each `email` is written as `\\u0040`; a JSON parser turns it back into `@`.",
                "schema": {"type": "object", "properties": {"product": ref("ProductReviews")}},
                "example": REVIEWS_RESULT,
            },
            "400": {
                "description": "`product` is missing (message `product is required`); `reviews` is empty (message `reviews is required`); a review has no `name`, `email` or `rating` (messages `name is required`, `email is required` and `rating is required`); a `rating` is outside `1` to `5`, such as `6`; or a review sends `date`. A `date` in the `yyyy-MM-ddTHH:mm:ss` format is rejected with the message `Product reviews could not be imported`, and in any other format with the message `dateCreated must be a valid date (yyyy-MM-dd'T'HH:mm:ss)`.",
                "schema": ERROR_REF,
            },
            "409": {"description": "The product is in the trash.", "schema": ERROR_REF},
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
        "description": "Returns one row in `locations` for each inventory location the product is assigned to, with the location's `id` as `warehouse`, its name as `warehouse_name`, the product's `stock` there and the `low_stock_level`, and whether it is the product's default. `available_stock` is the sum of the rows' `stock`, and exactly one row has `is_default` set to `true`. A product with no location returns `multi_location_enabled: false` and `locations: []`, and a product with variations also returns `variations`. Query parameters are ignored." + "\n\n**Check this before you change stock.** `track_inventory` says whether the product tracks its stock. While it is `false`, `available_stock` reads `0`, the stock cannot be set, and shipping an order does not lower it. Turn tracking on with [Change a product's stock](/api-reference/products/change-a-products-stock) before you sync stock. `locations: []` means the store keeps the product's stock without inventory locations: change it with `tracking` in [Change a product's stock](/api-reference/products/change-a-products-stock), not with [Set a product's stock](/api-reference/products/set-a-products-stock).",
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
        "description": "Send `locations` with one row for every location the product keeps; a location you leave out is unassigned, even while it holds stock. Each row takes the location's `id` as `warehouse`, the units as `stock`, and optionally `low_stock_level` and `is_default`. When no row has `is_default: true`, the first row you send becomes the product's default. The rows [Retrieve a product's stock](" + STOCK_PAGE + ") returns can be sent back as they are: `warehouse_name` and other extra keys are ignored." + "\n\n**Use this only for a product assigned to inventory locations.** When [Retrieve a product's stock](/api-reference/products/retrieve-a-products-stock) returns `locations: []`, the store keeps the product's stock without locations: this call then answers `400` with the message `locations is required`. Set the figure with `tracking` in [Change a product's stock](/api-reference/products/change-a-products-stock) instead.",
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
    {
        "key": "count_products",
        "slug": "count-products",
        "title": "Count products",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns how many products match the filters you send, without the products themselves.",
        "description": "Returns `total` and `count`, which hold the same number: the products that match the filters. Draft products are counted and products in the trash are not, so with no filter the count equals `pagination.total` of [List products](" + LIST_PAGE + "). Send the list's filters: `search_text`, `name`, `sku`, `ids`, `parent`, `product_type`, `status`, `stock`, `is_available`, `is_inventory_enabled`, `created_by`, `price_from`, `price_to`, `created_from`, `created_to`, `updated_from` and `updated_to`. `productType` and `priceFrom` work as well as `product_type` and `price_from`, and the error messages name the camelCase form. Paging and sorting parameters, such as `limit`, `offset` and `sortBy`, are rejected with `400` and the reason `unknown_parameter`. `HEAD` on this path returns `404`.",
        "parameters": COUNT_PARAMETERS,
        "responses": {
            "200": {
                "description": "`total` is the number of products that match, and `count` repeats it.",
                "schema": ref("ProductCount"),
                "example": COUNT_RESULT,
            },
            "400": {
                "description": "You sent `limit`, `offset`, `sortBy` or another parameter the count does not accept (reason `unknown_parameter`), a `status` other than `active`, `inactive` or `draft` (reason `invalid_enum`), a `product_type` other than `physical`, `downloadable`, `gift_card` or `bundle` (reason `invalid_enum`), or a `price_from` that is not a number (reason `invalid_number`).",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": {"search_text": "shirt"}},
    },
    {
        "key": "check_product_sku",
        "slug": "check-a-product-sku",
        "title": "Check a product SKU",
        "method": "GET",
        "path": BASE + "/check-sku",
        "summary": "Tells you whether a SKU is free and, when it is not, which product holds it.",
        "description": "Send `sku` to learn whether a product already holds it. The match ignores letter case and also finds a SKU held by a product in the trash and by a variant. A variant's SKU is reported under the variant's own product `id`, not the `id` of the product it belongs to. Send `exclude_product_id` with the `id` of the product you are editing to treat that product's own SKU as free. [Create a product](" + CREATE_PAGE + ") rejects a SKU another product holds with `409`.",
        "parameters": SKU_PARAMETERS,
        "responses": {
            "200": {
                "description": "`available` is `true` and `is_exist` is `false` when the SKU is free; `product` is then `null` and the response has no `id`. When a product holds the SKU, `available` is `false`, `is_exist` is `true`, `product` gives the holder's `id`, `name` and `status` (`active` or `trashed`), and `id` repeats the holder's `id`.",
                "schema": ref("ProductSkuCheck"),
                "example": SKU_HELD,
            },
            "400": {
                "description": "`sku` is missing or empty (message `sku is required`), or you sent a parameter other than `sku` and `exclude_product_id`, `SKU` in capital letters included (reason `unknown_parameter`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": {"sku": "TSHIRT-001"}},
    },
    {
        "key": "list_special_products",
        "slug": "list-special-products",
        "title": "List special products",
        "method": "GET",
        "path": BASE + "/special",
        "summary": "Returns one selection of products: on sale, featured, new, top selling, or a customer's last bought or last viewed.",
        "description": "Send `type` to choose the selection: `onSale`, `featured`, `new`, `topSelling`, `lastBought` or `lastViewed`. Each row has the product's name, SKU, image, URL and its price fields, such as `base_price`, `sale_price` and `tax`. Page with `max` (`1` to `100`, default `10`) and `offset`; `pagination.limit` repeats `max`. `lastBought` and `lastViewed` are per customer, so also send `customerId` or `customer_email`. Parameters the endpoint does not know, `page` included, are ignored.",
        "parameters": SPECIAL_PARAMETERS,
        "responses": {
            "200": {
                "description": "`products` holds the selection's rows, `total` is the number of products in the selection, and `pagination` has `total`, `limit`, `offset`, `has_previous` and `has_next`. A per-customer selection that has no products also returns `status` set to `success`; a selection with products does not.",
                "schema": ref("ProductSpecialPage"),
                "example": SPECIAL_RESULT,
            },
            "400": {
                "description": "`type` is missing (reason `required`) or is not one of the six values (reason `invalid_enum`); `max` or `offset` is out of range (reason `out_of_range`); `lastBought` or `lastViewed` has neither `customerId` nor `customer_email` (reason `customer_required`); or `customerId` names no customer (reason `unknown_reference`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": {"type": "featured", "max": 10}},
    },
    {
        "key": "bulk_delete_products",
        "slug": "delete-several-products",
        "title": "Delete several products",
        "method": "POST",
        "path": BASE + "/bulk-delete",
        "summary": "Moves the products whose `id` values you send to the trash and counts the ones that could not be moved.",
        "description": "Send `ids`, the `id` of each product to move to the trash, at the top level of the body with no wrapper. Each product moves to the trash the way [Delete a product](" + DELETE_PAGE + ") moves it: it still reads back with `status` set to `trashed`, and nothing is deleted permanently. The call returns `200` even when some `id` values fail, so read `failed` and `errors` instead of the status code.",
        "body": {"schema": ref("ProductsBulkDeleteInput"), "example": BULK_DELETE_BODY},
        "responses": {
            "200": {
                "description": "`deleted` counts the products moved to the trash and `failed` counts the others. `errors` lists each failure with its `id` and a `reason`, such as `not_found`.",
                "schema": ref("ProductsBulkDeleteResult"),
                "example": BULK_DELETE_RESULT,
            },
            "400": {
                "description": "`ids` is missing or an empty list (reason `required`, message `ids: must be a non-empty list of product ids`). A body that sends `product_ids` instead of `ids` is rejected the same way.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
    {
        "key": "list_product_reviews",
        "slug": "list-a-products-reviews",
        "title": "List a product's reviews",
        "method": "GET",
        "path": BASE + "/{product_id}/reviews",
        "summary": "Returns the product's reviews, 20 per call by default, with paging details.",
        "description": "Returns the reviews of the product whose `id` you pass as `product_id`, under `reviews`, with a `pagination` block. Page with `limit` (`1` to `100`, default `20`) and `offset`. `status` and `page` are ignored: a request sent with `status=pending` still returns approved reviews. Each review is the same record [Import a product's reviews](" + REVIEWS_PAGE + ") returns. `HEAD` on this path returns `404`.",
        "parameters": [PRODUCT_ID, REVIEW_LIMIT, REVIEW_OFFSET],
        "responses": {
            "200": {
                "description": "`reviews` holds the reviews on this page, and `pagination` has `total`, `limit`, `offset`, `has_previous` and `has_next`. A product with no reviews returns `reviews: []`.",
                "schema": ref("ProductReviewList"),
                "example": REVIEW_LIST,
            },
            "400": {"description": "`limit` or `offset` is out of range (reason `out_of_range`).", "schema": ERROR_REF},
            "404": {"description": "No product has that `product_id`. The message is `Product not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}, "query": {"limit": 20}},
    },
    {
        "key": "get_product_review",
        "slug": "retrieve-a-products-review",
        "title": "Retrieve a product's review",
        "method": "GET",
        "path": BASE + "/{product_id}/reviews/{review_id}",
        "summary": "Returns one review of the product, under `review`.",
        "description": "Returns the review whose `id` you pass as `review_id`, under the `review` key. The review must belong to the product you pass as `product_id`.",
        "parameters": [PRODUCT_ID, REVIEW_ID],
        "responses": {
            "200": {
                "description": "The review, with the same fields as an entry of [List a product's reviews](" + LIST_REVIEWS_PAGE + ").",
                "schema": {"type": "object", "properties": {"review": ref("ProductReview")}},
                "example": {"review": REVIEW_ROW},
            },
            "400": {"description": "The review belongs to another product. The message is `Review does not belong to this product`.", "schema": ERROR_REF},
            "404": {"description": "No review has that `review_id`, for example because you deleted it. The message is `Review not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101, "review_id": 31}},
    },
    {
        "key": "patch_product_review",
        "slug": "patch-a-products-review",
        "title": "Patch a product's review",
        "method": "PATCH",
        "path": BASE + "/{product_id}/reviews/{review_id}",
        "summary": "Changes the `status`, `rating` or `comment` of one review and returns the review.",
        "description": "Send `status`, `rating` and `comment` at the top level of the body, with no wrapper. `status` is `pending` or `approved`. Only the fields you send change. A new `comment` changes the review's `review` text too, because the two hold the same text.",
        "parameters": [PRODUCT_ID, REVIEW_ID],
        "body": {"schema": ref("ProductReviewPatchInput"), "example": REVIEW_PATCH_BODY},
        "responses": {
            "200": {
                "description": "The review after the change, under `review`.",
                "schema": {"type": "object", "properties": {"review": ref("ProductReview")}},
                "example": REVIEW_PATCHED,
            },
            "400": {"description": "`status` is not `pending` or `approved`, `rejected` included. The reason is `invalid_enum` and the message is `status must be one of pending, approved`.", "schema": ERROR_REF},
            "404": {"description": "No review has that `review_id`. The message is `Review not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101, "review_id": 31}},
    },
    {
        "key": "delete_product_review",
        "slug": "delete-a-products-review",
        "title": "Delete a product's review",
        "method": "DELETE",
        "path": BASE + "/{product_id}/reviews/{review_id}",
        "summary": "Deletes one review of the product permanently.",
        "description": "Deletes the review whose `id` you pass as `review_id` and returns `204` with no body. The review does not go to the trash: [Retrieve a product's review](" + RETRIEVE_REVIEW_PAGE + ") then returns `404`, and deleting it again returns `404`.",
        "parameters": [PRODUCT_ID, REVIEW_ID],
        "responses": {
            "204": {"description": "The review is deleted. No body."},
            "404": {"description": "No review has that `review_id`, for example because you already deleted it.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101, "review_id": 31}},
    },
    {
        "key": "create_product_inventory",
        "slug": "update-a-products-inventory",
        "title": "Update a product's inventory",
        "method": "POST",
        "path": BASE + "/{product_id}/inventories",
        "summary": "Sets whether the product tracks stock, its available stock and its low stock level.",
        "description": "Wrap the settings in `product.product_pricing_and_stock` and send `track_inventory`, `available_stock` and optionally `low_level_stock`. The call returns `201`. Read the new stock with [Retrieve a product's stock](" + STOCK_PAGE + "): on a store with one inventory location, `locations` is empty. The stock of the product's variants does not change, because each variant keeps its own. To store a transaction number, pass `transaction_no` in the SDKs, which sends the `X-Transaction-No` header.",
        "parameters": [PRODUCT_ID, INVENTORY_TRANSACTION_NO],
        "body": {"schema": ref("ProductInventoryInput"), "example": INVENTORY_BODY},
        "responses": {
            "201": {
                "description": "`status` is `success` and `message` is `Inventory has been updated successfully`. `transaction_no` shows the product's number from before this write, so it is `null` when this write is the first to store one. The response has an `ETag` header.",
                "schema": ref("ProductInventoryResult"),
                "example": INVENTORY_RESULT,
            },
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "create_product_image",
        "slug": "upload-images-to-a-product",
        "title": "Upload images to a product",
        "method": "POST",
        "path": BASE + "/{product_id}/image",
        "summary": "Stores one or more base64-encoded images on the product and returns the images it stored.",
        "description": "Send JSON: wrap the files in `product.image_and_video.images`, each with a `filename` and the file's bytes as base64 text in `base64`. You can send several files in one call. A multipart body is rejected with `415`. The store keeps each file under your `filename` with a UUID and `_` in front. To add one image at a chosen `position`, use [Add an image to a product's media](" + ADD_MEDIA_PAGE + ").",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductImageUploadInput"), "example": IMAGE_BODY},
        "responses": {
            "201": {
                "description": "`product.images` holds only the files this call stored, each with `id`, `filename`, `alt_text`, `thumbnail` and `link`; `videos` and `specs` are empty. `transaction_no` is the product's number, or `null`. The response has no `Location` header.",
                "schema": ref("ProductMediaUploaded"),
                "example": IMAGE_RESULT,
            },
            "415": {"description": "The body is not JSON. The message is `Content-Type must be application/json` and `details[0].field` is `Content-Type`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "create_product_media",
        "slug": "add-an-image-to-a-products-media",
        "title": "Add an image to a product's media",
        "method": "POST",
        "path": BASE + "/{product_id}/media",
        "summary": "Stores one base64-encoded image on the product and returns the stored image as one row.",
        "description": "Send JSON at the top level of the body, with no wrapper: `type` set to `images`, a `filename`, and `content`, which is the file's bytes as base64 text or a `data:image/png;base64,...` address. `position` is optional. Only images are accepted. A multipart body is rejected with `415`. The store keeps the file under your `filename` with a UUID and `_` in front. To store several files in one call, use [Upload images to a product](" + UPLOAD_IMAGES_PAGE + ").",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductMediaUploadInput"), "example": MEDIA_BODY},
        "responses": {
            "201": {
                "description": "The stored image as one row, not wrapped in `product`: `id`, `filename`, `position`, `primary`, `alt_text`, `url` and `thumbnail_url`. The first image of a product has `position` `1` and `primary` `true`. The `Location` header is the path of the image, `/api/v4/admin/products/{product_id}/media/images/{image_id}`.",
                "schema": ref("ProductMediaImage"),
                "example": MEDIA_RESULT,
            },
            "400": {
                "description": "`type` is `videos` or `specification_file` (reason `not_supported`, message `videos cannot be uploaded through the API yet - images only`); `filename` or `content` is missing (reason `required`); or you sent a field the call does not accept, such as `base64` in place of `content` (reason `unknown_field`).",
                "schema": ERROR_REF,
            },
            "415": {"description": "The body is not JSON. The message is `Content-Type must be application/json`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "delete_product_media_image",
        "slug": "delete-a-products-image",
        "title": "Delete a product's image",
        "method": "DELETE",
        "path": BASE + "/{product_id}/media/images/{image_id}",
        "summary": "Deletes one image from the product.",
        "description": "Deletes the image whose `id` you pass as `image_id` and returns `204` with no body. Deleting it again returns `404`.",
        "parameters": [PRODUCT_ID, IMAGE_ID],
        "responses": {
            "204": {"description": "The image is deleted. No body."},
            "404": {"description": "The product has no image with that `image_id`, for example because you already deleted it. The message is `Image id: <image_id> not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101, "image_id": 1876}},
    },
    {
        "key": "update_product_media_order",
        "slug": "set-the-order-of-a-products-images",
        "title": "Set the order of a product's images",
        "method": "PUT",
        "path": BASE + "/{product_id}/media/order",
        "summary": "Sets the order of all of the product's images and returns them in the new order.",
        "description": "Send `type` set to `images` and `ids`, the `id` of every image of the product in the order you want, at the top level of the body with no wrapper. You must name every image exactly once. The first `id` becomes the `primary` image. The call returns the product's images in the new order under `images`. To move one image, use [Move a product's image](" + MOVE_IMAGE_PAGE + ").",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductMediaOrderInput"), "example": IMAGE_ORDER_BODY},
        "responses": {
            "200": {
                "description": "The product's images in the new order, under `images`. The first one has `position` `1` and `primary` `true`.",
                "schema": ref("ProductMediaOrder"),
                "example": IMAGE_ORDER_RESULT,
            },
            "400": {"description": "`ids` does not name every image of the product exactly once. The reason is `invalid_set`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "patch_product_media_image",
        "slug": "move-a-products-image",
        "title": "Move a product's image",
        "method": "PATCH",
        "path": BASE + "/{product_id}/media/images/{image_id}",
        "summary": "Moves one image of the product to the position you send and returns the image.",
        "description": "Send `position`, counted from `1`, at the top level of the body with no wrapper. `position` is the only field the call takes: any other body, `alt_text` and a wrapper included, is rejected with `400` and the reason `invalid_body`. The call returns the image as one flat row, not wrapped in `product`. The image at position `1` is `primary`. To order all images at once, use [Set the order of a product's images](" + MEDIA_ORDER_PAGE + ").",
        "parameters": [PRODUCT_ID, IMAGE_ID],
        "body": {"schema": ref("ProductMediaImagePatchInput"), "example": IMAGE_MOVE_BODY},
        "responses": {
            "200": {
                "description": "The image after the move, as one row: `id`, `filename`, `position`, `primary`, `alt_text`, `url` and `thumbnail_url`.",
                "schema": ref("ProductMediaImage"),
                "example": IMAGE_MOVED,
            },
            "400": {"description": "The body is anything other than `{\"position\": n}`. The reason is `invalid_body`.", "schema": ERROR_REF},
            "404": {"description": "The product has no image with that `image_id`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101, "image_id": 1877}},
    },
    {
        "key": "get_product_seo",
        "slug": "retrieve-a-products-seo-settings",
        "title": "Retrieve a product's SEO settings",
        "method": "GET",
        "path": BASE + "/{product_id}/seo",
        "summary": "Returns the product's URL handle, title, description, analytics, custom code, social cards and AI visibility settings.",
        "description": "Returns the product's SEO settings under `seo`: `url_handle`, `title`, `description`, `advanced_settings`, `analytics` (Google Analytics, Facebook Pixel and Google Ads), `custom_code`, `social` and `ai_visibility`. The call ignores `field_metadata`. `HEAD` on this path returns `404`.",
        "parameters": [PRODUCT_ID],
        "responses": {
            "200": {
                "description": "The product's SEO settings under `seo`.",
                "schema": {"type": "object", "properties": {"seo": ref("ProductSeo")}},
                "example": SEO_RESULT,
            },
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "patch_product_stock",
        "slug": "change-a-products-stock",
        "title": "Change a product's stock",
        "method": "PATCH",
        "path": BASE + "/{product_id}/stock",
        "summary": "Changes the product's stock tracking or its stock at each location, and returns the stock and the adjustment it recorded.",
        "description": "Send at least one of `tracking`, `locations`, `note` and `transaction_no` at the top level of the body, with no wrapper. `tracking` takes `enabled`, `available_stock` and `low_stock_level`, and the fields you send are merged into the product's tracking. `locations` takes rows in the form [Set a product's stock](" + SET_STOCK_PAGE + ") takes. `note` and `transaction_no` go on the adjustment. The call returns the product's `stock` as it is now, and the `adjustment` it recorded. `adjustment` is `null` when the stock figure did not change, and its `note` is `via API` unless you send one. A wrapper, or `available_stock` outside `tracking`, is rejected with `400` and the reason `unknown_field`." + "\n\n**Before you set stock, make sure tracking is on.**\n\n1. Read the product with [Retrieve a product's stock](/api-reference/products/retrieve-a-products-stock).\n2. If `track_inventory` is `true`, send `{\"tracking\": {\"available_stock\": 25}}`.\n3. If it is `false`, turn tracking on and set the figure in the same call: `{\"tracking\": {\"enabled\": true, \"available_stock\": 25}}`.\n\nSetting `available_stock` while tracking is off is refused with `409` and the message `inventory tracking is off for this product - turn tracking.enabled on to set its stock` (field `tracking.available_stock`, reason `tracking_disabled`); resend it with `\"enabled\": true`.\n\nTo turn tracking off, send `{\"tracking\": {\"enabled\": false}}` on its own: the same `409` refuses a call that also sends `available_stock`, so set the figure first and turn tracking off in a second call.",
        "parameters": [PRODUCT_ID],
        "body": {"schema": ref("ProductStockPatchInput"), "example": STOCK_PATCH_BODY},
        "responses": {
            "200": {
                "description": "`stock` is the product's stock after the change, and `adjustment` is the change the store recorded, or `null` when the figure did not change.",
                "schema": ref("ProductStockPatchResult"),
                "example": STOCK_PATCH_RESULT,
            },
            "400": {"description": "The body is wrapped, or sends `available_stock` outside `tracking`. The reason is `unknown_field`.", "schema": ERROR_REF},
            "409": {"description": "`tracking.available_stock` was sent while the product's stock tracking is off. The message is `inventory tracking is off for this product - turn tracking.enabled on to set its stock` and the reason `tracking_disabled`. Resend with `tracking.enabled` set to `true`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 101}},
    },
    {
        "key": "list_product_stock_adjustments",
        "slug": "list-a-products-stock-adjustments",
        "title": "List a product's stock adjustments",
        "method": "GET",
        "path": BASE + "/{product_id}/stock/adjustments",
        "summary": "Returns the product's stock changes, newest first, with paging details.",
        "description": "Returns the product's stock adjustments under `adjustments`, newest first, with a `pagination` block. Page with `limit`, which defaults to `20`, and `offset`. Each row has the change as `delta` (the new figure minus the old one), its `note`, who made it and when. Every row returns `transaction_no` as `null`, also for a change you sent with a `transaction_no`. `HEAD` on this path returns `404`.",
        "parameters": [PRODUCT_ID] + ADJUSTMENT_PARAMETERS,
        "responses": {
            "200": {
                "description": "The adjustments on this page under `adjustments`, and `pagination` with five keys: `total`, `limit`, `offset`, `has_previous` and `has_next`.",
                "schema": ref("ProductStockAdjustmentPage"),
                "example": ADJUSTMENTS_RESULT,
            },
        },
        "example_call": {"path": {"product_id": 101}, "query": {"limit": 20}},
    },
]

READ_ONLY = "Read-only: a changed value is rejected with `400` and the reason `read_only_field`."
DIMENSION = "Read-only here: write it in `product_properties`. A changed value is rejected with `400` and the reason `read_only_field`."
STAMP = "Changes when the product changes. A value you send is ignored."
ADVANCED_CODE = "Write it here: at the top level of the product it is rejected with `400` and the reason `unknown_field`."

SCHEMAS = {
    "Product": {"type": "object", "description": "One product: 46 fields, the same set on every product. Prices, flags, dimensions, availability and stock settings are inside blocks such as `pricing`, `advanced` and `available_for_purchase`; flat fields such as `base_price` and `is_featured` are not returned.", "properties": {
        "id": typed("integer", "The product's `id`. Pass it as `product_id` in a path. " + READ_ONLY),
        "name": typed("string"),
        "sku": typed("string"),
        "status": typed("string", "`active` on a new product and `trashed` on a product you deleted. Read-only: sending it is rejected with `400` and the reason `unknown_field`."),
        "urls": dict(ref("ProductUrls"), description=READ_ONLY),
        "heading": typed("string"),
        "created_by": dict(ref("ProductNamedReference"), description="Who created the product. " + READ_ONLY),
        "created_at": typed("string", READ_ONLY),
        "updated_at": typed("string", STAMP),
        "transaction_no": nullable("string", "The product's transaction number, or `null` when it has none."),
        "product_type": typed("string"),
        "custom_type": typed("string"),
        "invoice_note": typed("string"),
        "product_page": dict(ref("ProductNamedReference"), description="The product's page as `id` and `name`. Some products return `{}` instead."),
        "product_layout": {"description": "`{}` on every product read."},
        "custom_class": typed("string", READ_ONLY),
        "password_protected": typed("boolean"),
        "password": typed("string", "`***` when the product has a password, `\"\"` when it has none. Sending back `***` keeps the stored password."),
        "version": typed("integer", "Changes when the product changes, including when its stock changes. A write that changes nothing keeps it. A value you send is ignored."),
        "variation_price_display": ref("ProductVariationPriceDisplay"),
        "product_pricing_and_stock": ref("ProductPricingAndStock"),
        "advanced": ref("ProductAdvanced"),
        "related_products": array_of("ProductLink"),
        "bundle": {"oneOf": [ref("ProductBundle"), {"type": "null"}], "description": "The product's bundle settings, or `null` when the product is not a bundle."},
        "seo_configs": array_of("ProductSeoConfig"),
        "tags": array_of("ProductTag"),
        "custom_properties": array_of("ProductCustomProperty"),
        "reviews": array_of("ProductReview", "Read-only: sending it is rejected with `400` and the reason `unknown_field`."),
        "product_variation": dict(ref("ProductVariation"), description="The product's variation types and variants, or `{}` on a product with no variations."),
        "has_variations": typed("boolean", READ_ONLY),
        "available_for_purchase": dict(ref("ProductAvailableForPurchase"), description="Availability in one block: `enabled` is whether the product is available, `active` is whether it is active in the administration and `who_can_view` is who can buy it."),
        "categories": array_of("ProductCategory", "The categories the product is filed under. In a write, send the `id` of each category in `parents`."),
        "description": typed("string", "The product's description."),
        "inventory": dict(ref("ProductInventory"), description="Stock settings in one block: stock tracking, the combined stock limit and pre-order."),
        "links": dict(ref("ProductLinks"), description="The API paths of the product and its sub-paths. Read-only."),
        "media": dict(ref("ProductMedia"), description="The product's images and videos."),
        "ordering": dict(ref("ProductOrdering"), description="The smallest and largest quantity a customer can order."),
        "pricing": dict(ref("ProductPricing"), description="Prices in one block: the base price, the cost price, the recommended retail price and the sale and advanced pricing settings. Read the product's price from `pricing.base_price`."),
        "product_url": typed("string", "The product's full storefront address. Read-only."),
        "restrictions": dict(ref("ProductRestrictions"), description="Who can see the price and who can buy, in one block."),
        "shipping": dict(ref("ProductShipping"), description="The product's shipping profile."),
        "summary": typed("string", "The product's summary."),
        "tax": dict(ref("ProductTax"), description="The product's tax settings in one block."),
        "up_sell_products": array_of("ProductLink", "The products offered as an up-sell. In a write, send `{\"id\": ...}` records."),
        "updated_by": dict(ref("ProductNamedReference"), description="Who last changed the product. A value you send returns `200` and is not kept."),
        "virtual": typed("boolean", "`true` when the product is virtual."),
    }},
    "ProductUrls": {"type": "object", "properties": {
        "url": typed("string", "The product's URL slug."),
        "product_url": typed("string", "The product's full storefront address."),
    }},
    "ProductNamedReference": {"type": "object", "description": "A record the product refers to: an author, a page, a customer or a customer group.", "properties": {
        "id": typed("integer", "The `id` of the named person, page, customer or customer group."),
        "name": typed("string"),
    }},
    "ProductSelectedCustomer": {"type": "object", "description": "One customer an audience names.", "properties": {
        "id": typed("integer", "The customer's `customer_id`."),
        "internal_id": typed("integer", "The customer's `internal_id`."),
        "name": typed("string"),
    }},
    "ProductSelectedCustomersInput": {"type": "object", "description": "An audience to write: customer and group ids.", "properties": {
        "customers": {"type": "array", "items": {"type": "integer"}, "description": "The `customer_id` of each customer."},
        "groups": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each customer group. A group sent as `{\"id\": ...}` is rejected with `400`."},
    }},
    "ProductSelectedCustomers": {"type": "object", "description": "Who the product is available to, or whom a restriction names. Both lists are empty when nobody is named.", "properties": {
        "customers": array_of("ProductSelectedCustomer", "The customers named."),
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
        "lowest_price_label": typed("string", "A second name for `label_for_lowest_price`."),
        "highest_price_label": typed("string", "A second name for `label_for_highest_price`."),
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
        "enable_product_identifiers": typed("boolean"),
        "gtin": typed("string"),
        "mpn": typed("string", ADVANCED_CODE),
        "upc": typed("string", ADVANCED_CODE),
        "barcode": typed("string", ADVANCED_CODE),
        "country_of_origin": typed("string"),
        "hs_code": typed("string", ADVANCED_CODE),
        "product_condition": typed("string"),
        "model": typed("string"),
    }},
    "ProductFlag": {"type": "object", "description": "A flag and the label shown with it.", "properties": {
        "enabled": typed("boolean"),
        "label": typed("string"),
    }},
    "ProductFlags": {"type": "object", "description": "The product's flags in one block.", "properties": {
        "featured": dict(ref("ProductFlag"), description="Whether the product is flagged as featured, and its label."),
        "new_product": typed("boolean", "Whether the product is flagged as new."),
        "sold_out": dict(ref("ProductFlag"), description="Whether the product is sold out, and its label. Read-only."),
        "model_number": typed("string", "The product's model number."),
    }},
    "ProductDimension": {"type": "object", "description": "The product's dimensions and their units. The two units are read-only here. Write the dimensions in `product_properties`.", "properties": {
        "length_unit": typed("string", "Read-only here."),
        "weight_unit": typed("string", "Read-only here."),
        "width": typed("number"),
        "height": typed("number"),
        "length": typed("number"),
        "weight": typed("number"),
    }},
    "ProductIdentifiers": {"type": "object", "description": "The same values as `advance_information`: a write here changes it there.", "properties": {
        "enabled": typed("boolean", "The same value as `enable_product_identifiers`."),
        "gtin": typed("string"),
        "condition": typed("string", "The same value as `product_condition`."),
        "barcode": typed("string"),
        "hs_code": typed("string"),
        "country_of_origin": typed("string"),
        "mpn": typed("string"),
        "upc": typed("string"),
    }},
    "ProductWebtool": {"type": "object", "description": "Read-only.", "properties": {
        "disable_tracking": typed("boolean", "The same value as `webtool_disable_tracking`."),
    }},
    "ProductAdvanced": {"type": "object", "properties": {
        "advance_information": ref("ProductAdvanceInformation"),
        "webtool_disable_tracking": typed("boolean"),
        "meta_tags": typed("array"),
        "product_flags": ref("ProductFlags"),
        "product_dimension": ref("ProductDimension"),
        "product_identifiers": ref("ProductIdentifiers"),
        "webtool": ref("ProductWebtool"),
    }},
    "ProductLink": {"type": "object", "description": "A related, similar or up-sell product. A write takes `{\"id\": ...}`; a bare id in `up_sell_products` returns `200` and is dropped.", "properties": {
        "id": typed("integer", "The linked product's id."),
        "name": typed("string"),
        "url": typed("string"),
        "status": typed("string"),
        "sku": typed("string"),
        "in_stock": typed("boolean"),
        "price": typed("number"),
    }},
    "ProductBundle": {"type": "object", "description": "The bundle settings of a product that is a bundle.", "properties": {
        "price_fixed": typed("boolean"),
        "quantity_flexible": typed("boolean"),
        "items": typed("array"),
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
    "ProductReviewer": {"type": "object", "description": "Who wrote a review: the same `name` and `email` as the review.", "properties": {
        "name": typed("string"),
        "email": typed("string"),
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
        "product_id": typed("integer", "The same value as `productId`."),
        "reviewer": ref("ProductReviewer"),
        "comment": nullable("string", "The same text as `review`."),
        "created_at": typed("string", "The same date as `date`, ending in `Z`."),
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
        "compare_at_price": typed("number"),
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
    "ProductCategory": {"type": "object", "description": "One category the product is filed under, as `categories` lists it. [List categories](" + CATEGORIES_PAGE + ") returns the store's categories.", "properties": {
        "id": typed("integer", "The category's id."),
        "name": typed("string"),
        "in_trash": typed("boolean"),
        "parent_in_trash": typed("boolean"),
        "disposable": typed("boolean"),
    }},
    "ProductMediaImage": {"type": "object", "description": "One image of the product. [Add an image to a product's media](" + ADD_MEDIA_PAGE + ") and [Move a product's image](" + MOVE_IMAGE_PAGE + ") return it as the whole response, and [Set the order of a product's images](" + MEDIA_ORDER_PAGE + ") returns a list of them.", "properties": {
        "id": typed("integer", "The image's id."),
        "filename": typed("string"),
        "position": typed("integer"),
        "primary": typed("boolean"),
        "alt_text": typed("string"),
        "url": typed("string"),
        "thumbnail_url": typed("string"),
    }},
    "ProductMediaVideo": {"type": "object", "properties": {
        "id": typed("integer", "The video's id."),
        "filename": typed("string"),
        "position": typed("integer"),
        "url": typed("string"),
        "thumbnail_url": typed("string"),
    }},
    "ProductMedia": {"type": "object", "description": "The product's images and videos. A write names files the product already holds, by `id`; any other `id` is rejected with `400`.", "properties": {
        "images": array_of("ProductMediaImage"),
        "videos": array_of("ProductMediaVideo"),
        "specification_file": {"description": "`null` on every product read."},
    }},
    "ProductWeekdayWindow": {"type": "object", "description": "One day of the schedule. Times are `HH:mm`.", "properties": {
        "enabled": typed("boolean"),
        "full_day": typed("boolean"),
        "start_time": typed("string"),
        "end_time": typed("string"),
    }},
    "ProductScheduleWeekdays": {"type": "object", "description": "The seven days of the schedule, each always present.", "properties": {
        "monday": ref("ProductWeekdayWindow"),
        "tuesday": ref("ProductWeekdayWindow"),
        "wednesday": ref("ProductWeekdayWindow"),
        "thursday": ref("ProductWeekdayWindow"),
        "friday": ref("ProductWeekdayWindow"),
        "saturday": ref("ProductWeekdayWindow"),
        "sunday": ref("ProductWeekdayWindow"),
    }},
    "ProductSchedule": {"type": "object", "description": "When the product is available.", "properties": {
        "enabled": typed("boolean"),
        "type": typed("string", "`date_range` or `custom_schedule`."),
        "start_date": typed("string"),
        "end_date": typed("string"),
        "preset": typed("string", "`all_days`, `weekdays`, `business_hour`, `weekends` or `custom`."),
        "weekdays": ref("ProductScheduleWeekdays"),
    }},
    "ProductPasswordProtection": {"type": "object", "description": "The same values as `password_protected` and `password`. A password that is set reads `***`.", "properties": {
        "enabled": typed("boolean"),
        "password": typed("string"),
    }},
    "ProductAvailableForPurchase": {"type": "object", "description": "Availability in one block.", "properties": {
        "enabled": typed("boolean", "Whether the product is available."),
        "active": typed("boolean", "Whether the product is active in the administration."),
        "who_can_view": typed("string", "Who can buy the product. `selected` limits it to the customers and groups in `selected_customers`."),
        "selected_customers": ref("ProductSelectedCustomers"),
        "restrict_for_selected_customers": dict(ref("ProductSelectedCustomers"), description="Read-only."),
        "schedule": ref("ProductSchedule"),
        "password_protection": ref("ProductPasswordProtection"),
    }},
    "ProductAvailableForPurchaseInput": {"type": "object", "description": "The availability block to write. While `enabled` is `false`, a write to `who_can_view`, `schedule` or `password_protection` returns `200` and is not kept.", "properties": {
        "enabled": typed("boolean"),
        "active": typed("boolean"),
        "who_can_view": typed("string"),
        "selected_customers": ref("ProductSelectedCustomersInput"),
        "schedule": ref("ProductSchedule"),
        "password_protection": ref("ProductPasswordProtection"),
    }},
    "ProductOnSale": {"type": "object", "description": "The sale price.", "properties": {
        "enabled": typed("boolean"),
        "discounted_price": typed("number"),
        "amount_type": typed("string", "The same value as `on_sale_price_type`."),
    }},
    "ProductQuantityMultiple": {"type": "object", "description": "Order in multiples of `multiple_of`.", "properties": {
        "enabled": typed("boolean"),
        "multiple_of": typed("integer"),
    }},
    "ProductExpectToPay": {"type": "object", "description": "The expect-to-pay price.", "properties": {
        "enabled": typed("boolean"),
        "price": typed("number"),
    }},
    "ProductAdvancedPricing": {"type": "object", "description": "The advanced pricing switches.", "properties": {
        "enabled": typed("boolean"),
        "quantity_multiple": ref("ProductQuantityMultiple"),
        "expect_to_pay": ref("ProductExpectToPay"),
        "call_for_price": typed("boolean"),
    }},
    "ProductPricing": {"type": "object", "description": "Prices in one block. On a create, `base_price` here is accepted in place of the top-level `base_price`.", "properties": {
        "base_price": typed("number"),
        "cost_price": typed("number"),
        "rrp_price": typed("number", "The recommended retail price."),
        "on_sale": ref("ProductOnSale"),
        "advanced_pricing": ref("ProductAdvancedPricing"),
    }},
    "ProductInventoryTracking": {"type": "object", "description": "Stock tracking.", "properties": {
        "enabled": typed("boolean"),
        "available_stock": typed("integer"),
        "low_stock_level": typed("integer"),
        "suppliers": {"type": "array", "description": "The supplier ids you wrote."},
    }},
    "ProductCombinedStockLimit": {"type": "object", "description": "The combined stock selling limit.", "properties": {
        "enabled": typed("boolean"),
        "units": typed("integer"),
    }},
    "ProductInventory": {"type": "object", "description": "Stock settings in one block.", "properties": {
        "tracking": ref("ProductInventoryTracking"),
        "combined_stock_limit": ref("ProductCombinedStockLimit"),
        "preorder": typed("boolean", "Whether the product can be pre-ordered."),
    }},
    "ProductOrdering": {"type": "object", "description": "The order quantity limits.", "properties": {
        "min_quantity": typed("integer"),
        "max_quantity": typed("integer", "`0` means no maximum."),
    }},
    "ProductRestriction": {"type": "object", "description": "A price or purchase restriction. Write only `mode`: `enabled` is read-only, and a value you send in `customers` returns `200` and is not kept.", "properties": {
        "enabled": typed("boolean", "Read-only."),
        "mode": typed("string"),
        "customers": {"type": "array"},
    }},
    "ProductRestrictions": {"type": "object", "description": "The same values as `restrict_price_for` and `restrict_purchase_for`, in one block. `enabled` and `display_only` are read-only.", "properties": {
        "enabled": typed("boolean", "Read-only."),
        "price": ref("ProductRestriction"),
        "purchase": ref("ProductRestriction"),
        "display_only": typed("boolean", "Read-only."),
    }},
    "ProductPriceIncludesTax": {"type": "object", "description": "Whether `base_price` includes tax, and how it is rounded.", "properties": {
        "enabled": typed("boolean"),
        "base_price_rounding": typed("string"),
    }},
    "ProductTax": {"type": "object", "description": "The product's tax settings in one block.", "properties": {
        "enabled": typed("boolean", "`true` when the product overrides the store's default tax settings."),
        "exempt": typed("boolean"),
        "custom_tax_profile": dict(ref("ProductNamedReference"), description="The custom tax profile. In a write, send its id or `{\"id\": ...}`."),
        "message": typed("string"),
        "show_price_with_tax": typed("boolean"),
        "price_includes_tax": ref("ProductPriceIncludesTax"),
    }},
    "ProductShipping": {"type": "object", "description": "The product's shipping profile.", "properties": {
        "enabled": typed("boolean", "`true` while a profile is set. Read-only."),
        "profile": dict(ref("ProductNamedReference"), description="The shipping profile. An update takes its id or `{\"id\": ...}`; a create drops it."),
    }},
    "ProductLinks": {"type": "object", "description": "The API paths of the product and its sub-paths. Read-only.", "properties": {
        "self": typed("string"),
        "variations": typed("string"),
        "stock": typed("string"),
        "reviews": typed("string"),
    }},
    "ProductPagination": {"type": "object", "properties": {
        "total": typed("integer", "The number of products that match."),
        "limit": typed("integer", "The page size the store applied."),
        "offset": typed("integer", "The number of products skipped before this page."),
        "has_previous": typed("boolean", "`true` when products come before this page."),
        "has_next": typed("boolean", "`true` when more products follow this page."),
    }},
    "ProductPage": {"type": "object", "description": "One page of the product list.", "properties": {
        "products": array_of("Product", "The products on this page, each the full record."),
        "pagination": ref("ProductPagination"),
        "field_metadata": ref("ProductFieldMetadata"),
    }},
    "ProductInput": {"type": "object", "description": "The body of `PUT` and `PATCH`. Send these fields at the top level of the body, not inside `product`. A `PUT` must include `name`, `sku`, `base_price`, `product_type`, `available`, `is_on_sale`, `available_on_date_range`, `available_on_weekdays`, `available_for` and `selected_customers`. Apart from those, only the fields you send change, inside nested blocks too. `product_url`, `links` and `restrict_for_selected_customers` are read-only, and a value you send in `updated_by` returns `200` and is not kept. A read-only field from [Retrieve a product](" + RETRIEVE_PAGE + ") is accepted when its value is unchanged and rejected with `400` and the reason `read_only_field` when it differs. `status` and `reviews` are rejected with the reason `unknown_field`. `updated_at`, `version`, `last_updated_on` and `last_updated_by` are ignored.", "properties": {
        "name": typed("string"),
        "sku": typed("string"),
        "transaction_no": typed("string", "A transaction number. A create stores it, unless you also send an `X-Transaction-No` header with a different value: the header's value is stored instead. `PUT` and `PATCH` store it only on a product that has no `transaction_no`; a product that has one keeps it, and the value you send is dropped with no error."),
        "heading": typed("string"),
        "product_type": typed("string"),
        "custom_type": typed("string"),
        "is_virtual": typed("boolean"),
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
        "parents": {"type": "array", "items": {"oneOf": [{"type": "integer"}, {"type": "object", "properties": {"id": typed("integer", "The category's `id`.")}}]}, "description": "The `id` of each category to file the product under, as a number or as `{\"id\": <category id>}`."},
        "related_products": typed("array"),
        "similar_products": typed("array"),
        "tags": typed("array"),
        "preorder_enabled": typed("boolean"),
        "selected_customers": dict(ref("ProductSelectedCustomersInput"), description="The customers and groups the product is available to, as ids."),
        "virtual": typed("boolean", "The same value as `is_virtual`."),
        "summary": typed("string", "The same text as `product_summary`."),
        "description": typed("string", "The same text as `product_description`."),
        "categories": {"type": "array", "items": {"oneOf": [{"type": "integer"}, {"type": "object", "properties": {"id": typed("integer", "The category's `id`.")}}]}, "description": "The `id` of each category, as a number or as `{\"id\": <category id>}`. `[]` returns `200` and changes nothing."},
        "up_sell_products": array_of("ProductLink", "The up-sell products, as `{\"id\": ...}` records. A list of bare ids returns `200` and leaves `up_sell_products` empty."),
        "media": ref("ProductMedia"),
        "available_for_purchase": ref("ProductAvailableForPurchaseInput"),
        "pricing": ref("ProductPricing"),
        "inventory": ref("ProductInventory"),
        "ordering": ref("ProductOrdering"),
        "restrictions": ref("ProductRestrictions"),
        "tax": ref("ProductTax"),
        "shipping": ref("ProductShipping"),
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
    "ProductError": {"type": "object", "description": "Rejections return this shape, except a `PATCH` body wrapped in `product`, which returns `ProductValidationError`. A method a path does not support is rejected too: `HEAD` on `/api/v4/admin/products`, on a product and on a product's `reviews` returns `404`, although a product's `Allow` header lists `HEAD`; `HEAD`, `POST` and `OPTIONS` on a product's `stock` return `404` with the message `No such endpoint: <METHOD> /api/v4/admin/products/<product_id>/stock`; and `GET` on `stock/locations/{inventory_location_id}` returns `405` with the reason `method_not_allowed`.", "properties": {"error": {"type": "object", "properties": {
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

SCHEMAS["ProductCreateInput"] = {"type": "object", "required": ["name", "base_price"], "description": "The body of a create. Send these fields at the top level of the body, not inside `product`: a body wrapped in `product` is rejected with `400`. `name` and `base_price` are required, and `sku` must not belong to another product.", "properties": SCHEMAS["ProductInput"]["properties"]}

SCHEMAS["ProductReviewInput"] = {"type": "object", "required": ["name", "email", "rating"], "description": "One review to add. Unknown keys, such as `title`, are accepted and dropped.", "properties": {
    "name": typed("string", "Required. The reviewer's name."),
    "email": typed("string", "Required. The reviewer's email address. A review with an `email` the product already has a review from replaces that review, which keeps its `id`, with no error."),
    "rating": {"type": "number", "minimum": 1, "maximum": 5, "description": "Required. From `1` to `5`. It reads back as a decimal number, such as `5.0`."},
    "review": typed("string", "The review's text."),
    "comment": typed("string", "Another name for `review`. It reads back as `review`."),
    "status": typed("string", "`approved` is kept. Any other value, or none, is stored as `pending`."),
    "dateCreated": typed("string", "The review's date, as `yyyy-MM-ddTHH:mm:ss`. It reads back as `date`. Sending `date` instead is rejected with `400`."),
}}

SCHEMAS["ProductReviewsImportInput"] = {"type": "object", "required": ["product"], "description": "Wrap the reviews in `product`. Send `transaction_no` beside `product`, not inside it.", "properties": {
    "product": {"type": "object", "required": ["reviews"], "properties": {
        "reviews": {"type": "array", "minItems": 1, "items": ref("ProductReviewInput"), "description": "Required and not empty. The reviews to add."},
    }},
    "transaction_no": typed("string", "Optional. A transaction number to tag the reviews with. An `X-Transaction-No` header with a different value wins over it."),
}}

SCHEMAS["ProductReviews"] = {"type": "object", "description": "Every review the product has, oldest first.", "properties": {
    "reviews": array_of("ProductReview", "Every review the product has, the ones you just added last."),
}}

SCHEMAS["ProductValidationError"] = {"type": "object", "description": "The rejection a `PATCH` body wrapped in `product` returns. Every other rejection returns `ProductError`.", "properties": {
    "request_id": typed("string", "Identifies this request."),
    "status": typed("integer", "`400`."),
    "code": typed("string", "`validation_error`."),
    "message": typed("string", "What went wrong."),
    "errors": {"type": "array", "description": "One entry per rejected field.", "items": {"type": "object", "properties": {
        "field": typed("string", "The field that was rejected."),
        "code": typed("string", "Why it was rejected, such as `unknown_field`."),
    }}},
}}

SCHEMAS["ProductCount"] = {"type": "object", "properties": {
    "total": typed("integer", "The number of products that match the filters."),
    "count": typed("integer", "The same number as `total`."),
}}

SCHEMAS["ProductSkuHolder"] = {"type": "object", "description": "The product that holds the SKU.", "properties": {
    "id": typed("integer", "The holder's `id`. A variant's SKU names the variant's own product, not the product it belongs to."),
    "name": typed("string"),
    "status": typed("string", "`active` or `trashed`."),
}}

SCHEMAS["ProductSkuCheck"] = {"type": "object", "properties": {
    "available": typed("boolean", "`true` when no product holds the SKU."),
    "is_exist": typed("boolean", "`true` when a product holds the SKU."),
    "product": {"oneOf": [ref("ProductSkuHolder"), {"type": "null"}], "description": "The product that holds the SKU, or `null` when the SKU is free."},
    "id": typed("integer", "The holder's `id`. Left out when the SKU is free."),
}}

SCHEMAS["ProductSpecial"] = {"type": "object", "description": "One product of the selection.", "properties": {
    "id": typed("integer", "The product's `id`. Pass it as `product_id` in a path."),
    "sku": typed("string"),
    "name": typed("string"),
    "image": typed("string", "The address of the product's image."),
    "base_price": typed("number"),
    "is_on_sale": typed("boolean"),
    "on_sale_amount_type": typed("string"),
    "effective_price": typed("number"),
    "actual_base_price": typed("number"),
    "on_sale_amount": typed("number"),
    "expect_to_pay_price": typed("number"),
    "expect_to_pay_price_with_tax": typed("number"),
    "tax_exclusive_base_price": typed("number"),
    "tax_exclusive_sale_price": typed("number"),
    "tax": typed("number"),
    "previous_price_to_display": nullable("number", "`null` when the product has no previous price."),
    "actual_price_to_display": typed("number"),
    "sale_price": typed("number"),
    "updated": typed("string", "When the product last changed, as `yyyy-MM-ddTHH:mm:ss`."),
    "url": typed("string", "The address of the product's page."),
    "summary": typed("string"),
    "description": typed("string"),
}}

SCHEMAS["ProductSpecialPage"] = {"type": "object", "properties": {
    "status": typed("string", "`success`. Only a per-customer selection with no products returns it."),
    "total": typed("integer", "The number of products in the selection."),
    "max": typed("integer", "The page size applied: the `max` you sent, or `10`."),
    "offset": typed("integer", "The number of products skipped before this page."),
    "products": array_of("ProductSpecial", "The products on this page."),
    "pagination": ref("ProductPagination"),
}}

SCHEMAS["ProductsBulkDeleteInput"] = {"type": "object", "required": ["ids"], "description": "Send `ids` at the top level of the body, with no wrapper. `product_ids` is rejected.", "properties": {
    "ids": {"type": "array", "minItems": 1, "items": {"type": "integer"}, "description": "Required and not empty. The `id` of each product to move to the trash."},
}}

SCHEMAS["ProductBulkDeleteError"] = {"type": "object", "properties": {
    "id": typed("integer", "The `id` that could not be moved to the trash."),
    "reason": typed("string", "Why, such as `not_found`."),
}}

SCHEMAS["ProductsBulkDeleteResult"] = {"type": "object", "properties": {
    "deleted": typed("integer", "The number of products moved to the trash."),
    "failed": typed("integer", "The number of `id` values that could not be moved."),
    "errors": array_of("ProductBulkDeleteError", "One entry per failure, or `[]`."),
}}

SCHEMAS["ProductReviewList"] = {"type": "object", "properties": {
    "reviews": array_of("ProductReview", "The reviews on this page, or `[]`."),
    "pagination": ref("ProductReviewPagination"),
}}

SCHEMAS["ProductReviewPagination"] = {"type": "object", "properties": {
    "total": typed("integer", "The number of reviews the product has."),
    "limit": typed("integer", "The page size applied: the `limit` you sent, or `20`."),
    "offset": typed("integer", "The number of reviews skipped before this page."),
    "has_previous": typed("boolean", "`true` when reviews come before this page."),
    "has_next": typed("boolean", "`true` when more reviews follow this page."),
}}

SCHEMAS["ProductReviewPatchInput"] = {"type": "object", "description": "Send these fields at the top level of the body, with no wrapper. Only the fields you send change.", "properties": {
    "status": {"type": "string", "enum": ["pending", "approved"], "description": "`pending` or `approved`. `rejected` is rejected with `400` and the reason `invalid_enum`."},
    "rating": {"type": "number", "minimum": 1, "maximum": 5, "description": "The rating, `1` to `5`."},
    "comment": typed("string", "The review's text. It changes `review` too."),
}}

SCHEMAS["ProductInventoryStockInput"] = {"type": "object", "properties": {
    "track_inventory": typed("boolean", "Whether the product tracks stock."),
    "available_stock": typed("integer", "The units available."),
    "low_level_stock": typed("integer", "The low stock level."),
}}

SCHEMAS["ProductInventoryInput"] = {"type": "object", "required": ["product"], "description": "Wrap the settings in `product.product_pricing_and_stock`.", "properties": {
    "product": {"type": "object", "required": ["product_pricing_and_stock"], "properties": {
        "product_pricing_and_stock": ref("ProductInventoryStockInput"),
    }},
}}

SCHEMAS["ProductInventoryResult"] = {"type": "object", "properties": {
    "status": typed("string", "`success`."),
    "message": typed("string", "`Inventory has been updated successfully`."),
    "transaction_no": nullable("string", "The product's transaction number from before this write, or `null`."),
}}

SCHEMAS["ProductImageFileInput"] = {"type": "object", "required": ["filename", "base64"], "properties": {
    "filename": typed("string", "The file name, such as `front.png`."),
    "base64": typed("string", "The file's bytes as base64 text."),
}}

SCHEMAS["ProductImageUploadInput"] = {"type": "object", "required": ["product"], "description": "Wrap the files in `product.image_and_video.images`. Send JSON: a multipart body is rejected with `415`.", "properties": {
    "product": {"type": "object", "required": ["image_and_video"], "properties": {
        "image_and_video": {"type": "object", "required": ["images"], "properties": {
            "images": {"type": "array", "minItems": 1, "items": ref("ProductImageFileInput"), "description": "The images to store. Send several to store them in one call."},
        }},
    }},
}}

SCHEMAS["ProductMediaUploaded"] = {"type": "object", "properties": {
    "product": ref("ProductImageAndVideo"),
    "transaction_no": nullable("string", "The product's transaction number, or `null`."),
}}

SCHEMAS["ProductMediaUploadInput"] = {"type": "object", "required": ["type", "filename", "content"], "description": "Send these fields at the top level of the body, with no wrapper.", "properties": {
    "type": {"type": "string", "enum": ["images"], "description": "`images`. `videos` and `specification_file` are rejected with `400` and the reason `not_supported`."},
    "filename": typed("string", "The file name, such as `side.png`."),
    "content": typed("string", "The file's bytes as base64 text, or a `data:image/png;base64,...` address."),
    "position": typed("integer", "Optional. The image's place among the product's images, counted from `1`."),
}}

SCHEMAS["ProductMediaOrderInput"] = {"type": "object", "required": ["type", "ids"], "description": "Send these fields at the top level of the body, with no wrapper.", "properties": {
    "type": {"type": "string", "enum": ["images"], "description": "`images`."},
    "ids": {"type": "array", "minItems": 1, "items": {"type": "integer"}, "description": "The `id` of every image of the product, each once, in the order you want. The first becomes the `primary` image. Any other set of `id` values is rejected with `400` and the reason `invalid_set`."},
}}

SCHEMAS["ProductMediaOrder"] = {"type": "object", "properties": {
    "images": array_of("ProductMediaImage", "The product's images in the new order."),
}}

SCHEMAS["ProductMediaImagePatchInput"] = {"type": "object", "required": ["position"], "description": "Send `position` at the top level of the body, with no wrapper. It is the only field the call takes.", "properties": {
    "position": {"type": "integer", "minimum": 1, "description": "The image's new place among the product's images, counted from `1`. The image at position `1` is `primary`."},
}}

SCHEMAS["ProductSeoAdvancedSettings"] = {"type": "object", "description": "The robots and canonical URL settings.", "properties": {
    "enabled": typed("boolean"),
    "robots_meta": typed("string"),
    "canonical_url": nullable("string", "`null` until set."),
}}

SCHEMAS["ProductSeoGoogleAnalyticsEvents"] = {"type": "object", "description": "Which Google Analytics events the product page sends.", "properties": {
    "enabled": typed("boolean"),
    "view_item": typed("boolean"),
    "view_item_list": typed("boolean"),
    "view_cart": typed("boolean"),
    "add_to_wish_list": typed("boolean"),
    "remove_from_cart": typed("boolean"),
    "begin_checkout": typed("boolean"),
    "add_shipping_info": typed("boolean"),
    "add_payment_info": typed("boolean"),
    "purchase": typed("boolean"),
}}

SCHEMAS["ProductSeoGoogleAnalytics"] = {"type": "object", "description": "Google Analytics on the product page.", "properties": {
    "enabled": typed("boolean"),
    "measurement_id": nullable("string", "`null` until set."),
    "events": ref("ProductSeoGoogleAnalyticsEvents"),
}}

SCHEMAS["ProductSeoFacebookPixelEvents"] = {"type": "object", "description": "Which Facebook Pixel events the product page sends.", "properties": {
    "enabled": typed("boolean"),
    "search": typed("boolean"),
    "add_to_cart": typed("boolean"),
    "add_to_wish_list": typed("boolean"),
    "initiate_checkout": typed("boolean"),
    "add_payment_info": typed("boolean"),
    "purchase": typed("boolean"),
}}

SCHEMAS["ProductSeoFacebookPixel"] = {"type": "object", "description": "The Facebook Pixel on the product page.", "properties": {
    "enabled": typed("boolean"),
    "pixel_id": nullable("string", "`null` until set."),
    "events": ref("ProductSeoFacebookPixelEvents"),
}}

SCHEMAS["ProductSeoGoogleAds"] = {"type": "object", "description": "The Google Ads conversion the product page reports.", "properties": {
    "conversion_id": nullable("string", "`null` until set."),
    "conversion_label": nullable("string", "`null` until set."),
}}

SCHEMAS["ProductSeoAnalytics"] = {"type": "object", "description": "The product page's analytics settings.", "properties": {
    "enabled": typed("boolean"),
    "platform": typed("string"),
    "google_analytics": ref("ProductSeoGoogleAnalytics"),
    "facebook_pixel": ref("ProductSeoFacebookPixel"),
    "google_ads": ref("ProductSeoGoogleAds"),
}}

SCHEMAS["ProductSeoCode"] = {"type": "object", "description": "One custom code block and whether it is on.", "properties": {
    "enabled": typed("boolean"),
    "code": nullable("string", "`null` until set."),
}}

SCHEMAS["ProductSeoCustomCode"] = {"type": "object", "description": "The custom code added to the product page's header and footer.", "properties": {
    "header": ref("ProductSeoCode"),
    "footer": ref("ProductSeoCode"),
}}

SCHEMAS["ProductSeoSocialCard"] = {"type": "object", "description": "The title, description and image one network shows for the product.", "properties": {
    "title": nullable("string", "`null` until set."),
    "description": nullable("string", "`null` until set."),
    "image_url": nullable("string", "`null` until set."),
}}

SCHEMAS["ProductSeoSocial"] = {"type": "object", "description": "The product's social card, and one card for each network.", "properties": {
    "title": nullable("string", "`null` until set."),
    "description": nullable("string", "`null` until set."),
    "image_url": nullable("string", "`null` until set."),
    "facebook": ref("ProductSeoSocialCard"),
    "twitter": ref("ProductSeoSocialCard"),
    "linkedin": ref("ProductSeoSocialCard"),
}}

SCHEMAS["ProductSeoAiVisibility"] = {"type": "object", "description": "What the product offers AI search. Each field is `null` until it is set.", "properties": {
    "structured_attributes": {"description": "`null` until set."},
    "product_faq": {"description": "`null` until set."},
    "citability_score": {"description": "`null` until set."},
    "json_ld": {"description": "`null` until set."},
}}

SCHEMAS["ProductSeo"] = {"type": "object", "description": "A product's SEO settings.", "properties": {
    "url_handle": typed("string", "The product's URL slug."),
    "title": nullable("string", "The page title, or `null` until set."),
    "description": nullable("string", "The page description, or `null` until set."),
    "advanced_settings": ref("ProductSeoAdvancedSettings"),
    "analytics": ref("ProductSeoAnalytics"),
    "custom_code": ref("ProductSeoCustomCode"),
    "social": ref("ProductSeoSocial"),
    "ai_visibility": ref("ProductSeoAiVisibility"),
}}

SCHEMAS["ProductStockTracking"] = {"type": "object", "description": "Whether the product tracks stock, its stock figure and its low-stock level.", "properties": {
    "enabled": typed("boolean", "Whether the product tracks stock."),
    "available_stock": typed("integer", "The units available."),
    "low_stock_level": typed("integer", "The low-stock level."),
}}

SCHEMAS["ProductStockSummary"] = {"type": "object", "description": "The product's stock after the change.", "properties": {
    "tracking": ref("ProductStockTracking"),
    "multi_location_enabled": typed("boolean"),
    "locations": array_of("ProductStockLocation", "One row per inventory location the product is assigned to, or `[]` when it has none."),
    "variations": array_of("ProductStockVariation", "One entry per variant, on a product with variations."),
}}

SCHEMAS["ProductStockAdjustmentUser"] = {"type": "object", "description": "The admin who made a stock change.", "properties": {
    "id": typed("integer", "The admin's `id`."),
    "name": typed("string"),
}}

SCHEMAS["ProductStockAdjustment"] = {"type": "object", "description": "One stock change.", "properties": {
    "id": typed("integer", "The adjustment's `id`."),
    "delta": typed("integer", "The new stock figure minus the old one."),
    "note": typed("string", "The note you sent, or `via API`."),
    "transaction_no": nullable("string", "`null` on every row [List a product's stock adjustments](" + ADJUSTMENTS_PAGE + ") returns, also for a change you sent with a `transaction_no`."),
    "created_by": ref("ProductStockAdjustmentUser"),
    "created_at": typed("string", "When the change was made."),
}}

SCHEMAS["ProductStockPatchInput"] = {"type": "object", "description": "Send these fields at the top level of the body, with no wrapper, and at least one of them. A wrapper, or `available_stock` outside `tracking`, is rejected with `400` and the reason `unknown_field`.", "properties": {
    "tracking": {"type": "object", "description": "The tracking fields to change. They are merged into the product's tracking.", "properties": {
        "enabled": typed("boolean", "Whether the product tracks stock."),
        "available_stock": typed("integer", "The units available."),
        "low_stock_level": typed("integer", "The low-stock level."),
    }},
    "locations": {"type": "array", "items": ref("ProductStockLocationInput"), "description": "Stock per location, with rows in the form [Set a product's stock](" + SET_STOCK_PAGE + ") takes."},
    "note": typed("string", "The note to record on the adjustment."),
    "transaction_no": typed("string", "The transaction number to record on the adjustment."),
}}

SCHEMAS["ProductStockPatchResult"] = {"type": "object", "properties": {
    "stock": ref("ProductStockSummary"),
    "adjustment": {"oneOf": [ref("ProductStockAdjustment"), {"type": "null"}], "description": "The change the store recorded, or `null` when the stock figure did not change."},
}}

SCHEMAS["ProductStockAdjustmentPage"] = {"type": "object", "properties": {
    "adjustments": array_of("ProductStockAdjustment", "The adjustments on this page, newest first."),
    "pagination": ref("ProductPagination"),
}}
