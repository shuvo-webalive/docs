"""The Order previews endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Order previews"
SLUG = "order-previews"
BASE = "/admin/orders/preview"
ICON = "clipboard-check"

CREATE_PAGE = "/api-reference/order-previews/start-an-order-preview"
RETRIEVE_PAGE = "/api-reference/order-previews/retrieve-an-order-preview"
CONFIRM_PAGE = "/api-reference/order-previews/place-the-order-from-a-preview"
APPLY_COUPON_PAGE = "/api-reference/order-previews/apply-a-coupon-to-a-preview"
REMOVE_COUPON_PAGE = "/api-reference/order-previews/remove-the-coupon-from-a-preview"
APPLY_GIFT_CARD_PAGE = "/api-reference/order-previews/apply-a-gift-card-to-a-preview"
REMOVE_GIFT_CARD_PAGE = "/api-reference/order-previews/remove-the-gift-card-from-a-preview"
GIFT_CARDS_PAGE = "/api-reference/gift-cards/list-gift-cards"
CREATE_ORDER_PAGE = "/api-reference/orders/create-an-order"
CREATE_DISCOUNT_PROFILE_PAGE = "/api-reference/discount-profiles/create-a-discount-profile"
RETRIEVE_CUSTOMER_PAGE = "/api-reference/customers/retrieve-a-customer"

OVERVIEW_DESCRIPTION = "Price an order before you place it, apply a coupon or a gift card to the price, and then place the order."
INTRO = (
    "The Order previews API has seven endpoints, and you can call every one from all seven SDKs. Every path"
    " starts with `/api/v4/admin/orders/preview`. You start a preview with the products, the customer and the"
    " delivery type, read the priced result, apply a coupon or a gift card, and place the order from the preview."
    " Starting a preview places no order."
)

WARNING = (
    "**[Place the order from a preview](" + CONFIRM_PAGE + ") creates a real order.**\n"
    "  It closes the preview, and every later call on it, including a second confirm, is rejected with `410`.\n"
    "  A preview also ends on its own: it expires 30 minutes after it was started or after the last time you\n"
    "  applied or removed a coupon or a gift card. Start a new preview when you need one again."
)

NOTES = [
    "**The path takes the `session_id` of the preview.** [Start an order preview](" + CREATE_PAGE + ") returns it as\n"
    "  `order.session.session_id`, a value such as `PRV-3f2a9c41b7d80e65`. Every other call takes it as\n"
    "  `preview_session_id` in the path. An unknown value returns `404` with the code `not_found`.",
    "**A preview lasts 30 minutes from its last change.** `order.session.expires_at` is 30 minutes after\n"
    "  `created_at`. Each time you apply or remove a coupon or a gift card, `expires_at` moves to 30 minutes after that\n"
    "  call. [Retrieve an order preview](" + RETRIEVE_PAGE + ") does not move it.",
    "**You send only `product_id` and `quantity` for each product.** The store reads the prices, taxes and\n"
    "  shipping cost itself, so a `price` or `product_name` in a product line is rejected with `400` and the reason\n"
    "  `unknown_field`. A body field the call does not accept, such as `coupon_code`, is rejected the same way: apply a\n"
    "  coupon with [Apply a coupon to a preview](" + APPLY_COUPON_PAGE + ").",
    "**Send `customer_id`, or send a billing address.** With `customer_id` alone, the preview uses the customer's\n"
    "  saved addresses. Without `customer_id` and without `billing_address`, the call is rejected with `400`, and so is a\n"
    "  preview that has a product to ship and no shipping address.",
    "**`delivery_type` is `delivery`, `others_shipping`, `shipping` or `store_pickup`.** It is `shipping` when you leave it\n"
    "  out. With `store_pickup`, `shipping.shipping_cost` is `0` and the grand total is lower by that amount.",
    "**A preview takes one coupon and one gift card at a time.** A second coupon, even the same code, is rejected with\n"
    "  `409` and the code `coupon_already_applied`, and a second gift card with `gift_card_already_applied`. Remove the\n"
    "  applied one first with [Remove the coupon from a preview](" + REMOVE_COUPON_PAGE + ") or\n"
    "  [Remove the gift card from a preview](" + REMOVE_GIFT_CARD_PAGE + ").",
    "**A coupon only works if its discount profile applies to every customer and every product.** Create the profile with\n"
    "  [Create a discount profile](" + CREATE_DISCOUNT_PROFILE_PAGE + ") and send `is_applied_to_all_customers` `true`,\n"
    "  `is_applied_to_all_products` `true` and `category` `[]`. Without them, applying the code is rejected with `422` and\n"
    "  the message `Invalid Code`. The code you send is the profile's `default_coupon_code`.",
    "**A gift card pays only for the customer whose email address it holds.** The card's `email` must equal the email of\n"
    "  the customer record you previewed; the billing address's email does not count. Find a customer's cards with\n"
    "  [List gift cards](" + GIFT_CARDS_PAGE + ") and its `email` filter, then use the card in\n"
    "  [Apply a gift card to a preview](" + APPLY_GIFT_CARD_PAGE + "). Applying a gift card lowers `due` and leaves\n"
    "  `grand_total` as it was, and the preview spends nothing from the card.",
]

PAYMENT_GATEWAYS = ["ACP", "API", "APY", "BDP", "CHQ", "COD", "CRD", "CRL", "EXC", "GCRD", "LPP", "MOR", "PAY_RIGHT", "PIS", "PPL", "SCR", "ZIP"]
DELIVERY_TYPES = ["delivery", "others_shipping", "shipping", "store_pickup"]


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


PREVIEW_SESSION_ID = {
    "name": "preview_session_id",
    "in": "path",
    "required": True,
    "description": "The preview's `session_id`, from `order.session.session_id` in the response to [Start an order preview](" + CREATE_PAGE + "). It looks like `PRV-3f2a9c41b7d80e65`.",
    "schema": {"type": "string", "example": "PRV-3f2a9c41b7d80e65"},
}

SESSION_ID = "PRV-3f2a9c41b7d80e65"

ERROR_REF = ref("OrderPreviewError")

SESSION = {"session_id": SESSION_ID, "status": "active", "created_at": "2026-11-05T06:00:00Z", "expires_at": "2026-11-05T06:30:00Z"}
CUSTOMER = {"customer_id": 512, "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com"}
ITEM = {
    "product_id": 101, "product_name": "Cotton T-Shirt", "sku": "TSHIRT-001", "quantity": 2, "price": 8.0,
    "discount": 0.0, "tax": 1.6, "total_amount": 16.0, "taxable": True, "shippable": True,
}
SHIPPING = {"delivery_type": "shipping", "shipping_type": "flat_rate", "shipping_cost": 100.0, "shipping_tax": 0.0}
NO_DISCOUNTS = {"coupon": None, "gift_card": None}
TOTALS = {
    "sub_total": 16.0, "total_discount": 0.0, "total_tax": 1.6, "shipping_cost": 100.0, "handling_cost": 10.0,
    "total_surcharge": 0.0, "gift_card_applied": 0.0, "grand_total": 127.6, "due": 127.6,
}
STARTED = {
    "session": SESSION, "customer": CUSTOMER, "delivery_type": "shipping", "currency_code": "AUD",
    "items": [ITEM], "shipping": SHIPPING, "discounts": NO_DISCOUNTS, "totals": TOTALS,
}
LATER_SESSION = dict(SESSION, expires_at="2026-11-05T06:35:00Z")
COUPON_DISCOUNTS = {"coupon": {"code": "SAVE10", "status": "applied", "amount": 1.6}, "gift_card": None}
COUPON_TOTALS = dict(TOTALS, total_discount=1.6, total_tax=1.44, grand_total=125.84, due=125.84)
GIFT_CARD_DISCOUNTS = {"coupon": None, "gift_card": {"code": "GIFT-0001", "status": "applied", "applied_amount": 10.0, "remaining_balance": None}}
GIFT_CARD_TOTALS = dict(TOTALS, gift_card_applied=10.0, due=117.6)

ADDRESS = {"first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "address_line_1": "1 Example Street", "city": "Melbourne", "post_code": "3000"}
CONFIRMED_ORDER = {
    "order_id": 1043, "order_no": 1043, "internal_id": 2187, "uuid": "3f2b8c1e-6d4a-4e7b-9a15-0c8d2e6f7a41",
    "transaction_no": "TXN-ORDER-0001", "currency_code": "AUD", "order_status": "in_progress",
    "payment_status": "partial", "shipping_status": "unshipped", "sub_total": 16.0, "shipping_cost": 100.0,
    "shipping_tax": 0.0, "handling_cost": 10.0, "total_surcharge": 0.0, "total_discount": 0.0, "total_tax": 1.6,
    "grand_total": 127.6, "paid": 10.0, "due": 117.6, "items_total": 2,
    "customer_summary": CUSTOMER,
    "order_line_details": [{"product_id": 101, "product_name": "Cotton T-Shirt", "sku": "TSHIRT-001", "quantity": 2, "price": 8.0, "total_amount": 16.0}],
    "payments": [{"status": "success", "amount": 10.0, "payment_method": "manual", "transaction_reference": "REF-0001", "transaction_date": "2026-11-05T06:12:00Z"}],
    "billing_address": ADDRESS,
    "shipping_address": ADDRESS,
    "custom_fields": [],
}

NOT_FOUND_404 = "No preview has that `session_id`. The code is `not_found` and the message is `Order preview <session_id> was not found.`"
CLOSED_410 = "An order was already placed from this preview, so it is closed. The code is `gone`, and `details` has an entry on `session_id` with the code `session_confirmed` and the message `An order was already placed from this preview.`"
CODE_400 = "`code` is missing or empty (the code `required`), or is longer than 100 characters (the code `too_long`)."

ENDPOINTS = [
    {
        "key": "create_order_preview",
        "slug": "start-an-order-preview",
        "title": "Start an order preview",
        "method": "POST",
        "path": BASE,
        "summary": "Prices the products you send and returns a preview session, without placing an order.",
        "description": "Send the fields at the top level of the body, not wrapped in `order`; only `products` is required. The store prices the products, taxes, shipping and handling, and returns them with a `session` that holds the `session_id` every other call takes as `preview_session_id`. No order is created, and the preview expires 30 minutes after it starts. Send `customer_id` to use the customer's saved addresses, or send `billing_address`, and `shipping_address` for a product that ships.",
        "body": {"schema": ref("OrderPreviewInput"), "example": {
            "customer_id": 512, "delivery_type": "shipping",
            "products": [{"product_id": 101, "quantity": 2}],
        }},
        "responses": {
            "201": {
                "description": "The priced preview under `order`: `session`, `customer`, `delivery_type`, `currency_code`, `items`, `shipping`, `discounts` and `totals`. `discounts.coupon` and `discounts.gift_card` are `null` until you apply one. `shipping.shipping_tax` is not a field of `totals`, and `totals.grand_total` is `sub_total` minus `total_discount`, plus `total_tax`, `shipping_tax`, `shipping_cost`, `handling_cost` and `total_surcharge`.",
                "schema": {"type": "object", "properties": {"order": ref("OrderPreview")}},
                "example": {"order": STARTED},
            },
            "400": {"description": "`products` is missing or is not a list of `{product_id, quantity}` entries; a product line has a field other than `product_id` and `quantity`, or no `product_id` (the code `required`), or a `product_id` no product has (the code `unresolved`); the body has a field the call does not accept (the code `unknown_field`); `delivery_type` is not one of the four values (the code `invalid_value`); there is no `customer_id` and no `billing_address`; or a product ships and the preview has no shipping address.", "schema": ERROR_REF},
            "404": {"description": "`customer_id` matches no customer. The message is `Customer not found`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_order_preview",
        "slug": "retrieve-an-order-preview",
        "title": "Retrieve an order preview",
        "method": "GET",
        "path": BASE + "/{preview_session_id}",
        "summary": "Returns the preview whose `session_id` you pass, with its current totals.",
        "description": "Returns the preview in the same shape as [Start an order preview](" + CREATE_PAGE + "), with any coupon or gift card you applied. Reading a preview does not move `session.expires_at`. A preview that was confirmed returns `410`.",
        "parameters": [PREVIEW_SESSION_ID],
        "responses": {
            "200": {
                "description": "The preview under `order`.",
                "schema": {"type": "object", "properties": {"order": ref("OrderPreview")}},
                "example": {"order": STARTED},
            },
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
    {
        "key": "confirm_order_preview",
        "slug": "place-the-order-from-a-preview",
        "title": "Place the order from a preview",
        "method": "POST",
        "path": BASE + "/{preview_session_id}/confirm",
        "summary": "Places a real order from the preview and closes the preview.",
        "description": "This creates an order. It matches the last preview: the same `grand_total` and `total_discount`, with `order_status` `in_progress`. The body is optional; with no body, or with `{}`, the order has `payment_status` `unpaid`, `paid` `0` and `due` equal to `grand_total`. To record a payment, send `payment`, whose `payment_method` is required; `payment_status` `success` records it, `failed` is kept in `payments` but leaves the order unpaid, and `pending` leaves it unpaid. An `amount` below the grand total sets `payment_status` to `partial`, and an `amount` equal to it sets `paid`. After the call the preview is closed. To file the order under a transaction number, send `transaction_no` in the body.",
        "body": {"schema": ref("OrderPreviewConfirmInput"), "example": {
            "send_email": False, "transaction_no": "TXN-ORDER-0001",
            "payment": {"amount": 10.0, "payment_status": "success", "payment_method": "manual", "transaction_reference": "REF-0001", "transaction_date": "2026-11-05T06:12:00Z"},
        }},
        "parameters": [PREVIEW_SESSION_ID],
        "responses": {
            "201": {
                "description": "The new order under `order`, in the same flat shape as the response to [Create an order](" + CREATE_ORDER_PAGE + "): `order_id`, `internal_id`, `transaction_no`, the totals, `customer_summary`, `order_line_details`, `payments` and the addresses.",
                "schema": {"type": "object", "properties": {"order": ref("OrderFlat")}},
                "example": {"order": CONFIRMED_ORDER},
            },
            "400": {"description": "The body has a field the call does not accept (the code `unknown_field`); `payment_gateway` is not one of the listed values, is empty, is `null`, or is `PAY_IN_STORE` (the code `invalid_value`); `send_email` is not `true` or `false` (the code `invalid_type`); `payment` has no `payment_method` (the code `required`); or `transaction_no` in the body differs from an `X-Transaction-No` header (the code `header_body_mismatch`).", "schema": ERROR_REF},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "`payment.amount` is more than the amount due. The code is `payment_exceeds_due` on `payment.amount`, no order is created and the preview stays open.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
    {
        "key": "apply_order_preview_coupon",
        "slug": "apply-a-coupon-to-a-preview",
        "title": "Apply a coupon to a preview",
        "method": "POST",
        "path": BASE + "/{preview_session_id}/coupon",
        "summary": "Applies a coupon code to the preview and returns the lower totals.",
        "description": "Send the coupon's `code` at the top level of the body: the `default_coupon_code` of a discount profile that applies to every customer and every product. The response returns `discounts.coupon` with the `amount` taken off, and `totals` with the new `total_discount`, `total_tax` and `grand_total`. A preview takes one coupon: a second call, with the same or another code, is rejected with `409`. This call moves `session.expires_at` to 30 minutes after the call.",
        "parameters": [PREVIEW_SESSION_ID],
        "body": {"schema": ref("OrderPreviewCodeInput"), "example": {"code": "SAVE10"}},
        "responses": {
            "200": {
                "description": "Only `session`, `discounts` and `totals` under `order`, in that order. `discounts.coupon` has the `code`, `status` `applied` and the `amount`.",
                "schema": {"type": "object", "properties": {"order": ref("OrderPreviewDiscountResult")}},
                "example": {"order": {"session": LATER_SESSION, "discounts": COUPON_DISCOUNTS, "totals": COUPON_TOTALS}},
            },
            "400": {"description": CODE_400, "schema": ERROR_REF},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
            "409": {"description": "A coupon is already applied. The code is `conflict` and the detail on `code` is `coupon_already_applied`.", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "No discount profile has that code, or the profile does not apply to every customer and every product. The code is `unprocessable`, the detail is `invalid_coupon` and the message is `Invalid Code`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
    {
        "key": "remove_order_preview_coupon",
        "slug": "remove-the-coupon-from-a-preview",
        "title": "Remove the coupon from a preview",
        "method": "DELETE",
        "path": BASE + "/{preview_session_id}/coupon",
        "summary": "Removes the applied coupon, so the totals return to what they were before it.",
        "description": "Removes the coupon and returns `204` with no body. [Retrieve an order preview](" + RETRIEVE_PAGE + ") then shows the totals the preview had before you applied the coupon. This call moves `session.expires_at` to 30 minutes after the call.",
        "parameters": [PREVIEW_SESSION_ID],
        "responses": {
            "204": {"description": "The coupon is removed. No body."},
            "404": {"description": "No preview has that `session_id` (the code `not_found`), or the preview has no coupon (the code `not_found`, the detail `coupon_not_applied`).", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
    {
        "key": "apply_order_preview_gift_card",
        "slug": "apply-a-gift-card-to-a-preview",
        "title": "Apply a gift card to a preview",
        "method": "POST",
        "path": BASE + "/{preview_session_id}/gift-card",
        "summary": "Applies a gift card to the preview, lowering the amount due.",
        "description": "Send the card's `code` at the top level of the body. The card pays up to its balance: `discounts.gift_card.applied_amount` is the smaller of the card's balance and `grand_total`, `totals.gift_card_applied` equals it, `grand_total` does not change and `due` is `grand_total` minus `gift_card_applied`. The preview spends nothing from the card. A preview takes one gift card, and the card must belong to the previewed customer. This call moves `session.expires_at` to 30 minutes after the call.",
        "parameters": [PREVIEW_SESSION_ID],
        "body": {"schema": ref("OrderPreviewCodeInput"), "example": {"code": "GIFT-0001"}},
        "responses": {
            "200": {
                "description": "Only `session`, `discounts` and `totals` under `order`, in that order. `discounts.gift_card` has the `code`, `status` `applied`, the `applied_amount` and `remaining_balance`, which is `null`.",
                "schema": {"type": "object", "properties": {"order": ref("OrderPreviewDiscountResult")}},
                "example": {"order": {"session": LATER_SESSION, "discounts": GIFT_CARD_DISCOUNTS, "totals": GIFT_CARD_TOTALS}},
            },
            "400": {"description": CODE_400, "schema": ERROR_REF},
            "404": {"description": NOT_FOUND_404, "schema": ERROR_REF},
            "409": {"description": "A gift card is already applied. The code is `conflict` and the detail on `code` is `gift_card_already_applied`.", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
            "422": {"description": "No gift card has that code, or the card has no balance, is past its `available_to` date, is inactive or unpaid, or holds an `email` other than the previewed customer's. The code is `unprocessable`, the detail is `invalid_gift_card` and the message is `Your code #<code> is not valid`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
    {
        "key": "remove_order_preview_gift_card",
        "slug": "remove-the-gift-card-from-a-preview",
        "title": "Remove the gift card from a preview",
        "method": "DELETE",
        "path": BASE + "/{preview_session_id}/gift-card",
        "summary": "Removes the applied gift card, so `due` returns to the grand total.",
        "description": "Removes the gift card and returns `204` with no body. This call moves `session.expires_at` to 30 minutes after the call.",
        "parameters": [PREVIEW_SESSION_ID],
        "responses": {
            "204": {"description": "The gift card is removed. No body."},
            "404": {"description": "No preview has that `session_id` (the code `not_found`), or the preview has no gift card (the code `not_found`, the detail `gift_card_not_applied`).", "schema": ERROR_REF},
            "410": {"description": CLOSED_410, "schema": ERROR_REF},
        },
        "example_call": {"path": {"preview_session_id": SESSION_ID}},
    },
]

SCHEMAS = {
    "OrderPreview": {"type": "object", "description": "A priced order that is not placed yet.", "properties": {
        "session": ref("OrderPreviewSession"),
        "customer": ref("OrderPreviewCustomer"),
        "delivery_type": text("`delivery`, `others_shipping`, `shipping` or `store_pickup`."),
        "currency_code": text("The store's currency, such as `AUD`."),
        "items": {"type": "array", "items": ref("OrderPreviewItem"), "description": "One entry for each product line. The same product sent twice is two lines."},
        "shipping": ref("OrderPreviewShipping"),
        "discounts": ref("OrderPreviewDiscounts"),
        "totals": ref("OrderPreviewTotals"),
    }},
    "OrderPreviewDiscountResult": {"type": "object", "description": "What the coupon and gift card calls return: only these three fields of the preview.", "properties": {
        "session": ref("OrderPreviewSession"),
        "discounts": ref("OrderPreviewDiscounts"),
        "totals": ref("OrderPreviewTotals"),
    }},
    "OrderPreviewSession": {"type": "object", "properties": {
        "session_id": text("The preview's `session_id`, such as `PRV-3f2a9c41b7d80e65`. Pass it as `preview_session_id` in the path of the other calls."),
        "status": text("`active`."),
        "created_at": text("When the preview started, in UTC, such as `2026-11-05T06:00:00Z`."),
        "expires_at": text("When the preview ends: 30 minutes after it started or after the last coupon or gift card change."),
    }},
    "OrderPreviewCustomer": {"type": "object", "description": "The customer. When you send a billing address, the names and email come from that address; otherwise they come from the customer's record.", "properties": {
        "customer_id": whole("The customer's `customer_id`."),
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": nullable_text("The email address, or `null`."),
    }},
    "OrderPreviewItem": {"type": "object", "properties": {
        "product_id": whole("The product's `product_id`."),
        "product_name": text("The product's name."),
        "sku": text("The product's SKU."),
        "quantity": whole("The quantity you sent."),
        "price": number("The unit price the store charges."),
        "discount": number("The discount on this line."),
        "tax": number("The tax on this line."),
        "total_amount": number("The line's total."),
        "taxable": flag("Whether the product is taxed."),
        "shippable": flag("Whether the product ships."),
    }},
    "OrderPreviewShipping": {"type": "object", "properties": {
        "delivery_type": text("The delivery type."),
        "shipping_type": nullable_text("The shipping type the store chose."),
        "shipping_cost": number("The shipping cost. `0` for `store_pickup`."),
        "shipping_tax": number("The tax on shipping. It is not a field of `totals`, but it is part of `totals.grand_total`. It is `0` when the call sent no addresses."),
    }},
    "OrderPreviewCoupon": {"type": "object", "properties": {
        "code": text("The coupon code."),
        "status": text("`applied`."),
        "amount": number("The amount the coupon takes off."),
    }},
    "OrderPreviewGiftCard": {"type": "object", "properties": {
        "code": text("The gift card's code."),
        "status": text("`applied`."),
        "applied_amount": number("The smaller of the card's balance and `totals.grand_total`."),
        "remaining_balance": {"type": ["number", "null"], "description": "`null`."},
    }},
    "OrderPreviewDiscounts": {"type": "object", "properties": {
        "coupon": {"oneOf": [ref("OrderPreviewCoupon"), {"type": "null"}], "description": "The applied coupon, or `null`."},
        "gift_card": {"oneOf": [ref("OrderPreviewGiftCard"), {"type": "null"}], "description": "The applied gift card, or `null`."},
    }},
    "OrderPreviewTotals": {"type": "object", "properties": {
        "sub_total": number("The total of the lines, before discounts and tax."),
        "total_discount": number("The coupon's discount."),
        "total_tax": number("The tax on the lines, recalculated after a coupon."),
        "shipping_cost": number("The shipping cost."),
        "handling_cost": number("The handling cost."),
        "total_surcharge": number("The surcharge."),
        "gift_card_applied": number("The amount the gift card pays. `0` with no gift card."),
        "grand_total": number("`sub_total` minus `total_discount`, plus `total_tax`, `shipping.shipping_tax`, `shipping_cost`, `handling_cost` and `total_surcharge`."),
        "due": number("`grand_total` minus `gift_card_applied`."),
    }},
    "OrderPreviewAddressInput": {"type": "object", "description": "An address, with the same fields as an address in [Create an order](" + CREATE_ORDER_PAGE + ").", "properties": {
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": text("The email address."),
        "address_line_1": text("The first address line."),
        "address_line_2": text("The second address line."),
        "city": text("The city."),
        "post_code": text("The post code."),
        "phone": text("The phone number."),
        "mobile": text("The mobile number."),
        "country_code": text("The country's code, such as `AU`."),
        "state_code": text("The state's code, such as `VIC`."),
    }},
    "OrderPreviewProductInput": {"type": "object", "required": ["product_id", "quantity"], "description": "A product line. Any other field is rejected with `400` and the reason `unknown_field`.", "properties": {
        "product_id": whole("The product's `product_id`."),
        "quantity": whole("A whole number of `1` or more."),
    }},
    "OrderPreviewInput": {"type": "object", "required": ["products"], "description": "Send these fields at the top level of the body. Any other field is rejected with `400` and the reason `unknown_field`.", "properties": {
        "customer_id": whole("The customer's `customer_id`, from [Retrieve a customer](" + RETRIEVE_CUSTOMER_PAGE + ") or a listing. Without it, send `billing_address`."),
        "delivery_type": {"type": "string", "enum": DELIVERY_TYPES, "description": "How the order is delivered. `shipping` when you leave it out."},
        "billing_address": ref("OrderPreviewAddressInput"),
        "shipping_address": ref("OrderPreviewAddressInput"),
        "products": {"type": "array", "items": ref("OrderPreviewProductInput"), "description": "The products to price. At least one."},
    }},
    "OrderPreviewCodeInput": {"type": "object", "required": ["code"], "properties": {
        "code": text("The coupon code or the gift card's code, up to 100 characters."),
    }},
    "OrderPreviewConfirmInput": {"type": "object", "description": "Every field is optional, and the body can be left out. Any other field is rejected with `400` and the reason `unknown_field`.", "properties": {
        "payment_gateway": {"type": "string", "enum": PAYMENT_GATEWAYS, "description": "The payment gateway. `PIS` is accepted and leaves the order unpaid. An empty value, `null`, `PAY_IN_STORE` or any other value is rejected with `400`."},
        "transaction_no": text("A transaction number you choose. The store files the order under it."),
        "send_email": flag("Whether the store emails the customer."),
        "payment": ref("OrderPreviewPaymentInput"),
    }},
    "OrderPreviewPaymentInput": {"type": "object", "required": ["payment_method"], "properties": {
        "amount": number("The amount paid. More than the amount due is rejected with `422`."),
        "payment_status": text("`success` records the payment. `failed` is kept in `payments` and the order stays unpaid. `pending` leaves it unpaid."),
        "payment_method": text("The payment method, such as `manual`. Required."),
        "transaction_reference": text("Your reference for the payment."),
        "transaction_date": text("When the payment was made."),
    }},
    "OrderPreviewError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": text("A machine-readable reason, such as `invalid_request`, `not_found`, `conflict`, `gone` or `unprocessable`."),
        "message": text("What went wrong, such as `Invalid Code`."),
        "details": {"type": "array", "description": "One entry for each rejected field, or an empty list.", "items": {"type": "object", "properties": {
            "field": text("The field, such as `code`, `session_id` or `payment.amount`."),
            "code": text("Why it was rejected, such as `required`, `unknown_field`, `coupon_already_applied` or `session_confirmed`."),
            "message": nullable_text("The rule that failed, or `null`."),
        }}},
        "request_id": text("Identifies this request."),
    }}}},
}
