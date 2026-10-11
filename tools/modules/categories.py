"""The Categories endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Categories"
SLUG = "categories"
BASE = "/admin/categories"
ICON = "sitemap"

OVERVIEW_DESCRIPTION = "List, count, create, retrieve, replace, update and delete your store's product categories, check whether a name is taken, and read or update one section of a category at a time."
INTRO = "The Categories API has ten endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/categories`."

LIST_PAGE = "/api-reference/categories/list-categories"
CHECK_PAGE = "/api-reference/categories/check-a-category-name"
CREATE_PAGE = "/api-reference/categories/create-a-category"
RETRIEVE_PAGE = "/api-reference/categories/retrieve-a-category"
REPLACE_PAGE = "/api-reference/categories/replace-a-category"
UPDATE_PAGE = "/api-reference/categories/update-a-category"
SECTION_PAGE = "/api-reference/categories/retrieve-a-category-section"
SECTION_UPDATE_PAGE = "/api-reference/categories/update-a-category-section"

WARNING = (
    "**After a `404`, the next request that sends the same `JSESSIONID` cookie gets that `404` back instead of its own result.**\n"
    "  A read of a category that exists then returns `404`, and a delete returns the earlier `404`, such as\n"
    "  `Category already in trash`, and leaves the category in place. Send the request that follows a `404`\n"
    "  without that cookie."
)

NOTES = [
    "**A category has six sections, and every write wraps them in `category`.** The sections are\n"
    "  `general`, `description`, `images_media`, `availability_visibility`, `tax_shipping` and\n"
    "  `assign_products`, as in `{\"category\": {\"general\": {\"name\": \"Seasonal Produce\"}}}`.\n"
    "  [Retrieve a category section](" + SECTION_PAGE + ") and [Update a category section](" + SECTION_UPDATE_PAGE + ")\n"
    "  read or write one section at a time, and the update takes the same wrapper. A key that a section does\n"
    "  not have is rejected with `400`, with `details[0].code` set to `unknown_field`. So is an unknown key\n"
    "  beside the sections, except in a section update, which ignores everything but its own section. A key\n"
    "  beside `category` is ignored.",
    "**`PUT` resets most fields you leave out, and `PATCH` keeps them.**\n"
    "  [Replace a category](" + REPLACE_PAGE + ") sets the fields you leave out back to the values of a new\n"
    "  category, except `name`, `sku`, `url`, both images and the `tax_shipping` fields `tax_exempt`,\n"
    "  `tax_message`, `show_price_with_tax`, `prices_entered_with_tax` and `base_price_rounding`. A `PUT`\n"
    "  without `general.parent_category` therefore moves a child category to the top level, one without\n"
    "  `assign_products` removes all its products, and one without `tax_shipping.tax_profile` or\n"
    "  `tax_shipping.shipping_profile` sets that profile to `null`, even when it sends other `tax_shipping`\n"
    "  fields. [Update a category](" + UPDATE_PAGE + ") and [Update a category section](" + SECTION_UPDATE_PAGE + ")\n"
    "  change only the fields you send, except that a `products` list you send replaces the category's\n"
    "  products.",
    "**Deleting moves a category to the trash.** The category leaves the listing and the count, but\n"
    "  [Retrieve a category](" + RETRIEVE_PAGE + ") still returns it with `in_trash` set to `true`, and\n"
    "  [Check a category name](" + CHECK_PAGE + ") still reports its name as taken. Deleting it again returns\n"
    "  `404` with the message `Category already in trash`. No call restores a category from the trash or\n"
    "  deletes it permanently.",
    "**A create rejects only a name that a top-level category has.** [Create a category](" + CREATE_PAGE + ")\n"
    "  rejects that name with `409 conflict`, in any letter case and even when the top-level category is in\n"
    "  the trash, whatever parent you give the new category. A name that only child categories have is\n"
    "  accepted at any level, even under the same parent, and the new category's `url` gets a suffix such\n"
    "  as `-1` or `-2`. [Check a category name](" + CHECK_PAGE + ") returns `\"available\": false` for a name\n"
    "  any category has, anywhere in the tree or in the trash, so it can report a name as taken that a\n"
    "  create accepts.",
    "**A listing returns at most 20 categories per call, from every level of the tree.** A larger\n"
    "  `limit` is capped at `20`. To get the next categories, send a higher `offset` while\n"
    "  `pagination.has_next` is `true`. Send `parent` with the parent category's `id` to list only its\n"
    "  children. The listing ignores query parameters it does not know instead of rejecting them, so a\n"
    "  misspelled filter filters nothing.",
    "**Point to another record by its `id`, send images as a file name and base64 data, and send booleans as `true` or `false`.**\n"
    "  `parent_category`, `layout`, `tax_profile` and `shipping_profile` take `{\"id\": ...}`, and responses\n"
    "  return them as `{\"id\": ..., \"name\": ...}`. `selected_customers` takes customer and group `id`\n"
    "  values, and `assign_products.products` takes product `id` values. Send an image as\n"
    "  `{\"filename\": \"banner.png\", \"base64\": \"...\"}`: a `data:` URI string returns `500`, and no call\n"
    "  removes a stored image. A string such as `\"false\"`, or `null`, sent for a boolean returns `200`\n"
    "  and leaves the stored value unchanged.",
]

SECTIONS = ["general", "description", "images_media", "availability_visibility", "tax_shipping", "assign_products"]
SORT_VALUES = ["id", "name", "title", "sku", "url", "created", "updated"]
AVAILABLE_FOR = ["everyone", "customer", "selected"]
DEFAULT_SORTING = ["alpha_asc", "alpha_desc", "price_desc", "price_asc", "created_asc", "created_desc"]

CATEGORY_ID = {
    "name": "category_id",
    "in": "path",
    "required": True,
    "description": "The category's `id`, from a listing or from the response to creating the category.",
    "schema": {"type": "integer", "example": 4321},
}

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `general`, `description`, `images_media`, `availability_visibility`, `tax_shipping` or `assign_products`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "tax_shipping"},
}

LIMIT = {"name": "limit", "in": "query", "description": "The number of categories per page. Defaults to `20`, which is also the most you can get: a larger value is capped at `20`, and `pagination.limit` shows the value applied. `0`, negative values and values that are not numbers are rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 10}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of categories to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 10}}
PAGE = {"name": "page", "in": "query", "description": "A 1-based page number, read as `offset = (page - 1) * limit` against the `limit` applied, so `page=2` alone skips 20 categories. `pagination.next_page` and `pagination.previous_page` use `offset`, not `page`.", "schema": {"type": "integer", "example": 2}}
SORT = {"name": "sort", "in": "query", "description": "What to sort by: `id`, `name`, `title`, `sku`, `url`, `created` or `updated`. Values such as `created_on`, `last_updated_on` and `-id` are rejected with `400`. Sorting by `name` ignores letter case. Without `sort`, the most recently updated categories come first. `dir` defaults to `desc`, so `sort=name` alone sorts Z to A.", "schema": {"type": "string", "enum": SORT_VALUES, "example": "name"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`, in any letter case. Defaults to `desc`. Any other value is rejected with `400`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
NAME = {"name": "name", "in": "query", "description": "Keeps only categories whose name contains this text, in any letter case.", "schema": {"type": "string", "example": "seasonal"}}
SEARCH_TEXT = {"name": "searchText", "in": "query", "description": "Keeps only categories whose name or `sku` contains this text, in any letter case. Every `sku` the store generates starts with `CATEGORY-`, so a value such as `cat` matches every category whose `sku` the store generated.", "schema": {"type": "string", "example": "seasonal"}}
PARENT = {"name": "parent", "in": "query", "description": "The parent category's `id`. Keeps only that category's children, and `0` keeps none. A value that is not a number returns `500`.", "schema": {"type": "integer", "example": 4310}}
FIELD_METADATA_LIST = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key that describes every field of a category: its type, whether you can write it, whether a write must send it, and its limits or accepted values. The categories are still returned.", "schema": {"type": "boolean", "example": True}}

COUNT_NAME = dict(NAME, description="Counts only categories whose name contains this text, in any letter case.")
COUNT_SEARCH_TEXT = dict(SEARCH_TEXT, description="Counts only categories whose name or `sku` contains this text, in any letter case.")
COUNT_PARENT = dict(PARENT, description="The parent category's `id`. Counts only that category's children. A value that is not a number returns `500`.")

CHECK_NAME = {"name": "name", "in": "query", "required": True, "description": "The name to check. An empty or missing `name` is rejected with `400`.", "schema": {"type": "string", "example": "Seasonal Produce"}}

FIELD_METADATA_ROW = dict(FIELD_METADATA_LIST, description="Send `true` to add a `field_metadata` key that describes every field of a category: its type, whether you can write it, whether a write must send it, and its limits or accepted values. The category is still returned.")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def causes(*parts):
    text = "; ".join(parts[:-1]) + "; or " + parts[-1] + "."
    return text[0].upper() + text[1:]


ERROR_REF = ref("CategoryError")
SERVER_ERROR_REF = ref("CategoryServerError")
ROW_REF = ref("Category")
GROUP_META_REF = ref("CategoryGroupMeta")
FIELD_METADATA_REF = ref("CategoryFieldMetadata")
WRITE_BODY_REF = ref("CategoryWriteBody")

ROW_RESPONSE = {"type": "object", "properties": {"category": ROW_REF, "group_meta": GROUP_META_REF}}
SECTION_RESPONSE = {"type": "object", "properties": {"category": ref("CategorySection")}}

SERVER_ERROR_EXAMPLE = {"status": "error", "code": 500, "message": "Unexpected Error Occurred"}
SERVER_ERROR_BODY = "The body has no `error` object: it is `{\"status\": \"error\", \"code\": 500, \"message\": \"Unexpected Error Occurred\"}`."
PARENT_500 = {"description": "`parent` is not a number, such as `parent=abc`. " + SERVER_ERROR_BODY, "schema": SERVER_ERROR_REF, "example": SERVER_ERROR_EXAMPLE}
IMAGE_500 = {"description": "An image is a `data:` URI string instead of a `{filename, base64}` object. " + SERVER_ERROR_BODY, "schema": SERVER_ERROR_REF, "example": SERVER_ERROR_EXAMPLE}
UNKNOWN_SECTION_404 = {"description": "No section has that name: the `code` is `not_found` and the message is `Section not found`.", "schema": ERROR_REF}
NUMERIC_ID_400 = {"description": "`category_id` is not a number, such as `abc`. The message is `id: id must be numeric` and `details[0].code` is `invalid_type`.", "schema": ERROR_REF}
SECTION_READ_404 = {"description": "No category has that `category_id`, with the message `Category not found`, or no section has that name, with the message `Section not found`. The `code` is `not_found` in both cases.", "schema": ERROR_REF}

WRAPPER_400 = "the body is not wrapped in `category` (`category is required`)"
SECTION_KEY_400 = "a section has a key it does not accept, such as `images_media.image_url` (`<section>.<key>: is not a recognised category field`, and `details[0].code` is `unknown_field`)"
BESIDE_KEY_400 = "`category` has an unknown key beside the sections (`<key>: is not a recognised category field`)"
ENUM_400 = "`available_for` or `default_sorting` is not one of its values, `null` included (`details[0].code` is `invalid_enum`)"
TITLE_400 = "`general.title` is longer than 200 characters (`general.title: must be at most 200 characters`, and `details[0].code` is `too_long`)"
FILTER_PROFILE_400 = "`general.filter_profile` names a filter profile `id` on a store without the filter plugin (`general.filter_profile.id: not found`)"

PRODUCTS = [
    {"id": 101, "name": "Royal Gala Apples 1kg", "sku": "APPLE-GALA-1KG"},
    {"id": 102, "name": "Navel Oranges 1kg", "sku": "ORANGE-NAVEL-1KG"},
    {"id": 103, "name": "Butternut Pumpkin", "sku": "PUMPKIN-BUTTERNUT"},
]

PARENT_CATEGORY = {"id": 4310, "name": "Fresh Food"}

GROUP_META = {
    section: {"kind": "section", "writable": True, "href": "/api/v4" + BASE + "/{id}/" + section}
    for section in SECTIONS
}

AVAILABILITY_DEFAULTS = {
    "available": True,
    "visible": True,
    "available_for": "everyone",
    "selected_customers": {"customers": [], "groups": []},
    "available_on_date_range": False,
    "available_from_date": None,
    "available_to_date": None,
    "password_protected": False,
    "custom_sorting": False,
    "default_sorting": None,
    "disable_tracking": False,
}

CREATE_BODY = {
    "category": {
        "general": {
            "name": "Seasonal Produce",
            "title": "Seasonal Produce",
            "heading": "Fresh this season",
            "summary": "Fruit and vegetables picked this week",
            "parent_category": {"id": 4310},
        },
        "description": {"content": "<p>What is in season right now.</p>"},
        "availability_visibility": {"visible": True, "custom_sorting": True, "default_sorting": "alpha_asc"},
        "tax_shipping": {"tax_message": "Prices include GST"},
        "assign_products": {"products": [101, 102]},
    }
}

CREATED_CATEGORY = {
    "general": {
        "name": "Seasonal Produce",
        "title": "Seasonal Produce",
        "sku": "CATEGORY-5e0c7a91d2f",
        "url": "seasonal-produce",
        "heading": "Fresh this season",
        "parent_category": PARENT_CATEGORY,
        "filter_profile": None,
        "layout": None,
        "summary": "Fruit and vegetables picked this week",
    },
    "description": {"content": "<p>What is in season right now.</p>"},
    "images_media": {"image_url": "", "background_image_url": ""},
    "availability_visibility": dict(AVAILABILITY_DEFAULTS, custom_sorting=True, default_sorting="alpha_asc"),
    "tax_shipping": {
        "tax_exempt": False,
        "tax_profile": None,
        "tax_message": "Prices include GST",
        "show_price_with_tax": True,
        "prices_entered_with_tax": False,
        "base_price_rounding": "nearest",
        "enable_shipping": False,
        "shipping_profile": None,
    },
    "assign_products": {"products": PRODUCTS[:2]},
    "id": 4321,
    "disposable": False,
    "in_trash": False,
    "parent_in_trash": False,
    "created_by": "admin@example.com",
    "created_on": "2026-10-05T03:12:44Z",
    "last_updated_by": "",
    "last_updated_on": "2026-10-05T03:12:44Z",
}

SAMPLE_CATEGORY = copy.deepcopy(CREATED_CATEGORY)
SAMPLE_CATEGORY["tax_shipping"].update(
    tax_profile={"id": 3, "name": "GST"},
    enable_shipping=True,
    shipping_profile={"id": 12, "name": "Standard Shipping"},
)
SAMPLE_CATEGORY["last_updated_on"] = "2026-10-06T08:40:10Z"

SIBLING_CATEGORY = {
    "general": {
        "name": "Vegetables",
        "title": None,
        "sku": "CATEGORY-a41b8e2c903",
        "url": "vegetables",
        "heading": None,
        "parent_category": PARENT_CATEGORY,
        "filter_profile": None,
        "layout": None,
        "summary": None,
    },
    "description": {"content": None},
    "images_media": {"image_url": "", "background_image_url": ""},
    "availability_visibility": copy.deepcopy(AVAILABILITY_DEFAULTS),
    "tax_shipping": {
        "tax_exempt": False,
        "tax_profile": None,
        "tax_message": "",
        "show_price_with_tax": True,
        "prices_entered_with_tax": False,
        "base_price_rounding": "nearest",
        "enable_shipping": False,
        "shipping_profile": None,
    },
    "assign_products": {"products": PRODUCTS[2:]},
    "id": 4325,
    "disposable": False,
    "in_trash": False,
    "parent_in_trash": False,
    "created_by": "admin@example.com",
    "created_on": "2026-09-30T22:05:31Z",
    "last_updated_by": "",
    "last_updated_on": "2026-09-30T22:05:31Z",
}

SAMPLE_PAGINATION = {
    "total": 12, "limit": 10, "offset": 10, "count": 2, "current_page": 2, "total_pages": 2,
    "has_next": False, "has_previous": True,
    "previous_page": "https://your-store.example.com/api/v4/admin/categories?sort=name&dir=asc&limit=10&offset=0",
    "next_page": None,
}

REPLACE_BODY = {"category": {"general": {"name": "Seasonal Produce", "heading": "New heading"}}}

REPLACED_CATEGORY = copy.deepcopy(SAMPLE_CATEGORY)
REPLACED_CATEGORY["general"].update(title=None, heading="New heading", parent_category=None, layout=None, summary=None)
REPLACED_CATEGORY["description"] = {"content": None}
REPLACED_CATEGORY["availability_visibility"] = copy.deepcopy(AVAILABILITY_DEFAULTS)
REPLACED_CATEGORY["assign_products"] = {"products": []}
REPLACED_CATEGORY["tax_shipping"].update(tax_profile=None, enable_shipping=False, shipping_profile=None)
REPLACED_CATEGORY["last_updated_on"] = "2026-10-07T09:15:02Z"

UPDATE_BODY = {"category": {"general": {"summary": "Updated summary"}, "availability_visibility": {"visible": False}}}

UPDATED_CATEGORY = copy.deepcopy(SAMPLE_CATEGORY)
UPDATED_CATEGORY["general"]["summary"] = "Updated summary"
UPDATED_CATEGORY["availability_visibility"]["visible"] = False
UPDATED_CATEGORY["last_updated_on"] = "2026-10-07T09:15:02Z"

SECTION_UPDATE_BODY = {"category": {"assign_products": {"products": [101, 102, 103]}}}

ENDPOINTS = [
    {
        "key": "list_categories",
        "slug": "list-categories",
        "title": "List categories",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 categories per call, from every tree level, most recently updated first.",
        "description": "Returns your categories in `categories`, from every level of the tree in one list, 20 per call unless you send a lower `limit`. Categories in the trash are left out, and the most recently updated come first unless you send `sort`. Narrow the list with `name`, `searchText` and `parent`; a category must match every filter you send. Query parameters the listing does not know, such as `q` or `search`, are ignored instead of rejected.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, DIR, NAME, SEARCH_TEXT, PARENT, FIELD_METADATA_LIST],
        "responses": {
            "200": {
                "description": "The categories on this page in `categories`. `group_meta` gives the path of each of the six sections, and `pagination` gives the `total` that match your filters and the URLs of the previous and next pages. With `field_metadata=true`, a `field_metadata` key is added. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "categories": {"type": "array", "items": ROW_REF},
                    "group_meta": GROUP_META_REF,
                    "pagination": ref("CategoryPagination"),
                    "field_metadata": FIELD_METADATA_REF,
                }},
                "example": {"categories": [SAMPLE_CATEGORY, SIBLING_CATEGORY], "group_meta": GROUP_META, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "`limit` is `0` (`'limit' must be a positive integer`, and `details[0].code` is `out_of_range`), negative or not a number (`'limit' must be a non-negative integer`, and `details[0].code` is `invalid_integer`), or sent twice, such as `limit=1&limit=2` (`limit: must be supplied once, not repeated`, and `details[0].code` is `repeated_param`); `sort` is a value the listing does not accept, such as `created_on` (`Sort field not exist`, and `details[0].code` is `invalid_sort_field`); or `dir` is not `asc` or `desc` (`Sort order must be asc or desc`). After a rejected `sort`, the next listing request sent with the same `JSESSIONID` cookie can return this `400` again.",
                "schema": ERROR_REF,
            },
            "500": PARENT_500,
        },
        "example_call": {"query": "limit=10&offset=10&sort=name&dir=asc"},
    },
    {
        "key": "count_categories",
        "slug": "count-categories",
        "title": "Count categories",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns how many categories are outside the trash, narrowed by any filters you send.",
        "description": "Returns the number of categories as `count`, inside a `categories` object. Categories in the trash are not counted. `name`, `searchText` and `parent` narrow the count as they narrow [List categories](" + LIST_PAGE + "), so the count matches that listing's `pagination.total`. `limit`, `sort` and `field_metadata` are accepted and change nothing.",
        "parameters": [COUNT_NAME, COUNT_SEARCH_TEXT, COUNT_PARENT],
        "responses": {
            "200": {
                "description": "The number of categories, as `count` inside `categories`.",
                "schema": {"type": "object", "properties": {"categories": {"type": "object", "properties": {
                    "count": {"type": "integer", "description": "The number of categories outside the trash that match your filters."},
                }}}},
                "example": {"categories": {"count": 2}},
            },
            "500": PARENT_500,
        },
        "example_call": {"query": "searchText=seasonal"},
    },
    {
        "key": "check_category_name",
        "slug": "check-a-category-name",
        "title": "Check a category name",
        "method": "GET",
        "path": BASE + "/check-name",
        "summary": "Returns `available`: `false` when any category, even one in the trash, has the name.",
        "description": "Send the name as `name`; other query parameters, such as `parent`, are ignored. You get `\"available\": false` when any category has exactly that name, in any letter case, wherever it sits in the tree and even when it is in the trash. A leading space counts as part of the name and trailing spaces do not, so a name with a leading space can be reported as available while the name without it is taken. A create rejects only a name that a top-level category has, so [Create a category](" + CREATE_PAGE + ") can accept a name this call reports as taken.",
        "parameters": [CHECK_NAME],
        "responses": {
            "200": {
                "description": "`available` is `true` when no category has the name, and `false` when one does.",
                "schema": {"type": "object", "properties": {
                    "available": {"type": "boolean", "description": "`true` when no category, in the trash or not, has the name."},
                }},
                "example": {"available": False},
            },
            "400": {"description": "`name` is empty or missing. The `code` is `invalid_request` and the message is `name is required`.", "schema": ERROR_REF},
        },
        "example_call": {"query": "name=Seasonal%20Produce"},
    },
    {
        "key": "create_category",
        "slug": "create-a-category",
        "title": "Create a category",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a category and returns it with its `id`, which other calls take as `category_id`.",
        "description": "Wrap the sections in `category`; only `general.name` is required. Fields you leave out get their defaults: `available` and `visible` are `true`, `available_for` is `everyone`, and the category has no images and no products. The store generates the `sku`, and makes the `url` from the name, when you leave them out. A name that a top-level category has, in any letter case and even in the trash, is rejected; a name that only child categories have is accepted, and the new `url` gets a suffix such as `-1`.",
        "body": {"schema": WRITE_BODY_REF, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new category in `category`, with its `id`, `sku` and `url`, and `group_meta`. `parent_category` returns as `{id, name}` and each product as `{id, name, sku}`, and `created_on` equals `last_updated_on`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"category": CREATED_CATEGORY, "group_meta": GROUP_META},
            },
            "400": {"description": causes(
                "the body is not a JSON object (`request body must be a JSON object`)",
                WRAPPER_400,
                "`general.name` is missing (`general.name: Category name is required`, and `details[0].code` is `required`)",
                "`general.name` is not 2 to 255 characters long, such as `x` (`general.name: must be 2-255 characters`, and `details[0].code` is `out_of_range`)",
                SECTION_KEY_400,
                BESIDE_KEY_400,
                ENUM_400,
                TITLE_400,
                FILTER_PROFILE_400,
            ), "schema": ERROR_REF},
            "409": {"description": "A top-level category already has that name, in any letter case, even one in the trash, whatever parent you give the new category. The `code` is `conflict`, the message is `Category name already exists`, and `details[0].code` is `already_exists`.", "schema": ERROR_REF},
            "500": IMAGE_500,
        },
        "example_call": {},
    },
    {
        "key": "get_category",
        "slug": "retrieve-a-category",
        "title": "Retrieve a category",
        "method": "GET",
        "path": BASE + "/{category_id}",
        "summary": "Returns the category whose `id` you pass as `category_id`, with all six sections.",
        "description": "Returns the category under `category`, with its six sections and eight read-only fields, and `group_meta`. A category in the trash still returns `200`, with `in_trash` set to `true`. Send `field_metadata=true` to add a description of every field. The response has no `ETag` header.",
        "parameters": [CATEGORY_ID, FIELD_METADATA_ROW],
        "responses": {
            "200": {
                "description": "The category and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added.",
                "schema": {"type": "object", "properties": dict(ROW_RESPONSE["properties"], field_metadata=FIELD_METADATA_REF)},
                "example": {"category": SAMPLE_CATEGORY, "group_meta": GROUP_META},
            },
            "400": NUMERIC_ID_400,
            "404": {"description": "No category has that `category_id`. The message is `Category not found`. A `category_id` with a decimal point, such as `1.5`, also returns `404`, but as an HTML page from the web server instead of a JSON error.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"category_id": 4321}},
    },
    {
        "key": "update_category",
        "slug": "replace-a-category",
        "title": "Replace a category",
        "method": "PUT",
        "path": BASE + "/{category_id}",
        "summary": "Replaces a category: most fields you leave out reset, but `name`, `sku`, `url` and images stay.",
        "description": "Most fields you leave out go back to the values of a new category: `title`, `heading`, `summary`, `layout` and `description.content` become `null`, `availability_visibility` returns to its defaults, the category loses its products, and a child category without `general.parent_category` moves to the top level. `name`, `sku`, `url` and both images keep their values, so a new `name` leaves the `url` as it was. In `tax_shipping`, a `tax_profile` or `shipping_profile` you leave out becomes `null` whether or not you send that section, clearing the shipping profile sets `enable_shipping` to `false`, and the other fields keep their values. To change only the fields you send, use [Update a category](" + UPDATE_PAGE + ").",
        "parameters": [CATEGORY_ID],
        "body": {"schema": WRITE_BODY_REF, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The category after the replace, with `group_meta`.",
                "schema": ROW_RESPONSE,
                "example": {"category": REPLACED_CATEGORY, "group_meta": GROUP_META},
            },
            "400": {"description": causes(WRAPPER_400, SECTION_KEY_400, BESIDE_KEY_400, ENUM_400, TITLE_400, FILTER_PROFILE_400), "schema": ERROR_REF},
            "500": IMAGE_500,
        },
        "example_call": {"path": {"category_id": 4321}},
    },
    {
        "key": "patch_category",
        "slug": "update-a-category",
        "title": "Update a category",
        "method": "PATCH",
        "path": BASE + "/{category_id}",
        "summary": "Changes only the fields you send, in any number of sections, and returns the category.",
        "description": "Send the fields to change inside `category`, grouped by section; one body can change several sections. Every field you leave out keeps its value. The exception is `assign_products.products`: the list you send replaces the category's products. A body that is not wrapped in `category` is rejected with `400` and the message `category is required`.",
        "parameters": [CATEGORY_ID],
        "body": {"schema": WRITE_BODY_REF, "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The whole category after the change, with `group_meta`.",
                "schema": ROW_RESPONSE,
                "example": {"category": UPDATED_CATEGORY, "group_meta": GROUP_META},
            },
            "400": {"description": causes(WRAPPER_400, SECTION_KEY_400, BESIDE_KEY_400, ENUM_400, TITLE_400, FILTER_PROFILE_400), "schema": ERROR_REF},
            "500": IMAGE_500,
        },
        "example_call": {"path": {"category_id": 4321}},
    },
    {
        "key": "delete_category",
        "slug": "delete-a-category",
        "title": "Delete a category",
        "method": "DELETE",
        "path": BASE + "/{category_id}",
        "summary": "Moves a category to the trash. You can still retrieve it, but it leaves the listing.",
        "description": "Moves the category to the trash and returns `204` with no body. The category leaves the listing and the count, but [Retrieve a category](" + RETRIEVE_PAGE + ") still returns it with `in_trash` set to `true`, and [Check a category name](" + CHECK_PAGE + ") still reports its name as taken. Its child categories stay in the listing, with `parent_category` still naming it and `parent_in_trash` still `false`. No call restores a category from the trash or deletes it permanently.",
        "parameters": [CATEGORY_ID],
        "responses": {
            "204": {"description": "Moved to the trash. No body."},
            "404": {"description": "The category is already in the trash: the `code` is `not_found` and the message is `Category already in trash`. You also get `404`, with the message `Category not found`, when no category has that `category_id`. After any `404`, the next delete sent with the same `JSESSIONID` cookie returns that `404` and leaves its category in place.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"category_id": 4321}},
    },
    {
        "key": "get_category_section",
        "slug": "retrieve-a-category-section",
        "title": "Retrieve a category section",
        "method": "GET",
        "path": BASE + "/{category_id}/{section}",
        "summary": "Returns one section of a category, inside `category`, such as its `tax_shipping` settings.",
        "description": "Returns the section named in the path inside `category`, such as `{\"category\": {\"tax_shipping\": {...}}}`, with the same values as [Retrieve a category](" + RETRIEVE_PAGE + "). The response has no `group_meta`, and query parameters, `field_metadata` included, add nothing. A category in the trash still returns its sections. An unknown section returns `404` with the message `Section not found`.",
        "parameters": [CATEGORY_ID, SECTION],
        "responses": {
            "200": {
                "description": "The section inside `category`, without `group_meta`.",
                "schema": SECTION_RESPONSE,
                "example": {"category": {"tax_shipping": SAMPLE_CATEGORY["tax_shipping"]}},
            },
            "400": NUMERIC_ID_400,
            "404": SECTION_READ_404,
        },
        "example_call": {"path": {"category_id": 4321, "section": "tax_shipping"}},
    },
    {
        "key": "patch_category_section",
        "slug": "update-a-category-section",
        "title": "Update a category section",
        "method": "PATCH",
        "path": BASE + "/{category_id}/{section}",
        "summary": "Changes only the fields you send in one section and returns the whole section.",
        "description": "Wrap the fields in `category` and then in the section's name, such as `{\"category\": {\"assign_products\": {\"products\": [101, 102, 103]}}}`. A body with only the section's name, or no wrapper at all, is rejected with `400` and the message `<section> is required`. Fields you leave out keep their values, except `assign_products.products`, which the list you send replaces. Anything else inside `category`, such as another section, is ignored.",
        "parameters": [CATEGORY_ID, SECTION],
        "body": {"schema": WRITE_BODY_REF, "example": SECTION_UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The whole section after the change, inside `category`, without `group_meta`.",
                "schema": SECTION_RESPONSE,
                "example": {"category": {"assign_products": {"products": PRODUCTS}}},
            },
            "400": {"description": causes(
                "the body is `{\"<section>\": {...}}` or the bare fields, without `category` around them (`<section> is required`, such as `assign_products is required`)",
                SECTION_KEY_400,
                ENUM_400,
                TITLE_400,
                FILTER_PROFILE_400,
            ), "schema": ERROR_REF},
            "404": UNKNOWN_SECTION_404,
            "500": IMAGE_500,
        },
        "example_call": {"path": {"category_id": 4321, "section": "assign_products"}},
    },
]

SECTION_PROPERTIES = {
    "general": ref("CategoryGeneral"),
    "description": ref("CategoryDescription"),
    "images_media": ref("CategoryImagesMedia"),
    "availability_visibility": ref("CategoryAvailabilityVisibility"),
    "tax_shipping": ref("CategoryTaxShipping"),
    "assign_products": ref("CategoryAssignProducts"),
}

READ_ONLY_PROPERTIES = {
    "id": {"type": "integer", "description": "The category's `id`, assigned by the store. Pass it as `category_id` in a path."},
    "disposable": {"type": "boolean", "description": "A flag the store sets. You cannot write it."},
    "in_trash": {"type": "boolean", "description": "`true` after you delete the category, which moves it to the trash."},
    "parent_in_trash": {"type": "boolean", "description": "`false` even when the parent category is in the trash. To check the parent, retrieve it and read its `in_trash`."},
    "created_by": {"type": "string", "description": "Identifies who created the category, such as an email address. It can be `\"\"`."},
    "created_on": {"type": "string", "description": "When the category was created."},
    "last_updated_by": {"type": "string", "description": "Always `\"\"`."},
    "last_updated_on": {"type": "string", "description": "When the category last changed. On a new category it equals `created_on`. The listing puts the most recent first unless you send `sort`."},
}

METADATA_ENTRY_REF = ref("CategoryFieldMetadataEntry")

SCHEMAS = {
    "Category": {"type": "object", "description": "A category: six sections and eight read-only fields. A listing entry, a category read and the response to a create, replace or update have the same fields.", "properties": dict(SECTION_PROPERTIES, **READ_ONLY_PROPERTIES)},
    "CategorySection": {"type": "object", "description": "Holds only the section named in the path.", "properties": SECTION_PROPERTIES},
    "CategoryReference": {"type": ["object", "null"], "description": "A record the category links to, such as its parent category, as `{id, name}`, or `null` when none is set. In a write, send only the record's `id`.", "properties": {
        "id": {"type": "integer", "description": "The linked record's `id`, such as the parent category's `id`."},
        "name": {"type": "string", "description": "The linked record's name. Returned in responses."},
    }},
    "CategoryGeneral": {"type": "object", "description": "The category's name, title, `sku`, `url`, heading, parent, filter profile, layout and summary.", "properties": {
        "name": {"type": "string", "description": "The category's name. A create rejects a name that a top-level category has, in any letter case."},
        "title": {"type": ["string", "null"], "description": "The category's title, or `null`."},
        "sku": {"type": "string", "description": "The category's SKU. When you create the category without one, the store generates `CATEGORY-` followed by 11 hexadecimal characters."},
        "url": {"type": "string", "description": "The category's `url`, such as `seasonal-produce`. When you create the category without one, the store makes it from the name, adding a suffix such as `-1` when another category has the same name. A `PUT` that renames the category leaves it as it was."},
        "heading": {"type": ["string", "null"], "description": "The category's heading, or `null`."},
        "parent_category": dict(ref("CategoryReference"), description="The parent category as `{id, name}`, or `null` for a top-level category."),
        "filter_profile": {"type": ["object", "null"], "description": "The category's filter profile, which comes from the filter plugin. `null` on a store without the plugin."},
        "layout": dict(ref("CategoryReference"), description="The layout as `{id, name}`, or `null`."),
        "summary": {"type": ["string", "null"], "description": "The category's summary, or `null`."},
    }},
    "CategoryDescription": {"type": "object", "description": "The category's description. Responses and writes use the same field.", "properties": {
        "content": {"type": ["string", "null"], "description": "The description, or `null`."},
    }},
    "CategoryImagesMedia": {"type": "object", "description": "The URLs of the category's two images. To upload an image, send `images_media.image` or `images_media.background_image` in a write.", "properties": {
        "image_url": {"type": "string", "description": "The category image's URL, ending in the file name you uploaded, or `\"\"` when no image is set."},
        "background_image_url": {"type": "string", "description": "The background image's URL, in a `background/` folder and ending in the file name you uploaded, or `\"\"` when no background image is set."},
    }},
    "CategorySelectedCustomers": {"type": "object", "description": "The customers and groups the category is available to when `available_for` is `selected`.", "properties": {
        "customers": {"type": "array", "items": ref("CategoryReference"), "description": "Each customer as `{id, name}`. Empty on a new category."},
        "groups": {"type": "array", "items": ref("CategoryReference"), "description": "Each group as `{id, name}`. Empty on a new category."},
    }},
    "CategoryAvailabilityVisibility": {"type": "object", "description": "Whether the category is available and visible, to whom and when, with its password and sorting settings.", "properties": {
        "available": {"type": "boolean", "description": "Whether the category is available. `true` on a new category."},
        "visible": {"type": "boolean", "description": "Whether the category is visible. `true` on a new category."},
        "available_for": {"type": "string", "enum": AVAILABLE_FOR, "description": "Who the category is available to: `everyone`, `customer` or `selected`. With `selected`, it is available to the customers and groups in `selected_customers`. `everyone` on a new category."},
        "selected_customers": ref("CategorySelectedCustomers"),
        "available_on_date_range": {"type": "boolean", "description": "Turns on the date range set by `available_from_date` and `available_to_date`. `false` on a new category."},
        "available_from_date": {"type": ["string", "null"], "description": "The start of the date range, such as `2026-11-02T00:00:00Z`, or `null`."},
        "available_to_date": {"type": ["string", "null"], "description": "The end of the date range, such as `2026-11-20T00:00:00Z`, or `null`."},
        "password_protected": {"type": "boolean", "description": "Whether the category is password protected. `false` on a new category. The password itself is never returned."},
        "custom_sorting": {"type": "boolean", "description": "Turns custom sorting on for the category. `false` on a new category."},
        "default_sorting": {"type": ["string", "null"], "enum": DEFAULT_SORTING + [None], "description": "The category's default sort order: `alpha_asc`, `alpha_desc`, `price_desc`, `price_asc`, `created_asc` or `created_desc`. `null` on a new category."},
        "disable_tracking": {"type": "boolean", "description": "Turns tracking off for the category. `false` on a new category."},
    }},
    "CategoryTaxShipping": {"type": "object", "description": "The category's tax and shipping settings. Responses and writes use the same fields. A `PUT` sets a `tax_profile` or `shipping_profile` it leaves out to `null`, whether or not it sends this section; clearing the shipping profile sets `enable_shipping` to `false`.", "properties": {
        "tax_exempt": {"type": "boolean", "description": "Whether the category is tax exempt. `false` on a new category."},
        "tax_profile": dict(ref("CategoryReference"), description="The tax profile as `{id, name}`, or `null`. Send `{\"id\": ...}` to set it; a `name` beside the `id` is ignored."),
        "tax_message": {"type": "string", "description": "A message about tax, such as `Prices include GST`. `\"\"` on a new category."},
        "show_price_with_tax": {"type": "boolean", "description": "Whether prices show with tax. `true` on a new category."},
        "prices_entered_with_tax": {"type": "boolean", "description": "Whether prices are entered with tax. `false` on a new category."},
        "base_price_rounding": {"type": "string", "description": "How the base price is rounded. `nearest` on a new category."},
        "enable_shipping": {"type": "boolean", "description": "Whether shipping is on. `false` on a new category. Setting a `shipping_profile` sets it to `true`, and setting it to `false` clears `shipping_profile`, even a profile sent in the same body."},
        "shipping_profile": dict(ref("CategoryReference"), description="The shipping profile as `{id, name}`, or `null`. Send `{\"id\": ...}` to set it, which also sets `enable_shipping` to `true`."),
    }},
    "CategoryProduct": {"type": "object", "description": "A product assigned to the category.", "properties": {
        "id": {"type": "integer", "description": "The product's `id`."},
        "name": {"type": "string", "description": "The product's name."},
        "sku": {"type": "string", "description": "The product's SKU."},
    }},
    "CategoryAssignProducts": {"type": "object", "description": "The products assigned to the category.", "properties": {
        "products": {"type": "array", "items": ref("CategoryProduct"), "description": "Each product as `{id, name, sku}`. Empty on a new category unless you assign products. A product can be in several categories."},
    }},
    "CategoryGroupMeta": {"type": "object", "description": "One entry per section. The listing, a category read, and the responses to create, replace and update return it; a section read or update does not.", "properties": {section: ref("CategorySectionMeta") for section in SECTIONS}},
    "CategorySectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "`section` for every entry."},
        "writable": {"type": "boolean", "description": "`true` for every entry."},
        "href": {"type": "string", "description": "The section's path, such as `/api/v4/admin/categories/{id}/general`. `{id}` is literal text: put the category's `id` in its place before you call the path."},
    }},
    "CategoryPagination": {"type": "object", "description": "Paging details for the listing. With an `offset` at or past `total`, `count` is `0` and `current_page` shows the last page, while `has_previous` shows `false` and `previous_page` is `null`.", "properties": {
        "total": {"type": "integer", "description": "The number of categories outside the trash that match your filters."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, capped at `20`, or `20`."},
        "offset": {"type": "integer", "description": "The number of categories skipped before this page."},
        "count": {"type": "integer", "description": "The number of categories on this page."},
        "current_page": {"type": "integer", "description": "The page number: `offset` divided by `limit`, rounded down, plus `1`, but never more than `total_pages`. It shows `1` when no category matches."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up."},
        "has_next": {"type": "boolean", "description": "`true` when `offset` plus `count` is less than `total`."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is above `0`, except that it shows `false` when `offset` is at or past `total`."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, or `null` when there is none. It sets `limit` and an `offset` that never goes below `0`, and repeats every other query parameter you sent except `page`, even `field_metadata` and parameters the listing ignores."},
        "next_page": {"type": ["string", "null"], "description": "The full URL of the next page, or `null` on the last page. It sets `limit` and the next `offset`, and repeats every other query parameter you sent except `page`, even `field_metadata` and parameters the listing ignores."},
    }},
    "CategoryFieldMetadata": {"type": "object", "description": "Describes every field of a category. Returned only when you send `field_metadata=true`. Each of the eight read-only fields has one entry, and each section is an object of entries keyed by field name; `availability_visibility.selected_customers` nests one level further, with `customers` and `groups`. The `images_media.image` and `images_media.background_image` entries describe a base64 `data:` URI string, but a write must send a `{filename, base64}` object: a `data:` URI string returns `500`. The `general.url` entry says a replace without `url` makes it from the name, but a `PUT` that renames a category without `url` leaves the `url` as it was.", "properties": dict(
        {name: METADATA_ENTRY_REF for name in READ_ONLY_PROPERTIES},
        **{section: {"type": "object", "additionalProperties": METADATA_ENTRY_REF, "description": "One entry per field of `" + section + "`, keyed by field name."} for section in SECTIONS},
    )},
    "CategoryFieldMetadataEntry": {"type": "object", "description": "Describes one field. Every entry has `type`, `read_only` and `key_path`; the other keys appear on some entries only.", "properties": {
        "type": {"type": "string", "description": "The field's value type."},
        "read_only": {"type": "boolean", "description": "`true` when you cannot write the field: the eight read-only fields, `general.filter_profile`, `images_media.image_url` and `images_media.background_image_url`."},
        "key_path": {"type": "string", "description": "Where the field sits in a category."},
        "required": {"type": "boolean", "description": "On a field you can write, whether a write must send it."},
        "min_length": {"type": "integer", "description": "The shortest value accepted, such as `2` for `general.name`."},
        "max_length": {"type": "integer", "description": "The longest value accepted: `255` for `general.name` and `general.url`, `200` for `general.title` and `general.heading`, and `500` for `general.summary`."},
        "values": {"type": "array", "items": {"type": "string"}, "description": "The values the field accepts, on a field that takes only a fixed list."},
        "note": {"type": "string", "description": "A remark about the field, such as the one on `last_updated_by`."},
        "write_only": {"type": "boolean", "description": "`true` on the three fields a write accepts but no response returns: `images_media.image`, `images_media.background_image` and `availability_visibility.password`."},
    }},
    "CategoryWriteBody": {"type": "object", "required": ["category"], "description": "Every write wraps its sections in `category`.", "properties": {
        "category": ref("CategoryInput"),
    }},
    "CategoryInput": {"type": "object", "description": "Group the fields by section. An unknown key beside the sections is rejected with `400` (`<key>: is not a recognised category field`), except in a section update, which reads only the section named in its path and ignores the rest. You cannot change the category's `id`: an `id` beside the sections is ignored, and so is a key beside `category`.", "properties": {
        "general": ref("CategoryGeneralInput"),
        "description": ref("CategoryDescription"),
        "images_media": ref("CategoryImagesMediaInput"),
        "availability_visibility": ref("CategoryAvailabilityVisibilityInput"),
        "tax_shipping": ref("CategoryTaxShipping"),
        "assign_products": ref("CategoryAssignProductsInput"),
    }},
    "CategoryGeneralInput": {"type": "object", "description": "The `general` fields you can write. Leave `filter_profile` out or send `null`: on a store without the filter plugin, a filter profile `id` there is rejected with `400`. Any other key is rejected with `400`, and `details[0].code` is `unknown_field`.", "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 255, "description": "Required when you create a category. 2 to 255 characters. A create rejects a name that a top-level category has, in any letter case, even one in the trash. A `PUT` without it keeps the current name."},
        "title": {"type": "string", "maxLength": 200, "description": "At most 200 characters."},
        "sku": {"type": "string", "description": "Generated when you create the category without it."},
        "url": {"type": "string", "maxLength": 255, "description": "At most 255 characters. Made from the name when you create the category without it."},
        "heading": {"type": "string", "maxLength": 200, "description": "At most 200 characters."},
        "parent_category": dict(ref("CategoryReference"), description="Send `{\"id\": ...}` with the parent category's `id`; a `name` beside the `id` is ignored. A `PUT` without it moves the category to the top level."),
        "layout": dict(ref("CategoryReference"), description="Send `{\"id\": ...}` with the layout's `id`; a `name` beside the `id` is ignored."),
        "summary": {"type": "string", "maxLength": 500, "description": "At most 500 characters."},
    }},
    "CategoryImagesMediaInput": {"type": "object", "description": "The images you can upload. Each returns as a URL in `image_url` or `background_image_url`. Sending `null` or `\"\"` does not remove a stored image, and sending `image_url` is rejected with `400`.", "properties": {
        "image": dict(ref("CategoryImage"), description="The category image."),
        "background_image": dict(ref("CategoryImage"), description="The background image, stored in a `background/` folder."),
    }},
    "CategoryImage": {"type": "object", "description": "One image upload. A `data:` URI string in place of this object returns `500`.", "properties": {
        "filename": {"type": "string", "description": "The file name, such as `banner.png`. The image's URL ends in it."},
        "base64": {"type": "string", "description": "The file's contents, base64-encoded."},
    }},
    "CategoryAvailabilityVisibilityInput": {"type": "object", "description": "The `availability_visibility` fields you can write: the fields a response returns, plus `password`. Send booleans as `true` or `false`: a string such as `\"false\"`, or `null`, returns `200` and leaves the stored value unchanged. A `PUT` that leaves this section out resets it to the defaults of a new category.", "properties": {
        "available": {"type": "boolean", "description": "Whether the category is available."},
        "visible": {"type": "boolean", "description": "Whether the category is visible."},
        "available_for": {"type": "string", "enum": AVAILABLE_FOR, "description": "Who the category is available to: `everyone`, `customer` or `selected`. Any other value, `null` included, is rejected with `400`."},
        "selected_customers": ref("CategorySelectedCustomersInput"),
        "available_on_date_range": {"type": "boolean", "description": "Turns on the date range."},
        "available_from_date": {"type": "string", "description": "The start of the date range, such as `2026-11-02T00:00:00Z`. A date without a time, such as `2026-11-02`, returns as `2026-11-02T00:00:00Z`."},
        "available_to_date": {"type": "string", "description": "The end of the date range. A date without a time returns at midnight UTC."},
        "password_protected": {"type": "boolean", "description": "Whether the category is password protected."},
        "password": {"type": "string", "description": "The category's password. It is never returned: responses show only `password_protected`."},
        "custom_sorting": {"type": "boolean", "description": "Turns custom sorting on for the category."},
        "default_sorting": {"type": "string", "enum": DEFAULT_SORTING, "description": "The category's default sort order: `alpha_asc`, `alpha_desc`, `price_desc`, `price_asc`, `created_asc` or `created_desc`. Any other value, `null` included, is rejected with `400`, so a write cannot set it back to `null`."},
        "disable_tracking": {"type": "boolean", "description": "Turns tracking off for the category."},
    }},
    "CategorySelectedCustomersInput": {"type": "object", "description": "The customers and groups the category is available to when `available_for` is `selected`. A customer `id` or group `id` that does not exist is dropped without an error.", "properties": {
        "customers": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each customer."},
        "groups": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each group."},
    }},
    "CategoryAssignProductsInput": {"type": "object", "description": "The products to assign.", "properties": {
        "products": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each product. The list replaces the category's products, and each product stays in any other category it is in."},
    }},
    "CategoryError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `conflict`."},
        "message": {"type": "string", "description": "What went wrong, such as `Category name already exists`."},
        "details": {"type": "array", "description": "One entry per rejected field or query parameter.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `unknown_field`, `already_exists`, `invalid_enum`, `too_long`, `invalid_sort_field` or `out_of_range`."},
            "message": {"type": ["string", "null"], "description": "What was wrong with it."},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
    "CategoryServerError": {"type": "object", "description": "The body of a `500`. It has no `error` object.", "properties": {
        "status": {"type": "string", "description": "Always `error`."},
        "code": {"type": "integer", "description": "Always `500`."},
        "message": {"type": "string", "description": "Always `Unexpected Error Occurred`."},
    }},
}
