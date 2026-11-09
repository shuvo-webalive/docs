"""The Dashboard banners endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Dashboard banners"
SLUG = "dashboard-banners"
BASE = "/admin/dashboard/banners"
ICON = "bullhorn"

OVERVIEW_DESCRIPTION = "List, create, retrieve, update and delete the announcement banners on the store's admin dashboard, and read the feed the dashboard shows them from."
INTRO = "The Dashboard banners API has six endpoints, and you can call every one from all seven SDKs. Five paths start with `/api/v4/admin/dashboard/banners`, and the feed is at `/api/v4/admin/dashboard/content_info`."

LIST_PAGE = "/api-reference/dashboard-banners/list-dashboard-banners"
CREATE_PAGE = "/api-reference/dashboard-banners/create-a-dashboard-banner"
GET_PAGE = "/api-reference/dashboard-banners/retrieve-a-dashboard-banner"
PATCH_PAGE = "/api-reference/dashboard-banners/update-a-dashboard-banner"
DELETE_PAGE = "/api-reference/dashboard-banners/delete-a-dashboard-banner"
FEED_PAGE = "/api-reference/dashboard-banners/get-the-dashboard-feed"

WARNING = (
    "**Banners are store-wide: a banner you create, change or delete shows on the dashboard of every admin.**\n"
    "  A created banner appears in [Get the dashboard feed](" + FEED_PAGE + ") at once while `active` is `true`,\n"
    "  and it stays until you delete it with [Delete a dashboard banner](" + DELETE_PAGE + "). Creating, moving\n"
    "  or deleting a banner also changes the `position` of the banners after it. The store already has banners of its own,\n"
    "  so list them with [List dashboard banners](" + LIST_PAGE + ") before you write, and change only banners you created."
)

NOTES = [
    "**Send the fields of every write as they are, with no wrapper.** Create and update take the banner's fields at\n"
    "  the top level of the body, and responses return the banner the same way. A field a banner does not have is\n"
    "  rejected with `400` and the reason `unknown_field`, and one `400` lists every field that failed.",
    "**Pass the banner's `key` as `banner_key`.** The `key` is a short name such as `spring_sale`: lowercase\n"
    "  letters, digits and `_`, starting with a letter, up to 64 characters, and unique. You choose it when you\n"
    "  create the banner, and you cannot change it afterwards. A `key` that matches no banner is rejected with `404`\n"
    "  and the reason `not_found`.",
    "**`learn_more` is required, and it takes one of two forms.** `{\"action\": \"open_link\", \"label\": \"...\",\n"
    "  \"url\": \"https://...\"}` opens a link. `{\"action\": \"open_modal\", \"label\": \"...\", \"title\": \"...\",\n"
    "  \"subtitle\": \"...\", \"steps\": [{\"title\": \"...\", \"description\": \"...\"}]}` opens a window with at least\n"
    "  one step. A `url` must start with `https`. `try_it` is optional: `{\"label\": \"...\", \"url\": \"...\"}` adds a\n"
    "  second button, and `null` means none.",
    "**`position` counts from `1` over every banner, hidden ones included.** Without `position`, a new banner goes\n"
    "  last. With one, from `1` to one more than the number of banners, the banners from that place move down by one.\n"
    "  Deleting a banner moves the banners after it back up, so the positions always run `1`, `2`, `3` and on.",
    "**An update changes only what you send, and replaces `learn_more` and `try_it` whole.** An `open_modal`\n"
    "  `learn_more` sent over an `open_link` one drops the `url`. `\"try_it\": null` removes the second button. `key` cannot\n"
    "  be sent, and an empty body is rejected with `400`. `icon` is saved as you send it and is not checked\n"
    "  against a list.",
    "**A banner with `active` `false` stays in the list but leaves the feed.** [List dashboard banners](" + LIST_PAGE + ")\n"
    "  returns every banner. [Get the dashboard feed](" + FEED_PAGE + ") returns only the active ones, and beside them the\n"
    "  support contact details the dashboard shows.",
]

BANNER_KEY = {
    "name": "banner_key",
    "in": "path",
    "required": True,
    "description": "The banner's `key`, from [List dashboard banners](" + LIST_PAGE + ") or the `key` you chose when you created it, such as `spring_sale`.",
    "schema": {"type": "string", "example": "spring_sale"},
}

ERROR_REF = {"$ref": "#/components/schemas/DashboardBannerError"}
BANNER_REF = {"$ref": "#/components/schemas/DashboardBanner"}

LINK = {"action": "open_link", "label": "Learn more", "url": "https://example.com/spring-sale"}
MODAL = {
    "action": "open_modal", "label": "Learn more", "title": "How it works", "subtitle": "Three steps",
    "steps": [
        {"title": "Pick a product", "description": "Choose the products in the sale."},
        {"title": "Set the price", "description": "Enter the sale price."},
        {"title": "Publish", "description": "Turn the sale on."},
    ],
}


def banner(**fields):
    row = {
        "key": "spring_sale", "position": 3, "active": True, "icon": "tag", "title": "Spring sale",
        "description": "Ends Friday.", "tags": ["Sales"], "learn_more": LINK, "try_it": None,
        "created_at": "2026-11-05T07:12:40Z", "updated_at": "2026-11-05T07:12:40Z",
    }
    row.update(fields)
    return row


FIRST = banner(key="new_checkout", position=1, icon="cart", title="New checkout", description="A faster checkout for your customers.",
               tags=["E-commerce", "Checkout"], learn_more=MODAL, try_it={"label": "Try it", "url": "https://example.com/checkout"},
               created_at="2026-08-21T00:00:00Z", updated_at="2026-08-21T00:00:00Z")
SECOND = banner(key="booking_reminders", position=2, icon="booking", title="Booking reminders", description="Send reminders before each booking.",
                tags=["Booking"], created_at="2026-08-21T00:00:00Z", updated_at="2026-08-21T00:00:00Z")
HIDDEN = banner(key="old_promo", position=4, active=False, title="Old promotion", description="No longer shown.", tags=[],
                created_at="2026-08-21T00:00:00Z", updated_at="2026-08-21T00:00:00Z")

CREATE_BODY = {
    "key": "spring_sale", "title": "Spring sale", "description": "Ends Friday.", "tags": ["Sales"], "icon": "tag",
    "learn_more": LINK,
}
PATCH_BODY = {"title": "Spring sale ends today", "active": False}

NOT_FOUND_404 = "No banner has that `key`. The reason is `not_found` and the message is `Banner ... was not found.`, ending in the `key` you sent."
RULES_400 = (
    "The body breaks a rule, and one response lists every field that failed: `title` is empty or longer than 80 "
    "characters, `description` is empty or longer than 200, `tags` holds more than 3 (`invalid_count`), `learn_more` is "
    "missing, `position` is outside `1` to one more than the number of banners (`out_of_range`), a `url` does not start with "
    "`https` (`invalid_value`), `try_it` lacks `label` or `url`, or the body has a field a banner does not have "
    "(`unknown_field`)."
)

ENDPOINTS = [
    {
        "key": "list_dashboard_banners",
        "slug": "list-dashboard-banners",
        "title": "List dashboard banners",
        "method": "GET",
        "path": BASE,
        "summary": "Returns every dashboard banner in `position` order, active and hidden ones.",
        "description": "Returns all the store's dashboard banners under `banners`, in one call with no paging. Each banner has its `key`, `position`, `active`, `icon`, `title`, `description`, `tags`, `learn_more` and `try_it`. To read only the banners the dashboard shows, use [Get the dashboard feed](" + FEED_PAGE + "). Query parameters you add are ignored.",
        "responses": {
            "200": {
                "description": "The banners under `banners`.",
                "schema": {"$ref": "#/components/schemas/DashboardBannerList"},
                "example": {"banners": [FIRST, SECOND, banner(), HIDDEN]},
            },
        },
        "example_call": {},
    },
    {
        "key": "create_dashboard_banner",
        "slug": "create-a-dashboard-banner",
        "title": "Create a dashboard banner",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a banner that shows on every admin's dashboard and returns it.",
        "description": "Send `key`, `title`, `description` and `learn_more`, which are required. The banner is `active` unless you send `active` `false`, `tags` is empty unless you send tags, and `position` is last unless you send one. The banner shows on the dashboard of every admin at once. The response is the banner, with no `Location` header. A `key` that another banner already has is rejected with `400`.",
        "body": {"schema": {"$ref": "#/components/schemas/DashboardBannerInput"}, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new banner.",
                "schema": BANNER_REF,
                "example": banner(),
            },
            "400": {"description": RULES_400 + " Or `key` breaks its rule or another banner has it (`duplicate`).", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_dashboard_banner",
        "slug": "retrieve-a-dashboard-banner",
        "title": "Retrieve a dashboard banner",
        "method": "GET",
        "path": BASE + "/{banner_key}",
        "summary": "Returns the banner whose `key` you pass as `banner_key`.",
        "description": "Returns one banner, active or hidden, with its `learn_more` and `try_it`. A hidden banner is returned too, with `active` `false`.",
        "parameters": [BANNER_KEY],
        "responses": {
            "200": {
                "description": "The banner.",
                "schema": BANNER_REF,
                "example": banner(),
            },
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"banner_key": "spring_sale"}},
    },
    {
        "key": "patch_dashboard_banner",
        "slug": "update-a-dashboard-banner",
        "title": "Update a dashboard banner",
        "method": "PATCH",
        "path": BASE + "/{banner_key}",
        "summary": "Changes only the fields you send and returns the banner.",
        "description": "Send only what changes. The change shows on the dashboard of every admin. `learn_more` and `try_it` are replaced whole, and `\"try_it\": null` removes the second button. `position` moves the banner and renumbers the others. `active` `false` hides the banner from [Get the dashboard feed](" + FEED_PAGE + ") and keeps it in the list. `key` cannot be sent.",
        "parameters": [BANNER_KEY],
        "body": {"schema": {"$ref": "#/components/schemas/DashboardBannerInput"}, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The banner after the change.",
                "schema": BANNER_REF,
                "example": banner(title="Spring sale ends today", active=False),
            },
            "400": {"description": "The body has no fields (the message is `request body is empty`), it sends `key` (`not_supported`), or it breaks a rule of [Create a dashboard banner](" + CREATE_PAGE + "), such as a blank `title` (`required`) or a field a banner does not have (`unknown_field`).", "schema": ERROR_REF},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"banner_key": "spring_sale"}},
    },
    {
        "key": "delete_dashboard_banner",
        "slug": "delete-a-dashboard-banner",
        "title": "Delete a dashboard banner",
        "method": "DELETE",
        "path": BASE + "/{banner_key}",
        "summary": "Deletes the banner whose `key` you pass as `banner_key` and returns no body.",
        "description": "Deletes the banner. It leaves the dashboard of every admin, and the banners after it move up one `position`.",
        "parameters": [BANNER_KEY],
        "responses": {
            "204": {"description": "The banner is deleted. The response has no body."},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
        },
        "example_call": {"path": {"banner_key": "spring_sale"}},
    },
    {
        "key": "get_dashboard_content_info",
        "slug": "get-the-dashboard-feed",
        "title": "Get the dashboard feed",
        "method": "GET",
        "path": "/admin/dashboard/content_info",
        "summary": "Returns the active banners the dashboard shows, with the support contact details.",
        "description": "Returns the active banners under `banners`, in `position` order, and beside them `contact` (the support `email`, `phone`, `live_chat` and `help_center_url`), `online_store` and `member_label`. A banner with `active` `false` is left out. A banner you create appears here at once.",
        "responses": {
            "200": {
                "description": "The active banners, the support contact and two store labels.",
                "schema": {"$ref": "#/components/schemas/DashboardBannerFeed"},
                "example": {
                    "banners": [FIRST, SECOND, banner()],
                    "contact": {"email": "support@example.com", "phone": "+1 555 0100", "live_chat": "Start a conversation", "help_center_url": "https://example.com/help"},
                    "online_store": True,
                    "member_label": "Customers",
                },
            },
        },
        "example_call": {},
    },
]

SCHEMAS = {
    "DashboardBannerStep": {"type": "object", "description": "One step of an `open_modal` window.", "properties": {
        "title": {"type": "string", "description": "The step's title."},
        "description": {"type": "string", "description": "What the step says."},
    }},
    "DashboardBannerLearnMore": {"type": "object", "description": "What the banner's main button does. It is `open_link` with a `url`, or `open_modal` with a `title`, a `subtitle` and at least one step.", "properties": {
        "action": {"type": "string", "enum": ["open_link", "open_modal"], "description": "`open_link` opens `url`. `open_modal` opens a window."},
        "label": {"type": "string", "description": "The button's text."},
        "url": {"type": "string", "description": "With `open_link`, the address to open. It must start with `https`."},
        "title": {"type": "string", "description": "With `open_modal`, the window's title."},
        "subtitle": {"type": "string", "description": "With `open_modal`, the window's subtitle."},
        "steps": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardBannerStep"}, "description": "With `open_modal`, the window's steps. At least one."},
    }},
    "DashboardBannerTryIt": {"type": "object", "description": "The banner's second button.", "properties": {
        "label": {"type": "string", "description": "The button's text."},
        "url": {"type": "string", "description": "The address the button opens. It must start with `https`."},
    }},
    "DashboardBanner": {"type": "object", "properties": {
        "key": {"type": "string", "description": "The banner's `key`. Pass it as `banner_key` in the path of the other calls."},
        "position": {"type": "integer", "description": "The banner's place among all banners, from `1`."},
        "active": {"type": "boolean", "description": "Whether the dashboard shows the banner."},
        "icon": {"type": "string", "description": "The icon name, saved as you sent it."},
        "title": {"type": "string", "description": "The banner's title, 1 to 80 characters."},
        "description": {"type": "string", "description": "The banner's text, 1 to 200 characters."},
        "tags": {"type": "array", "items": {"type": "string"}, "description": "Up to 3 tags."},
        "learn_more": {"$ref": "#/components/schemas/DashboardBannerLearnMore"},
        "try_it": {"oneOf": [{"$ref": "#/components/schemas/DashboardBannerTryIt"}, {"type": "null"}], "description": "The second button, or `null` when the banner has none."},
        "created_at": {"type": "string", "description": "When the banner was created, such as `2026-11-05T07:12:40Z`."},
        "updated_at": {"type": "string", "description": "When the banner was created or last changed."},
    }},
    "DashboardBannerList": {"type": "object", "properties": {
        "banners": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardBanner"}, "description": "Every banner, with no paging."},
    }},
    "DashboardBannerContact": {"type": "object", "description": "The support details the dashboard shows.", "properties": {
        "email": {"type": "string", "description": "The support email address."},
        "phone": {"type": "string", "description": "The support phone number."},
        "live_chat": {"type": "string", "description": "The live chat label."},
        "help_center_url": {"type": "string", "description": "The help centre address."},
    }},
    "DashboardBannerFeed": {"type": "object", "properties": {
        "banners": {"type": "array", "items": {"$ref": "#/components/schemas/DashboardBanner"}, "description": "The active banners only, in `position` order."},
        "contact": {"$ref": "#/components/schemas/DashboardBannerContact"},
        "online_store": {"type": "boolean", "description": "Whether the store has an online store."},
        "member_label": {"type": "string", "description": "What the dashboard calls the store's customers, such as `Customers`."},
    }},
    "DashboardBannerInput": {"type": "object", "minProperties": 1, "description": "Send the fields at the top level of the body. Create needs `key`, `title`, `description` and `learn_more`; update takes only the fields to change and never `key`.", "properties": {
        "key": {"type": "string", "maxLength": 64, "pattern": "^[a-z][a-z0-9_]*$", "description": "On create, the banner's `key`: lowercase letters, digits and `_`, starting with a letter, unique."},
        "title": {"type": "string", "minLength": 1, "maxLength": 80, "description": "The banner's title."},
        "description": {"type": "string", "minLength": 1, "maxLength": 200, "description": "The banner's text."},
        "icon": {"type": "string", "description": "The icon name. It is saved as you send it."},
        "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 3, "description": "Up to 3 tags. Empty when you leave it out."},
        "learn_more": {"$ref": "#/components/schemas/DashboardBannerLearnMore"},
        "try_it": {"oneOf": [{"$ref": "#/components/schemas/DashboardBannerTryIt"}, {"type": "null"}], "description": "The second button. On update, `null` removes it."},
        "position": {"type": "integer", "minimum": 1, "description": "The banner's place, from `1` to one more than the number of banners. The last place when you leave it out on create."},
        "active": {"type": "boolean", "description": "Whether the dashboard shows the banner. `true` when you leave it out on create."},
    }},
    "DashboardBannerError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
        "message": {"type": "string", "description": "What went wrong, such as `Banner ... was not found.`"},
        "details": {"type": "array", "description": "One entry per rejected field, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field, such as `title` or `position`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `duplicate`, `invalid_count`, `invalid_value`, `invalid_enum`, `out_of_range`, `not_supported` or `unknown_field`."},
            "message": {"type": "string", "description": "The rule that failed."},
        }}},
        "request_id": {"type": "string", "description": "A value that identifies this request."},
    }}}},
}
