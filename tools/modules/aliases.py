"""The Domain aliases endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Domain aliases"
SLUG = "domain-aliases"
BASE = "/admin/aliases"
ICON = "globe"

LIST_PAGE = "/api-reference/domain-aliases/list-domain-aliases"
CREATE_PAGE = "/api-reference/domain-aliases/create-a-domain-alias"
DELETE_PAGE = "/api-reference/domain-aliases/delete-a-domain-alias"

OVERVIEW_DESCRIPTION = "List, create and delete your store's domain aliases, the extra hostnames your store responds to."
INTRO = "The Domain aliases API has four endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/aliases`."

WARNING = (
    "**Send the hostname in `alias` as a plain string, with no wrapper.** The create body is\n"
    "  `{\"alias\": \"shop.example.com\"}`. The create response returns the new alias as a record under the\n"
    "  same `alias` key, but a body in that record shape, `{\"alias\": {\"alias\": \"shop.example.com\"}}`, is\n"
    "  rejected with `400 invalid_hostname`."
)

NOTES = [
    "**You can list, create and delete aliases, but you cannot read or change one alias.**\n"
    "  `/admin/aliases/{alias_id}` allows only `DELETE` and `OPTIONS`. `GET`, `HEAD`, `PUT`, `PATCH` and\n"
    "  `POST` on it return `405` with the header `Allow: DELETE, OPTIONS`, and a `PUT` or `PATCH` changes\n"
    "  nothing. To find one alias, page through [List domain aliases](" + LIST_PAGE + ") and match the\n"
    "  hostname in `alias` or the alias's `id`. There is no count call: `GET /admin/aliases/count` also\n"
    "  returns `405`, because the store reads `count` as an `alias_id`.",
    "**The site settings show the same hostnames under `domain_settings.aliases`.** There they are a\n"
    "  read-only list of strings. Creating an alias here adds its hostname to that list, and deleting\n"
    "  the alias removes it.",
    "**`alias` must be a well-formed hostname that no other alias has, in any letter case.** A hostname\n"
    "  with a space, a scheme, an underscore, a leading hyphen or an 87-character label is rejected with\n"
    "  `400 invalid_hostname`, and so is an `alias` that is a number or a list. A hostname another alias\n"
    "  already has, in the same or another letter case, is rejected with `409` and the message\n"
    "  `alias already exists`. The store trims whitespace around the hostname and keeps the letter case you send.",
    "**A listing returns at most 20 aliases per call.** A larger `limit` is capped at `20`, and\n"
    "  `pagination.limit` shows `20`. To get more, send the next `page` or a higher `offset` while\n"
    "  `pagination.has_next` is `true`. The listing accepts only `limit`, `offset`, `page` and\n"
    "  `field_metadata`, and rejects any other parameter with `400 unknown_parameter`. `field_metadata`\n"
    "  adds nothing to the response.",
    "**Every error body has `status`, `code` and `message` at the top level.** `status` is `error`, and\n"
    "  `code` is the HTTP status, such as `404`. Some errors also have `error`, a machine-readable reason\n"
    "  such as `invalid_hostname` or `method_not_allowed`. A `400` for a bad hostname or a bad query\n"
    "  parameter also has an `errors` list, and each entry names the rejected `field` and a `code`.",
]

ALIAS_ID = {
    "name": "alias_id",
    "in": "path",
    "required": True,
    "description": "The alias's `id`, from [List domain aliases](" + LIST_PAGE + ") or from the response to [Create a domain alias](" + CREATE_PAGE + ").",
    "schema": {"type": "integer", "example": 115},
}

LIMIT = {"name": "limit", "in": "query", "description": "Aliases per page. The default and the maximum are `20`: a larger value is capped at `20`, and `pagination.limit` shows `20`. `0`, a negative number or a value that is not a number is rejected with `400`; for `0` the message is `'limit' must be a positive integer`.", "schema": {"type": "integer", "minimum": 1, "maximum": 20, "example": 20}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of aliases to skip. When you send both `offset` and `page`, `offset` wins.", "schema": {"type": "integer", "example": 0}}
PAGE = {"name": "page", "in": "query", "description": "1-based page number, read as `offset = (page - 1) * limit` against the limit the store applied. `page=2` alone skips 20 aliases; `limit=1&page=2` skips 1. `page=0` returns the first page.", "schema": {"type": "integer", "example": 1}}
FIELD_METADATA = {"name": "field_metadata", "in": "query", "description": "Accepted, but adds nothing: `field_metadata=true` returns the same keys and the same aliases as `false`.", "schema": {"type": "boolean", "example": True}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR_REF = ref("AliasError")
ROW_REF = ref("Alias")

SAMPLE_ROWS = [
    {"id": 40, "alias": "shop2.example.com", "created_at": "2026-08-03T11:08:54", "updated_at": "2026-08-03T11:08:54"},
    {"id": 109, "alias": "shop3.example.com", "created_at": "2026-08-24T12:08:10", "updated_at": "2026-08-24T12:08:10"},
    {"id": 115, "alias": "shop.example.com", "created_at": "2026-08-31T11:57:23", "updated_at": "2026-08-31T11:57:23"},
]

SAMPLE_PAGINATION = {"total": 3, "limit": 20, "offset": 0, "has_previous": False, "has_next": False}

UNKNOWN_PARAMETER = {
    "status": "error", "code": 400, "message": "unknown query parameter(s): q", "error": "unknown_parameter",
    "errors": [{"field": "q", "code": "unknown_parameter"}],
}
INVALID_HOSTNAME = {
    "status": "error", "code": 400, "message": "alias must be a valid hostname", "error": "invalid_hostname",
    "errors": [{"field": "alias", "code": "invalid_hostname", "message": "must be a well-formed hostname/FQDN (e.g. shop.example.com)", "provided": "not a valid host!!"}],
}
ALREADY_EXISTS = {"status": "error", "code": 409, "message": "alias already exists"}
UNEXPECTED_ERROR = {"status": "error", "code": 500, "message": "Unexpected Error Occurred"}
NOT_FOUND = {"status": "error", "code": 404, "message": "alias not found"}

ENDPOINTS = [
    {
        "key": "list_aliases",
        "slug": "list-domain-aliases",
        "title": "List domain aliases",
        "method": "GET",
        "path": BASE,
        "summary": "Returns up to 20 domain aliases per call, with paging details.",
        "description": "Returns your store's domain aliases, up to 20 per call, with a `pagination` block. Only `limit`, `offset`, `page` and `field_metadata` are accepted; any other parameter, such as `q` or `sort`, is rejected with `400 unknown_parameter`. After a rejected `limit`, the next request on the same client returns that rejection's body instead of its own. A client you create after the rejection is not affected.",
        "parameters": [LIMIT, OFFSET, PAGE, FIELD_METADATA],
        "responses": {
            "200": {
                "description": "`aliases` lists up to 20 domain aliases, each with its `id`, its hostname in `alias`, `created_at` and `updated_at`. A new alias is listed last. In `pagination`, `total` is the number of aliases in the store and `has_next` is `true` when more follow. The response has no `ETag` or `Last-Modified` header.",
                "schema": {"type": "object", "properties": {
                    "aliases": {"type": "array", "items": ROW_REF},
                    "pagination": ref("AliasPagination"),
                }},
                "example": {"aliases": SAMPLE_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": {
                "description": "You sent a parameter the listing does not accept, such as `q`: `error` is `unknown_parameter` and the message is `unknown query parameter(s): <name>`. Or `limit` is `0`, a negative number or not a number; for `limit=0` the message is `'limit' must be a positive integer`.",
                "schema": ERROR_REF,
                "example": UNKNOWN_PARAMETER,
            },
        },
        "example_call": {"query": "limit=20"},
    },
    {
        "key": "head_aliases",
        "slug": "check-the-domain-aliases-list",
        "title": "Check the domain aliases list",
        "method": "HEAD",
        "path": BASE,
        "summary": "Checks that the domain aliases list is reachable. Returns headers only, with no body.",
        "description": "Returns `200` with headers only and no body. The SDK function sends no query parameters. Neither this response nor the listing has an `ETag` or `Last-Modified` header.",
        "responses": {
            "200": {"description": "The list is reachable. Headers only, no body."},
        },
        "example_call": {},
    },
    {
        "key": "create_alias",
        "slug": "create-a-domain-alias",
        "title": "Create a domain alias",
        "method": "POST",
        "path": BASE,
        "summary": "Adds a hostname as an alias. Returns the new alias, whose `id` delete takes as `alias_id`.",
        "description": "Adds a hostname to your store's domain aliases and returns the new alias as a record under `alias`. The alias's `id` is what [Delete a domain alias](" + DELETE_PAGE + ") takes as `alias_id`. Send the hostname as a plain string: `{\"alias\": \"shop.example.com\"}`. The store ignores unknown fields, `created_at` and `updated_at` in the body, but a body with an `id` field returns `500` and creates nothing.",
        "body": {"schema": ref("AliasInput"), "example": {"alias": "shop.example.com"}},
        "responses": {
            "201": {
                "description": "The new alias as a record under `alias`: its `id`, the hostname in `alias`, and `created_at` and `updated_at`, which are equal. The response has no `Location` header.",
                "schema": {"type": "object", "properties": {"alias": ROW_REF}},
                "example": {"alias": SAMPLE_ROWS[2]},
            },
            "400": {
                "description": "`alias` is not a well-formed hostname, or is a number, a list or a record instead of a string: `error` is `invalid_hostname` and the message is `alias must be a valid hostname`. `alias` is an empty string or `null`, or the body has other fields but no `alias`: the message is `alias is required`. The body is `{}`: `error` is `empty_body` and the message is `request body is empty`.",
                "schema": ERROR_REF,
                "example": INVALID_HOSTNAME,
            },
            "409": {
                "description": "Another alias already has that hostname, in the same or another letter case. The message is `alias already exists`.",
                "schema": ERROR_REF,
                "example": ALREADY_EXISTS,
            },
            "500": {
                "description": "The create body includes an `id` field. The message is `Unexpected Error Occurred`, and no alias is created.",
                "schema": ERROR_REF,
                "example": UNEXPECTED_ERROR,
            },
        },
        "example_call": {},
    },
    {
        "key": "delete_alias",
        "slug": "delete-a-domain-alias",
        "title": "Delete a domain alias",
        "method": "DELETE",
        "path": BASE + "/{alias_id}",
        "summary": "Deletes the domain alias whose `id` you pass as `alias_id`. Returns `204` with no body.",
        "description": "Deletes the domain alias whose `id` you pass as `alias_id` and returns `204` with no body. The delete is permanent: the alias leaves the listing and `pagination.total` goes down by one. No call reads one alias, so to confirm the delete, check that the alias's `id` is gone from [List domain aliases](" + LIST_PAGE + ").",
        "parameters": [ALIAS_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {
                "description": "No alias has that `alias_id`, including an alias you already deleted, or `alias_id` is not a number. The message is `alias not found`.",
                "schema": ERROR_REF,
                "example": NOT_FOUND,
            },
        },
        "example_call": {"path": {"alias_id": 115}},
    },
]

SCHEMAS = {
    "Alias": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The alias's `id`, assigned by the store. Pass it as `alias_id` to delete the alias."},
        "alias": {"type": "string", "description": "The hostname, such as `shop.example.com`, with surrounding whitespace trimmed and the letter case you sent."},
        "created_at": {"type": "string", "description": "When the alias was created, such as `2026-08-31T11:57:23`. Set by the store: a value you send on create is ignored."},
        "updated_at": {"type": "string", "description": "Set by the store: a value you send on create is ignored. Equal to `created_at` on a new alias."},
    }},
    "AliasInput": {"type": "object", "required": ["alias"], "properties": {
        "alias": {"type": "string", "description": "Required. The hostname as a plain string, such as `shop.example.com`. It must be well formed, and no other alias may have it in any letter case. A record here is rejected with `400 invalid_hostname`."},
    }},
    "AliasPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of domain aliases in the store."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `20`."},
        "offset": {"type": "integer", "description": "The number of aliases skipped before this page."},
        "has_previous": {"type": "boolean", "description": "`true` when `offset` is more than `0`."},
        "has_next": {"type": "boolean", "description": "`true` when more aliases follow this page."},
    }},
    "AliasError": {"type": "object", "properties": {
        "status": {"type": "string", "description": "Always `error`."},
        "code": {"type": "integer", "description": "The HTTP status, such as `404`."},
        "message": {"type": "string", "description": "What was wrong, such as `alias not found`."},
        "error": {"type": "string", "description": "A machine-readable reason, on some errors only: `method_not_allowed`, `unknown_parameter`, `invalid_pagination`, `invalid_number`, `invalid_hostname` or `empty_body`."},
        "errors": {"type": "array", "description": "Only on a `400` for a bad hostname or a bad query parameter. Each entry names the rejected `field` and a `code`.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field or query parameter that was rejected, such as `alias` or `q`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `invalid_hostname` or `unknown_parameter`."},
            "message": {"type": "string", "description": "On a bad hostname: `must be a well-formed hostname/FQDN (e.g. shop.example.com)`."},
            "provided": {"type": "string", "description": "On a bad hostname: the value you sent."},
        }}},
    }},
}
