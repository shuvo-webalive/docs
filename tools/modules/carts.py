"""The Carts endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Carts"
SLUG = "carts"
BASE = "/carts"
ICON = "cart-shopping"

ADD_PAGE = "/api-reference/carts/add-a-product-to-a-cart"
RETRIEVE_PAGE = "/api-reference/carts/retrieve-a-cart"
UPDATE_PAGE = "/api-reference/carts/update-a-cart-item"
REMOVE_PAGE = "/api-reference/carts/remove-an-item-from-a-cart"
ORDER_PAGE = "/api-reference/carts/create-an-order-from-a-cart"
CREATE_CUSTOMER_PAGE = "/api-reference/customers/create-a-customer"
STOCK_PAGE = "/api-reference/inventory-locations/list-stock-at-an-inventory-location"

OVERVIEW_DESCRIPTION = "Add products to a customer's cart, read it, change or remove its items, empty it, and turn it into an order."
INTRO = (
    "The Carts API has seven endpoints, and you can call every one from all seven SDKs. Six of them have paths that"
    " start with `/api/v4/carts` and use the same access token as every other endpoint;"
    " [Create an order from a cart](" + ORDER_PAGE + ") uses `/api/v4/admin/orders/carts/{session_id}`."
)

WARNING = (
    "**Adding a product and creating an order take different numbers for the same customer.**\n"
    "  [Add a product to a cart](" + ADD_PAGE + ") takes the customer's `internal_id` in its `customer_id`\n"
    "  field, and rejects the customer's `customer_id` with `400` and the message `No Customer Found`.\n"
    "  [Create an order from a cart](" + ORDER_PAGE + ") takes the customer's `customer_id`.\n"
    "  [Create a customer](" + CREATE_CUSTOMER_PAGE + ") returns both values."
)

NOTES = [
    "**You name each cart with a `session_id` you choose.** Send it in the body each time you add a product,\n"
    "  and pass the same value as the `session_id` path parameter in every other cart call. If you add a\n"
    "  product without it, the store names the cart with your HTTP session's 32-character `JSESSIONID` cookie\n"
    "  value, and only `cart.session_id` in the response tells you that name.",
    "**A cart exists only while it has items.** Reading a cart with no items returns `400` with the message\n"
    "  `Your shopping cart is empty`, not `404`. That happens after you empty the cart, remove its last item\n"
    "  or turn it into an order, and for a `session_id` you never used. Emptying a cart that is already empty\n"
    "  returns the same `400`.",
    "**Only the response to adding a product shows the customer.** Its `cart.customer_id` is the customer's\n"
    "  `internal_id` you sent. [Retrieve a cart](" + RETRIEVE_PAGE + ") and [Update a cart item](" + UPDATE_PAGE + ")\n"
    "  return `cart.customer_id` as `null`, even when your client sends back the `JSESSIONID` cookie the store set.\n"
    "  A cart never holds the customer's `customer_id`, so keep it yourself:\n"
    "  [Create an order from a cart](" + ORDER_PAGE + ") needs it.",
    "**The shipping address sets the cart's shipping taxes, but no cart response returns an address.** The\n"
    "  `shipping_address.country_code` you send when you add a product or update an item decides\n"
    "  `shipping.shipping_tax` and `shipping.handling_tax`, and every later read of the cart shows the result.\n"
    "  Without a shipping address, both are `0.0`. The store does not check any address field, and accepts `{}`.",
    "**An order gets the customer's saved addresses by default.** When you send `shipping_address` and\n"
    "  `billing_address` to [Update a cart item](" + UPDATE_PAGE + ") and then call\n"
    "  [Create an order from a cart](" + ORDER_PAGE + ") with the same `JSESSIONID` cookie, the order gets those\n"
    "  two addresses instead. Addresses you send when you add a product never reach the order. The order's\n"
    "  `shipping_tax` follows the order's addresses, so it can differ from the cart's `shipping.shipping_tax`.\n"
    "  No cart call changes the customer's saved addresses.",
    "**A `200` does not always mean the call worked.** The store does not handle `GET` on `/carts`, `POST` on\n"
    "  `/carts/{session_id}`, or `GET` and `PATCH` on `/carts/{session_id}/cart_items/{cart_item_id}`: each\n"
    "  returns `200` with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}`. Add products with `POST`\n"
    "  on `/carts`, and change an item's quantity with `PATCH` on `/carts/{session_id}`.",
]

SESSION_ID = {
    "name": "session_id",
    "in": "path",
    "required": True,
    "description": "The cart's `session_id`: the value you sent when you added the first product, or `cart.session_id` from that response.",
    "schema": {"type": "string", "example": "cart-7f3a9c2e1b"},
}

CART_ITEM_ID = {
    "name": "cart_item_id",
    "in": "path",
    "required": True,
    "description": "The cart item's `id`, from `items[].id` in a cart response. The store numbers cart items across all carts, so take the value from a response and do not count from `1`.",
    "schema": {"type": "integer", "example": 42},
}

SESSION = "cart-7f3a9c2e1b"
REQUEST_ID = "8d2f6c1a-4b7e-4f3a-9c5d-2e1b0a7f6c34"
IMAGE = "https://your-store.example.com/resources/product/product-101/150-cotton-t-shirt.webp"


def error(code, message):
    return {"error": {"code": code, "message": message, "details": [], "request_id": REQUEST_ID}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


EMPTY_CART = error("invalid_request", "Your shopping cart is empty")
NO_CUSTOMER = error("invalid_request", "No Customer Found")
ITEM_NOT_FOUND = error("not_found", "f:cart item not found")

ERROR_REF = ref("CartError")
CART_RESPONSE = {"type": "object", "properties": {"cart": ref("Cart")}}

ADDRESS = {
    "first_name": "Alex", "last_name": "Taylor", "address_line1": "1 Example Street", "address_line2": "",
    "city": "Sydney", "post_code": "2000", "phone": "", "mobile": "", "fax": "", "email": "alex.taylor@example.com",
    "country_code": "AU", "state_code": "NSW",
}

SAMPLE_PRODUCT = {
    "id": 101, "sku": "TSHIRT-001", "base_price": 25.0, "available_stock": 25, "on_sale": False, "cost_price": 0.0,
    "sale_price": 0.0, "url": "cotton-t-shirt", "name": "Cotton T-Shirt", "product_type": "simple", "image_link": IMAGE,
}


def sample_cart(quantity, customer_id):
    return {
        "customer_id": customer_id,
        "session_id": SESSION,
        "currency_code": "AUD",
        "currency_symbol": "$",
        "delivery_type": "shipping",
        "totals": {"subtotal": 25.0 * quantity, "discount": 0.0, "shipping_discount": 0.0, "tax": 2.5 * quantity,
                   "total": 27.5 * quantity, "grand_total": 27.5 * quantity, "paid": 0.0},
        "shipping": {"cost": 10.0, "handling_fee": 0.0, "handling_tax": 0.0, "shipping_tax": 1.0, "total_tax": 0.0},
        "items": [{
            "id": 42, "quantity": quantity, "variations": None, "taxable": True, "shippable": True,
            "pricing": {"unit_price": 25.0, "display_unit_price": 27.5, "total": 27.5 * quantity, "discount": 0.0,
                        "discount_tax": 0.0, "tax": 2.5 * quantity},
            "product": SAMPLE_PRODUCT,
        }],
        "discount": {"discount": 0.0, "order_discount": 0.0, "shipping_discount": 0.0, "discount_on_tax": 0.0,
                     "discount_on_shipping_tax": 0.0},
        "messages": {"discount": {"message": "", "status": None}},
    }


SAMPLE_GROUP_META = {"cart": {"kind": "resource", "writable": True, "href": "/api/v4/carts/{sessionId}"}}

COUNTRY = {"id": 12, "name": "Australia", "code": "AU"}
STATE = {"id": 71, "name": "New South Wales", "code": "NSW"}


def order_address(address_id):
    return {
        "id": address_id, "first_name": "Alex", "last_name": "Taylor", "email": "alex.taylor@example.com",
        "company_name": "", "address_line_1": "1 Example Street", "address_line_2": "", "country": COUNTRY,
        "state": STATE, "city": "Sydney", "post_code": "2000", "mobile": "", "phone": "", "fax": "",
    }


ORDER_BODY = {"customer_id": 123, "payment_gateway": "PIS", "delivery_type": "shipping", "transaction_no": "web-order-0001"}

SAMPLE_ORDER = {
    "order_id": 1052,
    "internal_id": 2310,
    "order_no": 1052,
    "transaction_no": None,
    "currency_code": "AUD",
    "order_status": "in_progress",
    "payment_status": "unpaid",
    "shipping_status": "unshipped",
    "sub_total": 25.0,
    "shipping_cost": 10.0,
    "shipping_tax": 1.0,
    "handling_cost": 0.0,
    "total_surcharge": 0.0,
    "total_discount": 0.0,
    "total_tax": 2.5,
    "grand_total": 38.5,
    "paid": 0.0,
    "due": 38.5,
    "items_total": 1,
    "ip_address": "203.0.113.10",
    "order_channel": None,
    "created_at": "2026-10-07T09:15:02",
    "updated_at": "2026-10-07T09:15:02",
    "customer_summary": {
        "first_name": "Alex", "last_name": "Taylor", "customer_group": "", "gender": None, "customer_id": 123,
        "internal_id": 45, "email": "alex.taylor@example.com", "address_line_1": "1 Example Street",
        "address_line_2": "", "city": "Sydney", "country": COUNTRY, "state": STATE, "post_code": "2000",
        "phone": "", "mobile": "", "fax": "", "company_name": "",
    },
    "order_line_details": [{
        "item_id": 3307, "product_name": "Cotton T-Shirt", "product_id": 101, "sku": "TSHIRT-001", "quantity": 1,
        "price": 25.0, "total_amount": 25.0, "tax": 2.5, "discount": 0.0, "tax_discount": 0.0, "is_taxable": True,
        "is_shippable": True, "image_url": IMAGE, "variations": [], "serial_batch_number": "",
    }],
    "payments": [{
        "id": 5530, "status": "awaiting", "amount": 38.5, "payment_method": "PIS", "track_info": "",
        "gateway_name": "", "gateway_code": "PIS", "gateway_response": "", "payer_info": "",
        "paying_date": "2026-10-07T09:15:02Z", "transaction_date": "2026-10-07T09:15:02Z",
        "transaction_reference": "",
    }],
    "external_reference_order_id": None,
    "external_reference_store_id": None,
    "external_reference_order_no": None,
    "external_reference_status": None,
    "external_reference_url": None,
    "customer_po_number": "",
    "payment_term": "",
    "fulfillment_mode": "MANUAL",
    "fulfillment_term": "IMMEDIATELY",
    "invoice_mode": "",
    "billing_address": order_address(8801),
    "shipping_address": order_address(8802),
    "custom_fields": [],
}

ENDPOINTS = [
    {
        "key": "add_cart_item",
        "slug": "add-a-product-to-a-cart",
        "title": "Add a product to a cart",
        "method": "POST",
        "path": BASE,
        "summary": "Adds a product to a cart, creating the cart if needed, and returns the cart.",
        "description": "Adds a product to the cart named by `session_id`, creating the cart if needed, and returns the whole cart under `cart`. Send the product's `id` as `product_id`, a `quantity`, and the customer's `internal_id` as `customer_id`, at the top level of the body. If you leave out `session_id`, the store names the cart with your HTTP session's `JSESSIONID` cookie value, and `cart.session_id` in the response shows that name. Adding a product that is already in the cart raises that cart item's `quantity` and keeps its `id`.",
        "body": {
            "schema": ref("CartItemInput"),
            "example": {"product_id": 101, "quantity": 1, "customer_id": 45, "session_id": SESSION, "shipping_address": ADDRESS},
        },
        "responses": {
            "201": {
                "description": "The cart under `cart`, with the `customer_id` you sent. The response has no `group_meta`. When your request sends no `JSESSIONID` cookie, the response sets one in a `Set-Cookie` header. If the product needs options and you send none, the call also returns `201`, but the body is not valid JSON: it has `\"status\": \"incomplete-info\"` instead of `cart`.",
                "schema": CART_RESPONSE,
                "example": {"cart": sample_cart(1, 45)},
            },
            "400": {
                "description": "`customer_id` or `quantity` is missing: the message is `customer_id not found` or `quantity not found`. You sent the customer's `customer_id` instead of the customer's `internal_id`: the message is `No Customer Found`. No product has that `product_id`, or the product was deleted: the message is `No product found`. A deleted product can still appear in [List stock at an inventory location](" + STOCK_PAGE + "). The cart would hold more of the product than its stock: the message is `f:<n> quantity of this product is not available`. Carts do not reserve stock, so this limit applies to each cart on its own.",
                "schema": ERROR_REF,
                "example": NO_CUSTOMER,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_cart",
        "slug": "retrieve-a-cart",
        "title": "Retrieve a cart",
        "method": "GET",
        "path": BASE + "/{session_id}",
        "summary": "Returns the cart for a `session_id`, with its items, totals and shipping taxes.",
        "description": "Returns the cart under `cart`, with `group_meta` beside it; no other cart call returns `group_meta`. `cart.customer_id` is `null` here, even when your client sends back the `JSESSIONID` cookie the store set when you added the product. A cart with no items returns `400` with the message `Your shopping cart is empty`, not `404`. Query parameters are ignored, `field_metadata` included.",
        "parameters": [SESSION_ID],
        "responses": {
            "200": {
                "description": "The cart under `cart`, with `customer_id` set to `null`, and `group_meta`. The response has the header `Cache-Control: no-cache, no-store`, and no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {"cart": ref("Cart"), "group_meta": ref("CartGroupMeta")}},
                "example": {"cart": sample_cart(1, None), "group_meta": SAMPLE_GROUP_META},
            },
            "400": {
                "description": "The cart has no items: you emptied it, removed its last item or turned it into an order, or no product was ever added under that `session_id`. The message is `Your shopping cart is empty`.",
                "schema": ERROR_REF,
                "example": EMPTY_CART,
            },
        },
        "example_call": {"path": {"session_id": SESSION}},
    },
    {
        "key": "resolve_cart_session",
        "slug": "resolve-a-cart-session",
        "title": "Resolve a cart session",
        "method": "PUT",
        "path": BASE + "/{session_id}",
        "summary": "Returns the `session_id` to use, as `sessionId`, and changes no cart.",
        "description": "Returns `sessionId` and changes nothing: no cart moves or merges, even when `sessionId` names another cart. Send `{}` to get back the `session_id` from the path, or send a `sessionId` to get that value back. Send `\"sessionId\": null` or `\"\"` to get your HTTP session's `JSESSIONID`: the cookie your client sends, or a new value when it sends none. A `session_id` key in the body is ignored.",
        "parameters": [SESSION_ID],
        "body": {"schema": ref("CartSessionInput"), "example": {}},
        "responses": {
            "200": {
                "description": "`sessionId`: the body's `sessionId` when you send one, your HTTP session's `JSESSIONID` when it is `null` or `\"\"`, and otherwise the `session_id` from the path.",
                "schema": ref("CartSession"),
                "example": {"sessionId": SESSION},
            },
        },
        "example_call": {"path": {"session_id": SESSION}},
    },
    {
        "key": "update_cart_item",
        "slug": "update-a-cart-item",
        "title": "Update a cart item",
        "method": "PATCH",
        "path": BASE + "/{session_id}",
        "summary": "Changes the `quantity` of one item in the cart and returns the updated cart.",
        "description": "Sets the `quantity` of the cart item whose `id` you send as `cart_item_id`, and returns the whole cart; other items do not change. A `shipping_address` sets the cart's shipping taxes, and an order you create with the same `JSESSIONID` cookie gets this call's `shipping_address` and `billing_address`. Always send `quantity`: without it the call returns `500`. Do not send `customer_id`: the call returns `500` with a body that is not valid JSON, and still saves the new `quantity`.",
        "parameters": [SESSION_ID],
        "body": {"schema": ref("CartItemUpdateInput"), "example": {"cart_item_id": 42, "quantity": 2}},
        "responses": {
            "200": {
                "description": "The cart under `cart`, with the item's new `quantity` and `totals.subtotal` recalculated. `customer_id` is `null`, and the response has no `group_meta`.",
                "schema": CART_RESPONSE,
                "example": {"cart": sample_cart(2, None)},
            },
            "400": {
                "description": "`cart_item_id` is missing: the message is `f:cart_item_id not found`. Or `quantity` is `0`: the message is `f:Minimum required quantity is 1`.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "No cart item has that `cart_item_id`.",
                "schema": ERROR_REF,
            },
            "500": {
                "description": "The body has no `quantity`: the message is `Cannot invoke method toBigInteger() on null object`. Or the body has `customer_id`: the code is `internal_error`, the response body is not valid JSON, and the new `quantity` is saved anyway.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"session_id": SESSION}},
    },
    {
        "key": "delete_cart",
        "slug": "empty-a-cart",
        "title": "Empty a cart",
        "method": "DELETE",
        "path": BASE + "/{session_id}",
        "summary": "Removes every item from the cart and returns `204` with no body.",
        "description": "Removes every item from the cart and returns `204` with no body. Reading the cart afterwards, or emptying it again, returns `400` with the message `Your shopping cart is empty`. To remove one item and keep the rest, use [Remove an item from a cart](" + REMOVE_PAGE + ").",
        "parameters": [SESSION_ID],
        "responses": {
            "204": {"description": "The cart is empty. No body."},
            "400": {
                "description": "The cart has no items, for example because you already emptied it. The message is `Your shopping cart is empty`.",
                "schema": ERROR_REF,
                "example": EMPTY_CART,
            },
        },
        "example_call": {"path": {"session_id": SESSION}},
    },
    {
        "key": "delete_cart_item",
        "slug": "remove-an-item-from-a-cart",
        "title": "Remove an item from a cart",
        "method": "DELETE",
        "path": BASE + "/{session_id}/cart_items/{cart_item_id}",
        "summary": "Removes one item from the cart and returns `204` with no body.",
        "description": "Removes the cart item whose `id` you pass as `cart_item_id`, and returns `204` with no body. Take `cart_item_id` from `items[].id` in a cart response: the store numbers cart items across all carts, so do not count from `1`. Removing the last item empties the cart, so reading it afterwards returns `400` with the message `Your shopping cart is empty`.",
        "parameters": [SESSION_ID, CART_ITEM_ID],
        "responses": {
            "204": {"description": "The item is removed. No body."},
            "404": {
                "description": "The cart holds no item with that `cart_item_id`. The message is `f:cart item not found`.",
                "schema": ERROR_REF,
                "example": ITEM_NOT_FOUND,
            },
        },
        "example_call": {"path": {"session_id": SESSION, "cart_item_id": 42}},
    },
    {
        "key": "create_order_from_cart",
        "slug": "create-an-order-from-a-cart",
        "title": "Create an order from a cart",
        "method": "POST",
        "path": "/admin/orders/carts/{session_id}",
        "summary": "Turns the cart into an order, empties the cart and returns the new order.",
        "description": "Creates an order from the cart's items, empties the cart, and returns the order under `order` with `status` set to `success`. Send the customer's `customer_id`, not the `internal_id` that [Add a product to a cart](" + ADD_PAGE + ") takes; it is the only required field, and `payment_gateway` defaults to `PIS`. The new order has `order_status` `in_progress`, `payment_status` `unpaid`, and one `order_line_details` entry per cart item. It gets the customer's saved addresses unless you sent addresses to [Update a cart item](" + UPDATE_PAGE + ") with the same `JSESSIONID` cookie as this call.",
        "parameters": [SESSION_ID],
        "body": {"schema": ref("CartOrderInput"), "example": ORDER_BODY},
        "responses": {
            "201": {
                "description": "`status` is `success`, and `order` holds the new order. The response shows `transaction_no` as `null`, although the order stores the value you sent. The response has no `Location` header. The order stays in your store: no call in the Carts API deletes it, and while it is unpaid it does not lower the product's stock.",
                "schema": {"type": "object", "properties": {
                    "status": {"type": "string", "description": "`success`."},
                    "order": ref("CartOrder"),
                }},
                "example": {"status": "success", "order": SAMPLE_ORDER},
            },
            "400": {
                "description": "The body has no `customer_id`. The message is `No Customer Found`, and the cart stays as it was.",
                "schema": ERROR_REF,
                "example": NO_CUSTOMER,
            },
        },
        "example_call": {"path": {"session_id": SESSION}},
    },
]


def number(description=None):
    return {"type": "number", "description": description} if description else {"type": "number"}


def text(description=None):
    return {"type": "string", "description": description} if description else {"type": "string"}


ADDRESS_INPUT_REF = ref("CartAddressInput")
ORDER_ADDRESS_REF = ref("CartOrderAddress")
REFERENCE_REF = ref("CartReference")

SCHEMAS = {
    "Cart": {"type": "object", "properties": {
        "customer_id": {"type": ["integer", "null"], "description": "The customer's `internal_id`, as you sent it to [Add a product to a cart](" + ADD_PAGE + "). Only that call's response shows it: [Retrieve a cart](" + RETRIEVE_PAGE + ") and [Update a cart item](" + UPDATE_PAGE + ") return `null`."},
        "session_id": text("The cart's `session_id`. Pass it as the `session_id` path parameter in the other cart calls."),
        "currency_code": text("The currency of the cart's amounts, such as `AUD`."),
        "currency_symbol": text("The currency symbol, such as `$`."),
        "delivery_type": text("The cart's delivery type, such as `shipping`."),
        "totals": ref("CartTotals"),
        "shipping": ref("CartShipping"),
        "items": {"type": "array", "items": ref("CartItem"), "description": "The cart's items. Adding a product that is already in the cart raises that item's `quantity` instead of adding an entry."},
        "discount": ref("CartDiscount"),
        "messages": ref("CartMessages"),
    }},
    "CartTotals": {"type": "object", "properties": {
        "subtotal": number("The sum of each item's `quantity` times its `pricing.unit_price`. A discount shows in `discount`, not here."),
        "discount": number("The discount on the cart."),
        "shipping_discount": number(),
        "tax": number(),
        "total": number(),
        "grand_total": number(),
        "paid": number(),
    }},
    "CartShipping": {"type": "object", "properties": {
        "cost": number("The shipping cost."),
        "handling_fee": number("The handling fee."),
        "handling_tax": number("Tax on the handling fee. It depends on `shipping_address.country_code`, and is `0.0` when you sent no shipping address."),
        "shipping_tax": number("Tax on shipping. It depends on `shipping_address.country_code`, and is `0.0` when you sent no shipping address."),
        "total_tax": number(),
    }},
    "CartItem": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The cart item's `id`. Pass it as `cart_item_id` to update or remove the item. The store numbers cart items across all carts, so a cart's first item can have any `id`."},
        "quantity": {"type": "integer", "description": "How many of the product the cart holds."},
        "variations": {},
        "taxable": {"type": "boolean"},
        "shippable": {"type": "boolean"},
        "pricing": ref("CartItemPricing"),
        "product": ref("CartItemProduct"),
    }},
    "CartItemPricing": {"type": "object", "properties": {
        "unit_price": number("The price of one unit. `totals.subtotal` adds up `quantity` times this for every item."),
        "display_unit_price": number(),
        "total": number(),
        "discount": number(),
        "discount_tax": number(),
        "tax": number(),
    }},
    "CartItemProduct": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The product's `id`, which you sent as `product_id`."},
        "sku": text(),
        "base_price": number(),
        "available_stock": {"type": "integer", "description": "The product's stock, not the item's `quantity`."},
        "on_sale": {"type": "boolean"},
        "cost_price": number(),
        "sale_price": number(),
        "url": text(),
        "name": text(),
        "product_type": text(),
        "image_link": text(),
    }},
    "CartDiscount": {"type": "object", "properties": {
        "discount": number(),
        "order_discount": number(),
        "shipping_discount": number(),
        "discount_on_tax": number(),
        "discount_on_shipping_tax": number(),
    }},
    "CartMessages": {"type": "object", "properties": {
        "discount": ref("CartDiscountMessage"),
    }},
    "CartDiscountMessage": {"type": "object", "properties": {
        "message": text(),
        "status": {},
    }},
    "CartGroupMeta": {"type": "object", "properties": {
        "cart": ref("CartSectionMeta"),
    }, "description": "Returned only by [Retrieve a cart](" + RETRIEVE_PAGE + ")."},
    "CartSectionMeta": {"type": "object", "properties": {
        "kind": text("`resource`."),
        "writable": {"type": "boolean", "description": "`true`."},
        "href": text("`/api/v4/carts/{sessionId}`, with `{sessionId}` left as written rather than your cart's `session_id`."),
    }},
    "CartSession": {"type": "object", "properties": {
        "sessionId": text("The value to use as the cart's `session_id`. Only this call spells the field `sessionId`, in both the request body and the response."),
    }},
    "CartItemInput": {"type": "object", "properties": {
        "product_id": {"type": "integer", "description": "Required. The product's `id`."},
        "quantity": {"type": "integer", "description": "Required. How many to add. If the product is already in the cart, this raises that item's `quantity`."},
        "customer_id": {"type": "integer", "description": "Required. The customer's `internal_id`. The customer's `customer_id` is rejected with `400` and the message `No Customer Found`."},
        "session_id": text("The name you choose for the cart. Without it, the store uses your HTTP session's `JSESSIONID`, and `cart.session_id` in the response shows it."),
        "shipping_address": dict(ADDRESS_INPUT_REF, description="Sets the cart's shipping taxes. It never reaches an order made from the cart."),
    }, "required": ["product_id", "quantity", "customer_id"], "description": "Send these fields at the top level of the body."},
    "CartItemUpdateInput": {"type": "object", "properties": {
        "cart_item_id": {"type": "integer", "description": "Required. The cart item's `id`, from `items[].id`. Without it the call is rejected with `400` and the message `f:cart_item_id not found`."},
        "quantity": {"type": "integer", "minimum": 1, "description": "Required. The item's new quantity. `0` is rejected with `400`, and a body without `quantity` returns `500`."},
        "shipping_address": dict(ADDRESS_INPUT_REF, description="Sets the cart's shipping taxes. An order you create with the same `JSESSIONID` cookie gets this address."),
        "billing_address": dict(ADDRESS_INPUT_REF, description="An order you create with the same `JSESSIONID` cookie gets this address."),
    }, "required": ["cart_item_id", "quantity"], "description": "Send these fields at the top level of the body. Do not send `customer_id`: it returns `500`, although the new `quantity` is saved."},
    "CartAddressInput": {"type": "object", "properties": {
        "first_name": text(),
        "last_name": text(),
        "address_line1": text("The first address line. Spelled without an underscore before the `1`, unlike `address_line_1` in an order's address."),
        "address_line2": text("The second address line."),
        "city": text(),
        "post_code": text(),
        "phone": text(),
        "mobile": text(),
        "fax": text(),
        "email": text(),
        "country_code": text("A country code, such as `AU`. In `shipping_address`, it decides the cart's `shipping.shipping_tax` and `shipping.handling_tax`."),
        "state_code": text("A state code, such as `NSW`."),
    }, "description": "The store does not check any field, and accepts `{}`. No cart response returns the address."},
    "CartSessionInput": {"type": "object", "properties": {
        "sessionId": {"type": ["string", "null"], "description": "A value to get back as `sessionId`. `null` or `\"\"` returns your HTTP session's `JSESSIONID` instead: the cookie your client sends, or a new value when it sends none."},
    }, "description": "Send `{}` to get back the `session_id` from the path. A `session_id` key is ignored."},
    "CartOrderInput": {"type": "object", "properties": {
        "customer_id": {"type": "integer", "description": "Required. The customer's `customer_id`, not the `internal_id` that [Add a product to a cart](" + ADD_PAGE + ") takes."},
        "payment_gateway": text("The payment gateway. Defaults to `PIS`."),
        "delivery_type": text("The delivery type, such as `shipping`."),
        "transaction_no": text("A transaction number to store on the order. The response shows `transaction_no` as `null`."),
    }, "required": ["customer_id"], "description": "Send these fields at the top level of the body."},
    "CartOrder": {"type": "object", "properties": {
        "order_id": {"type": "integer", "description": "The new order's `order_id`, assigned by the store."},
        "internal_id": {"type": "integer", "description": "The order's `internal_id`. The customer's `internal_id` is in `customer_summary.internal_id`."},
        "order_no": {"type": "integer"},
        "transaction_no": {"type": ["string", "null"], "description": "`null` in this response, even when you sent `transaction_no`. The order stores the value you sent."},
        "currency_code": text(),
        "order_status": text("`in_progress` on an order made from a cart."),
        "payment_status": text("`unpaid` on an order made from a cart."),
        "shipping_status": text(),
        "sub_total": number(),
        "shipping_cost": number(),
        "shipping_tax": number("Tax on shipping. It follows the order's addresses, not the cart's `shipping.shipping_tax`."),
        "handling_cost": number(),
        "total_surcharge": number(),
        "total_discount": number(),
        "total_tax": number(),
        "grand_total": number(),
        "paid": number(),
        "due": number(),
        "items_total": {"type": "integer"},
        "ip_address": text(),
        "order_channel": {"description": "`null` on an order made from a cart."},
        "created_at": text(),
        "updated_at": text(),
        "customer_summary": dict(ref("CartOrderCustomer"), description="The customer the order belongs to, with both the customer's `customer_id` and `internal_id`."),
        "order_line_details": {"type": "array", "items": ref("CartOrderLine"), "description": "One entry per cart item."},
        "payments": {"type": "array", "items": ref("CartOrderPayment"), "description": "The order's payments. When you send `\"payment_gateway\": \"PIS\"` or leave `payment_gateway` out, this holds one `PIS` payment with `status` `awaiting`."},
        "external_reference_order_id": {"description": "`null` on an order made from a cart."},
        "external_reference_store_id": {"description": "`null` on an order made from a cart."},
        "external_reference_order_no": {"description": "`null` on an order made from a cart."},
        "external_reference_status": {"description": "`null` on an order made from a cart."},
        "external_reference_url": {"description": "`null` on an order made from a cart."},
        "customer_po_number": text(),
        "payment_term": text(),
        "fulfillment_mode": text(),
        "fulfillment_term": text(),
        "invoice_mode": text(),
        "billing_address": ORDER_ADDRESS_REF,
        "shipping_address": ORDER_ADDRESS_REF,
        "custom_fields": {"type": "array", "items": {}},
    }},
    "CartOrderCustomer": {"type": "object", "properties": {
        "first_name": text(),
        "last_name": text(),
        "customer_group": text(),
        "gender": {"type": ["string", "null"]},
        "customer_id": {"type": "integer", "description": "The customer's `customer_id`: the number [Create an order from a cart](" + ORDER_PAGE + ") takes."},
        "internal_id": {"type": "integer", "description": "The customer's `internal_id`: the number [Add a product to a cart](" + ADD_PAGE + ") takes."},
        "email": text(),
        "address_line_1": text(),
        "address_line_2": text(),
        "city": text(),
        "country": REFERENCE_REF,
        "state": REFERENCE_REF,
        "post_code": text(),
        "phone": text(),
        "mobile": text(),
        "fax": text(),
        "company_name": text(),
    }},
    "CartOrderLine": {"type": "object", "properties": {
        "item_id": {"type": "integer"},
        "product_name": text(),
        "product_id": {"type": "integer", "description": "The product's `id`, as in the cart item's `product.id`."},
        "sku": text(),
        "quantity": {"type": "integer", "description": "The cart item's `quantity`."},
        "price": number(),
        "total_amount": number(),
        "tax": number(),
        "discount": number(),
        "tax_discount": number(),
        "is_taxable": {"type": "boolean"},
        "is_shippable": {"type": "boolean"},
        "image_url": text(),
        "variations": {"type": "array", "items": {}},
        "serial_batch_number": text(),
    }},
    "CartOrderPayment": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The payment's `id`."},
        "status": text("`awaiting` on a new `PIS` payment."),
        "amount": number(),
        "payment_method": text("`PIS` when you send `\"payment_gateway\": \"PIS\"` or leave `payment_gateway` out."),
        "track_info": text(),
        "gateway_name": text(),
        "gateway_code": text("`PIS` when you send `\"payment_gateway\": \"PIS\"` or leave `payment_gateway` out."),
        "gateway_response": text(),
        "payer_info": text(),
        "paying_date": text(),
        "transaction_date": text(),
        "transaction_reference": text(),
    }},
    "CartOrderAddress": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The address's `id`."},
        "first_name": text(),
        "last_name": text(),
        "email": text(),
        "company_name": text(),
        "address_line_1": text(),
        "address_line_2": text(),
        "country": REFERENCE_REF,
        "state": REFERENCE_REF,
        "city": text(),
        "post_code": text(),
        "mobile": text(),
        "phone": text(),
        "fax": text(),
    }, "description": "The customer's saved address, unless you sent addresses to [Update a cart item](" + UPDATE_PAGE + ") with the same `JSESSIONID` cookie as [Create an order from a cart](" + ORDER_PAGE + "): then the address that update sent. Addresses you send to [Add a product to a cart](" + ADD_PAGE + ") never appear here."},
    "CartReference": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The country's or state's `id`."},
        "name": text("Such as `Australia`."),
        "code": text("Such as `AU`."),
    }, "description": "A country or a state. A state is `{}` when the address has none."},
    "CartError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": text("A machine-readable reason, such as `invalid_request`, `not_found` or `internal_error`."),
        "message": text("What went wrong, such as `Your shopping cart is empty`. Some messages start with `f:`, such as `f:cart item not found`."),
        "details": {"type": "array", "items": {}, "description": "An empty list."},
        "request_id": text("Identifies this request."),
    }}}},
}
