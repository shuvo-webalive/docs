"""The Order custom fields endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Order custom fields"
SLUG = "order-custom-fields"
BASE = "/admin/order_custom_fields"
ICON = "clipboard-list"

OVERVIEW_DESCRIPTION = "List, count and retrieve the custom fields your store's orders can have, and check a timeslot against an order limit."
INTRO = "The Order custom fields API has four endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/order_custom_fields`."

LIST_PAGE = "/api-reference/order-custom-fields/list-order-custom-fields"
COUNT_PAGE = "/api-reference/order-custom-fields/count-order-custom-fields"
RETRIEVE_PAGE = "/api-reference/order-custom-fields/retrieve-an-order-custom-field"
VALIDATE_PAGE = "/api-reference/order-custom-fields/validate-a-timeslot"

WARNING = (
    "**Validating a timeslot stores nothing, even though it returns `201`.**\n"
    "  [Validate a timeslot](" + VALIDATE_PAGE + ") does not reserve the timeslot or change the field: the\n"
    "  field's `last_updated_on` and the number of order custom fields stay the same, and the same check\n"
    "  sent again returns the same result. The status is `201` whether the timeslot is available or not,\n"
    "  so read `valid` in the response."
)

NOTES = [
    "**You can read order custom fields, but not create, change or delete them.** `POST` on\n"
    "  `/admin/order_custom_fields`, and `PUT`, `PATCH` and `DELETE` on\n"
    "  `/admin/order_custom_fields/{order_custom_field_id}`, are rejected with `405 method_not_allowed` and\n"
    "  the message `HTTP method not allowed for this endpoint.` The listing's `group_meta` shows\n"
    "  `writable: false`. `OPTIONS` lists `HEAD` in its `Allow` header, but `HEAD` returns `404` on the\n"
    "  listing and on a field's path, and `405` on `/count`.",
    "**Send the timeslot keys at the top level of the body.** [Validate a timeslot](" + VALIDATE_PAGE + ")\n"
    "  takes `selected_date`, `weekday_id`, `start_hour`, `end_hour` and `order_limit` unwrapped. A body\n"
    "  wrapped in a key, such as `{\"validate_timeslot\": {...}}` or `{\"order_custom_field\": {...}}`, is\n"
    "  read as a body without `selected_date` and rejected with `400`. `selected_date` is required,\n"
    "  written `dd/MM/yyyy`, such as `25/10/2026`.",
    "**A listing returns at most 20 fields per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get every field, raise `offset` by the number of fields each page\n"
    "  returned until you reach `pagination.total`. `filterBy` keeps one field type, in the listing and in\n"
    "  the count. The query parameters `q`, `search`, `name`, `label` and `is_active` are accepted and\n"
    "  ignored: no parameter searches the fields.",
    "**`sort` takes its own names for five keys, not the names the response uses.** To sort by\n"
    "  `field_type`, `order_no`, `is_active`, `created_on` or `last_updated_on`, send `type`, `orderNo`,\n"
    "  `isActive`, `created` or `updated`. Those five response names are rejected with `400`, and so is a\n"
    "  leading `-`: set `dir` to `asc` or `desc` instead. `id`, `label` and `name` sort by the field's key\n"
    "  of the same name.",
    "**After a rejected query parameter, your next call can be rejected too.** When a query parameter is\n"
    "  rejected with `400`, your next call on the same client returns the same `400` if its endpoint reads\n"
    "  that parameter, even when that call's own parameters are valid. The listing reads all seven of its\n"
    "  parameters: `limit`, `offset`, `page`, `sort`, `dir`, `filterBy` and `field_metadata`.\n"
    "  [Retrieve an order custom field](" + RETRIEVE_PAGE + ") reads `field_metadata`, and\n"
    "  [Count order custom fields](" + COUNT_PAGE + ") reads `filterBy`. Send that call again: the call\n"
    "  after it runs normally, and so does every call on a new client. A rejected timeslot body does not\n"
    "  affect the next call.",
]

FIELD_TYPES = [
    "longtext", "text", "displaytext", "single.select.radio", "single.select.dropdown",
    "multi.select.checkbox", "multi.select.list", "date", "time", "delivery",
]
INPUT_FORMATS = ["none", "email", "alphanumeric", "alphabetic", "number", "phone"]
SORT_VALUES = ["id", "label", "name", "type", "orderNo", "isActive", "created", "updated"]
METADATA_KEYS = [
    "id", "name", "label", "field_type", "input_format", "is_required", "has_max_length", "max_length",
    "is_active", "order_no", "hover_text", "placeholder", "default_value", "html_class", "options",
    "rate_id", "created_on", "last_updated_on",
]

ORDER_CUSTOM_FIELD_ID = {
    "name": "order_custom_field_id",
    "in": "path",
    "required": True,
    "description": "The order custom field's `id`, from a listing.",
    "schema": {"type": "integer", "example": 42},
}

LIMIT = {"name": "limit", "in": "query", "description": "Fields per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0`, a negative number and text are rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of fields to skip. When you send both `offset` and `page`, `offset` wins. A negative number or text is rejected with `400`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied: `page=2` alone skips 20 fields, and `limit=5&page=3` skips 10. `page=0` returns the first page. A negative number or text is rejected with `400`.", "schema": {"type": "integer", "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "What to sort the fields by: `id`, `label`, `name`, `type`, `orderNo`, `isActive`, `created` or `updated`. `type`, `orderNo`, `isActive`, `created` and `updated` sort by `field_type`, `order_no`, `is_active`, `created_on` and `last_updated_on`, in that order. Those five response key names, a leading `-` and any other value are rejected with `400`. An empty value is ignored.", "schema": {"type": "string", "enum": SORT_VALUES, "example": "label"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`, in any letter case, such as `DESC`. A value such as `sideways` is rejected with `400` and the message `dir: must be one of: asc, desc`. An empty value is ignored.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
FILTER_BY = {"name": "filterBy", "in": "query", "description": "Keeps only the fields of this type, and sets `pagination.total` to their number. Send the type exactly as `field_type` shows it, in lower case. `LONGTEXT`, or any value that is not one of the ten types, is rejected with `400`. An empty value is ignored.", "schema": {"type": "string", "enum": FIELD_TYPES, "example": "longtext"}}
COUNT_FILTER_BY = {"name": "filterBy", "in": "query", "description": "Counts only the fields of this type. Send the type exactly as the fields show it in `field_type`, in lower case, such as `date` or `single.select.dropdown`. `LONGTEXT`, or any value that is not one of the ten types, is rejected with `400`. An empty value is ignored.", "schema": {"type": "string", "enum": FIELD_TYPES, "example": "date"}}
LIST_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` or `1` to add `field_metadata`, which describes an order custom field's keys, including all 12 that a listed field has: each key's type and, for some keys, the allowed values or the maximum length. `false` and `0` add nothing. Any other value, including `True` and `TRUE`, is rejected with `400`.", "schema": {"type": "boolean", "example": True}}
FIELD_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` or `1` to add `field_metadata` beside the field. It describes the field's keys, except the four `is_allowed_for_*` keys: each key's type and, for some keys, the allowed values or the maximum length. `false` and `0` add nothing. Any other value, including `True` and `TRUE`, is rejected with `400`.", "schema": {"type": "boolean", "example": True}}

REQUEST_ID = "3b7e9c1a-2d4f-4e8b-9a6c-5f1d0e2b7c48"


def error(code, message, details=None):
    return {"error": {"code": code, "message": message, "details": details or [], "request_id": REQUEST_ID}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


NOT_FOUND = error("not_found", "Field not found")

ERROR_REF = ref("OrderCustomFieldError")
FIELD_METADATA_PROPERTY = dict(ref("OrderCustomFieldMetadata"), description="Only when you send `field_metadata=true` or `1`.")

SAMPLE_ROWS = [
    {"id": 43, "field_type": "longtext", "label": "Delivery instructions", "name": "delivery_instructions", "is_active": True, "order_no": None, "created_on": "2026-07-16T06:30:12Z", "last_updated_on": "2026-08-19T11:14:38Z", "is_required": False, "input_format": "none", "has_max_length": True, "max_length": 500},
    {"id": 44, "field_type": "text", "label": "Gift message", "name": "gift_message", "is_active": True, "order_no": None, "created_on": "2026-07-17T05:16:21Z", "last_updated_on": "2026-07-17T05:16:21Z", "is_required": False, "input_format": "none", "has_max_length": True, "max_length": 100},
    {"id": 42, "field_type": "date", "label": "Preferred delivery date", "name": "preferred_delivery_date", "is_active": True, "order_no": None, "created_on": "2026-07-16T06:24:24Z", "last_updated_on": "2026-08-16T14:19:53Z", "is_required": False, "input_format": "none", "has_max_length": False, "max_length": None},
]

SAMPLE_PAGINATION = {
    "total": 3, "limit": 20, "offset": 0, "count": 3, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

SAMPLE_GROUP_META = {"order_custom_fields": {"kind": "resource", "writable": False, "href": "/api/v4" + BASE}}

SAMPLE_FIELD = dict(
    SAMPLE_ROWS[2],
    hover_text="The day you would like your order delivered.",
    placeholder="dd/mm/yyyy",
    default_value=None,
    html_class=None,
    options=[],
    is_allowed_for_shipping=True,
    is_allowed_for_delivery=True,
    is_allowed_for_store_pickup=False,
    is_allowed_for_pre_order=False,
)

TIMESLOT_BODY = {"selected_date": "25/10/2026", "weekday_id": 1, "start_hour": 9, "end_hour": 12, "order_limit": 10}

ENDPOINTS = [
    {
        "key": "list_order_custom_fields",
        "slug": "list-order-custom-fields",
        "title": "List order custom fields",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 order custom fields per call, with the total and paging details.",
        "description": "Returns up to 20 of the store's order custom fields under `order_custom_fields`, each with 12 keys; [Retrieve an order custom field](" + RETRIEVE_PAGE + ") returns all 21. `pagination` gives the total number of matching fields and the page you are on, and `group_meta` marks the list read-only with `writable: false`. Send `filterBy` to keep one field type, `sort` and `dir` to order the fields, and `field_metadata=true` to add a description of each key. `q`, `search`, `name`, `label`, `is_active` and unknown parameters are accepted and ignored: no parameter searches the fields.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, DIR, FILTER_BY, LIST_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The fields on this page under `order_custom_fields`, `pagination` with the total and the page size, and `group_meta`, which shows `writable: false`. With `field_metadata=true`, the response also has a `field_metadata` key. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "order_custom_fields": {"type": "array", "items": ref("OrderCustomFieldSummary")},
                    "pagination": ref("OrderCustomFieldPagination"),
                    "group_meta": ref("OrderCustomFieldGroupMeta"),
                    "field_metadata": FIELD_METADATA_PROPERTY,
                }},
                "example": {"order_custom_fields": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION, "group_meta": SAMPLE_GROUP_META},
            },
            "400": {
                "description": "You sent a value the listing rejects. `limit=0` is rejected with the message `'limit' must be a positive integer`. A negative or non-numeric `limit`, `offset` or `page` is rejected with `'<name>' must be a non-negative integer` and `details[0].code` set to `invalid_integer`. A `sort` other than the eight accepted values is rejected with `sort: must be one of: id, label, name, type, orderNo, isActive, created, updated` and `details[0].code` set to `invalid_value`. A `dir` such as `sideways` is rejected with `dir: must be one of: asc, desc`. A `filterBy` that is not one of the ten field types is rejected with `details[0].code` set to `invalid_enum`. A `field_metadata` other than `true`, `false`, `1` or `0` is rejected with `field_metadata must be true/false or 0/1` and `details[0].code` set to `invalid_boolean`. You also get this `400` when the call just before this one on the same client was rejected for one of these parameters, including a `filterBy` rejected by [Count order custom fields](" + COUNT_PAGE + ") and a `field_metadata` rejected by [Retrieve an order custom field](" + RETRIEVE_PAGE + "); send the call again.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "sort=label&dir=asc"},
    },
    {
        "key": "count_order_custom_fields",
        "slug": "count-order-custom-fields",
        "title": "Count order custom fields",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of order custom fields, or of one field type with `filterBy`.",
        "description": "Returns the number of order custom fields as `count`, the only key in the body. The number matches `pagination.total` from [List order custom fields](" + LIST_PAGE + "). Send `filterBy` to count only the fields of one type. `limit`, `sort`, `field_metadata` and unknown parameters are ignored, even a `sort` the listing rejects.",
        "parameters": [COUNT_FILTER_BY],
        "responses": {
            "200": {
                "description": "The number of order custom fields in `count`, or the number of the type you sent in `filterBy`.",
                "schema": {"type": "object", "properties": {"count": {"type": "integer", "description": "The number of order custom fields, or of the `filterBy` type."}}},
                "example": {"count": 1},
            },
            "400": {
                "description": "You sent a `filterBy` that is not one of the ten field types, such as `LONGTEXT`. The message is `filterBy: must be one of: longtext, text, displaytext, single.select.radio, single.select.dropdown, multi.select.checkbox, multi.select.list, date, time, delivery` and `details[0].code` is `invalid_enum`. You also get this `400` when the call just before this one on the same client was rejected for its `filterBy`; send the call again.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "filterBy=date"},
    },
    {
        "key": "get_order_custom_field",
        "slug": "retrieve-an-order-custom-field",
        "title": "Retrieve an order custom field",
        "method": "GET",
        "path": BASE + "/{order_custom_field_id}",
        "summary": "Returns the order custom field whose `id` you pass as `order_custom_field_id`, with all 21 keys.",
        "description": "Returns one order custom field under the `order_custom_field` key, with 21 keys. These are the 12 keys a listing returns, with the same values, plus `hover_text`, `placeholder`, `default_value`, `html_class`, `options` and the four `is_allowed_for_*` keys. Send `field_metadata=true` to add a description of the field's keys beside it; it leaves out the four `is_allowed_for_*` keys. Unknown query parameters are ignored, and the response has no `ETag` header.",
        "parameters": [ORDER_CUSTOM_FIELD_ID, FIELD_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The order custom field under `order_custom_field`, with all 21 keys. With `field_metadata=true`, the response also has a `field_metadata` key beside it.",
                "schema": {"type": "object", "properties": {
                    "order_custom_field": ref("OrderCustomField"),
                    "field_metadata": FIELD_METADATA_PROPERTY,
                }},
                "example": {"order_custom_field": SAMPLE_FIELD},
            },
            "400": {
                "description": "You sent a `field_metadata` other than `true`, `false`, `1` or `0`, such as `True`. You also get this `400` when the call just before this one on the same client was rejected for its `field_metadata`; send the call again.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "No order custom field has that `order_custom_field_id`. The `code` is `not_found` and the message is `Field not found`.",
                "schema": ERROR_REF,
                "example": NOT_FOUND,
            },
        },
        "example_call": {"path": {"order_custom_field_id": 42}},
    },
    {
        "key": "validate_order_custom_field_timeslot",
        "slug": "validate-a-timeslot",
        "title": "Validate a timeslot",
        "method": "POST",
        "path": BASE + "/{order_custom_field_id}/validate_timeslot",
        "summary": "Checks a timeslot against an order limit and returns whether it is available. Stores nothing.",
        "description": "Checks a date and timeslot against an order limit, for the order custom field whose `id` you pass as `order_custom_field_id`, and returns `valid` and `message`. Send the keys at the top level of the body: `selected_date`, written `dd/MM/yyyy`, is required, and `start_hour` and `end_hour` are required when `order_limit` is above `0`. An `order_limit` of `0` returns `valid: false`, and a negative `order_limit`, or none, returns `valid: true`. Nothing is stored, and the field does not need to be a `delivery` field.",
        "parameters": [ORDER_CUSTOM_FIELD_ID],
        "body": {"schema": ref("OrderCustomFieldTimeslotInput"), "example": TIMESLOT_BODY},
        "responses": {
            "201": {
                "description": "The result: `valid` is `true` with the message `Timeslot available`, or `false` with `Timeslot fully booked`. Nothing is stored, and the response has no `Location` header.",
                "schema": ref("OrderCustomFieldTimeslotResult"),
                "example": {"valid": True, "message": "Timeslot available"},
            },
            "400": {
                "description": "The body was rejected. `{}` or a JSON array is rejected with the message `Request body required`. Any other body without `selected_date`, including one wrapped in a key, is rejected with `selected_date: is required, in dd/MM/yyyy form, e.g. 25/07/2026`. `details[].code` gives the reason: `required` when `selected_date` is missing, empty or `null`; `invalid_date` when it is not a real date written `dd/MM/yyyy`, such as `31/02/2026` or `2026-10-25`; `invalid_type` when `weekday_id`, `start_hour`, `end_hour` or `order_limit` is not a whole number; `out_of_range` for an hour outside `0` to `23`. An `order_limit` above `0` sent without `start_hour` or `end_hour` is rejected, and the error says the missing hour `is required when order_limit is above 0`.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "No order custom field has that `order_custom_field_id`. The message is `Field not found`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"order_custom_field_id": 42}},
    },
]

SUMMARY_PROPERTIES = {
    "id": {"type": "integer", "description": "The order custom field's `id`, assigned by the store. Pass it as `order_custom_field_id` in a path."},
    "field_type": {"type": "string", "enum": FIELD_TYPES, "description": "The field's type, one of the ten values `filterBy` takes. `sort=type` sorts by it."},
    "label": {"type": "string", "maxLength": 500, "description": "The field's label, at most 500 characters. `sort=label` sorts by it."},
    "name": {"type": "string", "description": "The field's name. `sort=name` sorts by it."},
    "is_active": {"type": "boolean", "description": "Whether the field is active. `sort=isActive` sorts by it."},
    "order_no": {"type": ["integer", "null"], "description": "An integer that `sort=orderNo` sorts by, or `null`."},
    "created_on": {"type": "string", "description": "When the field was created. `sort=created` sorts by it."},
    "last_updated_on": {"type": "string", "description": "When the field last changed. `sort=updated` sorts by it."},
    "is_required": {"type": "boolean", "description": "Whether the field is required."},
    "input_format": {"type": "string", "enum": INPUT_FORMATS, "description": "The field's input format: `none`, `email`, `alphanumeric`, `alphabetic`, `number` or `phone`."},
    "has_max_length": {"type": "boolean", "description": "Whether the field has a maximum length."},
    "max_length": {"type": ["integer", "null"], "description": "The field's maximum length, or `null`."},
}

DETAIL_PROPERTIES = {
    "hover_text": {"type": ["string", "null"], "maxLength": 100, "description": "The field's hover text, at most 100 characters, or `null`."},
    "placeholder": {"type": ["string", "null"], "maxLength": 100, "description": "The field's placeholder text, at most 100 characters, or `null`."},
    "default_value": {"type": ["string", "null"], "maxLength": 500, "description": "The field's default value, at most 500 characters, or `null`."},
    "html_class": {"type": ["string", "null"], "maxLength": 100, "description": "The field's HTML class, at most 100 characters, or `null`."},
    "options": {"type": "array", "items": {"type": "string"}, "description": "The choices of a `single.select.radio`, `single.select.dropdown`, `multi.select.checkbox` or `multi.select.list` field, each a string. The list can be empty."},
    "is_allowed_for_shipping": {"type": "boolean", "description": "Whether the field is allowed for shipping. `field_metadata` does not describe it."},
    "is_allowed_for_delivery": {"type": "boolean", "description": "Whether the field is allowed for delivery. `field_metadata` does not describe it."},
    "is_allowed_for_store_pickup": {"type": "boolean", "description": "Whether the field is allowed for store pickup. `field_metadata` does not describe it."},
    "is_allowed_for_pre_order": {"type": "boolean", "description": "Whether the field is allowed for pre-orders. `field_metadata` does not describe it."},
}

SCHEMAS = {
    "OrderCustomFieldSummary": {"type": "object", "description": "The 12 keys each field has in a listing. [Retrieve an order custom field](" + RETRIEVE_PAGE + ") returns these, with the same values, and nine more.", "properties": SUMMARY_PROPERTIES},
    "OrderCustomField": {"type": "object", "description": "An order custom field with all 21 keys, as [Retrieve an order custom field](" + RETRIEVE_PAGE + ") returns it.", "properties": dict(SUMMARY_PROPERTIES, **DETAIL_PROPERTIES)},
    "OrderCustomFieldPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of order custom fields that match your request: all of them, or those of the `filterBy` type."},
        "limit": {"type": "integer", "description": "The page size the store applied: the `limit` you sent, at most `20`, or `20` when you send none."},
        "offset": {"type": "integer", "description": "The number of fields skipped before this page."},
        "count": {"type": "integer", "description": "The number of fields on this page."},
        "current_page": {"type": "integer", "description": "The number of this page: `1` at `offset=0`, and also `1` when no field matches. For an `offset` past the last field, the number of the last page."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up. `0` when no field matches."},
        "has_next": {"type": "boolean", "description": "Whether a page comes after this one."},
        "has_previous": {"type": "boolean", "description": "Whether a page comes before this one. `false` on the first page, and also `false` for an `offset` past the last field."},
        "previous_page": {"type": ["string", "null"], "description": "The previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The next page, or `null` on the last page."},
    }},
    "OrderCustomFieldGroupMeta": {"type": "object", "description": "Returned only by [List order custom fields](" + LIST_PAGE + "), with one entry.", "properties": {
        "order_custom_fields": ref("OrderCustomFieldResourceMeta"),
    }},
    "OrderCustomFieldResourceMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "`resource` for this list."},
        "writable": {"type": "boolean", "description": "`false`: you cannot create, change or delete order custom fields through the API."},
        "href": {"type": "string", "description": "The listing's own path, `/api/v4/admin/order_custom_fields`."},
    }},
    "OrderCustomFieldMetadata": {"type": "object", "description": "Describes 18 order custom field keys, one entry per key name. Returned only when you send `field_metadata=true` or `1`. The `field_type` entry lists the ten field types and `input_format` the six input formats; `options` applies to the four select types and `rate_id` to `delivery` fields. The `label`, `hover_text`, `placeholder`, `default_value` and `html_class` entries give their maximum lengths. It describes `rate_id`, which neither a listing nor [Retrieve an order custom field](" + RETRIEVE_PAGE + ") returns, and leaves out the four `is_allowed_for_*` keys that a retrieved field has.", "properties": {
        key: ref("OrderCustomFieldMetadataEntry") for key in METADATA_KEYS
    }},
    "OrderCustomFieldMetadataEntry": {"type": "object", "additionalProperties": True, "description": "Describes one key. Every entry has `type`; the other keys differ from entry to entry.", "properties": {
        "type": {"type": "string", "description": "The kind of value the key holds."},
        "values": {"type": "array", "items": {"type": "string"}, "description": "The allowed values, such as the ten field types on the `field_type` entry."},
        "read_only": {"type": "boolean", "description": "`true` on the entries for the field's `id`, `name`, `created_on` and `last_updated_on`."},
    }},
    "OrderCustomFieldTimeslotInput": {"type": "object", "required": ["selected_date"], "description": "Send these keys at the top level of the body, not wrapped in a key. Other keys, such as `field_name`, are accepted with any value.", "properties": {
        "selected_date": {"type": "string", "example": "25/10/2026", "description": "Required. A real date written `dd/MM/yyyy`, such as `25/10/2026`; a date in the past is accepted. `31/02/2026`, `2026-10-25`, `5/1/2026`, a number and a date with spaces around it are rejected with `400`."},
        "weekday_id": {"type": "integer", "description": "A whole number. Its range is not checked: `0`, `9` and `-3` are all accepted."},
        "start_hour": {"type": "integer", "minimum": 0, "maximum": 23, "description": "The timeslot's start hour, a whole number from `0` to `23`. Required when `order_limit` is above `0`."},
        "end_hour": {"type": "integer", "minimum": 0, "maximum": 23, "description": "The timeslot's end hour, a whole number from `0` to `23`. Required when `order_limit` is above `0`. It is not checked against `start_hour`."},
        "order_limit": {"type": "integer", "description": "A whole number. `0` returns `valid: false`; a negative number, or no `order_limit`, returns `valid: true`. Above `0`, send `start_hour` and `end_hour` too."},
    }},
    "OrderCustomFieldTimeslotResult": {"type": "object", "properties": {
        "valid": {"type": "boolean", "description": "`true` when the timeslot is available, `false` when it is fully booked."},
        "message": {"type": "string", "description": "`Timeslot available` when `valid` is `true`, and `Timeslot fully booked` when it is `false`."},
    }},
    "OrderCustomFieldError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What went wrong, such as `Field not found` or `field_metadata must be true/false or 0/1`."},
        "details": {"type": "array", "description": "One entry per rejected body key or query parameter. Empty on a `404` or a `405`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The body key or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `invalid_date`, `invalid_type`, `out_of_range`, `invalid_value`, `invalid_enum`, `invalid_integer` or `invalid_boolean`."},
            "message": {"type": ["string", "null"], "description": "`null` when `limit`, `offset`, `page` or `field_metadata` was rejected."},
            "value": {"description": "The value you sent. Left out when the reason is `required`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
