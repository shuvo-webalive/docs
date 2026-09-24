"""The Tax zones endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Tax zones"
SLUG = "tax-zones"
BASE = "/admin/tax_zones"
ICON = "map-location-dot"

RETRIEVE_PAGE = "/api-reference/tax-zones/retrieve-a-tax-zone"

OVERVIEW_DESCRIPTION = "List, create, read, update and delete tax zones, each a named set of countries, states and post codes."
INTRO = "The Tax zones API has seven endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/tax_zones`; the path in the old API collection, `/api/v4/admin/tax/custom_zones`, returns `404 not_found` with a message that starts `Unknown tax path`."

WARNING = (
    "**An update replaces the zone's lists.** A `PUT` replaces `countries`, `states` and `post_code` with\n"
    "  the lists you send, so a list you leave out comes back empty. A `use_radius` you leave out comes back\n"
    "  `false`. `radius` and `start_location` keep their stored values when you leave them out. Send every\n"
    "  list on each update, and send `name` too: an update without it fails with `500`."
)

NOTES = [
    "**Wrap every write in `tax_zone`, and always send `name`.** Send\n"
    "  `{\"tax_zone\": {\"name\": \"Sydney Metro\"}}` to create a zone. A bare record is rejected with `400`\n"
    "  and the message `tax_zone missing`. A body with no `name` fails with `500`, on an update as well as\n"
    "  on a create.",
    "**`countries` and `states` take records that hold the country's or state's `id`.** Send\n"
    "  `\"countries\": [{\"id\": 12}]`, where `12` is the country's `id`. You can read country and state `id`\n"
    "  values from the `countries` and `states` of the zones in a listing. A plain number such as `[12]`, a\n"
    "  record with only a `code`, or an `id` that matches no country or state fails with `500`. The store\n"
    "  saves a new zone before it checks these records, so after that `500` on a create the zone can still\n"
    "  be in the listing. The `500` does not include the zone's `id`: look for the zone by `name`.",
    "**You send `post_code` as a flat list and get it back nested.** Send `[\"2000\", \"3000\"]`, and the zone\n"
    "  returns `[[\"2000\"], [\"3000\"]]`. Sending the nested form fails with `500` and the message\n"
    "  `JSONArray cannot be cast to String`.",
    "**After a `400` or `404` from a tax endpoint, the next request on the same connection can fail too.**\n"
    "  Straight after a `404`, the next retrieve returns `404`, even for a zone that exists. A retrieve from\n"
    "  another tax collection returns `404` with that collection's own message, such as `Profile not found`.\n"
    "  Straight after a `400` `invalid_pagination`, the next listing returns the same `400`, even on another\n"
    "  tax collection. The request after it works normally. A `DELETE` sent straight after a `404` returns\n"
    "  that `404` and deletes nothing; sent after a successful read, it returns `204` and the zone is gone.",
    "**A listing returns at most 20 zones per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get every zone, raise `offset` by the number of zones each page\n"
    "  returned until you reach `pagination.total`. The listing reads only `limit`, `offset` and `page`;\n"
    "  `q` and `field_metadata` are accepted and ignored.",
]

TAX_ZONE_ID = {
    "name": "tax_zone_id",
    "in": "path",
    "required": True,
    "description": "The tax zone's `id`, from a listing or from the response to creating the zone.",
    "schema": {"type": "integer", "example": 83},
}

LIMIT = {"name": "limit", "in": "query", "description": "Zones per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. A `limit` below `1`, or one that is not a number, is rejected with `400 invalid_pagination`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of zones to skip. An `offset` that is not a number is rejected with `400 invalid_pagination`.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the `limit` you send with it. `limit=2&page=2` skips 2 zones.", "schema": {"type": "integer", "example": 1}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ROW_REF = ref("TaxZone")
WRITE_BODY = {"type": "object", "required": ["tax_zone"], "properties": {"tax_zone": ref("TaxZoneInput")}}
ROW_RESPONSE = {"type": "object", "properties": {"tax_zone": ROW_REF}}

AUSTRALIA = {"id": 12, "name": "Australia", "code": "AU"}
NEW_SOUTH_WALES = {"id": 67, "name": "New South Wales", "code": "NSW"}
VICTORIA = {"id": 72, "name": "Victoria", "code": "VIC"}

SAMPLE_ROWS = [
    {
        "id": 1, "name": "New South Wales", "system_generated": True, "default": False,
        "use_radius": False, "radius": 0.0, "start_location": "",
        "countries": [AUSTRALIA], "states": [NEW_SOUTH_WALES], "post_code": [],
        "created_at": "2026-01-12T03:20:00", "updated_at": "2026-01-12T03:20:00",
    },
    {
        "id": 2, "name": "Victoria", "system_generated": True, "default": False,
        "use_radius": False, "radius": 0.0, "start_location": "",
        "countries": [AUSTRALIA], "states": [VICTORIA], "post_code": [],
        "created_at": "2026-01-12T03:20:00", "updated_at": "2026-01-12T03:20:00",
    },
]

SAMPLE_PAGINATION = {
    "total": 42, "limit": 2, "offset": 0, "count": 2, "current_page": 1, "total_pages": 21,
    "has_next": True, "has_previous": False, "previous_page": None,
    "next_page": "https://your-store.example.com/api/v4/admin/tax_zones?limit=2&offset=2",
}

CREATE_BODY = {"tax_zone": {
    "name": "Sydney Metro",
    "countries": [{"id": 12}],
    "states": [{"id": 67}],
    "post_code": ["2000", "3000"],
}}

CREATED_ZONE = {
    "id": 83, "name": "Sydney Metro", "system_generated": False, "default": False,
    "use_radius": False, "radius": 0.0, "start_location": "",
    "countries": [AUSTRALIA], "states": [NEW_SOUTH_WALES], "post_code": [["2000"], ["3000"]],
    "created_at": "2026-09-22T04:15:00", "updated_at": "2026-09-22T04:15:00",
}

UPDATE_BODY = {"tax_zone": {
    "name": "Sydney Metro and Parramatta",
    "countries": [{"id": 12}],
    "states": [{"id": 67}],
    "post_code": ["2000", "2150"],
}}

UPDATED_ZONE = dict(
    CREATED_ZONE,
    name="Sydney Metro and Parramatta",
    post_code=[["2000"], ["2150"]],
    updated_at="2026-09-22T04:30:00",
)

WRAPPER_400 = "The body is not wrapped in `tax_zone`. The message is `tax_zone missing`."

ENDPOINTS = [
    {
        "key": "list_tax_zones",
        "slug": "list-tax-zones",
        "title": "List tax zones",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 tax zones per call, with paging details in `pagination`.",
        "description": "Returns the tax zones under `tax_zones`, up to 20 per call, with a `pagination` block. Each zone has the same twelve fields that [Retrieve a tax zone](" + RETRIEVE_PAGE + ") returns. To get every zone, raise `offset` by the number of zones each page returned until you reach `pagination.total`. `q` and `field_metadata` are accepted and ignored: `q` does not filter the zones, and `field_metadata=true` returns no field descriptions.",
        "parameters": [LIMIT, OFFSET, PAGE],
        "responses": {
            "200": {
                "description": "The zones on this page under `tax_zones`, and a `pagination` block with the total, the applied `limit` and the URLs of the pages before and after.",
                "schema": {"type": "object", "properties": {
                    "tax_zones": {"type": "array", "items": ROW_REF},
                    "pagination": ref("TaxZonePagination"),
                }},
                "example": {"tax_zones": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {"description": "`limit` is below `1`, or `limit` or `offset` is not a number. The call is rejected with `invalid_pagination`, and an `errors` list names the field. The next listing you send on the same connection gets this same `400` back, even from another tax collection."},
        },
        "example_call": {"query": "limit=2"},
    },
    {
        "key": "head_tax_zones",
        "slug": "check-the-tax-zones-list",
        "title": "Check the tax zones list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns `200` with headers only, to check that the tax zones path exists.",
        "description": "Returns `200` with headers only and no body. The `200` only tells you the path exists: the store also returns `200` for methods it does not handle, and a `HEAD` response has no body to tell the two apart. Neither this response nor the listing has an `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {"description": "The path exists. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_tax_zone",
        "slug": "create-a-tax-zone",
        "title": "Create a tax zone",
        "method": "POST",
        "path": BASE,
        "summary": "Creates a tax zone and returns it with its `id`, which other calls take as `tax_zone_id`.",
        "description": "Creates a tax zone and returns it with the zone's `id`; pass that `id` as `tax_zone_id` to retrieve, update or delete the zone. Wrap the fields in `tax_zone` and always send `name`. `radius` and `start_location` are read only when you send `use_radius: true`: without it they are stored as `0.0` and `\"\"`, and a `radius` is stored as a whole number, so `7.5` reads back as `7`. A new zone always has `default` and `system_generated` set to `false`, and fields a zone does not have are ignored.",
        "body": {"schema": WRITE_BODY, "example": CREATE_BODY},
        "responses": {
            "201": {
                "description": "The new tax zone under `tax_zone`, with each post code in `post_code` in a list of its own.",
                "schema": ROW_RESPONSE,
                "example": {"tax_zone": CREATED_ZONE},
            },
            "400": {"description": WRAPPER_400},
            "500": {"description": "The body has no `name`. Or a `countries` or `states` entry is a plain number instead of a record (`No such property: id for class: java.lang.Integer`), holds only a `code`, or holds an `id` that matches no country or state (`Cannot get property 'id' on null object`). Or `post_code` is nested (`JSONArray cannot be cast to String`). After a `500` from a bad `countries` or `states` entry, the zone can still have been created, and the `500` does not include its `id`: look for the zone by `name` in the listing."},
        },
        "example_call": {},
    },
    {
        "key": "get_tax_zone",
        "slug": "retrieve-a-tax-zone",
        "title": "Retrieve a tax zone",
        "method": "GET",
        "path": BASE + "/{tax_zone_id}",
        "summary": "Returns the tax zone whose `id` you pass as `tax_zone_id`.",
        "description": "Returns one tax zone under the `tax_zone` key, with the same twelve fields a listing row has. `post_code` comes back as a list of lists, such as `[[\"2000\"], [\"3000\"]]`. The response has no `ETag` or `Last-Modified` header.",
        "parameters": [TAX_ZONE_ID],
        "responses": {
            "200": {
                "description": "The tax zone.",
                "schema": ROW_RESPONSE,
                "example": {"tax_zone": SAMPLE_ROWS[0]},
            },
            "404": {"description": "No zone has that `tax_zone_id`. The message is `Rule not found`, not the `Zone not found` that a delete returns. The next retrieve you send on the same connection, from any tax collection, returns `404` too, even when that record exists."},
        },
        "example_call": {"path": {"tax_zone_id": 1}},
    },
    {
        "key": "head_tax_zone",
        "slug": "check-a-tax-zone",
        "title": "Check a tax zone",
        "method": "HEAD",
        "path": BASE + "/{tax_zone_id}",
        "summary": "Returns headers only, and `200` even when no zone has that `tax_zone_id`.",
        "description": "Returns `200` with headers only and no body. It returns `200` even when no zone has that `tax_zone_id`, so it does not tell you whether the zone exists. To check that, use [Retrieve a tax zone](" + RETRIEVE_PAGE + "), which returns `404` when no zone has it.",
        "parameters": [TAX_ZONE_ID],
        "responses": {
            "200": {"description": "Headers only, no body. Returned even when no zone has that `tax_zone_id`."},
        },
        "example_call": {"path": {"tax_zone_id": 1}},
    },
    {
        "key": "update_tax_zone",
        "slug": "update-a-tax-zone",
        "title": "Update a tax zone",
        "method": "PUT",
        "path": BASE + "/{tax_zone_id}",
        "summary": "Replaces a tax zone's name, countries, states and post codes, and returns the updated zone.",
        "description": "Updates the tax zone whose `id` you pass as `tax_zone_id` and returns the updated zone. Wrap the fields in `tax_zone`, and always send `name`: an update without it fails with `500`. The call replaces `countries`, `states` and `post_code` with the lists you send, so a list you leave out comes back empty, and a `use_radius` you leave out comes back `false`. `radius` and `start_location` are saved only with `use_radius: true`, and keep their stored values when you leave them out.",
        "parameters": [TAX_ZONE_ID],
        "body": {"schema": WRITE_BODY, "example": UPDATE_BODY},
        "responses": {
            "200": {
                "description": "The updated tax zone under `tax_zone`. A method these paths do not handle also returns `200`, with `{\"isSuccess\": false, \"message\": \"Invalid API Request\"}` and nothing stored, so check that the response holds `tax_zone`.",
                "schema": ROW_RESPONSE,
                "example": {"tax_zone": UPDATED_ZONE},
            },
            "400": {"description": WRAPPER_400},
            "500": {"description": "The body has no `name`. Or a `countries` or `states` entry is a plain number, holds only a `code`, or holds an `id` that matches no country or state. Or `post_code` is nested."},
        },
        "example_call": {"path": {"tax_zone_id": 83}},
    },
    {
        "key": "delete_tax_zone",
        "slug": "delete-a-tax-zone",
        "title": "Delete a tax zone",
        "method": "DELETE",
        "path": BASE + "/{tax_zone_id}",
        "summary": "Deletes a tax zone permanently and returns `204` with no body.",
        "description": "Deletes the zone permanently and returns `204` with no body. The zone leaves the listing, and `pagination.total` goes down by one. A `DELETE` sent straight after a `404` from a tax endpoint returns that same `404` and deletes nothing; sent after a successful read, it deletes the zone.",
        "parameters": [TAX_ZONE_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {"description": "No zone has that `tax_zone_id`, including a zone you already deleted. The message is `Zone not found`. You also get the previous request's `404`, with nothing deleted, when the tax request just before this one was rejected with `404`."},
        },
        "example_call": {"path": {"tax_zone_id": 83}},
    },
]


def place(kind):
    return {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The %s's `id`. Send it in a zone's `%s` list, as in `[{\"id\": %d}]`, to add this %s to the zone." % (kind, "countries" if kind == "country" else "states", 12 if kind == "country" else 67, kind)},
        "name": {"type": "string", "description": "The %s's name." % kind},
        "code": {"type": "string", "description": "The %s's code." % kind},
    }}


def place_input(kind):
    return {"type": "object", "required": ["id"], "description": "A record holding the %s's `id`. A plain number instead of a record, a record with only a `code`, or an `id` that matches no %s fails with `500`." % (kind, kind), "properties": {
        "id": {"type": "integer", "description": "The %s's `id`, as a zone's `%s` list returns it." % (kind, "countries" if kind == "country" else "states")},
    }}


SCHEMAS = {
    "TaxZone": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The tax zone's `id`, assigned by the store. The other calls take it as `tax_zone_id`."},
        "name": {"type": "string", "description": "The zone's name. Required on a create and on every update."},
        "system_generated": {"type": "boolean", "description": "`true` on the zones the store created itself. Read-only: a zone you create has `false`."},
        "default": {"type": "boolean", "description": "Read-only. A zone you create has `false`, even if you send `true`."},
        "use_radius": {"type": "boolean", "description": "Whether a write saves `radius` and `start_location`. An update that leaves it out sets it to `false`."},
        "radius": {"type": "number", "description": "Stored as a whole number: `7.5` reads back as `7`. A write saves it only when you also send `use_radius: true`; a create without `use_radius: true` stores `0.0`."},
        "start_location": {"type": "string", "description": "A write saves it only when you also send `use_radius: true`; a create without `use_radius: true` stores `\"\"`."},
        "countries": {"type": "array", "items": ref("TaxZoneCountry"), "description": "The countries in the zone. An update that leaves it out empties it."},
        "states": {"type": "array", "items": ref("TaxZoneState"), "description": "The states in the zone. An update that leaves it out empties it."},
        "post_code": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}, "description": "The zone's post codes, each in a list of its own: `[[\"2000\"], [\"3000\"]]`. You send them as a flat list. An update that leaves it out empties it."},
        "created_at": {"type": "string", "description": "When the zone was created."},
        "updated_at": {"type": "string", "description": "When the zone was last changed."},
    }},
    "TaxZoneCountry": place("country"),
    "TaxZoneState": place("state"),
    "TaxZoneInput": {"type": "object", "required": ["name"], "properties": {
        "name": {"type": "string", "description": "Required on a create and on every update. A body without it fails with `500`."},
        "countries": {"type": "array", "items": ref("TaxZoneCountryInput"), "description": "The countries in the zone, such as `[{\"id\": 12}]`. On an update, leaving it out empties the list."},
        "states": {"type": "array", "items": ref("TaxZoneStateInput"), "description": "The states in the zone, such as `[{\"id\": 67}]`. On an update, leaving it out empties the list."},
        "post_code": {"type": "array", "items": {"type": "string"}, "description": "A flat list, such as `[\"2000\", \"3000\"]`. The nested form a zone returns fails with `500`. On an update, leaving it out empties the list."},
        "radius": {"type": "number", "description": "Saved only when you also send `use_radius: true`. Stored as a whole number, so `7.5` reads back as `7`."},
        "start_location": {"type": "string", "description": "Saved only when you also send `use_radius: true`."},
        "use_radius": {"type": "boolean", "description": "Send `true` to store `radius` and `start_location`. On an update, leaving it out sets it to `false`."},
    }},
    "TaxZoneCountryInput": place_input("country"),
    "TaxZoneStateInput": place_input("state"),
    "TaxZonePagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of tax zones in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of zones skipped before this page."},
        "count": {"type": "integer", "description": "The number of zones on this page."},
        "current_page": {"type": "integer", "description": "The number of this page."},
        "total_pages": {"type": "integer", "description": "The number of pages."},
        "has_next": {"type": "boolean", "description": "Whether more zones follow this page."},
        "has_previous": {"type": "boolean", "description": "Whether zones come before this page."},
        "previous_page": {"type": ["string", "null"], "description": "The URL of the previous page, or `null` on the first page."},
        "next_page": {"type": ["string", "null"], "description": "The URL of the next page, or `null` on the last page."},
    }},
}
