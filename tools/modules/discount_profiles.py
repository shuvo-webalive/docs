"""The Discount profiles endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Discount profiles"
SLUG = "discount-profiles"
BASE = "/admin/discount_profiles"
ICON = "tags"

ASSIGN_PATH = "/admin/discount_coupons/assign-customer"

CREATE_PAGE = "/api-reference/discount-profiles/create-a-discount-profile"
RETRIEVE_PAGE = "/api-reference/discount-profiles/retrieve-a-discount-profile"
REPLACE_PAGE = "/api-reference/discount-profiles/replace-a-discount-profile"
COUPONS_PAGE = "/api-reference/discount-profiles/generate-coupon-codes"
ASSIGN_PAGE = "/api-reference/discount-profiles/assign-a-coupon-code-to-a-customer"

OVERVIEW_DESCRIPTION = "List, create, replace and delete discount profiles, generate coupon codes for a profile, and assign a code to a customer."
INTRO = "The Discount profiles API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/discount_profiles`, except [Assign a coupon code to a customer](" + ASSIGN_PAGE + "), which is `/api/v4/admin/discount_coupons/assign-customer`."

WARNING = (
    "**Replacing a discount profile resets every flag, date and limit you leave out of the body.** On `PUT`,\n"
    "  an omitted `is_*` flag becomes `false`, `start_date` becomes `null`, `end_date` becomes `\"\"`, and\n"
    "  `maximum_use_count`, `maximum_use_customer_count` and `maximum_discount_allowed_amount` become\n"
    "  `null`. Send every value you want to keep, and always send the details block of the profile's\n"
    "  `discount_details_type`: without it the call returns `500` and changes nothing."
)

NOTES = [
    "**Send a profile at the top level of the body, not inside `discount_profile`.** Create and replace\n"
    "  take the fields unwrapped, and responses return the profile inside `discount_profile`. A create\n"
    "  wrapped in `discount_profile` is rejected with `400` and the message\n"
    "  `name: Discount profile name is required`. A create drops any top-level field the store does not\n"
    "  know, without an error.",
    "**Each profile has one details block, chosen by `discount_details_type`.** `amount` uses\n"
    "  `amount_details`, `shipping` uses `shipping_details` and `product` uses `product_details`. A profile\n"
    "  returns only its own block, and the other two keys are absent. A create with a missing or empty block\n"
    "  is rejected with `400`, but a block without a field the store needs returns `500 internal_error` and\n"
    "  stores nothing: a `single` `amount_details` needs `type`, `apply_to`, `single_amount` and\n"
    "  `single_amount_type`, a `shipping_details` needs `apply_to` and `minimum_qty_on`, and a\n"
    "  `product_details` needs `free_product_min_qty_on`.",
    "**Dates go in as `yyyy-MM-dd HH:mm:ss` and come back in UTC.** The store reads `start_date` and\n"
    "  `end_date` in its own time zone and returns them converted to UTC as `yyyy-MM-ddTHH:mm:ss`, with no\n"
    "  zone suffix, so the time you read back can differ from the time you sent. A profile without dates\n"
    "  returns `start_date` as `null` and `end_date` as `\"\"`. A create stores `end_date` only when the\n"
    "  same body sets `is_specify_end_date` to `true`.",
    "**The listing returns at most 20 profiles per call and ignores unknown query parameters.** A larger\n"
    "  `limit` is capped at `20`. The listing reads only `limit`, `offset`, `page`, `sort`, `dir`, `type`,\n"
    "  `name` and `field_metadata`: any other parameter, such as `q`, `search` or `is_active`, is ignored, so\n"
    "  a misspelt filter returns the unfiltered listing. `dir` sorts descending when it is absent, empty or\n"
    "  exactly `desc`, and ascending for any other value, `DESC` included.",
    "**Coupon codes belong to a profile.** [Generate coupon codes](" + COUPONS_PAGE + ") adds codes to a\n"
    "  profile that has `is_apply_coupon_code` set to `true`, and\n"
    "  [Assign a coupon code to a customer](" + ASSIGN_PAGE + ") gives a code to a customer by email\n"
    "  address. Errors from the assign call come as a flat body with `status`, `message` and\n"
    "  `detailsMessage`, not the `error` object the other calls return. Deleting a profile deletes its codes.",
    "**After a rejected read, the client's next call to the same endpoint can return the same error.**\n"
    "  After a listing is rejected with `400`, the next listing on that client can return the same `400`, even\n"
    "  when its own parameters are valid. After a `400` or `404` from\n"
    "  [Retrieve a discount profile](" + RETRIEVE_PAGE + "), the next read of an existing profile on that\n"
    "  client can return the same error. A client created after the rejection is not affected, so send the\n"
    "  call again on a new client.",
]

PROFILE_TYPES = ["customer", "promote_product", "offer_incentive_and_sell_more", "offer_coupon"]
DETAILS_TYPES = ["amount", "shipping", "product"]
SORT_FIELDS = ["id", "name", "type"]
SHARED_FIELDS = [
    "id", "uuid", "name", "type", "discount_details_type", "is_active", "start_date", "is_specify_end_date",
    "end_date", "is_apply_coupon_code", "default_coupon_code", "is_coupon_code_auto_generate",
    "is_create_unique_coupon_each_customer", "is_imported_coupon", "is_maximum_use_total", "maximum_use_count",
    "is_maximum_use_customer", "maximum_use_customer_count", "is_maximum_discount_allowed",
    "maximum_discount_allowed_amount", "is_exclude_products_on_sale", "is_discount_used_with_other_discount",
    "is_display_discount_information_prod_detail", "is_display_text_coupon", "display_text_coupon",
    "is_display_text_cart", "display_text_cart", "is_display_text_partial_discount_condition",
    "display_text_partial_discount_condition", "invoice_note", "exclude_products", "customer_coupons", "usage",
    "created_on", "last_updated_on",
]
DETAILS_KEYS = ["amount_details", "shipping_details", "product_details"]

DISCOUNT_PROFILE_ID = {
    "name": "discount_profile_id",
    "in": "path",
    "required": True,
    "description": "The discount profile's `id`, from a listing or from the response to creating the profile.",
    "schema": {"type": "integer", "example": 1001},
}

LIMIT = {"name": "limit", "in": "query", "description": "Profiles per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0` is rejected with `400` and the message `'limit' must be a positive integer`, and a negative number or text with `'limit' must be a non-negative integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of profiles to skip. When you send both `offset` and `page`, `offset` wins. A negative number or text is rejected with `400`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied. `page=0` returns the first page, and text is rejected with `400`.", "schema": {"type": "integer", "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "What to sort by: the profile's `id`, `name` or `type`. Without `sort`, the listing sorts by the profile's `id`. Sorting by `name` ignores letter case. Any other value, including `NAME`, `-name` and `created_on`, is rejected with `400`, the reason `invalid_sort_field` and the message `Sort field not exist`.", "schema": {"type": "string", "enum": SORT_FIELDS, "example": "name"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction. The listing sorts descending when `dir` is absent, empty or exactly `desc`, and ascending for any other value, `DESC` included. Send `asc` or `desc` in lower case.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
TYPE = {"name": "type", "in": "query", "description": "Keeps only profiles of this type: `customer`, `promote_product`, `offer_incentive_and_sell_more` or `offer_coupon`. An empty value keeps every profile. Any other value, including `OFFER_COUPON` and a comma-separated list, is rejected with `400` and the reason `invalid_enum`.", "schema": {"type": "string", "enum": PROFILE_TYPES, "example": "offer_coupon"}}
NAME = {"name": "name", "in": "query", "description": "Keeps only profiles whose `name` contains this text, in any letter case. `%` and `_` match only themselves.", "schema": {"type": "string", "example": "spring"}}
LIST_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` or `1` to add `field_metadata`, which describes every field of a profile. `false` adds nothing.", "schema": {"type": "boolean", "example": True}}
PROFILE_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add `field_metadata` beside the profile: the same description of every field that the listing returns.", "schema": {"type": "boolean", "example": True}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def flag(description):
    return {"type": "boolean", "description": description}


ERROR_REF = ref("DiscountProfileError")
PROFILE_RESPONSE = {"type": "object", "properties": {"discount_profile": ref("DiscountProfile")}}
FIELD_METADATA_PROPERTY = dict(ref("DiscountProfileFieldMetadata"), description="Only when you send `field_metadata=true`.")

COUPON_TEXT = "Use code SPRING40 at checkout"
CART_TEXT = "Spring sale discount applied"
PARTIAL_TEXT = "Add one more item to get the spring discount"

CREATE_BODY = {
    "name": "Spring 40 Off",
    "type": "offer_coupon",
    "discount_details_type": "amount",
    "amount_details": {"type": "single", "apply_to": "total_order", "single_amount": 40, "single_amount_type": "PERCENT"},
    "is_active": True,
    "start_date": "2026-11-06 09:30:00",
    "is_specify_end_date": True,
    "end_date": "2026-11-16 18:00:00",
    "is_apply_coupon_code": True,
    "default_coupon_code": "SPRING40",
    "is_maximum_use_total": True,
    "maximum_use_count": 100,
    "is_maximum_use_customer": True,
    "maximum_use_customer_count": 1,
    "is_maximum_discount_allowed": True,
    "maximum_discount_allowed_amount": 200,
    "is_display_text_coupon": True,
    "display_text_coupon": COUPON_TEXT,
    "is_display_text_cart": True,
    "display_text_cart": CART_TEXT,
    "is_display_text_partial_discount_condition": True,
    "display_text_partial_discount_condition": PARTIAL_TEXT,
}

CREATED_PROFILE = {
    "id": 1001,
    "uuid": "5b1f8c2e-7d4a-4e9b-a3c6-0f2d9e8b7a41",
    "name": "Spring 40 Off",
    "type": "offer_coupon",
    "discount_details_type": "amount",
    "amount_details": {"type": "single", "apply_to": "total_order", "single_amount": 40.0, "single_amount_type": "PERCENT", "minimum_amount_on": "each_item", "tiers": []},
    "is_active": True,
    "start_date": "2026-11-05T22:30:00",
    "is_specify_end_date": True,
    "end_date": "2026-11-16T07:00:00",
    "is_apply_coupon_code": True,
    "default_coupon_code": "SPRING40",
    "is_coupon_code_auto_generate": False,
    "is_create_unique_coupon_each_customer": False,
    "is_imported_coupon": False,
    "is_maximum_use_total": True,
    "maximum_use_count": 100,
    "is_maximum_use_customer": True,
    "maximum_use_customer_count": 1,
    "is_maximum_discount_allowed": True,
    "maximum_discount_allowed_amount": 200.0,
    "is_exclude_products_on_sale": False,
    "is_discount_used_with_other_discount": False,
    "is_display_discount_information_prod_detail": False,
    "is_display_text_coupon": True,
    "display_text_coupon": COUPON_TEXT,
    "is_display_text_cart": True,
    "display_text_cart": CART_TEXT,
    "is_display_text_partial_discount_condition": True,
    "display_text_partial_discount_condition": PARTIAL_TEXT,
    "invoice_note": None,
    "exclude_products": [],
    "customer_coupons": [],
    "usage": [],
    "created_on": "2026-10-07T03:15:42Z",
    "last_updated_on": "2026-10-07T03:15:42Z",
}

UPDATE_BODY = {
    "name": "Spring 50 Off",
    "type": "offer_coupon",
    "discount_details_type": "amount",
    "amount_details": {"type": "single", "apply_to": "total_order", "single_amount": 50, "single_amount_type": "PERCENT", "minimum_amount_on": "each_item"},
    "is_active": True,
    "start_date": "2026-11-06 09:30:00",
    "is_specify_end_date": True,
    "end_date": "2026-11-20 18:00:00",
    "is_apply_coupon_code": True,
    "is_maximum_use_total": True,
    "maximum_use_count": 150,
    "is_maximum_use_customer": True,
    "maximum_use_customer_count": 1,
    "is_maximum_discount_allowed": True,
    "maximum_discount_allowed_amount": 200,
    "is_display_text_coupon": True,
    "is_display_text_cart": True,
}

UPDATED_PROFILE = dict(
    CREATED_PROFILE,
    name="Spring 50 Off",
    amount_details=dict(CREATED_PROFILE["amount_details"], single_amount=50.0),
    end_date="2026-11-20T07:00:00",
    maximum_use_count=150,
    is_display_text_partial_discount_condition=False,
    last_updated_on="2026-10-07T04:02:18Z",
)

GENERATED_CODES = ["A1B2C3D4E5", "F6G7H8J9K0", "L1M2N3P4Q5"]
CUSTOMER_EMAIL = "jane.citizen@example.com"

RETRIEVED_PROFILE = dict(UPDATED_PROFILE, customer_coupons=[
    {"id": 5001, "code": GENERATED_CODES[0], "customer_email": CUSTOMER_EMAIL},
    {"id": 5002, "code": GENERATED_CODES[1], "customer_email": ""},
    {"id": 5003, "code": GENERATED_CODES[2], "customer_email": ""},
])

LOYAL_PROFILE = {
    "id": 1002,
    "uuid": "c3e9a1d7-2f6b-4a85-9d0e-7b4f1a6c2e93",
    "name": "Loyal Customers 15",
    "type": "customer",
    "discount_details_type": "amount",
    "amount_details": {"type": "single", "apply_to": "total_order", "single_amount": 15.0, "single_amount_type": "PERCENT", "minimum_amount_on": "each_item", "tiers": []},
    "is_active": True,
    "start_date": None,
    "is_specify_end_date": False,
    "end_date": "",
    "is_apply_coupon_code": True,
    "default_coupon_code": "LOYAL15",
    "is_coupon_code_auto_generate": False,
    "is_create_unique_coupon_each_customer": False,
    "is_imported_coupon": False,
    "is_maximum_use_total": False,
    "maximum_use_count": None,
    "is_maximum_use_customer": False,
    "maximum_use_customer_count": None,
    "is_maximum_discount_allowed": False,
    "maximum_discount_allowed_amount": None,
    "is_exclude_products_on_sale": False,
    "is_discount_used_with_other_discount": False,
    "is_display_discount_information_prod_detail": False,
    "is_display_text_coupon": False,
    "display_text_coupon": "",
    "is_display_text_cart": False,
    "display_text_cart": "",
    "is_display_text_partial_discount_condition": False,
    "display_text_partial_discount_condition": "",
    "invoice_note": None,
    "exclude_products": [],
    "customer_coupons": [],
    "usage": [],
    "created_on": "2026-10-07T05:10:33Z",
    "last_updated_on": "2026-10-07T05:10:33Z",
}

SAMPLE_PAGINATION = {
    "total": 2, "limit": 20, "offset": 0, "count": 2, "current_page": 1, "total_pages": 1,
    "has_next": False, "has_previous": False, "previous_page": None, "next_page": None,
}

SAMPLE_GROUP_META = {"discount_profiles": {"kind": "resource", "writable": True, "href": "/api/v4" + BASE}}

ENDPOINTS = [
    {
        "key": "list_discount_profiles",
        "slug": "list-discount-profiles",
        "title": "List discount profiles",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 discount profiles per call, newest first, with paging details.",
        "description": "Returns the discount profiles in `discount_profiles`, newest first, 20 per call unless you send a smaller `limit`. `pagination` gives the number of profiles that match your filters in `total`, and the URLs of the next and previous pages in `next_page` and `previous_page`. Send `name` to keep profiles whose name contains that text, `type` to keep one profile type, and `sort` with `dir` to change the order. A query parameter the listing does not read, such as `q`, `search` or `is_active`, is ignored, so a misspelt filter returns the unfiltered listing.",
        "parameters": [LIMIT, OFFSET, PAGE, SORT, DIR, TYPE, NAME, LIST_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "`discount_profiles` lists the profiles on this page. `pagination` gives `total`, `limit`, `offset`, `count`, `current_page`, `total_pages`, `has_next`, `has_previous`, `next_page` and `previous_page`, and `group_meta` gives the listing's own path in `href`. With `field_metadata=true`, the response also has a `field_metadata` key. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "discount_profiles": {"type": "array", "items": ref("DiscountProfile")},
                    "group_meta": ref("DiscountProfileGroupMeta"),
                    "pagination": ref("DiscountProfilePagination"),
                    "field_metadata": FIELD_METADATA_PROPERTY,
                }},
                "example": {"discount_profiles": [LOYAL_PROFILE, RETRIEVED_PROFILE], "group_meta": SAMPLE_GROUP_META, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a value the listing rejects: `limit=0` (message `'limit' must be a positive integer`), a negative or non-numeric `limit` (`'limit' must be a non-negative integer`), a negative or non-numeric `offset`, a non-numeric `page`, a `sort` other than `id`, `name` or `type` (reason `invalid_sort_field`, message `Sort field not exist`), or a non-empty `type` that is not one of the four profile types (reason `invalid_enum`). After a `400`, the next listing on the same client can return the same `400`, even when its own parameters are valid; send it again on a new client.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": "sort=name&dir=asc"},
    },
    {
        "key": "create_discount_profile",
        "slug": "create-a-discount-profile",
        "title": "Create a discount profile",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a discount profile and returns it with its `id`, which other calls take as `discount_profile_id`.",
        "description": "Creates a discount profile from the fields you send at the top level of the body, not wrapped in `discount_profile`, and returns the new profile. `name`, `discount_details_type` and the details block it names are required: `amount_details` for `amount`, `shipping_details` for `shipping`, or `product_details` for `product`. Dates go in as `yyyy-MM-dd HH:mm:ss` and come back converted to UTC as `yyyy-MM-ddTHH:mm:ss`. A `product_details` with keys the store does not recognise can return `500` and still store the profile, so after a `500`, list profiles by `name` before you send the create again.",
        "body": {"schema": ref("DiscountProfileCreate"), "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new discount profile under `discount_profile`, with the details block its `discount_details_type` names and no other. `minimum_amount_on` defaults to `each_item`, a `type` you leave out is returned as `\"\"`, and the dates come back in UTC. The response has no `Location` header.",
                "schema": PROFILE_RESPONSE,
                "example": {"discount_profile": CREATED_PROFILE},
            },
            "400": {
                "description": "The body was rejected and nothing was stored. A field is rejected when `name` is missing, as in a body wrapped in `discount_profile` (message `name: Discount profile name is required`), over 255 characters (reason `too_long`) or contains `<`, `>`, `javascript:` or `expression()` (reason `invalid_character`); `discount_details_type` is missing (the message says `is required; one of amount, shipping, product`); the details block it names is missing or empty (message such as `amount_details: is required when discount_details_type is amount`); `type` is not one of the four profile types (reason `invalid_enum`); in a `single` `amount_details`, `single_amount_type` is not `FLAT` or `PERCENT` (reason `invalid_enum`), or `single_amount` is negative or a `PERCENT` value above `100` (reason `out_of_range`); `start_date` is not a real date and time in `yyyy-MM-dd HH:mm:ss` form (reason `invalid_date`); `end_date` is before `start_date` while `is_specify_end_date` is `true` (reason `invalid_range`); or `is_specify_end_date` or `is_imported_coupon` is a string (reason `invalid_boolean`). The body is also rejected when `default_coupon_code` is already used by another coupon (`Coupon code#<code> already exists`), when it sends the profile's `id`, which the store sets itself (reason `read_only_field`), when it is `{}` (`request body is empty`), and when it is not a JSON object (`request body must be a JSON object`).",
                "schema": ERROR_REF,
            },
            "409": {
                "description": "Another profile already has that `name`, in any letter case. The reason is `conflict` and the message is `Discount Name already exists`.",
                "schema": ERROR_REF,
            },
            "500": {
                "description": "A details block lacks a field the store needs (reason `internal_error`), or `exclude_products` has a product `id` that no product has. In both cases nothing is stored. A `single` `amount_details` needs `type`, `apply_to`, `single_amount` and `single_amount_type`, a `shipping_details` needs `apply_to` and `minimum_qty_on`, and a `product_details` needs `free_product_min_qty_on`. A `product_details` with keys the store does not recognise can also return `500` and still store the profile, so list profiles by `name` before you send the create again.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {},
    },
    {
        "key": "get_discount_profile",
        "slug": "retrieve-a-discount-profile",
        "title": "Retrieve a discount profile",
        "method": "GET",
        "path": BASE + "/{discount_profile_id}",
        "summary": "Returns the discount profile whose `id` you pass as `discount_profile_id`, with its coupon codes.",
        "description": "Returns the profile whose `id` you pass as `discount_profile_id` under the `discount_profile` key, with the same fields the listing returns for it, including its coupon codes in `customer_coupons`. Send `field_metadata=true` to add a description of every field beside the profile. After a `400` or `404`, the next read of an existing profile on the same client can return the same error; send it again on a new client. The response has no `ETag` or `Last-Modified` header.",
        "parameters": [DISCOUNT_PROFILE_ID, PROFILE_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The discount profile under `discount_profile`. With `field_metadata=true`, the response also has a `field_metadata` key beside it.",
                "schema": {"type": "object", "properties": {
                    "discount_profile": ref("DiscountProfile"),
                    "field_metadata": FIELD_METADATA_PROPERTY,
                }},
                "example": {"discount_profile": RETRIEVED_PROFILE},
            },
            "400": {
                "description": "`discount_profile_id` is not a number, such as `abc` or `count`. The reason is `invalid_id` and the message is `id: must be a numeric discount profile id`. Right after this `400`, the next read on the same client can return it for an existing profile; send that read again on a new client.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "No discount profile has that `discount_profile_id`. The reason is `not_found` and the message is `Discount Profile not found`. A `discount_profile_id` with a decimal point, such as `1.5`, also returns `404`, with an HTML page instead of a JSON body. Right after a `404`, the next read on the same client can return this `404` for an existing profile; send that read again on a new client.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"discount_profile_id": 1001}},
    },
    {
        "key": "update_discount_profile",
        "slug": "replace-a-discount-profile",
        "title": "Replace a discount profile",
        "method": "PUT",
        "path": BASE + "/{discount_profile_id}",
        "summary": "Replaces a discount profile and returns it, resetting any flag, date or limit you leave out.",
        "description": "Replaces the profile whose `id` you pass as `discount_profile_id` with the fields you send at the top level of the body, and returns it; `PATCH` on this path is rejected with `405`. Every `is_*` flag you leave out becomes `false`, `start_date` becomes `null`, `end_date` becomes `\"\"`, and `maximum_use_count`, `maximum_use_customer_count` and `maximum_discount_allowed_amount` become `null`, while `name`, `type`, `default_coupon_code`, the three display texts, `invoice_note` and `exclude_products` keep their values. Always send the details block of the profile's `discount_details_type`: without it the call returns `500` and changes nothing. This call skips most checks a create makes: a `type` outside the four profile types, a `single_amount_type` outside `FLAT` and `PERCENT`, a negative `single_amount`, a `PERCENT` amount above `100` and an `end_date` before `start_date` are stored as sent, and a `start_date` that is not a date is stored as `null`.",
        "parameters": [DISCOUNT_PROFILE_ID],
        "body": {"schema": ref("DiscountProfileReplace"), "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The profile after the replace. When the body sets `is_apply_coupon_code` to `true`, this response shows `customer_coupons` as `[]` even when the profile has coupon codes: retrieve the profile to read them.",
                "schema": PROFILE_RESPONSE,
                "example": {"discount_profile": UPDATED_PROFILE},
            },
            "400": {
                "description": "`name` contains `<`, `>`, `javascript:` or `expression()` (reason `invalid_character`), or `is_specify_end_date` or `is_imported_coupon` is a string (reason `invalid_boolean`). Of the checks a create makes, only these two return `400` here.",
                "schema": ERROR_REF,
            },
            "404": {
                "description": "No discount profile has that `discount_profile_id`, for example because you deleted it. The message is `Discount not found`.",
                "schema": ERROR_REF,
            },
            "500": {
                "description": "The body has no details block for the profile's `discount_details_type` (message `Cannot get property 'type' on null object`), the block for a new `discount_details_type` lacks a field the store needs, or `name` is blank, over 255 characters or already used by another profile in any letter case (message `Discount Name already exists`). The reason is `internal_error`, and the profile does not change.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"discount_profile_id": 1001}},
    },
    {
        "key": "delete_discount_profile",
        "slug": "delete-a-discount-profile",
        "title": "Delete a discount profile",
        "method": "DELETE",
        "path": BASE + "/{discount_profile_id}",
        "summary": "Deletes a discount profile and its coupon codes permanently, and returns no body.",
        "description": "Deletes the profile whose `id` you pass as `discount_profile_id`, with all its coupon codes, and returns `204` with no body. The profile leaves the listing, and `pagination.total` falls by one. Retrieving, replacing or deleting it again returns `404`, and assigning one of its codes to a customer is rejected with `coupon.not.found.by.code`.",
        "parameters": [DISCOUNT_PROFILE_ID],
        "responses": {
            "204": {"description": "Deleted, with its coupon codes. No body."},
            "404": {"description": "No discount profile has that `discount_profile_id`, for example because you already deleted it.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"discount_profile_id": 1001}},
    },
    {
        "key": "create_discount_profile_coupons",
        "slug": "generate-coupon-codes",
        "title": "Generate coupon codes",
        "method": "POST",
        "path": BASE + "/{discount_profile_id}/create-coupons",
        "summary": "Generates new coupon codes for a discount profile and returns them in `codes`.",
        "description": "Generates the number of codes you send as `requested_codes` for the profile whose `id` you pass as `discount_profile_id`, and returns them in `codes`. The profile must have `is_apply_coupon_code` set to `true`, and the number goes at the top level of the body, such as `{\"requested_codes\": 3}`. The codes are added to the end of the profile's `customer_coupons` with an empty `customer_email`, and the profile's `last_updated_on` does not change. To give a code to a customer, use [Assign a coupon code to a customer](" + ASSIGN_PAGE + ").",
        "parameters": [DISCOUNT_PROFILE_ID],
        "body": {"schema": ref("DiscountProfileGenerateCodesInput"), "example": {"requested_codes": 3}},
        "responses": {
            "201": {
                "description": "The new codes in `codes`, with `status` set to `success` and `message` set to `<n> new codes generated.`, where `<n>` is the number of codes. The response has no `Location` header.",
                "schema": ref("DiscountProfileGeneratedCodes"),
                "example": {"status": "success", "message": "3 new codes generated.", "codes": GENERATED_CODES},
            },
            "400": {
                "description": "No codes were generated. `requested_codes` of `0` or missing, no body, or a body wrapped in a key is rejected with the reason `invalid_request` and the message `Invalid request data`, and a negative `requested_codes` with `Invalid number of requested codes`. A profile without `is_apply_coupon_code` is rejected with `Coupon code not allowed`, and a `discount_profile_id` that no profile has with `Invalid discount ID`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"path": {"discount_profile_id": 1001}},
    },
    {
        "key": "assign_discount_coupon_customer",
        "slug": "assign-a-coupon-code-to-a-customer",
        "title": "Assign a coupon code to a customer",
        "method": "POST",
        "path": ASSIGN_PATH,
        "summary": "Assigns a coupon code to an existing customer by email and returns `status` set to `success`.",
        "description": "Assigns a coupon code to the customer whose email address you send, and returns `status` set to `success`. Send `code` and `email` at the top level of the body: `code` is a code from [Generate coupon codes](" + COUPONS_PAGE + "), and `email` belongs to an existing customer, matched in any letter case, including a customer awaiting verification. The coupon's `customer_email` on the profile then shows that customer's email as their customer record spells it; the same pair sent again returns `201` again, and a code that is already assigned moves to the customer you name. Errors come as a flat body with `status`, `message` and `detailsMessage`, not the `error` object the other discount profile calls return.",
        "body": {"schema": ref("DiscountProfileAssignInput"), "example": {"code": GENERATED_CODES[0], "email": CUSTOMER_EMAIL}},
        "responses": {
            "201": {
                "description": "`status` is `success` and `message` is `customer has been assigned successfully.` The response has no `Location` header.",
                "schema": ref("DiscountProfileAssignResult"),
                "example": {"status": "success", "message": "customer has been assigned successfully."},
            },
            "400": {
                "description": "The code was not assigned. The body is flat, with `status` set to `error`. `detailsMessage` is `customer.not.found` when no customer has that `email`, with the message `Error customer assign to code`, and `coupon.not.found.by.code` when no coupon has that `code`, for example because you deleted its profile. A body without `email` or `code` is rejected with `Email is required` or `Code is required`, and a body wrapped in a key is rejected with `Code is required`.",
                "schema": ref("DiscountProfileAssignError"),
                "example": {"status": "error", "message": "Error customer assign to code", "detailsMessage": "customer.not.found"},
            },
        },
        "example_call": {},
    },
]

PROFILE_PROPERTIES = {
    "id": {"type": "integer", "description": "The discount profile's `id`, assigned by the store. Pass it as `discount_profile_id` in a path."},
    "uuid": {"type": "string", "description": "The profile's `uuid`, assigned by the store."},
    "name": {"type": "string", "maxLength": 255, "description": "The profile's name, unique in any letter case."},
    "type": {"type": "string", "description": "The profile type: `customer`, `promote_product`, `offer_incentive_and_sell_more` or `offer_coupon`, or `\"\"` when the profile was created without one. A replace stores any value you send, including one outside these four."},
    "discount_details_type": {"type": "string", "enum": DETAILS_TYPES, "description": "Which details block the profile has: `amount`, `shipping` or `product`."},
    "amount_details": dict(ref("DiscountProfileAmountDetails"), description="Only on a profile whose `discount_details_type` is `amount`."),
    "shipping_details": dict(ref("DiscountProfileShippingDetails"), description="Only on a profile whose `discount_details_type` is `shipping`."),
    "product_details": dict(ref("DiscountProfileProductDetails"), description="Only on a profile whose `discount_details_type` is `product`."),
    "is_active": flag("Whether the profile is active."),
    "start_date": {"type": ["string", "null"], "description": "When the discount starts, in UTC, written `yyyy-MM-ddTHH:mm:ss` with no zone suffix, or `null` when not set."},
    "is_specify_end_date": flag("Whether the profile has an `end_date`."),
    "end_date": {"type": "string", "description": "When the discount ends, in UTC, written `yyyy-MM-ddTHH:mm:ss` with no zone suffix, or `\"\"` when not set."},
    "is_apply_coupon_code": flag("Whether the profile uses coupon codes. [Generate coupon codes](" + COUPONS_PAGE + ") works only when this is `true`."),
    "default_coupon_code": {"type": ["string", "null"], "description": "The profile's default coupon code. It is not listed in `customer_coupons`."},
    "is_coupon_code_auto_generate": flag("Whether coupon codes are generated automatically."),
    "is_create_unique_coupon_each_customer": flag("Whether each customer gets a unique coupon code."),
    "is_imported_coupon": flag("Whether the coupon codes are imported."),
    "is_maximum_use_total": flag("Whether the discount has a total use limit, set in `maximum_use_count`."),
    "maximum_use_count": {"type": ["integer", "null"], "description": "The total number of uses allowed, or `null`."},
    "is_maximum_use_customer": flag("Whether each customer has a use limit, set in `maximum_use_customer_count`."),
    "maximum_use_customer_count": {"type": ["integer", "null"], "description": "The number of uses allowed for each customer, or `null`."},
    "is_maximum_discount_allowed": flag("Whether the discount has a maximum amount, set in `maximum_discount_allowed_amount`."),
    "maximum_discount_allowed_amount": {"type": ["number", "null"], "description": "The maximum discount amount allowed, returned as a decimal such as `200.0`, or `null`."},
    "is_exclude_products_on_sale": flag("Whether products on sale are excluded from the discount."),
    "is_discount_used_with_other_discount": flag("Whether the discount can be used with other discounts."),
    "is_display_discount_information_prod_detail": flag("Whether discount information shows on the product detail page."),
    "is_display_text_coupon": flag("Whether `display_text_coupon` is shown."),
    "display_text_coupon": {"type": ["string", "null"], "description": "The coupon display text."},
    "is_display_text_cart": flag("Whether `display_text_cart` is shown."),
    "display_text_cart": {"type": ["string", "null"], "description": "The cart display text."},
    "is_display_text_partial_discount_condition": flag("Whether `display_text_partial_discount_condition` is shown."),
    "display_text_partial_discount_condition": {"type": ["string", "null"], "description": "The partial discount condition display text."},
    "invoice_note": {"type": ["string", "null"], "description": "A note for the invoice, or `null` when not set."},
    "exclude_products": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each product the discount excludes. A product `id` you sent twice is listed twice."},
    "customer_coupons": {"type": "array", "items": ref("DiscountProfileCustomerCoupon"), "description": "The coupon codes generated for the profile, in the order they were generated. [Generate coupon codes](" + COUPONS_PAGE + ") adds to the end of this list."},
    "usage": {"type": "array", "items": {"type": "integer"}, "description": "A list of whole numbers set by the store."},
    "created_on": {"type": "string", "description": "When the profile was created, written `yyyy-MM-ddTHH:mm:ssZ`, such as `2026-10-07T03:15:42Z`."},
    "last_updated_on": {"type": "string", "description": "When the profile last changed, written like `created_on`. On a new profile it equals `created_on`. Generating coupon codes does not change it."},
}

INPUT_PROPERTIES = {
    "name": {"type": "string", "maxLength": 255, "description": "Required on create. Spaces at either end are removed. At most 255 characters, unique in any letter case, and without `<`, `>`, `javascript:` or `expression()`. A replace without it keeps the name; a replace with a blank, longer or taken name returns `500`."},
    "type": {"type": "string", "enum": PROFILE_TYPES, "description": "`customer`, `promote_product`, `offer_incentive_and_sell_more` or `offer_coupon`. A create rejects any other value with `400` and the reason `invalid_enum`; a replace stores any value. Without it, a create returns `\"\"` and a replace keeps the current type."},
    "discount_details_type": {"type": "string", "enum": DETAILS_TYPES, "description": "Required on create. `amount`, `shipping` or `product`: the body then needs `amount_details`, `shipping_details` or `product_details`. To change it on a replace, also send the complete details block the new value names; the profile then returns that block and not the old one."},
    "amount_details": dict(ref("DiscountProfileAmountDetails"), description="Required when `discount_details_type` is `amount`."),
    "shipping_details": dict(ref("DiscountProfileShippingDetails"), description="Required when `discount_details_type` is `shipping`."),
    "product_details": dict(ref("DiscountProfileProductDetails"), description="Required when `discount_details_type` is `product`."),
    "is_active": flag("Whether the profile is active."),
    "start_date": {"type": "string", "example": "2026-11-06 09:30:00", "description": "When the discount starts, written `yyyy-MM-dd HH:mm:ss`. The store reads it in its own time zone and returns it in UTC. A create rejects a value that is not a real date and time in that form with `400`; a replace stores such a value as `null`. A replace without it sets it to `null`."},
    "is_specify_end_date": flag("Whether the profile has an `end_date`. A string such as `\"yes\"` is rejected with `400`, on create and on replace."),
    "end_date": {"type": "string", "example": "2026-11-16 18:00:00", "description": "When the discount ends, written like `start_date`. A create stores it only when `is_specify_end_date` is `true`, and then rejects an `end_date` before `start_date` with `400`; a replace stores an earlier `end_date` as sent. A replace without it sets it to `\"\"`."},
    "is_apply_coupon_code": flag("Whether the profile uses coupon codes. On create, `true` without a `default_coupon_code` makes the store generate one. [Generate coupon codes](" + COUPONS_PAGE + ") works only when this is `true`. A replace that sets it to `true` returns `customer_coupons` as `[]`: retrieve the profile to read its codes."),
    "default_coupon_code": {"type": ["string", "null"], "description": "The profile's default coupon code. On create, a code another coupon already has is rejected with `400` and the message `Coupon code#<code> already exists`. A replace without it keeps the current code. On a replace that sets `is_apply_coupon_code` to `true`, `\"\"` or `null` makes the store generate a new code in its place; without that flag, `\"\"` keeps the current code."},
    "is_coupon_code_auto_generate": flag("Whether coupon codes are generated automatically."),
    "is_create_unique_coupon_each_customer": flag("Whether each customer gets a unique coupon code."),
    "is_imported_coupon": flag("Whether the coupon codes are imported. A string is rejected with `400`, on create and on replace."),
    "is_maximum_use_total": flag("Whether the discount has a total use limit, set in `maximum_use_count`. `is_maximum_use_limit` is accepted as another name."),
    "maximum_use_count": {"type": ["integer", "null"], "description": "The total number of uses allowed. `maximum_use_limit` is accepted as another name. A replace without it sets it to `null`."},
    "is_maximum_use_customer": flag("Whether each customer has a use limit, set in `maximum_use_customer_count`. `is_maximum_use_limit_by_customer` is accepted as another name."),
    "maximum_use_customer_count": {"type": ["integer", "null"], "description": "The number of uses allowed for each customer. `maximum_use_limit_by_customer` is accepted as another name. A replace without it sets it to `null`."},
    "is_maximum_discount_allowed": flag("Whether the discount has a maximum amount, set in `maximum_discount_allowed_amount`."),
    "maximum_discount_allowed_amount": {"type": ["number", "null"], "description": "The maximum discount amount allowed. `maximum_discount_allowed` is accepted as another name. A replace without it sets it to `null`."},
    "is_exclude_products_on_sale": flag("Whether products on sale are excluded from the discount."),
    "is_discount_used_with_other_discount": flag("Whether the discount can be used with other discounts."),
    "is_display_discount_information_prod_detail": flag("Whether discount information shows on the product detail page."),
    "is_display_text_coupon": flag("Whether `display_text_coupon` is shown."),
    "display_text_coupon": {"type": "string", "description": "The coupon display text. A replace without it keeps the text, and `\"\"` clears it."},
    "is_display_text_cart": flag("Whether `display_text_cart` is shown."),
    "display_text_cart": {"type": "string", "description": "The cart display text. A replace without it keeps the text, and `\"\"` clears it."},
    "is_display_text_partial_discount_condition": flag("Whether `display_text_partial_discount_condition` is shown."),
    "display_text_partial_discount_condition": {"type": "string", "description": "The partial discount condition display text. A replace without it keeps the text, and `\"\"` clears it."},
    "invoice_note": {"type": ["string", "null"], "description": "A note for the invoice. A replace without it keeps the note, and `null` clears it."},
    "exclude_products": {"type": "array", "items": {"type": "integer"}, "description": "The `id` of each product the discount excludes. Every entry must be an existing product's `id`: one that no product has returns `500` and stores nothing. A numeric string is read as the number, and a product `id` sent twice is kept twice. A replace without it keeps the list, and `[]` clears it."},
}

ALIASES = "`is_maximum_use_limit`, `maximum_use_limit`, `is_maximum_use_limit_by_customer`, `maximum_use_limit_by_customer` and `maximum_discount_allowed` are accepted as other names for `is_maximum_use_total`, `maximum_use_count`, `is_maximum_use_customer`, `maximum_use_customer_count` and `maximum_discount_allowed_amount`; when you send both names, the name the response uses wins."

FREE_SHIPPING_NULL = "In a `free_shipping` block, returned as `null` even when you send a value."
FREE_PRODUCT_NULL = "In a `free_product` block, returned as `null` even when you send a value."

SCHEMAS = {
    "DiscountProfile": {"type": "object", "description": "A discount profile: the 35 fields every profile has, and the one details block its `discount_details_type` names. The listing, [Retrieve a discount profile](" + RETRIEVE_PAGE + "), [Create a discount profile](" + CREATE_PAGE + ") and [Replace a discount profile](" + REPLACE_PAGE + ") return the same fields.", "properties": PROFILE_PROPERTIES},
    "DiscountProfileCreate": {"type": "object", "required": ["name", "discount_details_type"], "description": "Send these fields at the top level of the body, not wrapped in `discount_profile`. `name`, `discount_details_type` and the details block it names are required. Fields the store does not know are dropped, and the profile's `id`, which the store sets itself, is rejected with `400`. The store also accepts `customer`, `customer_group`, `product`, `category`, `is_applied_to_all_customers` and `is_applied_to_all_products`, but no read returns them. " + ALIASES, "properties": INPUT_PROPERTIES},
    "DiscountProfileReplace": {"type": "object", "description": "Send these fields at the top level of the body. The body replaces the profile: every `is_*` flag you leave out becomes `false`, `start_date` becomes `null`, `end_date` becomes `\"\"`, and `maximum_use_count`, `maximum_use_customer_count` and `maximum_discount_allowed_amount` become `null`. `name`, `type`, `default_coupon_code`, the three display texts, `invoice_note` and `exclude_products` keep their values when you leave them out. Always send the details block of the profile's `discount_details_type`: a body without it returns `500`. " + ALIASES, "properties": INPUT_PROPERTIES},
    "DiscountProfileAmountDetails": {"type": "object", "description": "The details block of an `amount` profile. A `single` block without `type`, `apply_to`, `single_amount` or `single_amount_type` returns `500` and stores nothing. `amount` and `amount_type` are accepted as other names for `single_amount` and `single_amount_type`, on create and on replace; when you send both names, `amount` and `amount_type` win.", "properties": {
        "type": {"type": "string", "description": "`single` for one amount, or `tiered`."},
        "apply_to": {"type": "string", "description": "What the discount applies to, such as `total_order`."},
        "single_amount": {"type": ["number", "null"], "description": "The discount amount, returned as a decimal such as `40.0`. A create rejects a negative value, or a `PERCENT` value above `100`, with `400` and the reason `out_of_range`; a replace stores it. A `tiered` block does not need it."},
        "single_amount_type": {"type": "string", "enum": ["FLAT", "PERCENT"], "description": "`FLAT` or `PERCENT`. A create rejects any other value with `400` and the reason `invalid_enum`; a replace stores it."},
        "minimum_amount_on": {"type": ["string", "null"], "description": "Defaults to `each_item`."},
        "tiers": {"type": "array", "items": {"type": "integer"}, "description": "Tier records you send are dropped: the profile returns `type: \"tiered\"` and `tiers: []`, so you cannot set tiers through the API. A profile whose tiers were set outside the API returns the `id` of each tier here, not the tier itself."},
    }},
    "DiscountProfileShippingDetails": {"type": "object", "description": "The details block of a `shipping` profile. Without `apply_to` or `minimum_qty_on`, the call returns `500` and stores nothing.", "properties": {
        "type": {"type": "string", "description": "The shipping discount's type, such as `free_shipping`. It is not checked: any value is stored as sent."},
        "apply_to": {"type": "string", "description": "Required. What the discount applies to, such as `total_order`."},
        "minimum_qty_on": {"type": "string", "description": "Required. For example `each_item`."},
        "amount_type": {"type": ["string", "null"], "description": "`FLAT` is returned as `single`."},
        "single_amount_type": {"type": ["string", "null"]},
        "minimum_qty": {"type": ["integer", "null"], "description": "The minimum quantity, stored as sent."},
        "minimum_amount": {"type": ["number", "null"], "description": "The minimum amount, stored as sent and returned as a decimal such as `50.0`."},
        "single_amount": {"description": FREE_SHIPPING_NULL},
        "cap_amount": {"description": FREE_SHIPPING_NULL},
        "maximum_time": {"description": FREE_SHIPPING_NULL},
        "zone": {"description": "Returned as `null`."},
        "shipping_class": {"description": "Returned as `null`."},
        "tiers": {"type": "array", "items": {}, "description": "Returned as `[]`."},
    }},
    "DiscountProfileProductDetails": {"type": "object", "description": "The details block of a `product` profile. A create without `free_product_min_qty_on` returns `500` and stores nothing. A create whose block has keys the store does not recognise can return `500` and still store the profile.", "properties": {
        "type": {"type": "string", "description": "The product discount's type, such as `free_product`."},
        "free_product_min_qty_on": {"type": "string", "description": "Required. For example `each_item`."},
        "free_product_max_qty": {"type": ["integer", "null"], "description": "Stored as sent."},
        "free_product_min_amount": {"type": ["number", "null"], "description": "Stored as sent and returned as a decimal such as `25.0`."},
        "minimum_qty_on": {"type": ["string", "null"]},
        "amount_type": {"type": ["string", "null"], "description": "`FLAT` is returned as `single`."},
        "single_amount_type": {"type": ["string", "null"]},
        "single_amount": {"description": FREE_PRODUCT_NULL},
        "cap_price": {"description": FREE_PRODUCT_NULL},
        "cap_price_max_qty": {"description": FREE_PRODUCT_NULL},
        "product_ids": {"type": "array", "items": {}, "description": "Accepted but not stored: returned as `[]`."},
        "category_ids": {"type": "array", "items": {}, "description": "Returned as `[]`."},
        "tiers": {"type": "array", "items": {}, "description": "Returned as `[]`."},
    }},
    "DiscountProfileCustomerCoupon": {"type": "object", "description": "One generated coupon code.", "properties": {
        "id": {"type": "integer", "description": "The coupon's own `id`, assigned by the store. No call takes it: [Assign a coupon code to a customer](" + ASSIGN_PAGE + ") finds the coupon by its `code`."},
        "code": {"type": "string", "description": "The coupon code. Send it as `code` to [Assign a coupon code to a customer](" + ASSIGN_PAGE + ")."},
        "customer_email": {"type": "string", "description": "The email address of the customer the code is assigned to, spelled as in the customer's record, or `\"\"` until a customer is assigned. Deleting that customer leaves it unchanged."},
    }},
    "DiscountProfilePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of profiles that match your filters. There is no count endpoint: `GET /admin/discount_profiles/count` is rejected with `400` and the reason `invalid_id`."},
        "limit": {"type": "integer", "description": "The page size the store applied: the `limit` you sent, at most `20`, or `20` when you send none."},
        "offset": {"type": "integer", "description": "The number of profiles skipped before this page."},
        "count": {"type": "integer", "description": "The number of profiles on this page."},
        "current_page": {"type": "integer", "description": "`offset` divided by `limit`, rounded down, plus one. On an empty page past the last profile, it is `total_pages` instead."},
        "total_pages": {"type": "integer", "description": "`total` divided by `limit`, rounded up."},
        "has_next": {"type": "boolean", "description": "`true` when more profiles come after this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is above `0`. On an empty page past the last profile, it is `false` even when `offset` is above `0`."},
        "previous_page": {"type": ["string", "null"], "description": "The full URL of the previous page, with the filters you sent, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The full URL of the next page, with the filters you sent, or `null` on the last page. It uses `offset`, even when you sent `page`."},
    }},
    "DiscountProfileGroupMeta": {"type": "object", "description": "Returned only by the listing, with one entry.", "properties": {
        "discount_profiles": ref("DiscountProfileResourceMeta"),
    }},
    "DiscountProfileResourceMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "`resource`."},
        "writable": {"type": "boolean", "description": "`true`: you can create, replace and delete discount profiles."},
        "href": {"type": "string", "description": "The listing's own path, `/api/v4/admin/discount_profiles`."},
    }},
    "DiscountProfileFieldMetadata": {"type": "object", "description": "Describes every field of a profile, one entry per field name: the 35 fields every profile has and the three details blocks. The listing and [Retrieve a discount profile](" + RETRIEVE_PAGE + ") return the same block. Its descriptions are wrong in two places: the `type` entry says an omitted `type` is stored as `null`, but a profile created without one returns `\"\"`; and the `shipping_details` and `product_details` entries say their fields are not validated, but a block without `apply_to`, `minimum_qty_on` or `free_product_min_qty_on` returns `500`.", "properties": {
        key: ref("DiscountProfileFieldMetadataEntry") for key in SHARED_FIELDS + DETAILS_KEYS
    }},
    "DiscountProfileFieldMetadataEntry": {"type": "object", "additionalProperties": True, "description": "Describes one field. Every entry has `type`.", "properties": {
        "type": {"type": "string", "description": "The kind of value the field holds."},
        "read_only": {"type": "boolean", "description": "`true` on the entries for `id`, `customer_coupons`, `created_on` and `last_updated_on`, and on no other entry."},
        "fields": {"description": "On the `amount_details` entry, the six fields of the amount block: `type`, `apply_to`, `single_amount`, `single_amount_type`, `minimum_amount_on` and `tiers`."},
    }},
    "DiscountProfileGenerateCodesInput": {"type": "object", "required": ["requested_codes"], "description": "Send `requested_codes` at the top level of the body, not wrapped in a key.", "properties": {
        "requested_codes": {"type": "integer", "minimum": 1, "example": 3, "description": "Required. The number of codes to generate, `1` or more. A numeric string such as `\"2\"` is read as the number. `0` or a missing value is rejected with `Invalid request data`, and a negative number with `Invalid number of requested codes`."},
    }},
    "DiscountProfileGeneratedCodes": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "message": {"type": "string", "description": "`<n> new codes generated.`, where `<n>` is the number of codes."},
        "codes": {"type": "array", "items": {"type": "string"}, "description": "The new codes, all different, in the order they were generated. They are added to the end of the profile's `customer_coupons`."},
    }},
    "DiscountProfileAssignInput": {"type": "object", "required": ["code", "email"], "description": "Send `code` and `email` at the top level of the body. A body wrapped in a key is rejected with `Code is required`.", "properties": {
        "code": {"type": "string", "description": "Required. A coupon code generated for a profile, from `codes` in the response to [Generate coupon codes](" + COUPONS_PAGE + ") or from the profile's `customer_coupons`."},
        "email": {"type": "string", "format": "email", "example": "jane.citizen@example.com", "description": "Required. The email address of an existing customer, in any letter case. A customer awaiting verification is accepted."},
    }},
    "DiscountProfileAssignResult": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "message": {"type": "string", "description": "`customer has been assigned successfully.`"},
    }},
    "DiscountProfileAssignError": {"type": "object", "description": "The flat error body that [Assign a coupon code to a customer](" + ASSIGN_PAGE + ") returns. It has no `error` object.", "properties": {
        "status": {"type": "string", "description": "`error`."},
        "message": {"type": "string", "description": "What went wrong, such as `Error customer assign to code`."},
        "detailsMessage": {"type": "string", "description": "The reason, such as `customer.not.found` when no customer has the `email` you sent, or `coupon.not.found.by.code` when no coupon has the `code` you sent."},
    }},
    "DiscountProfileError": {"type": "object", "description": "The error body of every discount profile call except [Assign a coupon code to a customer](" + ASSIGN_PAGE + "), which returns a flat body instead.", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found`, `conflict` or `internal_error`."},
        "message": {"type": "string", "description": "What went wrong, such as `Discount Profile not found` or `Discount Name already exists`."},
        "details": {"type": "array", "description": "More about the rejection. For a rejected field, each entry's `code` gives the reason, such as `invalid_enum`, `out_of_range`, `invalid_date`, `invalid_range`, `invalid_boolean` or `required`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected, such as `sort`, or `id` when `discount_profile_id` is not a number."},
            "code": {"type": "string", "description": "Why the field was rejected."},
            "message": {"type": ["string", "null"], "description": "What was wrong with the value, such as `must be a numeric discount profile id`. `null` when the listing rejects `limit`, `offset`, `page` or `sort`."},
            "value": {"description": "The value you sent, such as `NAME` for a rejected `sort`."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
