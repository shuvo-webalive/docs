"""The Product listing settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Product listing"
SLUG = "product-listing"
BASE = "/admin/settings/product_listing"
ICON = "table-cells"

OVERVIEW_DESCRIPTION = "Read and change what your store's product listings show for each product, and how they page and sort."
INTRO = "The Product listing API has three endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/product_listing`."

GET_PAGE = "/api-reference/product-listing/get-product-listing-settings"
UPDATE_PAGE = "/api-reference/product-listing/update-product-listing-settings"

SECTIONS = ["product_information", "load", "sorting", "sortable_items"]
LOAD_TYPES = ["pagination", "load_more"]
POSITIONS = ["top", "bottom", "top_and_bottom"]
SORT_BY = ["alpha_asc", "alpha_desc", "price_desc", "price_asc", "created_asc", "created_desc"]

WARNING = (
    "**Product listing has no section paths.** Other settings areas with sections, such as Category page,\n"
    "  let you read or write one section at its own path. `/api/v4/admin/settings/product_listing/{section}`\n"
    "  returns `404` for every method, even for the four real section names, with the message\n"
    "  `Unknown settings path: product_listing/<name>`. To change one section, name it inside the\n"
    "  `product_listing` wrapper of [Update product listing settings](" + UPDATE_PAGE + ")."
)

NOTES = [
    "**Every write is wrapped in `product_listing`, then in the section name.** Send\n"
    "  `{\"product_listing\": {\"sorting\": {\"enabled\": true}}}`. A bare section such as `{\"sorting\": {...}}`,\n"
    "  or a field at the top level, is rejected with `400 missing_wrapper` and the message\n"
    "  `request body must be wrapped in a 'product_listing' object`. A field placed directly inside\n"
    "  `product_listing` is rejected with `400 validation_failed` and `<field>: not a recognized section`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values, including other fields in the same nested block and any section you did\n"
    "  not name. One body can change all four sections. `PUT`, `POST` and `DELETE` are rejected with\n"
    "  `405 method_not_allowed` and an `Allow: GET, HEAD, PATCH, OPTIONS` header. There is nothing to\n"
    "  create or delete: the four sections already exist.",
    "**Values must match the field's type and allowed values.** Booleans take `true`, `false`, `0` or `1`;\n"
    "  a string is rejected with `must be a boolean (true/false or 0/1)`. `load.type` takes `pagination` or\n"
    "  `load_more`. `load.pagination.position` takes `top`, `bottom`, `top_and_bottom` or `null`.\n"
    "  `sorting.sort_by` takes `alpha_asc`, `alpha_desc`, `price_desc`, `price_asc`, `created_asc`,\n"
    "  `created_desc` or `null`. Any other value is rejected with `400`, and an unknown field is rejected\n"
    "  with `400` and `not a recognized field`.",
    "**A write to a dependent field is accepted even when the field it depends on does not switch it on.**\n"
    "  `load.load_more.per_load` at `0` is accepted while `load.type` is `pagination`, and you can set\n"
    "  `load.type` while `load.enabled` is `false`. `load.pagination.per_page` is still checked: `0` is\n"
    "  rejected with `400` and `must be a positive integer for the selected load type`, and `1000000`\n"
    "  with `400` and `must be between 1 and 999999`.",
    "**Add `field_metadata=true` to a read to get a description of every field.** The settings and\n"
    "  `group_meta` are still returned. `field_metadata` is keyed by section, then nested the same way as\n"
    "  that section, with one entry for every field. For `product_information.variation_combination.types`,\n"
    "  the entry's `allowed_values` lists your store's variation type names; any other name is rejected\n"
    "  with `400` and `unknown variation type`. `load` has a field named `type`, so use the settings body,\n"
    "  not the presence of a `type` key, to tell a nested block from a field's entry.",
]

FIELD_METADATA = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in all four sections. It is keyed by section, then nested the same way as that section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_PRODUCT_INFORMATION = {
    "interaction_buttons": {"enabled": True, "add_to_cart": True, "show_details": True, "show_on_hover": False},
    "show_summary": True,
    "show_sale_percentage": True,
    "show_stock_availability": False,
    "show_parent_category": False,
    "show_loyalty_point": False,
    "price": {"enabled": True, "expect_to_pay": False, "expect_to_pay_with_tax": False},
    "reviews": {"rating_active": True, "show_review_count": True},
    "variation_combination": {"enabled": True, "types": ["Size", "Color"]},
    "show_variations_as_products": False,
}

SAMPLE_LOAD = {
    "enabled": True,
    "type": "pagination",
    "pagination": {"position": "bottom", "per_page": 12, "allow_user_per_page": False},
    "load_more": {"per_load": 10},
}

SAMPLE_SORTING = {"enabled": False, "sort_by": None}

SAMPLE_SORTABLE_ITEMS = {
    "enabled": True,
    "options": {"alphabetic": True, "featured": False, "new": True, "top_selling": False, "price": True, "date": False},
}

SAMPLE_GROUP_META = {section: {"kind": "setting", "writable": True} for section in SECTIONS}

SAMPLE_PRODUCT_LISTING = {
    "product_listing": {
        "product_information": SAMPLE_PRODUCT_INFORMATION,
        "load": SAMPLE_LOAD,
        "sorting": SAMPLE_SORTING,
        "sortable_items": SAMPLE_SORTABLE_ITEMS,
    },
    "group_meta": SAMPLE_GROUP_META,
}

UPDATE_EXAMPLE = {"product_listing": {"sorting": {"enabled": True, "sort_by": "price_asc"}, "load": {"pagination": {"per_page": 24}}}}

PATCHED_PRODUCT_LISTING = copy.deepcopy(SAMPLE_PRODUCT_LISTING)
PATCHED_PRODUCT_LISTING["product_listing"]["sorting"] = {"enabled": True, "sort_by": "price_asc"}
PATCHED_PRODUCT_LISTING["product_listing"]["load"]["pagination"]["per_page"] = 24


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


PRODUCT_LISTING_RESPONSE = {"type": "object", "properties": {
    "product_listing": ref("ProductListingSettings"),
    "group_meta": ref("ProductListingGroupMeta"),
}}

ERROR = ref("ProductListingError")

UPDATE_400 = (
    "The body is not wrapped in `product_listing` (`400 missing_wrapper`: `request body must be wrapped in a 'product_listing' object`), "
    "names something other than the four sections directly inside it (`400 validation_failed`: `<name>: not a recognized section`), "
    "or sends a field or value the section does not accept. The messages for those include `not a recognized field`, "
    "`must be a boolean (true/false or 0/1)`, `must be a positive integer for the selected load type`, "
    "`must be between 1 and 999999` and `unknown variation type`. A value outside the allowed list of `load.type`, "
    "`load.pagination.position` or `sorting.sort_by` is rejected with `400` too."
)

ENDPOINTS = [
    {
        "key": "get_product_listing",
        "slug": "get-product-listing-settings",
        "title": "Get product listing settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all four product listing sections and a `group_meta` block describing each one.",
        "description": "Returns every product listing setting under `product_listing`, with all four sections in full: `product_information`, `load`, `sorting` and `sortable_items`. Beside it, `group_meta` gives each section's `kind` and whether it is `writable`; it has no `href`, because no section has a path of its own. Add `field_metadata=true` to also get a description of every field, keyed by section. The response has no `ETag` header.",
        "parameters": [FIELD_METADATA],
        "responses": {
            "200": {
                "description": "All four sections and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(PRODUCT_LISTING_RESPONSE["properties"], field_metadata=dict(
                    ref("ProductListingFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section.",
                ))},
                "example": SAMPLE_PRODUCT_LISTING,
            },
        },
        "example_call": {},
    },
    {
        "key": "patch_product_listing",
        "slug": "update-product-listing-settings",
        "title": "Update product listing settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change inside `product_listing`, grouped by section name. Only the fields you send change: other fields in the same block, and sections you leave out, keep their stored values. One body can change all four sections. Returns all the settings after the change, with `group_meta`, as [Get product listing settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "required": ["product_listing"], "properties": {
                "product_listing": dict(ref("ProductListingSettings"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": UPDATE_EXAMPLE,
        },
        "responses": {
            "200": {
                "description": "All the settings after the change, with `group_meta`.",
                "schema": PRODUCT_LISTING_RESPONSE,
                "example": PATCHED_PRODUCT_LISTING,
            },
            "400": {"description": UPDATE_400, "schema": ERROR},
        },
        "example_call": {},
    },
    {
        "key": "head_product_listing",
        "slug": "check-the-product-listing-settings",
        "title": "Check the product listing settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the product listing settings are reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0`. Neither this response nor [Get product listing settings](" + GET_PAGE + ") has an `ETag` header.",
        "responses": {
            "200": {"description": "The settings are reachable. Headers only, with `Content-Length: 0` and no `ETag` header. No body."},
        },
        "example_call": {},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def whole(description, minimum, maximum):
    return {"type": "integer", "minimum": minimum, "maximum": maximum, "description": description}


def choice(values, description, nullable=False):
    if nullable:
        return {"type": ["string", "null"], "enum": values + [None], "description": description}
    return {"type": "string", "enum": values, "description": description}


SCHEMAS = {
    "ProductListingSettings": {"type": "object", "description": "The product listing settings, in four sections.", "properties": {
        "product_information": ref("ProductListingProductInformation"),
        "load": ref("ProductListingLoad"),
        "sorting": ref("ProductListingSorting"),
        "sortable_items": ref("ProductListingSortableItems"),
    }},
    "ProductListingProductInformation": {"type": "object", "description": "What each product shows on a listing tile.", "properties": {
        "interaction_buttons": ref("ProductListingInteractionButtons"),
        "show_summary": flag("Show the product summary on each tile."),
        "show_sale_percentage": flag("Show the sale percentage on each tile."),
        "show_stock_availability": flag("Show the stock availability on each tile."),
        "show_parent_category": flag("Show the product's parent category on each tile."),
        "show_loyalty_point": flag("Show loyalty points on each tile."),
        "price": ref("ProductListingPrice"),
        "reviews": ref("ProductListingReviews"),
        "variation_combination": ref("ProductListingVariationCombination"),
        "show_variations_as_products": flag("Show variations as separate products in the listing."),
    }},
    "ProductListingInteractionButtons": {"type": "object", "description": "The add to cart and view details buttons on each listing tile.", "properties": {
        "enabled": flag("Show the buttons on each tile."),
        "add_to_cart": flag("Show the add to cart button."),
        "show_details": flag("Show the view details button."),
        "show_on_hover": flag("Show the buttons on hover."),
    }},
    "ProductListingPrice": {"type": "object", "description": "Which prices each listing tile shows.", "properties": {
        "enabled": flag("Show the price."),
        "expect_to_pay": flag("Show the expect to pay price."),
        "expect_to_pay_with_tax": flag("Show the expect to pay price with tax."),
    }},
    "ProductListingReviews": {"type": "object", "description": "The rating stars on each listing tile and the review count beside them.", "properties": {
        "rating_active": flag("Show the rating stars."),
        "show_review_count": flag("Show the review count beside the stars."),
    }},
    "ProductListingVariationCombination": {"type": "object", "description": "Which variation types each listing tile combines.", "properties": {
        "enabled": flag("Show variation combinations on each tile."),
        "types": {"type": "array", "items": {"type": "string"}, "description": "Names of your store's variation types, such as `Color`. The entry for this field in `field_metadata` lists the names you can send under `allowed_values`. Any other name is rejected with `400` and `unknown variation type`."},
    }},
    "ProductListingLoad": {"type": "object", "description": "Whether a listing pages or loads more. `type` selects which block applies.", "properties": {
        "enabled": flag("Turn the load settings on."),
        "type": choice(LOAD_TYPES, "How the listing loads products: `pagination` uses the `pagination` block and `load_more` uses the `load_more` block. Any other value is rejected with `400`."),
        "pagination": ref("ProductListingLoadPagination"),
        "load_more": ref("ProductListingLoadMore"),
    }},
    "ProductListingLoadPagination": {"type": "object", "description": "Where the pager shows and how many products a page holds.", "properties": {
        "position": choice(POSITIONS, "Where the pager shows: `top`, `bottom` or `top_and_bottom`, or `null`. Any other value is rejected with `400`.", nullable=True),
        "per_page": whole("Products per page, from `1` to `999999`. `0` is rejected with `must be a positive integer for the selected load type`, and `1000000` with `must be between 1 and 999999`.", 1, 999999),
        "allow_user_per_page": flag("Let shoppers change the number of products per page."),
    }},
    "ProductListingLoadMore": {"type": "object", "description": "How many products each press of load more adds.", "properties": {
        "per_load": whole("Products added each time a shopper presses load more, from `1` to `999999`. While `load.type` is `pagination`, `0` is accepted.", 1, 999999),
    }},
    "ProductListingSorting": {"type": "object", "description": "The order a listing is shown in.", "properties": {
        "enabled": flag("Turn sorting on."),
        "sort_by": choice(SORT_BY, "The sort order: `alpha_asc`, `alpha_desc`, `price_desc`, `price_asc`, `created_asc` or `created_desc`, or `null`. Any other value is rejected with `400`.", nullable=True),
    }},
    "ProductListingSortableItems": {"type": "object", "description": "Whether a shopper can re-sort a listing, and by what.", "properties": {
        "enabled": flag("Let shoppers re-sort the listing."),
        "options": ref("ProductListingSortableOptions"),
    }},
    "ProductListingSortableOptions": {"type": "object", "description": "The sort orders a shopper can pick from.", "properties": {
        "alphabetic": flag("Offer alphabetical sorting."),
        "featured": flag("Offer sorting by featured products."),
        "new": flag("Offer sorting by newest."),
        "top_selling": flag("Offer sorting by top selling."),
        "price": flag("Offer sorting by price."),
        "date": flag("Offer sorting by date."),
    }},
    "ProductListingGroupMeta": {"type": "object", "description": "One entry per section. No entry has an `href`, because no section has a path of its own.", "properties": {
        section: ref("ProductListingSectionMeta") for section in SECTIONS
    }},
    "ProductListingSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for all four sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for all four sections."},
    }},
    "ProductListingFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Keyed by section, then nested the same way as that section's settings, with a `ProductListingFieldMetadataEntry` in place of each field's value. Every field has an entry, and there are no other entries."},
    "ProductListingFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes, such as `enum_list` for `product_information.variation_combination.types`."},
        "allowed_values": {"type": "array", "items": {}, "description": "The values the field accepts. For `product_information.variation_combination.types`, the names of your store's variation types."},
        "depends_on": {"description": "Present on a field that depends on another field's value, such as `load.load_more.per_load`. A write to the field is still accepted when that other value does not switch it on."},
        "nullable": {"description": "Whether the field accepts `null`."},
    }},
    "ProductListingError": {"type": "object", "description": "Describes why the request was rejected. The message gives the reason, such as `request body must be wrapped in a 'product_listing' object`."},
}
