"""The Gift cards endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Gift cards"
SLUG = "gift-cards"
BASE = "/admin/gift_cards"
ICON = "gift"

PREVIEW_GIFT_CARD_PAGE = "/api-reference/order-previews/apply-a-gift-card-to-a-preview"

OVERVIEW_DESCRIPTION = "List your store's gift cards, newest first, and filter them by code, email address or active state."
INTRO = "The Gift cards API has one endpoint, and you can call it from all seven SDKs. Its path is `/api/v4/admin/gift_cards`."

WARNING = None

NOTES = [
    "**A listing returns at most 20 gift cards per call, newest first.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get more, send `page` or `offset` while `pagination.has_next` is `true`.\n"
    "  `limit=0` is rejected with `400` and the reason `invalid_pagination`.",
    "**`code` and `email` match the whole value.** Both ignore letter case, and a part of a code or of an address\n"
    "  matches nothing. Pass the whole address to find a customer's cards, then use the card's `code` in\n"
    "  [Apply a gift card to a preview](" + PREVIEW_GIFT_CARD_PAGE + ").",
    "**The listing accepts only six parameters.** `limit`, `offset`, `page`, `code`, `email` and `is_active` are the\n"
    "  ones on this page; any other name, such as `is_paid`, `balance`, `customer_id` or `sort`, is rejected with `400` and\n"
    "  the reason `unknown_parameter`.",
    "**This API only lists gift cards.** There is no endpoint to create or change one.",
]

LIMIT = {"name": "limit", "in": "query", "description": "Gift cards per page, at most `20`. A larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of gift cards to skip.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "The page to return, counting from `1`. `page=0` is read as `1`.", "schema": {"type": "integer", "minimum": 1, "example": 1}}
CODE = {"name": "code", "in": "query", "description": "Keeps the gift card with exactly this code, in any letter case. A part of a code matches nothing.", "schema": {"type": "string", "example": "GIFT-0001"}}
EMAIL = {"name": "email", "in": "query", "description": "Keeps the gift cards held by exactly this email address, in any letter case. A part of an address matches nothing.", "schema": {"type": "string", "example": "jane.doe@example.com"}}
IS_ACTIVE = {"name": "is_active", "in": "query", "description": "Send `true` or `1` to keep active gift cards, or `false` or `0` to keep inactive ones. Any other value is rejected with `400` and the reason `invalid_boolean`.", "schema": {"type": "string", "enum": ["true", "false", "1", "0"], "example": "true"}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def text(description):
    return {"type": "string", "description": description}


def nullable_text(description):
    return {"type": ["string", "null"], "description": description}


def number(description):
    return {"type": "number", "description": description}


def whole(description):
    return {"type": "integer", "description": description}


def flag(description):
    return {"type": "boolean", "description": description}


GIFT_CARD = {
    "id": 31, "code": "GIFT-0001", "balance": 10.0, "initial_amount": 25.0, "email": "jane.doe@example.com",
    "first_name": "Jane", "last_name": "Doe", "message": None, "is_active": True, "is_paid": True,
    "available_to": None, "external_reference": None, "product_name": "Gift card",
    "created_on": "2026-11-03T08:10:28Z",
}
OLDER_GIFT_CARD = dict(GIFT_CARD, id=30, code="GIFT-0000", balance=25.0, created_on="2026-10-28T02:41:05Z")
SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

ENDPOINTS = [
    {
        "key": "list_gift_cards",
        "slug": "list-gift-cards",
        "title": "List gift cards",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 gift cards per call, newest first, with paging details.",
        "description": "Returns the gift cards in `gift_cards`, newest first, up to 20 per call, with a `pagination` block. Filter with `code`, `email` and `is_active`; `code` and `email` match the whole value in any letter case. Any query parameter not listed here is rejected with `400`.",
        "parameters": [CODE, EMAIL, IS_ACTIVE, LIMIT, OFFSET, PAGE],
        "responses": {
            "200": {
                "description": "The gift cards on this page in `gift_cards`, and `pagination` with `total`, `limit`, `offset`, `count`, `current_page`, `total_pages`, `has_next`, `has_previous`, `previous_page` and `next_page`. `next_page` is a full URL, or `null` on the last page.",
                "schema": {"type": "object", "properties": {
                    "gift_cards": {"type": "array", "items": ref("GiftCard")},
                    "pagination": ref("GiftCardPagination"),
                }},
                "example": {"gift_cards": [GIFT_CARD, OLDER_GIFT_CARD], "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a query parameter the listing does not accept (the reason `unknown_parameter`), `is_active` is not `true`, `false`, `1` or `0` (the reason `invalid_boolean`), or `limit` is `0` (the reason `invalid_pagination`).",
                "schema": ref("GiftCardError"),
            },
        },
        "example_call": {"query": {"email": "jane.doe@example.com", "is_active": "true"}},
    },
]

SCHEMAS = {
    "GiftCard": {"type": "object", "properties": {
        "id": whole("The gift card's `id`."),
        "code": text("The code a customer enters to pay with the card."),
        "balance": number("What is left on the card."),
        "initial_amount": number("The amount the card started with."),
        "email": nullable_text("The email address of the customer who holds the card. A card pays only for the customer whose record has this email."),
        "first_name": nullable_text("The holder's first name."),
        "last_name": nullable_text("The holder's last name."),
        "message": nullable_text("The message on the card, or `null`."),
        "is_active": flag("Whether the card is active."),
        "is_paid": flag("Whether the card was paid for."),
        "available_to": nullable_text("The last date the card can be used, or `null` for no end date."),
        "external_reference": nullable_text("A reference from another system, or `null`."),
        "product_name": nullable_text("The name of the gift card product."),
        "created_on": text("When the card was created, in UTC, such as `2026-11-03T08:10:28Z`."),
    }},
    "GiftCardPagination": {"type": "object", "properties": {
        "total": whole("The number of gift cards that match your request."),
        "limit": whole("The page size applied: the `limit` you sent, at most `20`."),
        "offset": whole("The number of gift cards skipped before this page."),
        "count": whole("The number of gift cards on this page."),
        "current_page": whole("This page's number, counting from `1`."),
        "total_pages": whole("The number of pages."),
        "has_next": flag("`true` when more gift cards follow."),
        "has_previous": flag("`true` when gift cards come before this page."),
        "previous_page": nullable_text("The full URL of the previous page, or `null` on the first page."),
        "next_page": nullable_text("The full URL of the next page, or `null` on the last page."),
    }},
    "GiftCardError": {"type": "object", "properties": {
        "status": text("`error`."),
        "code": whole("The HTTP status, such as `400`."),
        "message": text("What went wrong, such as `unknown query parameter(s): sort`."),
        "error": text("A machine-readable reason, such as `unknown_parameter`, `invalid_boolean` or `invalid_pagination`."),
        "errors": {"type": "array", "description": "One entry for each rejected query parameter.", "items": {"type": "object", "properties": {
            "field": text("The query parameter."),
            "code": text("Why it was rejected, such as `unknown_parameter` or `out_of_range`."),
        }}},
    }},
}
