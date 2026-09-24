"""The Customers endpoints, as measured against a live store and recorded in the SDKs' ENDPOINTS.md."""

TAG = "Customers"
BASE = "/admin/customers"

CUSTOMER_ID = {
    "name": "customer_id",
    "in": "path",
    "required": True,
    "description": "The customer's `customer_id`, as returned by the listing. Not `internal_id`.",
    "schema": {"type": "integer", "example": 123},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rows per page. Capped at 20: a larger value is accepted and the cap is echoed back in `pagination.limit`.", "schema": {"type": "integer", "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rows to skip. Takes precedence over `page` when both are sent.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read against the applied `limit`.", "schema": {"type": "integer", "example": 1}}

STATUS_VALUES = ["active", "inactive", "pending", "approval_awaiting", "awaiting_verification"]


def text(name, description):
    return {"name": name, "in": "query", "description": description, "schema": {"type": "string"}}


FILTERS = [
    text("search", "Free-text search. `searchText`, `query` and `keyword` are accepted spellings of the same parameter."),
    text("email", "Filter by email address."),
    text("companyName", "Filter by company name."),
    text("phone", "Filter by phone number."),
    text("mobile", "Filter by mobile number."),
    text("country", "Filter by country."),
    text("state", "Filter by state."),
    text("city", "Filter by city."),
    text("postCode", "Filter by post code. Parameter names are case-sensitive, so `postcode` is refused."),
    text("customerGroup", "Filter by customer group."),
    {"name": "status", "in": "query", "description": "Filter by status, matched case-insensitively. Any other value is refused with `400`.", "schema": {"type": "string", "enum": STATUS_VALUES}},
]

EXPORT_COLUMNS = [
    "firstName", "lastName", "customerType", "addressLine1", "addressLine2", "city", "country",
    "state", "postCode", "phone", "mobile", "fax", "status", "abn", "storeCredit", "groups",
    "parentGroup", "companyName",
]

SAMPLE_CUSTOMER = {
    "customer_id": 123,
    "internal_id": 45,
    "first_name": "Jane",
    "last_name": "Doe",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "status": "active",
    "company_name": None,
    "store_credit": 0.0,
    "customer_groups": [],
    "addresses": [
        {"id": 901, "type": "primary", "first_name": "Jane", "last_name": "Doe", "address_line_1": "1 Example Street", "city": "Sydney", "post_code": "2000"},
    ],
    "custom_properties": [],
    "created_at": "2026-09-01T10:00:00Z",
    "updated_at": "2026-09-01T10:00:00Z",
}

SAMPLE_PAGINATION = {
    "total": 42, "limit": 20, "offset": 0, "count": 20, "current_page": 1, "total_pages": 3,
    "has_next": True, "has_previous": False, "previous_page": None, "next_page": "2",
}

ENDPOINTS = [
    {
        "key": "list_customers",
        "slug": "list-customers",
        "title": "List customers",
        "method": "GET",
        "path": BASE,
        "summary": "A page of customers, with a `pagination` block for the next page.",
        "description": "Returns customers one page at a time. Filters narrow the page; `sort` reorders it and must name a real field, or the call is refused with `400 invalid_sort_field`. Parameter names are case-sensitive and an unknown one is refused with `400 unknown_parameter`. The date-range parameters `createdFrom`, `createdTo`, `updatedFrom` and `updatedTo` are accepted but not applied.",
        "parameters": [LIMIT, OFFSET, PAGE] + FILTERS + [text("sort", "Field to sort by. An unknown field is refused with `400 invalid_sort_field`.")],
        "responses": {
            "200": {"description": "A page of customers.", "schema": {"type": "object", "properties": {"customers": {"type": "array", "items": {"$ref": "#/components/schemas/Customer"}}, "pagination": {"$ref": "#/components/schemas/Pagination"}}}, "example": {"customers": [SAMPLE_CUSTOMER], "pagination": SAMPLE_PAGINATION}},
            "400": {"description": "An unknown parameter, sort field or status value."},
        },
    },
    {
        "key": "get_customer",
        "slug": "retrieve-a-customer",
        "title": "Retrieve a customer",
        "method": "GET",
        "path": BASE + "/{customer_id}",
        "summary": "One customer by `customer_id`.",
        "description": "Returns one customer. Use the `customer_id` from a listing. `internal_id` is a second id space over the same records: sending it can return a different customer with a `200` rather than a `404`, so check the record you get back is the one you asked for.",
        "parameters": [CUSTOMER_ID],
        "responses": {
            "200": {"description": "The customer.", "schema": {"type": "object", "properties": {"customer": {"$ref": "#/components/schemas/Customer"}}}, "example": {"customer": SAMPLE_CUSTOMER}},
            "404": {"description": "No customer has that id."},
        },
    },
    {
        "key": "count_customers",
        "slug": "count-customers",
        "title": "Count customers",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "The number of customers, optionally filtered.",
        "description": "Returns the total as one key. `email`, `search`, `status`, `companyName`, `phone`, `city`, `state` and `customerGroup` narrow the total. `country`, the paging parameters, `sort` and the date ranges are accepted and ignored, so they return the unfiltered total.",
        "parameters": [p for p in FILTERS if p["name"] in {"search", "email", "status", "companyName", "phone", "city", "state", "customerGroup"}],
        "responses": {
            "200": {"description": "The total.", "schema": {"type": "object", "properties": {"total": {"type": "integer"}}}, "example": {"total": 42}},
        },
    },
    {
        "key": "check_email",
        "slug": "check-an-email-address",
        "title": "Check an email address",
        "method": "GET",
        "path": BASE + "/check-email",
        "summary": "Whether an email address already belongs to a customer.",
        "description": "Answers `exists`. For a free address that is the only key. For a taken one the answer also carries that customer's `customer_id` and `internal_id`.",
        "parameters": [{"name": "email", "in": "query", "required": True, "description": "The address to check.", "schema": {"type": "string", "format": "email", "example": "jane@example.com"}}],
        "responses": {
            "200": {"description": "Whether the address is taken.", "schema": {"type": "object", "properties": {"exists": {"type": "boolean"}, "customer_id": {"type": "integer"}, "internal_id": {"type": "integer"}}}, "example": {"exists": True, "customer_id": 123, "internal_id": 45}},
        },
    },
    {
        "key": "export_customers",
        "slug": "export-customers",
        "title": "Export customers",
        "method": "GET",
        "path": BASE + "/export",
        "summary": "Every customer as an XLSX spreadsheet.",
        "description": "Returns a spreadsheet of every customer. Filters are not applied: `status=active` does not narrow the export. Each of the 18 column parameters keeps its column when omitted or sent as `1`, `true`, `on` or `yes`, and removes it for any other value.",
        "parameters": [{"name": c, "in": "query", "description": "Keep or remove this column.", "schema": {"type": "string", "example": "1"}} for c in EXPORT_COLUMNS],
        "responses": {
            "200": {"description": "An XLSX file.", "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "schema": {"type": "string", "format": "binary"}},
        },
    },
    {
        "key": "create_customer",
        "slug": "create-a-customer",
        "title": "Create a customer",
        "method": "POST",
        "path": BASE,
        "summary": "Add a customer and get back its new `customer_id`.",
        "description": "Creates a customer and returns it with its new `customer_id`. Without `status`, a new customer is `awaiting_verification` and has no usable login, whatever `password` was sent; send `status: \"active\"` with a `password` for a customer who can sign in. Address fields sent inline are accepted and discarded: use [Add addresses](/api-reference/customers/add-addresses) instead. The answer always carries three addresses of the store's own making: primary, shipping and billing.",
        "body": {"schema": {"type": "object", "required": ["customer"], "properties": {"customer": {"$ref": "#/components/schemas/CustomerInput"}, "transaction_no": {"type": "string", "description": "Optional reference for this write."}}}, "example": {"customer": {"first_name": "Jane", "last_name": "Doe", "email": "jane@example.com", "company": False}}},
        "responses": {
            "201": {"description": "The new customer.", "schema": {"type": "object", "properties": {"customer": {"$ref": "#/components/schemas/Customer"}}}, "example": {"customer": SAMPLE_CUSTOMER}},
            "400": {"description": "A required field is missing, for example `Customer name is required`."},
            "409": {"description": "The email address is already registered."},
        },
    },
    {
        "key": "update_customer",
        "slug": "update-a-customer",
        "title": "Update a customer",
        "method": "PUT",
        "path": BASE + "/{customer_id}",
        "summary": "Change only the fields you send; the rest stay as they are.",
        "description": "Send only the fields that change; the rest are left alone. Sending `custom_properties` replaces the whole list rather than adding to it.",
        "parameters": [CUSTOMER_ID],
        "body": {"schema": {"type": "object", "required": ["customer"], "properties": {"customer": {"$ref": "#/components/schemas/CustomerInput"}}}, "example": {"customer": {"last_name": "Smith"}}},
        "responses": {
            "200": {"description": "The updated customer.", "schema": {"type": "object", "properties": {"customer": {"$ref": "#/components/schemas/Customer"}}}, "example": {"customer": dict(SAMPLE_CUSTOMER, last_name="Smith", name="Jane Smith")}},
            "404": {"description": "No customer has that id."},
        },
    },
    {
        "key": "delete_customer",
        "slug": "delete-a-customer",
        "title": "Delete a customer",
        "method": "DELETE",
        "path": BASE + "/{customer_id}",
        "summary": "Remove a customer permanently.",
        "description": "Deletes the customer. The answer has no body.",
        "parameters": [CUSTOMER_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No customer has that id."},
        },
    },
    {
        "key": "add_addresses",
        "slug": "add-addresses",
        "title": "Add addresses",
        "method": "POST",
        "path": BASE + "/{customer_id}/addresses",
        "summary": "Add shipping, billing or primary addresses to a customer.",
        "description": "Adds one or more addresses. `type` is `primary`, `shipping` or `billing`; any other value is refused with `400 invalid_enum`. A `state` that is not in the `country` is refused with `400 state_country_mismatch`.",
        "parameters": [CUSTOMER_ID],
        "body": {"schema": {"type": "object", "required": ["customer"], "properties": {"customer": {"type": "object", "properties": {"addresses": {"type": "array", "items": {"$ref": "#/components/schemas/AddressInput"}}}}}}, "example": {"customer": {"addresses": [{"type": "shipping", "first_name": "Jane", "last_name": "Doe", "address_line_1": "1 Example Street", "city": "Sydney", "post_code": "2000"}]}}},
        "responses": {
            "201": {"description": "The customer with its addresses.", "schema": {"type": "object", "properties": {"customer": {"$ref": "#/components/schemas/Customer"}}}, "example": {"customer": SAMPLE_CUSTOMER}},
            "400": {"description": "An invalid address `type`, or a state outside the country."},
        },
    },
    {
        "key": "reset_password",
        "slug": "reset-a-password",
        "title": "Reset a password",
        "method": "POST",
        "path": BASE + "/{customer_id}/reset-password",
        "summary": "Set a new password without the old one.",
        "description": "Sets the customer's password. The old password is not needed.",
        "parameters": [CUSTOMER_ID],
        "body": {"schema": {"type": "object", "required": ["customer"], "properties": {"customer": {"type": "object", "required": ["password"], "properties": {"password": {"type": "string"}}}, "transaction_no": {"type": "string", "description": "Optional reference for this write."}}}, "example": {"customer": {"password": "NewPassw0rd!"}}},
        "responses": {
            "201": {"description": "The password was reset.", "schema": {"$ref": "#/components/schemas/Message"}, "example": {"status": "success", "message": "Password has been changed successfully"}},
        },
    },
    {
        "key": "change_password",
        "slug": "change-a-password",
        "title": "Change a password",
        "method": "POST",
        "path": BASE + "/{customer_id}/change-password",
        "summary": "Change a password by giving the old one.",
        "description": "Changes the password when `old_password` matches. A wrong old password is answered `401`, and so is a customer who is still `awaiting_verification`, even straight after a reset. The SDKs return that `401` as it is and do not retry it.",
        "parameters": [CUSTOMER_ID],
        "body": {"schema": {"type": "object", "required": ["customer"], "properties": {"customer": {"type": "object", "required": ["email", "old_password", "password"], "properties": {"email": {"type": "string", "format": "email"}, "old_password": {"type": "string"}, "password": {"type": "string"}}}, "transaction_no": {"type": "string", "description": "Optional reference for this write."}}}, "example": {"customer": {"email": "jane@example.com", "old_password": "OldPassw0rd!", "password": "NewPassw0rd!"}}},
        "responses": {
            "200": {"description": "The password was changed.", "schema": {"$ref": "#/components/schemas/Message"}, "example": {"status": "success", "message": "Password has been changed successfully"}},
            "401": {"description": "The old password is wrong, or the customer has no usable login yet."},
        },
    },
    {
        "key": "bulk_reset_passwords",
        "slug": "bulk-reset-passwords",
        "title": "Bulk reset passwords",
        "method": "POST",
        "path": BASE + "/bulk-reset-password",
        "summary": "Email a password reset to several customers.",
        "description": "Queues a password reset email for each id. Ids that match no customer are returned in `skipped` with a reason rather than failing the call. An empty list, or ids that are not integers, is refused with `400`.",
        "body": {"schema": {"type": "object", "required": ["customer_ids"], "properties": {"customer_ids": {"type": "array", "items": {"type": "integer"}}}}, "example": {"customer_ids": [123, 124]}},
        "responses": {
            "202": {"description": "The resets were queued.", "schema": {"type": "object", "properties": {"queued": {"type": "array", "items": {"type": "integer"}}, "skipped": {"type": "array", "items": {"type": "object", "properties": {"customer_id": {"type": "integer"}, "reason": {"type": "string"}}}}, "total_queued": {"type": "integer"}, "requested": {"type": "integer"}, "status": {"type": "string"}, "message": {"type": "string"}}}, "example": {"queued": [123, 124], "skipped": [], "total_queued": 2, "requested": 2, "status": "queued", "message": "Password reset emails queued for 2 of 2 customers."}},
        },
    },
    {
        "key": "import_customers",
        "slug": "import-customers",
        "title": "Import customers",
        "method": "POST",
        "path": BASE + "/import",
        "summary": "Create or update customers from a CSV or spreadsheet file.",
        "description": "Upload one file in a multipart part named exactly `file`. The filename's extension picks the parser: `.csv`, `.xls` or `.xlsx`. A row with a `customer_id` updates that customer; a row without one creates a customer. The call can answer `201` even when rows failed, so check `failed` and `errors`.",
        "multipart": True,
        "body": {"schema": {"type": "object", "required": ["file"], "properties": {"file": {"type": "string", "format": "binary", "description": "The file to import."}}}},
        "responses": {
            "201": {"description": "The import result.", "schema": {"type": "object", "properties": {"total": {"type": "integer"}, "created": {"type": "integer"}, "updated": {"type": "integer"}, "failed": {"type": "integer"}, "errors": {"type": "array", "items": {"type": "object"}}}}, "example": {"total": 1, "created": 0, "updated": 1, "failed": 0, "errors": []}},
        },
    },
    {
        "key": "list_store_credit_adjustments",
        "slug": "list-store-credit-adjustments",
        "title": "List store credit adjustments",
        "method": "GET",
        "path": BASE + "/{customer_id}/store-credit/adjustments",
        "summary": "A customer's store credit movements, newest first.",
        "description": "Returns the customer's store credit adjustments one page at a time, newest first. Only the paging parameters apply: other parameters, including `sort` and a filter on `action`, are accepted and ignored.",
        "parameters": [CUSTOMER_ID, LIMIT, OFFSET, PAGE],
        "responses": {
            "200": {"description": "A page of adjustments.", "schema": {"type": "object", "properties": {"store_credit_adjustments": {"type": "array", "items": {"$ref": "#/components/schemas/StoreCreditAdjustment"}}, "pagination": {"$ref": "#/components/schemas/Pagination"}}}, "example": {"store_credit_adjustments": [{"id": 7, "customer_id": 123, "action": "add", "amount": 20.0, "note": "Refund", "balance_before": 0.0, "balance_after": 20.0, "created_at": "2026-09-01T10:00:00Z"}], "pagination": dict(SAMPLE_PAGINATION, total=1, count=1, total_pages=1, has_next=False, next_page=None)}},
        },
    },
    {
        "key": "adjust_store_credit",
        "slug": "adjust-store-credit",
        "title": "Adjust store credit",
        "method": "POST",
        "path": BASE + "/{customer_id}/store-credit/adjustments",
        "summary": "Add to or deduct from a customer's store credit.",
        "description": "The body is the adjustment itself, with no wrapping key. `action` is `add` or `deduct` and carries the direction; `amount` is always positive. The answer carries the adjustment and the balance it left.",
        "parameters": [CUSTOMER_ID],
        "body": {"schema": {"$ref": "#/components/schemas/StoreCreditAdjustmentInput"}, "example": {"action": "add", "amount": 20, "note": "Refund"}},
        "responses": {
            "201": {"description": "The adjustment and the new balance.", "schema": {"type": "object", "properties": {"store_credit_adjustment": {"$ref": "#/components/schemas/StoreCreditAdjustment"}, "store_credit": {"type": "number"}}}, "example": {"store_credit_adjustment": {"id": 8, "customer_id": 123, "action": "add", "amount": 20.0, "note": "Refund", "balance_before": 0.0, "balance_after": 20.0}, "store_credit": 20.0}},
        },
    },
]


def nullable(kind, **extra):
    return dict({"type": kind}, **extra)


REFERENCE = {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "code": {"type": "string"}}}

ERROR_EXAMPLE = {"status": "error", "code": 400, "message": "invalid customer id", "error": "validation_failed", "errors": [{"field": "id", "code": "invalid_id", "message": "customer id must be numeric"}]}

SCHEMAS = {
    "Reference": REFERENCE,
    "Address": {"type": "object", "properties": {
        "id": {"type": "integer"}, "type": {"type": "string", "description": "`primary`, `shipping` or `billing`."},
        "first_name": {"type": "string"}, "last_name": {"type": "string"}, "email": {"type": "string"},
        "company_name": {"type": "string"}, "address_line_1": {"type": "string"}, "address_line_2": {"type": "string"},
        "country": {"$ref": "#/components/schemas/Reference"}, "state": {"$ref": "#/components/schemas/Reference"},
        "city": {"type": "string"}, "post_code": {"type": "string"}, "mobile": {"type": "string"},
        "phone": {"type": "string"}, "fax": {"type": "string"},
    }},
    "AddressInput": {"type": "object", "required": ["type"], "properties": {
        "type": {"type": "string", "enum": ["primary", "shipping", "billing"]},
        "first_name": {"type": "string"}, "last_name": {"type": "string"}, "company_name": {"type": "string"},
        "address_line_1": {"type": "string"}, "address_line_2": {"type": "string"}, "city": {"type": "string"},
        "post_code": {"type": "string"}, "country": {"type": "string"}, "state": {"type": "string"},
    }},
    "CustomProperty": {"type": "object", "properties": {"id": {"type": "integer"}, "label": {"type": "string"}, "description": {"type": "string"}}},
    "Customer": {"type": "object", "properties": {
        "customer_id": {"type": "integer", "description": "The id every `{customer_id}` path takes."},
        "internal_id": {"type": "integer", "description": "A second id space over the same records. No path takes it."},
        "first_name": {"type": "string"}, "last_name": {"type": "string"}, "name": {"type": "string"},
        "email": {"type": "string"}, "status": {"type": "string", "enum": STATUS_VALUES},
        "gender": {"type": "string"}, "company_name": {"type": "string"}, "store_credit": {"type": "number"},
        "customer_groups": {"type": "array", "items": {"$ref": "#/components/schemas/Reference"}},
        "addresses": {"type": "array", "items": {"$ref": "#/components/schemas/Address"}},
        "custom_properties": {"type": "array", "items": {"$ref": "#/components/schemas/CustomProperty"}},
        "abn": {"type": "string"}, "credit_limit": {"type": "number"}, "allow_credit_limit": {"type": "boolean"},
        "account_hold": {"type": "boolean"}, "hide_price": {"type": "boolean"}, "sms_subscribed": {"type": "boolean"},
        "default_tax_code": {"type": "string"}, "note": {"type": "string"}, "source": {"type": "string"},
        "timezone": {"type": "string"}, "created_at": {"type": "string"}, "updated_at": {"type": "string"},
    }},
    "CustomerInput": {"type": "object", "properties": {
        "first_name": {"type": "string", "description": "Required on create."},
        "last_name": {"type": "string"}, "email": {"type": "string", "format": "email"},
        "password": {"type": "string"},
        "status": {"type": "string", "enum": STATUS_VALUES, "description": "Omit on create and the customer is `awaiting_verification`."},
        "company": {"type": "boolean"}, "company_name": {"type": "string"},
        "custom_properties": {"type": "array", "description": "Replaces the whole list.", "items": {"type": "object", "properties": {"label": {"type": "string"}, "description": {"type": "string"}}}},
    }},
    "StoreCreditAdjustment": {"type": "object", "properties": {
        "id": {"type": "integer"}, "customer_id": {"type": "integer"}, "internal_id": {"type": "integer"},
        "action": {"type": "string", "enum": ["add", "deduct"]}, "amount": {"type": "number"}, "note": {"type": "string"},
        "created_at": {"type": "string"}, "balance_before": {"type": "number"}, "balance_after": {"type": "number"},
    }},
    "StoreCreditAdjustmentInput": {"type": "object", "required": ["action", "amount"], "properties": {
        "action": {"type": "string", "enum": ["add", "deduct"], "description": "The direction of the movement."},
        "amount": {"type": "number", "description": "Always positive; `action` carries the sign."},
        "note": {"type": "string"},
    }},
    "Pagination": {"type": "object", "properties": {
        "total": {"type": "integer"}, "limit": {"type": "integer"}, "offset": {"type": "integer"},
        "count": {"type": "integer"}, "current_page": {"type": "integer"}, "total_pages": {"type": "integer"},
        "has_next": {"type": "boolean"}, "has_previous": {"type": "boolean"},
        "previous_page": {"type": "string"}, "next_page": {"type": "string"},
    }},
    "Message": {"type": "object", "properties": {"message": {"type": "string"}, "status": {"type": "string"}}},
    "Error": {"type": "object", "properties": {
        "status": {"type": "string", "example": "error"}, "code": {"type": "integer"}, "message": {"type": "string"},
        "error": {"type": "string", "description": "A machine-readable reason, when the API gives one."},
        "errors": {"type": "array", "description": "One entry per rejected field, when the API gives them.", "items": {"type": "object", "properties": {"field": {"type": "string"}, "code": {"type": "string"}, "message": {"type": "string"}}}},
    }},
}
