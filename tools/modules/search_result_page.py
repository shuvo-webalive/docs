"""The Search result page settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Search result page"
SLUG = "search-result-page"
BASE = "/admin/settings/page_settings/search_result_page"
ICON = "magnifying-glass"

PAGE = "/api-reference/" + SLUG + "/"
LIST_PAGE = PAGE + "list-product-promotions"

SECTIONS = ["product_information", "seo", "reinitialise"]

SECTION_READ = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read: `product_information`, `seo` or `reinitialise`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "product_information"},
}

SECTION_WRITE = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to write. Only `product_information` accepts a write: a write to `seo` or `reinitialise` is rejected with `400`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "product_information"},
}

PROMOTION_ID = {
    "name": "promotion_id",
    "in": "path",
    "required": True,
    "description": "The product promotion's `id`, from a listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 4},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field, keyed by section: `product_information`, `seo` and `reinitialise`. The settings and `group_meta` are still returned. It does not describe the promotion fields: send `field_metadata=true` to the promotions listing for those.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_PROMOTIONS = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata` with two keys. `fields` describes each promotion field, including the values `rule` and `position` accept. `group_meta.product_promotion.max_items` is the most promotions the collection holds.",
    "schema": {"type": "boolean", "example": True},
}

OFFSET = {
    "name": "offset",
    "in": "query",
    "description": "Number of promotions to skip before the first one returned. `pagination.offset` shows the value you sent.",
    "schema": {"type": "integer", "example": 0},
}

LIMIT = {
    "name": "limit",
    "in": "query",
    "description": "Not applied. The listing returns the same promotions whatever `limit` you send, and `pagination.limit` shows the collection's own limit, such as `20`, not the value you sent.",
    "schema": {"type": "integer", "example": 20},
}

SAMPLE_PRODUCT_INFORMATION = {
    "use_default_product_listing_configurations": False,
    "product_interaction_buttons": {
        "enabled": False, "display_add_to_cart_button": True, "display_add_to_compare_button": True,
        "display_add_to_wishlist_button": True, "display_view_details_button": False,
        "display_on_hover": False, "display_quick_view_button": False,
    },
    "display_content_page": True,
    "number_of_searches_per_result": {"enabled": True, "items_per_page": 16},
    "display_short_description": False,
    "display_variations_combination": False,
    "set_product_display_preferences": {
        "enabled": True, "display_mode": "pagination", "select_pagination_position": "bottom",
        "number_of_products_per_page": 5, "allow_users_to_select_number_of_products": False,
        "number_of_products_per_load": 10,
    },
    "set_product_sorting": {"enabled": False, "default_sort": "alpha_asc"},
    "configure_sorting_options": {
        "enabled": False, "alphabetical": False, "featured": False, "new": False,
        "top_selling": False, "price": False, "created_date": False,
    },
    "display_loyalty_points": True,
    "display_price": {"enabled": True, "display_expect_to_pay_price": False, "show_tax_with_the_expect_to_pay_price": False},
    "label_for_price": "Price",
}

SAMPLE_SEO = {"read_only": True, "page_kind": "search_result"}
SAMPLE_REINITIALISE = {"action": "POST"}

SAMPLE_GROUP_META = {
    "product_information": {"kind": "setting", "writable": True, "ui_label": "Product Information", "href": "/api/v4" + BASE + "/product_information"},
    "seo": {"kind": "setting", "writable": False, "ui_label": "SEO", "href": "/api/v4/admin/seo-settings"},
    "product_promotion": {"kind": "resource", "writable": True, "ui_label": "Product Promotion", "href": "/api/v4" + BASE + "/product_promotion"},
    "reinitialise": {"kind": "action", "writable": False, "ui_label": "Reinitialise", "href": "/api/v4/admin/search/reindex"},
}

SAMPLE_SETTINGS = {
    "search_result_page": {
        "product_information": SAMPLE_PRODUCT_INFORMATION,
        "seo": SAMPLE_SEO,
        "product_promotion": {"read_only": True},
        "reinitialise": SAMPLE_REINITIALISE,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_SETTINGS = copy.deepcopy(SAMPLE_SETTINGS)
PATCHED_SETTINGS["search_result_page"]["product_information"]["display_short_description"] = True

PATCHED_PRODUCT_INFORMATION = dict(copy.deepcopy(SAMPLE_PRODUCT_INFORMATION), display_short_description=True)

SAMPLE_PROMOTION = {
    "id": 4, "name": "Winter campaign", "rule": "all_search_result", "position": "top",
    "specific_keywords": "", "is_active": True, "is_always_available": True,
    "available_from_date": None, "available_to_date": None, "product_ids": [829],
    "created": "2026-08-20T01:02:52Z", "updated": "2026-08-20T01:02:52Z",
}

SECOND_PROMOTION = {
    "id": 5, "name": "Boots search", "rule": "if_matches_specific_keywords", "position": "bottom",
    "specific_keywords": "boots", "is_active": True, "is_always_available": True,
    "available_from_date": None, "available_to_date": None, "product_ids": [412, 413],
    "created": "2026-09-02T04:10:00Z", "updated": "2026-09-02T04:10:00Z",
}

CREATED_PROMOTION = {
    "id": 6, "name": "Spring campaign", "rule": "all_search_result", "position": "top",
    "specific_keywords": "", "is_active": True, "is_always_available": True,
    "available_from_date": None, "available_to_date": None, "product_ids": [],
    "created": "2026-09-19T03:15:00Z", "updated": "2026-09-19T03:15:00Z",
}

MOVED_PROMOTION = dict(CREATED_PROMOTION, position="bottom", updated="2026-09-19T03:20:00Z")
PAUSED_PROMOTION = dict(MOVED_PROMOTION, is_active=False, updated="2026-09-19T03:25:00Z")

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}


def error(code, message, request_id):
    return {"error": {"code": code, "message": message, "details": [], "request_id": request_id}}


UNKNOWN_SECTION = error("not_found", "Unknown page-settings section: search_result_page/bogus", "3f6b2a91-7c4d-4e58-9a1f-2d8c5b7e6a14")
SEO_READ_ONLY = error("invalid_request", "seo is a read-only section", "8d2e4c17-5b9a-4f63-b0e2-7a1c9d3f5e28")
NAME_REQUIRED = error("invalid_request", "name is required", "c5a19e3b-2f7d-4b86-9c40-1e6d8a2b7f53")
PROMOTION_NOT_FOUND = error("not_found", "Product promotion not found", "6e0d8b42-9a3c-4d17-8f5b-3c2a7e1d9b60")
RETRIEVE_NOT_FOUND = error("not_found", "Product promotion not found: 6", "9b4c7e21-5d8a-4f36-a0e9-2c7b1f6d3a85")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("SearchResultPageError")

SETTINGS_RESPONSE = {"type": "object", "properties": {
    "search_result_page": ref("SearchResultPageSettings"),
    "group_meta": ref("SearchResultGroupMeta"),
}}

SECTION_RESPONSE = {"type": "object", "properties": {
    "search_result_page": {"type": "object", "description": "Holds only the section in the path.", "properties": {
        "product_information": ref("SearchResultProductInformation"),
        "seo": ref("SearchResultSeo"),
        "reinitialise": ref("SearchResultReinitialise"),
    }},
}}

PROMOTION_RESPONSE = {"type": "object", "properties": {"product_promotion": ref("ProductPromotion")}}

RATE_LIMITED = {
    "description": "Too many settings writes in a short time. Writes to the settings and to each section share one limit. The code is `rate_limited`, and the `Retry-After` header counts down the time left before writes are accepted again.",
    "schema": ERROR,
}

ENDPOINTS = [
    {
        "key": "get_search_result_page",
        "slug": "get-search-result-page-settings",
        "title": "Get search result page settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all search result page settings and a `group_meta` block describing each section.",
        "description": "Returns the settings under `search_result_page`: the `product_information`, `seo` and `reinitialise` sections. The promotions are not included: `product_promotion` holds only `{\"read_only\": true}`, so use [List product promotions](" + LIST_PAGE + ") to get them. Beside the settings, `group_meta` has one entry for each section and one for the promotions, each with a `kind`, a `writable` flag, a `ui_label` and the `href` where it is managed. Add `field_metadata=true` to also get a description of every field, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "The settings and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(SETTINGS_RESPONSE["properties"], field_metadata=dict(
                    ref("SearchResultFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section: `product_information`, `seo` and `reinitialise`.",
                ))},
                "example": SAMPLE_SETTINGS,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_search_result_page",
        "slug": "update-search-result-page-settings",
        "title": "Update search result page settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the `product_information` fields you send and returns all the settings.",
        "description": "Send the fields to change inside `search_result_page` and then `product_information`, the only section you can write. Fields you leave out keep their stored values, even inside a nested block such as `product_interaction_buttons`. Returns all the settings after the change, with `group_meta`. A body that is not wrapped in `search_result_page` is rejected with `400 invalid_request`.",
        "body": {
            "schema": {"type": "object", "required": ["search_result_page"], "properties": {
                "search_result_page": {"type": "object", "description": "The fields to change, inside `product_information`. Send only the fields that change.", "properties": {
                    "product_information": ref("SearchResultProductInformation"),
                }},
            }},
            "example": {"search_result_page": {"product_information": {"display_short_description": True}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": SETTINGS_RESPONSE, "example": PATCHED_SETTINGS},
            "400": {"description": "The body is not wrapped in `search_result_page`. The code is `invalid_request`, and the error names `search_result_page`.", "schema": ERROR},
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_search_result_page",
        "slug": "get-search-result-page-settings-headers",
        "title": "Get search result page settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the search result page settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_search_result_page_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one section, such as `product_information`, inside a `search_result_page` key.",
        "description": "Returns one section inside the `search_result_page` key, not under the section's own key: a read of `seo` returns `{\"search_result_page\": {\"seo\": {\"read_only\": true, \"page_kind\": \"search_result\"}}}`. The response has no `group_meta`. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION_READ, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section inside `search_result_page`. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": {"type": "object", "properties": dict(SECTION_RESPONSE["properties"], field_metadata=dict(
                    ref("SearchResultFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by field name.",
                ))},
                "example": {"search_result_page": {"product_information": SAMPLE_PRODUCT_INFORMATION}},
            },
            "404": {"description": "No section has that name. The message is `Unknown page-settings section: search_result_page/<section>`.", "schema": ERROR, "example": UNKNOWN_SECTION},
        },
        "example_call": {"path": {"section": "product_information"}},
    },
    {
        "key": "patch_search_result_page_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in `product_information` and returns the whole section.",
        "description": "Send the fields to change wrapped in the section's own key, `product_information`. A body wrapped in `search_result_page` and then `product_information` is accepted too. Only the fields you send change, and the response is the whole section after the change, inside `search_result_page` and without `group_meta`. `seo` and `reinitialise` cannot be written: a write to either is rejected with `400`.",
        "parameters": [SECTION_WRITE],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in `product_information`, or in `search_result_page` and then `product_information`.", "properties": {
                "product_information": ref("SearchResultProductInformation"),
                "search_result_page": {"type": "object", "properties": {"product_information": ref("SearchResultProductInformation")}},
            }},
            "example": {"product_information": {"display_short_description": True}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, inside `search_result_page`.", "schema": SECTION_RESPONSE, "example": {"search_result_page": {"product_information": PATCHED_PRODUCT_INFORMATION}}},
            "400": {
                "description": "The body is not wrapped in the section's key: the code is `invalid_request`, and the error names the section with the code `required`. Or the section is `seo` (`seo is a read-only section`) or `reinitialise` (`reinitialise is not a writable setting`). Or a field or value is not accepted, for example `unknown field`, `must be a boolean`, `invalid enum value for display_mode` or `items_per_page must be >= 5`.",
                "schema": ERROR,
                "example": SEO_READ_ONLY,
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "product_information"}},
    },
    {
        "key": "get_search_result_page_product_promotions",
        "slug": "list-product-promotions",
        "title": "List product promotions",
        "method": "GET",
        "path": BASE + "/product_promotion",
        "summary": "Returns the store's product promotions under `product_promotions`. Send `offset` to skip some; `limit` is ignored.",
        "description": "Returns the product promotions as a list under `product_promotions`, with a `pagination` block that gives the `total` and the `offset` you sent. Send `offset` to skip promotions. `limit` is not applied: you get the same promotions whatever `limit` you send, and `pagination.limit` shows the collection's own limit. Add `field_metadata=true` to also get a description of each promotion field, the values `rule` and `position` accept, and the most promotions the collection holds, as `max_items`.",
        "parameters": [OFFSET, LIMIT, FIELD_METADATA_PROMOTIONS],
        "responses": {
            "200": {
                "description": "The promotions and the `pagination` block. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": {
                    "product_promotions": {"type": "array", "items": ref("ProductPromotion")},
                    "pagination": ref("ProductPromotionPagination"),
                    "field_metadata": ref("ProductPromotionFieldMetadata"),
                }},
                "example": {"product_promotions": [SAMPLE_PROMOTION, SECOND_PROMOTION], "pagination": SAMPLE_PAGINATION},
            },
        },
        "example_call": {},
    },
    {
        "key": "create_search_result_page_product_promotion",
        "slug": "create-a-product-promotion",
        "title": "Create a product promotion",
        "method": "POST",
        "path": BASE + "/product_promotion",
        "summary": "Creates a product promotion and returns it with its `id`, which other calls take as `promotion_id`.",
        "description": "Creates a promotion from a body wrapped in `product_promotion`, in which `name`, `rule` and `position` are required. Returns `201` with the new promotion, including the `id` the other promotion calls take as `promotion_id`. Fields you leave out get their defaults: `is_active` and `is_always_available` both default to `true`. The response has no `Location` header.",
        "body": {
            "schema": {"type": "object", "required": ["product_promotion"], "properties": {"product_promotion": ref("ProductPromotionInput")}},
            "example": {"product_promotion": {"name": "Spring campaign", "rule": "all_search_result", "position": "top"}},
        },
        "responses": {
            "201": {"description": "The new promotion.", "schema": PROMOTION_RESPONSE, "example": {"product_promotion": CREATED_PROMOTION}},
            "400": {
                "description": "The body is not wrapped in `product_promotion`, or leaves out `name`, `rule` or `position` (for example `name is required`). Or a value is not accepted: `invalid enum value for rule`, `invalid enum value for position`, `keywords are required when rule is keywords` (`rule` is `if_matches_specific_keywords` and `specific_keywords` is missing), `product_ids must be an array of integers`, or `unknown product id` when a product `id` in `product_ids` matches no product in your store.",
                "schema": ERROR,
                "example": NAME_REQUIRED,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_search_result_page_product_promotion",
        "slug": "retrieve-a-product-promotion",
        "title": "Retrieve a product promotion",
        "method": "GET",
        "path": BASE + "/product_promotion/{promotion_id}",
        "summary": "Returns the product promotion whose `id` you pass as `promotion_id`.",
        "description": "Returns one promotion under the `product_promotion` key, with the same fields as a listing row. Returns `404 not_found` when no promotion has that `promotion_id`, including a promotion you deleted.",
        "parameters": [PROMOTION_ID],
        "responses": {
            "200": {"description": "The promotion.", "schema": PROMOTION_RESPONSE, "example": {"product_promotion": SAMPLE_PROMOTION}},
            "404": {"description": "No promotion has that `promotion_id`. The message is `Product promotion not found: <promotion_id>`, ending with the `promotion_id` you sent.", "schema": ERROR, "example": RETRIEVE_NOT_FOUND},
        },
        "example_call": {"path": {"promotion_id": 4}},
    },
    {
        "key": "patch_search_result_page_product_promotion",
        "slug": "update-a-product-promotion",
        "title": "Update a product promotion",
        "method": "PATCH",
        "path": BASE + "/product_promotion/{promotion_id}",
        "summary": "Changes the promotion fields you send and returns the whole promotion.",
        "description": "Send the fields to change wrapped in `product_promotion`, as on create. Only the fields you send change; the others keep their stored values. Returns the whole promotion after the change.",
        "parameters": [PROMOTION_ID],
        "body": {
            "schema": {"type": "object", "required": ["product_promotion"], "properties": {"product_promotion": ref("ProductPromotionUpdate")}},
            "example": {"product_promotion": {"position": "bottom"}},
        },
        "responses": {
            "200": {"description": "The whole promotion after the change.", "schema": PROMOTION_RESPONSE, "example": {"product_promotion": MOVED_PROMOTION}},
        },
        "example_call": {"path": {"promotion_id": 6}},
    },
    {
        "key": "patch_search_result_page_product_promotion_active",
        "slug": "turn-a-product-promotion-on-or-off",
        "title": "Turn a product promotion on or off",
        "method": "PATCH",
        "path": BASE + "/product_promotion/{promotion_id}/active",
        "summary": "Turns a product promotion on or off and returns the whole promotion.",
        "description": "Send `{\"product_promotion\": {\"is_active\": false}}` to turn the promotion off, or `true` to turn it on; `is_active` is required. Every other field in the body is ignored. Returns the whole promotion after the change. This path takes only `PATCH`: a `GET` of it is rejected with `405 method_not_allowed`.",
        "parameters": [PROMOTION_ID],
        "body": {
            "schema": {"type": "object", "required": ["product_promotion"], "properties": {"product_promotion": {"type": "object", "required": ["is_active"], "properties": {
                "is_active": {"type": "boolean", "description": "`true` to turn the promotion on, `false` to turn it off. Any other field you send is ignored."},
            }}}},
            "example": {"product_promotion": {"is_active": False}},
        },
        "responses": {
            "200": {"description": "The whole promotion after the change.", "schema": PROMOTION_RESPONSE, "example": {"product_promotion": PAUSED_PROMOTION}},
        },
        "example_call": {"path": {"promotion_id": 6}},
    },
    {
        "key": "delete_search_result_page_product_promotion",
        "slug": "delete-a-product-promotion",
        "title": "Delete a product promotion",
        "method": "DELETE",
        "path": BASE + "/product_promotion/{promotion_id}",
        "summary": "Deletes a product promotion permanently and returns `204` with no body.",
        "description": "Deletes the promotion permanently and returns `204` with no body. The promotion leaves the listing, and retrieving the same `promotion_id` then returns `404 not_found`.",
        "parameters": [PROMOTION_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No promotion has that `promotion_id`. The message is `Product promotion not found`.", "schema": ERROR, "example": PROMOTION_NOT_FOUND},
        },
        "example_call": {"path": {"promotion_id": 6}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def whole(description):
    return {"type": "integer", "description": description}


def text(description):
    return {"type": "string", "description": description}


def text_or_null(description):
    return {"type": ["string", "null"], "description": description}


PROMOTION_FIELDS = {
    "name": text("The promotion's name."),
    "rule": text("Which searches show the promotion, such as `all_search_result`, or `if_matches_specific_keywords` to match the promotion's `specific_keywords`. Required on create. The listing's `field_metadata` gives every accepted value in `allowed_values`. A create with any other value is rejected with `400` and `invalid enum value for rule`."),
    "position": text("Where the promotion shows on the search result page, such as `top` or `bottom`. Required on create. The listing's `field_metadata` gives every accepted value in `allowed_values`. A create with any other value is rejected with `400` and `invalid enum value for position`."),
    "specific_keywords": text_or_null("The keywords for the `if_matches_specific_keywords` rule, which requires them. An empty string or `null` when not set."),
    "is_active": flag("Whether the promotion is on. Defaults to `true` on create."),
    "is_always_available": flag("Whether the promotion is always available. Defaults to `true` on create. When it is `false`, the listing's `field_metadata` marks `available_from_date` and `available_to_date` as required."),
    "available_from_date": text_or_null("The start of the promotion's availability, or `null`."),
    "available_to_date": text_or_null("The end of the promotion's availability, or `null`."),
    "product_ids": {"type": "array", "items": {"type": "integer"}, "description": "The products in the promotion, as a list of product `id`s. On create, a value that is not a list of integers is rejected with `400` and `product_ids must be an array of integers`, and a product `id` that matches no product in your store with `400` and `unknown product id`."},
}

SCHEMAS = {
    "SearchResultPageSettings": {"type": "object", "properties": {
        "product_information": ref("SearchResultProductInformation"),
        "seo": ref("SearchResultSeo"),
        "product_promotion": ref("SearchResultPromotionMarker"),
        "reinitialise": ref("SearchResultReinitialise"),
    }},
    "SearchResultProductInformation": {"type": "object", "description": "Each search result, and how the result list displays, pages and sorts. The only section you can write.", "properties": {
        "use_default_product_listing_configurations": flag("Use the store's default product listing settings for the search result page."),
        "product_interaction_buttons": ref("SearchResultInteractionButtons"),
        "display_content_page": flag("Show content pages on the search result page."),
        "number_of_searches_per_result": ref("SearchResultItemsPerPage"),
        "display_short_description": flag("Show each product's short description."),
        "display_variations_combination": flag("Show each product's variation combinations."),
        "set_product_display_preferences": ref("SearchResultDisplayPreferences"),
        "set_product_sorting": ref("SearchResultDefaultSorting"),
        "configure_sorting_options": ref("SearchResultSortingOptions"),
        "display_loyalty_points": flag("Show loyalty points on each result."),
        "display_price": ref("SearchResultDisplayPrice"),
        "label_for_price": text("The label for the price."),
    }},
    "SearchResultInteractionButtons": {"type": "object", "description": "The buttons each search result shows.", "properties": {
        "enabled": flag("Show the interaction buttons."),
        "display_add_to_cart_button": flag("Show the Add to Cart button."),
        "display_add_to_compare_button": flag("Show the Add to Compare button."),
        "display_add_to_wishlist_button": flag("Show the Add to Wishlist button."),
        "display_view_details_button": flag("Show the View Details button."),
        "display_on_hover": flag("Show the buttons on hover."),
        "display_quick_view_button": flag("Show the Quick View button."),
    }},
    "SearchResultItemsPerPage": {"type": "object", "description": "Whether the results are paged, and how many items a page shows.", "properties": {
        "enabled": flag("Page the search results."),
        "items_per_page": {"type": "integer", "minimum": 5, "description": "Items per page. At least `5`: a lower value is rejected with `400` and `items_per_page must be >= 5`, and a number with a fraction with `400` and `must be an integer`."},
    }},
    "SearchResultDisplayPreferences": {"type": "object", "description": "How the results load, and where the pagination control shows.", "properties": {
        "enabled": flag("Apply the display preferences in this block."),
        "display_mode": text("How the results load, such as `pagination`. A value the store does not accept is rejected with `400` and `invalid enum value for display_mode`."),
        "select_pagination_position": text("Where the pagination control shows, such as `bottom`. A value the store does not accept is rejected with `400` and `invalid enum value for select_pagination_position`."),
        "number_of_products_per_page": whole("Products per page."),
        "allow_users_to_select_number_of_products": flag("Let shoppers choose how many products a page shows."),
        "number_of_products_per_load": whole("Products added each time a shopper loads more."),
    }},
    "SearchResultDefaultSorting": {"type": "object", "description": "Whether a default sort order applies, and which one.", "properties": {
        "enabled": flag("Apply a default sort order."),
        "default_sort": text("The default sort order, such as `alpha_asc`. A value the store does not accept is rejected with `400` and `invalid enum value for default_sort`."),
    }},
    "SearchResultSortingOptions": {"type": "object", "description": "The sort orders a shopper can switch to.", "properties": {
        "enabled": flag("Show the sort options."),
        "alphabetical": flag("Offer alphabetical sorting."),
        "featured": flag("Offer featured sorting."),
        "new": flag("Offer sorting by new products."),
        "top_selling": flag("Offer top selling sorting."),
        "price": flag("Offer price sorting."),
        "created_date": flag("Offer created date sorting."),
    }},
    "SearchResultDisplayPrice": {"type": "object", "description": "Whether a result shows a price, and which price.", "properties": {
        "enabled": flag("Show the price."),
        "display_expect_to_pay_price": flag("Show the expect to pay price."),
        "show_tax_with_the_expect_to_pay_price": flag("Include tax in the expect to pay price."),
    }},
    "SearchResultSeo": {"type": "object", "description": "Read-only. This page's SEO is managed at `/api/v4/admin/seo-settings`, the `href` in `group_meta.seo`.", "properties": {
        "read_only": flag("`true`: you cannot write this section."),
        "page_kind": text("The kind of page: `search_result`."),
    }},
    "SearchResultReinitialise": {"type": "object", "description": "Read-only. It describes the search reindex action at `/api/v4/admin/search/reindex`, the `href` in `group_meta.reinitialise`.", "properties": {
        "action": text("Returned as `POST`."),
    }},
    "SearchResultPromotionMarker": {"type": "object", "description": "Returned in place of the promotions, which the settings do not include. Use [List product promotions](" + LIST_PAGE + ") to get them.", "properties": {
        "read_only": flag("Returned as `true`."),
    }},
    "SearchResultGroupMeta": {"type": "object", "description": "One entry per section, plus one for the promotions. Only [Get search result page settings](" + PAGE + "get-search-result-page-settings) and [Update search result page settings](" + PAGE + "update-search-result-page-settings) return it.", "properties": {
        "product_information": ref("SearchResultSectionMeta"),
        "seo": ref("SearchResultSectionMeta"),
        "product_promotion": ref("SearchResultSectionMeta"),
        "reinitialise": ref("SearchResultSectionMeta"),
    }},
    "SearchResultSectionMeta": {"type": "object", "properties": {
        "kind": text("What the entry is: `setting` for `product_information` and `seo`, `resource` for `product_promotion`, and `action` for `reinitialise`."),
        "writable": flag("Whether you can write it: `true` for `product_information` and `product_promotion`, `false` for `seo` and `reinitialise`."),
        "ui_label": text("The entry's label, such as `Product Information`."),
        "href": text("Where it is managed. For `seo` this is `/api/v4/admin/seo-settings`, and for `reinitialise` it is `/api/v4/admin/search/reindex`. The other two point to their own paths here."),
    }},
    "SearchResultFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Describes each field. Returned only when you send `field_metadata=true`."},
    "ProductPromotion": {"type": "object", "properties": dict(
        {"id": {"type": "integer", "description": "The product promotion's `id`, assigned by the store. The other promotion calls take it as `promotion_id`."}},
        **PROMOTION_FIELDS,
        created={"type": "string", "format": "date-time", "description": "When the promotion was created."},
        updated={"type": "string", "format": "date-time", "description": "When the promotion was last changed."},
    )},
    "ProductPromotionInput": {"type": "object", "required": ["name", "rule", "position"], "properties": PROMOTION_FIELDS},
    "ProductPromotionUpdate": {"type": "object", "description": "Send only the fields that change.", "properties": PROMOTION_FIELDS},
    "ProductPromotionFieldMetadata": {"type": "object", "description": "Returned only when you send `field_metadata=true`.", "properties": {
        "fields": {"type": "object", "additionalProperties": True, "description": "One entry per promotion field, keyed by field name: every field except the promotion's `id`, `created` and `updated`. The entries for `rule` and `position` list the values they accept in `allowed_values`."},
        "group_meta": {"type": "object", "properties": {"product_promotion": {"type": "object", "properties": {
            "kind": text("What the entry is: `resource`."),
            "writable": flag("Whether you can write the promotions: `true`."),
            "max_items": {"type": "integer", "description": "The most promotions the collection holds. The `group_meta` returned with the settings does not include it."},
        }}}},
    }},
    "ProductPromotionPagination": {"type": "object", "properties": {
        "total": whole("The number of promotions in the collection."),
        "limit": whole("The collection's own limit, such as `20`. It does not change with the `limit` you send."),
        "offset": whole("The number of promotions skipped before this page."),
        "count": whole("The number of promotions on this page."),
        "current_page": whole("The current page number."),
        "total_pages": whole("The number of pages."),
        "has_next": flag("Whether there is a next page."),
        "has_previous": flag("Whether there is a previous page."),
        "previous_page": text_or_null("The URL of the previous page, or `null` when `has_previous` is `false`."),
        "next_page": text_or_null("The next page, or `null` on the last page."),
    }},
    "SearchResultPageError": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": text("A machine-readable reason, such as `invalid_request`, `not_found`, `method_not_allowed` or `rate_limited`."),
            "message": text("What went wrong, such as `seo is a read-only section`."),
            "details": {"type": "array", "items": {"type": "object"}, "description": "More detail, or an empty list."},
            "request_id": text("Identifies this request."),
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Read and change how your store's search result page shows products, and create, change and delete its product promotions."
INTRO = "The Search result page API has eleven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/page_settings/search_result_page`."
WARNING = (
    "A section read and a section write use different wrappers. `GET /search_result_page/{section}`\n"
    "  returns the section inside `search_result_page`, such as `{\"search_result_page\": {\"seo\": {...}}}`,\n"
    "  not under the section's own key. `PATCH /search_result_page/{section}` takes the fields wrapped in\n"
    "  the section's own key, such as `{\"product_information\": {...}}`, and also accepts them wrapped in\n"
    "  `search_result_page` and then `product_information`. A body with no wrapper is rejected with\n"
    "  `400 invalid_request`."
)
NOTES = [
    "**Only `product_information` can be written.** `group_meta` marks `seo` and `reinitialise` as\n"
    "  `writable: false`, and its `href` for each points to where it is managed: `/api/v4/admin/seo-settings`\n"
    "  for this page's SEO, and `/api/v4/admin/search/reindex` for the search reindex. A write to `seo` is\n"
    "  rejected with `400` and `seo is a read-only section`, and a write to `reinitialise` with `400` and\n"
    "  `reinitialise is not a writable setting`.",
    "**The promotions are a collection, not a settings section.** Reading the settings returns\n"
    "  `product_promotion` as `{\"read_only\": true}` only. [List product promotions](" + LIST_PAGE + ")\n"
    "  returns them under `product_promotions` with a `pagination` block. The listing ignores `limit`: send\n"
    "  `offset` to skip promotions. Each promotion's `id` is the `promotion_id` the other promotion calls take.",
    "**The promotion collection has a cap.** Send `field_metadata=true` to the listing to read it as\n"
    "  `field_metadata.group_meta.product_promotion.max_items`; the `group_meta` returned with the settings\n"
    "  does not include it. Every promotion in the store counts towards the cap, so delete promotions you no\n"
    "  longer need.",
    "**`PATCH` is the only way to change settings, and it changes only the fields you send.** Fields you\n"
    "  leave out keep their stored values, including the other fields inside a nested block such as\n"
    "  `product_interaction_buttons`. The settings path and each section path allow only `GET`, `HEAD`,\n"
    "  `PATCH` and `OPTIONS`, as their `Allow` header shows: `PUT`, `POST` or `DELETE` on the settings, or\n"
    "  `PUT` on a section, returns `405 method_not_allowed`.",
    "**Settings writes share one rate limit.** Writes to the settings and to each section count against\n"
    "  one allowance. Once it is spent, a write is rejected with `429 rate_limited` and a `Retry-After`\n"
    "  header that counts down the time left. A retry counts as another write, so wait until `Retry-After`\n"
    "  has passed. Promotion writes have a separate allowance.",
]
