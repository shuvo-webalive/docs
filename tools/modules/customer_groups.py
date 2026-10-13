"""The Customer groups endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Customer groups"
SLUG = "customer-groups"
BASE = "/admin/customer_groups"
ICON = "user-group"

OVERVIEW_DESCRIPTION = "List, count, create, update and delete customer groups, and choose which customers belong to each group."
INTRO = "The Customer groups API has nine endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/customer_groups`."

RETRIEVE_PAGE = "/api-reference/customer-groups/retrieve-a-customer-group"
MEMBERS_PAGE = "/api-reference/customer-groups/replace-the-members-of-a-customer-group"
ASSIGN_PAGE = "/api-reference/customer-groups/add-a-customer-to-a-customer-group"
CUSTOMER_PAGE = "/api-reference/customers/retrieve-a-customer"
DELETE_CUSTOMER_PAGE = "/api-reference/customers/delete-a-customer"

WARNING = (
    "**Replacing a group's members removes every customer you leave out of the list.**\n"
    "  [Replace the members of a customer group](" + MEMBERS_PAGE + ") makes the list you send the\n"
    "  whole membership, and `{\"customers\": []}` empties the group. To add one customer and keep the\n"
    "  others, use [Add a customer to a customer group](" + ASSIGN_PAGE + ")."
)

NOTES = [
    "**Wrap a group in `customer_group` when you create or update it.** Send\n"
    "  `{\"customer_group\": {\"name\": \"Wholesale Partners\"}}`. A body without the wrapper is rejected\n"
    "  with `400` and the message `customer_group is required`. Replacing the members and adding a\n"
    "  customer take bodies without that wrapper: `{\"customers\": [...]}` and\n"
    "  `{\"customer\": ..., \"group\": ...}`.",
    "**An update changes only the fields you send, inside nested settings too.**\n"
    "  `{\"customer_group\": {\"tax_configuration\": {\"tax_exempt\": true}}}` changes `tax_exempt` and keeps\n"
    "  the other five tax settings. There is no replace: `PUT` on a group is rejected with `405`.",
    "**Members are customers, identified by their `customer_id`.** The member calls take the customer's\n"
    "  `customer_id`, as a number or a string, not its `internal_id`. A customer's groups are listed\n"
    "  under `customer_groups` when you [retrieve the customer](" + CUSTOMER_PAGE + ").",
    "**A listing returns 20 groups per call unless you send `limit`.** `limit` takes `1` to `100`. To get\n"
    "  more, send a higher `offset`, or `page`, while `pagination.has_next` is `true`. To sort by date,\n"
    "  send `sort=created` or `sort=updated`: `created_at` and `updated_at` are rejected with `400`.",
    "**There is no `HEAD` call.** `HEAD` returns `404` on every customer group path, even though the\n"
    "  `Allow` header of an `OPTIONS` request lists it on the listing, count and group paths. Use `GET`\n"
    "  instead.",
    "**Groups already in the store can hold values a write rejects.** A stored group can have a `status`\n"
    "  other than `A` or `I`, a `default_tax_code` a create rejects, or a `name` with spaces at either end.\n"
    "  Such a group matches neither `status=A` nor `status=I`, so those two counts can add up to less\n"
    "  than the total.",
]

CUSTOMER_GROUP_ID = {
    "name": "customer_group_id",
    "in": "path",
    "required": True,
    "description": "The customer group's `id`, from a listing or from the response to creating the group.",
    "schema": {"type": "integer", "example": 1234},
}

CUSTOMER_ID = {
    "name": "customer_id",
    "in": "path",
    "required": True,
    "description": "The customer's `customer_id`, which is the `id` of the customer's entry in the group's `customers` list. Do not send the customer's `internal_id`: the store reads the value as a `customer_id` and looks up that customer instead.",
    "schema": {"type": "integer", "example": 5678},
}

SEARCH_TEXT = {"name": "search_text", "in": "query", "description": "Keeps only groups whose `name` contains this text, in any letter case. It does not search `description`.", "schema": {"type": "string", "example": "wholesale"}}
NAME = {"name": "name", "in": "query", "description": "Another name for `search_text`. Keeps only groups whose `name` contains this text, in any letter case.", "schema": {"type": "string", "example": "wholesale"}}
STATUS = {"name": "status", "in": "query", "description": "Keeps only active groups (`A` or `active`) or inactive groups (`I` or `inactive`). Any other value is rejected with `400` (`invalid_enum`).", "schema": {"type": "string", "enum": ["A", "I", "active", "inactive"], "example": "active"}}
LIMIT = {"name": "limit", "in": "query", "description": "The number of groups per page, from `1` to `100`. Defaults to `20`. `pagination.limit` shows the value applied. `0` is rejected with `400` and the message `'limit' must be a positive integer`; a value above `100` with the message `page size must be 100 or fewer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "The number of groups to skip. A negative value is rejected with `400`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "The page number, starting at `1`. The store skips `(page - 1) * limit` groups, so `limit=2&page=2` skips 2 groups.", "schema": {"type": "integer", "minimum": 1, "example": 1}}
SORT = {"name": "sort", "in": "query", "description": "The field to sort by: `id`, `name`, `status`, `description`, `created` or `updated`. Without it, groups are sorted by `name`. Any other value, including `created_at` and `updated_at`, is rejected with `400` (`invalid_sort_field`).", "schema": {"type": "string", "enum": ["id", "name", "status", "description", "created", "updated"], "example": "name"}}
DIR = {"name": "dir", "in": "query", "description": "The sort direction: `asc` or `desc`. Defaults to `asc`. Any other value is rejected with `400`.", "schema": {"type": "string", "enum": ["asc", "desc"], "example": "asc"}}
LIST_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key beside the groups and `pagination`. It describes each field of a group.", "schema": {"type": "boolean", "example": True}}
GET_FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Send `true` to add a `field_metadata` key beside the group. It describes each field of a group.", "schema": {"type": "boolean", "example": True}}

ERROR_REF = {"$ref": "#/components/schemas/CustomerGroupError"}
ROW_REF = {"$ref": "#/components/schemas/CustomerGroup"}
DETAIL_REF = {"$ref": "#/components/schemas/CustomerGroupDetail"}
MEMBER_REF = {"$ref": "#/components/schemas/CustomerGroupMember"}
FIELD_METADATA_REF = {"$ref": "#/components/schemas/CustomerGroupFieldMetadata"}

ROW_RESPONSE = {"type": "object", "properties": {"customer_group": ROW_REF}}
DETAIL_RESPONSE = {"type": "object", "properties": {"customer_group": DETAIL_REF}}
WRITE_BODY = {"type": "object", "required": ["customer_group"], "properties": {"customer_group": {"$ref": "#/components/schemas/CustomerGroupInput"}}}

NOT_FOUND = {"description": "No customer group has that `customer_group_id`. The code is `not_found` and the message `Customer group not found`.", "schema": ERROR_REF}
NO_WRAPPER = "The body is not wrapped in `customer_group`: the code is `invalid_request` and the message `customer_group is required`."
BAD_REFERENCE = "`default_tax_code` names a tax code the store does not have: the code is `invalid_reference` and the message `no tax code with code <code>`. Or `shipping_profile` is an object instead of a bare number: the message is `shipping profile id must be numeric`."


def amount(enabled, value):
    return {"enabled": enabled, "amount": value}


DEFAULT_SETTINGS = {
    "purchase_preference": {
        "minimum_purchase": amount(False, None),
        "on_account_purchase": {
            "enabled": False,
            "max_purchase": amount(False, None),
            "credit_limit": amount(False, None),
            "payment_terms": {"enabled": False, "terms": None},
        },
    },
    "tax_configuration": {
        "override_store_tax": False, "tax_exempt": False, "tax_message": None,
        "show_prices_with_tax_included": False, "prices_entered_with_tax_included": False,
        "base_price_rounding": None,
    },
    "product_display": {
        "overwrite_default": False, "variation_display_type": None, "display_parent_image": False,
        "activate_colour_variation_image": False, "show_selected_variation_value": False,
        "strike_through_out_of_stock": False, "single_click_variation_loading": False,
        "price_display_method": None,
    },
}


def group(group_id, name, description, status, created_at, updated_at, settings=None):
    row = {
        "id": group_id, "name": name, "description": description, "status": status,
        "default_tax_code": None, "add_as_new_customer_default_group": False,
        "shipping_profile": None, "background_image": None,
    }
    row.update(copy.deepcopy(settings or DEFAULT_SETTINGS))
    row.update({"created_at": created_at, "updated_at": updated_at})
    return row


CREATE_BODY = {"customer_group": {
    "name": "Wholesale Partners",
    "description": "Trade accounts",
    "status": "active",
    "purchase_preference": {
        "minimum_purchase": amount(True, 50),
        "on_account_purchase": {
            "enabled": True,
            "max_purchase": amount(True, 500),
            "credit_limit": amount(True, 1000),
            "payment_terms": {"enabled": True, "terms": "NET_30"},
        },
    },
    "tax_configuration": {
        "override_store_tax": True, "tax_exempt": False, "tax_message": "Prices exclude GST",
        "show_prices_with_tax_included": True, "prices_entered_with_tax_included": False,
        "base_price_rounding": "up",
    },
    "product_display": {
        "overwrite_default": True, "variation_display_type": "enable_matrix_view", "display_parent_image": True,
        "activate_colour_variation_image": False, "show_selected_variation_value": True,
        "strike_through_out_of_stock": False, "single_click_variation_loading": True,
        "price_display_method": "highest",
    },
}}

CREATED_SETTINGS = copy.deepcopy({key: CREATE_BODY["customer_group"][key] for key in ("purchase_preference", "tax_configuration", "product_display")})
CREATED_SETTINGS["purchase_preference"]["on_account_purchase"]["payment_terms"]["terms"] = "net_30"

CREATED_ROW = group(1234, "Wholesale Partners", "Trade accounts", "A", "2026-10-11T09:15:02", "2026-10-11T09:15:02", CREATED_SETTINGS)

PATCH_BODY = {"customer_group": {"status": "inactive", "purchase_preference": {"minimum_purchase": {"amount": 75}}}}
PATCHED_ROW = copy.deepcopy(CREATED_ROW)
PATCHED_ROW["status"] = "I"
PATCHED_ROW["purchase_preference"]["minimum_purchase"]["amount"] = 75
PATCHED_ROW["updated_at"] = "2026-10-11T09:20:41"

SAMPLE_ROWS = [
    group(1236, "Members Club", None, "A", "2026-07-16T06:24:24", "2026-07-16T06:24:24"),
    CREATED_ROW,
]

SAMPLE_PAGINATION = {"total": 2, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

MEMBERS = [
    {"id": 5678, "first_name": "Jane", "last_name": "Citizen", "email": "jane.citizen@example.com"},
    {"id": 5679, "first_name": "Sam", "last_name": "Lee", "email": "sam.lee@example.com"},
]

DETAIL_ROW = dict(copy.deepcopy(CREATED_ROW), customer_count=1, customers=[MEMBERS[0]])
MEMBERS_ROW = dict(copy.deepcopy(CREATED_ROW), updated_at="2026-10-11T09:30:12", customer_count=2, customers=MEMBERS)

ENDPOINTS = [
    {
        "key": "list_customer_groups",
        "slug": "list-customer-groups",
        "title": "List customer groups",
        "method": "GET",
        "path": BASE,
        "summary": "Returns customer groups, 20 per call or the `limit` you send, sorted by `name` by default.",
        "description": "Returns the customer groups under `customer_groups`, sorted by `name` unless you send `sort`, with a `pagination` block. Send `search_text` to keep only groups whose `name` contains that text, and `status` to keep only active or inactive groups. Query parameters this call does not list, such as `q`, are ignored. The response has no `ETag` or `Last-Modified` header.",
        "parameters": [SEARCH_TEXT, NAME, STATUS, SORT, DIR, LIMIT, OFFSET, PAGE, LIST_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The groups on this page in `customer_groups`, and `pagination` with `total`, `limit`, `offset`, `has_previous` and `has_next`. Each group has the 13 fields of `CustomerGroup`, without its members. With `field_metadata=true`, a `field_metadata` key is added.",
                "schema": {"type": "object", "properties": {
                    "customer_groups": {"type": "array", "items": ROW_REF},
                    "pagination": {"$ref": "#/components/schemas/CustomerGroupPagination"},
                    "field_metadata": FIELD_METADATA_REF,
                }},
                "example": {"customer_groups": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "A query parameter has a value the listing does not accept: `limit` is `0` (`'limit' must be a positive integer`) or above `100` (`page size must be 100 or fewer`); `offset` is negative; `status` is not `A`, `I`, `active` or `inactive` (`invalid_enum`); `sort` is not one of its six fields (`invalid_sort_field`); or `dir` is not `asc` or `desc`.",
                "schema": ERROR_REF,
            },
        },
        "example_call": {"query": {"search_text": "wholesale", "status": "active", "limit": 50}},
    },
    {
        "key": "count_customer_groups",
        "slug": "count-customer-groups",
        "title": "Count customer groups",
        "method": "GET",
        "path": BASE + "/count",
        "summary": "Returns the number of customer groups that match your `search_text`, `name` and `status` filters.",
        "description": "Returns the number of groups as `total`. `search_text`, `name` and `status` narrow the count the same way they narrow the listing, so `total` matches the listing's `pagination.total` for the same filters. `limit`, `offset` and `field_metadata` change nothing. The response has no `ETag` header.",
        "parameters": [SEARCH_TEXT, NAME, STATUS],
        "responses": {
            "200": {
                "description": "The number of groups that match, under `total`.",
                "schema": {"type": "object", "properties": {"total": {"type": "integer"}}},
                "example": {"total": 2},
            },
            "400": {"description": "`status` is not `A`, `I`, `active` or `inactive` (`invalid_enum`).", "schema": ERROR_REF},
        },
        "example_call": {"query": "search_text=wholesale&status=I"},
    },
    {
        "key": "create_customer_group",
        "slug": "create-a-customer-group",
        "title": "Create a customer group",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a customer group and returns it, with the group's `id` to pass as `customer_group_id`.",
        "description": "Wrap the group in `customer_group`; only `name` is required. The store trims spaces from the ends of `name`, and no other group can have the same name in any letter case. A field you leave out gets its default: `status` becomes `A`, `description` becomes `null`, every flag becomes `false`, and every amount, text and choice becomes `null`. `status` accepts `active` and `inactive` and returns `A` or `I`.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new group, with the group's `id`, which the other calls take as `customer_group_id`. `payment_terms.terms` returns in lower case, such as `net_30`. The response has no `Location` header.",
                "schema": ROW_RESPONSE,
                "example": {"customer_group": CREATED_ROW},
            },
            "400": {"description": NO_WRAPPER + " Or " + BAD_REFERENCE, "schema": ERROR_REF},
        },
        "example_call": {},
    },
    {
        "key": "get_customer_group",
        "slug": "retrieve-a-customer-group",
        "title": "Retrieve a customer group",
        "method": "GET",
        "path": BASE + "/{customer_group_id}",
        "summary": "Returns the customer group whose `id` you pass as `customer_group_id`, with its members.",
        "description": "Returns one group under `customer_group`, with the 13 fields a listing entry has plus `customer_count` and `customers`. Each entry in `customers` gives a member's `customer_id` as `id`, with `first_name`, `last_name` and `email`. Send `field_metadata=true` to add a description of each field beside the group. The response has an `ETag` header.",
        "parameters": [CUSTOMER_GROUP_ID, GET_FIELD_METADATA],
        "responses": {
            "200": {
                "description": "The group and its members. With `field_metadata=true`, a `field_metadata` key is added beside `customer_group`.",
                "schema": {"type": "object", "properties": {"customer_group": DETAIL_REF, "field_metadata": FIELD_METADATA_REF}},
                "example": {"customer_group": DETAIL_ROW},
            },
            "404": NOT_FOUND,
        },
        "example_call": {"path": {"customer_group_id": 1234}},
    },
    {
        "key": "patch_customer_group",
        "slug": "update-a-customer-group",
        "title": "Update a customer group",
        "method": "PATCH",
        "path": BASE + "/{customer_group_id}",
        "summary": "Changes only the fields you send, nested settings included, and returns the customer group.",
        "description": "Wrap the change in `customer_group`. Only the fields you send change, and inside `purchase_preference`, `tax_configuration` and `product_display` only the keys you send change. Send `null` to clear `default_tax_code`, `shipping_profile` or `background_image`. `PUT` on a group is rejected with `405` and the message `HTTP method not allowed for this endpoint.`",
        "parameters": [CUSTOMER_GROUP_ID],
        "body": {"schema": WRITE_BODY, "example": PATCH_BODY},
        "responses": {
            "200": {
                "description": "The group after the change, with the 13 fields a listing entry has. To get its members, use [Retrieve a customer group](" + RETRIEVE_PAGE + ").",
                "schema": ROW_RESPONSE,
                "example": {"customer_group": PATCHED_ROW},
            },
            "400": {"description": NO_WRAPPER + " Or " + BAD_REFERENCE, "schema": ERROR_REF},
        },
        "example_call": {"path": {"customer_group_id": 1234}},
    },
    {
        "key": "delete_customer_group",
        "slug": "delete-a-customer-group",
        "title": "Delete a customer group",
        "method": "DELETE",
        "path": BASE + "/{customer_group_id}",
        "summary": "Deletes a customer group permanently. Its members stay in the store as customers.",
        "description": "Deletes the group permanently and returns `204` with no body; retrieving or deleting it again returns `404`. Its members stay as customers, and the group is removed from each member's `customer_groups`. When this call returns `404`, the next [customer delete](" + DELETE_CUSTOMER_PAGE + ") on the same connection can return `404` with the message `Customer already in trash`, or `204`, and not delete the customer: its `is_in_trash` stays `false`. Send that customer delete on a new connection, or send it again.",
        "parameters": [CUSTOMER_GROUP_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No customer group has that `customer_group_id`, for example because you already deleted it.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"customer_group_id": 1234}},
    },
    {
        "key": "update_customer_group_customers",
        "slug": "replace-the-members-of-a-customer-group",
        "title": "Replace the members of a customer group",
        "method": "PATCH",
        "path": BASE + "/{customer_group_id}/customers",
        "summary": "Replaces a customer group's whole member list with the `customer_id` values you send.",
        "description": "Send `{\"customers\": [...]}` with the `customer_id` of every customer who should be in the group, as numbers or strings. The list you send becomes the membership: a customer you leave out leaves the group, and `[]` removes every member. To add one customer and keep the others, use [Add a customer to a customer group](" + ASSIGN_PAGE + "). The `updated_at` in the response is the time the store responded, but the stored `updated_at` does not change, so a later read returns the earlier value.",
        "parameters": [CUSTOMER_GROUP_ID],
        "body": {"schema": {"$ref": "#/components/schemas/CustomerGroupCustomersInput"}, "example": {"customers": [5678, "5679"]}},
        "responses": {
            "200": {
                "description": "The group with its new members in `customers`, and `customer_count` set to the number of members.",
                "schema": DETAIL_RESPONSE,
                "example": {"customer_group": MEMBERS_ROW},
            },
            "400": {"description": "The body has no `customers` array. The message is `A 'customers' array is required (send [] to remove all members).`", "schema": ERROR_REF},
            "500": {"description": "You sent a bare array instead of `{\"customers\": [...]}`. The message is `Unexpected Error Occurred`. Wrap the list in `customers`."},
        },
        "example_call": {"path": {"customer_group_id": 1234}},
    },
    {
        "key": "get_customer_group_customer",
        "slug": "retrieve-a-member-of-a-customer-group",
        "title": "Retrieve a member of a customer group",
        "method": "GET",
        "path": BASE + "/{customer_group_id}/customers/{customer_id}",
        "summary": "Returns one member of a customer group, by the customer's `customer_id`.",
        "description": "Returns the member under `customer`, with the same four fields as the member's entry in the group's `customers` list: `id`, which is the customer's `customer_id`, `first_name`, `last_name` and `email`. Use it to check whether a customer belongs to a group: a customer who is not a member returns `404`. The response has no `ETag` header.",
        "parameters": [CUSTOMER_GROUP_ID, CUSTOMER_ID],
        "responses": {
            "200": {
                "description": "The member.",
                "schema": {"type": "object", "properties": {"customer": MEMBER_REF}},
                "example": {"customer": MEMBERS[0]},
            },
            "404": {"description": "The customer with that `customer_id` is not a member of this group: the code is `not_found` and the message `Customer <customer_id> is not a member of this group.` No customer has that `customer_id`: the message is `No Customer Found`. No customer group has that `customer_group_id`: the message is `Customer group not found`.", "schema": ERROR_REF},
        },
        "example_call": {"path": {"customer_group_id": 1234, "customer_id": 5678}},
    },
    {
        "key": "assign_customer_group",
        "slug": "add-a-customer-to-a-customer-group",
        "title": "Add a customer to a customer group",
        "method": "POST",
        "path": BASE + "/assign",
        "summary": "Adds one customer to a customer group and keeps the group's other members.",
        "description": "Send the customer's `customer_id` as `customer` and the group's `customer_group_id` as `group`, as numbers or strings, with no wrapper. The customer joins the group beside its other members. The call returns `201` whether or not it added the customer: `added` is `true` when the customer joined and `false` when the customer was already a member.",
        "body": {"schema": {"$ref": "#/components/schemas/CustomerGroupAssignInput"}, "example": {"customer": 5678, "group": 1234}},
        "responses": {
            "201": {
                "description": "`status` set to `success`, the customer's `customer_id` and `email`, the group in `group` with the 13 fields a listing entry has, and `added`.",
                "schema": {"$ref": "#/components/schemas/CustomerGroupAssignment"},
                "example": {"status": "success", "customer_id": 5678, "email": "jane.citizen@example.com", "group": CREATED_ROW, "added": True},
            },
        },
        "example_call": {},
    },
]

AMOUNT_SETTING_REF = {"$ref": "#/components/schemas/CustomerGroupAmountSetting"}

GROUP_FIELDS = {
    "id": {"type": "integer", "description": "The customer group's `id`, assigned by the store. Pass it as `customer_group_id` in a path, or as `group` when you add a customer."},
    "name": {"type": "string", "description": "The group's name. No two groups have the same name in any letter case."},
    "description": {"type": ["string", "null"], "description": "Free text, or `null` when none is set."},
    "status": {"type": "string", "description": "`A` for an active group and `I` for an inactive one. A group already in the store can hold another value."},
    "default_tax_code": {"type": ["string", "null"], "description": "The code of the group's default tax code, or `null`. See [Tax codes](/tax-codes)."},
    "add_as_new_customer_default_group": {"type": "boolean", "description": "Marks the group as the default group for new customers. At most one group has it set to `true`."},
    "shipping_profile": {"oneOf": [{"$ref": "#/components/schemas/CustomerGroupShippingProfile"}, {"type": "null"}], "description": "The group's shipping profile, or `null`."},
    "background_image": {"oneOf": [{"$ref": "#/components/schemas/CustomerGroupBackgroundImage"}, {"type": "null"}], "description": "The group's background image, or `null`."},
    "purchase_preference": {"$ref": "#/components/schemas/CustomerGroupPurchasePreference"},
    "tax_configuration": {"$ref": "#/components/schemas/CustomerGroupTaxConfiguration"},
    "product_display": {"$ref": "#/components/schemas/CustomerGroupProductDisplay"},
    "created_at": {"type": "string", "description": "When the group was created."},
    "updated_at": {"type": "string", "description": "When the group last changed. Replacing the members does not change it."},
}

MEMBER_FIELDS = {
    "customer_count": {"type": "integer", "description": "The number of members, the length of `customers`."},
    "customers": {"type": "array", "items": MEMBER_REF, "description": "The group's members. The order is not the order you sent them in."},
}

SCHEMAS = {
    "CustomerGroup": {"type": "object", "description": "One customer group, as a listing, a create, an update and an add-a-customer response return it.", "properties": GROUP_FIELDS},
    "CustomerGroupDetail": {"type": "object", "description": "One customer group with its members, as retrieving a group and replacing its members return it.", "properties": dict(GROUP_FIELDS, **MEMBER_FIELDS)},
    "CustomerGroupInput": {"type": "object", "required": ["name"], "description": "Send these fields inside `customer_group`. On an update, send only the fields you want to change.", "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 100, "description": "Required on create. 2 to 100 characters. The store trims spaces from both ends, and no other group can have the same name in any letter case."},
        "description": {"type": ["string", "null"], "description": "Free text. `null` when you leave it out on create."},
        "status": {"type": "string", "enum": ["A", "I", "active", "inactive"], "description": "`A` or `active` for an active group, `I` or `inactive` for an inactive one. Always returned as `A` or `I`. Defaults to `A`."},
        "default_tax_code": {"type": ["string", "null"], "description": "The code of a tax code the store has. An unknown code is rejected with `400`. Send `null` to clear it."},
        "add_as_new_customer_default_group": {"type": "boolean", "description": "Marks the group as the default group for new customers. At most one group has it set to `true`. Defaults to `false`."},
        "shipping_profile": {"type": ["integer", "null"], "description": "The shipping profile's `id`, as a bare number. `{\"id\": 3}` is rejected with `400`. Send `null` to clear it. It returns as an object with `id` and `name`."},
        "background_image": {"type": ["string", "null"], "description": "The image as a base64 string or a `data:` URI, such as `data:image/png;base64,...`. It returns as an object with `url`, `width` and `height`. Send `null` to remove it."},
        "purchase_preference": {"$ref": "#/components/schemas/CustomerGroupPurchasePreference"},
        "tax_configuration": {"$ref": "#/components/schemas/CustomerGroupTaxConfiguration"},
        "product_display": {"$ref": "#/components/schemas/CustomerGroupProductDisplay"},
    }},
    "CustomerGroupShippingProfile": {"type": "object", "description": "The shipping profile a group uses. A write sends only the profile's `id`, as a bare number.", "properties": {
        "id": {"type": "integer", "description": "The shipping profile's `id`."},
        "name": {"type": "string", "description": "The shipping profile's name."},
    }},
    "CustomerGroupBackgroundImage": {"type": "object", "description": "The stored image. A write sends a base64 string or a `data:` URI instead.", "properties": {
        "url": {"type": "string", "description": "Where the image is stored, under the store's `/resources/` path."},
        "width": {"type": "integer", "description": "The image width in pixels."},
        "height": {"type": "integer", "description": "The image height in pixels."},
    }},
    "CustomerGroupAmountSetting": {"type": "object", "description": "A switch and its amount. `minimum_purchase`, `max_purchase` and `credit_limit` all take this shape.", "properties": {
        "enabled": {"type": "boolean"},
        "amount": {"type": ["number", "null"], "description": "A number, or `null` when none is set."},
    }},
    "CustomerGroupPaymentTerms": {"type": "object", "properties": {
        "enabled": {"type": "boolean"},
        "terms": {"type": ["string", "null"], "description": "Send `NET_30`, `NET_60` or `NET_90`. It returns in lower case, such as `net_30`."},
    }},
    "CustomerGroupOnAccountPurchase": {"type": "object", "properties": {
        "enabled": {"type": "boolean"},
        "max_purchase": AMOUNT_SETTING_REF,
        "credit_limit": AMOUNT_SETTING_REF,
        "payment_terms": {"$ref": "#/components/schemas/CustomerGroupPaymentTerms"},
    }},
    "CustomerGroupPurchasePreference": {"type": "object", "description": "On an update, only the keys you send change.", "properties": {
        "minimum_purchase": AMOUNT_SETTING_REF,
        "on_account_purchase": {"$ref": "#/components/schemas/CustomerGroupOnAccountPurchase"},
    }},
    "CustomerGroupTaxConfiguration": {"type": "object", "description": "On an update, only the keys you send change.", "properties": {
        "override_store_tax": {"type": "boolean"},
        "tax_exempt": {"type": "boolean"},
        "tax_message": {"type": ["string", "null"]},
        "show_prices_with_tax_included": {"type": "boolean"},
        "prices_entered_with_tax_included": {"type": "boolean"},
        "base_price_rounding": {"type": ["string", "null"], "enum": ["nearest", "up", "down", None], "description": "`nearest`, `up` or `down`, or `null` when none is set."},
    }},
    "CustomerGroupProductDisplay": {"type": "object", "description": "On an update, only the keys you send change.", "properties": {
        "overwrite_default": {"type": "boolean"},
        "variation_display_type": {"type": ["string", "null"], "description": "Such as `enable_matrix_view`, or `null` when none is set."},
        "display_parent_image": {"type": "boolean"},
        "activate_colour_variation_image": {"type": "boolean"},
        "show_selected_variation_value": {"type": "boolean"},
        "strike_through_out_of_stock": {"type": "boolean"},
        "single_click_variation_loading": {"type": "boolean"},
        "price_display_method": {"type": ["string", "null"], "enum": ["lowest", "highest", None], "description": "`lowest` or `highest`, or `null` when none is set."},
    }},
    "CustomerGroupMember": {"type": "object", "description": "One member of a customer group.", "properties": {
        "id": {"type": "integer", "description": "The member's `customer_id`. Pass it as `customer_id` in a path."},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
    }},
    "CustomerGroupCustomersInput": {"type": "object", "required": ["customers"], "description": "Send `customers` at the top level of the body, with no wrapper.", "properties": {
        "customers": {"type": "array", "items": {"type": ["integer", "string"]}, "description": "The `customer_id` of every customer who should be in the group, as numbers or strings. Customers you leave out leave the group. `[]` removes every member."},
    }},
    "CustomerGroupAssignInput": {"type": "object", "required": ["customer", "group"], "description": "Send both fields at the top level of the body, with no wrapper.", "properties": {
        "customer": {"type": ["integer", "string"], "description": "The customer's `customer_id`, as a number or a string."},
        "group": {"type": ["integer", "string"], "description": "The customer group's `customer_group_id`, as a number or a string."},
    }},
    "CustomerGroupAssignment": {"type": "object", "properties": {
        "status": {"type": "string", "description": "`success`."},
        "customer_id": {"type": "integer", "description": "The customer's `customer_id`."},
        "email": {"type": "string", "description": "The customer's email address."},
        "group": ROW_REF,
        "added": {"type": "boolean", "description": "`true` when the customer joined the group, `false` when the customer was already a member."},
    }},
    "CustomerGroupPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of groups that match your request."},
        "limit": {"type": "integer", "description": "The page size applied: the `limit` you sent, or `20`."},
        "offset": {"type": "integer", "description": "The number of groups skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when there is a page before this one. An `offset` past the last group returns no groups and `false`."},
        "has_next": {"type": "boolean", "description": "`true` when there is a page after this one."},
    }},
    "CustomerGroupFieldDescription": {"type": "object", "description": "Describes one field. Each entry has `type`; the other keys appear only where they apply, along with the field's bounds, such as the 2 to 100 character length of `name`.", "properties": {
        "type": {"type": "string", "description": "The field's value type."},
        "required": {"type": "boolean", "description": "Whether a create must send the field. `true` on `name`."},
        "read_only": {"type": "boolean", "description": "`true` on a field no write can set. Every field except the ten in `CustomerGroupInput` has it."},
        "values": {"type": "array", "description": "The field's allowed values."},
        "default": {"description": "The field's default value."},
        "fields": {"type": "object", "description": "On `purchase_preference`, `tax_configuration` and `product_display`, a description of each nested field, keyed by dotted path such as `minimum_purchase.amount`."},
    }},
    "CustomerGroupFieldMetadata": {"type": "object", "description": "Describes each field of a customer group, keyed by field name: the 13 fields of `CustomerGroup` and `customer_count`. Returned only when you send `field_metadata=true`.", "additionalProperties": {"$ref": "#/components/schemas/CustomerGroupFieldDescription"}},
    "CustomerGroupError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `invalid_reference`, `not_found` or `method_not_allowed`."},
        "message": {"type": "string", "description": "What went wrong, such as `customer_group is required`."},
        "details": {"type": "array", "description": "One entry per rejected field or parameter, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected."},
            "message": {"type": ["string", "null"]},
            "value": {"description": "The value you sent, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
