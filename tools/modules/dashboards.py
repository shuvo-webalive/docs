"""The Dashboards endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Dashboards"
SLUG = "dashboards"
BASE = "/admin/dashboards"
ICON = "table-columns"

OVERVIEW_DESCRIPTION = "List, create, retrieve, update and delete the dashboard layouts that choose which sections the store's admin dashboard shows, in what order, and which KPI tiles it starts with."
INTRO = "The Dashboards API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/dashboards`."

LIST_PAGE = "/api-reference/dashboards/list-dashboard-layouts"
CREATE_PAGE = "/api-reference/dashboards/create-a-dashboard-layout"
GET_PAGE = "/api-reference/dashboards/retrieve-a-dashboard-layout"
PATCH_PAGE = "/api-reference/dashboards/update-a-dashboard-layout"
DELETE_PAGE = "/api-reference/dashboards/delete-a-dashboard-layout"

WARNING = (
    "**Creating a layout changes the store, and making a layout the default changes the dashboard for every admin.**\n"
    "  A layout you create is saved to the store and stays there until you delete it with\n"
    "  [Delete a dashboard layout](" + DELETE_PAGE + "). Sending `\"default\": true` moves the store's default\n"
    "  layout to the layout you name, and every admin then sees that layout. Before you do, note which row of\n"
    "  [List dashboard layouts](" + LIST_PAGE + ") has `default` `true`, so you can set it back."
)

NOTES = [
    "**Send the fields of every write as they are, with no wrapper.** Create and update take the layout's fields at\n"
    "  the top level of the body, such as `{\"name\": \"Weekly\"}`. Responses return the layout the same way, with no\n"
    "  wrapper. A body with no fields is rejected with `400`, and a field the layout does not have is ignored.",
    "**Pass the layout's `id` as `dashboard_id`.** The `id` is a UUID, and you read it from\n"
    "  [List dashboard layouts](" + LIST_PAGE + ") or from the response to creating the layout. An `id` that\n"
    "  matches no layout is rejected with `404`, the reason `not_found`, and the detail on the field `dashboard_id`.",
    "**A new layout is a copy of the default layout.** [Create a dashboard layout](" + CREATE_PAGE + ") copies the\n"
    "  default layout's sections and its KPI tiles, or the layout whose `id` you send as `copy_from`. The\n"
    "  `customisable_sections` and `kpis` you send are then applied on top of the copy. A new layout is never the\n"
    "  default unless you send `default` `true`.",
    "**An update changes only what you send, and sections are matched by `key`.** Send `standard_sections`,\n"
    "  `customisable_sections` or `kpis` with just the entries to change. A section you leave out keeps its\n"
    "  `visible` value and its `position`. The four standard sections (`announcement`, `performance`, `activity`\n"
    "  and `contact`) take only `visible`, and `contact` cannot be hidden. The customisable sections\n"
    "  (`setup_guide`, `section_tabs` and `seo`) also take a `position`. Send the tabs of `section_tabs` as `tabs`\n"
    "  and the parts of `seo` as `parts`, each with its `key`.",
    "**`kpis` is the full list of the layout's KPI tiles, as 2 to 5 distinct keys in tile order.** The keys are\n"
    "  the metric keys that the KPI options list, such as `total_sales` or `aov`. Sending `kpis` replaces the\n"
    "  tiles the layout has, and `position` in the response counts from `1`.",
    "**A layout name is unique and at most 60 characters.** A `name` that another layout already has is rejected\n"
    "  with `409`, the reason `conflict` and the detail code `name_taken`. A blank `name` or one longer than 60\n"
    "  characters is rejected with `400`.",
]

DASHBOARD_ID = {
    "name": "dashboard_id",
    "in": "path",
    "required": True,
    "description": "The layout's `id`, a UUID, from [List dashboard layouts](" + LIST_PAGE + ") or from the response to creating the layout.",
    "schema": {"type": "string", "example": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01"},
}

ERROR_REF = {"$ref": "#/components/schemas/DashboardLayoutError"}
LAYOUT_REF = {"$ref": "#/components/schemas/DashboardLayout"}

STANDARD_SECTIONS = [
    {"key": "announcement", "title": "Announcement Banner", "description": "New features and product news", "visible": True, "can_hide": True},
    {"key": "performance", "title": "Performance Overview", "description": "Key metrics for the selected date range", "visible": True, "can_hide": True},
    {"key": "activity", "title": "Recent Activity Feed", "description": "Latest orders, sign-ups and site changes", "visible": True, "can_hide": True},
    {"key": "contact", "title": "Contact Information", "description": "How to reach support", "visible": True, "can_hide": False},
]
TABS = [
    {"key": "ecommerce", "title": "E-commerce", "description": "Order updates and best-selling products", "visible": True, "can_hide": True, "position": 1},
    {"key": "content", "title": "Content", "description": "Content to review and your most visited pages", "visible": True, "can_hide": True, "position": 2},
    {"key": "bookings", "title": "Bookings", "description": "Appointments today, payments to collect and your upcoming schedule", "visible": True, "can_hide": True, "position": 3},
    {"key": "courses", "title": "Courses", "description": "New enrolments, unpaid course orders and your popular courses", "visible": True, "can_hide": True, "position": 4},
    {"key": "blog", "title": "Blog", "description": "Comments, drafts and your most viewed posts", "visible": True, "can_hide": True, "position": 5},
]
PARTS = [
    {"key": "kpis", "title": "KPIs", "visible": True, "can_hide": False},
    {"key": "records", "title": "Records by result", "visible": False, "can_hide": True},
    {"key": "types", "title": "Score by record type", "visible": False, "can_hide": True},
    {"key": "todo", "title": "To do", "visible": False, "can_hide": True},
    {"key": "store_checks", "title": "Store-wide checks", "visible": False, "can_hide": True},
]
CUSTOMISABLE_SECTIONS = [
    {"key": "setup_guide", "title": "Setup Guide", "description": "Steps to finish setting up your site", "visible": False, "can_hide": True, "position": 1},
    {"key": "section_tabs", "title": "Section tabs", "visible": True, "can_hide": True, "position": 2, "tabs": TABS},
    {"key": "seo", "title": "SEO & AI Health", "description": "SEO score and AI readiness of your store", "visible": True, "can_hide": True, "position": 3, "parts": PARTS},
]
KPIS = [
    {"position": 1, "key": "total_sales", "label": "Total Sales", "group": "ecommerce"},
    {"position": 2, "key": "total_orders", "label": "Total Orders", "group": "ecommerce"},
    {"position": 3, "key": "aov", "label": "Average Order Value", "group": "ecommerce"},
]


def layout(**fields):
    row = {
        "id": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01", "name": "Weekly", "default": False,
        "standard_sections": STANDARD_SECTIONS, "customisable_sections": CUSTOMISABLE_SECTIONS, "kpis": KPIS,
        "created_at": "2026-11-05T07:12:40Z", "updated_at": "2026-11-05T07:12:40Z",
    }
    row.update(fields)
    return row


HIDDEN_ANNOUNCEMENT = [dict(STANDARD_SECTIONS[0], visible=False)] + STANDARD_SECTIONS[1:]

LISTING = {"dashboards": [
    {"id": "64934ef3-095c-4e15-8f8d-45acfa55a2ce", "name": "Default dashboard", "default": True,
     "created_at": "2026-10-12T04:00:45Z", "updated_at": "2026-11-05T07:26:25Z"},
    {"id": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01", "name": "Weekly", "default": False,
     "created_at": "2026-11-05T07:12:40Z", "updated_at": "2026-11-05T07:12:40Z"},
]}

CREATE_BODY = {"name": "Weekly", "kpis": ["total_sales", "total_orders", "aov"]}
PATCH_BODY = {"standard_sections": [{"key": "announcement", "visible": False}]}

NOT_FOUND_404 = (
    "No layout has that `dashboard_id`. The reason is `not_found`, the message is `dashboard not found`, and the "
    "detail is on the field `dashboard_id`."
)

ENDPOINTS = [
    {
        "key": "list_dashboards",
        "slug": "list-dashboard-layouts",
        "title": "List dashboard layouts",
        "method": "GET",
        "path": BASE,
        "summary": "Returns every dashboard layout with its `id`, `name` and whether it is the default.",
        "description": "Returns all the store's dashboard layouts under `dashboards`, in one call with no paging. Each row has `id`, `name`, `default`, `created_at` and `updated_at`, and exactly one row has `default` `true`. The rows do not include sections or KPI tiles: pass a row's `id` as `dashboard_id` to [Retrieve a dashboard layout](" + GET_PAGE + ") to read them. Query parameters you add are ignored.",
        "responses": {
            "200": {
                "description": "The layouts under `dashboards`.",
                "schema": {"$ref": "#/components/schemas/DashboardLayoutList"},
                "example": LISTING,
            },
        },
        "example_call": {},
    },
    {
        "key": "create_dashboard",
        "slug": "create-a-dashboard-layout",
        "title": "Create a dashboard layout",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a layout as a copy of the default layout and returns it with its `id`.",
        "description": "Send `name`, which is required. The new layout copies the default layout's sections and KPI tiles, or the layout whose `id` you send as `copy_from`. The `customisable_sections` and `kpis` you send are applied on top of the copy. The layout is not the default unless you send `default` `true`, which changes the dashboard for every admin. The response is the whole layout, and it has no `Location` header.",
        "body": {"schema": {"$ref": "#/components/schemas/DashboardLayoutInput"}, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new layout, with its `id`, which the other calls take as `dashboard_id`.",
                "schema": LAYOUT_REF,
                "example": layout(),
            },
            "400": {"description": "The body has no fields (the message is `request body is empty`), or a field breaks a rule: `name` is blank (`required`) or longer than 60 characters (`too_long`), a section `key` is unknown (`invalid_enum`), a standard section has a `position` (`not_supported`), `contact` is hidden (`not_hideable`), or `kpis` does not hold 2 to 5 keys (`invalid_count`).", "schema": ERROR_REF},
            "409": {"description": "Another layout already has that `name`. The reason is `conflict` and the detail code is `name_taken`, on the field `name`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_dashboard",
        "slug": "retrieve-a-dashboard-layout",
        "title": "Retrieve a dashboard layout",
        "method": "GET",
        "path": BASE + "/{dashboard_id}",
        "summary": "Returns the layout whose `id` you pass as `dashboard_id`, with its sections and KPI tiles.",
        "description": "Returns one layout: its `standard_sections` (`announcement`, `performance`, `activity` and `contact`), its `customisable_sections` (`setup_guide`, `section_tabs` with its five `tabs`, and `seo` with its `parts`) and its `kpis`. Each section says whether it is `visible` and whether it `can_hide`. Each customisable section has a `position`.",
        "parameters": [DASHBOARD_ID],
        "responses": {
            "200": {
                "description": "The whole layout.",
                "schema": LAYOUT_REF,
                "example": layout(),
            },
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"dashboard_id": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01"}},
    },
    {
        "key": "patch_dashboard",
        "slug": "update-a-dashboard-layout",
        "title": "Update a dashboard layout",
        "method": "PATCH",
        "path": BASE + "/{dashboard_id}",
        "summary": "Changes only the fields you send and returns the whole layout.",
        "description": "Send only what changes. Sections are matched by `key`, so `standard_sections` with `{\"key\": \"announcement\", \"visible\": false}` hides that section and leaves every other section as it is. A `position` on a customisable section or on a tab reorders the others to fit. `kpis` replaces the layout's KPI tiles. `default` `true` makes this layout the default for every admin. Sending `default` `false` for a layout that is not the default returns `200` and changes nothing.",
        "parameters": [DASHBOARD_ID],
        "body": {"schema": {"$ref": "#/components/schemas/DashboardLayoutInput"}, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The whole layout after the change.",
                "schema": LAYOUT_REF,
                "example": layout(standard_sections=HIDDEN_ANNOUNCEMENT, updated_at="2026-11-05T07:20:02Z"),
            },
            "400": {"description": "The body has no fields (the message is `request body is empty`), or a field breaks a rule: `name` is blank or longer than 60 characters, a section `key` is unknown (`invalid_enum`), a standard section has a `position` (`not_supported`), `contact` is hidden (`not_hideable`), or `kpis` does not hold 2 to 5 keys (`invalid_count`).", "schema": ERROR_REF},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
            "409": {"description": "Another layout already has that `name` (`name_taken`), or you sent `default` `false` for the default layout (`default_required`). Make another layout the default instead.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"dashboard_id": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01"}},
    },
    {
        "key": "delete_dashboard",
        "slug": "delete-a-dashboard-layout",
        "title": "Delete a dashboard layout",
        "method": "DELETE",
        "path": BASE + "/{dashboard_id}",
        "summary": "Deletes the layout whose `id` you pass as `dashboard_id` and returns no body.",
        "description": "Deletes the layout. The layout is then missing from [List dashboard layouts](" + LIST_PAGE + ").",
        "parameters": [DASHBOARD_ID],
        "responses": {
            "204": {"description": "The layout is deleted. The response has no body."},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"dashboard_id": "3f2b8c1e-7a4d-4e29-9b1a-5c6d7e8f9a01"}},
    },
]

STANDARD_INPUT = {"type": "object", "required": ["key"], "description": "One standard section. Send its `key` and what changes.", "properties": {
    "key": {"type": "string", "enum": ["announcement", "performance", "activity", "contact"], "description": "The section to change."},
    "visible": {"type": "boolean", "description": "Whether the dashboard shows the section. `contact` cannot be hidden."},
}}

SCHEMAS = {
    "DashboardLayoutPart": {"type": "object", "description": "One part of the `seo` section.", "properties": {
        "key": {"type": "string", "description": "`kpis`, `records`, `types`, `todo` or `store_checks`."},
        "title": {"type": "string", "description": "The part's name on the dashboard."},
        "visible": {"type": "boolean", "description": "Whether the dashboard shows the part."},
        "can_hide": {"type": "boolean", "description": "`false` when the part cannot be hidden."},
    }},
    "DashboardLayoutTab": {"type": "object", "description": "One tab of the `section_tabs` section.", "properties": {
        "key": {"type": "string", "description": "`ecommerce`, `content`, `bookings`, `courses` or `blog`."},
        "title": {"type": "string", "description": "The tab's name on the dashboard."},
        "description": {"type": "string", "description": "What the tab shows."},
        "visible": {"type": "boolean", "description": "Whether the dashboard shows the tab."},
        "can_hide": {"type": "boolean", "description": "`false` when the tab cannot be hidden."},
        "position": {"type": "integer", "description": "The tab's place among the tabs, from `1`."},
    }},
    "DashboardLayoutSection": {"type": "object", "description": "One section of the layout. Standard sections have no `position`.", "properties": {
        "key": {"type": "string", "description": "The section's key, such as `announcement`, `setup_guide`, `section_tabs` or `seo`."},
        "title": {"type": "string", "description": "The section's name on the dashboard."},
        "description": {"type": "string", "description": "What the section shows. `section_tabs` has none."},
        "visible": {"type": "boolean", "description": "Whether the dashboard shows the section."},
        "can_hide": {"type": "boolean", "description": "`false` when the section cannot be hidden. `contact` cannot."},
        "position": {"type": "integer", "description": "The section's place among the customisable sections, from `1`. Only customisable sections have it."},
        "tabs": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutTab"}, "description": "Only on `section_tabs`."},
        "parts": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutPart"}, "description": "Only on `seo`."},
    }},
    "DashboardLayoutKpi": {"type": "object", "description": "One KPI tile of the layout.", "properties": {
        "position": {"type": "integer", "description": "The tile's place, from `1`."},
        "key": {"type": "string", "description": "The metric key, such as `total_sales`."},
        "label": {"type": "string", "description": "The tile's name on the dashboard."},
        "group": {"type": "string", "description": "The metric's group, such as `ecommerce`."},
    }},
    "DashboardLayout": {"type": "object", "properties": {
        "id": {"type": "string", "description": "The layout's `id`, a UUID. Pass it as `dashboard_id` in the path of the other calls."},
        "name": {"type": "string", "description": "The layout's name, unique across layouts, up to 60 characters."},
        "default": {"type": "boolean", "description": "`true` for the store's default layout, which every admin sees."},
        "standard_sections": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutSection"}, "description": "`announcement`, `performance`, `activity` and `contact`, in that order."},
        "customisable_sections": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutSection"}, "description": "`setup_guide`, `section_tabs` and `seo`, each with a `position`."},
        "kpis": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutKpi"}, "description": "The layout's KPI tiles, 2 to 5, in tile order."},
        "created_at": {"type": "string", "description": "When the layout was created, such as `2026-11-05T07:12:40Z`."},
        "updated_at": {"type": "string", "description": "When the layout last changed."},
    }},
    "DashboardLayoutSummary": {"type": "object", "description": "A layout as listed, without sections or KPI tiles.", "properties": {
        "id": {"type": "string", "description": "The layout's `id`, a UUID. Pass it as `dashboard_id` in the path of the other calls."},
        "name": {"type": "string", "description": "The layout's name."},
        "default": {"type": "boolean", "description": "`true` for the store's default layout. Exactly one row has it."},
        "created_at": {"type": "string", "description": "When the layout was created."},
        "updated_at": {"type": "string", "description": "When the layout last changed."},
    }},
    "DashboardLayoutList": {"type": "object", "properties": {
        "dashboards": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardLayoutSummary"}, "description": "Every layout, with no paging."},
    }},
    "DashboardLayoutInput": {"type": "object", "minProperties": 1, "description": "Send the fields at the top level of the body. Create needs `name`; update takes only the fields to change.", "properties": {
        "name": {"type": "string", "maxLength": 60, "description": "The layout's name. No other layout may have it."},
        "default": {"type": "boolean", "description": "Send `true` to make this layout the default for every admin."},
        "copy_from": {"type": "string", "description": "On create, the `id` of the layout to copy. The default layout when you leave it out."},
        "standard_sections": {"type": "array", "items": STANDARD_INPUT, "description": "The standard sections to change, each with its `key`. They take only `visible`."},
        "customisable_sections": {"type": "array", "items": {"type": "object", "required": ["key"], "properties": {
            "key": {"type": "string", "enum": ["setup_guide", "section_tabs", "seo"], "description": "The section to change."},
            "visible": {"type": "boolean", "description": "Whether the dashboard shows the section."},
            "position": {"type": "integer", "description": "The section's new place among the customisable sections, from `1`."},
            "tabs": {"type": "array", "items": {"type": "object", "required": ["key"], "properties": {
                "key": {"type": "string", "enum": ["ecommerce", "content", "bookings", "courses", "blog"]},
                "visible": {"type": "boolean"},
                "position": {"type": "integer"},
            }}, "description": "On `section_tabs`, the tabs to change."},
            "parts": {"type": "array", "items": {"type": "object", "required": ["key"], "properties": {
                "key": {"type": "string", "enum": ["kpis", "records", "types", "todo", "store_checks"]},
                "visible": {"type": "boolean"},
            }}, "description": "On `seo`, the parts to change. `kpis` cannot be hidden."},
        }}, "description": "The customisable sections to change, each with its `key`."},
        "kpis": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 5, "description": "The layout's KPI tiles as 2 to 5 distinct metric keys in tile order, such as `[\"total_sales\", \"total_orders\"]`. It replaces the layout's tiles."},
    }},
    "DashboardLayoutError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `conflict` or `not_found`."},
        "message": {"type": "string", "description": "What went wrong, such as `dashboard not found`."},
        "details": {"type": "array", "description": "One entry per rejected field, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field, such as `name` or `dashboard_id`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `too_long`, `invalid_enum`, `not_supported`, `not_hideable`, `invalid_count`, `name_taken`, `default_required` or `not_found`."},
            "message": {"type": "string", "description": "The rule that failed."},
            "value": {"type": "string", "description": "The value you sent, when the store echoes it back."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
