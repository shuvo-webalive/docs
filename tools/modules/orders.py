"""The Orders endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Orders"
SLUG = "orders"
BASE = "/admin/orders"
ICON = "receipt"

LIST_PAGE = "/api-reference/orders/list-orders"
COUNT_PAGE = "/api-reference/orders/count-orders"
CREATE_PAGE = "/api-reference/orders/create-an-order"
RETRIEVE_PAGE = "/api-reference/orders/retrieve-an-order"
UPDATE_PAGE = "/api-reference/orders/update-an-order"
PATCH_PAGE = "/api-reference/orders/update-selected-order-fields"
ADDRESSES_PAGE = "/api-reference/orders/update-an-orders-addresses"
ADD_COMMENT_PAGE = "/api-reference/orders/add-a-comment-to-an-order"
CUSTOM_FIELDS_PAGE = "/api-reference/orders/retrieve-an-orders-custom-fields"
PAYMENT_PAGE = "/api-reference/orders/record-a-payment-on-an-order"
ORDER_REFUND_PAGE = "/api-reference/orders/refund-an-order"
PAYMENT_REFUND_PAGE = "/api-reference/orders/refund-a-payment"
INVOICE_PAGE = "/api-reference/orders/send-an-orders-invoice"
SHIPMENTS_PAGE = "/api-reference/orders/list-an-orders-shipments"
CREATE_SHIPMENT_PAGE = "/api-reference/orders/create-a-shipment"
UPDATE_SHIPMENT_PAGE = "/api-reference/orders/update-a-shipment"
STATUS_PAGE = "/api-reference/orders/change-an-orders-status"
CUSTOM_STATUS_PAGE = "/api-reference/orders/add-a-custom-order-status"
CUSTOMER_ORDERS_PAGE = "/api-reference/orders/list-a-customers-orders"
CANCEL_PAGE = "/api-reference/orders/cancel-an-order"
WITH_PAYMENT_PAGE = "/api-reference/orders/create-an-order-with-a-payment"
ORDER_FLAGS_PAGE = "/api-reference/order-flags/list-order-flags"
ECOMMERCE_SETTINGS_PAGE = "/api-reference/ecommerce-settings/get-ecommerce-settings"

OVERVIEW_DESCRIPTION = "List, count, create, change, cancel and delete orders, add comments, record payments, refunds and shipments, and email invoices."
INTRO = (
    "The Orders API has 24 endpoints, and you can call every one from all seven SDKs. Most paths start with"
    " `/api/v4/admin/orders`; [Refund a payment](" + PAYMENT_REFUND_PAGE + ") uses `/api/v4/admin/payment`,"
    " [Add a custom order status](" + CUSTOM_STATUS_PAGE + ") uses `/api/v4/admin/order`, and"
    " [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + ") uses `/api/v4/admin/customers`."
)

WARNING = (
    "**Two paths take the order's `internal_id`, not its `order_id`.**\n"
    "  [Retrieve an order's custom fields](" + CUSTOM_FIELDS_PAGE + ") and [Send an order's invoice](" + INVOICE_PAGE + ")\n"
    "  find the order by its `internal_id`. If you pass an `order_id`, they return `404`, or, when another order\n"
    "  has that number as its `internal_id`, they return that order's custom fields or email that order's invoice.\n"
    "  Every other order path takes the `order_id`. Responses that return an order include both numbers."
)

NOTES = [
    "**An order comes back in one of two shapes.** [Retrieve an order](" + RETRIEVE_PAGE + "),\n"
    "  [List orders](" + LIST_PAGE + "), [Update an order](" + UPDATE_PAGE + ") and\n"
    "  [Update selected order fields](" + PATCH_PAGE + ") return it in sections: `customer`, `billing_address`,\n"
    "  `shipping_address`, `items`, `shipping`, `discounts`, `charges_totals`, `payments` and `fulfillment`.\n"
    "  The two create calls, [Cancel an order](" + CANCEL_PAGE + "), [Change an order's status](" + STATUS_PAGE + ") and\n"
    "  [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + ") return it flat: the totals and fulfillment fields at the\n"
    "  top level, the customer in `customer_summary` and the lines in `order_line_details`. A listing row has no\n"
    "  `billing_address` or `shipping_address`.",
    "**The customer filters take different customer numbers.** The `customerId` filter of\n"
    "  [List orders](" + LIST_PAGE + ") and [Count orders](" + COUNT_PAGE + ") takes the customer's `internal_id`, and the\n"
    "  customer's `customer_id` matches nothing there. [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + ") takes the\n"
    "  `customer_id`, and the customer's `internal_id` returns `404` there.",
    "**Every address you send replaces the whole stored address.** This holds when you create an order and in\n"
    "  [Update an order](" + UPDATE_PAGE + "), [Update selected order fields](" + PATCH_PAGE + ") and\n"
    "  [Update an order's addresses](" + ADDRESSES_PAGE + "): a field you leave out becomes `\"\"`. `company_name` is\n"
    "  never stored and always reads `\"\"`. An address without `first_name` returns `500` with the body `{}`, and on\n"
    "  an update an address without `country_code` returns `500` with the message\n"
    "  `Cannot get property 'id' on null object`. Send both in every address.",
    "**A listing returns at most 20 orders per call and leaves out cancelled orders.** A larger `limit` is capped\n"
    "  at `20`, and `pagination.limit` shows `20`. Send `page` or `offset` for the next orders; when you send both,\n"
    "  `offset` wins. Cancelled orders are listed only when you send `order_status=cancelled`, and\n"
    "  [Count orders](" + COUNT_PAGE + ") leaves them out too. A query parameter that is not on the\n"
    "  [List orders](" + LIST_PAGE + ") page, `q` included, is rejected with `400`.",
    "**Payments and refunds change different totals.** [Record a payment on an order](" + PAYMENT_PAGE + ") raises\n"
    "  `paid`. [Refund a payment](" + PAYMENT_REFUND_PAGE + ") lowers `paid` and raises `refunded`, and needs an\n"
    "  `Idempotency-Key` header. [Refund an order](" + ORDER_REFUND_PAGE + ") raises `refunded` and leaves `paid` as it was.",
    "**Shipping lowers stock, and deleting the order does not restore it.** [Create a shipment](" + CREATE_SHIPMENT_PAGE + ")\n"
    "  lowers the stock of a product that tracks its stock by the units shipped. Creating, paying, cancelling,\n"
    "  completing and deleting an order change no stock.",
]

ORDER_STATUSES = ["cancelled", "completed", "draft", "in_progress", "paused", "reopened"]
SORT_FIELDS = ["orderNo", "customerName", "created", "orderStatus", "paymentStatus", "shippingStatus", "deliveryType", "scheduledDate", "total", "items"]
PAYMENT_GATEWAYS = ["ACP", "API", "APY", "BDP", "CHQ", "COD", "CRD", "CRL", "EXC", "GCRD", "LPP", "MOR", "PAY_RIGHT", "PIS", "PPL", "SCR", "ZIP"]
DELIVERY_TYPES = ["delivery", "others_shipping", "shipping", "store_pickup"]


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ORDER_ID = {
    "name": "order_id",
    "in": "path",
    "required": True,
    "description": "The order's `order_id`, from a listing or from the response to creating the order. It equals the order's `order_no` and is not the order's `internal_id`.",
    "schema": {"type": "integer", "example": 1043},
}

ORDER_INTERNAL_ID = {
    "name": "order_internal_id",
    "in": "path",
    "required": True,
    "description": "The order's `internal_id`, from any response that returns the order. Do not pass the order's `order_id`: this path finds the order by `internal_id`, so an `order_id` returns `404` or reaches the order whose `internal_id` has that number.",
    "schema": {"type": "integer", "example": 2187},
}

PAYMENT_ID = {
    "name": "payment_id",
    "in": "path",
    "required": True,
    "description": "The payment's `id`, from `payment.id` in the response to [Record a payment on an order](" + PAYMENT_PAGE + ").",
    "schema": {"type": "integer", "example": 7712},
}

SHIPMENT_ID = {
    "name": "shipment_id",
    "in": "path",
    "required": True,
    "description": "The shipment's `shipping_id`, from the response to [Create a shipment](" + CREATE_SHIPMENT_PAGE + ") or from [List an order's shipments](" + SHIPMENTS_PAGE + ").",
    "schema": {"type": "integer", "example": 905},
}

CUSTOMER_ID = {
    "name": "customer_id",
    "in": "path",
    "required": True,
    "description": "The customer's `customer_id`. The customer's `internal_id` returns `404` with the message `Customer Not Found`.",
    "schema": {"type": "integer", "example": 512},
}

IDEMPOTENCY_KEY = {
    "name": "Idempotency-Key",
    "in": "header",
    "required": True,
    "description": "A value you choose for this refund, such as `refund-0001`. Without it the call is rejected with `400` and the reason `idempotency_key_required`. Sending the same value again returns the first refund again and refunds nothing more, so use a new value for each new refund.",
    "schema": {"type": "string", "example": "refund-0001"},
}


def query(name, description, schema):
    return {"name": name, "in": "query", "description": description, "schema": schema}


FILTERS = [
    query("customerId", "Keeps the orders of one customer. Send the customer's `internal_id`: the customer's `customer_id` matches nothing here.", {"type": "integer", "example": 88}),
    query("customerName", "Keeps orders whose customer name contains this text, in any letter case.", {"type": "string", "example": "doe"}),
    query("search_text", "Keeps orders whose customer's email address matches this text.", {"type": "string", "example": "jane.doe@example.com"}),
    query("order_status", "Keeps orders with this status. Cancelled orders are listed only when you send `cancelled`. A value outside this list, such as a custom status from [Add a custom order status](" + CUSTOM_STATUS_PAGE + "), is rejected. `orderStatus` and `status` are other names for this parameter.", {"type": "string", "enum": ORDER_STATUSES, "example": "in_progress"}),
    query("payment_status", "Keeps orders with this payment status, such as `unpaid` or `partial`. `paymentStatus` is another name for this parameter.", {"type": "string", "example": "unpaid"}),
    query("shipping_status", "Keeps orders with this shipping status. Send `not_shipped` for orders with no shipment. `shippingStatus` is another name for this parameter.", {"type": "string", "example": "not_shipped"}),
    query("total", "Keeps orders whose total matches this amount.", {"type": "number", "example": 40.0}),
    query("gatewayCode", "Keeps orders that use this payment gateway code, such as `PIS`.", {"type": "string", "example": "PIS"}),
    query("currency_code", "Keeps orders in this currency, in any letter case. `currencyCode` is another name for this parameter.", {"type": "string", "example": "AUD"}),
    query("productId", "Keeps orders with a line for this product, by the `product_id` the order's lines show.", {"type": "integer", "example": 101}),
    query("productName", "Keeps orders with a line for a product of this name.", {"type": "string", "example": "Cotton T-Shirt"}),
    query("productSku", "Keeps orders with a line for a product with this SKU.", {"type": "string", "example": "TSHIRT-001"}),
    query("orderFrom", "Keeps orders created from this date, written `YYYY-MM-DD`.", {"type": "string", "format": "date", "example": "2026-10-01"}),
    query("orderTo", "Keeps orders created up to this date, written `YYYY-MM-DD`.", {"type": "string", "format": "date", "example": "2026-10-31"}),
    query("order_id", "Keeps the order with this `order_id`. `orderId` is another name for this parameter.", {"type": "integer", "example": 1043}),
    query("order_no", "Keeps the order with this `order_no`.", {"type": "integer", "example": 1043}),
    query("orderIds", "Keeps the order with this `internal_id`. The order's `order_id` matches nothing here.", {"type": "integer", "example": 2187}),
    query("externalReferenceOrderId", "Keeps orders with this `external_reference_order_id`. `external_reference_order_id` is another name for this parameter.", {"type": "string", "example": "EXT-0001"}),
    query("flag", "Keeps orders that have this order flag. Send the flag's `id` from [List order flags](" + ORDER_FLAGS_PAGE + "). Orders with no flag are left out, and no Orders endpoint puts a flag on an order.", {"type": "integer", "example": 3}),
]

SORT = query("sort", "Sorts the orders by this field. Without it, the newest order comes first. `id` is accepted and keeps the default order; any other value is rejected with `400` and the reason `invalid_sort_field`.", {"type": "string", "enum": SORT_FIELDS, "example": "total"})
DIR = query("dir", "The sort direction: `asc` or `desc`. Sent without `sort`, it changes the direction of the default order.", {"type": "string", "enum": ["asc", "desc"], "example": "asc"})
LIMIT = query("limit", "Orders per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`.", {"type": "integer", "minimum": 1, "maximum": 20, "example": 20})
PAGE = query("page", "The page to return, counting from `1`, at the page size applied: `limit=1&page=2` skips one order. When you also send `offset`, `offset` wins, even `offset=0`.", {"type": "integer", "minimum": 1, "example": 1})
OFFSET = query("offset", "Number of orders to skip.", {"type": "integer", "minimum": 0, "example": 0})
FIELD_METADATA = query("field_metadata", "Send `true` or `1` to add `field_metadata`, which describes every order field. `false` adds nothing.", {"type": "boolean", "example": True})

ERROR_REF = ref("OrderError")
FLAT_ERROR_REF = ref("OrderFlatError")
EMPTY_BODY = {"type": "object", "description": "An empty object, `{}`."}

ADDRESS_500 = {
    "description": "An address has no `first_name`, and the body is `{}`. Or, on this update, an address has no `country_code`: the reason is `internal_error` and the message `Cannot get property 'id' on null object`. Send `first_name` and `country_code` in every address.",
    "schema": {"anyOf": [EMPTY_BODY, ERROR_REF]},
}

AUSTRALIA = {"id": 13, "name": "Australia", "code": "AU"}
VICTORIA = {"id": 7, "name": "Victoria", "code": "VIC"}

ADDRESS_INPUT = {
    "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com",
    "address_line_1": "1 Example Street", "address_line_2": "Level 2", "city": "Melbourne",
    "post_code": "3000", "phone": "0300000000", "mobile": "0400000000",
    "country_code": "AU", "state_code": "VIC",
}
NEW_ADDRESS_INPUT = dict(ADDRESS_INPUT, address_line_1="10 Example Street")

BILLING = {
    "id": 9001, "first_name": "Jane", "last_name": "Doe", "email": "jane.doe@example.com", "company_name": "",
    "address_line_1": "1 Example Street", "address_line_2": "Level 2", "country": AUSTRALIA, "state": VICTORIA,
    "city": "Melbourne", "post_code": "3000", "mobile": "0400000000", "phone": "0300000000", "fax": "",
}
SHIPPING_ADDRESS = dict(BILLING, id=9002)
NEW_BILLING = dict(BILLING, address_line_1="10 Example Street")
NEW_SHIPPING_ADDRESS = dict(SHIPPING_ADDRESS, address_line_1="10 Example Street")

CUSTOMER = {
    "first_name": "Jane", "last_name": "Doe", "customer_group": None, "gender": None,
    "customer_id": 512, "internal_id": 88, "email": "jane.doe@example.com",
    "address_line_1": "1 Example Street", "address_line_2": "Level 2", "city": "Melbourne",
    "country": AUSTRALIA, "state": VICTORIA, "post_code": "3000", "phone": "0300000000",
    "mobile": "0400000000", "fax": "", "company_name": "",
}
LISTED_CUSTOMER = {"customer_id": 512, "internal_id": 88, "first_name": "Jane", "last_name": "Doe", "customer_group": None}

SHIRT = {
    "item_id": 3301, "product_name": "Cotton T-Shirt", "product_id": 101, "sku": "TSHIRT-001", "quantity": 1,
    "price": 25.0, "total_amount": 25.0, "tax": 0.0, "discount": 0.0, "tax_discount": 0.0,
    "is_taxable": False, "is_shippable": True, "image_url": None, "variations": [], "serial_batch_number": None,
}
TOTE = dict(SHIRT, item_id=3302, product_name="Canvas Tote Bag", product_id=102, sku="TOTE-001", price=15.0, total_amount=15.0)
ITEMS = [SHIRT, TOTE]
CREATED_ITEMS = [dict(SHIRT, variations=None), dict(TOTE, variations=None)]

PIS_PAYMENT = {
    "id": 7701, "status": "awaiting", "amount": 40.0, "payment_method": None, "track_info": None,
    "gateway_name": None, "gateway_code": "PIS", "payer_info": None, "paying_date": None,
    "transaction_date": None, "transaction_reference": None,
}
FLAT_PIS_PAYMENT = dict(PIS_PAYMENT, gateway_response=None)
API_PAYMENT = {
    "id": 7702, "status": "success", "amount": 20.0, "payment_method": "API", "track_info": "Paid at the counter",
    "gateway_name": None, "gateway_code": "API", "gateway_response": None, "payer_info": "", "paying_date": None,
    "transaction_date": "2026-10-07T09:15:02Z", "transaction_reference": "",
}

FULFILLMENT = {
    "fulfillment_mode": None, "fulfillment_term": None, "invoice_mode": None, "payment_term": None,
    "customer_po_number": None, "external_reference_order_id": None, "external_reference_store_id": None,
    "external_reference_order_no": None, "external_reference_status": None, "external_reference_url": None,
    "custom_fields": [],
}

ORDER = {
    "order_id": 1043, "order_no": 1043, "internal_id": 2187, "order_status": "in_progress",
    "payment_status": "unpaid", "shipping_status": "not_shipped", "currency_code": "AUD",
    "transaction_no": "TXN-ORDER-0001", "ip_address": "203.0.113.10",
    "created_on": "2026-10-07T09:15:02Z", "last_updated_on": "2026-10-07T09:15:02Z",
    "customer": CUSTOMER,
    "billing_address": BILLING,
    "shipping_address": SHIPPING_ADDRESS,
    "items": ITEMS,
    "shipping": {"delivery_type": "shipping", "shipping_type": None, "shipping_status": "not_shipped", "shipping_cost": 0.0, "shipping_tax": 0.0},
    "discounts": {"total_discount": 0.0, "coupon_code": None, "gift_card_code": None},
    "charges_totals": {
        "sub_total": 40.0, "total_tax": 0.0, "handling_cost": 0.0, "total_surcharge": 0.0, "other_charges": 0.0,
        "grand_total": 40.0, "paid": 0.0, "due": 40.0, "refunded": 0.0, "refund_status": None, "items_total": 2,
    },
    "payments": [PIS_PAYMENT],
    "fulfillment": FULFILLMENT,
}

LISTED_ORDER = {key: value for key, value in ORDER.items() if key not in ("billing_address", "shipping_address")}
LISTED_ORDER["customer"] = LISTED_CUSTOMER
OLDER_LISTED_ORDER = dict(
    LISTED_ORDER, order_id=1042, order_no=1042, internal_id=2186, transaction_no="TXN-ORDER-0000",
    created_on="2026-10-06T16:40:11Z", last_updated_on="2026-10-06T16:40:11Z",
)

UPDATED_ORDER = dict(ORDER, billing_address=NEW_BILLING, last_updated_on="2026-10-07T10:02:44Z")
PATCHED_ORDER = dict(
    ORDER, last_updated_on="2026-10-07T10:05:18Z",
    fulfillment=dict(FULFILLMENT, customer_po_number="PO-0001", payment_term="NET30"),
)

FLAT_ORDER = {
    "order_id": 1043, "order_no": 1043, "internal_id": 2187, "transaction_no": "TXN-ORDER-0001",
    "currency_code": "AUD", "order_status": "in_progress", "payment_status": "unpaid", "shipping_status": "unshipped",
    "sub_total": 40.0, "shipping_cost": 0.0, "shipping_tax": 0.0, "handling_cost": 0.0, "total_surcharge": 0.0,
    "total_discount": 0.0, "total_tax": 0.0, "grand_total": 40.0, "paid": 0.0, "due": 40.0, "items_total": 2,
    "ip_address": "203.0.113.10", "created_at": "2026-10-07T09:15:02Z", "updated_at": "2026-10-07T09:15:02Z",
    "customer_summary": CUSTOMER,
    "order_line_details": CREATED_ITEMS,
    "payments": [FLAT_PIS_PAYMENT],
    "external_reference_order_id": None, "external_reference_store_id": None, "external_reference_order_no": None,
    "external_reference_status": None, "external_reference_url": None,
    "customer_po_number": None, "payment_term": None, "fulfillment_mode": None, "fulfillment_term": None,
    "invoice_mode": None,
    "billing_address": BILLING,
    "shipping_address": SHIPPING_ADDRESS,
    "custom_fields": [],
}
PAID_FLAT_ORDER = dict(
    FLAT_ORDER, transaction_no=None, payment_status="partial", paid=20.0, due=20.0, payments=[API_PAYMENT],
)
CANCELLED_FLAT_ORDER = dict(FLAT_ORDER, order_line_details=ITEMS, order_status="cancelled", updated_at="2026-10-07T11:20:31Z")
PAUSED_FLAT_ORDER = dict(FLAT_ORDER, order_line_details=ITEMS, order_status="paused", updated_at="2026-10-07T11:22:05Z")
CUSTOMER_FLAT_ORDER = dict(FLAT_ORDER, order_line_details=ITEMS)

SECTION_META = {"kind": "section", "writable": True}
PAYMENTS_META = dict(SECTION_META, href="/api/v4/admin/orders/{id}/payments")
ADDRESS_META = dict(SECTION_META, href="/api/v4/admin/orders/{id}/addresses")
LIST_GROUP_META = {
    "customer": SECTION_META, "items": SECTION_META, "shipping": SECTION_META, "discounts": SECTION_META,
    "charges_totals": dict(SECTION_META, writable=False), "payments": PAYMENTS_META, "fulfillment": SECTION_META,
}
ORDER_GROUP_META = {
    "customer": SECTION_META, "billing_address": ADDRESS_META, "shipping_address": ADDRESS_META,
    "items": SECTION_META, "shipping": SECTION_META, "discounts": SECTION_META,
    "charges_totals": dict(SECTION_META, writable=False), "payments": PAYMENTS_META, "fulfillment": SECTION_META,
}

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

COMMENT = {"id": 4410, "content": "Called to confirm the address.", "admin_name": "Store Admin", "visible_to_customer": False, "admin": True, "created": "10/7/2026  14:05:09"}
OLDER_COMMENT = dict(COMMENT, id=4402, content="Customer asked about delivery times.", created="10/7/2026  09:41:27")

SHIPPED_SHIRT = {
    "order_item_id": 3301, "product_id": 101, "product_name": "Cotton T-Shirt", "product_sku": "TSHIRT-001",
    "shipping_class": None, "order_quantity": 1, "shipped_quantity": 1, "total_amount": 25.0,
}
SHIPMENT = {
    "shipping_id": 905, "order_id": 1043, "order_internal_id": 2187, "customer_id": 512, "customer_internal_id": 88,
    "order_address_id": None, "date_created": "2026-10-08T08:00:00", "tracking_number": "TRACK-0001",
    "shipping_method": "Example Courier", "shipping_address": SHIPPING_ADDRESS, "billing_address": BILLING,
    "items": [SHIPPED_SHIRT],
}
UPDATED_SHIPMENT = dict(SHIPMENT, tracking_number="TRACK-0002")

ORDER_RESPONSE = {"type": "object", "properties": {"order": ref("Order")}}
FLAT_ORDER_RESPONSE = {"type": "object", "properties": {"order": ref("OrderFlat")}}
CREATED_ORDER_RESPONSE = {"type": "object", "properties": {
    "order": ref("OrderFlat"),
    "status": {"type": "string", "description": "`success`."},
}}
SHIPMENT_RESPONSE = {"type": "object", "properties": {
    "shipment": ref("OrderShipment"),
    "status": {"type": "string", "description": "`success`."},
}}


def wrapped(name, description):
    return {"type": "object", "description": description, "properties": {"order": ref(name)}}


ENDPOINTS = [
    {
        "key": "list_orders",
        "slug": "list-orders",
        "title": "List orders",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 orders per call, newest first, leaving out cancelled orders.",
        "description": "Returns the orders newest first, up to 20 per call, with a `pagination` block and a `group_meta` block. Cancelled orders are left out unless you send `order_status=cancelled`. Each filter narrows the list to the orders that match it, and any query parameter not listed here, `q` included, is rejected with `400`. A row has every section except `billing_address` and `shipping_address`, and its `customer` has only `customer_id`, `internal_id`, `first_name`, `last_name` and `customer_group`.",
        "parameters": FILTERS + [SORT, DIR, LIMIT, PAGE, OFFSET, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The orders on this page in `orders`, the paging details in `pagination`, and `group_meta` with an entry for each of the seven sections a row has. With `field_metadata=true` or `1`, `field_metadata` is added. `next_page` is a full URL, or `null` on the last page, and `previous_page` is `null` on the first page. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "orders": {"type": "array", "items": ref("Order")},
                    "pagination": ref("OrderPagination"),
                    "group_meta": ref("OrderGroupMeta"),
                    "field_metadata": ref("OrderFieldMetadata"),
                }},
                "example": {"orders": [LISTED_ORDER, OLDER_LISTED_ORDER], "pagination": SAMPLE_PAGINATION, "group_meta": LIST_GROUP_META},
            },
            "400": {
                "description": "You sent a query parameter the listing does not accept: the message is `unknown query parameter(s): <name>` and the reason `unknown_parameter`. Or `sort` is not one of the listed values (reason `invalid_sort_field`), or you sent `limit=0` (message `'limit' must be a positive integer`).",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "order_status=in_progress&payment_status=unpaid&limit=10"},
    },
    {
        "key": "count_orders",
        "slug": "count-orders",
        "title": "Count orders",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of orders that match the listing's filters, leaving out cancelled orders.",
        "description": "Returns the number of orders as `count`, inside an `orders` object. It takes the same filters as [List orders](" + LIST_PAGE + "), and for the same filters it equals that listing's `pagination.total`. Cancelled orders are left out. `limit`, `page`, `sort`, `dir` and `field_metadata` are accepted and change nothing, and any other query parameter is rejected with `400`.",
        "parameters": FILTERS,
        "responses": {
            "200": {
                "description": "The number of orders that match, as `orders.count`.",
                "schema": {"type": "object", "properties": {"orders": {"type": "object", "properties": {"count": {"type": "integer"}}}}},
                "example": {"orders": {"count": 2}},
            },
            "400": {"description": "You sent a query parameter other than the filters listed here and `limit`, `page`, `sort`, `dir` and `field_metadata`.", "schema": ERROR_REF},
        },
        "example_call": {"query": "customerId=88&payment_status=unpaid"},
    },
    {
        "key": "create_order",
        "slug": "create-an-order",
        "title": "Create an order",
        "method": "POST",
        "path": BASE,
        "summary": "Creates an order for the products you send and returns it with its `order_id`.",
        "description": "Send the fields at the top level of the body, not wrapped in `order`; only `products` is required, each line with a `product_id` and a `quantity`. Without `customer_id` the order is a guest order; `payment_gateway` defaults to `PIS` (pay in store), and `delivery_type` defaults to `shipping`. The new order is `in_progress` and `unpaid`, and with `PIS` its `payments` holds one `awaiting` payment for the grand total. A `transaction_no` another order already has creates a second order: the store does not check it for duplicates.",
        "body": {"schema": ref("OrderInput"), "example": {
            "customer_id": 512, "payment_gateway": "PIS", "delivery_type": "shipping", "is_send_email": False,
            "transaction_no": "TXN-ORDER-0001", "billing_address": ADDRESS_INPUT, "shipping_address": ADDRESS_INPUT,
            "products": [{"product_id": 101, "quantity": 1}, {"product_id": 102, "quantity": 1}],
        }},
        "responses": {
            "201": {
                "description": "The new order in the flat shape under `order`, with `\"status\": \"success\"` beside it. `order_no` equals `order_id`, and `internal_id` is a different number. In this response `shipping_status` is `unshipped` and each line's `variations` is `null`; [Retrieve an order](" + RETRIEVE_PAGE + ") shows `not_shipped` and `[]` for the same order. The response has no `Location` header.",
                "schema": CREATED_ORDER_RESPONSE,
                "example": {"order": FLAT_ORDER, "status": "success"},
            },
            "400": {
                "description": "`products` is missing (message `invalid.arguments`); the body has a field this call does not accept (reason `unknown_field`, message `is not a recognised order field`); or `payment_gateway` or `delivery_type` is not one of the listed values, such as `PAY_IN_STORE` or `SHIPPING` (reason `invalid_value`).",
                "schema": ERROR_REF,
            },
            "422": {"description": "`discounts.coupon_code` is not a code any discount has. The reason is `unprocessable` and the message `Invalid Code`.", "schema": ERROR_REF},
            "500": {"description": "An address has no `first_name`, and the body is `{}`. Send `first_name` in every address.", "schema": EMPTY_BODY, "example": {}},
        },
        "example_call": {},
    },
    {
        "key": "create_order_with_payment",
        "slug": "create-an-order-with-a-payment",
        "title": "Create an order with a payment",
        "method": "POST",
        "path": BASE + "/with-payment",
        "summary": "Creates an order and records one payment on it, returning the order with `paid` and `due`.",
        "description": "Send the same fields as [Create an order](" + CREATE_PAGE + ") plus a `payment` record, which is required; `customer` and `customer_id` both name the customer. The store files the payment under gateway `API` with `payment_method` `API`, whatever you send: it keeps `amount` and `track_info`, stores `payer_info` and `transaction_reference` as `\"\"`, and sets `transaction_date` to the time of the call. The order's own `transaction_no` and `external_reference_order_id` are accepted and not stored.",
        "body": {"schema": ref("OrderWithPaymentInput"), "example": {
            "customer_id": 512, "payment_gateway": "PIS", "delivery_type": "shipping",
            "billing_address": ADDRESS_INPUT, "shipping_address": ADDRESS_INPUT,
            "products": [{"product_id": 101, "quantity": 1}, {"product_id": 102, "quantity": 1}],
            "payment": {"amount": 20.0, "status": "success", "payment_method": "manual", "track_info": "Paid at the counter"},
        }},
        "responses": {
            "201": {
                "description": "The new order in the flat shape under `order`, with `\"status\": \"success\"` beside it. `paid` is the payment's `amount`, `due` is the rest of the grand total, and `payments` holds the one payment.",
                "schema": CREATED_ORDER_RESPONSE,
                "example": {"order": PAID_FLAT_ORDER, "status": "success"},
            },
            "400": {"description": "`payment` is missing. The message is `Payment information is required`.", "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_order",
        "slug": "retrieve-an-order",
        "title": "Retrieve an order",
        "method": "GET",
        "path": BASE + "/{order_id}",
        "summary": "Returns the order whose `order_id` you pass, with its addresses, lines, totals and payments.",
        "description": "Returns the order under `order` in sections: `customer`, `billing_address`, `shipping_address`, `items`, `shipping`, `discounts`, `charges_totals`, `payments` and `fulfillment`, beside eleven top-level fields. A `group_meta` block beside it has an entry for each of the nine sections. Send `field_metadata=true` or `1` to add a description of every field; any other query parameter is ignored. The response has no `ETag` header.",
        "parameters": [ORDER_ID, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The order in sections and `group_meta`. Every field a listing row has matches the row. With `field_metadata=true` or `1`, `field_metadata` is added.",
                "schema": {"type": "object", "properties": {
                    "order": ref("Order"),
                    "group_meta": ref("OrderGroupMeta"),
                    "field_metadata": ref("OrderFieldMetadata"),
                }},
                "example": {"order": ORDER, "group_meta": ORDER_GROUP_META},
            },
            "404": {"description": "No order has that `order_id`. The reason is `not_found` and the message `Order Not Found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "update_order",
        "slug": "update-an-order",
        "title": "Update an order",
        "method": "PUT",
        "path": BASE + "/{order_id}",
        "summary": "Changes an order's customer or addresses and keeps everything you leave out.",
        "description": "Send `customer_id`, or a `customer` record with a `customer_id`, to move the order to that customer, and `billing_address` or `shipping_address` to replace that address. Sections you leave out keep their values, so this call merges rather than replaces. Wrap the fields in `order` or send them at the top level; `items` is rejected with `400` and the reason `not_implemented`, and any other field with the reason `unknown_field`. An address you send replaces the stored one, so a field you leave out becomes `\"\"`.",
        "parameters": [ORDER_ID],
        "body": {"schema": wrapped("OrderUpdateInput", "Wrap the fields in `order`, or send the same fields at the top level."), "example": {"order": {"billing_address": NEW_ADDRESS_INPUT}}},
        "responses": {
            "200": {
                "description": "The order in sections under `order`, after the change. `{\"order\": {}}` returns `200` and changes nothing.",
                "schema": ORDER_RESPONSE,
                "example": {"order": UPDATED_ORDER},
            },
            "400": {
                "description": "`items` is in the body (reason `not_implemented`); a field other than `customer`, `customer_id`, `billing_address` and `shipping_address` is in the body (reason `unknown_field`); or the body is `{}` (message `request body must be a non-empty JSON object`).",
                "schema": ERROR_REF,
            },
            "500": ADDRESS_500,
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "patch_order",
        "slug": "update-selected-order-fields",
        "title": "Update selected order fields",
        "method": "PATCH",
        "path": BASE + "/{order_id}",
        "summary": "Changes the order fields you send: status, addresses, purchase order number or payment term.",
        "description": "Send any of `order_status`, `billing_address`, `shipping_address`, `customer_po_number` and `payment_term`, wrapped in `order` or at the top level; only those fields change, and any other field is rejected with `400` and the reason `unknown_field`. Inside the `order` wrapper you can also send `customer_po_number` and `payment_term` in a `fulfillment` record; a top-level `fulfillment` key is rejected with `400`. `order_status` takes `cancelled`, `completed`, `draft`, `in_progress`, `paused` or `reopened`. An address you send replaces the stored one, so a field you leave out becomes `\"\"`.",
        "parameters": [ORDER_ID],
        "body": {"schema": wrapped("OrderPatchInput", "Wrap the fields in `order`, or send them at the top level. `fulfillment` is accepted only inside the `order` wrapper."), "example": {"order": {"customer_po_number": "PO-0001", "payment_term": "NET30"}}},
        "responses": {
            "200": {
                "description": "The order in sections under `order`, after the change.",
                "schema": ORDER_RESPONSE,
                "example": {"order": PATCHED_ORDER},
            },
            "400": {
                "description": "A field other than the five listed is in the body (reason `unknown_field`), or `fulfillment` is sent at the top level.",
                "schema": ERROR_REF,
            },
            "500": ADDRESS_500,
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "delete_order",
        "slug": "delete-an-order",
        "title": "Delete an order",
        "method": "DELETE",
        "path": BASE + "/{order_id}",
        "summary": "Deletes an order permanently. An unknown `order_id` also returns `200`, with `status` `not_found`.",
        "description": "Deletes the order permanently and returns `\"status\": \"deleted\"` with the order's `order_id` and `internal_id`. Retrieving the order afterwards returns `404`, and [Count orders](" + COUNT_PAGE + ") goes down by one. When no order has that `order_id`, for example because you already deleted it, the call still returns `200`, with `\"status\": \"not_found\"`, so read `status` rather than the HTTP status. Stock that the order's shipments took is not given back.",
        "parameters": [ORDER_ID],
        "responses": {
            "200": {
                "description": "`status` is `deleted`, with the deleted order's `order_id` and `internal_id`. When no order has that `order_id`, `status` is `not_found` and the body is `{\"status\": \"not_found\", \"order_id\": 1043}`.",
                "schema": {"type": "object", "properties": {
                    "status": {"type": "string", "enum": ["deleted", "not_found"], "description": "`deleted`, or `not_found` when no order has that `order_id`."},
                    "order_id": {"type": "integer", "description": "The `order_id` you passed."},
                    "internal_id": {"type": "integer", "description": "The deleted order's `internal_id`. Not present when `status` is `not_found`."},
                }},
                "example": {"status": "deleted", "order_id": 1043, "internal_id": 2187},
            },
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "update_order_addresses",
        "slug": "update-an-orders-addresses",
        "title": "Update an order's addresses",
        "method": "PATCH",
        "path": BASE + "/{order_id}/addresses",
        "summary": "Replaces one or both of an order's addresses and returns both as they now stand.",
        "description": "Send `billing_address`, `shipping_address` or both at the top level of the body; an address you leave out does not change. Each address you send replaces the stored one, so a field you leave out becomes `\"\"`. Name the country and state with `country_code` and `state_code`, or with `country` and `state` records that hold their `id`. A body with neither address, or with the addresses wrapped in `order`, is rejected with `400`.",
        "parameters": [ORDER_ID],
        "body": {"schema": ref("OrderAddressesInput"), "example": {"transaction_no": "TXN-ADDR-0001", "shipping_address": NEW_ADDRESS_INPUT}},
        "responses": {
            "200": {
                "description": "The order's `order_id` and `internal_id`, and both addresses as they now stand.",
                "schema": ref("OrderAddresses"),
                "example": {"order_id": 1043, "internal_id": 2187, "billing_address": BILLING, "shipping_address": NEW_SHIPPING_ADDRESS},
            },
            "400": {"description": "Neither address is in the body, or the addresses are wrapped in `order`. The message is `billing_address or shipping_address is required`.", "schema": ERROR_REF},
            "500": {
                "description": "An address has no `first_name`, and the body is `{}`. Or an address has neither `country_code` nor a `country` record: the reason is `internal_error` and the message `Cannot get property 'id' on null object`. Send `first_name` and the country in every address.",
                "schema": {"anyOf": [EMPTY_BODY, ERROR_REF]},
            },
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "cancel_order",
        "slug": "cancel-an-order",
        "title": "Cancel an order",
        "method": "POST",
        "path": BASE + "/{order_id}/cancel",
        "summary": "Cancels an order and returns it with `order_status` set to `cancelled`.",
        "description": "Cancels the order and returns it in the flat shape with `order_status` set to `cancelled`; the body is optional, and a request with no body or `{}` cancels too. A cancelled order no longer appears in [Count orders](" + COUNT_PAGE + ") or [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + "), or in [List orders](" + LIST_PAGE + ") unless you send `order_status=cancelled`. You can cancel a completed order, and [Change an order's status](" + STATUS_PAGE + ") can move a cancelled order back. Cancelling an order that is already cancelled is rejected with `409`.",
        "parameters": [ORDER_ID],
        "body": {"schema": ref("OrderCancelInput"), "example": {"reason": "Customer asked to cancel", "refund_automatically": False, "is_gateway_refund": False}},
        "responses": {
            "201": {
                "description": "The cancelled order in the flat shape under `order`. There is no `status` key beside it.",
                "schema": FLAT_ORDER_RESPONSE,
                "example": {"order": CANCELLED_FLAT_ORDER},
            },
            "409": {"description": "The order is already cancelled. The reason is `conflict` and the message `order <n> is already cancelled`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "list_order_comments",
        "slug": "list-an-orders-comments",
        "title": "List an order's comments",
        "method": "GET",
        "path": BASE + "/{order_id}/comments",
        "summary": "Returns all of an order's comments, oldest first, in one list.",
        "description": "Returns every comment on the order under `comments`, oldest first, without paging. An order with no comments returns `\"comments\": []`. Each comment matches the response to [Add a comment to an order](" + ADD_COMMENT_PAGE + "), and `limit` is ignored.",
        "parameters": [ORDER_ID],
        "responses": {
            "200": {
                "description": "The order's comments, oldest first.",
                "schema": {"type": "object", "properties": {"comments": {"type": "array", "items": ref("OrderComment")}}},
                "example": {"comments": [OLDER_COMMENT, COMMENT]},
            },
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "create_order_comment",
        "slug": "add-a-comment-to-an-order",
        "title": "Add a comment to an order",
        "method": "POST",
        "path": BASE + "/{order_id}/comments",
        "summary": "Adds a comment to an order and returns it.",
        "description": "Send `content` at the top level of the body; a body wrapped in `comment` is rejected with `400` and the message `content: must not be empty`. `\"save_and_send\": true` sets the comment's `visible_to_customer` to `true`, and `false` leaves it `false`. The comment is returned under `comment` with `admin` set to `true`, and its `created` time is written `M/D/YYYY`, two spaces and a time, not ISO 8601.",
        "parameters": [ORDER_ID],
        "body": {"schema": ref("OrderCommentInput"), "example": {"content": "Called to confirm the address.", "save_and_send": False}},
        "responses": {
            "201": {
                "description": "The new comment under `comment`.",
                "schema": {"type": "object", "properties": {"comment": ref("OrderComment")}},
                "example": {"comment": COMMENT},
            },
            "400": {"description": "`content` is missing, for example because the body is wrapped in `comment`. The message is `content: must not be empty`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "get_order_custom_fields",
        "slug": "retrieve-an-orders-custom-fields",
        "title": "Retrieve an order's custom fields",
        "method": "GET",
        "path": BASE + "/{order_internal_id}/custom_fields",
        "summary": "Returns the custom field values of the order whose `internal_id` you pass.",
        "description": "Pass the order's `internal_id`, not its `order_id`: this path finds the order by `internal_id`, so an `order_id` returns `404` or the custom fields of the order whose `internal_id` has that number. The response's `order_id` field holds the `internal_id` you passed, and `custom_fields` lists the order's custom field values. An order with `delivery_type` `delivery` also returns `delivery_cost`.",
        "parameters": [ORDER_INTERNAL_ID],
        "responses": {
            "200": {
                "description": "The order's custom field values.",
                "schema": ref("OrderCustomFields"),
                "example": {"order_id": 2187, "custom_fields": []},
            },
            "404": {"description": "No order has that `internal_id`. The message is `Order not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_internal_id": 2187}},
    },
    {
        "key": "create_order_payment",
        "slug": "record-a-payment-on-an-order",
        "title": "Record a payment on an order",
        "method": "POST",
        "path": BASE + "/{order_id}/payments",
        "summary": "Records a payment on an order and returns a receipt whose `id` is the payment's `payment_id`.",
        "description": "Wrap the payment in `payment`, with `transaction_no` beside the wrapper if you send it; `payment_method` is required. The receipt's `id` is the `payment_id` that [Refund a payment](" + PAYMENT_REFUND_PAGE + ") takes. The order's `paid` rises by the amount, a payment for part of the total sets `payment_status` to `partial`, and the `awaiting` payment an order created with `PIS` starts with stays in the order's `payments` beside the new payment. `transaction_date` and `transaction_reference` are returned as you sent them.",
        "parameters": [ORDER_ID],
        "body": {
            "schema": {"type": "object", "required": ["payment"], "properties": {
                "payment": ref("OrderPaymentInput"),
                "transaction_no": {"type": "string", "description": "Your reference for this call. Send it beside `payment`, not inside it."},
            }},
            "example": {"transaction_no": "TXN-PAY-0001", "payment": {
                "amount": 20.0, "payment_method": "manual", "payment_status": "success", "track_info": "Bank transfer",
                "payer_info": "Jane Doe", "transaction_date": "2026-10-07T09:30:00Z", "transaction_reference": "BT-0001", "surcharge": 0.0,
            }},
        },
        "responses": {
            "201": {
                "description": "The receipt under `payment`: its `id`, `payment_applied`, `paid_amount`, `due_amount`, the order's `order_id` and `order_internal_id`, and the customer in `customer`, whose `id` field holds the customer's `customer_id`.",
                "schema": {"type": "object", "properties": {"payment": ref("OrderPaymentReceipt")}},
                "example": {"payment": {
                    "status": "success", "id": 7712, "date": None, "transaction_date": "2026-10-07T09:30:00Z",
                    "transaction_reference": "BT-0001", "payment_applied": 20.0, "payment_method": "manual", "payer_info": "Jane Doe",
                    "order_id": 1043, "order_internal_id": 2187, "order_total": 40.0, "due_amount": 20.0, "paid_amount": 20.0,
                    "customer": {"id": 512, "internal_id": 88, "name": "Jane Doe"}, "created_by": None, "created_at": "2026-10-07T09:30:04Z",
                }},
            },
            "400": {"description": "The body has no `payment` wrapper (message `payment info missing`), or `payment_method` is missing (message `payment_method is required`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "create_order_refund",
        "slug": "refund-an-order",
        "title": "Refund an order",
        "method": "POST",
        "path": BASE + "/{order_id}/refunds",
        "summary": "Records a refund against an order, raising `refunded` and leaving `paid` unchanged.",
        "description": "Wrap the refund in `refund`; `refund_date` is required, `line_items` is optional, and you send `amount` as text, such as `\"3.00\"`. The order's `charges_totals.refunded` rises by the amount and `paid` does not change. An `amount` greater than what was paid less earlier refunds is rejected with `400` and the reason `exceeds_paid`. To lower `paid` as well, use [Refund a payment](" + PAYMENT_REFUND_PAGE + ").",
        "parameters": [ORDER_ID],
        "body": {
            "schema": {"type": "object", "required": ["refund"], "properties": {"refund": ref("OrderRefundInput")}},
            "example": {"refund": {"amount": "3.00", "refund_date": "2026-10-07T14:00:00Z", "reason": "One item returned", "line_items": [{"order_item_id": 3302, "quantity": 1, "amount": 3.0}]}},
        },
        "responses": {
            "201": {
                "description": "`status` is `created`, with the new refund's `refund_id`, the order's `order_id` and `internal_id`, and `amount` as the text you sent.",
                "schema": ref("OrderRefund"),
                "example": {"status": "created", "refund_id": 61, "order_id": 1043, "internal_id": 2187, "amount": "3.00"},
            },
            "400": {"description": "The body has no `refund` wrapper (message `refund info missing`), `refund_date` is missing, or `amount` is more than what was paid less earlier refunds (reason `exceeds_paid`).", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "create_payment_refund",
        "slug": "refund-a-payment",
        "title": "Refund a payment",
        "method": "POST",
        "path": "/admin/payment/{payment_id}/refunds",
        "summary": "Refunds an amount from a payment, lowering the order's `paid`. Needs an `Idempotency-Key` header.",
        "description": "Send an `Idempotency-Key` header with a value you choose, and the refund wrapped in `refund`, with `transaction_no` beside the wrapper if you send it. The refund lowers the order's `paid` and raises `refunded`; after a partial refund, the order's `refund_status` and the payment's `status` in the order's `payments` show `partial`. Sending the same key again returns the first refund again, with `idempotent_replay` set to `true`, and refunds nothing more. In the response, `order_id` holds the order's `internal_id` and `order_no` holds its `order_id`.",
        "parameters": [PAYMENT_ID, IDEMPOTENCY_KEY],
        "body": {
            "schema": {"type": "object", "required": ["refund"], "properties": {
                "refund": ref("OrderPaymentRefundInput"),
                "transaction_no": {"type": "string", "description": "Your reference for this call. Send it beside `refund`, not inside it."},
            }},
            "example": {"transaction_no": "TXN-PREF-0001", "refund": {"amount": "5.00", "reason": "Damaged item", "is_gateway_refund": False, "send_refund_email": False, "adjust_with_order": False}},
        },
        "responses": {
            "200": {
                "description": "The refund, with `status` set to `success` and `amount` as a number. A repeat under the same `Idempotency-Key` returns the same `refund_id`, adds `\"idempotent_replay\": true`, and leaves out `adjust_with_order`, `gateway_refund`, `inventory_readjusted` and `refund_email_queued`.",
                "schema": ref("OrderPaymentRefund"),
                "example": {
                    "status": "success", "refund_id": 62, "payment_id": 7712, "order_id": 2187, "order_no": 1043, "currency": "AUD",
                    "amount": 5.0, "reason": "Damaged item", "gateway_refund": False, "gateway_transaction_id": None,
                    "transaction_status": None, "payment_status": "partial", "payment_refund_status": None, "order_refund_status": "partial",
                    "order_refunded_total": 5.0, "order_adjustment": 0.0, "order_total": 40.0, "available_for_refund": 15.0,
                    "adjust_with_order": False, "refund_email_queued": False, "inventory_readjusted": False,
                    "refunded_at": "2026-10-07T10:12:40Z",
                },
            },
            "400": {"description": "The `Idempotency-Key` header is missing. The reason is `idempotency_key_required`.", "schema": ERROR_REF},
            "409": {"description": "The order is paid in full, shipped in full and completed. The reason is `conflict` and the message `Refund is not allowed`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"payment_id": 7712}},
    },
    {
        "key": "send_order_invoice",
        "slug": "send-an-orders-invoice",
        "title": "Send an order's invoice",
        "method": "POST",
        "path": BASE + "/{order_internal_id}/send-invoice",
        "summary": "Emails the invoice of the order whose `internal_id` you pass to its billing email address.",
        "description": "Pass the order's `internal_id`, not its `order_id`: this path finds the order by `internal_id`, so an `order_id` returns `404` or emails the invoice of the order whose `internal_id` has that number. The call needs no body. The response names the address in `sent_to`, the time in `sent_at`, and `template` as `send-invoice`.",
        "parameters": [ORDER_INTERNAL_ID],
        "responses": {
            "200": {
                "description": "`status` is `success`. `sent_to` is the email address of the order's billing address.",
                "schema": ref("OrderInvoiceDispatch"),
                "example": {"status": "success", "order_id": 1043, "internal_id": 2187, "sent_to": "jane.doe@example.com", "template": "send-invoice", "invoice_document": None, "sent_at": "2026-10-07T09:40:12Z"},
            },
            "404": {"description": "No order has that `internal_id`. The message is `Order Not Found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_internal_id": 2187}},
    },
    {
        "key": "get_order_shipment_status",
        "slug": "retrieve-an-orders-shipment-status",
        "title": "Retrieve an order's shipment status",
        "method": "GET",
        "path": BASE + "/{order_id}/shipment-status",
        "summary": "Returns how far an order has shipped, with tracking details for each shipment.",
        "description": "Returns the order's `shipment_status` and, in `shipments_info`, one entry per shipment with its `shipping_provider`, `tracking_number` and `last_updated`. `shipment_status` is `unshipped` before the first shipment, `partial` while some units are still to ship, and `shipped` once every unit has shipped. Before the first shipment, [Retrieve an order](" + RETRIEVE_PAGE + ") shows `shipping_status` as `not_shipped`, while this call returns `unshipped`.",
        "parameters": [ORDER_ID],
        "responses": {
            "200": {
                "description": "The order's `order_id` and `internal_id`, its `shipment_status`, and one `shipments_info` entry per shipment. Before the first shipment, `shipments_info` is `[]`.",
                "schema": ref("OrderShipmentStatus"),
                "example": {"order_id": 1043, "internal_id": 2187, "shipment_status": "partial", "shipments_info": [
                    {"shipping_provider": "Example Courier", "tracking_number": "TRACK-0001", "last_updated": "2026-10-08T08:00:00"},
                ]},
            },
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "list_order_shipments",
        "slug": "list-an-orders-shipments",
        "title": "List an order's shipments",
        "method": "GET",
        "path": BASE + "/{order_id}/shipments",
        "summary": "Returns all of an order's shipments in one list.",
        "description": "Returns every shipment of the order under `shipments`, without paging; an order with none returns `\"shipments\": []`. Each shipment matches the response to [Create a shipment](" + CREATE_SHIPMENT_PAGE + "), and its `shipping_id` is the `shipment_id` that [Update a shipment](" + UPDATE_SHIPMENT_PAGE + ") takes.",
        "parameters": [ORDER_ID],
        "responses": {
            "200": {
                "description": "The order's shipments.",
                "schema": {"type": "object", "properties": {"shipments": {"type": "array", "items": ref("OrderShipment")}}},
                "example": {"shipments": [SHIPMENT]},
            },
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "create_order_shipment",
        "slug": "create-a-shipment",
        "title": "Create a shipment",
        "method": "POST",
        "path": BASE + "/{order_id}/shipments",
        "summary": "Ships units of an order's lines and returns the new shipment with its `shipping_id`.",
        "description": "Send `method`, `shipping_date` and `shipment_items` at the top level of the body; `tracking_info` is optional. The response returns `method` as `shipping_method`, `shipping_date` as `date_created` and `tracking_info` as `tracking_number`, which is `null` when you leave `tracking_info` out, and each line shows `shipped_quantity` beside `order_quantity`. The order's `shipping_status` moves to `partial`, and to `shipped` once every unit has shipped, and the first shipment's method becomes `shipping.shipping_type`. Shipping a product that tracks its stock lowers that stock by the units shipped.",
        "parameters": [ORDER_ID],
        "body": {"schema": ref("OrderShipmentInput"), "example": {
            "transaction_no": "TXN-SHIP-0001", "method": "Example Courier", "tracking_info": "TRACK-0001",
            "shipping_date": "2026-10-08T08:00:00", "shipment_items": [{"order_item_id": 3301, "quantity": 1}],
        }},
        "responses": {
            "201": {
                "description": "The new shipment under `shipment`, with `\"status\": \"success\"` beside it. Its `shipping_id` is the `shipment_id` that [Update a shipment](" + UPDATE_SHIPMENT_PAGE + ") takes.",
                "schema": SHIPMENT_RESPONSE,
                "example": {"shipment": SHIPMENT, "status": "success"},
            },
            "400": {"description": "`shipping_date` is missing. The message is `Shipping date is required`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "update_order_shipment",
        "slug": "update-a-shipment",
        "title": "Update a shipment",
        "method": "PATCH",
        "path": BASE + "/{order_id}/shipments/{shipment_id}",
        "summary": "Changes the shipment fields you send and returns the shipment.",
        "description": "Send any of `method`, `tracking_info`, `shipping_date` and `shipment_items`; only those fields change. `shipment_items` needs a `change_note`, or the call is rejected with `400`, and the note is not saved as an order comment. Changing `shipment_items` changes `shipped_quantity`, and the order's `shipping_status` becomes `shipped` once every unit has shipped.",
        "parameters": [ORDER_ID, SHIPMENT_ID],
        "body": {"schema": ref("OrderShipmentUpdateInput"), "example": {"tracking_info": "TRACK-0002"}},
        "responses": {
            "200": {
                "description": "The shipment after the change under `shipment`, with `\"status\": \"success\"` beside it.",
                "schema": SHIPMENT_RESPONSE,
                "example": {"shipment": UPDATED_SHIPMENT, "status": "success"},
            },
            "400": {"description": "`shipment_items` is sent without `change_note`. The message is `Change note is required when updating shipment items`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043, "shipment_id": 905}},
    },
    {
        "key": "update_order_status",
        "slug": "change-an-orders-status",
        "title": "Change an order's status",
        "method": "PATCH",
        "path": BASE + "/{order_id}/update-status",
        "summary": "Moves an order to another status and returns the order.",
        "description": "Send `status` with `cancelled`, `completed`, `draft`, `in_progress`, `paused` or `reopened`; this call does not read the key `order_status`. Any move is allowed, including out of `completed` or `cancelled`. A custom status from [Add a custom order status](" + CUSTOM_STATUS_PAGE + ") is rejected. Returns the order in the flat shape with the new `order_status`.",
        "parameters": [ORDER_ID],
        "body": {"schema": ref("OrderStatusInput"), "example": {"status": "paused", "refund_automatically": False}},
        "responses": {
            "200": {
                "description": "The order in the flat shape under `order`, with the new `order_status`.",
                "schema": FLAT_ORDER_RESPONSE,
                "example": {"order": PAUSED_FLAT_ORDER},
            },
            "400": {"description": "`status` is missing. The message is `Order Status Required`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"order_id": 1043}},
    },
    {
        "key": "create_order_status",
        "slug": "add-a-custom-order-status",
        "title": "Add a custom order status",
        "method": "POST",
        "path": "/admin/order/add-order-status",
        "summary": "Adds a custom order status value. No endpoint applies, lists or deletes it.",
        "description": "Send the fields at the top level of the body; the call returns `201` with `{\"success\": \"true\"}`, where `true` is text, for a new value and for one you already added. The order keeps its status, and the new value is rejected by [Change an order's status](" + STATUS_PAGE + "), [Update selected order fields](" + PATCH_PAGE + ") and the `order_status` filter of [List orders](" + LIST_PAGE + "). [Get ecommerce settings](" + ECOMMERCE_SETTINGS_PAGE + ") does not offer it in `order_filters.default_order_status`, and no endpoint lists or deletes a custom status, so each one stays in the store. A body without `order_id` returns `500`.",
        "body": {"schema": ref("OrderCustomStatusInput"), "example": {
            "order_id": 1043, "order_status_value": "ready_for_pickup", "order_status_label": "Ready For Pickup",
            "order_type": "Order", "status_type": "custom",
        }},
        "responses": {
            "201": {
                "description": "`success` is the text `\"true\"`, not a boolean.",
                "schema": {"type": "object", "properties": {"success": {"type": "string", "description": "The text `\"true\"`."}}},
                "example": {"success": "true"},
            },
            "500": {
                "description": "`order_id` is missing, and the body is flat, not wrapped in `error`. Send an order's `order_id`.",
                "schema": FLAT_ERROR_REF,
                "example": {"status": "error", "code": 500, "message": "Unexpected Error Occurred"},
            },
        },
        "example_call": {},
    },
    {
        "key": "list_customer_orders",
        "slug": "list-a-customers-orders",
        "title": "List a customer's orders",
        "method": "GET",
        "path": "/admin/customers/{customer_id}/orders",
        "summary": "Returns all of a customer's orders, newest first, leaving out cancelled orders.",
        "description": "Pass the customer's `customer_id`; the customer's `internal_id` returns `404` with the message `Customer Not Found`. Returns the customer's `customer_id` and `internal_id` and their orders in the flat shape, newest first, without paging; cancelled orders are left out. A customer with no orders returns `\"orders\": []`, and query parameters such as `limit`, `offset` and `sort` are ignored.",
        "parameters": [CUSTOMER_ID],
        "responses": {
            "200": {
                "description": "The customer's `customer_id` and `internal_id`, and their orders in the flat shape. Each line's `variations` is `[]`.",
                "schema": {"type": "object", "properties": {
                    "customer_id": {"type": "integer", "description": "The customer's `customer_id`."},
                    "internal_id": {"type": "integer", "description": "The customer's `internal_id`."},
                    "orders": {"type": "array", "items": ref("OrderFlat")},
                }},
                "example": {"customer_id": 512, "internal_id": 88, "orders": [CUSTOMER_FLAT_ORDER]},
            },
            "404": {
                "description": "No customer has that `customer_id`, for example because you passed the customer's `internal_id`. The body is flat, not wrapped in `error`.",
                "schema": FLAT_ERROR_REF,
                "example": {"status": "error", "code": 404, "message": "Customer Not Found"},
            },
        },
        "example_call": {"path": {"customer_id": 512}},
    },
]


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


ADDRESS_INPUT_PROPERTIES = {
    "first_name": text("Required. An address without it returns `500` with the body `{}`."),
    "last_name": text("The last name."),
    "email": text("The email address. [Send an order's invoice](" + INVOICE_PAGE + ") emails the billing address's `email`."),
    "company_name": text("Accepted and never stored: it always reads `\"\"`."),
    "address_line_1": text("The first address line."),
    "address_line_2": text("The second address line."),
    "city": text("The city."),
    "post_code": text("The post code."),
    "phone": text("The phone number."),
    "mobile": text("The mobile number."),
    "fax": text("The fax number."),
    "country_code": text("The country's code, such as `AU`. On an update, an address without it returns `500`. [Update an order's addresses](" + ADDRESSES_PAGE + ") also accepts a `country` record with the country's `id` instead."),
    "state_code": text("The state's code, such as `VIC`. [Update an order's addresses](" + ADDRESSES_PAGE + ") also accepts a `state` record with the state's `id` instead."),
}

ORDER_INPUT_PROPERTIES = {
    "customer_id": whole("The customer's `customer_id`. Without it, and without `customer`, the order is a guest order and its customer's `customer_id` and `internal_id` are `null`."),
    "customer": whole("Another name for `customer_id`."),
    "payment_gateway": {"type": "string", "enum": PAYMENT_GATEWAYS, "description": "A payment gateway code. Defaults to `PIS`, pay in store. `PAY_IN_STORE` is rejected with `400` and the reason `invalid_value`."},
    "delivery_type": {"type": "string", "enum": DELIVERY_TYPES, "description": "Lower case. Defaults to `shipping`. `SHIPPING` is rejected with `400` and the reason `invalid_value`."},
    "is_send_email": flag("Whether to send the order email."),
    "transaction_no": text("Your reference for the order. The store does not check it for duplicates."),
    "external_reference_order_id": text("An order number from another system. The listing's `externalReferenceOrderId` filter matches it."),
    "billing_address": ref("OrderAddressInput"),
    "shipping_address": ref("OrderAddressInput"),
    "products": {"type": "array", "minItems": 1, "items": ref("OrderProductInput"), "description": "Required. One line per product."},
    "discounts": {"type": "object", "description": "Discounts to apply.", "properties": {
        "coupon_code": text("A coupon code. A code no discount has is rejected with `422` and the message `Invalid Code`."),
    }},
}

WITH_PAYMENT_PROPERTIES = dict(
    {name: value for name, value in ORDER_INPUT_PROPERTIES.items() if name != "discounts"},
    transaction_no=text("Accepted and not stored."),
    external_reference_order_id=text("Accepted and not stored."),
    payment=ref("OrderInitialPaymentInput"),
)

SCHEMAS = {
    "Order": {"type": "object", "description": "One order in sections. A listing row has no `billing_address` or `shipping_address`, and its `customer` has only `customer_id`, `internal_id`, `first_name`, `last_name` and `customer_group`.", "properties": {
        "order_id": whole("The order's number in every order path except the custom fields and invoice paths. Equals `order_no`."),
        "order_no": whole("Equals `order_id`."),
        "internal_id": whole("A second number for the order. [Retrieve an order's custom fields](" + CUSTOM_FIELDS_PAGE + ") and [Send an order's invoice](" + INVOICE_PAGE + ") take it, and the listing's `orderIds` filter matches it."),
        "order_status": {"type": "string", "enum": ORDER_STATUSES, "description": "`in_progress` on a new order."},
        "payment_status": text("`unpaid` on a new order, and `partial` after a payment for part of the total."),
        "shipping_status": text("`not_shipped` before the first shipment, then `partial`, and `shipped` once every unit has shipped."),
        "currency_code": text("The order's currency code."),
        "transaction_no": nullable_text("The `transaction_no` sent when the order was created."),
        "ip_address": text("The IP address the order was placed from."),
        "created_on": text("When the order was created."),
        "last_updated_on": text("When the order last changed."),
        "customer": ref("OrderCustomer"),
        "billing_address": ref("OrderAddress"),
        "shipping_address": {"anyOf": [ref("OrderAddress"), {"type": "null"}], "description": "The shipping address, or `null` when the order has none, as on a `store_pickup` order."},
        "items": {"type": "array", "items": ref("OrderItem"), "description": "The order's lines."},
        "shipping": ref("OrderShipping"),
        "discounts": ref("OrderDiscounts"),
        "charges_totals": ref("OrderChargesTotals"),
        "payments": {"type": "array", "items": ref("OrderPayment"), "description": "The order's payments. An order created with `PIS` keeps its `awaiting` payment for the grand total beside each payment you record."},
        "fulfillment": ref("OrderFulfillment"),
    }},
    "OrderFlat": {"type": "object", "description": "One order in the flat shape: the totals and fulfillment fields at the top level, the customer in `customer_summary` and the lines in `order_line_details`. Creating, cancelling and changing the status of an order, and listing a customer's orders, return this shape.", "properties": {
        "order_id": whole("The order's number in every order path except the custom fields and invoice paths. Equals `order_no`."),
        "order_no": whole("Equals `order_id`."),
        "internal_id": whole("A second number for the order, taken by the custom fields and invoice paths."),
        "transaction_no": nullable_text("The `transaction_no` sent when the order was created. [Create an order with a payment](" + WITH_PAYMENT_PAGE + ") does not store it."),
        "currency_code": text("The order's currency code."),
        "order_status": {"type": "string", "enum": ORDER_STATUSES},
        "payment_status": text("`unpaid` on a new order, and `partial` after a payment for part of the total."),
        "shipping_status": text("`unshipped` before the first shipment and `shipped` once every unit has shipped. Where this shape shows `unshipped`, the sectioned shape shows `not_shipped`."),
        "sub_total": number("The total of the lines."),
        "shipping_cost": number("The shipping cost."),
        "shipping_tax": number("The tax on shipping."),
        "handling_cost": number("The handling cost."),
        "total_surcharge": number("The total surcharge."),
        "total_discount": number("The total discount."),
        "total_tax": number("The total tax."),
        "grand_total": number("The order's total."),
        "paid": number("The amount paid."),
        "due": number("The amount still due."),
        "items_total": whole("The `items_total` of `charges_totals` in the sectioned shape."),
        "ip_address": text("The IP address the order was placed from."),
        "created_at": text("When the order was created."),
        "updated_at": text("When the order last changed."),
        "customer_summary": ref("OrderCustomer"),
        "order_line_details": {"type": "array", "items": ref("OrderItem"), "description": "The order's lines."},
        "payments": {"type": "array", "items": ref("OrderPayment"), "description": "The order's payments."},
        "external_reference_order_id": nullable_text("An order number from another system."),
        "external_reference_store_id": nullable_text("A store reference from another system."),
        "external_reference_order_no": nullable_text("An order number from another system."),
        "external_reference_status": nullable_text("A status from another system."),
        "external_reference_url": nullable_text("A link to the order in another system."),
        "customer_po_number": nullable_text("The customer's purchase order number."),
        "payment_term": nullable_text("The payment term."),
        "fulfillment_mode": nullable_text("The fulfillment mode."),
        "fulfillment_term": nullable_text("The fulfillment term."),
        "invoice_mode": nullable_text("The invoice mode."),
        "billing_address": ref("OrderAddress"),
        "shipping_address": {"anyOf": [ref("OrderAddress"), EMPTY_BODY], "description": "The shipping address, or `{}` when the order has none, as on a `store_pickup` order."},
        "custom_fields": {"type": "array", "items": {}, "description": "The order's custom field values."},
        "delivery_cost": number("Only on an order with `delivery_type` `delivery`."),
    }},
    "OrderCustomer": {"type": "object", "description": "The order's customer. A listing row has only `customer_id`, `internal_id`, `first_name`, `last_name` and `customer_group`. On a guest order, `customer_id` and `internal_id` are `null`.", "properties": {
        "first_name": text("The customer's first name."),
        "last_name": text("The customer's last name."),
        "customer_group": nullable_text("The customer's group."),
        "gender": nullable_text("The customer's gender."),
        "customer_id": {"type": ["integer", "null"], "description": "The customer's `customer_id`, which [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + ") takes."},
        "internal_id": {"type": ["integer", "null"], "description": "The customer's `internal_id`, which the listing's `customerId` filter takes."},
        "email": text("The customer's email address."),
        "address_line_1": text("The first address line."),
        "address_line_2": text("The second address line."),
        "city": text("The city."),
        "country": ref("OrderReference"),
        "state": ref("OrderReference"),
        "post_code": text("The post code."),
        "phone": text("The phone number."),
        "mobile": text("The mobile number."),
        "fax": text("The fax number."),
        "company_name": text("The company name."),
    }},
    "OrderAddress": {"type": "object", "description": "A billing or shipping address. A field the last write left out reads `\"\"`.", "properties": {
        "id": whole("The address's own `id`."),
        "first_name": text("The first name."),
        "last_name": text("The last name."),
        "email": text("The email address. [Send an order's invoice](" + INVOICE_PAGE + ") emails the billing address's `email`."),
        "company_name": text("Always `\"\"`: the store never stores it."),
        "address_line_1": text("The first address line."),
        "address_line_2": text("The second address line."),
        "country": ref("OrderReference"),
        "state": ref("OrderReference"),
        "city": text("The city."),
        "post_code": text("The post code."),
        "mobile": text("The mobile number."),
        "phone": text("The phone number."),
        "fax": text("The fax number."),
    }},
    "OrderReference": {"type": "object", "description": "A country or a state.", "properties": {
        "id": whole("Identifies the country or state. [Update an order's addresses](" + ADDRESSES_PAGE + ") accepts it in a `country` or `state` record."),
        "name": text("The name, such as `Australia`."),
        "code": text("The code, such as `AU`, as `country_code` and `state_code` take it."),
    }},
    "OrderItem": {"type": "object", "description": "One order line.", "properties": {
        "item_id": whole("Identifies the line. Send it as `order_item_id` to ship or refund the line."),
        "product_name": text("The product's name."),
        "product_id": whole("The product's `product_id`, as the listing's `productId` filter takes it."),
        "sku": text("The product's SKU."),
        "quantity": whole("The quantity ordered."),
        "price": number("The unit price."),
        "total_amount": number("The line total."),
        "tax": number("The tax on the line."),
        "discount": number("The discount on the line."),
        "tax_discount": number("The tax discount on the line."),
        "is_taxable": flag("Whether the line is taxable."),
        "is_shippable": flag("Whether the line can be shipped."),
        "image_url": nullable_text("The product image's URL."),
        "variations": {"type": ["array", "null"], "items": {}, "description": "`[]`, or `null` in the response to creating the order."},
        "serial_batch_number": nullable_text("The serial or batch number."),
    }},
    "OrderShipping": {"type": "object", "properties": {
        "delivery_type": {"type": "string", "enum": DELIVERY_TYPES, "description": "The delivery type the order was created with."},
        "shipping_type": nullable_text("The method of the order's first shipment."),
        "shipping_status": text("`not_shipped` before the first shipment, then `partial`, and `shipped` once every unit has shipped."),
        "shipping_cost": number("The shipping cost."),
        "shipping_tax": number("The tax on shipping."),
    }},
    "OrderDiscounts": {"type": "object", "properties": {
        "total_discount": number("The total discount."),
        "coupon_code": nullable_text("The coupon code applied."),
        "gift_card_code": nullable_text("The gift card code applied."),
    }},
    "OrderChargesTotals": {"type": "object", "description": "The order's totals. `group_meta` marks this section `writable: false`.", "properties": {
        "sub_total": number("The total of the lines."),
        "total_tax": number("The total tax."),
        "handling_cost": number("The handling cost."),
        "total_surcharge": number("The total surcharge."),
        "other_charges": number("Other charges."),
        "grand_total": number("The order's total."),
        "paid": number("The amount paid. A payment raises it and a payment refund lowers it; an order refund does not change it."),
        "due": number("The amount still due."),
        "refunded": number("The amount refunded. Both kinds of refund raise it."),
        "refund_status": nullable_text("`partial` after a partial payment refund."),
        "items_total": whole("The order's item total."),
    }},
    "OrderPayment": {"type": "object", "description": "One payment on the order.", "properties": {
        "id": whole("Identifies the payment."),
        "status": text("Such as `awaiting` for the payment an order created with `PIS` starts with, `success` for a recorded payment, or `partial` after part of the payment is refunded."),
        "amount": number("The payment's amount."),
        "payment_method": nullable_text("The payment method."),
        "track_info": nullable_text("Tracking details for the payment."),
        "gateway_name": nullable_text("The payment gateway's name."),
        "gateway_code": text("The payment gateway's code, such as `PIS`, or `API` for the payment from [Create an order with a payment](" + WITH_PAYMENT_PAGE + ")."),
        "gateway_response": nullable_text("Only in the flat shape."),
        "payer_info": nullable_text("Details of the payer."),
        "paying_date": nullable_text("When the payment was made."),
        "transaction_date": nullable_text("The transaction's date."),
        "transaction_reference": nullable_text("The transaction's reference."),
    }},
    "OrderFulfillment": {"type": "object", "properties": {
        "fulfillment_mode": nullable_text("The fulfillment mode."),
        "fulfillment_term": nullable_text("The fulfillment term."),
        "invoice_mode": nullable_text("The invoice mode."),
        "payment_term": nullable_text("The payment term. [Update selected order fields](" + PATCH_PAGE + ") changes it."),
        "customer_po_number": nullable_text("The customer's purchase order number. [Update selected order fields](" + PATCH_PAGE + ") changes it."),
        "external_reference_order_id": nullable_text("An order number from another system, as sent when the order was created."),
        "external_reference_store_id": nullable_text("A store reference from another system."),
        "external_reference_order_no": nullable_text("An order number from another system."),
        "external_reference_status": nullable_text("A status from another system."),
        "external_reference_url": nullable_text("A link to the order in another system."),
        "custom_fields": {"type": "array", "items": {}, "description": "The order's custom field values."},
    }},
    "OrderGroupMeta": {"type": "object", "description": "One entry per section: seven on a listing, which has no address entries, and nine on [Retrieve an order](" + RETRIEVE_PAGE + ").", "properties": {
        "customer": ref("OrderSectionMeta"),
        "billing_address": ref("OrderSectionMeta"),
        "shipping_address": ref("OrderSectionMeta"),
        "items": ref("OrderSectionMeta"),
        "shipping": ref("OrderSectionMeta"),
        "discounts": ref("OrderSectionMeta"),
        "charges_totals": ref("OrderSectionMeta"),
        "payments": ref("OrderSectionMeta"),
        "fulfillment": ref("OrderSectionMeta"),
    }},
    "OrderSectionMeta": {"type": "object", "properties": {
        "kind": text("`section`."),
        "writable": flag("Whether you can write the section. `false` for `charges_totals`."),
        "href": text("The section's own path, only on `payments` and the two addresses. It comes back with the placeholder `{id}`, such as `/api/v4/admin/orders/{id}/addresses`; put the order's `order_id` in its place."),
    }},
    "OrderFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Returned when you send `field_metadata=true` or `1`. One entry per top-level order field, each with `type`, `read_only` and `key_path`, and on some fields `required`, `note`, `values`, `format`, `max_length` or `in_list`. Each section, the two addresses included, has an entry for each of its own fields."},
    "OrderPagination": {"type": "object", "properties": {
        "total": whole("The number of orders that match your filters, cancelled orders left out unless you ask for them."),
        "limit": whole("The page size applied: the `limit` you sent, at most `20`, or `20`."),
        "offset": whole("The number of orders skipped before this page."),
        "count": whole("The number of orders on this page."),
        "current_page": whole("The number of this page, counting from `1`."),
        "total_pages": whole("The number of pages."),
        "has_next": flag("`true` when there is a page after this one."),
        "has_previous": flag("`true` when there is a page before this one."),
        "previous_page": nullable_text("The previous page, or `null` on the first page."),
        "next_page": nullable_text("The next page as a full URL, or `null` on the last page."),
    }},
    "OrderAddresses": {"type": "object", "properties": {
        "order_id": whole("The order's `order_id`."),
        "internal_id": whole("The order's `internal_id`."),
        "billing_address": ref("OrderAddress"),
        "shipping_address": ref("OrderAddress"),
    }},
    "OrderComment": {"type": "object", "properties": {
        "id": whole("Identifies the comment."),
        "content": text("The comment's text."),
        "admin_name": text("The name of the admin user who added the comment."),
        "visible_to_customer": flag("`true` when the comment was added with `\"save_and_send\": true`."),
        "admin": flag("`true` for a comment added through this API."),
        "created": text("When the comment was added, written `M/D/YYYY`, two spaces and a time, such as `10/7/2026  14:05:09`. Not ISO 8601."),
    }},
    "OrderCustomFields": {"type": "object", "properties": {
        "order_id": whole("The order's `internal_id`: the number you passed."),
        "custom_fields": {"type": "array", "items": {}, "description": "The order's custom field values."},
        "delivery_cost": number("Only on an order with `delivery_type` `delivery`."),
    }},
    "OrderPaymentReceipt": {"type": "object", "properties": {
        "status": text("Such as `success`."),
        "id": whole("Identifies the payment. Pass it as `payment_id` to [Refund a payment](" + PAYMENT_REFUND_PAGE + ")."),
        "date": nullable_text("The payment's date."),
        "transaction_date": nullable_text("The `transaction_date` you sent."),
        "transaction_reference": nullable_text("The `transaction_reference` you sent."),
        "payment_applied": number("The amount applied to the order."),
        "payment_method": text("The payment method."),
        "payer_info": nullable_text("Details of the payer."),
        "order_id": whole("The order's `order_id`."),
        "order_internal_id": whole("The order's `internal_id`."),
        "order_total": number("The order's grand total."),
        "due_amount": number("The amount still due after this payment."),
        "paid_amount": number("The amount paid, this payment included."),
        "customer": ref("OrderPaymentReceiptCustomer"),
        "created_by": nullable_text("Who recorded the payment."),
        "created_at": text("When the payment was recorded."),
    }},
    "OrderPaymentReceiptCustomer": {"type": "object", "description": "The order's customer.", "properties": {
        "id": whole("The customer's `customer_id`, not the customer's `internal_id`."),
        "internal_id": whole("The customer's `internal_id`."),
        "name": text("The customer's name."),
    }},
    "OrderRefund": {"type": "object", "properties": {
        "status": text("`created`."),
        "refund_id": whole("Identifies the new refund."),
        "order_id": whole("The order's `order_id`."),
        "internal_id": whole("The order's `internal_id`."),
        "amount": text("The `amount` you sent, as text."),
    }},
    "OrderPaymentRefund": {"type": "object", "description": "A payment refund. `order_id` and `order_no` are named the other way round from every other response.", "properties": {
        "status": text("`success`."),
        "refund_id": whole("Identifies the refund. A repeat under the same `Idempotency-Key` returns the same value."),
        "payment_id": whole("The `payment_id` you passed."),
        "order_id": whole("The order's `internal_id`, not its `order_id`."),
        "order_no": whole("The order's `order_id`."),
        "currency": text("The currency code."),
        "amount": number("The amount refunded, as a number."),
        "reason": nullable_text("The `reason` you sent."),
        "gateway_refund": flag("Whether the refund went through the payment gateway. Not in a repeat."),
        "gateway_transaction_id": nullable_text("The gateway's transaction reference."),
        "transaction_status": nullable_text("The transaction's status."),
        "payment_status": text("The payment's status, `partial` while part of it is left."),
        "payment_refund_status": nullable_text("The payment's refund status."),
        "order_refund_status": nullable_text("The order's refund status, such as `partial`."),
        "order_refunded_total": number("The order's refunded total."),
        "order_adjustment": number("The adjustment made to the order."),
        "order_total": number("The order's grand total."),
        "available_for_refund": number("What can still be refunded."),
        "adjust_with_order": flag("The `adjust_with_order` you sent. Not in a repeat."),
        "refund_email_queued": flag("Whether a refund email was queued. Not in a repeat."),
        "inventory_readjusted": flag("Whether stock was readjusted. Not in a repeat."),
        "refunded_at": text("When the refund was made."),
        "idempotent_replay": flag("`true` on a repeat under the same `Idempotency-Key`. Only in a repeat."),
    }},
    "OrderInvoiceDispatch": {"type": "object", "properties": {
        "status": text("`success`."),
        "order_id": whole("The order's `order_id`."),
        "internal_id": whole("The order's `internal_id`."),
        "sent_to": text("The email address of the order's billing address."),
        "template": text("`send-invoice`."),
        "invoice_document": {"description": "`null`."},
        "sent_at": text("When the invoice was sent."),
    }},
    "OrderShipmentStatus": {"type": "object", "properties": {
        "order_id": whole("The order's `order_id`."),
        "internal_id": whole("The order's `internal_id`."),
        "shipment_status": {"type": "string", "enum": ["unshipped", "partial", "shipped"], "description": "`unshipped` before the first shipment, `partial` while some units are still to ship, and `shipped` once every unit has shipped."},
        "shipments_info": {"type": "array", "items": ref("OrderShipmentTracking"), "description": "One entry per shipment."},
    }},
    "OrderShipmentTracking": {"type": "object", "properties": {
        "shipping_provider": text("The shipment's shipping provider."),
        "tracking_number": nullable_text("The shipment's tracking number."),
        "last_updated": text("When the shipment last changed."),
    }},
    "OrderShipment": {"type": "object", "description": "One shipment. The `method`, `tracking_info` and `shipping_date` you write come back as `shipping_method`, `tracking_number` and `date_created`.", "properties": {
        "shipping_id": whole("Identifies the shipment. Pass it as `shipment_id` to [Update a shipment](" + UPDATE_SHIPMENT_PAGE + ")."),
        "order_id": whole("The order's `order_id`."),
        "order_internal_id": whole("The order's `internal_id`."),
        "customer_id": {"type": ["integer", "null"], "description": "The customer's `customer_id`."},
        "customer_internal_id": {"type": ["integer", "null"], "description": "The customer's `internal_id`."},
        "order_address_id": {"type": ["integer", "null"], "description": "Identifies an address of the order."},
        "date_created": text("The `shipping_date` you sent."),
        "tracking_number": nullable_text("The `tracking_info` you sent, or `null`."),
        "shipping_method": text("The `method` you sent."),
        "shipping_address": ref("OrderAddress"),
        "billing_address": ref("OrderAddress"),
        "items": {"type": "array", "items": ref("OrderShipmentItem"), "description": "The lines in the shipment."},
    }},
    "OrderShipmentItem": {"type": "object", "properties": {
        "order_item_id": whole("The order line's `item_id`."),
        "product_id": whole("The product's `product_id`."),
        "product_name": text("The product's name."),
        "product_sku": text("The product's SKU."),
        "shipping_class": nullable_text("The product's shipping class."),
        "order_quantity": whole("The quantity ordered."),
        "shipped_quantity": whole("The quantity shipped."),
        "total_amount": number("The line total."),
    }},
    "OrderInput": {"type": "object", "required": ["products"], "description": "Send these fields at the top level of the body. Any other field is rejected with `400` and the reason `unknown_field`.", "properties": ORDER_INPUT_PROPERTIES},
    "OrderWithPaymentInput": {"type": "object", "required": ["products", "payment"], "description": "The fields of [Create an order](" + CREATE_PAGE + ") and the `payment` to record, at the top level of the body.", "properties": WITH_PAYMENT_PROPERTIES},
    "OrderInitialPaymentInput": {"type": "object", "description": "The payment to record. The store files it under gateway `API` with `payment_method` `API`.", "properties": {
        "amount": number("The amount paid. The order's `paid` is set to it."),
        "surcharge": number("A surcharge on the payment."),
        "status": text("The payment's status, such as `success`."),
        "payment_method": text("Accepted, but the payment's `payment_method` is stored as `API`."),
        "track_info": text("Tracking details for the payment. Stored."),
        "payer_info": text("Accepted, and stored as `\"\"`."),
        "transaction_reference": text("Accepted, and stored as `\"\"`."),
        "transaction_date": text("Accepted, but set to the time of the call."),
    }},
    "OrderAddressInput": {"type": "object", "required": ["first_name"], "description": "An address. It replaces the whole stored address, so a field you leave out becomes `\"\"`.", "properties": ADDRESS_INPUT_PROPERTIES},
    "OrderProductInput": {"type": "object", "description": "One line to order.", "properties": {
        "product_id": whole("The product's `id`, which the order's lines show as `product_id`."),
        "quantity": whole("How many units of the product to order."),
    }},
    "OrderUpdateInput": {"type": "object", "description": "Accepts only these four fields. `items` is rejected with `400` and the reason `not_implemented`.", "properties": {
        "customer_id": whole("The `customer_id` of the customer to move the order to."),
        "customer": {"type": "object", "description": "Another way to move the order to a customer.", "properties": {"customer_id": whole("The customer's `customer_id`.")}},
        "billing_address": ref("OrderAddressInput"),
        "shipping_address": ref("OrderAddressInput"),
    }},
    "OrderPatchInput": {"type": "object", "description": "Accepts only these fields. Any other field is rejected with `400` and the reason `unknown_field`.", "properties": {
        "order_status": {"type": "string", "enum": ORDER_STATUSES, "description": "The order's new status. A custom status from [Add a custom order status](" + CUSTOM_STATUS_PAGE + ") is rejected."},
        "customer_po_number": text("The customer's purchase order number."),
        "payment_term": text("The payment term, such as `NET30`."),
        "billing_address": ref("OrderAddressInput"),
        "shipping_address": ref("OrderAddressInput"),
        "fulfillment": {"type": "object", "description": "Accepted only inside the `order` wrapper. A top-level `fulfillment` key is rejected with `400`.", "properties": {
            "customer_po_number": text("The customer's purchase order number."),
            "payment_term": text("The payment term."),
        }},
    }},
    "OrderAddressesInput": {"type": "object", "description": "Send at least one address, at the top level of the body. An address you leave out does not change. Each address may name its country and state with `country` and `state` records holding their `id` instead of `country_code` and `state_code`.", "properties": {
        "transaction_no": text("Your reference for this call."),
        "billing_address": ref("OrderAddressInput"),
        "shipping_address": ref("OrderAddressInput"),
    }},
    "OrderCancelInput": {"type": "object", "description": "Every field is optional, and you can send no body at all.", "properties": {
        "transaction_no": text("Your reference for this call."),
        "reason": text("Why the order is cancelled."),
        "refund_automatically": flag("Whether to refund the order automatically."),
        "is_gateway_refund": flag("Whether to refund through the payment gateway."),
    }},
    "OrderCommentInput": {"type": "object", "required": ["content"], "description": "Send these fields at the top level of the body, not wrapped in `comment`.", "properties": {
        "content": text("Required. The comment's text."),
        "save_and_send": flag("`true` makes the comment visible to the customer."),
        "transaction_no": text("Your reference for this call."),
    }},
    "OrderPaymentInput": {"type": "object", "required": ["payment_method"], "description": "The payment, inside the `payment` wrapper.", "properties": {
        "amount": number("The amount paid."),
        "payment_method": text("Required, such as `manual`."),
        "payment_status": text("The payment's status, such as `success`."),
        "track_info": text("Tracking details for the payment."),
        "payer_info": text("Details of the payer."),
        "transaction_date": text("The transaction's date. Returned as you sent it."),
        "transaction_reference": text("The transaction's reference. Returned as you sent it."),
        "surcharge": number("A surcharge on the payment."),
    }},
    "OrderRefundInput": {"type": "object", "required": ["refund_date"], "description": "The refund, inside the `refund` wrapper.", "properties": {
        "amount": text("The amount to refund, as text, such as `\"3.00\"`. It may not be more than what was paid less earlier refunds."),
        "refund_date": text("Required. When the refund was made."),
        "reason": text("Why the order is refunded."),
        "line_items": {"type": "array", "items": ref("OrderRefundLineInput"), "description": "Optional. The lines the refund is for."},
    }},
    "OrderRefundLineInput": {"type": "object", "properties": {
        "order_item_id": whole("The order line's `item_id`."),
        "quantity": whole("How many units of the line are refunded."),
        "amount": number("The amount refunded for the line."),
    }},
    "OrderPaymentRefundInput": {"type": "object", "description": "The refund, inside the `refund` wrapper.", "properties": {
        "amount": {"type": ["string", "number"], "description": "The amount to refund, as text such as `\"5.00\"` or as a number."},
        "reason": text("Why the payment is refunded."),
        "is_gateway_refund": flag("Whether to refund through the payment gateway."),
        "send_refund_email": flag("Whether to send a refund email."),
        "adjust_with_order": flag("Whether to adjust the order."),
    }},
    "OrderShipmentInput": {"type": "object", "required": ["method", "shipping_date", "shipment_items"], "description": "Send these fields at the top level of the body.", "properties": {
        "transaction_no": text("Your reference for this call."),
        "method": text("Required. The shipping method, returned as `shipping_method`."),
        "tracking_info": text("Optional. The tracking number, returned as `tracking_number`."),
        "shipping_date": text("Required. The shipping date, returned as `date_created`."),
        "shipment_items": {"type": "array", "items": ref("OrderShipmentItemInput"), "description": "Required. The lines to ship."},
    }},
    "OrderShipmentUpdateInput": {"type": "object", "description": "Send only the fields to change, at the top level of the body.", "properties": {
        "transaction_no": text("Your reference for this call."),
        "method": text("The shipping method, returned as `shipping_method`."),
        "tracking_info": text("The tracking number, returned as `tracking_number`."),
        "shipping_date": text("The shipping date, returned as `date_created`."),
        "shipment_items": {"type": "array", "items": ref("OrderShipmentItemInput"), "description": "The shipment's lines. Needs `change_note`."},
        "change_note": text("Required with `shipment_items`. Not saved as an order comment."),
    }},
    "OrderShipmentItemInput": {"type": "object", "properties": {
        "order_item_id": whole("The order line's `item_id`."),
        "quantity": whole("How many units of the line to ship."),
    }},
    "OrderStatusInput": {"type": "object", "required": ["status"], "properties": {
        "status": {"type": "string", "enum": ORDER_STATUSES, "description": "Required. The order's new status. The key `order_status` is not read here."},
        "transaction_no": text("Your reference for this call."),
        "refund_automatically": flag("Whether to refund the order automatically."),
    }},
    "OrderCustomStatusInput": {"type": "object", "required": ["order_id"], "properties": {
        "order_id": whole("Required. An order's `order_id`. Without it the call returns `500`. The order keeps its status."),
        "order_status_value": text("The custom status value, such as `ready_for_pickup`."),
        "order_status_label": text("The label for the value, such as `Ready For Pickup`."),
        "order_type": text("Such as `Order`."),
        "status_type": text("Such as `custom`."),
    }},
    "OrderError": {"type": "object", "description": "Most rejections return this shape. The more specific reasons the endpoint pages name, such as `unknown_field` or `exceeds_paid`, appear in `code` or in `details`. A method a path does not support returns `404` with the message `No such endpoint: <METHOD> <path>`, such as `PUT` on an order's `addresses`, `update-status` or a shipment; `GET` on `/admin/order/add-order-status` returns `405`.", "properties": {"error": {"type": "object", "properties": {
        "code": text("A machine-readable reason, such as `invalid_request`, `not_found`, `conflict`, `unprocessable` or `internal_error`."),
        "message": text("What went wrong, such as `Order Not Found`."),
        "details": {"type": "array", "items": {"type": "object"}, "description": "More detail about the rejection."},
        "request_id": text("Identifies this request."),
    }}}},
    "OrderFlatError": {"type": "object", "description": "The flat error shape that [List a customer's orders](" + CUSTOMER_ORDERS_PAGE + ") and [Add a custom order status](" + CUSTOM_STATUS_PAGE + ") return.", "properties": {
        "status": text("`error`."),
        "code": whole("The HTTP status."),
        "message": text("What went wrong."),
    }},
}
