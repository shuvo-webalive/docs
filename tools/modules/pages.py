"""The Pages endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Pages"
SLUG = "pages"
BASE = "/admin/pages"
ICON = "file"

OVERVIEW_DESCRIPTION = "List, count, create, replace, update, duplicate and delete the store's pages, change a page's URL and set the landing page."
INTRO = "The Pages API has fifteen endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/pages`."

LIST_PAGE = "/api-reference/pages/list-pages"
RETRIEVE_PAGE = "/api-reference/pages/retrieve-a-page"
REPLACE_PAGE = "/api-reference/pages/replace-a-page"
UPDATE_PAGE = "/api-reference/pages/update-a-page"
DELETE_PAGE = "/api-reference/pages/delete-a-page"
URL_PAGE = "/api-reference/pages/change-the-url-of-a-page"
LANDING_PAGE = "/api-reference/pages/set-the-landing-page"
BLOCKERS_PAGE = "/api-reference/pages/get-the-delete-blockers-of-a-page"
TRASH_LIST_PAGE = "/api-reference/trash/list-items-in-the-trash"
CUSTOMERS_LIST_PAGE = "/api-reference/customers/list-customers"
CUSTOMER_GROUPS_LIST_PAGE = "/api-reference/customer-groups/list-customer-groups"

WARNING = (
    "**[Set the landing page](" + LANDING_PAGE + ") changes the landing page for the whole store.**\n"
    "  The page you name gets `landing` `true`, and the page that was the landing page gets `false`.\n"
    "  Before you call it, find the current landing page, the row with `landing` `true` in\n"
    "  [List pages](" + LIST_PAGE + ") with `limit=all`, so you can set it back. The landing page cannot be\n"
    "  deleted. [Delete a page](" + DELETE_PAGE + ") without `force=true` moves the page to the trash, and\n"
    "  with `force=true` deletes it permanently."
)

NOTES = [
    "**Wrap the fields of every write in `page`, except when you change a URL.** Create, replace and update\n"
    "  take `{\"page\": {...}}`, and a bare record is rejected with `400` and the reason `unknown_field`.\n"
    "  [Change the URL of a page](" + URL_PAGE + ") is the exception: it takes a bare `{\"url\": \"...\"}`, and a\n"
    "  body wrapped in `page` is rejected with `400`. Responses return the page inside `page`.",
    "**`PUT` replaces a page, and `PATCH` changes only the fields you send.**\n"
    "  [Replace a page](" + REPLACE_PAGE + ") needs ten fields: `name`, `title`, `subtitle`, `url`, `layout`,\n"
    "  `visibility`, `body_class`, `active`, `disable_tracking` and `password_protection`. Each one you leave\n"
    "  out is named in the `400` response with the code `required`. To change one field, use\n"
    "  [Update a page](" + UPDATE_PAGE + ").",
    "**A deleted page stays in the trash until you delete it with `force=true`.** A page in the trash is left\n"
    "  out of [List pages](" + LIST_PAGE + "), but [Retrieve a page](" + RETRIEVE_PAGE + ") still returns it\n"
    "  with `in_trash` set to `true`. [Update a page](" + UPDATE_PAGE + ") on it is rejected with `409`, and a\n"
    "  second delete without `force=true` with `400`. A page in the trash is listed in\n"
    "  [List items in the trash](" + TRASH_LIST_PAGE + ") until you delete it permanently.",
    "**Send `If-Match` to avoid overwriting someone else's change.** [Retrieve a page](" + RETRIEVE_PAGE + "),\n"
    "  replace, update, the URL change, setting the landing page and duplicating all return the page's\n"
    "  `ETag` header; creating a page does not. Send that value, quotes included, as `If-Match` on a replace,\n"
    "  update or delete. If the page changed since, the call is rejected with `412` and the reason\n"
    "  `precondition_failed`, before the body is checked.",
    "**A listing returns 20 pages per call unless you send `limit`.** `limit` takes `1` to `100`, or `all`\n"
    "  for every page in one call; with `all`, `pagination.limit` is the total. To get more, send a higher\n"
    "  `offset` while `pagination.has_next` is `true`. A query parameter the listing does not accept, or\n"
    "  one you send twice, is rejected with `400`.",
    "**`visibility` is `open`, `hidden` or `restricted`, but some older pages return other values.** A page\n"
    "  can return a `visibility` such as `OPEN` or `public`, as it was stored. Treat any value other than the\n"
    "  three as unknown. The `visibility` filter on the listing matches in any letter case, so\n"
    "  `visibility=open` also returns pages stored as `OPEN`.",
]

PAGE_ID = {
    "name": "page_id",
    "in": "path",
    "required": True,
    "description": "The page's `id`, from a listing or from the response to creating the page.",
    "schema": {"type": "integer", "example": 812},
}

IF_MATCH = {
    "name": "If-Match",
    "in": "header",
    "required": False,
    "description": "Optional. The page's current `ETag`, from [Retrieve a page](" + RETRIEVE_PAGE + ") or from the response to your last replace or update of the page, sent exactly as returned, quotes included. If the page changed since, the call is rejected with `412` and the reason `precondition_failed`, and nothing is saved.",
    "schema": {"type": "string", "example": "\"5d41402abc4b2a76\""},
}

FORCE = {
    "name": "force",
    "in": "query",
    "description": "Send `true` to delete the page permanently, from the trash or before it is in the trash. Without it, the page moves to the trash.",
    "schema": {"type": "boolean", "example": True},
}

SORT_FIELDS = ["name", "title", "visibility", "created_at", "updated_at"]

SEARCH = {"name": "search", "in": "query", "description": "Keeps only pages whose `name` or `title` contains this text.", "schema": {"type": "string", "example": "about"}}
ACTIVE = {"name": "active", "in": "query", "description": "Send `true` to keep only active pages, or `false` to keep only inactive ones.", "schema": {"type": "boolean", "example": True}}
HAS_LAYOUT = {"name": "has_layout", "in": "query", "description": "Send `true` to keep only pages that have a `layout`, or `false` to keep only pages without one.", "schema": {"type": "boolean", "example": True}}
VISIBILITY = {"name": "visibility", "in": "query", "description": "Keeps only pages with this `visibility`: `open`, `hidden` or `restricted`. It matches in any letter case, so `open` also returns pages stored as `OPEN`.", "schema": {"type": "string", "enum": ["open", "hidden", "restricted"], "example": "open"}}
CREATED_FROM = {"name": "created_from", "in": "query", "description": "Keeps only pages created on or after this date, as `YYYY-MM-DD`.", "schema": {"type": "string", "format": "date", "example": "2026-10-01"}}
CREATED_TO = {"name": "created_to", "in": "query", "description": "Keeps only pages created on or before this date, as `YYYY-MM-DD`.", "schema": {"type": "string", "format": "date", "example": "2026-10-31"}}
UPDATED_FROM = {"name": "updated_from", "in": "query", "description": "Keeps only pages last changed on or after this date, as `YYYY-MM-DD`.", "schema": {"type": "string", "format": "date", "example": "2026-10-01"}}
UPDATED_TO = {"name": "updated_to", "in": "query", "description": "Keeps only pages last changed on or before this date, as `YYYY-MM-DD`.", "schema": {"type": "string", "format": "date", "example": "2026-10-31"}}
AUTHOR = {"name": "author", "in": "query", "description": "Keeps only pages whose `author` has this `id`. Read it from a page's `author.id`.", "schema": {"type": "integer", "example": 3}}
STORE = {"name": "store", "in": "query", "description": "A store's `id`. An `id` that matches no store is rejected with `400`, the reason `unknown_reference` and the message `no store exists with id ...`. `store` is `null` on every page, yet a known store value returns every page, so this filter does not narrow the listing.", "schema": {"type": "integer"}}
NOT_IN_STORE = {"name": "not_in_store", "in": "query", "description": "Send `true` to keep pages that are not in a store. Because `store` is `null` on every page, `true` returns every page and `false` returns none.", "schema": {"type": "boolean", "example": True}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by. Without it, pages come newest `updated_at` first. Any other value is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "name"}}
ORDER = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Any other value is rejected with `400`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of pages per call, from `1` to `100`, or `all` for every page. Defaults to `20`. `pagination.limit` shows the value applied; with `all`, it is the total. `0` and values above `100` are rejected with `400` and the reason `out_of_range`.", "schema": {"oneOf": [{"type": "integer", "minimum": 1, "maximum": 100}, {"type": "string", "enum": ["all"]}], "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of pages to skip. An `offset` past the last page returns no pages, with `has_previous` set to `true`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}

FILTERS = [SEARCH, ACTIVE, HAS_LAYOUT, VISIBILITY, CREATED_FROM, CREATED_TO, UPDATED_FROM, UPDATED_TO, AUTHOR, STORE, NOT_IN_STORE]

ERROR_REF = {"$ref": "#/components/schemas/PageError"}
ROW_REF = {"$ref": "#/components/schemas/Page"}
ROW_RESPONSE = {"type": "object", "properties": {"page": ROW_REF}}

LAYOUT = {"id": 28, "name": "Standard Layout"}
AUTHOR_REF = {"id": 3, "name": "Example Admin"}
NO_PUBLISHING = {"draft": False, "draft_page_id": None, "published_page_id": None, "pending_approval": False, "pending_approval_count": 0, "pending_approval_ids": [], "disposable": False}
NO_PASSWORD = {"enabled": False, "password": None}
NO_MENU = {"enabled": False, "navigation": None}


def page_row(**fields):
    row = {
        "id": 812, "name": "About us", "title": "About us", "subtitle": None, "url": "about-us",
        "full_url": "https://your-store.example.com/about-us", "layout": LAYOUT, "visibility": "open",
        "visible_to": None, "customers": [], "customer_groups": [], "body_class": None,
        "password_protection": NO_PASSWORD, "menu_placement": NO_MENU, "active": True, "disable_tracking": False,
        "landing": False, "in_trash": False, "publishing": NO_PUBLISHING, "store": None, "author": AUTHOR_REF,
        "created_at": "2026-10-20T09:15:02Z", "updated_at": "2026-10-20T09:15:02Z",
    }
    row.update(fields)
    return row


CREATED_PAGE = page_row()
TEAM_PAGE = page_row(id=640, name="About our team", title="About our team", url="about-our-team",
                     full_url="https://your-store.example.com/about-our-team",
                        created_at="2026-09-02T04:41:19Z", updated_at="2026-10-18T02:07:44Z")
REPLACED_PAGE = page_row(subtitle="Who we are", body_class="about-page", updated_at="2026-10-20T09:21:40Z")
PATCHED_PAGE = page_row(title="About our company", updated_at="2026-10-20T09:24:11Z")
MOVED_PAGE = page_row(title="About our company", url="about-our-company",
                      full_url="https://your-store.example.com/about-our-company", updated_at="2026-10-20T09:26:35Z")
LANDING_SET_PAGE = page_row(landing=True, updated_at="2026-10-20T09:28:03Z")
COPY_PAGE = page_row(id=813, name="About us - Copy", url="about-us-copy",
                     full_url="https://your-store.example.com/about-us-copy",
                     created_at="2026-10-20T09:30:12Z", updated_at="2026-10-20T09:30:12Z")

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

CREATE_BODY = {"page": {"name": "About us", "title": "About us", "visibility": "open", "layout": {"id": 28}}}
REPLACE_BODY = {"page": {
    "name": "About us", "title": "About us", "subtitle": "Who we are", "url": "about-us", "layout": {"id": 28},
    "visibility": "open", "body_class": "about-page", "active": True, "disable_tracking": False,
    "password_protection": {"enabled": False},
}}
PATCH_BODY = {"page": {"title": "About our company"}}
URL_BODY = {"url": "about-our-company"}

LIST_400 = (
    "A query parameter is not one the listing accepts (reason `unknown_parameter`), or you sent one twice "
    "(reason `duplicate_parameter`). Or `limit` is `0` or more than `100` (reason `out_of_range`), `sort` is not "
    "one of the five sort fields (reason `invalid_enum`), `order` is not `asc` or `desc` (reason `invalid_enum`), or `store` names no store "
    "(reason `unknown_reference`)."
)
WRAPPER_400 = "The fields are not wrapped in `page` (reason `unknown_field`)"
FIELD_RULES_400 = (
    "a field breaks a rule of the request body: `title` or `subtitle` is 1 character or longer than 255, `layout` "
    "is a bare number instead of `{\"id\": ...}` (reason `invalid_type`), or the body sends the read-only `store` "
    "(reason `read_only`)"
)
DUPLICATE_409 = (
    "Another page already has that `name` (`details[].code` `duplicate`, `details[].field` `page.name`), or that "
    "`url`, and the message names the page that has it."
)
NOT_FOUND_404 = (
    "No page has that `page_id`, for example because you deleted it with `force=true`. The reason is `not_found` "
    "and the message is `No page with id ...`, ending in the `page_id` you sent."
)
STALE_412 = "Your `If-Match` value is not the page's current `ETag`. The reason is `precondition_failed`, and nothing is saved."

ENDPOINTS = [
    {
        "key": "list_pages",
        "slug": "list-pages",
        "title": "List pages",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 pages per call, newest change first, with paging details.",
        "description": "Returns the pages that are not in the trash in `pages`, 20 per call unless you send `limit`, and a `pagination` block. Pages come newest `updated_at` first unless you send `sort` and `order`. Filter with `search`, `active`, `has_layout`, `visibility`, the created and updated date ranges, `author`, `store` and `not_in_store`. Any other query parameter, or a parameter you send twice, is rejected with `400`.",
        "parameters": FILTERS + [SORT, ORDER, LIMIT, OFFSET],
        "responses": {
            "200": {
                "description": "The pages on this call in `pages`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. Each page has the same fields [Retrieve a page](" + RETRIEVE_PAGE + ") returns, except that a set `password_protection.password` is masked as `***`. The response has no `ETag` header.",
                "schema": {"type": "object", "properties": {
                    "pages": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/PagePagination"},
                }},
                "example": {"pages": [TEAM_PAGE, CREATED_PAGE], "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": LIST_400, "schema": ERROR_REF},
        },
        "example_call": {"query": {"search": "about", "visibility": "open", "sort": "name", "order": "asc"}},
    },
    {
        "key": "head_pages",
        "slug": "check-the-pages-list",
        "title": "Check the pages list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns `200` and the headers of the pages listing, with no body.",
        "description": "Returns `200` with headers only and no body. To read the pages, use [List pages](" + LIST_PAGE + ").",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "count_pages",
        "slug": "count-pages",
        "title": "Count pages",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of pages that match the listing's filters, as `total`.",
        "description": "Returns the number of pages as `total`, at the top level of the body. The filters of [List pages](" + LIST_PAGE + ") narrow the count the same way. `sort`, `order`, `limit` and `offset` are ignored, and any other query parameter is rejected with `400`.",
        "parameters": FILTERS,
        "responses": {
            "200": {
                "description": "The number of matching pages.",
                "schema": {"$ref": "#/components/schemas/PageCount"},
                "example": {"total": 2},
            },
            "400": {"description": "You sent a query parameter the count does not accept.", "schema": ERROR_REF},
        },
        "example_call": {"query": {"active": "true", "has_layout": "true"}},
    },
    {
        "key": "head_pages_count",
        "slug": "check-the-page-count",
        "title": "Check the page count",
        "method": "HEAD",
        "path": BASE + "/count",
        "summary": "Returns `200` and the headers of the page count, with no body.",
        "description": "Returns `200` with headers only and no body. To read the number, use [Count pages](/api-reference/pages/count-pages).",
        "responses": {
            "200": {"description": "Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_page",
        "slug": "create-a-page",
        "title": "Create a page",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a page and returns it with its `id`, which other calls take as `page_id`.",
        "description": "Send the fields inside `page`; `name` and `visibility` are required. The store makes the page's `url` from `name` when you do not send one. A `name` or `url` that another page has is rejected with `409`. The response has a `Location` header but no `ETag`, so retrieve the page before you send `If-Match`.",
        "body": {"schema": {"$ref": "#/components/schemas/PageCreateBody"}, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new page, with its `id`, which the other calls take as `page_id`. The `Location` header holds the URL of the new page. The response has no `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"page": CREATED_PAGE},
            },
            "400": {"description": WRAPPER_400 + "; `name` or `visibility` is missing; or " + FIELD_RULES_400 + ".", "schema": ERROR_REF},
            "409": {"description": DUPLICATE_409, "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_page",
        "slug": "retrieve-a-page",
        "title": "Retrieve a page",
        "method": "GET",
        "path": BASE + "/{page_id}",
        "summary": "Returns the page whose `id` you pass as `page_id`, with an `ETag` header.",
        "description": "Returns one page under the `page` key, with `password_protection.password` as saved. A page in the trash still returns `200`, with `in_trash` set to `true`. Query parameters you add are ignored. Send the `ETag` header's value as `If-Match` on a later replace, update or delete.",
        "parameters": [PAGE_ID],
        "responses": {
            "200": {
                "description": "The page, with an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"page": CREATED_PAGE},
            },
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "head_page",
        "slug": "check-a-page",
        "title": "Check a page",
        "method": "HEAD",
        "path": BASE + "/{page_id}",
        "summary": "Returns headers only for the page in `page_id`, including its `ETag`.",
        "description": "Returns `200` with headers only and no body. The `ETag` is the same one [Retrieve a page](" + RETRIEVE_PAGE + ") returns, so you can check whether the page changed without reading it.",
        "parameters": [PAGE_ID],
        "responses": {
            "200": {"description": "Headers only, including the page's `ETag`. No body."},
            "404": {"description": "No page has that `page_id`. Headers only, no body."},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "update_page",
        "slug": "replace-a-page",
        "title": "Replace a page",
        "method": "PUT",
        "path": BASE + "/{page_id}",
        "summary": "Replaces a page with the ten required fields you send in `page`, and returns it.",
        "description": "Send the whole page inside `page`. `name`, `title`, `subtitle`, `url`, `layout`, `visibility`, `body_class`, `active`, `disable_tracking` and `password_protection` are required, and `subtitle`, `body_class` and `layout` take `null`. Each required field you leave out is named in the `400` response with the code `required`. To change only some fields, use [Update a page](" + UPDATE_PAGE + ").",
        "parameters": [PAGE_ID, IF_MATCH],
        "body": {"schema": {"$ref": "#/components/schemas/PageReplaceBody"}, "example": REPLACE_BODY},
        "responses": {
            "200": {
                "description": "The page after the replace, with an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"page": REPLACED_PAGE},
            },
            "400": {"description": "A required field is missing: `details` has one entry per missing field, with the code `required`. Or " + WRAPPER_400[0].lower() + WRAPPER_400[1:] + ", or " + FIELD_RULES_400 + ".", "schema": ERROR_REF},
            "409": {"description": DUPLICATE_409, "schema": ERROR_REF},
            "412": {"description": STALE_412, "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "patch_page",
        "slug": "update-a-page",
        "title": "Update a page",
        "method": "PATCH",
        "path": BASE + "/{page_id}",
        "summary": "Changes only the fields you send inside `page` and returns the page.",
        "description": "Send only the fields to change, inside `page`; every field you leave out keeps its value. An empty `page` object is rejected with `400`. A page in the trash cannot be changed: the call is rejected with `409` and the reason `in_trash`. Send `If-Match` to have the call rejected with `412` when the page changed since you read it.",
        "parameters": [PAGE_ID, IF_MATCH],
        "body": {"schema": {"$ref": "#/components/schemas/PagePatchBody"}, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The page after the change, with an `ETag` header. Fields you did not send keep their values.",
                "schema": ROW_RESPONSE,
                "example": {"page": PATCHED_PAGE},
            },
            "400": {"description": "`page` is empty, so there is no field to change. Or " + WRAPPER_400[0].lower() + WRAPPER_400[1:] + ", or " + FIELD_RULES_400 + ".", "schema": ERROR_REF},
            "409": {"description": "The page is in the trash (`details[].code` `in_trash`). Or " + DUPLICATE_409[0].lower() + DUPLICATE_409[1:], "schema": ERROR_REF},
            "412": {"description": STALE_412, "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "delete_page",
        "slug": "delete-a-page",
        "title": "Delete a page",
        "method": "DELETE",
        "path": BASE + "/{page_id}",
        "summary": "Moves a page to the trash, or deletes it permanently with `force=true`.",
        "description": "Without `force`, the page moves to the trash and the call returns `204`: [Retrieve a page](" + RETRIEVE_PAGE + ") still returns it with `in_trash` set to `true`, and [List pages](" + LIST_PAGE + ") leaves it out. Send `force=true` to delete the page permanently, from the trash or before it is in the trash; retrieving it then returns `404`. A second delete without `force=true` is rejected with `400`. You cannot delete the landing page: the call is rejected with `409`.",
        "parameters": [PAGE_ID, FORCE, IF_MATCH],
        "responses": {
            "204": {"description": "The page is in the trash, or deleted permanently with `force=true`. No body."},
            "400": {"description": "The page is already in the trash and you did not send `force=true`. The message is `The page could not be deleted.` and `details` is empty.", "schema": ERROR_REF},
            "409": {"description": "The page is the landing page (`details[].code` `landing_page`). Make another page the landing page first with [Set the landing page](" + LANDING_PAGE + ").", "schema": ERROR_REF},
            "412": {"description": "Your `If-Match` value is not the page's current `ETag`. The reason is `precondition_failed`, and the page is not deleted.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "update_page_url",
        "slug": "change-the-url-of-a-page",
        "title": "Change the URL of a page",
        "method": "PUT",
        "path": BASE + "/{page_id}/url",
        "summary": "Sets a page's `url` from a bare `{\"url\": ...}` body and returns the page.",
        "description": "Send only `url`, at the top level of the body. A body wrapped in `page` is rejected with `400`, and a request with no body with `415`. A `url` that another page has is rejected with `409`. The response returns the whole page with an `ETag` header.",
        "parameters": [PAGE_ID],
        "body": {"schema": {"$ref": "#/components/schemas/PageUrlInput"}, "example": URL_BODY},
        "responses": {
            "200": {
                "description": "The page with its new `url` and `full_url`, with an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"page": MOVED_PAGE},
            },
            "400": {"description": "The body wraps `url` in `page`. Send `{\"url\": \"...\"}` at the top level.", "schema": ERROR_REF},
            "409": {"description": "Another page already has that `url`.", "schema": ERROR_REF},
            "415": {"description": "The request has no body."},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "set_landing_page",
        "slug": "set-the-landing-page",
        "title": "Set the landing page",
        "method": "PATCH",
        "path": BASE + "/{page_id}/landing",
        "summary": "Makes a page the store's landing page; the previous landing page stops being it.",
        "description": "Send no body. The page you name gets `landing` set to `true`, and the page that was the landing page gets `false`, so this call changes two pages. Before you call it, note the current landing page, the row with `landing` `true` in [List pages](" + LIST_PAGE + ") with `limit=all`, so you can set it back. The landing page cannot be deleted, so make another page the landing page before you delete this one.",
        "parameters": [PAGE_ID],
        "responses": {
            "200": {
                "description": "The page, now the landing page, with an `ETag` header.",
                "schema": ROW_RESPONSE,
                "example": {"page": LANDING_SET_PAGE},
            },
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "get_page_delete_blockers",
        "slug": "get-the-delete-blockers-of-a-page",
        "title": "Get the delete blockers of a page",
        "method": "GET",
        "path": BASE + "/{page_id}/delete-blockers",
        "summary": "Returns whether a page can be deleted and, if not, what stops the delete.",
        "description": "Returns `can_delete`, a `blockers` list and a `linked` list, and changes nothing. Each blocker has a `code` and a `message`: the landing page returns `can_delete` set to `false` and a blocker with the code `landing_page` and the message `This page is the store landing page. Set another landing page first.` A page in the trash still returns `200`.",
        "parameters": [PAGE_ID],
        "responses": {
            "200": {
                "description": "Whether a delete would succeed, and what blocks it.",
                "schema": {"$ref": "#/components/schemas/PageDeleteBlockers"},
                "example": {"can_delete": True, "blockers": [], "linked": []},
            },
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "head_page_delete_blockers",
        "slug": "check-the-delete-blockers-of-a-page",
        "title": "Check the delete blockers of a page",
        "method": "HEAD",
        "path": BASE + "/{page_id}/delete-blockers",
        "summary": "Returns headers only, with no body, for the delete check of the page in `page_id`.",
        "description": "Returns `200` with headers only and no body. To read `can_delete` and the blockers, use [Get the delete blockers of a page](" + BLOCKERS_PAGE + ").",
        "parameters": [PAGE_ID],
        "responses": {
            "200": {"description": "Headers only, no body."},
            "404": {"description": "No page has that `page_id`. Headers only, no body."},
        },
        "example_call": {"path": {"page_id": 812}},
    },
    {
        "key": "duplicate_page",
        "slug": "duplicate-a-page",
        "title": "Duplicate a page",
        "method": "POST",
        "path": BASE + "/{page_id}/duplicate",
        "summary": "Copies a page and returns the copy, its name ending ` - Copy` and its URL `-copy`.",
        "description": "Send no body, or `{}`; a body with any field is rejected with `400` and the reason `not_allowed`. The copy is named `<name> - Copy` with the URL `<url>-copy`, and the next copy `<name> - Copy 1` at `<url>-copy-1`. The copy keeps the access list and the password, and has `landing` and `menu_placement.enabled` set to `false`.",
        "parameters": [PAGE_ID],
        "responses": {
            "201": {
                "description": "The copy, with its own `id`, which the other calls take as `page_id`. The response has `Location` and `ETag` headers.",
                "schema": ROW_RESPONSE,
                "example": {"page": COPY_PAGE},
            },
            "400": {"description": "The body has a field (`details[].code` `not_allowed`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"page_id": 812}},
    },
]

REFERENCE_REF = {"$ref": "#/components/schemas/PageReference"}

INPUT_PROPERTIES = {
    "name": {"type": "string", "description": "The page's name. No other page may have the same name."},
    "title": {"type": "string", "description": "Empty, or 2 to 255 characters."},
    "subtitle": {"type": ["string", "null"], "description": "Empty, or 2 to 255 characters. `null` for no subtitle."},
    "url": {"type": "string", "description": "The page's URL path. No other page may have the same `url`. On create, the store makes it from `name` when you leave it out."},
    "layout": {"oneOf": [{"type": "object", "properties": {"id": {"type": "integer"}}}, {"type": "null"}], "description": "`{\"id\": ...}` with a layout's `id`, such as the `layout.id` of an existing page, or `null` for no layout. A bare number is rejected with `400`."},
    "visibility": {"type": "string", "enum": ["open", "hidden", "restricted"], "description": "Who can see the page."},
    "visible_to": {"type": "string", "enum": ["all", "selected"], "description": "Only with `visibility` `restricted`."},
    "customers": {"type": "array", "description": "The customers on the access list. Each entry is a customer's `customer_id` from [List customers](" + CUSTOMERS_LIST_PAGE + "), as a number or as `{\"id\": ...}`.", "items": {"oneOf": [{"type": "integer"}, {"type": "object", "properties": {"id": {"type": "integer"}}}]}},
    "customer_groups": {"type": "array", "description": "The customer groups on the access list. Each entry is a group's `id` from [List customer groups](" + CUSTOMER_GROUPS_LIST_PAGE + "), as a number or as `{\"id\": ...}`.", "items": {"oneOf": [{"type": "integer"}, {"type": "object", "properties": {"id": {"type": "integer"}}}]}},
    "body_class": {"type": ["string", "null"], "description": "A CSS class for the page body, or `null`."},
    "password_protection": {"type": "object", "description": "Send `{\"enabled\": true, \"password\": \"...\"}` to protect the page with a password. Sending `\"enabled\": false` keeps the stored password.", "properties": {
        "enabled": {"type": "boolean"},
        "password": {"type": "string"},
    }},
    "menu_placement": {"type": "object", "description": "Whether the page is linked from a navigation. When `enabled` is `true`, `navigation` must be `{\"id\": ...}` with the navigation's `id`.", "properties": {
        "enabled": {"type": "boolean"},
        "navigation": {"type": ["object", "null"], "properties": {"id": {"type": "integer"}}},
    }},
    "active": {"type": "boolean", "description": "Whether the page is active."},
    "disable_tracking": {"type": "boolean", "description": "Whether tracking is turned off on the page."},
}

READ_ONLY_NOTE = "`id`, `full_url`, `landing`, `in_trash`, `publishing`, `store`, `author`, `created_at` and `updated_at` are read-only; sending `store` is rejected with `400`."

SCHEMAS = {
    "Page": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The page's `id`, set by the store. Pass it as `page_id` in the path of the other calls."},
        "name": {"type": "string", "description": "The page's name, unique across pages."},
        "title": {"type": "string", "description": "The page's title. Empty, or 2 to 255 characters."},
        "subtitle": {"type": ["string", "null"], "description": "The page's subtitle, or `null`."},
        "url": {"type": "string", "description": "The page's URL path, unique across pages, such as `about-us`."},
        "full_url": {"type": "string", "description": "The page's full address, ending in `url`. Read-only."},
        "layout": {"oneOf": [REFERENCE_REF, {"type": "null"}], "description": "The page's layout, with `id` and `name`, or `null` for no layout."},
        "visibility": {"type": "string", "description": "`open`, `hidden` or `restricted`. Some older pages return another value, such as `OPEN` or `public`, as it was stored."},
        "visible_to": {"type": ["string", "null"], "description": "`all` or `selected` on a restricted page, and `null` otherwise."},
        "customers": {"type": "array", "items": REFERENCE_REF, "description": "The customers on the access list. `id` is the customer's `customer_id`."},
        "customer_groups": {"type": "array", "items": REFERENCE_REF, "description": "The customer groups on the access list, with each group's `id` and `name`."},
        "body_class": {"type": ["string", "null"], "description": "The CSS class of the page body, or `null`."},
        "password_protection": {"$ref": "#/components/schemas/PagePasswordProtection"},
        "menu_placement": {"$ref": "#/components/schemas/PageMenuPlacement"},
        "active": {"type": "boolean", "description": "Whether the page is active."},
        "disable_tracking": {"type": "boolean", "description": "Whether tracking is turned off on the page."},
        "landing": {"type": "boolean", "description": "`true` only on the store's landing page. Exactly one page has it, and only [Set the landing page](" + LANDING_PAGE + ") changes it. Read-only."},
        "in_trash": {"type": "boolean", "description": "`true` when the page is in the trash. Read-only."},
        "publishing": {"$ref": "#/components/schemas/PagePublishing"},
        "store": {"description": "`null` on every page. Read-only."},
        "author": {"$ref": "#/components/schemas/PageReference", "description": "The page's author, an operator, with `id` and `name`. The `author` filter of the listing takes this `id`. Read-only."},
        "created_at": {"type": "string", "description": "When the page was created, such as `2026-10-20T09:15:02Z`. Read-only."},
        "updated_at": {"type": "string", "description": "When the page last changed. Read-only."},
    }},
    "PageReference": {"type": "object", "description": "An `id` and `name` pair for a layout, a customer, a customer group, a navigation or an author. A write names one by `{\"id\": ...}`; `name` is read-only.", "properties": {
        "id": {"type": "integer", "description": "The referenced record's `id`. For a customer, its `customer_id`."},
        "name": {"type": "string", "description": "The referenced record's name."},
    }},
    "PagePasswordProtection": {"type": "object", "description": "The page's password. A listing row masks `password` as `***`; retrieving the page and every write return it as saved.", "properties": {
        "enabled": {"type": "boolean", "description": "Whether the page asks for the password."},
        "password": {"type": ["string", "null"], "description": "The password. Turning protection off keeps it stored."},
    }},
    "PageMenuPlacement": {"type": "object", "description": "Whether the page is linked from a navigation.", "properties": {
        "enabled": {"type": "boolean", "description": "`true` when the page is linked from a navigation."},
        "navigation": {"oneOf": [REFERENCE_REF, {"type": "null"}], "description": "The navigation, with `id` and `name`, or `null` when the page is not linked from one."},
    }},
    "PagePublishing": {"type": "object", "description": "The page's draft and approval state. Read-only.", "properties": {
        "draft": {"type": "boolean"},
        "draft_page_id": {"type": ["integer", "null"], "description": "A page `id`, or `null`."},
        "published_page_id": {"type": ["integer", "null"], "description": "A page `id`, or `null`."},
        "pending_approval": {"type": "boolean"},
        "pending_approval_count": {"type": "integer"},
        "pending_approval_ids": {"type": "array", "items": {"type": ["integer", "null"]}},
        "disposable": {"type": "boolean"},
    }},
    "PageCreateInput": {"type": "object", "required": ["name", "visibility"], "description": "Send these fields inside `page`. " + READ_ONLY_NOTE, "properties": INPUT_PROPERTIES},
    "PageReplaceInput": {"type": "object", "required": ["name", "title", "subtitle", "url", "layout", "visibility", "body_class", "active", "disable_tracking", "password_protection"], "description": "Send the whole page inside `page`. The ten required fields must all be present; `subtitle`, `body_class` and `layout` take `null`. " + READ_ONLY_NOTE, "properties": INPUT_PROPERTIES},
    "PagePatchInput": {"type": "object", "minProperties": 1, "description": "Send only the fields to change, inside `page`. Fields you leave out keep their values. " + READ_ONLY_NOTE, "properties": INPUT_PROPERTIES},
    "PageCreateBody": {"type": "object", "required": ["page"], "properties": {"page": {"$ref": "#/components/schemas/PageCreateInput"}}},
    "PageReplaceBody": {"type": "object", "required": ["page"], "properties": {"page": {"$ref": "#/components/schemas/PageReplaceInput"}}},
    "PagePatchBody": {"type": "object", "required": ["page"], "properties": {"page": {"$ref": "#/components/schemas/PagePatchInput"}}},
    "PageUrlInput": {"type": "object", "required": ["url"], "description": "Send `url` at the top level of the body, not inside `page`.", "properties": {
        "url": {"type": "string", "description": "The new URL path. No other page may have it."},
    }},
    "PagePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of pages that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`. With `limit=all`, the total."},
        "offset": {"type": "integer", "description": "The number of pages skipped before this call's rows."},
        "has_previous": {"type": "boolean", "description": "`true` when pages come before this call's rows. An `offset` past the last page also returns `true`."},
        "has_next": {"type": "boolean", "description": "`true` when more pages follow."},
    }},
    "PageCount": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of pages that match the filters you sent."},
    }},
    "PageDeleteBlocker": {"type": "object", "description": "One reason the page cannot be deleted.", "properties": {
        "code": {"type": "string", "description": "The reason, such as `landing_page`."},
        "message": {"type": "string", "description": "The reason in words."},
    }},
    "PageDeleteBlockers": {"type": "object", "properties": {
        "can_delete": {"type": "boolean", "description": "`true` when a delete would succeed."},
        "blockers": {"type": "array", "items": {"$ref": "#/components/schemas/PageDeleteBlocker"}, "description": "What stops the delete. Empty when `can_delete` is `true`."},
        "linked": {"type": "array", "description": "A list that has been empty on every page read so far."},
    }},
    "PageError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason for the rejection, such as `invalid_request`, `not_found` or `precondition_failed`."},
        "message": {"type": "string", "description": "What went wrong, such as `The page could not be deleted.` or `1 parameter failed validation.`"},
        "details": {"type": "array", "description": "One entry per rejected field or query parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter, such as `page.name` or `limit`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `duplicate`, `unknown_field`, `in_trash`, `landing_page`, `not_allowed`, `unknown_parameter` or `out_of_range`."},
            "message": {"type": ["string", "null"], "description": "The rule that failed, such as `must be a whole number from 1 to 100, or all`, or `null`."},
            "value": {"type": "string", "description": "The value you sent, as text, for a rejected query parameter."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
