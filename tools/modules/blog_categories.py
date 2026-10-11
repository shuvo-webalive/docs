"""The Blog categories endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Blog categories"
SLUG = "blog-categories"
BASE = "/admin/blog_categories"
ICON = "folder-open"

OVERVIEW_DESCRIPTION = "List, create, retrieve, update and delete the categories you file your blog posts under."
INTRO = "The Blog categories API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/blog_categories`."

UPDATE_PAGE = "/api-reference/blog-categories/update-a-blog-category"

WARNING = (
    "**Updating a blog category clears its `description` unless you send it again.** A `description`\n"
    "  you leave out of a `PUT`, or send as `null`, is saved as `\"\"`, while a `url` or an `image` you\n"
    "  leave out keeps its value. `name` is required on every update. To keep the description, send it\n"
    "  with every call to [Update a blog category](" + UPDATE_PAGE + ")."
)

NOTES = [
    "**Create and update wrap the category in `blog_category`.** Send\n"
    "  `{\"blog_category\": {\"name\": \"Recipes\"}}` to create a category. A body that sends the fields\n"
    "  without the wrapper, wraps them in the plural `blog_categories`, or is `{}` or\n"
    "  `{\"blog_category\": {}}`, is rejected with `400` and the message `blog_category info missing`.\n"
    "  Create, retrieve and update return the category inside `blog_category` too.",
    "**`name` must be unique, and a create without `url` makes one from `name`.** `name` is required on\n"
    "  create and update, 2 to 255 characters. A `name` another category already has is rejected with\n"
    "  `400`, not `409`, and the message `Blog category name exists`. Whether the store makes the `url`\n"
    "  from `name` or you send one, it lowercases it, turns each run of characters other than ASCII\n"
    "  letters, digits and `_` into one hyphen, drops a hyphen at either end and cuts it to 50\n"
    "  characters. A `url` another category already has is saved with `-1` added to the end.",
    "**An image is stored only when you send `base64`.** `image` takes `file_name`, `base64`, `title` and\n"
    "  `alternative_text`. Send `base64` without a `data:` prefix: a value such as\n"
    "  `data:image/png;base64,...` is rejected with `400`. Without `base64`, the other image fields are\n"
    "  ignored, so to change `title` or `alternative_text`, upload the image again. `image.link` ends in a\n"
    "  query string that changes on every read, and deleting the category deletes the uploaded file.",
    "**Link blog posts with `blogs`; a category's responses never list them.** On a create, send `blogs`\n"
    "  as a list of entries that each hold a blog post's `id`, such as `[{\"id\": 1234}]`: each post then\n"
    "  lists the category in its `categories`. An update without `blogs`, or with `[]`, keeps every link.\n"
    "  Deleting a category keeps its blog posts and takes the category off their `categories`.",
    "**A listing returns at most 20 categories per call, ordered by `name`.** The default order ignores\n"
    "  letter case; send `sort` and `dir` to change it. A larger `limit` is capped at `20`. To get more,\n"
    "  send the next `page` or a higher `offset` while `pagination.has_next` is `true`. Only `limit`,\n"
    "  `offset`, `page`, `sort`, `dir` and `field_metadata` are accepted: any other parameter, such as\n"
    "  `q`, `search` or `name`, is rejected with `400`. There is no count endpoint:\n"
    "  `GET /admin/blog_categories/count` is rejected with `400` and the message `id must be a number`,\n"
    "  so read `pagination.total` instead.",
    "**After a rejected `limit`, `offset`, `page`, `sort` or `dir`, your next request on the same client returns the same `400`.**\n"
    "  It does so even when its own parameters are valid, with a new `request_id`. The request after that\n"
    "  runs normally, and so does every request on a new client: send the request that got the repeated\n"
    "  `400` again.",
]

BLOG_CATEGORY_ID = {
    "name": "blog_category_id",
    "in": "path",
    "required": True,
    "description": "The blog category's `id`, from a listing or from the response to creating the category.",
    "schema": {"type": "integer", "example": 15},
}

SORT_VALUES = ["id", "name", "url", "description", "created", "updated"]

LIMIT = {"name": "limit", "in": "query", "description": "The number of blog categories per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`. A negative number, or a value that is not a number such as `abc`, is rejected with `400` and the message `'limit' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of blog categories to skip. When you send both `offset` and `page`, `offset` wins. A negative number, or a value that is not a number such as `abc`, is rejected with `400` and the message `'offset' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied. `page=2` alone skips 20 categories; `limit=1&page=2` skips 1. A page past the last category returns no categories. A negative number, or a value that is not a number such as `abc`, is rejected with `400` and the message `'page' must be a non-negative integer`.", "schema": {"type": "integer", "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "What to sort the blog categories by: `id`, `name`, `url`, `description`, `created` or `updated`. Without `sort`, the categories are ordered by `name`, ignoring letter case. Any other value, such as `Name` or `-id`, is rejected with `400` and the message `Sort field not exist`. So are `created_on` and `last_updated_on`, although a blog category has fields with those names. To reverse the order, send `dir=desc`.", "schema": {"type": "string", "enum": SORT_VALUES, "example": "id"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`, in lower case. `dir=desc` without `sort` lists the categories by `name` in reverse. `DESC`, `Desc` or any other capitalised form is not rejected, but the store ignores it and returns the categories in ascending order. Any other value, such as `sideways`, is rejected with `400` and the message `Sort order must be asc or desc`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "desc"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted, but adds nothing: the response still has only `blog_categories` and `pagination`.", "schema": {"type": "boolean", "example": True}}

REQUEST_ID = "6a3f9c2e-1b7d-4e58-9f0a-2c4b8d1e7a35"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): q", [{"field": "q", "code": "unknown_parameter", "message": None}])
NAME_REQUIRED = error("invalid_request", "name: is required", [{"field": "name", "code": "required", "message": "is required"}])
WRAPPER_MISSING = error("invalid_request", "blog_category info missing")
NOT_A_NUMBER = error("invalid_request", "id must be a number")
NOT_FOUND = error("not_found", "blog category not found")

ERROR_REF = ref("BlogCategoryError")
ROW_REF = ref("BlogCategory")
ROW_RESPONSE = {"type": "object", "properties": {"blog_category": ROW_REF}}
WRITE_BODY = {"type": "object", "required": ["blog_category"], "properties": {"blog_category": ref("BlogCategoryInput")}}

PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
IMAGE_LINK = "https://your-store.example.com/resources/your-store-id/blog-category/category-15/450-seasonal-promotions.png"


def image(stamp):
    return {"title": "Seasonal promotions", "alternative_text": "Seasonal promotions banner", "file_name": "seasonal-promotions.png", "link": IMAGE_LINK + "?" + stamp}


CREATED_ROW = {"id": 15, "name": "Seasonal Promotions", "url": "seasonal-promotions", "description": "Sale announcements and limited-time offers.", "is_disposable": False, "is_in_trash": False, "image": image("20261007091502113+1100"), "created_on": "2026-10-06T22:15:02", "last_updated_on": "2026-10-06T22:15:02", "seo_configs": []}

SAMPLE_ROWS = [
    {"id": 12, "name": "Product News", "url": "product-news", "description": "New arrivals and product updates.", "is_disposable": False, "is_in_trash": False, "image": {}, "created_on": "2026-07-16T06:24:24", "last_updated_on": "2026-08-19T11:14:38", "seo_configs": []},
    {"id": 9, "name": "Recipes", "url": "recipes", "description": "Cooking with our products.", "is_disposable": False, "is_in_trash": False, "image": {}, "created_on": "2026-07-14T02:10:51", "last_updated_on": "2026-07-14T02:10:51", "seo_configs": []},
    dict(CREATED_ROW, image=image("20261007091544871+1100")),
]

RETRIEVED_ROW = dict(CREATED_ROW, image=image("20261007091610342+1100"))
UPDATED_ROW = dict(CREATED_ROW, name="Seasonal Offers", url="seasonal-offers", description="Offers and clearance announcements.", image=image("20261007092035208+1100"), last_updated_on="2026-10-06T22:20:35")

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

CREATE_BODY = {"blog_category": {
    "name": "Seasonal Promotions",
    "url": "seasonal-promotions",
    "description": "Sale announcements and limited-time offers.",
    "image": {"file_name": "seasonal-promotions.png", "base64": PNG_BASE64, "title": "Seasonal promotions", "alternative_text": "Seasonal promotions banner"},
}}
UPDATE_BODY = {"blog_category": {"name": "Seasonal Offers", "url": "seasonal-offers", "description": "Offers and clearance announcements."}}

ENDPOINTS = [
    {
        "key": "list_blog_categories",
        "slug": "list-blog-categories",
        "title": "List blog categories",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 blog categories, ordered by `name`, with the total and page links.",
        "description": "Returns up to 20 blog categories under `blog_categories`, ordered by `name` and ignoring letter case, and `pagination` with the total and the links to the next and previous pages. Send `sort` and `dir` to change the order, and `page` or `offset` to get the next page. Only `limit`, `offset`, `page`, `sort`, `dir` and `field_metadata` are accepted; any other parameter, such as `q` or `name`, is rejected with `400`. After a rejected `limit`, `offset`, `page`, `sort` or `dir`, your next request on the same client returns that same `400`, even when its own parameters are valid.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, DIR, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The blog categories on this page under `blog_categories`, and `pagination` with the total, the page size and links to the next and previous pages. `field_metadata=true` adds no key. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "blog_categories": {"type": "array", "items": ROW_REF},
                    "pagination": ref("BlogCategoryPagination"),
                }},
                "example": {"blog_categories": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "The listing rejected a query parameter, and the message says which. A parameter it does not accept returns `unknown query parameter(s): <name>`, with `details[0].field` naming the parameter and `details[0].code` set to `unknown_parameter`. A `sort` value it does not accept returns `Sort field not exist`, with `details[0].code` set to `invalid_sort_field`. A `dir` other than `asc` or `desc` in any letter case, such as `sideways`, returns `Sort order must be asc or desc`, with an empty `details`. `limit=0` returns `'limit' must be a positive integer`, with `details[0].code` set to `out_of_range`, and a negative or non-numeric `limit` returns `'limit' must be a non-negative integer`, with `details[0].code` set to `invalid_integer`. A negative or non-numeric `offset` returns `'offset' must be a non-negative integer`, and a negative or non-numeric `page` returns `'page' must be a non-negative integer`, each with `details[0].code` set to `invalid_integer`. After a rejected `limit`, `offset`, `page`, `sort` or `dir`, your next request on the same client returns this `400` too; send that request again.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": "limit=20&offset=0"},
    },
    {
        "key": "create_blog_category",
        "slug": "create-a-blog-category",
        "title": "Create a blog category",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a blog category and returns it with its `id`, which other calls take as `blog_category_id`.",
        "description": "Creates a blog category and returns it with the `id` the store assigned, which the other calls take as `blog_category_id`. Wrap the fields in `blog_category`; only `name` is required, and a `url` you leave out is made from `name`. Send `base64` inside `image` to upload an image, and `blogs` to file existing blog posts under the new category. Do not send the category's `id`: a create with an `id` inside `blog_category` returns `500` and stores nothing.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new blog category under `blog_category`, with the `id` the store assigned: the other calls take it as `blog_category_id`. `name`, `url` and `description` are as saved, `is_disposable` and `is_in_trash` are `false`, and `seo_configs` is `[]`. After an upload, `image.link` points to the store's copy of the file; without one, `image` is `{}`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"blog_category": CREATED_ROW},
            },
            "400": {
                "description": "The body was rejected, and the message says why. The body is not wrapped in `blog_category`, or the wrapper is empty (`blog_category info missing`); `name` is missing or empty (`name: is required`) or longer than 255 characters (`name: must be between 2 and 255 characters`); another blog category already has that `name` (`Blog category name exists`); or `image.base64` starts with a `data:` prefix (`Image upload operation failed. Please upload a valid Image.`).",
                "schema": ERROR_REF,
                "example": NAME_REQUIRED,
            },
            "500": {
                "description": "The body has an `id` field inside `blog_category`. The `code` is `internal_error`, and nothing is stored. Leave `id` out: the store assigns the category's `id` itself.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_blog_category",
        "slug": "retrieve-a-blog-category",
        "title": "Retrieve a blog category",
        "method": "GET",
        "path": BASE + "/{blog_category_id}",
        "summary": "Returns the blog category whose `id` you pass as `blog_category_id`.",
        "description": "Returns the blog category whose `id` you pass as `blog_category_id`, under the `blog_category` key, with the same ten fields as a listing entry. Query parameters are ignored, and the response has no `ETag` or `Last-Modified` header. `HEAD` on this path returns `404` even for a category that exists, so use this call to check that a category exists.",
        "parameters": [BLOG_CATEGORY_ID],
        "responses": {
            "200": {
                "description": "The blog category under `blog_category`. Two reads of a category with an image differ in the query string at the end of `image.link`.",
                "schema": ROW_RESPONSE,
                "example": {"blog_category": RETRIEVED_ROW},
            },
            "400": {
                "description": "The `blog_category_id` is not a number, such as `abc` or `count`. The `code` is `invalid_request` and the message is `id must be a number`.",
                "schema": ERROR_REF,
                "example": NOT_A_NUMBER,
            },
            "404": {
                "description": "No blog category has that `blog_category_id`. The `code` is `not_found` and the message is `blog category not found`. A `blog_category_id` with a dot, such as `1.5`, also returns `404`, but as a `text/html` page instead of JSON.",
                "schema": ERROR_REF,
                "example": NOT_FOUND,
            },
        },
        "example_call": {"path": {"blog_category_id": 15}},
    },
    {
        "key": "update_blog_category",
        "slug": "update-a-blog-category",
        "title": "Update a blog category",
        "method": "PUT",
        "path": BASE + "/{blog_category_id}",
        "summary": "Changes a blog category and returns it. A `description` you leave out is cleared.",
        "description": "Changes the blog category whose `id` you pass as `blog_category_id`, and returns the updated category. Wrap the fields in `blog_category` and send `name` every time, even when it does not change. Leaving out `description` saves it as `\"\"`; leaving out `url`, `image` or `blogs` keeps what the category has. `PATCH` is rejected with `405 method_not_allowed`, so send every change with `PUT`.",
        "parameters": [BLOG_CATEGORY_ID],
        "body": {"schema": WRITE_BODY, "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The blog category after the update, under `blog_category`. `created_on` keeps its value, and `last_updated_on` changes only when a value changed.",
                "schema": ROW_RESPONSE,
                "example": {"blog_category": UPDATED_ROW},
            },
            "400": {
                "description": "The body was rejected, and the message says why. The body is not wrapped in `blog_category`, or the wrapper is empty (`blog_category info missing`); `name` is missing or empty (`name: is required`) or longer than 255 characters (`name: must be between 2 and 255 characters`); or another blog category already has that `name` (`Blog category name exists`).",
                "schema": ERROR_REF,
                "example": WRAPPER_MISSING,
            },
        },
        "example_call": {"path": {"blog_category_id": 15}},
    },
    {
        "key": "delete_blog_category",
        "slug": "delete-a-blog-category",
        "title": "Delete a blog category",
        "method": "DELETE",
        "path": BASE + "/{blog_category_id}",
        "summary": "Deletes a blog category and its uploaded image permanently. Its blog posts are kept.",
        "description": "Deletes the blog category whose `id` you pass as `blog_category_id`, with its uploaded image, and returns `204` with no body. The category leaves the listing, and `pagination.total` goes down by one. Blog posts filed under the category are kept, without it in their `categories`. Rarely, retrieving the category straight after the delete still returns it with `200`, while deleting it again returns `404`.",
        "parameters": [BLOG_CATEGORY_ID],
        "responses": {
            "204": {"description": "The blog category is deleted. No body."},
            "404": {
                "description": "No blog category has that `blog_category_id`. Deleting a category you already deleted returns this `404` with the message `Blog Category not found`, which differs in letter case from the `blog category not found` that a retrieve returns.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"blog_category_id": 15}},
    },
]

SCHEMAS = {
    "BlogCategory": {"type": "object", "description": "One blog category. A listing entry, a retrieve, a create and an update return the same ten fields.", "properties": {
        "id": {"type": "integer", "description": "The blog category's `id`, assigned by the store. Pass it as `blog_category_id` in a path."},
        "name": {"type": "string", "minLength": 2, "maxLength": 255, "description": "The category's name, 2 to 255 characters. No two blog categories have the same name."},
        "url": {"type": "string", "description": "The category's URL slug, such as `seasonal-promotions`. A create without one gets a `url` made from `name`, and a `url` another category already has is saved with `-1` added to the end."},
        "description": {"type": "string", "description": "The category's description, saved as sent, HTML included. `\"\"` when none is set."},
        "is_disposable": {"type": "boolean", "description": "`false` on a category you create. A create ignores a value you send for it."},
        "is_in_trash": {"type": "boolean", "description": "`false` on a category you create. A create ignores a value you send for it."},
        "image": dict(ref("BlogCategoryImage"), description="The category's image, or `{}` when it has none."),
        "created_on": {"type": "string", "description": "When the category was created, in UTC, written `YYYY-MM-DDTHH:MM:SS` without a time zone, such as `2026-07-16T06:24:24`. An update never changes it."},
        "last_updated_on": {"type": "string", "description": "When the category last changed, written like `created_on`. On a new category it equals `created_on` or is one second later, so do not expect the two to match. An update changes it only when a value changed."},
        "seo_configs": {"type": "array", "items": ref("BlogCategorySeoConfig"), "description": "The category's SEO entries. You cannot set them through this API: a category you create has `[]`, and a create or update that sends `seo_configs` stores nothing."},
    }},
    "BlogCategoryImage": {"type": "object", "description": "An uploaded image. `{}` when the category has no image; otherwise all four keys.", "properties": {
        "title": {"type": "string", "description": "The image title, or `\"\"` when the upload sent none."},
        "alternative_text": {"type": "string", "description": "The image's alternative text, or `\"\"` when the upload sent none."},
        "file_name": {"type": "string", "description": "The `file_name` sent with the upload, or a name the store chose when the upload sent none."},
        "link": {"type": "string", "description": "Where the image is served. An upload made through the API is served from your store's own host at `/resources/<store id>/blog-category/category-<blog_category_id>/450-<file_name>`; some categories link to a CDN copy whose name differs from `file_name`. The link ends in a query string that changes on every read, so compare links without it. Once the category is deleted, the link returns `404`."},
    }},
    "BlogCategorySeoConfig": {"type": "object", "description": "One SEO entry of a blog category.", "properties": {
        "id": {"type": "integer", "description": "The SEO entry's `id`."},
        "value": {"type": "string", "description": "The entry's value, as text."},
        "type": {"type": "string", "description": "The entry's type, such as `page_seo`."},
        "config_key": {"type": "string", "description": "The entry's key."},
    }},
    "BlogCategoryInput": {"type": "object", "required": ["name"], "description": "Send these fields inside `blog_category`, on a create and on an update. A create ignores unknown fields and the fields you cannot write here: `is_disposable`, `is_in_trash`, `created_on`, `last_updated_on` and `seo_configs`. An update ignores `seo_configs` too. Do not send the category's `id`: inside `blog_category`, it returns `500` on a create and is ignored on an update.", "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 255, "description": "Required on create and update, 2 to 255 characters. A `name` another blog category already has is rejected with `400`."},
        "url": {"type": ["string", "null"], "description": "Optional. The store lowercases it, turns each run of characters other than ASCII letters, digits and `_` into one hyphen, drops a hyphen at either end and cuts it to 50 characters. On a create without it, the store makes it from `name` the same way. A `url` another blog category already has is saved with `-1` added to the end. On an update, sending the category's current `url` keeps it as it is, and a `url` you leave out, or send as `\"\"` or `null`, keeps its value."},
        "description": {"type": ["string", "null"], "description": "Optional. Saved as sent, HTML included, and `\"\"` when you leave it out. On an update, a `description` you leave out, or send as `null`, is saved as `\"\"`."},
        "image": dict(ref("BlogCategoryImageInput"), description="Optional. An image to upload. On an update, an `image` you leave out, or send as `{}` or `null`, keeps the current image."),
        "blogs": {"type": "array", "items": ref("BlogCategoryBlogLink"), "description": "Optional. Blog posts to file under the category. On a create, each post then lists the category in its `categories`. On an update, `blogs` left out or sent as `[]` keeps every link."},
    }},
    "BlogCategoryImageInput": {"type": "object", "description": "An image upload. Nothing in `image` is stored without `base64`.", "properties": {
        "file_name": {"type": "string", "description": "The name to save the file under. Without it, the store chooses a name."},
        "base64": {"type": "string", "description": "The image file, base64-encoded, without a `data:` prefix: a value such as `data:image/png;base64,...` is rejected with `400`. On an update, a new `base64` replaces the current image."},
        "title": {"type": "string", "description": "The image title. Saved only with a `base64` in the same request; otherwise ignored, on a create and on an update."},
        "alternative_text": {"type": "string", "description": "The image's alternative text. Saved only with a `base64` in the same request; otherwise ignored."},
    }},
    "BlogCategoryBlogLink": {"type": "object", "description": "A blog post to file under the category.", "properties": {
        "id": {"type": "integer", "description": "The blog post's `id`."},
    }},
    "BlogCategoryPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of blog categories in the listing, across all pages."},
        "limit": {"type": "integer", "description": "The page size the store applied: the `limit` you sent, at most `20`, or `20` when you sent none."},
        "offset": {"type": "integer", "description": "The number of categories skipped before this page."},
        "count": {"type": "integer", "description": "The number of categories on this page."},
        "current_page": {"type": "integer", "description": "The number of this page, counting from `1`. Past the last category it does not follow `page`: `page=2` with 20 or fewer categories returns `1`."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up."},
        "has_next": {"type": "boolean", "description": "`true` when more categories follow this page."},
        "has_previous": {"type": "boolean", "description": "`true` when categories come before this page. `false` on a page past the last category, such as `page=2` with 20 or fewer categories."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, with `limit` and `offset`, or `null` when `has_previous` is `false`."},
        "next_page": {"type": ["string", "null"], "description": "The full URL of the next page, with `limit` and `offset`, or `null` when `has_next` is `false`."},
    }},
    "BlogCategoryError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found`, `method_not_allowed` or `internal_error`."},
        "message": {"type": "string", "description": "What went wrong, such as `blog category not found`."},
        "details": {"type": "array", "description": "Names the rejected field when the listing rejects `limit`, `offset`, `page`, `sort` or a parameter it does not accept, or when a write rejects a missing or too-long `name`. An empty list on every other error, including a rejected `dir` and a `name` another category already has.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter or body field that was rejected, such as `limit`, `sort` or `name`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_parameter`, `invalid_sort_field`, `out_of_range`, `invalid_integer`, `required` or `invalid_length`."},
            "message": {"type": ["string", "null"], "description": "`null` when the listing rejects a query parameter. When a write rejects `name`, the reason without the field name, such as `is required`."},
            "value": {"type": ["integer", "string"], "description": "The value you sent, such as `abc` or `created_on`. On the `out_of_range` error for `limit=0` it is the number `0`; on the `invalid_integer` error for `limit=-1` it is the string `\"-1\"`. On a `name` rejected for its length, it is the number of characters you sent. Absent on a parameter the listing does not accept and on a missing `name`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
