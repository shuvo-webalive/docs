"""The Dashboard reports endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Dashboard reports"
SLUG = "dashboard-reports"
BASE = "/admin/dashboard/reports"
ICON = "chart-line"

DURATIONS = [
    "today", "yesterday", "last_24_hours", "last_7_days", "last_30_days", "this_month", "last_month", "last_3_months",
    "last_6_months", "last_12_months", "last_24_months", "last_36_months", "last_48_months", "last_60_months", "custom",
]
KPI_KEYS = [
    "total_sales", "total_orders", "aov", "net_sales", "conversion_rate", "cart_to_order", "cart_abandonment_rate",
    "refund_rate", "returning_customer_rate", "new_customers", "sessions", "pending_fulfillment", "total_page_views",
    "total_visitors", "blog_views", "blog_new_comments", "blog_published", "blog_pending_comments", "total_bookings",
    "booking_upcoming_today", "booking_revenue", "booking_active_services", "course_enrolments", "course_revenue",
    "course_orders", "course_unpaid", "course_active",
]

OVERVIEW_DESCRIPTION = "Read the store's quick report, sales report and summary for a period, or check that each one can be read without fetching the body."
INTRO = "The Dashboard reports API has six endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/dashboard/reports`."

QUICK_PAGE = "/api-reference/dashboard-reports/get-the-quick-report"
SALES_PAGE = "/api-reference/dashboard-reports/get-the-sales-report"
SUMMARY_PAGE = "/api-reference/dashboard-reports/get-the-summary-report"

WARNING = None

NOTES = [
    "**Every report takes the same period.** Send `duration`, or `start_date` with `end_date` as `YYYY-MM-DD`.\n"
    "  Without either, the period is `last_30_days`. `duration` is one of "
    + ", ".join("`%s`" % d for d in DURATIONS[:-1])
    + ", or `custom`, which the response uses when you send dates. `period` in every response shows the days covered, the\n"
    "  days before them that `previous_value` covers, the `time_zone` and the `currency`.",
    "**A bad value is rejected with `400`, and one response lists every field that failed.** A `duration` outside the\n"
    "  list, a `duration` sent twice, and a `start_date` without an `end_date` (or the reverse) are rejected with the reason\n"
    "  `invalid_request`. A query parameter a report does not know is ignored.",
    "**The reports are read-only, and each has a `HEAD` form.** The `HEAD` call returns `200` with no body and checks\n"
    "  the same query as the `GET`, so a bad value is rejected with `400`. Use it to check that a report can be read.",
    "**A period with no sales has no rows.** [Get the sales report](" + SALES_PAGE + ") returns `rows` as an empty\n"
    "  list and still returns `totals`. Lists such as `view_report.items` can be empty too.",
    "**Do not expect two reports to give the same total.** In the same call, `orders.count` and the `total_orders` tile\n"
    "  can differ, and the sales report covers only paid orders.",
]

PERIOD_PARAMS = [
    {"name": "duration", "in": "query", "description": "The period the report covers: " + ", ".join("`%s`" % d for d in DURATIONS) + ". Defaults to `last_30_days`.", "schema": {"type": "string", "enum": DURATIONS, "example": "last_12_months"}},
    {"name": "start_date", "in": "query", "description": "The first day of a custom period, as `YYYY-MM-DD`. Send it with `end_date`. The dates cannot be reversed or in the future. A `start_date` without `end_date` is rejected with `400` and the detail code `required` on `end_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-01"}},
    {"name": "end_date", "in": "query", "description": "The last day of a custom period, as `YYYY-MM-DD`. Send it with `start_date`.", "schema": {"type": "string", "format": "date", "example": "2026-05-31"}},
]
KPIS_PARAM = {"name": "kpis", "in": "query", "description": "A comma-separated list of metric keys that narrows `kpis` to those metrics, in the order you list them, such as `total_sales,aov`. A key that is not one of the 27 keys is rejected with `400` and the detail code `invalid_enum`, which lists them.", "schema": {"type": "string", "example": "total_sales,aov"}}
ENTITY_PARAM = {"name": "entity_name", "in": "query", "description": "What `view_report` ranks: `page` or `product`. Defaults to `page`. Any other value is rejected with `400` and the message `must be page or product`.", "schema": {"type": "string", "enum": ["page", "product"], "example": "product"}}
BREAKDOWN_PARAM = {"name": "breakdown", "in": "query", "description": "Send `true` to add `orders`, `orders_value`, `gross_sales`, `shipping`, `handling`, `tax`, `discount`, `refunds`, `average_order_value` and, on rows, `top_product` to each row and to `totals`. `false` is the default. Any other value is rejected with `400` and the detail code `invalid_boolean`.", "schema": {"type": "boolean", "example": True}}
SORT_PARAM = {"name": "sort", "in": "query", "description": "What the rows are sorted by: `date` or `sales`. Defaults to `date`. Any other value is rejected with `400` and the detail code `invalid_enum`.", "schema": {"type": "string", "enum": ["date", "sales"], "example": "sales"}}
ORDER_PARAM = {"name": "order", "in": "query", "description": "The sort direction: `asc` or `desc`. Defaults to `asc`. Any other value is rejected with `400` and the detail code `invalid_enum`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "desc"}}
COMPARE_PARAM = {"name": "compare_previous", "in": "query", "description": "`true` or `false`. Any other value is rejected with `400` and the detail code `invalid_boolean`. The response has the same fields either way.", "schema": {"type": "boolean", "example": True}}

ERROR_REF = {"$ref": "#/components/schemas/DashboardReportError"}
PERIOD = {
    "duration": "last_12_months", "start_date": "2025-11-09", "end_date": "2026-11-09",
    "previous_start_date": "2024-11-09", "previous_end_date": "2025-11-09", "time_zone": "Africa/Abidjan", "currency": "USD",
}
PERIOD_400 = "A period value is bad: `duration` is not one of the values above or is sent twice, or only one of `start_date` and `end_date` is sent. The reason is `invalid_request`, and every failed field is listed in `details`."
HEAD_200 = {"description": "Headers only, no body."}

KPI_TILE = {"key": "total_sales", "code": "total_sales", "label": "Total Sales", "group": "ecommerce", "format": "money", "value": 5281.89, "previous_value": 4100.0, "change_percent": 28.8, "direction": "up"}
TREND = {"key": "order_count", "code": "order_count", "label": "Orders", "format": "count", "value": 3.0, "previous_value": 2.0, "change_percent": 50.0, "direction": "up"}
ORDERS = {"count": 3, "pending": 1, "cancelled": 0}
SALES = {"subtotal": 6289.18, "total": 5281.89, "items_sold": 7, "average_order_value": 1760.63}
GROUPS = {
    "orders": ORDERS, "sales": SALES, "customers": {"new": 4}, "products": {"new": 2, "out_of_stock": 1},
    "page_views": {"total": 120, "unique": 80},
    "view_report": {"entity": "page", "items": [{"page": {"id": 43, "name": "Home"}, "views": 19}]},
}
QUICK_EXAMPLE = dict({"period": PERIOD, "kpis": [KPI_TILE]}, **GROUPS, trends=[TREND])

SALES_ROW = {"date": "2026-05", "year": 2026, "month": 5, "label": "May 2026", "month_name": "May 2026", "sales": 5281.89, "total_sales": 5281.89}
SALES_ROW_BREAKDOWN = dict(SALES_ROW, orders=3, orders_value=5281.89, gross_sales=6289.18, shipping=200.0, handling=20.0, tax=787.29,
                           discount=10.0, refunds=0.0, average_order_value=1760.63, top_product={"id": 427, "name": "Gift card"})
SALES_EXAMPLE = {"period": PERIOD, "group_by": "month", "sort": "date", "order": "asc", "rows": [SALES_ROW], "totals": {"sales": 5281.89}}

SUMMARY_EXAMPLE = {
    "period": PERIOD,
    "quick_report": GROUPS,
    "order_by_month": [{"date": "2026-05", "year": 2026, "month": 5, "count": 3}],
    "orders_over_time": [{"date": "2026-05", "year": 2026, "month": 5, "count": 3}],
    "sales_report": [SALES_ROW],
    "most_visited_products": [{"product": {"id": 427, "name": "Gift card"}, "views": 40}],
    "best_selling_products": [{"product": {"id": 427, "name": "Gift card"}, "units_sold": 5}],
    "order_updates": {"low_stock_items": 2, "pending_fulfillment": 1, "payments_to_capture": 0},
}

ENDPOINTS = [
    {
        "key": "get_dashboard_report_quick",
        "slug": "get-the-quick-report",
        "title": "Get the quick report",
        "method": "GET",
        "path": BASE + "/quick",
        "summary": "Returns the dashboard's KPI figures, order and sales totals, and most viewed items for a period.",
        "description": "Returns `kpis` (the 27 metrics, or only the ones you list in `kpis`), `orders`, `sales`, `customers`, `products`, `page_views`, `view_report` and 12 `trends`, for the period you send. `view_report` ranks the most viewed pages, or products when you send `entity_name` `product`. The period is `last_30_days` unless you send `duration`, or `start_date` with `end_date`.",
        "parameters": PERIOD_PARAMS + [KPIS_PARAM, ENTITY_PARAM],
        "responses": {
            "200": {
                "description": "The period and the report's groups of figures.",
                "schema": {"$ref": "#/components/schemas/DashboardReportQuick"},
                "example": QUICK_EXAMPLE,
            },
            "400": {"description": PERIOD_400 + " Or `kpis` holds a key that is not a metric key (`invalid_enum`), or `entity_name` is not `page` or `product`.", "schema": ERROR_REF},
        },
        "example_call": {"query": {"duration": "last_12_months", "kpis": "total_sales,aov", "entity_name": "product"}},
    },
    {
        "key": "head_dashboard_report_quick",
        "slug": "check-the-quick-report",
        "title": "Check the quick report",
        "method": "HEAD",
        "path": BASE + "/quick",
        "summary": "Returns `200` and the headers of the quick report, with no body.",
        "description": "Returns `200` with headers only and no body, after checking the same query as [Get the quick report](" + QUICK_PAGE + "). A bad value in the query is rejected with `400`.",
        "parameters": PERIOD_PARAMS + [KPIS_PARAM, ENTITY_PARAM],
        "responses": {
            "200": HEAD_200,
            "400": {"description": "A value in the query is bad, as in [Get the quick report](" + QUICK_PAGE + ")."},
        },
        "example_call": {"query": {"duration": "last_12_months"}},
    },
    {
        "key": "get_dashboard_report_sales",
        "slug": "get-the-sales-report",
        "title": "Get the sales report",
        "method": "GET",
        "path": BASE + "/sales",
        "summary": "Returns sales by day or month for a period, with totals.",
        "description": "Returns `rows`, one for each day or month in the period that has sales, and `totals`. `group_by` in the response is `day` for a period of about a month or less and `month` for a longer one. Add `breakdown=true` to get orders, shipping, tax, discounts, refunds and the top product on each row and in the totals. Sort with `sort` and `order`. A period with no sales returns `rows` as an empty list.",
        "parameters": PERIOD_PARAMS + [BREAKDOWN_PARAM, SORT_PARAM, ORDER_PARAM],
        "responses": {
            "200": {
                "description": "The period, how the rows are grouped and sorted, the rows and the totals.",
                "schema": {"$ref": "#/components/schemas/DashboardReportSales"},
                "example": SALES_EXAMPLE,
            },
            "400": {"description": PERIOD_400 + " Or `sort` or `order` is not one of its values (`invalid_enum`), or `breakdown` is not `true` or `false` (`invalid_boolean`).", "schema": ERROR_REF},
        },
        "example_call": {"query": {"duration": "last_12_months", "breakdown": "true", "sort": "sales", "order": "desc"}},
    },
    {
        "key": "head_dashboard_report_sales",
        "slug": "check-the-sales-report",
        "title": "Check the sales report",
        "method": "HEAD",
        "path": BASE + "/sales",
        "summary": "Returns `200` and the headers of the sales report, with no body.",
        "description": "Returns `200` with headers only and no body, after checking the same query as [Get the sales report](" + SALES_PAGE + "). A bad value in the query is rejected with `400`.",
        "parameters": PERIOD_PARAMS + [BREAKDOWN_PARAM, SORT_PARAM, ORDER_PARAM],
        "responses": {
            "200": HEAD_200,
            "400": {"description": "A value in the query is bad, as in [Get the sales report](" + SALES_PAGE + ")."},
        },
        "example_call": {"query": {"duration": "last_12_months"}},
    },
    {
        "key": "get_dashboard_report_summary",
        "slug": "get-the-summary-report",
        "title": "Get the summary report",
        "method": "GET",
        "path": BASE + "/summary",
        "summary": "Returns the quick report's totals, orders by month, sales rows, top products and order updates in one call.",
        "description": "Returns `quick_report` (the quick report without `kpis` and `trends`), `order_by_month`, `orders_over_time`, `sales_report` (the rows of the sales report), `most_visited_products`, `best_selling_products` with the highest `units_sold` first, and `order_updates`, for the period you send.",
        "parameters": PERIOD_PARAMS + [COMPARE_PARAM],
        "responses": {
            "200": {
                "description": "The period and the summary's lists and figures.",
                "schema": {"$ref": "#/components/schemas/DashboardReportSummary"},
                "example": SUMMARY_EXAMPLE,
            },
            "400": {"description": PERIOD_400 + " Or `compare_previous` is not `true` or `false` (`invalid_boolean`).", "schema": ERROR_REF},
        },
        "example_call": {"query": {"duration": "last_12_months"}},
    },
    {
        "key": "head_dashboard_report_summary",
        "slug": "check-the-summary-report",
        "title": "Check the summary report",
        "method": "HEAD",
        "path": BASE + "/summary",
        "summary": "Returns `200` and the headers of the summary report, with no body.",
        "description": "Returns `200` with headers only and no body, after checking the same query as [Get the summary report](" + SUMMARY_PAGE + "). A bad value in the query is rejected with `400`.",
        "parameters": PERIOD_PARAMS + [COMPARE_PARAM],
        "responses": {
            "200": HEAD_200,
            "400": {"description": "A value in the query is bad, as in [Get the summary report](" + SUMMARY_PAGE + ")."},
        },
        "example_call": {"query": {"duration": "last_12_months"}},
    },
]


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def number(description):
    return {"type": "number", "description": description}


def whole(description):
    return {"type": "integer", "description": description}


ENTITY = {"type": "object", "description": "A page or product, with its `id` and name.", "properties": {
    "id": whole("The page's or product's `id`."),
    "name": {"type": "string", "description": "Its name."},
}}

SCHEMAS = {
    "DashboardReportPeriod": {"type": "object", "description": "The period the report covers and the one before it.", "properties": {
        "duration": {"type": "string", "description": "The `duration` applied, or `custom` when you sent dates."},
        "start_date": {"type": "string", "description": "The first day of the period, as `YYYY-MM-DD`."},
        "end_date": {"type": "string", "description": "The last day of the period."},
        "previous_start_date": {"type": "string", "description": "The first day of the period before it, used for `previous_value`."},
        "previous_end_date": {"type": "string", "description": "The last day of the period before it."},
        "time_zone": {"type": "string", "description": "The time zone the days are counted in."},
        "currency": {"type": "string", "description": "The currency of money figures."},
    }},
    "DashboardReportEntity": ENTITY,
    "DashboardReportKpi": {"type": "object", "description": "One metric's figure. In `trends`, `key` is the metric's code and there is no `group`.", "properties": {
        "key": {"type": "string", "description": "The metric's key."},
        "code": {"type": "string", "description": "The metric's code."},
        "label": {"type": "string", "description": "The metric's name."},
        "group": {"type": "string", "description": "The metric's group, such as `ecommerce`. Not in `trends`."},
        "format": {"type": "string", "enum": ["money", "count", "percent"], "description": "How the figure is shown."},
        "value": number("The figure for the period. It is always a decimal."),
        "previous_value": number("The figure for the period before it."),
        "change_percent": {"type": ["number", "null"], "description": "The change in percent. `null` when `previous_value` is `0`."},
        "direction": {"type": "string", "enum": ["up", "down", "flat"], "description": "Whether `value` rose, fell or stayed the same."},
    }},
    "DashboardReportViewItem": {"type": "object", "description": "One most viewed page or product. A page has `page`, a product has `product`.", "properties": {
        "page": ref("DashboardReportEntity"),
        "product": ref("DashboardReportEntity"),
        "views": whole("The number of views in the period."),
    }},
    "DashboardReportGroups": {"type": "object", "properties": {
        "orders": {"type": "object", "properties": {
            "count": whole("The number of orders in the period."),
            "pending": whole("The number of pending orders."),
            "cancelled": whole("The number of cancelled orders."),
        }},
        "sales": {"type": "object", "properties": {
            "subtotal": number("The subtotal of the sales."),
            "total": number("The total of the sales."),
            "items_sold": whole("The number of items sold."),
            "average_order_value": number("The average value of an order."),
        }},
        "customers": {"type": "object", "properties": {"new": whole("The number of new customers.")}},
        "products": {"type": "object", "properties": {
            "new": whole("The number of new products."),
            "out_of_stock": whole("The number of products out of stock."),
        }},
        "page_views": {"type": "object", "properties": {
            "total": whole("The number of page views."),
            "unique": whole("The number of unique page views."),
        }},
        "view_report": {"type": "object", "properties": {
            "entity": {"type": "string", "enum": ["page", "product"], "description": "What `items` ranks."},
            "items": {"type": "array", "items": ref("DashboardReportViewItem"), "description": "The most viewed pages or products. Can be empty."},
        }},
    }},
    "DashboardReportQuick": {"type": "object", "properties": {
        "period": ref("DashboardReportPeriod"),
        "kpis": {"type": "array", "items": ref("DashboardReportKpi"), "description": "The 27 metrics, or the ones you list in `kpis`, in the order you list them."},
        "orders": {"type": "object", "properties": {"count": whole("The number of orders in the period."), "pending": whole("The number of pending orders."), "cancelled": whole("The number of cancelled orders.")}},
        "sales": {"type": "object", "properties": {"subtotal": number("The subtotal of the sales."), "total": number("The total of the sales."), "items_sold": whole("The number of items sold."), "average_order_value": number("The average value of an order.")}},
        "customers": {"type": "object", "properties": {"new": whole("The number of new customers.")}},
        "products": {"type": "object", "properties": {"new": whole("The number of new products."), "out_of_stock": whole("The number of products out of stock.")}},
        "page_views": {"type": "object", "properties": {"total": whole("The number of page views."), "unique": whole("The number of unique page views.")}},
        "view_report": {"type": "object", "properties": {"entity": {"type": "string", "enum": ["page", "product"], "description": "What `items` ranks."}, "items": {"type": "array", "items": ref("DashboardReportViewItem"), "description": "The most viewed pages or products. Can be empty."}}},
        "trends": {"type": "array", "items": ref("DashboardReportKpi"), "description": "12 figures: `order_count`, `total_customers`, `sales`, `gross_sales`, `total_item_sold`, `average_order_value`, `cancelled_order`, `pending_order`, `new_product`, `out_of_stock_product`, `total_page_view` and `unique_page_view`."},
    }},
    "DashboardReportSalesRow": {"type": "object", "description": "One day or month. The fields after `total_sales` are there only with `breakdown=true`.", "properties": {
        "date": {"type": "string", "description": "`YYYY-MM` for a month, or `YYYY-MM-DD` for a day."},
        "year": whole("The year."),
        "month": whole("The month, from `1` to `12`."),
        "day": whole("The day. Only on day rows."),
        "label": {"type": "string", "description": "The row's name, such as `May 2026`."},
        "month_name": {"type": "string", "description": "The month's name and year."},
        "sales": number("The sales of the day or month."),
        "total_sales": number("The sales of the day or month."),
        "orders": whole("The number of orders."),
        "orders_value": number("The value of the orders."),
        "gross_sales": number("The gross sales."),
        "shipping": number("The shipping charged."),
        "handling": number("The handling charged."),
        "tax": number("The tax charged."),
        "discount": number("The discounts given."),
        "refunds": number("The refunds paid."),
        "average_order_value": number("The average value of an order."),
        "top_product": ref("DashboardReportEntity"),
    }},
    "DashboardReportSales": {"type": "object", "properties": {
        "period": ref("DashboardReportPeriod"),
        "group_by": {"type": "string", "enum": ["day", "month"], "description": "`day` for a period of about a month or less, otherwise `month`. It does not depend on `breakdown`."},
        "sort": {"type": "string", "enum": ["date", "sales"], "description": "The sort applied."},
        "order": {"type": "string", "enum": ["asc", "desc"], "description": "The direction applied."},
        "rows": {"type": "array", "items": ref("DashboardReportSalesRow"), "description": "One row for each day or month with sales. Empty when the period has no sales."},
        "totals": {"type": "object", "description": "The totals for the period: `sales`, and with `breakdown=true` also `orders`, `orders_value`, `gross_sales`, `shipping`, `handling`, `tax`, `discount`, `refunds` and `average_order_value`.", "properties": {
            "sales": number("The sales of the period."),
            "orders": whole("The number of orders."),
            "orders_value": number("The value of the orders."),
            "gross_sales": number("The gross sales."),
            "shipping": number("The shipping charged."),
            "handling": number("The handling charged."),
            "tax": number("The tax charged."),
            "discount": number("The discounts given."),
            "refunds": number("The refunds paid."),
            "average_order_value": number("The average value of an order."),
        }},
    }},
    "DashboardReportOrderCount": {"type": "object", "properties": {
        "date": {"type": "string", "description": "The month, as `YYYY-MM`."},
        "year": whole("The year."),
        "month": whole("The month, from `1` to `12`."),
        "count": whole("The number of orders."),
    }},
    "DashboardReportSummary": {"type": "object", "properties": {
        "period": ref("DashboardReportPeriod"),
        "quick_report": dict(ref("DashboardReportGroups"), description="`orders`, `sales`, `customers`, `products`, `page_views` and `view_report`, as in the quick report. It has no `kpis` and no `trends`."),
        "order_by_month": {"type": "array", "items": ref("DashboardReportOrderCount"), "description": "The number of orders in each month."},
        "orders_over_time": {"type": "array", "items": ref("DashboardReportOrderCount"), "description": "The number of orders over the period."},
        "sales_report": {"type": "array", "items": ref("DashboardReportSalesRow"), "description": "The rows of the sales report."},
        "most_visited_products": {"type": "array", "items": {"type": "object", "properties": {"product": ref("DashboardReportEntity"), "views": whole("The number of views.")}}},
        "best_selling_products": {"type": "array", "items": {"type": "object", "properties": {"product": ref("DashboardReportEntity"), "units_sold": whole("The number of units sold.")}}, "description": "The highest `units_sold` first."},
        "order_updates": {"type": "object", "properties": {
            "low_stock_items": whole("The number of items low in stock."),
            "pending_fulfillment": whole("The number of orders waiting to be fulfilled."),
            "payments_to_capture": whole("The number of payments waiting to be captured."),
        }},
    }},
    "DashboardReportError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`."},
        "message": {"type": "string", "description": "What went wrong, such as `one or more fields are invalid`."},
        "details": {"type": "array", "description": "One entry per rejected query parameter.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The query parameter, such as `duration` or `end_date`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `invalid_enum`, `invalid_boolean` or `required`."},
            "message": {"type": "string", "description": "The rule that failed, such as `must be page or product`."},
            "value": {"type": "string", "description": "The value you sent."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
