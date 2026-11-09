"""The Dashboard KPIs endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Dashboard KPIs"
SLUG = "dashboard-kpis"
BASE = "/admin/dashboard"
ICON = "gauge"

KPI_KEYS = [
    "total_sales", "total_orders", "aov", "net_sales", "conversion_rate", "cart_to_order", "cart_abandonment_rate",
    "refund_rate", "returning_customer_rate", "new_customers", "sessions", "pending_fulfillment", "total_page_views",
    "total_visitors", "blog_views", "blog_new_comments", "blog_published", "blog_pending_comments", "total_bookings",
    "booking_upcoming_today", "booking_revenue", "booking_active_services", "course_enrolments", "course_revenue",
    "course_orders", "course_unpaid", "course_active",
]
DURATIONS = [
    "today", "yesterday", "last_24_hours", "last_7_days", "last_30_days", "this_month", "last_month", "last_3_months",
    "last_6_months", "last_12_months", "last_24_months", "last_36_months", "last_48_months", "last_60_months", "custom",
]

OVERVIEW_DESCRIPTION = "List the metrics the dashboard's KPI tiles can show, read the tiles in use with their figures for a period, and choose which 2 to 5 tiles the dashboard shows."
INTRO = "The Dashboard KPIs API has three endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/dashboard`."

OPTIONS_PAGE = "/api-reference/dashboard-kpis/list-kpi-options"
SELECTION_PAGE = "/api-reference/dashboard-kpis/get-the-kpi-selection"
UPDATE_PAGE = "/api-reference/dashboard-kpis/update-the-kpi-selection"

WARNING = (
    "**[Update the KPI selection](" + UPDATE_PAGE + ") changes the tiles on the dashboard of every admin.**\n"
    "  It writes the KPI tiles of the store's default dashboard layout, so the change shows at once for everyone,\n"
    "  and the layout's `updated_at` moves. Before you call it, read the keys in `selected` from\n"
    "  [List KPI options](" + OPTIONS_PAGE + "), so you can send them back to restore the tiles."
)

NOTES = [
    "**Select metrics by `key`, not by `code`.** Each metric has a `key` and a `code`. For most metrics they are\n"
    "  the same. For some they differ, such as `key` `aov` with `code` `average_order_value`. [Update the KPI\n"
    "  selection](" + UPDATE_PAGE + ") takes the `key`.",
    "**The dashboard shows 2 to 5 tiles.** `min` and `max` in [List KPI options](" + OPTIONS_PAGE + ") give the\n"
    "  limits. The store has 27 metrics in five groups: `ecommerce`, `content`, `blog`, `bookings` and `courses`.",
    "**The figures follow the period you send.** [Get the KPI selection](" + SELECTION_PAGE + ") and the update\n"
    "  take `duration` (the default is `last_30_days`) or `start_date` with `end_date` as `YYYY-MM-DD`. Each tile\n"
    "  has `value` and `previous_value`, the figure for the period before it, and `change_percent`, which is `null`\n"
    "  when `previous_value` is `0`. A bad value, or one date without the other, is rejected with `400`.",
    "**The update sends the full list, and the tiles follow your order.** The response has the same fields as\n"
    "  [Get the KPI selection](" + SELECTION_PAGE + "), with the tiles in the order you sent and `position` from `1`.\n"
    "  A body with a field other than `metrics` is not an error: the other fields are ignored.",
]

PERIOD_PARAMS = [
    {"name": "duration", "in": "query", "description": "The period the figures cover: " + ", ".join("`%s`" % d for d in DURATIONS) + ". Defaults to `last_30_days`.", "schema": {"type": "string", "enum": DURATIONS, "example": "last_7_days"}},
    {"name": "start_date", "in": "query", "description": "The first day of a custom period, as `YYYY-MM-DD`. Send it with `end_date`; the response then has `duration` `custom`. A `start_date` without `end_date` is rejected with `400` and the detail code `required` on `end_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-01"}},
    {"name": "end_date", "in": "query", "description": "The last day of a custom period, as `YYYY-MM-DD`. Send it with `start_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-31"}},
]

ERROR_REF = {"$ref": "#/components/schemas/DashboardKpiError"}
PERIOD = {
    "duration": "last_30_days", "start_date": "2026-10-10", "end_date": "2026-11-09",
    "previous_start_date": "2026-09-10", "previous_end_date": "2026-10-10", "time_zone": "Africa/Abidjan", "currency": "USD",
}
DASHBOARD = {"id": "64934ef3-095c-4e15-8f8d-45acfa55a2ce", "name": "Default dashboard"}
TILES = [
    {"position": 1, "key": "total_sales", "code": "total_sales", "label": "Total Sales", "group": "ecommerce", "format": "money", "value": 2455.2, "previous_value": 27810.1, "change_percent": -91.2, "direction": "down"},
    {"position": 2, "key": "total_orders", "code": "total_orders", "label": "Total Orders", "group": "ecommerce", "format": "count", "value": 19.0, "previous_value": 247.0, "change_percent": -92.3, "direction": "down"},
    {"position": 3, "key": "aov", "code": "average_order_value", "label": "Average Order Value", "group": "ecommerce", "format": "money", "value": 129.2, "previous_value": 112.6, "change_percent": 14.7, "direction": "up"},
]
SELECTION = {"dashboard": DASHBOARD, "online_store": True, "period": PERIOD, "selected": TILES}

PERIOD_400 = "`duration` is not one of the values above, you sent `duration` twice, or you sent one of `start_date` and `end_date` without the other. The reason is `invalid_request`, and every failed field is listed in `details`."

ENDPOINTS = [
    {
        "key": "get_dashboard_kpi_options",
        "slug": "list-kpi-options",
        "title": "List KPI options",
        "method": "GET",
        "path": BASE + "/kpi_options",
        "summary": "Returns every metric a KPI tile can show, by group, and the keys now selected.",
        "description": "Returns the 27 metrics in five `groups`, each metric with its `key`, `code`, `label`, `format` (`money`, `count` or `percent`) and `in_use`. `selected` lists the keys of the tiles the default layout shows now, `min` and `max` give the number of tiles allowed, and `dashboard` names the layout. Read this before [Update the KPI selection](" + UPDATE_PAGE + ") to see the keys you can send.",
        "responses": {
            "200": {
                "description": "The groups with their metrics, the keys in use, and the tile limits.",
                "schema": {"$ref": "#/components/schemas/DashboardKpiOptions"},
                "example": {
                    "dashboard": DASHBOARD, "min": 2, "max": 5,
                    "selected": ["total_sales", "total_orders", "aov"],
                    "groups": [
                        {"key": "ecommerce", "label": "E-commerce", "metrics": [
                            {"key": "total_sales", "code": "total_sales", "label": "Total Sales", "format": "money", "in_use": True},
                            {"key": "total_orders", "code": "total_orders", "label": "Total Orders", "format": "count", "in_use": True},
                            {"key": "aov", "code": "average_order_value", "label": "Average Order Value", "format": "money", "in_use": True},
                            {"key": "conversion_rate", "code": "conversion_rate", "label": "Conversion Rate", "format": "percent", "in_use": False},
                        ]},
                        {"key": "content", "label": "Content", "metrics": [
                            {"key": "total_page_views", "code": "total_page_views", "label": "Total Page Views", "format": "count", "in_use": False},
                        ]},
                    ],
                },
            },
        },
        "example_call": {},
    },
    {
        "key": "get_dashboard_kpi_selection",
        "slug": "get-the-kpi-selection",
        "title": "Get the KPI selection",
        "method": "GET",
        "path": BASE + "/kpi_selection",
        "summary": "Returns the KPI tiles the dashboard shows, with their figures for a period.",
        "description": "Returns the default layout's KPI tiles in `selected`, in tile order, with each tile's `value`, `previous_value`, `change_percent` and `direction` (`up`, `down` or `flat`) for the period in `period`. The period is `last_30_days` unless you send `duration`, or `start_date` with `end_date`.",
        "parameters": PERIOD_PARAMS,
        "responses": {
            "200": {
                "description": "The layout, the period, and the tiles with their figures.",
                "schema": {"$ref": "#/components/schemas/DashboardKpiSelection"},
                "example": SELECTION,
            },
            "400": {"description": PERIOD_400, "schema": ERROR_REF},
        },
        "example_call": {"query": {"duration": "last_7_days"}},
    },
    {
        "key": "update_dashboard_kpi_selection",
        "slug": "update-the-kpi-selection",
        "title": "Update the KPI selection",
        "method": "PUT",
        "path": BASE + "/kpi_selection",
        "summary": "Sets the 2 to 5 KPI tiles the dashboard shows, for every admin, and returns them.",
        "description": "Send `metrics`, the full list of 2 to 5 distinct metric keys in tile order. The list replaces the tiles of the store's default layout, so every admin sees the change at once. Read the current `selected` keys from [List KPI options](" + OPTIONS_PAGE + ") first so you can send them back. `duration`, or `start_date` with `end_date`, sets the period of the figures in the response. Fields other than `metrics` are ignored.",
        "parameters": PERIOD_PARAMS,
        "body": {"schema": {"$ref": "#/components/schemas/DashboardKpiSelectionInput"}, "example": {"metrics": ["total_sales", "total_orders", "aov"]}},
        "responses": {
            "200": {
                "description": "The same fields as [Get the KPI selection](" + SELECTION_PAGE + "), with the tiles in the order you sent.",
                "schema": {"$ref": "#/components/schemas/DashboardKpiSelection"},
                "example": SELECTION,
            },
            "400": {"description": "`metrics` is missing (`required`, with the message `send \"metrics\": the full list of 2 to 5 KPI keys in tile order`), holds fewer than 2 or more than 5 keys (`invalid_count`), repeats a key (`duplicate_value`), holds an unknown key (`invalid_enum`) or is not a list (`invalid_type`). Or the period query is bad, as in [Get the KPI selection](" + SELECTION_PAGE + ").", "schema": ERROR_REF},
        },
        "example_call": {"query": {"duration": "last_7_days"}},
    },
]

PERIOD_SCHEMA = {"type": "object", "description": "The period the figures cover and the one before it.", "properties": {
    "duration": {"type": "string", "description": "The `duration` applied, or `custom` when you sent dates."},
    "start_date": {"type": "string", "description": "The first day of the period, as `YYYY-MM-DD`."},
    "end_date": {"type": "string", "description": "The last day of the period."},
    "previous_start_date": {"type": "string", "description": "The first day of the period before it, used for `previous_value`."},
    "previous_end_date": {"type": "string", "description": "The last day of the period before it."},
    "time_zone": {"type": "string", "description": "The time zone the days are counted in."},
    "currency": {"type": "string", "description": "The currency of `money` figures."},
}}

SCHEMAS = {
    "DashboardKpiLayout": {"type": "object", "description": "The dashboard layout the tiles belong to.", "properties": {
        "id": {"type": "string", "description": "The layout's `id`, a UUID."},
        "name": {"type": "string", "description": "The layout's name."},
    }},
    "DashboardKpiMetric": {"type": "object", "properties": {
        "key": {"type": "string", "description": "The metric's key. [Update the KPI selection](" + UPDATE_PAGE + ") takes it in `metrics`."},
        "code": {"type": "string", "description": "The metric's code. It differs from `key` for some metrics, such as `average_order_value` for `aov`."},
        "label": {"type": "string", "description": "The metric's name on the dashboard."},
        "format": {"type": "string", "enum": ["money", "count", "percent"], "description": "How the figure is shown."},
        "in_use": {"type": "boolean", "description": "`true` when a tile of the default layout shows the metric."},
    }},
    "DashboardKpiGroup": {"type": "object", "properties": {
        "key": {"type": "string", "enum": ["ecommerce", "content", "blog", "bookings", "courses"], "description": "The group's key."},
        "label": {"type": "string", "description": "The group's name."},
        "metrics": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardKpiMetric"}, "description": "The group's metrics."},
    }},
    "DashboardKpiOptions": {"type": "object", "properties": {
        "dashboard": {"$ref": "#/components/schemas/DashboardKpiLayout"},
        "min": {"type": "integer", "description": "The fewest tiles the dashboard shows: `2`."},
        "max": {"type": "integer", "description": "The most tiles the dashboard shows: `5`."},
        "selected": {"type": "array", "items": {"type": "string"}, "description": "The keys of the tiles in use, in tile order."},
        "groups": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardKpiGroup"}, "description": "`ecommerce` (12 metrics), `content` (2), `blog` (4), `bookings` (4) and `courses` (5)."},
    }},
    "DashboardKpiPeriod": PERIOD_SCHEMA,
    "DashboardKpiTile": {"type": "object", "properties": {
        "position": {"type": "integer", "description": "The tile's place, from `1`."},
        "key": {"type": "string", "description": "The metric's key."},
        "code": {"type": "string", "description": "The metric's code."},
        "label": {"type": "string", "description": "The tile's name."},
        "group": {"type": "string", "description": "The metric's group."},
        "format": {"type": "string", "enum": ["money", "count", "percent"], "description": "How the figure is shown."},
        "value": {"type": "number", "description": "The figure for the period. It is always a decimal, such as `19.0`."},
        "previous_value": {"type": "number", "description": "The figure for the period before it."},
        "change_percent": {"type": ["number", "null"], "description": "The change from `previous_value` to `value`, in percent. `null` when `previous_value` is `0`."},
        "direction": {"type": "string", "enum": ["up", "down", "flat"], "description": "Whether `value` rose, fell or stayed the same."},
    }},
    "DashboardKpiSelection": {"type": "object", "properties": {
        "dashboard": {"$ref": "#/components/schemas/DashboardKpiLayout"},
        "online_store": {"type": "boolean", "description": "Whether the store has an online store."},
        "period": {"$ref": "#/components/schemas/DashboardKpiPeriod"},
        "selected": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardKpiTile"}, "description": "The tiles in tile order, 2 to 5."},
    }},
    "DashboardKpiSelectionInput": {"type": "object", "required": ["metrics"], "properties": {
        "metrics": {"type": "array", "items": {"type": "string", "enum": KPI_KEYS}, "minItems": 2, "maxItems": 5, "description": "The full list of 2 to 5 distinct metric keys, in tile order. It replaces the tiles."},
    }},
    "DashboardKpiError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`."},
        "message": {"type": "string", "description": "What went wrong, such as `one or more fields are invalid`."},
        "details": {"type": "array", "description": "One entry per rejected field.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field, such as `metrics`, `duration` or `end_date`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `invalid_enum`, `invalid_count`, `duplicate_value` or `invalid_type`."},
            "message": {"type": "string", "description": "The rule that failed."},
            "value": {"type": "string", "description": "The value you sent, for a rejected query parameter."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
