"""The Blogs endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Blogs"
SLUG = "blogs"
BASE = "/admin/blogs"
ICON = "newspaper"

OVERVIEW_DESCRIPTION = "List, count, create, change and delete blog posts, and add, read, approve and mark as spam the comments on each post."
INTRO = "The Blogs API has twelve endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/blogs`."

LIST_PAGE = "/api-reference/blogs/list-blog-posts"
CREATE_PAGE = "/api-reference/blogs/create-a-blog-post"
UPDATE_PAGE = "/api-reference/blogs/update-a-blog-post"
APPROVE_PAGE = "/api-reference/blogs/approve-a-comment"
CUSTOMERS_PAGE = "/api-reference/customers/list-customers"

WARNING = (
    "**Replacing a blog post resets the fields you leave out of the body.** `PUT` sets `content` to\n"
    "  `null`, `is_published` to `false`, `date` to the current time, `categories` to the store's default\n"
    "  category, `seo_configs` to `{\"meta_tag\": []}`, `visible_to` to `null` and `selected_customers` to\n"
    "  `[]`. It keeps the image and `created_by`, and keeps `url` unless you send a new one. To change\n"
    "  only some fields, use\n"
    "  [Update a blog post](" + UPDATE_PAGE + "), which sends `PATCH`."
)

NOTES = [
    "**Wrap every request body in `blog`, comments included.** Send `{\"blog\": {...}}` to\n"
    "  create, replace or update a blog post, and `{\"blog\": {\"comment\": {...}}}` to add a comment. A blog\n"
    "  post write without the wrapper, or with an empty one, is rejected with `400` and the message\n"
    "  `blog info missing`, and a field it does not recognise is rejected with `400` and the reason\n"
    "  `unknown_field`. A comment that is not wrapped in both returns `404` with the message\n"
    "  `comment is required`.",
    "**Deleting a blog post moves it to the trash, and no call on this API restores it or empties the trash.**\n"
    "  The post leaves the listing and the count, and retrieving, replacing or updating it returns `404`.\n"
    "  Its `title` stays taken: a create or replace with that title, in any letter case, is rejected with\n"
    "  `400`, and the message says the title `is already used by a blog in the trash; restore or rename it`.\n"
    "  Its comments stay readable and you can still approve them, but adding a comment to the post\n"
    "  returns `404`.",
    "**In every comment response, the top-level `id` is the blog post's `id`, not the comment's.** One\n"
    "  comment is returned as `{\"id\": <blog_id>, \"comment\": {...}}`, and the comment listing as\n"
    "  `{\"id\": <blog_id>, \"comments\": [...]}`. Read the comment's own `id` inside `comment` and pass it\n"
    "  as `blog_comment_id`. No call updates or deletes a comment.",
    "**A listing returns at most 20 blog posts per call, latest `date` first.** A larger `limit` is capped\n"
    "  at `20`. To get more, send the next `page` or a higher `offset` while `pagination.has_next` is\n"
    "  `true`. Only `limit`, `offset`, `page`, `sort`, `dir`, `ids`, `category`, `visibility`, `search`\n"
    "  and `field_metadata` are accepted: any other parameter is rejected with `400`. To filter by several\n"
    "  blog post `id` values, repeat `ids`, as in `ids=1201&ids=1202`: a comma list returns `500`.",
    "**After the listing rejects `limit=0`, a `sort` or a `dir`, your next request on the same client returns the same `400`.**\n"
    "  It does so even when its own parameters are valid. The request after that runs normally, and so\n"
    "  does every request on a new client: send the request that got the repeated `400` again.",
    "**A restricted blog post names its audience by each customer's `internal_id`.** Set `visibility` to\n"
    "  `restricted` and `visible_to` to `selected`, and send `selected_customers` as\n"
    "  `{\"customers\": [...], \"groups\": [...]}`, with each customer's `internal_id` from\n"
    "  [List customers](" + CUSTOMERS_PAGE + ") and each customer group's `id`. A customer's `customer_id`\n"
    "  there is dropped without an error, which leaves the audience empty. A post returns `selected_customers` as\n"
    "  an object once it names anyone, and as `[]`, a list, while it names no one.",
]

BLOG_ID = {
    "name": "blog_id",
    "in": "path",
    "required": True,
    "description": "The blog post's `id`, from a listing or from the response to creating the post.",
    "schema": {"type": "integer", "example": 1201},
}

BLOG_COMMENT_ID = {
    "name": "blog_comment_id",
    "in": "path",
    "required": True,
    "description": "The comment's `id`, from `comment.id` in the response to adding the comment, or from `comments[].id` in the comment listing. It is not the top-level `id` of those responses, which is the blog post's `id`.",
    "schema": {"type": "integer", "example": 77},
}

SORT_VALUES = ["id", "name", "url", "date", "created", "updated"]
VISIBILITY_VALUES = ["open", "hidden", "restricted"]

LIMIT = {"name": "limit", "in": "query", "description": "The number of blog posts per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of blog posts to skip.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "The page to return, counting from `1`. The store reads it as `offset = (page - 1) * limit`. `page=0` returns the first page.", "schema": {"type": "integer", "minimum": 0, "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "What to sort the blog posts by: `id`, `name`, `url`, `date`, `created` or `updated`. Without `sort`, the posts come latest `date` first. Any other value, including `title`, `created_on` and `last_updated_on`, is rejected with `400` and the message `Sort field not exist`.", "schema": {"type": "string", "enum": SORT_VALUES, "example": "id"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`. Defaults to `desc`. Any other value is rejected with `400` and the message `Sort order must be asc or desc`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
IDS = {"name": "ids", "in": "query", "style": "form", "explode": True, "description": "Keeps only the blog posts whose `id` you list. Repeat the parameter for each post, as in `ids=1201&ids=1202`. A comma list such as `ids=1201,1202` returns `500`, and a bracketed name such as `ids[]=1201` is rejected with `400`. A post in the trash is never returned.", "schema": {"type": "array", "items": {"type": "integer"}, "example": [1201, 1202]}}
CATEGORY = {"name": "category", "in": "query", "description": "Keeps only the blog posts filed under the blog category whose `id` you send. A blog category `id` that no post is filed under, or that matches no blog category, returns no posts and no error.", "schema": {"type": "integer", "example": 31}}
VISIBILITY = {"name": "visibility", "in": "query", "description": "Keeps only the blog posts with this `visibility`: `open`, `hidden` or `restricted`, in any letter case. Any other value returns no posts instead of an error.", "schema": {"type": "string", "enum": VISIBILITY_VALUES, "example": "open"}}
SEARCH = {"name": "search", "in": "query", "description": "Accepted, but it filters nothing: the listing returns the same posts whatever you send.", "schema": {"type": "string", "example": "spring"}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key that describes each of the seventeen fields of a blog post. Takes `true`, `false`, `1` or `0`; any other value, `True` included, is rejected with `400` and the message `field_metadata must be true/false or 0/1`.", "schema": {"type": "boolean", "example": True}}

COUNT_IDS = dict(IDS, description="Counts only the blog posts whose `id` you list. Repeat the parameter for each post, as in `ids=1201&ids=1202`. A comma list such as `ids=1201,1202` returns `500`. A post in the trash is never counted.")
COUNT_CATEGORY = dict(CATEGORY, description="Counts only the blog posts filed under the blog category whose `id` you send.")
COUNT_VISIBILITY = dict(VISIBILITY, description="Counts only the blog posts with this `visibility`: `open`, `hidden` or `restricted`, in any letter case. Any other value returns `0`.")

REQUEST_ID = "6b2e8f1a-3c4d-4e5f-9a0b-1c2d3e4f5a6b"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


UNKNOWN_PARAMETER = error("invalid_request", "unknown query parameter(s): q", [{"field": "q", "code": "unknown_parameter", "message": None}])
WRAPPER_MISSING = error("invalid_request", "blog info missing")
UNKNOWN_FIELD = error("invalid_request", "author: is not a recognised blog field", [{"field": "author", "code": "unknown_field"}])
BLOG_NOT_FOUND = error("not_found", "Blog not found")
COMMENT_REQUIRED = error("not_found", "comment is required")
COMMENTS_BLOG_NOT_FOUND = error("not_found", "blog not found")
COMMENT_NOT_FOUND = error("not_found", "blog comment not found")
SERVER_ERROR = {"status": "error", "code": 500, "message": "Unexpected Error Occurred"}
SERVER_ERROR_BODY = "The body has no `error` object: it is `{\"status\": \"error\", \"code\": 500, \"message\": \"Unexpected Error Occurred\"}`."

ERROR_REF = ref("BlogError")
SERVER_ERROR_REF = ref("BlogServerError")
ROW_REF = ref("Blog")
COMMENT_REF = ref("BlogComment")
GROUP_META_REF = ref("BlogGroupMeta")
FIELD_METADATA_REF = ref("BlogFieldMetadata")

ROW_RESPONSE = {"type": "object", "properties": {"blog": ROW_REF}}
ROW_WITH_META_RESPONSE = {"type": "object", "properties": {"blog": ROW_REF, "group_meta": GROUP_META_REF}}
BLOG_ID_FIELD = {"type": "integer", "description": "The blog post's `id`, the same value as `blog_id` in the path. It is not the comment's `id`."}
COMMENT_RESPONSE = {"type": "object", "properties": {"id": BLOG_ID_FIELD, "comment": COMMENT_REF}}
WRITE_BODY = {"type": "object", "required": ["blog"], "properties": {"blog": ref("BlogInput")}}
COMMENT_BODY = {"type": "object", "required": ["blog"], "properties": {"blog": {
    "type": "object", "required": ["comment"], "description": "The wrapper every comment write needs.",
    "properties": {"comment": ref("BlogCommentInput")},
}}}

PNG_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

GROUP_META = {"blogs": {"kind": "resource", "writable": True, "href": "/api/v4/admin/blogs"}}
PROMOTIONS = {"id": 31, "name": "Promotions", "is_disposable": False, "is_in_trash": False}
CARE_GUIDES = {"id": 30, "name": "Care Guides", "is_disposable": False, "is_in_trash": False}
AUTHOR = {"id": 3, "name": "Store Admin"}
SPRING_SEO = {"meta_tag": [{"name": "description", "value": "Spring sale: up to 40% off"}]}


def spring_image(stamp):
    return {"title": "Spring sale cover", "alternative_text": "Spring sale banner", "file_name": "spring-cover.png",
            "link": "https://your-store.example.com/resources/blog/1201_spring-cover.png?v=" + stamp}


CREATED_ROW = {
    "id": 1201, "title": "Spring Sale Announcement", "url": "spring-sale-announcement",
    "content": "<p>Save up to 40% on selected products until the end of the month.</p>",
    "date": "2026-09-28T00:00:00", "is_published": True, "visibility": "open", "visible_to": None,
    "categories": [PROMOTIONS], "created_on": "2026-10-07T09:15:02", "last_updated_on": "2026-10-07T09:15:02",
    "is_disposable": False, "is_in_trash": False, "image": spring_image("20261007091502"),
    "created_by": AUTHOR, "selected_customers": [], "seo_configs": SPRING_SEO,
}

OLDER_ROW = {
    "id": 1198, "title": "Caring for Linen Shirts", "url": "caring-for-linen-shirts",
    "content": "<p>Wash cold and dry flat.</p>",
    "date": "2026-09-14T08:30:00", "is_published": True, "visibility": "open", "visible_to": None,
    "categories": [CARE_GUIDES], "created_on": "2026-09-14T08:31:44", "last_updated_on": "2026-09-14T08:31:44",
    "is_disposable": False, "is_in_trash": False, "image": {},
    "created_by": AUTHOR, "selected_customers": [], "seo_configs": {"meta_tag": []},
}

SAMPLE_ROWS = [dict(CREATED_ROW, image=spring_image("20261007091544")), OLDER_ROW]
RETRIEVED_ROW = dict(CREATED_ROW, image=spring_image("20261007091610"))

REPLACED_ROW = dict(
    CREATED_ROW, title="Spring Sale Extended", content="<p>The spring sale now runs one more week.</p>",
    visibility="restricted", visible_to="selected", last_updated_on="2026-10-07T09:20:41",
    image=spring_image("20261007092041"),
    selected_customers={"customers": [{"id": 5501, "name": "Ada Reader"}], "groups": []},
)
PATCHED_ROW = dict(CREATED_ROW, title="Spring Sale: Final Week", last_updated_on="2026-10-07T09:25:10", image=spring_image("20261007092510"))

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

CREATE_BODY = {"blog": {
    "title": "Spring Sale Announcement",
    "content": "<p>Save up to 40% on selected products until the end of the month.</p>",
    "date": "2026-09-28",
    "is_published": True,
    "visibility": "open",
    "categories": [{"id": 31}],
    "image": {"file_name": "spring-cover.png", "base64": PNG_BASE64, "title": "Spring sale cover", "alternative_text": "Spring sale banner"},
    "seo_configs": SPRING_SEO,
}}

REPLACE_BODY = {"blog": {
    "title": "Spring Sale Extended",
    "content": "<p>The spring sale now runs one more week.</p>",
    "date": "2026-09-28",
    "is_published": True,
    "visibility": "restricted",
    "visible_to": "selected",
    "categories": [{"id": 31}],
    "seo_configs": SPRING_SEO,
    "selected_customers": {"customers": [5501], "groups": []},
}}

PATCH_BODY = {"blog": {"title": "Spring Sale: Final Week"}}

NEW_COMMENT = {
    "id": 77, "status": "pending", "name": "Ada Reader", "email": "ada@example.com",
    "post_title": "Spring Sale Announcement", "content": "Great article, thanks for the sale details!",
    "spam": False, "likes": 0, "total_reply": 0,
    "created_on": "2026-10-07T09:30:12", "last_updated_on": "2026-10-07T09:30:12", "replies": [],
}
SECOND_COMMENT = {
    "id": 78, "status": "pending", "name": None, "email": None,
    "post_title": "Spring Sale Announcement", "content": "Does the sale include gift cards?",
    "spam": False, "likes": 0, "total_reply": 0,
    "created_on": "2026-10-07T09:41:05", "last_updated_on": "2026-10-07T09:41:05", "replies": [],
}
APPROVED_COMMENT = dict(NEW_COMMENT, status="approved", last_updated_on="2026-10-07T09:35:40")
SPAM_COMMENT = dict(NEW_COMMENT, status="spam", spam=True, last_updated_on="2026-10-07T09:36:18")

COMMENT_CREATE_BODY = {"blog": {"comment": {"content": "Great article, thanks for the sale details!", "name": "Ada Reader", "email": "ada@example.com"}}}


def write_400(title_required=False, extra=""):
    return (
        "The body was rejected, and the message says why. The body is not wrapped in `blog`, or the wrapper is empty "
        "(`blog info missing`); it has a field the store does not recognise (`<name>: is not a recognised blog field`, "
        "reason `unknown_field`); " + extra + ("`title` is missing; " if title_required else "")
        + "`title` is shorter than 2 or longer than 255 characters once trimmed "
        "(`invalid_length`); another blog post has the same `title` in any letter case (`duplicate`; the message says "
        "`is already used by another blog`, or `is already used by a blog in the trash; restore or rename it` when "
        "that post is in the trash); `date` is not `yyyy-MM-dd` or an ISO 8601 date and time (`invalid_date`); "
        "`is_published` is a string, `\"true\"` included (`invalid_boolean`); `visibility` is not `open`, `hidden` or "
        "`restricted` in lower case, or `visible_to` is not `all` or `selected` (`invalid_enum`); a blog category `id` "
        "in `categories` matches no blog category (`invalid_reference`, `names blog categories that do not exist: "
        "<id>`); or `visibility` is `restricted` and `visible_to` is `selected` with no one in `selected_customers` "
        "(`Please select at least one customer or customer group for restricted visibility`)."
    )


CATEGORY_500 = "A bare number in `categories`, such as `[31]`, returns `500`: send each category as an object holding the category's `id`, such as `[{\"id\": 31}]`."

ENDPOINTS = [
    {
        "key": "list_blogs",
        "slug": "list-blog-posts",
        "title": "List blog posts",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 blog posts, latest `date` first, with the total and page links.",
        "description": "Returns up to 20 blog posts under `blogs`, latest `date` first, with `group_meta` and a `pagination` block that holds the total and the links to the next and previous pages. Filter with `ids`, `category` and `visibility`, change the order with `sort` and `dir`, and send `page` or `offset` to get the next page. Any query parameter other than the ten on this page is rejected with `400`. After the listing rejects `limit=0`, a `sort` or a `dir`, your next request on the same client returns that same `400`, even when its own parameters are valid.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, DIR, IDS, CATEGORY, VISIBILITY, SEARCH, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The blog posts on this page under `blogs`, `group_meta`, and `pagination` with the total, the page size and the links to the next and previous pages. With `field_metadata=true`, a `field_metadata` key is added that describes each field. Posts in the trash are not listed. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "blogs": {"type": "array", "items": ROW_REF},
                    "group_meta": GROUP_META_REF,
                    "pagination": ref("BlogPagination"),
                    "field_metadata": dict(FIELD_METADATA_REF, description="Only when you send `field_metadata=true`."),
                }},
                "example": {"blogs": SAMPLE_ROWS, "group_meta": GROUP_META, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "The listing rejected a query parameter. A parameter it does not accept, including a bracketed name such as `ids[]`, returns `unknown query parameter(s): <name>` with `details[0].code` set to `unknown_parameter`. `limit=0` returns `'limit' must be a positive integer`, with `details[0].code` set to `out_of_range`. A `sort` it does not accept returns `Sort field not exist`, with the reason `invalid_sort_field`, and a `dir` other than `asc` or `desc` returns `Sort order must be asc or desc`. A `field_metadata` other than `true`, `false`, `1` or `0` returns `field_metadata must be true/false or 0/1`, with `details[0].code` set to `invalid_boolean`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
            "500": {
                "description": "`ids` was sent as a comma list, such as `ids=1201,1202`. Repeat the parameter instead: `ids=1201&ids=1202`. " + SERVER_ERROR_BODY,
                "schema": SERVER_ERROR_REF,
                "example": SERVER_ERROR,
            },
        },
        "example_call": {"query": "visibility=open&limit=20"},
    },
    {
        "key": "count_blogs",
        "slug": "count-blog-posts",
        "title": "Count blog posts",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of blog posts, narrowed by `ids`, `category` or `visibility` if you send them.",
        "description": "Returns the number of blog posts as `count`, inside a `blogs` object. `ids`, `category` and `visibility` narrow the number as they narrow [List blog posts](" + LIST_PAGE + "), so it matches that listing's `pagination.total` for the same filters. The listing's other parameters are accepted and change nothing, and any other parameter is rejected with `400`. Posts in the trash are not counted.",
        "parameters": [COUNT_IDS, COUNT_CATEGORY, COUNT_VISIBILITY],
        "responses": {
            "200": {
                "description": "The number of blog posts that match your filters, as `blogs.count`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {"blogs": {"type": "object", "properties": {"count": {"type": "integer", "description": "The number of blog posts that match your filters."}}}}},
                "example": {"blogs": {"count": 2}},
            },
            "400": {
                "description": "You sent a query parameter the listing does not accept: the message is `unknown query parameter(s): <name>` and `details[0].code` is `unknown_parameter`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
            "500": {
                "description": "`ids` was sent as a comma list, such as `ids=1201,1202`. Repeat the parameter instead: `ids=1201&ids=1202`. " + SERVER_ERROR_BODY,
                "schema": SERVER_ERROR_REF,
                "example": SERVER_ERROR,
            },
        },
        "example_call": {"query": "visibility=open"},
    },
    {
        "key": "create_blog",
        "slug": "create-a-blog-post",
        "title": "Create a blog post",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a blog post and returns it with its `id`, which other calls take as `blog_id`.",
        "description": "Creates a blog post from the fields you wrap in `blog` and returns it with `201`; only `title` is required. The store makes `url` from `title` and ignores a `url` you send, files a post without `categories` under the store's default category, and sets `visibility` to `open`, `is_published` to `false` and `date` to the current time when you leave them out. Send `base64` inside `image` to upload a cover image. Do not send an `id` field: the store assigns the post's `id`, and a create that sends one returns `500` and stores nothing.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new blog post under `blog`, with the post's `id`: the other calls take it as `blog_id`. The response has no `group_meta` and no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"blog": CREATED_ROW},
            },
            "400": {"description": write_400(title_required=True), "schema": ERROR_REF, "example": UNKNOWN_FIELD},
            "500": {"description": "The body has an `id` field inside `blog`, or a bare number in `categories`. With an `id` field, nothing is stored: leave it out, because the store assigns the post's `id` itself. Send each blog category as an object holding the category's `id`, such as `[{\"id\": 31}]`, not a bare number such as `[31]`."},
        },
        "example_call": {},
    },
    {
        "key": "get_blog",
        "slug": "retrieve-a-blog-post",
        "title": "Retrieve a blog post",
        "method": "GET",
        "path": BASE + "/{blog_id}",
        "summary": "Returns the blog post whose `id` you pass as `blog_id`.",
        "description": "Returns the blog post under `blog`, with the same seventeen fields as its listing entry, and `group_meta`. Send `field_metadata=true` to add a `field_metadata` key that describes each field; other query parameters are ignored. A post in the trash returns `404`. `HEAD` on this path returns `404` even for a post that exists, so use this call to check that a post exists.",
        "parameters": [BLOG_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The blog post under `blog`, and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them. Two reads of a post with an image differ in the query string at the end of `image.link`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "blog": ROW_REF,
                    "group_meta": GROUP_META_REF,
                    "field_metadata": dict(FIELD_METADATA_REF, description="Only when you send `field_metadata=true`."),
                }},
                "example": {"blog": RETRIEVED_ROW, "group_meta": GROUP_META},
            },
            "400": {
                "description": "`field_metadata` is not `true`, `false`, `1` or `0`: the message is `field_metadata must be true/false or 0/1` and `details[0].code` is `invalid_boolean`.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "The blog post is in the trash, or no blog post has that `blog_id`. Both return the `code` `not_found` and the message `Blog not found`.",
                "schema": ERROR_REF,
                "example": BLOG_NOT_FOUND,
            },
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "update_blog",
        "slug": "replace-a-blog-post",
        "title": "Replace a blog post",
        "method": "PUT",
        "path": BASE + "/{blog_id}",
        "summary": "Replaces a blog post and returns it. Most fields you leave out are reset.",
        "description": "Replaces the blog post with the fields you wrap in `blog` and returns it; send `title` and `visibility` every time. Fields you leave out are reset: `content` to `null`, `is_published` to `false`, `date` to the current time, `categories` to the store's default category, `seo_configs` to `{\"meta_tag\": []}`, `visible_to` to `null` and `selected_customers` to `[]`. The image and `created_by` are kept, and so is `url` unless you send a new one, which the store turns into a slug the same way as on create. To change only some fields, use [Update a blog post](" + UPDATE_PAGE + ").",
        "parameters": [BLOG_ID],
        "body": {"schema": WRITE_BODY, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The blog post after the replace, under `blog`, without `group_meta`. A customer in the audience reads as the customer's `internal_id` and name.",
                "schema": ROW_RESPONSE,
                "example": {"blog": REPLACED_ROW},
            },
            "400": {
                "description": write_400(title_required=True, extra="`visibility` is missing (`visibility: is required on update; one of open, hidden, restricted`); "),
                "schema": ERROR_REF,
                "example": WRAPPER_MISSING,
            },
            "404": {
                "description": "The blog post is in the trash, or no blog post has that `blog_id`. For a post in the trash, the message is `Blog not found`.",
                "schema": ERROR_REF,
                "example": BLOG_NOT_FOUND,
            },
            "500": {"description": CATEGORY_500},
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "patch_blog",
        "slug": "update-a-blog-post",
        "title": "Update a blog post",
        "method": "PATCH",
        "path": BASE + "/{blog_id}",
        "summary": "Changes only the fields you send and returns the blog post.",
        "description": "Changes only the fields you send inside `blog`, and returns the blog post with `group_meta`. A new `title` leaves `url` as it was: to change `url`, send it beside `title`, because a `url` sent without `title` is ignored. Moving a restricted post to `open` or `hidden` sets `visible_to` to `null` but keeps `selected_customers`. Each field you send is checked the same way as on [Create a blog post](" + CREATE_PAGE + ").",
        "parameters": [BLOG_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The blog post after the change, under `blog`, and `group_meta`. Besides the fields you sent, only `last_updated_on` changes, and `visible_to` when you move a restricted post to `open` or `hidden`.",
                "schema": ROW_WITH_META_RESPONSE,
                "example": {"blog": PATCHED_ROW, "group_meta": GROUP_META},
            },
            "400": {"description": write_400(), "schema": ERROR_REF, "example": WRAPPER_MISSING},
            "404": {
                "description": "The blog post is in the trash, or no blog post has that `blog_id`. For a post in the trash, the message is `Blog not found`.",
                "schema": ERROR_REF,
                "example": BLOG_NOT_FOUND,
            },
            "500": {"description": CATEGORY_500},
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "delete_blog",
        "slug": "delete-a-blog-post",
        "title": "Delete a blog post",
        "method": "DELETE",
        "path": BASE + "/{blog_id}",
        "summary": "Moves a blog post to the trash and returns `204`; nothing on this API restores it.",
        "description": "Moves the blog post to the trash and returns `204` with no body. The post leaves the listing and the count, and retrieving, replacing, updating or deleting it again returns `404`. Its `title` stays taken, so no create or replace can use that title again, and no call on this API restores the post or empties the trash. Its comments stay readable and you can still approve them, but adding a comment to the post returns `404`.",
        "parameters": [BLOG_ID],
        "responses": {
            "204": {"description": "The blog post is in the trash. No body."},
            "404": {
                "description": "No blog post has that `blog_id`, or the post is already in the trash: deleting a post a second time returns the message `Blog already in trash`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "list_blog_comments",
        "slug": "list-comments-on-a-blog-post",
        "title": "List comments on a blog post",
        "method": "GET",
        "path": BASE + "/{blog_id}/comments",
        "summary": "Returns every comment on a blog post, oldest first, in one response.",
        "description": "Returns every comment on the blog post under `comments`, oldest first and with no paging. The top-level `id` beside `comments` is the blog post's `id`, not a comment's. Query parameters are ignored. It returns the comments of a blog post in the trash too, and `404` for a `blog_id` that matches no blog post.",
        "parameters": [BLOG_ID],
        "responses": {
            "200": {
                "description": "The blog post's `id` and every comment on it, oldest first. Each comment has the same twelve fields as the response to adding it. A post without comments returns `comments` as `[]`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {"id": BLOG_ID_FIELD, "comments": {"type": "array", "items": COMMENT_REF}}},
                "example": {"id": 1201, "comments": [NEW_COMMENT, SECOND_COMMENT]},
            },
            "404": {
                "description": "No blog post, in the listing or in the trash, has that `blog_id`: the `code` is `not_found` and the message is `blog not found`.",
                "schema": ERROR_REF,
                "example": COMMENTS_BLOG_NOT_FOUND,
            },
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "create_blog_comment",
        "slug": "add-a-comment-to-a-blog-post",
        "title": "Add a comment to a blog post",
        "method": "POST",
        "path": BASE + "/{blog_id}/comments",
        "summary": "Adds a comment to a blog post and returns it with `status` set to `pending`.",
        "description": "Adds a comment to the blog post and returns it with `201` and `status` set to `pending`. Wrap the comment in `blog` and then `comment`, with `content` required and `name` and `email` optional: any other shape returns `404` with the message `comment is required`. The store drops fields it does not recognise and the `id`, `spam`, `likes`, `total_reply` and `post_title` fields, but stores any `status` you send without checking it, so leave `status` out. A comment on a blog post in the trash returns `404`.",
        "parameters": [BLOG_ID],
        "body": {"schema": COMMENT_BODY, "example": COMMENT_CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new comment under `comment`, with `status` set to `pending`, `spam` to `false`, `likes` and `total_reply` to `0`, `replies` to `[]`, and `post_title` to the blog post's title. A `name` or `email` you left out reads `null`. The top-level `id` is the blog post's `id`.",
                "schema": COMMENT_RESPONSE,
                "example": {"id": 1201, "comment": NEW_COMMENT},
            },
            "400": {
                "description": "A comment field was rejected, and the message says why: `content` is missing or blank (`content: is required`) or longer than 1000 characters (`too_long`); `name` is shorter than 2 or longer than 100 characters once trimmed (`invalid_length`); or `email` is not a valid email address (`invalid_email`).",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "The comment is not wrapped in `blog` and then `comment` (`comment is required`), or the blog post with that `blog_id` is in the trash (`Blog not found`).",
                "schema": ERROR_REF,
                "example": COMMENT_REQUIRED,
            },
            "500": {
                "description": "`replies` is a list that is not empty. Leave `replies` out: no call on this API adds a reply.",
                "schema": SERVER_ERROR_REF,
            },
        },
        "example_call": {"path": {"blog_id": 1201}},
    },
    {
        "key": "get_blog_comment",
        "slug": "retrieve-a-comment",
        "title": "Retrieve a comment",
        "method": "GET",
        "path": BASE + "/{blog_id}/comments/{blog_comment_id}",
        "summary": "Returns the comment whose `id` you pass as `blog_comment_id`.",
        "description": "Returns the comment under `comment`, with the same twelve fields as its entry in the comment listing. The top-level `id` is the blog post's `id`, not the comment's. It also returns a comment on a blog post in the trash.",
        "parameters": [BLOG_ID, BLOG_COMMENT_ID],
        "responses": {
            "200": {
                "description": "The blog post's `id` and the comment. The response has no `ETag` header.",
                "schema": COMMENT_RESPONSE,
                "example": {"id": 1201, "comment": NEW_COMMENT},
            },
            "404": {
                "description": "No comment on the blog post with that `blog_id` has that `blog_comment_id`, including a comment that belongs to another blog post: the message is `blog comment not found`. When no blog post has that `blog_id`, the message is `blog not found`. Both return the `code` `not_found`.",
                "schema": ERROR_REF,
                "example": COMMENT_NOT_FOUND,
            },
        },
        "example_call": {"path": {"blog_id": 1201, "blog_comment_id": 77}},
    },
    {
        "key": "approve_blog_comment",
        "slug": "approve-a-comment",
        "title": "Approve a comment",
        "method": "POST",
        "path": BASE + "/{blog_id}/comments/{blog_comment_id}/approve",
        "summary": "Sets a comment's `status` to `approved` and returns the comment.",
        "description": "Sets the comment's `status` to `approved` and returns `201` with the comment; nothing else changes but `last_updated_on`. It does not reset `spam`: a comment marked as spam and then approved has `status` `approved` and `spam` `true`. Send no body; one you send is ignored.",
        "parameters": [BLOG_ID, BLOG_COMMENT_ID],
        "responses": {
            "201": {
                "description": "The blog post's `id` and the comment, with `status` set to `approved`.",
                "schema": COMMENT_RESPONSE,
                "example": {"id": 1201, "comment": APPROVED_COMMENT},
            },
        },
        "example_call": {"path": {"blog_id": 1201, "blog_comment_id": 77}},
    },
    {
        "key": "mark_blog_comment_spam",
        "slug": "mark-a-comment-as-spam",
        "title": "Mark a comment as spam",
        "method": "POST",
        "path": BASE + "/{blog_id}/comments/{blog_comment_id}/mark-spam",
        "summary": "Sets a comment's `status` to `spam` and `spam` to `true`, and returns the comment.",
        "description": "Sets the comment's `status` to `spam` and `spam` to `true`, and returns `201` with the comment. Send no body; one you send is ignored. [Approve a comment](" + APPROVE_PAGE + ") later changes `status` to `approved` but leaves `spam` set to `true`.",
        "parameters": [BLOG_ID, BLOG_COMMENT_ID],
        "responses": {
            "201": {
                "description": "The blog post's `id` and the comment, with `status` set to `spam` and `spam` to `true`.",
                "schema": COMMENT_RESPONSE,
                "example": {"id": 1201, "comment": SPAM_COMMENT},
            },
        },
        "example_call": {"path": {"blog_id": 1201, "blog_comment_id": 77}},
    },
]

SCHEMAS = {
    "Blog": {"type": "object", "description": "One blog post. A listing entry, a retrieve, and the response to a create, a replace or an update return the same seventeen fields.", "properties": {
        "id": {"type": "integer", "description": "The blog post's `id`, assigned by the store. Pass it as `blog_id` in a path."},
        "title": {"type": "string", "minLength": 2, "maxLength": 255, "description": "The post's title, 2 to 255 characters once trimmed. No two blog posts, live or in the trash, have the same title in any letter case."},
        "url": {"type": "string", "description": "The post's URL slug, such as `spring-sale-announcement`. A create makes it from `title`: lower case, with spaces turned into hyphens and `-1` added when another post already has that slug. A later change of `title` alone does not change it; a replace that sends `url`, or an update that sends `url` beside `title`, sets it."},
        "content": {"type": ["string", "null"], "description": "The post's body, as sent, or `null` when none is set."},
        "date": {"type": "string", "description": "The post's date, written `yyyy-MM-ddTHH:mm:ss` with no time zone. A `date` sent as `2026-09-28` reads `2026-09-28T00:00:00`, and `2026-09-28T10:11:12Z` reads `2026-09-28T10:11:12`."},
        "is_published": {"type": "boolean", "description": "Whether the post is published. A create or replace that leaves it out sets it to `false`."},
        "visibility": {"type": "string", "description": "Who can see the post: `open`, `hidden` or `restricted`. Some existing posts read `OPEN` in upper case."},
        "visible_to": {"type": ["string", "null"], "enum": ["all", "selected", None], "description": "`all` or `selected` on a restricted post, and `null` on a post that is `open` or `hidden`."},
        "categories": {"type": "array", "items": ref("BlogCategoryReference"), "description": "The blog categories the post is filed under. A post created without `categories` is filed under the store's default category. Some existing posts read `[]`."},
        "created_on": {"type": "string", "description": "When the post was created, such as `2026-10-07T09:15:02`."},
        "last_updated_on": {"type": "string", "description": "When the post last changed."},
        "is_disposable": {"type": "boolean", "description": "Set by the store: a write that sends it is rejected with `400`."},
        "is_in_trash": {"type": "boolean", "description": "`false` on a post you create. A write that sends it is rejected with `400`."},
        "image": dict(ref("BlogImage"), description="The post's cover image, or `{}` when it has none."),
        "created_by": dict(ref("BlogAuthor"), description="Who created the post, or `{}` on some existing posts. A write that sends it is rejected with `400`."),
        "selected_customers": {"description": "The audience of a restricted post: `[]`, a list, while it names no one, and an object holding `customers` and `groups` once it names anyone.", "oneOf": [
            {"type": "array", "maxItems": 0, "description": "No audience."},
            ref("BlogAudience"),
        ]},
        "seo_configs": ref("BlogSeoConfigs"),
    }},
    "BlogCategoryReference": {"type": "object", "description": "A blog category the post is filed under.", "properties": {
        "id": {"type": "integer", "description": "The blog category's `id`."},
        "name": {"type": "string", "description": "The blog category's name."},
        "is_disposable": {"type": "boolean", "description": "The blog category's `is_disposable` flag."},
        "is_in_trash": {"type": "boolean", "description": "The blog category's `is_in_trash` flag."},
    }},
    "BlogImage": {"type": "object", "description": "The cover image. `{}` when the post has none; otherwise all four keys.", "properties": {
        "title": {"type": "string", "description": "The image title."},
        "alternative_text": {"type": "string", "description": "The image's alternative text."},
        "file_name": {"type": "string", "description": "The image's file name: the `file_name` sent with the upload, or a name the store chose when the upload sent `filename` instead."},
        "link": {"type": "string", "description": "Where the image is served: one URL whose path ends in the file name. Its query string changes on every read, so compare links without it."},
    }},
    "BlogAuthor": {"type": "object", "description": "Who created the post.", "properties": {
        "id": {"type": "integer", "description": "The creator's `id`."},
        "name": {"type": "string", "description": "The creator's name."},
    }},
    "BlogAudience": {"type": "object", "description": "The customers and customer groups a restricted post is shown to.", "properties": {
        "customers": {"type": "array", "items": ref("BlogAudienceMember"), "description": "One entry per customer: the customer's `internal_id` as `id`, and the customer's first and last name as `name`."},
        "groups": {"type": "array", "items": ref("BlogAudienceMember"), "description": "One entry per customer group: the group's `id` and `name`."},
    }},
    "BlogAudienceMember": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "For a customer, the customer's `internal_id`; for a customer group, the group's `id`."},
        "name": {"type": "string", "description": "The customer's or customer group's name."},
    }},
    "BlogSeoConfigs": {"type": "object", "description": "The post's SEO meta tags, the same on a write and a read. Other keys inside it are ignored on a write.", "properties": {
        "meta_tag": {"type": "array", "items": ref("BlogMetaTag"), "description": "One entry per meta tag. A post without any reads `[]`."},
    }},
    "BlogMetaTag": {"type": "object", "description": "One meta tag.", "properties": {
        "name": {"type": "string", "description": "The meta tag's name, such as `description`."},
        "value": {"type": "string", "description": "The meta tag's value."},
    }},
    "BlogGroupMeta": {"type": "object", "description": "Describes the blog posts collection. Returned by the listing, a retrieve and an update, but not by a create or a replace.", "properties": {
        "blogs": ref("BlogResourceMeta"),
    }},
    "BlogResourceMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the collection is: `resource`."},
        "writable": {"type": "boolean", "description": "Whether you can write to the collection: `true`."},
        "href": {"type": "string", "description": "The collection's path, `/api/v4/admin/blogs`."},
    }},
    "BlogPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of blog posts that match your filters, across all pages."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, at most `20`, or `20` when you sent none."},
        "offset": {"type": "integer", "description": "The number of posts skipped before this page."},
        "count": {"type": "integer", "description": "The number of posts on this page."},
        "current_page": {"type": "integer", "description": "The page that `offset` falls in, counting from `1`."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up."},
        "has_next": {"type": "boolean", "description": "`true` when more posts follow this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is more than `0`."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, with your query, or `null` when `has_previous` is `false`."},
        "next_page": {"type": ["string", "null"], "description": "The full URL of the next page, with your query, or `null` when `has_next` is `false`."},
    }},
    "BlogFieldMetadata": {"type": "object", "additionalProperties": ref("BlogFieldMetadataEntry"), "description": "One entry for each of the seventeen fields of a blog post, keyed by field name. Returned only when you send `field_metadata=true` to the listing or a retrieve. Some of its notes differ from what the store does: `url` is marked `read_only`, but a replace that sends `url`, or an update that sends it beside `title`, sets it; `title` is described as unique among live posts, but a post in the trash keeps its title taken too; and `visible_to` is described as required when `visibility` is `restricted`, but a create without it is accepted."},
    "BlogFieldMetadataEntry": {"type": "object", "description": "Describes one field. `type` and `note` are always present; the other keys only where they apply.", "properties": {
        "type": {"type": "string", "description": "The field's value type."},
        "note": {"type": "string", "description": "What the field holds and how a write treats it."},
        "required": {"type": "boolean", "description": "Whether a write must send the field."},
        "read_only": {"type": "boolean", "description": "Whether the field is marked as not writable."},
        "min_length": {"type": "integer", "description": "The shortest value accepted."},
        "max_length": {"type": "integer", "description": "The longest value accepted."},
        "format": {"type": "string", "description": "The format the value takes."},
        "default": {"description": "The value used when a write leaves the field out."},
        "values": {"type": "array", "items": {}, "description": "The values the field accepts."},
        "item_type": {"type": "string", "description": "The type of each item, for a list field."},
    }},
    "BlogInput": {"type": "object", "description": "Send these fields inside `blog`. A create needs `title`; a replace needs `title` and `visibility` and resets most fields it leaves out; an update changes only the fields it sends. Any other field, including `created_on`, `created_by`, `is_disposable` and `is_in_trash`, is rejected with `400`. An `id` field here returns `500` on a create and is ignored on a replace or an update.", "properties": {
        "title": {"type": "string", "minLength": 2, "maxLength": 255, "description": "Required on create and replace. 2 to 255 characters once trimmed. No other blog post, live or in the trash, can have the same title in any letter case."},
        "url": {"type": "string", "description": "Ignored on create, where the store makes `url` from `title`. A replace sets it, and an update sets it only when you send `title` too. The store makes it lower case, turns spaces into hyphens and adds `-1` when another post has it. An empty value is ignored."},
        "content": {"type": ["string", "null"], "description": "Free text, saved as sent. A create or replace that leaves it out sets it to `null`."},
        "date": {"type": "string", "description": "`yyyy-MM-dd` or an ISO 8601 date and time, such as `2026-09-28` or `2026-09-28T10:11:12Z`. A create or replace that leaves it out sets it to the current time. Any other form is rejected with `400` (`invalid_date`)."},
        "is_published": {"type": "boolean", "description": "`true`, `false`, `1` or `0`. A create or replace that leaves it out sets it to `false`. A string, `\"true\"` included, is rejected with `400` (`invalid_boolean`)."},
        "visibility": {"type": "string", "enum": VISIBILITY_VALUES, "description": "`open`, `hidden` or `restricted`, in lower case: `OPEN` is rejected with `400` (`invalid_enum`). Defaults to `open` on create. Required on replace."},
        "visible_to": {"type": "string", "enum": ["all", "selected"], "description": "`all` or `selected`. Kept only while `visibility` is `restricted`; with `open` or `hidden` the post reads `null`. Any other value is rejected with `400` (`invalid_enum`)."},
        "categories": {"type": "array", "items": ref("BlogCategoryRefInput"), "description": "The blog categories to file the post under, each as an object holding the blog category's `id`, such as `{\"id\": 31}`. A bare number such as `[31]` returns `500`, and a blog category `id` that matches no blog category is rejected with `400` (`invalid_reference`). Sent as `[]`, or left out of a create or replace, the post is filed under the store's default category."},
        "image": ref("BlogImageInput"),
        "seo_configs": ref("BlogSeoConfigs"),
        "selected_customers": ref("BlogAudienceInput"),
    }},
    "BlogCategoryRefInput": {"type": "object", "required": ["id"], "description": "A blog category to file the post under. Other keys in the entry are ignored.", "properties": {
        "id": {"type": "integer", "description": "The blog category's `id`."},
    }},
    "BlogImageInput": {"type": "object", "description": "A cover image to upload. Nothing changes without `base64`: `{}`, `null` or a new `title` alone leaves the current image as it is. No call removes an image.", "properties": {
        "file_name": {"type": "string", "description": "The name to save the file under. `filename` is accepted instead, but the store then chooses the name itself."},
        "base64": {"type": "string", "description": "The image file, base64-encoded. A new `base64` replaces the current image."},
        "title": {"type": "string", "description": "The image title."},
        "alternative_text": {"type": "string", "description": "The image's alternative text."},
    }},
    "BlogAudienceInput": {"type": "object", "description": "Who a restricted post is shown to. Needed when `visibility` is `restricted` and `visible_to` is `selected`: without anyone in it, the write is rejected with `400`. With `visibility` `open`, or `visible_to` `all`, the audience is dropped and reads `[]`.", "properties": {
        "customers": {"type": "array", "items": {"type": "integer"}, "description": "Each customer's `internal_id`, from [List customers](" + CUSTOMERS_PAGE + "). A customer's `customer_id` here is dropped without an error."},
        "groups": {"type": "array", "items": {"type": "integer"}, "description": "Each customer group's `id`."},
    }},
    "BlogComment": {"type": "object", "description": "One comment on a blog post. The comment listing, a retrieve, and the response to adding, approving or marking a comment as spam return the same twelve fields.", "properties": {
        "id": {"type": "integer", "description": "The comment's `id`, assigned by the store. Pass it as `blog_comment_id` in a path."},
        "status": {"type": "string", "description": "`pending` on a new comment, `approved` after [Approve a comment](" + APPROVE_PAGE + "), and `spam` after marking it as spam. A `status` sent when adding the comment is stored as sent."},
        "name": {"type": ["string", "null"], "description": "The commenter's name, or `null` when none was sent."},
        "email": {"type": ["string", "null"], "description": "The commenter's email address, or `null` when none was sent."},
        "post_title": {"type": "string", "description": "The blog post's current `title`. It changes when the post's title changes."},
        "content": {"type": "string", "description": "The comment text."},
        "spam": {"type": "boolean", "description": "`true` after the comment is marked as spam. Approving the comment does not set it back to `false`."},
        "likes": {"type": "integer", "description": "`0` on a new comment."},
        "total_reply": {"type": "integer", "description": "`0` on a new comment."},
        "created_on": {"type": "string", "description": "When the comment was added, such as `2026-10-07T09:30:12`."},
        "last_updated_on": {"type": "string", "description": "When the comment last changed."},
        "replies": {"type": "array", "items": {}, "description": "`[]` on a new comment. No call on this API adds a reply."},
    }},
    "BlogCommentInput": {"type": "object", "required": ["content"], "description": "Send these fields inside `blog` and then `comment`. Fields the store does not recognise are dropped, and so are the `id`, `spam`, `likes`, `total_reply` and `post_title` fields. Leave out `status`, which is stored as sent, and `replies`, which returns `500` when it is not empty.", "properties": {
        "content": {"type": "string", "minLength": 1, "maxLength": 1000, "description": "Required. At most 1000 characters; blank is rejected with `400`."},
        "name": {"type": "string", "minLength": 2, "maxLength": 100, "description": "Optional. 2 to 100 characters once trimmed."},
        "email": {"type": "string", "format": "email", "description": "Optional. A malformed address is rejected with `400` (`invalid_email`)."},
    }},
    "BlogError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string", "description": "What went wrong, such as `blog info missing` or `Blog not found`."},
        "details": {"type": "array", "description": "One entry per rejected field or query parameter, or an empty list. A rejected `dir` is not named in it.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `unknown_parameter`, `unknown_field`, `out_of_range`, `invalid_sort_field` or `invalid_boolean`."},
            "message": {"type": ["string", "null"], "description": "`null` when the listing, the count or a retrieve rejects a query parameter."},
            "value": {"type": ["integer", "string"], "description": "The value you sent, such as `title` for a rejected `sort`, `True` for a rejected `field_metadata`, or the number `0` for `limit=0`. Left out when the listing does not accept the parameter at all."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
    "BlogServerError": {"type": "object", "description": "The body of a `500`. It has no `error` object.", "properties": {
        "status": {"type": "string", "description": "Always `error`."},
        "code": {"type": "integer", "description": "Always `500`."},
        "message": {"type": "string", "description": "Always `Unexpected Error Occurred`."},
    }},
}
