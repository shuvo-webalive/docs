"""The Product page settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Product page"
SLUG = "product-page"
BASE = "/admin/settings/page_settings/product_page"
ICON = "box-open"

SECTIONS = ["configuration", "variations", "image_and_video", "up_sell", "related_products", "review_and_ratings", "quick_view"]

GET_PAGE = "/api-reference/product-page/get-product-page-settings"

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `configuration`, `variations`, `image_and_video`, `up_sell`, `related_products`, `review_and_ratings` or `quick_view`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "up_sell"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in all seven sections, keyed by section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name and nested the way the section is. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_CONFIGURATION = {
    "actions_buttons": {
        "show_product_action_buttons": True, "display_add_to_cart_button": True, "display_buy_now_button": True,
        "display_on_hover": True, "display_add_to_compare_button": True, "display_add_to_wishlist_button": True,
    },
    "details": {
        "display_description": True, "display_sale_percentage": True,
        "use_strike_through_on_previous_price": True, "display_tax_with_expect_to_pay_price": True,
    },
    "social_sharing": {
        "enable_share_on_social_media": True, "facebook": True, "twitter": True, "pinterest": True, "messenger": True,
        "linkedin": True, "email": True, "snapchat": True, "telegram": True, "reddit": True, "instagram": True,
        "youtube": True, "tiktok": True, "threads": False, "whatsapp": True, "bluesky": False, "mastodon": False,
        "copy_link": False, "display_title": False, "title": "",
    },
    "set_product_properties": {
        "display_height": True, "display_width": True, "display_length": True, "display_weight": True,
        "display_add_to_gift_registry": True,
    },
}

SAMPLE_VARIATIONS = {
    "labels_and_display": {
        "disable_variation_label_for_price": True, "display_product_image_as_variation_icons": True,
        "display_selected_variation_value": True, "enable_colour_type_variation_image_display": True,
        "use_strike_through_for_out_of_stock_variations": True, "enable_single_click_variation_loading": True,
    },
    "layout": {
        "select_variation_view": True,
        "select_variation_view_type": "matrix_view",
        "display_variation_combinations": True,
        "variation_combinations": [{"id": 4, "name": "Colour"}, {"id": 46, "name": "Size"}],
        "variation_price_display_mode": True,
        "variation_price_display_type": "lowest",
    },
}

SAMPLE_IMAGE_AND_VIDEO = {
    "allow_single_file_upload_per_product": True,
    "image_display": {
        "enable_image_slider": True, "product_thumbnail_vertical_view": True, "product_image_view": True,
        "product_image_view_type": "enable_grid_view", "image_zoom_type": True, "zoom_type": "fade_in_out",
    },
    "video": {"enable_video_preview": True, "display_video_thumbnail_in_first_order": True},
}

SAMPLE_UP_SELL = {
    "number_of_products": 10, "allow_viewers_to_change_display_mode": False, "grid_view": True, "list_view": True,
    "tabular_view": True, "select_display_type": "image", "maximum_number_of_columns_per_row": 6,
    "maximum_number_of_columns_per_row_list": 2, "short_description": True, "display_on_hover": True,
    "display_add_to_cart_button": True, "display_add_to_compare_button": True, "display_add_to_wishlist_button": True,
    "price": True, "show_expect_to_pay_price": True, "display_rating": True, "display_review_count": True,
}

SAMPLE_RELATED_PRODUCTS = dict(SAMPLE_UP_SELL, number_of_products=20, maximum_number_of_columns_per_row=4)

SAMPLE_REVIEW_AND_RATINGS = {"capabilities": {"available": True}, "enable_review_in_tab": True, "enable_new_version": True}

SAMPLE_QUICK_VIEW = {
    "product_quick_view": True, "display_product_name": True, "display_sku": True, "display_product_rating": True,
    "display_product_stock": True, "display_product_variation": True, "display_product_image": True,
    "display_variation_image": True, "display_product_summary": True, "display_add_to_cart_button": True,
    "display_add_to_compare_button": True, "display_add_to_wishlist_button": True,
}

SAMPLE_SETTINGS = {
    "configuration": SAMPLE_CONFIGURATION,
    "variations": SAMPLE_VARIATIONS,
    "image_and_video": SAMPLE_IMAGE_AND_VIDEO,
    "up_sell": SAMPLE_UP_SELL,
    "related_products": SAMPLE_RELATED_PRODUCTS,
    "review_and_ratings": SAMPLE_REVIEW_AND_RATINGS,
    "quick_view": SAMPLE_QUICK_VIEW,
}

UI_LABELS = {
    "configuration": "Product Configuration",
    "variations": "Product Variations",
    "image_and_video": "Image and Video",
    "up_sell": "Up-sell",
    "related_products": "Related Products",
    "review_and_ratings": "Review and Ratings",
    "quick_view": "Product Quick View",
}


def section_meta(section):
    meta = {"kind": "setting", "writable": True}
    if section == "review_and_ratings":
        meta.update(plugin="product-review", available=True)
    meta.update(ui_label=UI_LABELS[section], href="/api/v4" + BASE + "/" + section)
    return meta


SAMPLE_GROUP_META = {section: section_meta(section) for section in SECTIONS}

SAMPLE_PRODUCT_PAGE = {"product_page": SAMPLE_SETTINGS, "group_meta": SAMPLE_GROUP_META}

REQUEST_ID = "3b8e1f2a-6c4d-4e7f-9a15-0d2c8b6e4f71"


def error_example(code, message, details):
    return {"error": {"code": code, "message": message, "details": details, "request_id": REQUEST_ID}}


UNKNOWN_FIELD = error_example("invalid_request", "display_sku: not a recognized field",
                              [{"field": "display_sku", "code": "unknown_field", "message": "not a recognized field"}])
WRAPPER_REQUIRED = error_example("invalid_request", "request body must be wrapped in a 'configuration' object",
                                 [{"field": "configuration", "code": "required", "message": "the request body must be wrapped in a 'configuration' object"}])
UNKNOWN_SECTION = error_example("not_found", "Unknown page-settings section: product_page/bogus", [])

ERROR = {"$ref": "#/components/schemas/Error"}

AREA_RESPONSE = {"type": "object", "properties": {
    "product_page": {"$ref": "#/components/schemas/ProductPageSettings"},
    "group_meta": {"$ref": "#/components/schemas/ProductPageGroupMeta"},
}}

SECTION_RESPONSE = {"type": "object", "properties": {
    "product_page": {"$ref": "#/components/schemas/ProductPageSettings", "description": "Holds only the section named in the path."},
}}

DEPENDS_ERROR = "sets a field to `true` while the field in its `depends_on` is off (`constraint_violation`, naming both fields)"

VALUE_ERRORS = (
    "tries to change the read-only `review_and_ratings.capabilities.available` (`read_only`), "
    "or sends a value the field does not accept: the wrong type (`invalid_type`), a value outside `allowed_values` "
    "(`invalid_enum`) or a number outside `min` and `max` (`out_of_range`). `details[].code` gives the reason. "
    "A body that is not valid JSON, or that repeats a key, is rejected with the error `code` `malformed_json`."
)

READ_LIMITED = {"description": "Too many reads in a short time. After twenty reads in about one and a half seconds, the next read is rejected, and the `Retry-After` header says how long to wait. Writes are still accepted."}
WRITE_LIMITED = {"description": "Too many writes in a short time. After ten writes, the next one is rejected with the error `code` `rate_limited` and the message `Too many writes to this resource`. The `Retry-After` header counts down the seconds left before writes are accepted again. Reads still return `200`."}

ENDPOINTS = [
    {
        "key": "get_product_page",
        "slug": "get-product-page-settings",
        "title": "Get product page settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all seven product page settings sections and a `group_meta` block describing each one.",
        "description": "Returns every product page setting under `product_page`, with all seven sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, its `ui_label` and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All seven sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(AREA_RESPONSE["properties"], field_metadata={
                    "$ref": "#/components/schemas/ProductPageFieldMetadata",
                    "description": "Only when you send `field_metadata=true`. Keyed by section.",
                })},
                "example": SAMPLE_PRODUCT_PAGE,
            },
            "429": READ_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_product_page",
        "slug": "update-product-page-settings",
        "title": "Update product page settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all the settings.",
        "description": "Send the fields to change, grouped by section name, inside `product_page` or with no wrapper at all. Only the fields you send change: other fields in the same block, and every section you leave out, keep their stored values. One body can change several sections at once. Returns all the settings after the change, with `group_meta`, as [Get product page settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "description": "Wrap the sections in `product_page`, or send the section names at the top level with no wrapper. Send only the fields that change.", "properties": {
                "product_page": {"$ref": "#/components/schemas/ProductPageSettings", "description": "The fields to change, grouped by section."},
            }},
            "example": {"product_page": {"configuration": {"details": {"display_description": True}}, "up_sell": {"short_description": True}}},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": AREA_RESPONSE, "example": SAMPLE_PRODUCT_PAGE},
            "400": {
                "description": "A key at the top level of the body is not a section name, such as a field sent without its section (`unknown_field`), or the body " + DEPENDS_ERROR + ". `details[].code` gives the reason.",
                "schema": ERROR,
                "example": UNKNOWN_FIELD,
            },
            "429": WRITE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_product_page",
        "slug": "check-the-product-page-settings",
        "title": "Check the product page settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the product page settings are reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_product_page_section",
        "slug": "get-a-product-page-section",
        "title": "Get a product page section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section, such as `quick_view`, inside the `product_page` key.",
        "description": "Returns one section inside `product_page`, such as `{\"product_page\": {\"quick_view\": {...}}}`, without `group_meta`. This differs from [Category page](/category-page), where a section comes back under its own name. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section inside `product_page`.",
                "schema": {"type": "object", "properties": dict(SECTION_RESPONSE["properties"], field_metadata={
                    "$ref": "#/components/schemas/ProductPageFieldMetadata",
                    "description": "Only when you send `field_metadata=true`. Keyed by field name. It matches the section's part of the `field_metadata` that Get product page settings returns.",
                })},
                "example": {"product_page": {"quick_view": SAMPLE_QUICK_VIEW}},
            },
            "404": {"description": "No section has that name.", "schema": ERROR, "example": UNKNOWN_SECTION},
            "429": READ_LIMITED,
        },
        "example_call": {"path": {"section": "quick_view"}},
    },
    {
        "key": "patch_product_page_section",
        "slug": "update-a-product-page-section",
        "title": "Update a product page section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change wrapped in the section's own name, such as `{\"configuration\": {...}}`, or in `product_page` and then the section name. A body wrapped in anything else is rejected with `400 invalid_request`, and `details[0].field` names the section. Only the fields you send change; the rest keep their stored values. Returns the whole section after the change inside `product_page`, without `group_meta`.",
        "parameters": [SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the name of the section in the path, or in `product_page` and then that section name.", "properties": {
                "configuration": {"$ref": "#/components/schemas/ProductPageConfiguration"},
                "variations": {"$ref": "#/components/schemas/ProductPageVariations"},
                "image_and_video": {"$ref": "#/components/schemas/ProductPageImageAndVideo"},
                "up_sell": {"$ref": "#/components/schemas/ProductPageListing"},
                "related_products": {"$ref": "#/components/schemas/ProductPageListing"},
                "review_and_ratings": {"$ref": "#/components/schemas/ProductPageReviewAndRatings"},
                "quick_view": {"$ref": "#/components/schemas/ProductPageQuickView"},
                "product_page": {"$ref": "#/components/schemas/ProductPageSettings", "description": "The other accepted wrapper: `product_page`, then the section name."},
            }},
            "example": {"configuration": {"details": {"display_description": True}}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, inside `product_page`.", "schema": SECTION_RESPONSE, "example": {"product_page": {"configuration": SAMPLE_CONFIGURATION}}},
            "400": {
                "description": "The body is not wrapped in the section's name or in `product_page` (`required`), names a field the section does not have (`unknown_field`), " + DEPENDS_ERROR + ", " + VALUE_ERRORS,
                "schema": ERROR,
                "example": WRAPPER_REQUIRED,
            },
            "404": {"description": "No section has that name.", "schema": ERROR, "example": UNKNOWN_SECTION},
            "429": WRITE_LIMITED,
        },
        "example_call": {"path": {"section": "configuration"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def choice(values, description):
    return {"type": "string", "enum": values, "description": description}


def ref(name, description=None):
    schema = {"$ref": "#/components/schemas/" + name}
    if description:
        schema["description"] = description
    return schema


SHOW_BUTTONS = "Depends on `configuration.actions_buttons.show_product_action_buttons`."
IMAGE_VIEW = "Depends on `image_and_video.image_display.product_image_view`."
SHARE = "Depends on `configuration.social_sharing.enable_share_on_social_media`."
DISPLAY_MODE = "Depends on `allow_viewers_to_change_display_mode` in the same section."

SCHEMAS = {
    "ProductPageSettings": {"type": "object", "description": "The product page settings, one key per section.", "properties": {
        "configuration": ref("ProductPageConfiguration"),
        "variations": ref("ProductPageVariations"),
        "image_and_video": ref("ProductPageImageAndVideo"),
        "up_sell": ref("ProductPageListing", "The up-sell product listing."),
        "related_products": ref("ProductPageListing", "The related products listing."),
        "review_and_ratings": ref("ProductPageReviewAndRatings"),
        "quick_view": ref("ProductPageQuickView"),
    }},
    "ProductPageConfiguration": {"type": "object", "description": "What the product page itself shows, in four blocks.", "properties": {
        "actions_buttons": ref("ProductPageActionButtons"),
        "details": ref("ProductPageDetails"),
        "social_sharing": ref("ProductPageSocialSharing"),
        "set_product_properties": ref("ProductPageProductProperties"),
    }},
    "ProductPageActionButtons": {"type": "object", "description": "Which buttons the product page shows.", "properties": {
        "show_product_action_buttons": flag("Show the product action buttons."),
        "display_add_to_cart_button": flag("Show the Add to Cart button. " + SHOW_BUTTONS),
        "display_buy_now_button": flag("Show the Buy Now button. " + SHOW_BUTTONS),
        "display_on_hover": flag("Show the buttons on hover. " + SHOW_BUTTONS),
        "display_add_to_compare_button": flag("Show the Add to Compare button."),
        "display_add_to_wishlist_button": flag("Show the Add to Wishlist button."),
    }},
    "ProductPageDetails": {"type": "object", "description": "Which parts of the product's details show.", "properties": {
        "display_description": flag("Show the product description."),
        "display_sale_percentage": flag("Show the sale percentage."),
        "use_strike_through_on_previous_price": flag("Show the previous price struck through."),
        "display_tax_with_expect_to_pay_price": flag("Show tax with the expect to pay price."),
    }},
    "ProductPageSocialSharing": {"type": "object", "description": "The social media share buttons, the networks they offer, and the title beside them.", "properties": {
        "enable_share_on_social_media": flag("Show the social media share buttons."),
        "facebook": flag("Offer sharing on Facebook. " + SHARE),
        "twitter": flag("Offer sharing on Twitter. " + SHARE),
        "pinterest": flag("Offer sharing on Pinterest. " + SHARE),
        "messenger": flag("Offer sharing on Messenger."),
        "linkedin": flag("Offer sharing on LinkedIn."),
        "email": flag("Offer sharing by email."),
        "snapchat": flag("Offer sharing on Snapchat."),
        "telegram": flag("Offer sharing on Telegram."),
        "reddit": flag("Offer sharing on Reddit."),
        "instagram": flag("Offer sharing on Instagram."),
        "youtube": flag("Offer sharing on YouTube."),
        "tiktok": flag("Offer sharing on TikTok."),
        "threads": flag("Offer sharing on Threads."),
        "whatsapp": flag("Offer sharing on WhatsApp."),
        "bluesky": flag("Offer sharing on Bluesky."),
        "mastodon": flag("Offer sharing on Mastodon."),
        "copy_link": flag("Offer a button that copies the product link."),
        "display_title": flag("Show a title beside the share buttons."),
        "title": {"type": "string", "description": "The share title text."},
    }},
    "ProductPageProductProperties": {"type": "object", "description": "Whether the product page lists the product's height, width, length and weight, and whether it shows Add to Gift Registry.", "properties": {
        "display_height": flag("Show the product's height."),
        "display_width": flag("Show the product's width."),
        "display_length": flag("Show the product's length."),
        "display_weight": flag("Show the product's weight."),
        "display_add_to_gift_registry": flag("Show Add to Gift Registry."),
    }},
    "ProductPageVariations": {"type": "object", "description": "How a product's variations are labelled and laid out.", "properties": {
        "labels_and_display": ref("ProductPageVariationLabels"),
        "layout": ref("ProductPageVariationLayout"),
    }},
    "ProductPageVariationLabels": {"type": "object", "description": "How a variation is labelled and drawn.", "properties": {
        "disable_variation_label_for_price": flag("Turn off the variation label for the price."),
        "display_product_image_as_variation_icons": flag("Show product images as variation icons."),
        "display_selected_variation_value": flag("Show the selected variation value."),
        "enable_colour_type_variation_image_display": flag("Show images for colour type variations."),
        "use_strike_through_for_out_of_stock_variations": flag("Strike through variations that are out of stock."),
        "enable_single_click_variation_loading": flag("Load a variation with a single click."),
    }},
    "ProductPageVariationLayout": {"type": "object", "description": "How variations are laid out, and which price shows.", "properties": {
        "select_variation_view": flag("Turn on the variation view that `select_variation_view_type` names."),
        "select_variation_view_type": choice(["matrix_view", "flat_chooser", "advanced_view"], "The variation view: `matrix_view`, `flat_chooser` or `advanced_view`."),
        "display_variation_combinations": flag("Show variation combinations."),
        "variation_combinations": {"type": "array", "items": ref("ProductPageVariationType"), "description": "The variation types shown as combinations, each with the variation type's `id` and `name`."},
        "variation_price_display_mode": flag("Turn on the variation price display that `variation_price_display_type` names."),
        "variation_price_display_type": choice(["lowest", "highest"], "Which variation price shows: `lowest` or `highest`."),
    }},
    "ProductPageVariationType": {"type": "object", "description": "One variation type shown as a combination.", "properties": {
        "id": {"type": "integer", "description": "The variation type's `id`."},
        "name": {"type": "string", "description": "The variation type's name."},
    }},
    "ProductPageImageAndVideo": {"type": "object", "description": "Whether a product takes a single file upload, how product images show and zoom, and the video preview.", "properties": {
        "allow_single_file_upload_per_product": flag("Allow a single file upload per product."),
        "image_display": ref("ProductPageImageDisplay"),
        "video": ref("ProductPageVideo"),
    }},
    "ProductPageImageDisplay": {"type": "object", "description": "How product images are laid out and zoomed.", "properties": {
        "enable_image_slider": flag("Turn on the image slider. " + IMAGE_VIEW),
        "product_thumbnail_vertical_view": flag("Show product thumbnails in a vertical view. " + IMAGE_VIEW),
        "product_image_view": flag("Turn on the product image view that `product_image_view_type` names."),
        "product_image_view_type": choice(["default", "enable_split_slider", "enable_grid_view"], "The product image view: `default`, `enable_split_slider` or `enable_grid_view`."),
        "image_zoom_type": flag("Turn on the image zoom that `zoom_type` names. " + IMAGE_VIEW),
        "zoom_type": choice(["standard", "tints", "inner", "lens", "fade_in_out", "easing", "mousewheel", "mousewheel_inner", "mousewheel_lens"], "The image zoom effect."),
    }},
    "ProductPageVideo": {"type": "object", "description": "The video preview, and where its thumbnail sits.", "properties": {
        "enable_video_preview": flag("Turn on the video preview."),
        "display_video_thumbnail_in_first_order": flag("Show the video thumbnail first."),
    }},
    "ProductPageListing": {"type": "object", "description": "A product listing on the product page. `up_sell` and `related_products` have the same fields.", "properties": {
        "number_of_products": {"type": "integer", "minimum": 1, "maximum": 999999, "description": "The number of products the listing shows, from `1` to `999999`."},
        "allow_viewers_to_change_display_mode": flag("Let visitors change the display mode."),
        "grid_view": flag("Turn on the grid view. " + DISPLAY_MODE),
        "list_view": flag("Turn on the list view. " + DISPLAY_MODE),
        "tabular_view": flag("Turn on the tabular view. " + DISPLAY_MODE),
        "select_display_type": choice(["image", "list", "scrollable", "tabular"], "The display type: `image`, `list`, `scrollable` or `tabular`."),
        "maximum_number_of_columns_per_row": {"type": "integer", "enum": [1, 2, 3, 4, 5, 6], "description": "The most columns per row, from `1` to `6`."},
        "maximum_number_of_columns_per_row_list": {"type": "integer", "enum": [1, 2], "description": "The most columns per row in list view: `1` or `2`."},
        "short_description": flag("Show each product's short description."),
        "display_on_hover": flag("Show the buttons on hover."),
        "display_add_to_cart_button": flag("Show the Add to Cart button."),
        "display_add_to_compare_button": flag("Show the Add to Compare button."),
        "display_add_to_wishlist_button": flag("Show the Add to Wishlist button."),
        "price": flag("Show the price."),
        "show_expect_to_pay_price": flag("Show the expect to pay price. Depends on `price` in the same section."),
        "display_rating": flag("Show the product rating."),
        "display_review_count": flag("Show the review count. Depends on `display_rating` in the same section."),
    }},
    "ProductPageReviewAndRatings": {"type": "object", "description": "Where product reviews show, and which version shows them. The product review plugin backs this section.", "properties": {
        "capabilities": ref("ProductPageReviewCapabilities"),
        "enable_review_in_tab": flag("Show reviews in a tab."),
        "enable_new_version": flag("Show reviews with the new version. Depends on `review_and_ratings.enable_review_in_tab`."),
    }},
    "ProductPageReviewCapabilities": {"type": "object", "description": "What the product review plugin offers. Read-only.", "properties": {
        "available": {"type": "boolean", "readOnly": True, "description": "Whether the product review plugin is installed. Read-only: a write that changes it is rejected with `400` and the code `read_only`."},
    }},
    "ProductPageQuickView": {"type": "object", "description": "The product quick view popup and what it shows. Every field except `product_quick_view` depends on `quick_view.product_quick_view`.", "properties": {
        "product_quick_view": flag("Turn on the product quick view popup."),
        "display_product_name": flag("Show the product name."),
        "display_sku": flag("Show the SKU."),
        "display_product_rating": flag("Show the product rating."),
        "display_product_stock": flag("Show the product stock."),
        "display_product_variation": flag("Show the product variations."),
        "display_product_image": flag("Show the product image."),
        "display_variation_image": flag("Show the variation image."),
        "display_product_summary": flag("Show the product summary."),
        "display_add_to_cart_button": flag("Show the Add to Cart button."),
        "display_add_to_compare_button": flag("Show the Add to Compare button."),
        "display_add_to_wishlist_button": flag("Show the Add to Wishlist button."),
    }},
    "ProductPageGroupMeta": {"type": "object", "description": "One entry per section. Only [Get product page settings](" + GET_PAGE + ") and [Update product page settings](/api-reference/product-page/update-product-page-settings) return it.", "properties": {
        section: ref("ProductPageSectionMeta") for section in SECTIONS
    }},
    "ProductPageSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for all seven sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for all seven sections."},
        "plugin": {"type": "string", "description": "The plugin behind the section. Only `review_and_ratings` has it, set to `product-review`."},
        "available": {"type": "boolean", "description": "Whether that plugin is available. Only the entry that has `plugin` has it."},
        "ui_label": {"type": "string", "description": "The section's label, such as `Up-sell`."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/page_settings/product_page/up_sell`."},
    }},
    "ProductPageFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `ProductPageFieldMetadataEntry` in place of each value."},
    "ProductPageFieldMetadataEntry": {"type": "object", "properties": {
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does."},
        "type": {"type": "string", "description": "The kind of value the field takes: `boolean`, `enum`, `integer`, `string` or `reference_list`."},
        "default": {"description": "The field's default value."},
        "read_only": {"type": "boolean", "description": "Whether the field is read-only. `true` only on `review_and_ratings.capabilities.available`."},
        "depends_on": {"type": "string", "description": "The field this one depends on, such as `quick_view.product_quick_view`. In `up_sell` and `related_products` it is the field name alone, such as `display_rating`. A write that sets this field to `true` while that field is off is rejected with `400`."},
        "allowed_values": {"type": "array", "items": {}, "description": "The values the field accepts. Every `enum` field has it. On `variations.layout.variation_combinations` it lists the store's variation types, each with the variation type's `id` and `name`."},
        "labels": {"type": "object", "additionalProperties": {"type": "string"}, "description": "A label for each allowed value. Four `enum` fields have it: `image_and_video.image_display.product_image_view_type`, `image_and_video.image_display.zoom_type`, and `select_display_type` in `up_sell` and `related_products`."},
        "accepts": {"type": "string", "description": "The forms an item can take when you write the field. Only `variations.layout.variation_combinations` has it: the variation type's `id`, an object with its `id`, an object with its `id` and `name`, or its name in any letter case."},
        "min": {"type": "integer", "description": "The lowest value, for an `integer` field."},
        "max": {"type": "integer", "description": "The highest value, for an `integer` field."},
        "item_shape": {"type": "string", "description": "The shape of each item, for a `reference_list` field: `{id,name}`."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `malformed_json`, `not_found`, `method_not_allowed` or `rate_limited`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The rejected field, such as `configuration.details.display_description`."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `required`, `constraint_violation`, `read_only`, `invalid_type`, `invalid_enum` or `out_of_range`."},
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": {"type": "string", "description": "The identifier the store gives this request."},
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Read and change what your store's product pages show, from action buttons and variations to images, up-sells, reviews and quick view."
INTRO = "The Product page API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/page_settings/product_page`."
WARNING = (
    "**Sending a section back as you read it can be rejected.** Many fields depend on another field, as\n"
    "  `depends_on` in `field_metadata` shows. A write that sets such a field to `true` while the field it\n"
    "  depends on is off is rejected with `400 invalid_request` and the code `constraint_violation`, naming\n"
    "  both fields. That holds whether the field it depends on is already off or is set to `false` in the\n"
    "  same body. Setting a field to `false` does not change the fields that depend on it, so a stored\n"
    "  section can hold a pair of values that this rule rejects. Send only the fields you change."
)
NOTES = [
    "**The settings are split into seven sections.** They are `configuration`, `variations`,\n"
    "  `image_and_video`, `up_sell`, `related_products`, `review_and_ratings` and `quick_view`. Read or\n"
    "  write them all through `/product_page`, or one through `/product_page/{section}`. An unknown section\n"
    "  returns `404 not_found` on both `GET` and `PATCH`.",
    "**A section always comes back inside `product_page`.** Reading or writing `/product_page/quick_view`\n"
    "  returns `{\"product_page\": {\"quick_view\": {...}}}`, not `{\"quick_view\": {...}}`. This differs from\n"
    "  [Category page](/category-page). A section write accepts either wrapper: the section's own name, or\n"
    "  `product_page` and then the section name.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values at every level, and one body to `/product_page` can change several sections.\n"
    "  `PUT`, `POST` and `DELETE` are rejected on every product page path with `405 method_not_allowed` and\n"
    "  an `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Writes and reads have separate rate limits.** The eleventh write to a section in a short time is\n"
    "  rejected with `429 rate_limited` and a `Retry-After` header that counts down the seconds left. Until\n"
    "  then, writes to `/product_page` and to other sections are rejected too, while reads still return\n"
    "  `200`. After twenty reads in about one and a half seconds, the next read is rejected with `429` and\n"
    "  `Retry-After`, while writes are still accepted.",
    "**Add `field_metadata=true` to a read to get a description of every field.** The settings are still\n"
    "  returned with it. Each entry gives the field's `ui_label`, `description`, `type`, `default` and\n"
    "  `read_only`, plus `depends_on` when the field depends on another, `allowed_values` for every `enum`\n"
    "  field, and `min` and `max` for an `integer` field. On `/product_page` it is keyed by section; on a\n"
    "  section it is keyed by the section's field names. The only read-only field is\n"
    "  `review_and_ratings.capabilities.available`.",
]
