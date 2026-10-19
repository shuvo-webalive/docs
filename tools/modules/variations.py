"""The Variations endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Variations"
SLUG = "variations"
BASE = "/admin/variations"
ICON = "swatchbook"

OVERVIEW_DESCRIPTION = "List, create, replace, update and delete variation types and their options, and list, import and update the variants of a product."
INTRO = "The Variations API has twelve endpoints, and you can call every one from all seven SDKs. Variation type paths start with `/api/v4/admin/variations`, and product variant paths start with `/api/v4/admin/products/{product_id}/variations`."

PRODUCT_BASE = "/admin/products/{product_id}/variations"

LIST_PAGE = "/api-reference/variations/list-variation-types"
RETRIEVE_PAGE = "/api-reference/variations/retrieve-a-variation-type"
REPLACE_PAGE = "/api-reference/variations/replace-a-variation-type"
UPDATE_PAGE = "/api-reference/variations/update-a-variation-type"
DELETE_PAGE = "/api-reference/variations/delete-a-variation-type"
DELETE_OPTION_PAGE = "/api-reference/variations/delete-a-variation-option"
PRODUCT_VARIANTS_PAGE = "/api-reference/variations/list-a-products-variants"
BULK_PAGE = "/api-reference/variations/update-a-products-variants"
IMPORT_PAGE = "/api-reference/variations/import-a-products-variants"
CREATE_PRODUCT_PAGE = "/api-reference/products/create-a-product"

WARNING = (
    "**Replacing a variation type deletes every option you leave out of the body.** `PUT` on a type\n"
    "  keeps only the options you send: an option sent with its `id` is changed, an option sent without\n"
    "  an `id` is added, and every other option is deleted. To change or add options without deleting any,\n"
    "  use [Update a variation type](" + UPDATE_PAGE + "), which changes only what you send."
)

NOTES = [
    "**Wrap every variation type write in `variation`.** Create, replace and update all take\n"
    "  `{\"variation\": {...}}`. A bare record is rejected with `400`: each top-level key is reported with\n"
    "  the reason `unknown_field`, and `variation` with the reason `required`.\n"
    "  [Update a product's variants](" + BULK_PAGE + ") and [Import a product's variants](" + IMPORT_PAGE + ")\n"
    "  are the opposite: send their fields at the top level of the body, with no wrapper.",
    "**Delete a variation type with `cascade=true`.** A type you create always has at least one option,\n"
    "  and you cannot delete a type's last option on its own. Without `cascade=true`,\n"
    "  [Delete a variation type](" + DELETE_PAGE + ") rejects a type that has options with `409` and the\n"
    "  message `This variation type still has N option(s).` With `cascade=true`, the type and its options\n"
    "  are deleted together. A type that a product's variants use cannot be deleted, even with `cascade=true`\n"
    "  and even after that product is moved to the trash: the call is rejected with `409`.",
    "**Importing variants can add options to the store's variation types.**\n"
    "  [Import a product's variants](" + IMPORT_PAGE + ") matches each `product_key` to the `name` of a\n"
    "  variation type and each variant `key` to that type's option labels. A label the type does not have\n"
    "  yet is added to the type itself, for the whole store. To add no option, use labels the type already\n"
    "  has: [List variation types](" + LIST_PAGE + ") returns them.",
    "**`variation_ids` takes each variant's `variation_id`, not a variation type's `id`.** Each variant that\n"
    "  [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns has its own `variation_id`.\n"
    "  Send those values in `variation_ids` to [Update a product's variants](" + BULK_PAGE + "). A variant\n"
    "  of another product is rejected with `400` and nothing is written.",
    "**On a product whose prices include tax, the variant prices you read are net of tax.**\n"
    "  [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns each variant's `base_price` and\n"
    "  `sale_price` divided by the tax rate and rounded to the cent: a stored `90.99` reads `82.72`.\n"
    "  [Update a product's variants](" + BULK_PAGE + ") stores the price you send as it is. A price you read\n"
    "  and write back is therefore not the price that was stored: send the price including tax.",
    "**The listing returns 20 types per call unless you send `limit`.** `limit` takes `1` to `100`. To get\n"
    "  more, send a higher `offset`, or the next `page`, while `pagination.has_next` is `true`. The listing\n"
    "  accepts only `search`, `standard`, `limit`, `offset`, `page` and `field_metadata`: any other query\n"
    "  parameter, such as `q` or `sort`, is rejected with `400` and the reason `unknown_parameter`.",
]

VARIATION_ID = {
    "name": "variation_id",
    "in": "path",
    "required": True,
    "description": "The variation type's `id`, from a listing or from the response to creating the type.",
    "schema": {"type": "integer", "example": 15},
}

VARIATION_OPTION_ID = {
    "name": "variation_option_id",
    "in": "path",
    "required": True,
    "description": "The option's `id`, from the variation type's `options` list. The option must belong to the type you pass as `variation_id`.",
    "schema": {"type": "integer", "example": 204},
}

PRODUCT_ID = {
    "name": "product_id",
    "in": "path",
    "required": True,
    "description": "The product's `id`. [Create a product](" + CREATE_PRODUCT_PAGE + ") returns it as `product.id`.",
    "schema": {"type": "integer", "example": 4321},
}

SEARCH = {"name": "search", "in": "query", "description": "Keeps only types whose `name` contains this text, in any letter case. It does not search option labels.", "schema": {"type": "string", "example": "size"}}
STANDARD = {"name": "standard", "in": "query", "description": "Keeps only types of this kind: `text`, `color` or `image`, in any letter case. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": ["text", "color", "image"], "example": "text"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of types per page, from `1` to `100`. Defaults to `20`. `pagination.limit` shows the value applied. `0`, values above `100` and text such as `abc` are rejected with `400` and the message `must be a whole number from 1 to 100`. The reason is `out_of_range` for `0` and values above `100`, and `invalid_integer` for text.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of types to skip, `0` or more. Do not send it with `page`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit`. Sending both `page` and `offset` is rejected with `400` and the reason `conflicting_params`.", "schema": {"type": "integer", "example": 2}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to also get `field_metadata`, which describes each field of a variation type and of an option: its type, its limits, and whether it is read-only. Accepts `true`, `false`, `1` and `0`; any other value is rejected with `400` and the reason `invalid_boolean`.", "schema": {"type": "boolean", "example": True}}
CASCADE = {"name": "cascade", "in": "query", "description": "Send `true` or `1` to delete the type's options with it. Without it, or with `false` or `0`, a type that has options is rejected with `409`. Any other value is rejected with `400` and the reason `invalid_boolean`.", "schema": {"type": "boolean", "example": True}}
TRANSACTION_NO = {"name": "X-Transaction-No", "in": "header", "description": "Optional. A transaction number to tag the imported variants with, such as `IMPORT-2026-10-18`. In the SDKs, pass it as `transaction_no`. You can send `transaction_no` in the body beside `variations` instead. When you send both with different values, the header's value is stored and the body's is lost, with no error. [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") does not show it. `GET /api/v4/admin/products/{product_id}/variations/{variation_id}` returns it as the variant's `transaction_no`, and [Retrieve a transaction](/api-reference/transactions/retrieve-a-transaction) counts the variant under `product_variation`.", "schema": {"type": "string", "example": "IMPORT-2026-10-18"}}
RESPONSE_MODE = {"name": "response", "in": "query", "description": "`slim` (the default) returns each updated variant's `id` and `name`. `full` returns fourteen fields for each one. Any other value is rejected with `400`, the reason `invalid_enum` and the message `must be one of slim, full`.", "schema": {"type": "string", "enum": ["slim", "full"], "example": "full"}}

ERROR_REF = {"$ref": "#/components/schemas/VariationError"}
ROW_REF = {"$ref": "#/components/schemas/Variation"}
INPUT_REF = {"$ref": "#/components/schemas/VariationInput"}
FIELD_METADATA_REF = {"$ref": "#/components/schemas/VariationFieldMetadata"}

ROW_RESPONSE = {"type": "object", "properties": {"variation": ROW_REF}}
ROW_WITH_METADATA_RESPONSE = {"type": "object", "properties": {
    "variation": ROW_REF,
    "field_metadata": dict(FIELD_METADATA_REF, description="Only when you send `field_metadata=true`."),
}}
WRITE_BODY = {"type": "object", "required": ["variation"], "properties": {"variation": INPUT_REF}}

NOT_FOUND_RESPONSE = {"description": "No variation type has that `variation_id`. The message is `Variation not found`.", "schema": ERROR_REF}

SAMPLE_ROWS = [
    {"id": 12, "name": "Size", "standard": "text", "disposable": False, "options": [
        {"id": 101, "label": "Small", "value": "S", "order": 1, "default": False, "image": None},
        {"id": 102, "label": "Medium", "value": "M", "order": 2, "default": True, "image": None},
    ]},
    {"id": 14, "name": "Shoe Size", "standard": "text", "disposable": False, "options": [
        {"id": 131, "label": "UK 8", "value": "8", "order": 1, "default": False, "image": None},
        {"id": 132, "label": "UK 9", "value": "9", "order": 2, "default": False, "image": None},
    ]},
]

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"variation": {"name": "Shirt Size", "standard": "text", "options": [
    {"label": "Small", "value": "S", "order": 1, "default": True},
    {"label": "Medium", "value": "M", "order": 2},
]}}
CREATED_ROW = {"id": 15, "name": "Shirt Size", "standard": "text", "disposable": False, "options": [
    {"id": 201, "label": "Small", "value": "S", "order": 1, "default": True, "image": None},
    {"id": 202, "label": "Medium", "value": "M", "order": 2, "default": False, "image": None},
]}

REPLACE_BODY = {"variation": {"name": "Shirt Size", "options": [
    {"id": 201, "label": "Small", "value": "S", "order": 1, "default": True},
    {"label": "Large", "value": "L", "order": 3},
]}}
REPLACED_ROW = {"id": 15, "name": "Shirt Size", "standard": "text", "disposable": False, "options": [
    {"id": 201, "label": "Small", "value": "S", "order": 1, "default": True, "image": None},
    {"id": 203, "label": "Large", "value": "L", "order": 3, "default": False, "image": None},
]}

PATCH_BODY = {"variation": {"options": [
    {"id": 201, "label": "Petite"},
    {"label": "Extra Large", "value": "XL", "order": 4},
]}}
PATCHED_ROW = {"id": 15, "name": "Shirt Size", "standard": "text", "disposable": False, "options": [
    {"id": 201, "label": "Petite", "value": "S", "order": 1, "default": True, "image": None},
    {"id": 203, "label": "Large", "value": "L", "order": 3, "default": False, "image": None},
    {"id": 204, "label": "Extra Large", "value": "XL", "order": 4, "default": False, "image": None},
]}

BULK_BODY = {"variation_ids": [91], "available": True, "available_stock": 12, "min_order_quantity": 1, "max_order_quantity": 5}
BULK_SLIM_RESULT = {"status": "success", "message": "1 variations updated", "updated": [{"id": 91, "name": "Cotton T-Shirt"}], "failed": []}

IMPORT_BODY = {"variations": [{"product_key": "Size", "variants": [
    {"key": "Small", "name": "Cotton T-Shirt Small", "sku": "TSHIRT-001-S", "pricing": {"base_price": 25.0}},
    {"key": "Medium", "name": "Cotton T-Shirt Medium", "sku": "TSHIRT-001-M", "pricing": {"base_price": 25.0}},
]}]}
IMPORT_RESULT = {"status": "success", "message": "2 of 2 variants imported successfully", "total_variants": 2}

ENDPOINTS = [
    {
        "key": "list_variations",
        "slug": "list-variation-types",
        "title": "List variation types",
        "method": "GET",
        "path": BASE,
        "summary": "Returns variation types with their options, by ascending `id`, 20 per call unless you send `limit`.",
        "description": "Returns the variation types in ascending order of each type's `id`, 20 per call unless you send `limit`. Each type comes with every one of its options. `pagination` gives the number of matching types in `total`, and `has_next` is `true` while another page follows. Send `search` to keep only types whose `name` contains that text, and `standard` to keep only one kind of type. Any query parameter not listed here is rejected with `400`.",
        "parameters": [SEARCH, STANDARD, LIMIT, OFFSET, PAGE, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The variation types on this page in `variations`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. With `field_metadata=true`, a `field_metadata` key is added between them. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "variations": {"type": "array", "items": ROW_REF},
                    "field_metadata": dict(FIELD_METADATA_REF, description="Only when you send `field_metadata=true`."),
                    "pagination": {"$ref": "#/components/schemas/VariationPagination"},
                }},
                "example": {"variations": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a query parameter the listing does not accept (reason `unknown_parameter`), a `standard` other than `text`, `color` or `image` (reason `invalid_enum`), a `limit` that is not a whole number from `1` to `100` (message `must be a whole number from 1 to 100`; reason `out_of_range` for `0` or `101`, and `invalid_integer` for text such as `abc`), both `page` and `offset` (reason `conflicting_params`), or a `field_metadata` that is not a boolean (reason `invalid_boolean`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": {"search": "size", "standard": "text"}},
    },
    {
        "key": "head_variations",
        "slug": "check-the-variation-types-list",
        "title": "Check the variation types list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the variation types list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The response has no `ETag` header. To read the types, use [List variation types](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_variation",
        "slug": "create-a-variation-type",
        "title": "Create a variation type",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a variation type with its options and returns it with the type's `id`.",
        "description": "Wrap the type in `variation` and send `name`, `standard` and at least one option. The response gives the type's `id`, which the other calls take as `variation_id`, and each option's own `id`. `name` and each option's `label` and `value` are trimmed, and `standard` is stored in lower case. For an `image` type, send each option's picture as `image` with `base64` and `filename`, and no `value`.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new variation type, with `disposable` set to `false` and an `id` on every option. The response has an `ETag` header and a `Location` header with the type's path, such as `/api/v4/admin/variations/15`.",
                "schema": ROW_RESPONSE,
                "example": {"variation": CREATED_ROW},
            },
            "400": {
                "description": "The body is not wrapped in `variation`: each top-level key is reported with the reason `unknown_field`, and `variation` with the reason `required`. Or a field breaks a rule: `name` must be 2 to 100 characters, `standard` must be `text`, `color` or `image`, `options` must hold 1 to 1000 options, and each option's `order` must be from `0` to `999`.",
                "schema": ERROR_REF,
            },
            "409": {
                "description": "Another type already has that `name`, in any letter case. The response body is not valid JSON: the message is `Variation type having name \"<name>\" already exists`, with the name inserted unescaped, and `details` is empty. Check the status code instead of parsing the body.",
            },
        },
        "example_call": {},
    },
    {
        "key": "get_variation",
        "slug": "retrieve-a-variation-type",
        "title": "Retrieve a variation type",
        "method": "GET",
        "path": BASE + "/{variation_id}",
        "summary": "Returns the variation type whose `id` you pass as `variation_id`, with its options.",
        "description": "Returns one variation type under the `variation` key, with the same five fields a listing entry has: `id`, `name`, `standard`, `disposable` and `options`. The response has an `ETag` header, which changes when the type's content changes. Send `field_metadata=true` to also get a description of each field.",
        "parameters": [VARIATION_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The variation type. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": ROW_WITH_METADATA_RESPONSE,
                "example": {"variation": SAMPLE_ROWS[0]},
            },
            "404": NOT_FOUND_RESPONSE,
        },
        "example_call": {"path": {"variation_id": 12}},
    },
    {
        "key": "head_variation",
        "slug": "check-a-variation-type",
        "title": "Check a variation type",
        "method": "HEAD",
        "path": BASE + "/{variation_id}",
        "summary": "Returns headers only for one variation type, including the same `ETag` a retrieve returns.",
        "description": "Returns `200` with headers only and no body. The `ETag` header has the same value that [Retrieve a variation type](" + RETRIEVE_PAGE + ") returns for the type, so you can check whether the type has changed without downloading it.",
        "parameters": [VARIATION_ID],
        "responses": {
            "200": {"description": "Headers only, no body, with the type's `ETag`."},
            "404": {"description": "No variation type has that `variation_id`. Headers only, no body."},
        },
        "example_call": {"path": {"variation_id": 12}},
    },
    {
        "key": "update_variation",
        "slug": "replace-a-variation-type",
        "title": "Replace a variation type",
        "method": "PUT",
        "path": BASE + "/{variation_id}",
        "summary": "Replaces a variation type's name and option list. Options you leave out are deleted.",
        "description": "Wrap the type in `variation` and send `name` and the full `options` list. An option sent with its `id` is changed, an option sent without an `id` is added, and every option you leave out is deleted. You can leave out `standard`: the type keeps its own. A different `standard` is rejected, because it cannot change after the type is created.",
        "parameters": [VARIATION_ID],
        "body": {"schema": WRITE_BODY, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The variation type after the replace, with exactly the options you sent. A new option has a new `id`. The response has the type's `ETag`.",
                "schema": ROW_RESPONSE,
                "example": {"variation": REPLACED_ROW},
            },
            "400": {
                "description": "The body is not wrapped in `variation`; `name` is missing (message `variation.name: is required`); `options` is missing (message `variation.options: must hold at least one option`); or `standard` differs from the type's own (reason `read_only_field`, message `cannot be changed after the variation type is created`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"variation_id": 15}},
    },
    {
        "key": "patch_variation",
        "slug": "update-a-variation-type",
        "title": "Update a variation type",
        "method": "PATCH",
        "path": BASE + "/{variation_id}",
        "summary": "Changes only the fields and options you send in a variation type and keeps the rest.",
        "description": "Wrap the change in `variation`. Sending `name` alone renames the type and keeps every option. An option sent with its `id` changes only the fields you send for it, and an option sent without an `id` is added. Setting `default` on one option takes it off the option that had it.",
        "parameters": [VARIATION_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The variation type after the change, with every option it had and any option you added. `{\"variation\": {}}` returns `200` with the type unchanged.",
                "schema": ROW_RESPONSE,
                "example": {"variation": PATCHED_ROW},
            },
            "400": {
                "description": "The body is not wrapped in `variation`, or `standard` differs from the type's own (reason `read_only_field`, message `cannot be changed after the variation type is created`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"variation_id": 15}},
    },
    {
        "key": "delete_variation",
        "slug": "delete-a-variation-type",
        "title": "Delete a variation type",
        "method": "DELETE",
        "path": BASE + "/{variation_id}",
        "summary": "Deletes a variation type permanently. Send `cascade=true` to delete its options with it.",
        "description": "Deletes the type permanently and returns `204` with no body. The type leaves the listing, and retrieving or deleting it again returns `404`. A type that has options is deleted only with `cascade=true`, which deletes its options too. A type that a product's variants use cannot be deleted, even with `cascade=true` and even after that product is moved to the trash.",
        "parameters": [VARIATION_ID, CASCADE],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "400": {"description": "`cascade` is not a boolean. The reason is `invalid_boolean`.", "schema": ERROR_REF},
            "404": {"description": "No variation type has that `variation_id`, for example because you already deleted it.", "schema": ERROR_REF},
            "409": {
                "description": "The type still has options and you did not send `cascade=true`: the message is `This variation type still has N option(s).`, and `details[0]` names the field `options` with the reason `in_use` and the message `send ?cascade=true to delete them with the type`. Or a product's variants use the type: the message is `This variation type is used by N product(s).` and `details[0].code` is `in_use`, with or without `cascade=true`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"variation_id": 15}, "query": "cascade=true"},
    },
    {
        "key": "delete_variation_option",
        "slug": "delete-a-variation-option",
        "title": "Delete a variation option",
        "method": "DELETE",
        "path": BASE + "/{variation_id}/options/{variation_option_id}",
        "summary": "Deletes one option from a variation type and leaves the type's other options unchanged.",
        "description": "Deletes the option permanently and returns `204` with no body. The type keeps every other option as it was. You cannot delete a type's last option: to remove it, delete the type with [Delete a variation type](" + DELETE_PAGE + ") and `cascade=true`.",
        "parameters": [VARIATION_ID, VARIATION_OPTION_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "The type has no option with that `variation_option_id`, for example because the option belongs to another type. The message is `Variation option N not found on this variation type`.", "schema": ERROR_REF},
            "409": {"description": "The option is the type's last one. The message is `a variation type must keep at least one option`, and `details[0].code` is `last_option`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"variation_id": 15, "variation_option_id": 204}},
    },
    {
        "key": "list_product_variations",
        "slug": "list-a-products-variants",
        "title": "List a product's variants",
        "method": "GET",
        "path": PRODUCT_BASE,
        "summary": "Returns every variant of the product whose `id` you pass as `product_id`.",
        "description": "Returns the product's variants in one call, with no paging, grouped under `variations`. Each group's `product_key` joins the product's variation type names with `/`, and each variant's `key` joins its option labels the same way. A product without variants returns `{\"variations\": []}`. Query parameters are ignored, and this path has no `HEAD`: it returns `404`.",
        "parameters": [PRODUCT_ID],
        "responses": {
            "200": {
                "description": "The product's variant groups in `variations`. Each variant has nineteen fields, including its `variation_id`, which [Update a product's variants](" + BULK_PAGE + ") takes in `variation_ids`. Prices arrive as whole numbers or decimals, such as `0` and `10.0`. On a product whose prices include tax, `base_price` and `sale_price` are net of tax. The response has no `ETag` header.",
                "schema": {"$ref": "#/components/schemas/VariationProductVariants"},
            },
            "404": {"description": "No product has that `product_id`. The message is `Product not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"product_id": 4321}},
    },
    {
        "key": "import_product_variations",
        "slug": "import-a-products-variants",
        "title": "Import a product's variants",
        "method": "POST",
        "path": PRODUCT_BASE,
        "summary": "Adds the variants you send to the product, changes the ones whose `key` it already has, and returns how many were imported.",
        "description": "Send `variations` at the top level of the body, with no wrapper. Each group's `product_key` names the product's variation types, joined with `/`, such as `Size/Colour`, and each variant's `key` names one option label per type, joined the same way, such as `Small/Red`. A `key` the product already has changes that variant in place and keeps its `variation_id`; a new `key` adds a variant beside the others. `product_key` is matched to the `name` of the store's variation types and `key` to their option labels: a label a type does not have yet is added to the type itself, for the whole store. Each variant needs `key` and takes `name`, `sku`, `custom_sku`, `title`, `summary`, `description`, `barcode`, `country_of_origin`, `hs_code`, `pricing`, `inventory`, `ordering`, `dimensions`, `badges` and `images`. Unknown keys at the top level or in a group are ignored. To tag the variants with a transaction number, send the `X-Transaction-No` header (in the SDKs, `transaction_no`) or `transaction_no` beside `variations`. Pass the product's `id` as `product_id`: [Create a product](" + CREATE_PRODUCT_PAGE + ") returns it as `product.id`.",
        "parameters": [PRODUCT_ID, TRANSACTION_NO],
        "body": {"schema": {"$ref": "#/components/schemas/VariationImportInput"}, "example": IMPORT_BODY},
        "responses": {
            "201": {
                "description": "`status` is `success`, `message` counts the variants, such as `2 of 2 variants imported successfully`, and `total_variants` is the number imported. The response returns no variant: read them with [List a product's variants](" + PRODUCT_VARIANTS_PAGE + "). There, the `dimensions.weight` you import can read back as text, such as `\"4\"`, so read it as a number or as text. The listing does not show the transaction number; `GET /api/v4/admin/products/{product_id}/variations/{variation_id}` returns it as the variant's `transaction_no`.",
                "schema": {"$ref": "#/components/schemas/VariationImportResult"},
                "example": IMPORT_RESULT,
            },
            "400": {
                "description": "`variations` is missing or empty, or the body is wrapped in another key (message `variations field is required`); a group's `variants` is empty (message `variations[0].variants must be a non-empty array`); a variant has no `key` (message `variations[0].variants[0].key: is required`); or a variant sends `available`, `is_base` or `tiered_pricing` (reason `unknown_field`).",
                "schema": ERROR_REF,
            },
            "409": {
                "description": "`product_key` names other variation types than the ones the product's variants already use, and nothing is imported. The message starts with `this product's variants use the option types`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"product_id": 4321}},
    },
    {
        "key": "update_product_variations",
        "slug": "update-a-products-variants",
        "title": "Update a product's variants",
        "method": "PATCH",
        "path": PRODUCT_BASE + "/bulk",
        "summary": "Sets availability, prices, stock or order quantities on several variants of one product.",
        "description": "Send `variation_ids` and at least one of `available`, `base_price`, `cost_price`, `available_stock`, `min_order_quantity` and `max_order_quantity`, at the top level of the body with no wrapper. Every variant you name gets the values you send. If any entry in `variation_ids` is not a variant of this product, the whole request is rejected and nothing is written. `available_stock` sets the variant's `inventory.quantity` even when inventory tracking is off. Other body fields, and query parameters other than `response`, are ignored.",
        "parameters": [PRODUCT_ID, RESPONSE_MODE],
        "body": {"schema": {"$ref": "#/components/schemas/VariationBulkInput"}, "example": BULK_BODY},
        "responses": {
            "200": {
                "description": "`status` is `success`, `message` gives the number of variants updated, `updated` lists each variant written, and `failed` is empty. With `response=full`, each `updated` entry has fourteen fields. A `GET` on the `url` in a `full` entry returns that one variant, and the entry's `sale_price` and `is_on_sale` can differ from what [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns for a product on sale: read the variant back there to check its values.",
                "schema": {"$ref": "#/components/schemas/VariationBulkResult"},
                "example": BULK_SLIM_RESULT,
            },
            "400": {
                "description": "`variation_ids` is empty (reason `invalid_variation_ids`); an entry in `variation_ids` is not a variant of this product (message `variation N does not belong to product M`); the body sends none of the six fields (message `send at least one of available, base_price, cost_price, available_stock, min_order_quantity, max_order_quantity`); the body is not a JSON object (message `request body must be a JSON object`); or `response` is not `slim` or `full` (reason `invalid_enum`, message `must be one of slim, full`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"product_id": 4321}},
    },
]

SCHEMAS = {
    "Variation": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The variation type's `id`, set by the store. Pass it as `variation_id` in a path. Read-only."},
        "name": {"type": "string", "description": "The type's name, 2 to 100 characters. No two types have the same name, in any letter case."},
        "standard": {"type": "string", "enum": ["text", "color", "image"], "description": "The kind of type: `text`, `color` or `image`. It cannot change after the type is created."},
        "disposable": {"type": "boolean", "description": "Read-only. `false` on a type you create."},
        "options": {"type": "array", "items": {"$ref": "#/components/schemas/VariationOption"}, "description": "The type's options."},
    }},
    "VariationOption": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The option's `id`, set by the store. Pass it as `variation_option_id` to delete the option, or send it as the option's `id` in a replace or update to change the option."},
        "label": {"type": "string", "description": "The option's label, unique within its type."},
        "value": {"type": ["string", "null"], "description": "The option's value. On a `color` type, a colour such as `#ff0000` or `rgb(0,0,255)`. `null` on an `image` option."},
        "order": {"type": "integer", "minimum": 0, "maximum": 999, "description": "The option's order number, from `0` to `999`."},
        "default": {"type": "boolean", "description": "`true` on the type's default option. At most one option has it."},
        "image": {"oneOf": [{"$ref": "#/components/schemas/VariationOptionImage"}, {"type": "null"}], "description": "The option's picture on an `image` type, or `null` on a `text` or `color` type."},
    }},
    "VariationOptionImage": {"type": "object", "properties": {
        "url": {"type": "string", "description": "The full address of the stored picture."},
        "file_name": {"type": "string", "description": "The `filename` you sent with the picture."},
    }},
    "VariationInput": {"type": "object", "description": "Send these fields inside `variation`. Create requires `name`, `standard` and `options`; replace requires `name` and `options`; update takes any of them.", "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 100, "description": "2 to 100 characters, trimmed. A name another type has, in any letter case, is rejected with `409`."},
        "standard": {"type": "string", "enum": ["text", "color", "image"], "description": "`text`, `color` or `image`, in any letter case; stored in lower case. Leave it out on replace and update, or send the type's own value: a different value is rejected with `400`."},
        "options": {"type": "array", "minItems": 1, "maxItems": 1000, "items": {"$ref": "#/components/schemas/VariationOptionInput"}, "description": "1 to 1000 options. On replace, this is the full list: options you leave out are deleted."},
    }},
    "VariationOptionInput": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "Send the `id` of one of this type's options to change that option. Leave it out to add a new option."},
        "label": {"type": "string", "description": "Unique within the type. Trimmed."},
        "value": {"type": "string", "description": "Trimmed. On a `color` type, a hex value, `rgb()`, `rgba()`, `hsl()`, `hsla()`, `hsv()` or a colour name. Leave it out on an `image` option."},
        "order": {"type": "integer", "minimum": 0, "maximum": 999, "description": "From `0` to `999`."},
        "default": {"type": "boolean", "description": "Optional. `true` makes this the type's default option and takes the flag off the option that had it."},
        "image": {"$ref": "#/components/schemas/VariationOptionImageInput"},
    }},
    "VariationOptionImageInput": {"type": "object", "description": "An option's picture on an `image` type. The response returns it as `image.url` and `image.file_name`.", "properties": {
        "base64": {"type": "string", "description": "The picture's file content, base64-encoded."},
        "filename": {"type": "string", "description": "The picture's file name, such as `swatch.png`."},
    }},
    "VariationPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of variation types that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of types skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is above `0`. It is `false` when `offset` is past the last type."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
    }},
    "VariationFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Describes the five fields of a variation type, keyed by field name. Each entry gives the field's `type`. `id` and `disposable` have `read_only` set to `true`. `standard` lists `text`, `color` and `image` in `values`. `options` has `min_items` `1`, `max_items` `1000` and a `fields` block that describes the six option fields."},
    "VariationProductVariants": {"type": "object", "properties": {
        "variations": {"type": "array", "items": {"$ref": "#/components/schemas/VariationProductVariantGroup"}, "description": "The product's variant groups. Empty for a product without variants."},
    }},
    "VariationProductVariantGroup": {"type": "object", "properties": {
        "product_key": {"type": "string", "description": "The product's variation type names joined with `/`, such as `Size/Colour`."},
        "variants": {"type": "array", "items": {"$ref": "#/components/schemas/VariationProductVariant"}},
    }},
    "VariationProductVariant": {"type": "object", "properties": {
        "variation_id": {"type": "integer", "description": "Identifies the variant. It is not a variation type's `id`. Send it in `variation_ids` to update the variant."},
        "available": {"type": "boolean", "description": "Whether the variant is available."},
        "is_base": {"type": "boolean"},
        "key": {"type": "string", "description": "The variant's option labels joined with `/`, such as `Small/Red`."},
        "name": {"type": "string", "description": "The variant's name."},
        "sku": {"type": "string", "description": "The variant's SKU."},
        "custom_sku": {"type": "string"},
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "description": {"type": "string"},
        "barcode": {"type": "string"},
        "country_of_origin": {"type": "string"},
        "hs_code": {"type": "string"},
        "pricing": {"$ref": "#/components/schemas/VariationProductVariantPricing"},
        "inventory": {"$ref": "#/components/schemas/VariationProductVariantInventory"},
        "ordering": {"$ref": "#/components/schemas/VariationProductVariantOrdering"},
        "dimensions": {"$ref": "#/components/schemas/VariationProductVariantDimensions"},
        "badges": {"$ref": "#/components/schemas/VariationProductVariantBadges"},
        "images": {"type": "array", "items": {"$ref": "#/components/schemas/VariationProductVariantImage"}, "description": "The variant's images."},
    }},
    "VariationProductVariantPricing": {"type": "object", "description": "On a product whose prices include tax, `base_price` and `sale_price` are the stored prices divided by the tax rate and rounded to the cent.", "properties": {
        "base_price": {"type": "number", "description": "The variant's base price."},
        "cost_price": {"type": "number", "description": "The variant's cost price."},
        "sale_price": {"type": "number", "description": "The variant's sale price."},
        "is_on_sale": {"type": "boolean", "description": "Whether the variant is on sale."},
        "sale_amount_type": {"type": "string"},
        "hide_price": {"type": "boolean"},
        "is_call_for_price": {"type": "boolean"},
        "expect_to_pay": {"$ref": "#/components/schemas/VariationProductVariantExpectToPay"},
        "tiered_pricing": {"type": "object"},
    }},
    "VariationProductVariantExpectToPay": {"type": "object", "properties": {
        "is_enabled": {"type": "boolean"},
        "price": {"type": "number"},
    }},
    "VariationProductVariantInventory": {"type": "object", "properties": {
        "is_enabled": {"type": "boolean", "description": "Whether inventory tracking is on for the variant."},
        "quantity": {"type": "integer", "description": "The variant's stock. `available_stock` in an update sets it, even when tracking is off."},
        "low_stock_threshold": {"type": "integer"},
        "is_sold_out": {"type": "boolean"},
        "sold_out_label": {"type": "string"},
    }},
    "VariationProductVariantOrdering": {"type": "object", "properties": {
        "min_quantity": {"type": "integer", "description": "The smallest quantity a customer can order."},
        "max_quantity": {"type": "integer", "description": "The largest quantity a customer can order. `0` means no maximum."},
        "multiple_of": {"type": "integer"},
        "is_multiple_quantity_required": {"type": "boolean"},
    }},
    "VariationProductVariantDimensions": {"type": "object", "properties": {
        "length": {"type": "number"},
        "width": {"type": "number"},
        "height": {"type": "number"},
        "weight": {"type": ["number", "string"], "description": "A number, or a numeric string such as `\"26.455471\"`. Read both forms."},
    }},
    "VariationProductVariantImage": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The image's `id`."},
        "url": {"type": "string", "description": "The full address of the image."},
        "thumbnail": {"type": "string", "description": "The full address of the image's thumbnail."},
    }},
    "VariationProductVariantBadges": {"type": "object", "properties": {
        "is_featured": {"type": "boolean"},
        "is_new_arrival": {"type": "boolean"},
    }},
    "VariationBulkInput": {"type": "object", "required": ["variation_ids"], "description": "Send these fields at the top level of the body, with no wrapper. Send `variation_ids` and at least one other field. Other fields are ignored.", "properties": {
        "variation_ids": {"type": "array", "minItems": 1, "items": {"type": ["integer", "string"]}, "description": "The `variation_id` of each variant to update, as numbers or numeric strings such as `\"22\"`. Every one must be a variant of the product whose `product_id` is in the path."},
        "available": {"type": "boolean", "description": "Whether the variants are available."},
        "base_price": {"type": "number", "description": "The base price to store, as sent. On a product whose prices include tax, send the price including tax."},
        "cost_price": {"type": "number", "description": "The cost price to store, as sent."},
        "available_stock": {"type": "integer", "description": "Sets each variant's `inventory.quantity`, even when inventory tracking is off."},
        "min_order_quantity": {"type": "integer", "description": "Sets each variant's `ordering.min_quantity`."},
        "max_order_quantity": {"type": "integer", "description": "Sets each variant's `ordering.max_quantity`. `0` means no maximum."},
    }},
    "VariationBulkResult": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "message": {"type": "string", "description": "The number of variants updated, such as `1 variations updated`."},
        "updated": {"type": "array", "items": {"$ref": "#/components/schemas/VariationBulkUpdate"}, "description": "One entry per variant written."},
        "failed": {"type": "array", "items": {}, "description": "An empty list. When an entry in `variation_ids` is not a variant of the product, the whole request is rejected with `400` instead."},
    }},
    "VariationBulkUpdate": {"type": "object", "description": "One updated variant. Only `id` and `name` unless you send `response=full`.", "properties": {
        "id": {"type": "integer", "description": "The variant's `variation_id`."},
        "name": {"type": "string", "description": "The variant's name."},
        "sku": {"type": "string"},
        "custom_sku": {"type": ["string", "null"], "description": "`null` where [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns `\"\"`."},
        "barcode": {"type": ["string", "null"], "description": "`null` where [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns `\"\"`."},
        "country_of_origin": {"type": ["string", "null"], "description": "`null` where [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns `\"\"`."},
        "hs_code": {"type": ["string", "null"], "description": "`null` where [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns `\"\"`."},
        "available": {"type": "boolean"},
        "options": {"type": "array", "items": {"$ref": "#/components/schemas/VariationBulkOption"}, "description": "The options that make up the variant."},
        "pricing": {"$ref": "#/components/schemas/VariationBulkPricing"},
        "inventory": {"$ref": "#/components/schemas/VariationBulkInventory"},
        "ordering": {"$ref": "#/components/schemas/VariationBulkOrdering"},
        "transaction_no": {"type": "string"},
        "url": {"type": "string", "description": "A path such as `/api/v4/admin/products/4321/variations/91`. A `GET` on it returns that one variant, with its `transaction_no`."},
    }},
    "VariationBulkOption": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The variation option's `id`."},
        "type": {"type": "string"},
        "label": {"type": "string", "description": "The option's label."},
    }},
    "VariationBulkPricing": {"type": "object", "description": "`base_price` is the price as stored, including tax on a product whose prices include tax. `sale_price` and `is_on_sale` can differ from what [List a product's variants](" + PRODUCT_VARIANTS_PAGE + ") returns for a product on sale.", "properties": {
        "base_price": {"type": "number"},
        "cost_price": {"type": "number"},
        "sale_price": {"type": "number"},
        "is_on_sale": {"type": "boolean"},
    }},
    "VariationBulkInventory": {"type": "object", "properties": {
        "is_enabled": {"type": "boolean"},
        "quantity": {"type": "integer"},
        "low_stock_threshold": {"type": "integer"},
    }},
    "VariationBulkOrdering": {"type": "object", "properties": {
        "min_quantity": {"type": "integer"},
        "max_quantity": {"type": "integer", "description": "`0` means no maximum."},
    }},
    "VariationImportInput": {"type": "object", "required": ["variations"], "description": "Send these fields at the top level of the body, with no wrapper. Unknown keys are ignored.", "properties": {
        "variations": {"type": "array", "minItems": 1, "items": {"$ref": "#/components/schemas/VariationImportGroupInput"}, "description": "Required and not empty. One group per set of variation types."},
        "transaction_no": {"type": "string", "description": "Optional. A transaction number to tag the variants with. An `X-Transaction-No` header with a different value wins over it."},
    }},
    "VariationImportGroupInput": {"type": "object", "description": "Unknown keys are ignored.", "properties": {
        "product_key": {"type": "string", "description": "The names of the product's variation types, joined with `/`, such as `Size/Colour`. Each name is matched to the `name` of one of the store's variation types. Names other than the ones the product's variants already use are rejected with `409`."},
        "variants": {"type": "array", "minItems": 1, "items": {"$ref": "#/components/schemas/VariationImportVariantInput"}, "description": "Must not be empty. The variants to add or change."},
    }},
    "VariationImportVariantInput": {"type": "object", "required": ["key"], "description": "One variant to add or change. `available`, `is_base` and `tiered_pricing` are rejected with `400` and the reason `unknown_field`.", "properties": {
        "key": {"type": "string", "description": "Required. One option label per variation type in `product_key`, joined with `/`, such as `Small/Red`. A `key` the product already has changes that variant and keeps its `variation_id`; a new `key` adds a variant. A label the type does not have yet is added to the type."},
        "name": {"type": "string", "description": "The variant's name."},
        "sku": {"type": "string", "description": "The variant's SKU."},
        "custom_sku": {"type": "string"},
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "description": {"type": "string"},
        "barcode": {"type": "string"},
        "country_of_origin": {"type": "string"},
        "hs_code": {"type": "string"},
        "pricing": {"$ref": "#/components/schemas/VariationProductVariantPricing"},
        "inventory": {"$ref": "#/components/schemas/VariationProductVariantInventory"},
        "ordering": {"$ref": "#/components/schemas/VariationProductVariantOrdering"},
        "dimensions": {"$ref": "#/components/schemas/VariationProductVariantDimensions"},
        "badges": {"$ref": "#/components/schemas/VariationProductVariantBadges"},
        "images": {"type": "array", "items": {}},
    }},
    "VariationImportResult": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "message": {"type": "string", "description": "Counts the variants imported, such as `2 of 2 variants imported successfully`."},
        "total_variants": {"type": "integer", "description": "The number of variants imported."},
    }},
    "VariationError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string", "description": "What went wrong, such as `Variation not found`."},
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `invalid_enum` or `last_option`."},
            "message": {"type": ["string", "null"], "description": "Why the field or parameter was rejected, or `null`."},
            "value": {"description": "The value you sent, when a value was rejected, such as `foo` for `standard`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
