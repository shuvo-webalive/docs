"""The Category page settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Category page"
SLUG = "category-page"
BASE = "/admin/settings/page_settings/category_page"
ICON = "folder-tree"

SECTIONS = ["category_information", "product_information"]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `category_information` or `product_information`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "category_information"},
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

SAMPLE_CATEGORY_INFORMATION = {
    "heading": {"enabled": True, "style": "h2"},
    "show_description": False,
    "show_banner_image": False,
    "show_image": False,
    "subcategory": {
        "enabled": True, "display": True, "load_type": "pagination", "pagination_position": "top_and_bottom",
        "per_page": 12, "allow_user_per_page": False, "per_load": 10, "display_products": True, "show_summary": True,
    },
}

SAMPLE_PRODUCT_INFORMATION = {
    "use_global_defaults": False,
    "interaction_buttons": {
        "enabled": True, "add_to_cart": True, "view_details": True, "show_on_hover": True,
        "add_to_wish_list": True, "add_to_compare": True, "quick_view": False,
    },
    "show_summary": False,
    "show_sale_percentage": False,
    "show_stock_availability": False,
    "show_parent_category": False,
    "price": {"enabled": True, "expect_to_pay": True, "expect_to_pay_with_tax": False, "strike_through_previous": True},
    "variation_combination": {"enabled": True, "types": [{"id": 1, "name": "Colour"}, {"id": 4, "name": "Size"}]},
    "rating": {"enabled": True, "show_review_count": False},
    "view_switcher": {"enabled": False, "grid": True, "list": True, "tabular": True},
    "default_display": {"enabled": True, "mode": "grid", "columns_per_row": {"grid": 4, "list": 2}, "show_variation_options_label_in_tabular": False},
    "load": {"enabled": True, "type": "pagination", "pagination_position": "top_and_bottom", "per_page": 24, "allow_user_per_page": False, "per_load": 10},
    "default_sort": {"enabled": True, "by": "price_desc"},
    "sort_options": {"enabled": True, "alphabetic": True, "featured": False, "new": True, "top_selling": False, "price": True, "date": False},
}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_CATEGORY_PAGE = {
    "category_page": {
        "category_information": SAMPLE_CATEGORY_INFORMATION,
        "product_information": SAMPLE_PRODUCT_INFORMATION,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_CATEGORY_PAGE = copy.deepcopy(SAMPLE_CATEGORY_PAGE)
PATCHED_CATEGORY_PAGE["category_page"]["category_information"]["show_description"] = True
PATCHED_CATEGORY_PAGE["category_page"]["category_information"]["subcategory"]["per_page"] = 24

PATCHED_CATEGORY_INFORMATION = dict(copy.deepcopy(SAMPLE_CATEGORY_INFORMATION), show_description=True)


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


CATEGORY_PAGE_RESPONSE = {"type": "object", "properties": {
    "category_page": {"$ref": "#/components/schemas/CategoryPageSettings"},
    "group_meta": {"$ref": "#/components/schemas/GroupMeta"},
}}

ERROR = {"$ref": "#/components/schemas/Error"}

RATE_LIMITED = {"description": "Too many writes in a short time. The `Retry-After` header says how long until you can write again."}

ENDPOINTS = [
    {
        "key": "get_category_page",
        "slug": "get-category-page-settings",
        "title": "Get category page settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns both settings sections and a `group_meta` block describing each one.",
        "description": "Returns every category page setting under `category_page`, with both sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "Both sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(CATEGORY_PAGE_RESPONSE["properties"], field_metadata={
                    "$ref": "#/components/schemas/FieldMetadata",
                    "description": "Only when you send `field_metadata=true`. Keyed by section.",
                })},
                "example": SAMPLE_CATEGORY_PAGE,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_category_page",
        "slug": "update-category-page-settings",
        "title": "Update category page settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or both sections and returns all settings.",
        "description": "Send the fields to change inside `category_page`, grouped by section name. Only the fields you send change: other fields in the same block, and a section you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get category page settings](/api-reference/category-page/get-category-page-settings) does. A body that is not wrapped in `category_page` is rejected with `400 invalid_request`.",
        "body": {
            "schema": {"type": "object", "required": ["category_page"], "properties": {
                "category_page": {"$ref": "#/components/schemas/CategoryPageSettings", "description": "The fields to change, grouped by section. Send only the fields that change."},
            }},
            "example": {"category_page": {"category_information": {"show_description": True, "subcategory": {"per_page": 24}}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": CATEGORY_PAGE_RESPONSE, "example": PATCHED_CATEGORY_PAGE},
            "400": {
                "description": "The body is not wrapped in `category_page`, names a section that does not exist, or is not valid JSON.",
                "schema": ERROR,
                "example": error_example("invalid_request", "not_a_group: not a recognized field",
                                         [{"field": "not_a_group", "code": "unknown_field", "message": "not a recognized field"}],
                                         "7c1e4b2a-5d3f-4a8e-9b61-2f0c8d7e4a19"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_category_page",
        "slug": "get-category-page-settings-headers",
        "title": "Get category page settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the category page settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_category_page_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `category_information`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `category_page`, and without `group_meta`. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": {
                    "category_information": {"$ref": "#/components/schemas/CategoryInformation"},
                    "product_information": {"$ref": "#/components/schemas/ProductInformation"},
                    "field_metadata": {"$ref": "#/components/schemas/FieldMetadata", "description": "Only when you send `field_metadata=true`. Keyed by field name."},
                }},
                "example": {"category_information": SAMPLE_CATEGORY_INFORMATION},
            },
            "404": {
                "description": "No section has that name.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown page-settings section: category_page/bogus", [],
                                         "2b9d6f1c-8e4a-4c37-a05e-6d1f3b8c9e27"),
            },
        },
        "example_call": {"path": {"section": "category_information"}},
    },
    {
        "key": "patch_category_page_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `category_information`. That is the only wrapper accepted: a body wrapped in `category_page`, or not wrapped at all, is rejected with `400 invalid_request`, and `details[0].field` names the section. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change, under the same key and without `group_meta`.",
        "parameters": [SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path. No other wrapper is accepted.", "properties": {
                "category_information": {"$ref": "#/components/schemas/CategoryInformation"},
                "product_information": {"$ref": "#/components/schemas/ProductInformation"},
            }},
            "example": {"category_information": {"show_description": True}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": {"type": "object", "properties": {
                "category_information": {"$ref": "#/components/schemas/CategoryInformation"},
                "product_information": {"$ref": "#/components/schemas/ProductInformation"},
            }}, "example": {"category_information": PATCHED_CATEGORY_INFORMATION}},
            "400": {
                "description": "The body is not wrapped in the section's name (`required`), names a field the section does not have (`unknown_field`), or sends a value the field does not accept (`invalid_boolean`, `invalid_enum`, `out_of_range` or `invalid_reference`). The reason is in `details[].code`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "show_description: must be a boolean (true/false or 0/1)",
                                         [{"field": "show_description", "code": "invalid_boolean", "message": "must be a boolean (true/false or 0/1)", "value": "nope"}],
                                         "9e4a7d2b-1c6f-4b8e-8f3a-5d2c7b1e6a40"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "category_information"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def whole(description, minimum, maximum):
    return {"type": "integer", "minimum": minimum, "maximum": maximum, "description": description}


def choice(values, description):
    return {"type": "string", "enum": values, "description": description}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


PAGING = ["pagination", "load_more"]
POSITIONS = ["top", "bottom", "top_and_bottom"]

SCHEMAS = {
    "CategoryPageSettings": {"type": "object", "properties": {
        "category_information": ref("CategoryInformation"),
        "product_information": ref("ProductInformation"),
    }},
    "CategoryInformation": {"type": "object", "description": "The category itself and its subcategory list.", "properties": {
        "heading": ref("CategoryHeading"),
        "show_description": flag("Show the category's description."),
        "show_banner_image": flag("Show the category banner image."),
        "show_image": flag("Show the category image."),
        "subcategory": ref("Subcategory"),
    }},
    "CategoryHeading": {"type": "object", "description": "Whether the category name shows as a heading, and at which level.", "properties": {
        "enabled": flag("Show the category name as a heading."),
        "style": choice(["h1", "h2", "h3", "h4", "h5", "h6"], "The HTML heading level for the category name."),
    }},
    "Subcategory": {"type": "object", "description": "Whether subcategories are listed, and how the list pages.", "properties": {
        "enabled": flag("Turn on the subcategory display settings."),
        "display": flag("Show subcategories on the category page."),
        "load_type": choice(PAGING, "How subcategories are paged: `pagination` or `load_more`."),
        "pagination_position": choice(POSITIONS, "Where the subcategory pagination control shows."),
        "per_page": whole("Subcategories per page.", 1, 999999),
        "allow_user_per_page": flag("Let visitors change the number of subcategories per page."),
        "per_load": whole("Subcategories fetched each time a visitor loads more.", 1, 999999),
        "display_products": flag("Show the products that belong to subcategories."),
        "show_summary": flag("Show a short summary for each subcategory."),
    }},
    "ProductInformation": {"type": "object", "description": "Each product card, and how the product listing displays, pages and sorts.", "properties": {
        "use_global_defaults": flag("Use the store's global product listing settings instead of the ones here."),
        "interaction_buttons": ref("InteractionButtons"),
        "show_summary": flag("Show a short product summary on each card."),
        "show_sale_percentage": flag("Show the discount percentage badge."),
        "show_stock_availability": flag("Show the stock availability tag."),
        "show_parent_category": flag("Show the product's parent category name."),
        "price": ref("Price"),
        "variation_combination": ref("VariationCombination"),
        "rating": ref("Rating"),
        "view_switcher": ref("ViewSwitcher"),
        "default_display": ref("DefaultDisplay"),
        "load": ref("ProductLoad"),
        "default_sort": ref("DefaultSort"),
        "sort_options": ref("SortOptions"),
    }},
    "InteractionButtons": {"type": "object", "description": "The buttons on each product card.", "properties": {
        "enabled": flag("Show the interaction buttons on each card."),
        "add_to_cart": flag("Show the Add to Cart button."),
        "view_details": flag("Show the View Details button."),
        "show_on_hover": flag("Show the buttons only on hover."),
        "add_to_wish_list": flag("Show the Add to Wish List button."),
        "add_to_compare": flag("Show the Add to Compare button."),
        "quick_view": flag("Show the Quick View button. Needs the Product Quick View plugin switched on."),
    }},
    "Price": {"type": "object", "description": "Whether a card shows a price, and which price.", "properties": {
        "enabled": flag("Show the product price."),
        "expect_to_pay": flag("Show the expect to pay price. Depends on `price.enabled`."),
        "expect_to_pay_with_tax": flag("Include tax in the expect to pay price. Depends on `price.expect_to_pay`."),
        "strike_through_previous": flag("Show the previous price struck through."),
    }},
    "VariationCombination": {"type": "object", "description": "Whether variation combinations show, and which variation types they offer.", "properties": {
        "enabled": flag("Show selectable variation combinations on each card."),
        "types": {"type": "array", "items": ref("VariationType"), "description": "The variation types offered as combinations. `field_metadata` lists every variation type your store defines, and the forms a write accepts under `accepts`. An id that matches no variation type is rejected with `400 invalid_reference`."},
    }},
    "VariationType": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The variation type's id."},
        "name": {"type": "string", "description": "The variation type's name."},
    }},
    "Rating": {"type": "object", "description": "Whether the rating shows, and the review count beside it.", "properties": {
        "enabled": flag("Show the product rating."),
        "show_review_count": flag("Show the review count. Depends on `rating.enabled`."),
    }},
    "ViewSwitcher": {"type": "object", "description": "Which display modes a visitor can switch between.", "properties": {
        "enabled": flag("Let visitors switch the product display mode."),
        "grid": flag("Offer the grid view."),
        "list": flag("Offer the list view."),
        "tabular": flag("Offer the tabular view."),
    }},
    "DefaultDisplay": {"type": "object", "description": "The mode the product listing opens in, and how many columns each row has.", "properties": {
        "enabled": flag("Set a default display mode."),
        "mode": choice(["grid", "list", "tabular"], "The default display mode."),
        "columns_per_row": ref("ColumnsPerRow"),
        "show_variation_options_label_in_tabular": flag("Show the variation options label in tabular view."),
    }},
    "ColumnsPerRow": {"type": "object", "description": "Product columns per row, for each display mode.", "properties": {
        "grid": whole("Columns per row in grid view.", 1, 6),
        "list": whole("Columns per row in list view.", 1, 2),
    }},
    "ProductLoad": {"type": "object", "description": "How the product listing pages, and where its pagination control shows.", "properties": {
        "enabled": flag("Turn on the product load settings."),
        "type": choice(PAGING, "How products are paged: `pagination` or `load_more`."),
        "pagination_position": choice(POSITIONS, "Where the product pagination control shows."),
        "per_page": whole("Products per page.", 1, 999999),
        "allow_user_per_page": flag("Let visitors change the number of products per page."),
        "per_load": whole("Products fetched each time a visitor loads more.", 1, 999999),
    }},
    "DefaultSort": {"type": "object", "description": "Whether a default sort order applies, and which one.", "properties": {
        "enabled": flag("Apply a default sort order."),
        "by": choice(["alpha_asc", "alpha_desc", "price_desc", "price_asc", "created_asc", "created_desc"],
                     "The default sort order: `alpha_asc` (A to Z), `alpha_desc` (Z to A), `price_desc` (high to low), `price_asc` (low to high), `created_asc` (oldest first) or `created_desc` (latest first)."),
    }},
    "SortOptions": {"type": "object", "description": "The sort orders a visitor can switch to.", "properties": {
        "enabled": flag("Show the sort options to visitors."),
        "alphabetic": flag("Offer alphabetical sorting."),
        "featured": flag("Offer featured sorting."),
        "new": flag("Offer newest first sorting."),
        "top_selling": flag("Offer top selling sorting."),
        "price": flag("Offer price sorting."),
        "date": flag("Offer created date sorting."),
    }},
    "GroupMeta": {"type": "object", "description": "One entry per section. Only [Get category page settings](/api-reference/category-page/get-category-page-settings) and [Update category page settings](/api-reference/category-page/update-category-page-settings) return it.", "properties": {
        "category_information": ref("SectionMeta"),
        "product_information": ref("SectionMeta"),
    }},
    "SectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for both sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for both sections."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/page_settings/category_page/category_information`."},
    }},
    "FieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `FieldMetadataEntry` in place of each value."},
    "FieldMetadataEntry": {"type": "object", "properties": {
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does."},
        "type": {"type": "string", "description": "The kind of value the field takes, such as `boolean`, `enum`, `integer` or `reference_list`."},
        "default": {"description": "The field's default value."},
        "allowed_values": {"type": "array", "items": {}, "description": "The values the field accepts, for an `enum` or `reference_list` field. For `variation_combination.types`, the `{id, name}` records your store defines."},
        "labels": {"type": "object", "additionalProperties": {"type": "string"}, "description": "A label for each allowed value, for an `enum` field."},
        "min": {"type": "integer", "description": "The lowest value, for an `integer` field."},
        "max": {"type": "integer", "description": "The highest value, for an `integer` field."},
        "requires": {"type": "string", "description": "The field this one depends on, such as `price.enabled`."},
        "item_shape": {"type": "string", "description": "The shape of each item, for a `reference_list` field."},
        "accepts": {"type": "string", "description": "The forms a write accepts, for a `reference_list` field."},
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

OVERVIEW_DESCRIPTION = "Read and change how your store's category pages show the category, its subcategories and its products."
INTRO = "The Category page API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/page_settings/category_page`."
WARNING = (
    "Every write body must be wrapped in a key, and the key depends on the path. On `/category_page`,\n"
    "  wrap the fields in `category_page` and then in the section name. On `/category_page/{section}`,\n"
    "  wrap them in the section's own name only, such as `category_information`: a body wrapped in\n"
    "  `category_page`, or not wrapped at all, is rejected with `400 invalid_request`."
)
NOTES = [
    "**The settings are split into two sections.** `category_information` controls the category itself\n"
    "  and its subcategory list. `product_information` controls each product card and how the product\n"
    "  listing displays, pages and sorts. Read or write both through `/category_page`, or one through\n"
    "  `/category_page/{section}`. An unknown section returns `404 not_found`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values, including other fields in the same nested block and a section you did\n"
    "  not name. `PUT`, `POST` and `DELETE` are rejected on both paths with `405 method_not_allowed`\n"
    "  and an `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Add `field_metadata=true` to a read to get a description of every field.** The settings are\n"
    "  still returned with it. Each entry gives the field's `ui_label`, `description`, `type` and\n"
    "  `default`, and every `enum` field also lists its `allowed_values`, with a label for each in\n"
    "  `labels`. For `variation_combination.types`, `allowed_values` lists the variation types your store\n"
    "  defines, with the ids you can send. On `/category_page` the block is keyed by section; on a\n"
    "  section it is keyed by field name.",
    "**All category page writes share one rate limit.** If you send eleven writes within about 2.3\n"
    "  seconds, the eleventh is rejected with `429` and a `Retry-After` header that counts down the time\n"
    "  left before writes are accepted again. Until then, writes to either section and to\n"
    "  `/category_page` are all rejected, while reads still return `200`. A retry before then counts as\n"
    "  another write, so wait until `Retry-After` has passed before you write again.",
    "**`400`, `404` and `405` responses share one shape:** an `error` object with `code`, `message`,\n"
    "  `details` (one entry per rejected field, each with its own `field`, `code` and `message`) and\n"
    "  `request_id`.",
]
