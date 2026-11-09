"""The Dashboard sections endpoint, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Dashboard sections"
SLUG = "dashboard-sections"
BASE = "/admin/dashboard/sections"
ICON = "table-cells"

SECTIONS = ["ecommerce", "content", "bookings", "courses", "blog"]
DURATIONS = [
    "today", "yesterday", "last_24_hours", "last_7_days", "last_30_days", "this_month", "last_month", "last_3_months",
    "last_6_months", "last_12_months", "last_24_months", "last_36_months", "last_48_months", "last_60_months", "custom",
]

OVERVIEW_DESCRIPTION = "Read what one tab of the admin dashboard's section tabs shows: order updates and best sellers, content to review, bookings, courses or blog activity."
INTRO = "The Dashboard sections API has one endpoint, and you can call it from all seven SDKs. Its path starts with `/api/v4/admin/dashboard/sections`."

GET_PAGE = "/api-reference/dashboard-sections/get-a-dashboard-section"

WARNING = None

NOTES = [
    "**Pass the tab's name as `section`.** `section` is one of `ecommerce`, `content`, `bookings`, `courses` or\n"
    "  `blog`. Any other value is rejected with `404`, the reason `not_found` and the message\n"
    "  `dashboard section not found`, with the detail on the field `key`.",
    "**Each tab returns its own fields beside `section` and `period`.** `ecommerce` returns `order_updates` and\n"
    "  `best_selling_products`. `content` returns `content_updates` and `top_pages`. `bookings` returns\n"
    "  `needs_attention` and `upcoming`. `courses` returns `new_enrolments`, `unpaid_orders` and `popular_courses`.\n"
    "  `blog` returns `comments_to_moderate`, `drafts_to_publish` and `most_viewed_posts`. A field of another tab is\n"
    "  not in the response.",
    "**The period is the one the reports use.** Send `duration`, or `start_date` with `end_date` as `YYYY-MM-DD`.\n"
    "  Without either, the period is `last_30_days`. A bad value is rejected with `400`. A query parameter the call does not\n"
    "  know is ignored.",
    "**Lists can be empty.** A period with no best sellers returns `best_selling_products` as an empty list, and a\n"
    "  store without bookings or courses returns empty `upcoming` and `popular_courses` lists.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The tab to read: `ecommerce`, `content`, `bookings`, `courses` or `blog`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "blog"},
}
PERIOD_PARAMS = [
    {"name": "duration", "in": "query", "description": "The period the tab covers: " + ", ".join("`%s`" % d for d in DURATIONS) + ". Defaults to `last_30_days`.", "schema": {"type": "string", "enum": DURATIONS, "example": "last_7_days"}},
    {"name": "start_date", "in": "query", "description": "The first day of a custom period, as `YYYY-MM-DD`. Send it with `end_date`; the response then has `duration` `custom`. A `start_date` without `end_date` is rejected with `400` and the detail code `required` on `end_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-01"}},
    {"name": "end_date", "in": "query", "description": "The last day of a custom period, as `YYYY-MM-DD`. Send it with `start_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-31"}},
]

ERROR_REF = {"$ref": "#/components/schemas/DashboardSectionError"}
PERIOD = {
    "duration": "last_30_days", "start_date": "2026-10-10", "end_date": "2026-11-09",
    "previous_start_date": "2026-09-10", "previous_end_date": "2026-10-10", "time_zone": "Africa/Abidjan", "currency": "USD",
}

ENDPOINTS = [
    {
        "key": "get_dashboard_section",
        "slug": "get-a-dashboard-section",
        "title": "Get a dashboard section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns what one tab of the dashboard's section tabs shows for a period.",
        "description": "Returns `section` (the tab you asked for), `period`, and the fields of that tab: order updates and best sellers for `ecommerce`, content to review and top pages for `content`, bookings for `bookings`, enrolments and unpaid orders for `courses`, and comments, drafts and most viewed posts for `blog`. The period is `last_30_days` unless you send `duration`, or `start_date` with `end_date`.",
        "parameters": [SECTION] + PERIOD_PARAMS,
        "responses": {
            "200": {
                "description": "The tab's name, the period, and the tab's own fields. Fields of other tabs are not in the response.",
                "schema": {"$ref": "#/components/schemas/DashboardSection"},
                "example": {
                    "section": "blog", "period": PERIOD, "comments_to_moderate": 1,
                    "drafts_to_publish": {"count": 12, "latest": [{"post": {"id": 18049, "name": "Spring recipes"}, "updated_at": "2026-10-29T06:38:33Z"}]},
                    "most_viewed_posts": [{"post": {"id": 18012, "name": "Welcome"}, "views": 34}],
                },
            },
            "400": {"description": "A period value is bad: `duration` is not one of the values above or is sent twice, or only one of `start_date` and `end_date` is sent. The reason is `invalid_request`, and every failed field is listed in `details`.", "schema": ERROR_REF},
            "404": {"description": "`section` is not one of the five tabs. The reason is `not_found`, the message is `dashboard section not found`, and the detail is on the field `key`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"section": "blog"}, "query": {"duration": "last_7_days"}},
    },
]


def whole(description):
    return {"type": "integer", "description": description}


ENTITY = {"type": "object", "properties": {
    "id": whole("The page's, product's or post's `id`."),
    "name": {"type": "string", "description": "Its name."},
}}

SCHEMAS = {
    "DashboardSectionPeriod": {"type": "object", "description": "The period the tab covers and the one before it.", "properties": {
        "duration": {"type": "string", "description": "The `duration` applied, or `custom` when you sent dates."},
        "start_date": {"type": "string", "description": "The first day of the period, as `YYYY-MM-DD`."},
        "end_date": {"type": "string", "description": "The last day of the period."},
        "previous_start_date": {"type": "string", "description": "The first day of the period before it."},
        "previous_end_date": {"type": "string", "description": "The last day of the period before it."},
        "time_zone": {"type": "string", "description": "The time zone the days are counted in."},
        "currency": {"type": "string", "description": "The currency of money figures."},
    }},
    "DashboardSectionEntity": ENTITY,
    "DashboardSection": {"type": "object", "description": "Only the fields of the tab you asked for are present.", "properties": {
        "section": {"type": "string", "enum": SECTIONS, "description": "The tab you asked for."},
        "period": {"$ref": "#/components/schemas/DashboardSectionPeriod"},
        "order_updates": {"type": "object", "description": "`ecommerce`. Counts of orders that need attention.", "properties": {
            "low_stock_items": whole("The number of items low in stock."),
            "pending_fulfillment": whole("The number of orders waiting to be fulfilled."),
            "payments_to_capture": whole("The number of payments waiting to be captured."),
        }},
        "best_selling_products": {"type": "array", "description": "`ecommerce`. The best sellers of the period, highest `units_sold` first. Empty when there are none.", "items": {"type": "object", "properties": {
            "product": {"$ref": "#/components/schemas/DashboardSectionEntity"},
            "units_sold": whole("The number of units sold."),
        }}},
        "content_updates": {"type": "array", "description": "`content`. Recently changed content.", "items": {"type": "object", "properties": {
            "key": {"type": "string", "description": "The kind of content, such as `recent_page`."},
            "label": {"type": "string", "description": "The content's name."},
            "count": {"type": "string", "description": "An empty string."},
        }}},
        "top_pages": {"type": "array", "description": "`content`. The most viewed pages of the period.", "items": {"type": "object", "properties": {
            "page": {"$ref": "#/components/schemas/DashboardSectionEntity"},
            "views": whole("The number of views."),
        }}},
        "needs_attention": {"type": "object", "description": "`bookings`. Bookings that need attention.", "properties": {
            "count": whole("The number of bookings."),
            "latest": {"type": "array", "description": "The latest of them.", "items": {}},
        }},
        "upcoming": {"type": "array", "description": "`bookings`. Upcoming bookings.", "items": {}},
        "new_enrolments": whole("`courses`. The number of new enrolments."),
        "unpaid_orders": whole("`courses`. The number of unpaid course orders."),
        "popular_courses": {"type": "array", "description": "`courses`. The popular courses.", "items": {}},
        "comments_to_moderate": whole("`blog`. The number of comments waiting for moderation."),
        "drafts_to_publish": {"type": "object", "description": "`blog`. Draft posts.", "properties": {
            "count": whole("The number of drafts."),
            "latest": {"type": "array", "description": "The latest drafts.", "items": {"type": "object", "properties": {
                "post": {"$ref": "#/components/schemas/DashboardSectionEntity"},
                "updated_at": {"type": "string", "description": "When the draft last changed."},
            }}},
        }},
        "most_viewed_posts": {"type": "array", "description": "`blog`. The most viewed posts of the period. Can be empty.", "items": {"type": "object", "properties": {
            "post": {"$ref": "#/components/schemas/DashboardSectionEntity"},
            "views": whole("The number of views."),
        }}},
    }},
    "DashboardSectionError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string", "description": "What went wrong, such as `dashboard section not found`."},
        "details": {"type": "array", "description": "One entry per rejected value.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field, such as `key`, `duration` or `end_date`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `not_found`, `invalid_enum` or `required`."},
            "message": {"type": "string", "description": "The rule that failed."},
            "value": {"type": "string", "description": "The value you sent."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
