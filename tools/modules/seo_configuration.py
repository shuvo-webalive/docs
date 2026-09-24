"""The SEO configuration settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "SEO configuration"
SLUG = "seo-configuration"
BASE = "/admin/settings/seo_configuration"
ICON = "magnifying-glass"

SECTIONS = ["global_store_settings", "custom_code", "url_settings"]

GET_PAGE = "/api-reference/seo-configuration/get-seo-configuration"
PATCH_PAGE = "/api-reference/seo-configuration/update-seo-configuration"
SECTION_PATCH_PAGE = "/api-reference/seo-configuration/update-a-settings-section"
DELETE_FILE_PAGE = "/api-reference/seo-configuration/delete-a-document-root-file"
RETRIEVE_REDIRECT_PAGE = "/api-reference/seo-configuration/retrieve-a-redirect"
PUT_PAGE = "/api-reference/seo-configuration/replace-seo-configuration-sections"

OVERVIEW_DESCRIPTION = "Read and change your store's SEO title and description templates, custom header and footer code and URL settings, and manage its redirects and document root files."
INTRO = "The SEO configuration API has fifteen endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/seo_configuration`."

WARNING = (
    "**A `PUT` resets every field you leave out of a section you send.** This applies on\n"
    "  `/seo_configuration` and on `/seo_configuration/{section}`. A section you leave out keeps its\n"
    "  values, but inside a section you send, each missing field goes back to its default: sending only\n"
    "  `regenerate_url_on_item_update` in `url_settings` resets a stored `true` in\n"
    "  `auto_redirect_on_url_change` to `false`. To change some fields and keep the rest, use `PATCH`,\n"
    "  or send each section whole."
)

NOTES = [
    "**SEO configuration has three settings sections and two collections.** `global_store_settings`,\n"
    "  `custom_code` and `url_settings` are settings: read or write all three through `/seo_configuration`,\n"
    "  or one through `/seo_configuration/{section}`. `document_root` (the uploaded files) and\n"
    "  `redirects` are collections that you manage through their own paths. `group_meta` marks both\n"
    "  collections `writable: false`, even though you can add and delete their rows.",
    "**Settings writes are wrapped, and the wrapper depends on the path.** On `/seo_configuration`, wrap\n"
    "  the fields in `seo_configuration` and then in the section name. On `/seo_configuration/{section}`,\n"
    "  wrap them in the section's own name, such as `url_settings`: a body that is not wrapped is rejected\n"
    "  with `400 invalid_request`. Redirect writes need no wrapper: send `source_url` and\n"
    "  `destination_url` as the body itself.",
    "**`custom_code` is code the storefront serves on every page.** `header.code` is raw HTML or\n"
    "  JavaScript added to `<head>`, and `footer.code` is added before `</body>`. `field_metadata` lists\n"
    "  each `code` as requiring its block's `enabled` (`header.enabled` or `footer.enabled`).",
    "**A collection listing returns at most 100 rows per call.** The default and the maximum `limit` are\n"
    "  `100`: a larger value is capped, and `pagination.limit` shows `100`. Send a higher `offset` to get\n"
    "  the next rows while `pagination.has_next` is `true`. `pagination` has five keys: `total`, `limit`,\n"
    "  `offset`, `has_previous` and `has_next`.",
    "**Writes are limited in a ten-second window.** The store accepts fewer writes than reads in each\n"
    "  fixed ten-second window, and a write over the limit is rejected with a `Retry-After` header. A retry\n"
    "  sent before then counts against the same limit, so wait the time `Retry-After` gives before you\n"
    "  write again.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The settings section: `global_store_settings`, `custom_code` or `url_settings`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "url_settings"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field of the three settings sections, keyed by section. The settings and `group_meta` are still returned. `document_root` and `redirects` have no entry.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. The section's settings are still returned. For `url_settings` it describes the two settings and not `redirects`. It works on reads only: a write sent with `field_metadata=true` returns the section without it.",
    "schema": {"type": "boolean", "example": True},
}

LIMIT = {"name": "limit", "in": "query", "description": "Rows per page, from `1` up. The default and the maximum are `100`: a larger value is capped at `100`, and `pagination.limit` shows `100`. `0`, a negative number or a value that is not a number is rejected with `400`.", "schema": {"type": "integer", "minimum": 1, "maximum": 100, "example": 100}}
OFFSET = {"name": "offset", "in": "query", "description": "Number of rows to skip. A negative number or a value that is not a number is rejected with `400`.", "schema": {"type": "integer", "minimum": 0, "example": 0}}
FIELD_METADATA_IGNORED = {"name": "field_metadata", "in": "query", "description": "Accepted and ignored: the response is the same without it.", "schema": {"type": "boolean", "example": True}}

CONFIG_KEY = {
    "name": "config_key",
    "in": "path",
    "required": True,
    "description": "The file's `config_key`, from the listing or from the response to uploading it, such as `seo-upload-6`. It is not the file name.",
    "schema": {"type": "string", "example": "seo-upload-6"},
}

REDIRECT_ID = {
    "name": "redirect_id",
    "in": "path",
    "required": True,
    "description": "The redirect's `id`, from the listing or from the response to creating it.",
    "schema": {"type": "integer", "example": 280},
}

LISTED_REDIRECT_ID = dict(REDIRECT_ID, schema={"type": "integer", "example": 16})

TITLE_SEPARATORS = ["|", "-", "•", "·", "›", "»"]

SAMPLE_GLOBAL_STORE_SETTINGS = {
    "store_name": "Example Store",
    "title_separator": "-",
    "pages": {"disable_indexing": False, "title_template": ["{title}", "{site_name}"], "description_template": ["{site_title}"]},
    "products": {"disable_indexing": False, "title_template": ["{title}", "{site_name}", "{price}"], "description_template": ["{description}"]},
    "categories": {"disable_indexing": False, "title_template": ["{title}"], "description_template": ["{site_title}"]},
}

SAMPLE_CUSTOM_CODE = {
    "header": {"enabled": True, "code": "<!-- demo header -->"},
    "footer": {"enabled": True, "code": "<!-- demo footer -->"},
}

SAMPLE_REDIRECT_ROWS = [
    {"id": 16, "source_url": "/old-home", "destination_url": "https://your-store.example.com/"},
    {"id": 19, "source_url": "/products/old-widget", "destination_url": "https://your-store.example.com/products/new-widget"},
]

SAMPLE_URL_SETTINGS = {
    "regenerate_url_on_item_update": False,
    "auto_redirect_on_url_change": True,
    "redirects": {"items": SAMPLE_REDIRECT_ROWS},
}

SAMPLE_DOCUMENT_ROOT_ROWS = [
    {"config_key": "seo-upload-2", "file_name": "ads.txt", "file_path": "seo-upload/ads.txt"},
    {"config_key": "seo-upload-3", "file_name": "site-verification.html", "file_path": "seo-upload/site-verification.html"},
]


def section_meta(name, kind, writable):
    return {"kind": kind, "writable": writable, "href": "/api/v4" + BASE + "/" + name}


SAMPLE_GROUP_META = {
    "global_store_settings": section_meta("global_store_settings", "setting", True),
    "custom_code": section_meta("custom_code", "setting", True),
    "document_root": section_meta("document_root", "collection", False),
    "url_settings": dict(section_meta("url_settings", "setting", True), redirects=section_meta("redirects", "collection", False)),
}

SAMPLE_SEO_CONFIGURATION = {
    "seo_configuration": {
        "global_store_settings": SAMPLE_GLOBAL_STORE_SETTINGS,
        "custom_code": SAMPLE_CUSTOM_CODE,
        "document_root": {"items": SAMPLE_DOCUMENT_ROOT_ROWS},
        "url_settings": SAMPLE_URL_SETTINGS,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_SEO_CONFIGURATION = copy.deepcopy(SAMPLE_SEO_CONFIGURATION)
PATCHED_SEO_CONFIGURATION["seo_configuration"]["url_settings"]["regenerate_url_on_item_update"] = True

REPLACED_SEO_CONFIGURATION = copy.deepcopy(PATCHED_SEO_CONFIGURATION)
REPLACED_SEO_CONFIGURATION["seo_configuration"]["url_settings"]["auto_redirect_on_url_change"] = True

PATCHED_URL_SETTINGS = dict(copy.deepcopy(SAMPLE_URL_SETTINGS), regenerate_url_on_item_update=True)

SAMPLE_PAGINATION = {"total": 2, "limit": 100, "offset": 0, "has_previous": False, "has_next": False}

UPLOADED_FILE = {"config_key": "seo-upload-6", "file_name": "verification.txt", "file_path": "seo-upload/verification.txt"}

NEW_REDIRECT = {"id": 280, "source_url": "/old-page", "destination_url": "https://your-store.example.com/new-page"}
MOVED_REDIRECT = dict(NEW_REDIRECT, destination_url="https://your-store.example.com/newer-page")


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


def collection_error(code, message, error, errors=None):
    body = {"status": "error", "code": code, "message": message, "error": error}
    if errors:
        body["errors"] = errors
    return body


def section_error(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


COLLECTION_ERROR = ref("SeoConfigurationError")
SECTION_ERROR = ref("SeoConfigurationSectionError")

WHOLE_RESPONSE = {"type": "object", "properties": {
    "seo_configuration": ref("SeoConfiguration"),
    "group_meta": ref("SeoGroupMeta"),
}}

SECTION_PROPERTIES = {
    "global_store_settings": ref("SeoGlobalStoreSettings"),
    "custom_code": ref("SeoCustomCode"),
    "url_settings": ref("SeoUrlSettings"),
}

SECTION_RESPONSE = {"type": "object", "description": "Holds only the key of the section in the path.", "properties": SECTION_PROPERTIES}

SECTION_BODY = {"type": "object", "description": "Wrap the fields in the name of the section in the path.", "properties": {
    "global_store_settings": ref("SeoGlobalStoreSettings"),
    "custom_code": ref("SeoCustomCode"),
    "url_settings": ref("SeoUrlSettingsInput"),
}}

REDIRECT_RESPONSE = {"type": "object", "properties": {"redirect": ref("SeoRedirect")}}

PAGING_400 = {
    "description": "A paging value is not accepted: `limit` is below `1`, `offset` is below `0`, or either is not a number. The message is `paging values must be non-negative integers`, and `details[0].code` is `invalid_integer`, with the value you sent in `details[0].value`.",
    "schema": SECTION_ERROR,
    "example": section_error(
        "invalid_request", "paging values must be non-negative integers",
        [{"field": None, "code": "invalid_integer", "message": None, "value": "abc"}],
        "316db837-49c8-4697-940d-90a46d9428a1",
    ),
}

ENDPOINTS = [
    {
        "key": "get_seo_configuration",
        "slug": "get-seo-configuration",
        "title": "Get SEO configuration",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all three settings sections, the document root files, the redirects and a `group_meta` block.",
        "description": "Returns every SEO setting under `seo_configuration`: the `global_store_settings`, `custom_code` and `url_settings` sections, the files of `document_root`, and, inside `url_settings`, the rows of `redirects`. The files and redirects come without a `pagination` block. Beside it, `group_meta` gives each part's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field in the three settings sections, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "The whole configuration and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(WHOLE_RESPONSE["properties"], field_metadata=dict(ref("SeoFieldMetadata"), description="Only when you send `field_metadata=true`. Keyed by section."))},
                "example": SAMPLE_SEO_CONFIGURATION,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_seo_configuration",
        "slug": "update-seo-configuration",
        "title": "Update SEO configuration",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns the whole configuration.",
        "description": "Send the fields to change inside `seo_configuration`, grouped by section name. Only the fields you send change: other fields, and sections you leave out, keep their stored values. Returns the whole configuration with `group_meta`, as [Get SEO configuration](" + GET_PAGE + ") does. A section name that does not exist, or a body that is not valid JSON, is rejected with `400`.",
        "body": {
            "schema": {"type": "object", "required": ["seo_configuration"], "properties": {
                "seo_configuration": dict(ref("SeoConfigurationInput"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"seo_configuration": {"url_settings": {"regenerate_url_on_item_update": True}}},
        },
        "responses": {
            "200": {"description": "The whole configuration after the change, with `group_meta`.", "schema": WHOLE_RESPONSE, "example": PATCHED_SEO_CONFIGURATION},
            "400": {
                "description": "The body names a section that does not exist (`<name>: not a recognized section`, with `errors[0].code` `unknown_field`), or is not valid JSON (`error` is `malformed_json`).",
                "schema": COLLECTION_ERROR,
                "example": collection_error(400, "Request body is not valid JSON", "malformed_json"),
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "put_seo_configuration",
        "slug": "replace-seo-configuration-sections",
        "title": "Replace SEO configuration sections",
        "method": "PUT",
        "path": BASE,
        "summary": "Replaces each section you send and returns the whole configuration. Omitted fields reset to defaults.",
        "description": "Send whole sections inside `seo_configuration`, grouped by section name. A section you leave out keeps its stored values. Inside a section you send, every field you leave out is reset to its default. Returns the whole configuration with `group_meta`; to change some fields and keep the rest, use [Update SEO configuration](" + PATCH_PAGE + ") instead.",
        "body": {
            "schema": {"type": "object", "required": ["seo_configuration"], "properties": {
                "seo_configuration": dict(ref("SeoConfigurationInput"), description="The sections to replace. Send every field of each section you name."),
            }},
            "example": {"seo_configuration": {"url_settings": {"regenerate_url_on_item_update": True, "auto_redirect_on_url_change": True}}},
        },
        "responses": {
            "200": {"description": "The whole configuration after the change, with `group_meta`.", "schema": WHOLE_RESPONSE, "example": REPLACED_SEO_CONFIGURATION},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_seo_configuration",
        "slug": "get-seo-configuration-headers",
        "title": "Get SEO configuration headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the whole SEO configuration, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and the same `ETag` that [Get SEO configuration](" + GET_PAGE + ") returns. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {},
    },
    {
        "key": "get_seo_configuration_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `url_settings`.",
        "description": "Returns one section under the section's own name rather than under `seo_configuration`, and without `group_meta`. `url_settings` also includes the rows of `redirects`, which you cannot write through this section. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. A section name that does not exist returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section in the path, and `field_metadata` when you ask for it.", "properties": dict(SECTION_PROPERTIES, field_metadata=dict(ref("SeoFieldMetadata"), description="Only when you send `field_metadata=true`. Keyed by field name."))},
                "example": {"url_settings": SAMPLE_URL_SETTINGS},
            },
            "404": {
                "description": "No section has that name.",
                "schema": SECTION_ERROR,
                "example": section_error("not_found", "Unknown seo_configuration section: bogus", [], "9c6626c9-a62f-4c91-88c3-9db4414845be"),
            },
        },
        "example_call": {"path": {"section": "url_settings"}},
    },
    {
        "key": "patch_seo_configuration_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that whole section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `url_settings`. A body that is not wrapped is rejected with `400 invalid_request`. Only the fields you send change; the rest keep their stored values. Returns the whole section under the same key, and for `url_settings` that includes the rows of `redirects`.",
        "parameters": [SECTION],
        "body": {"schema": SECTION_BODY, "example": {"url_settings": {"regenerate_url_on_item_update": True}}},
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": SECTION_RESPONSE, "example": {"url_settings": PATCHED_URL_SETTINGS}},
            "400": {
                "description": "The body is not wrapped in the section's name: the error names the section, with the code `required`. Or a field is rejected, and `details[].code` gives the reason: `unknown_field` for a field the section does not have, `invalid_enum` for a separator or template token that is not allowed, `invalid_type` for a template that is not an array, `invalid_boolean` for a flag that is not a boolean, or `required` for an empty `store_name` (`Site Name is required`).",
                "schema": SECTION_ERROR,
                "example": section_error(
                    "invalid_request",
                    "global_store_settings.title_separator: must be one of [|, -, •, ·, ›, »]",
                    [{"field": "global_store_settings.title_separator", "code": "invalid_enum", "message": "must be one of [|, -, •, ·, ›, »]", "value": "???"}],
                    "dbe0b00b-5d3b-44a0-8cdb-0b7c5d9aa344",
                ),
            },
        },
        "example_call": {"path": {"section": "url_settings"}},
    },
    {
        "key": "put_seo_configuration_section",
        "slug": "replace-a-settings-section",
        "title": "Replace a settings section",
        "method": "PUT",
        "path": BASE + "/{section}",
        "summary": "Replaces one section, resetting omitted fields to their defaults, and returns that whole section.",
        "description": "Send the whole section, wrapped in the section's own name, such as `url_settings`. Every field you leave out is reset to its default: sending only `regenerate_url_on_item_update` to `url_settings` resets a stored `true` in `auto_redirect_on_url_change` to `false`. Returns the whole section under the same key. To change some fields and keep the rest, use [Update a settings section](" + SECTION_PATCH_PAGE + ") instead.",
        "parameters": [SECTION],
        "body": {"schema": SECTION_BODY, "example": {"url_settings": {"regenerate_url_on_item_update": True, "auto_redirect_on_url_change": True}}},
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": SECTION_RESPONSE, "example": {"url_settings": dict(copy.deepcopy(SAMPLE_URL_SETTINGS), regenerate_url_on_item_update=True, auto_redirect_on_url_change=True)}},
            "400": {
                "description": "The body is not wrapped in the section's name: the call is rejected with `400 invalid_request`, and the error names the section, with the code `required`.",
                "schema": SECTION_ERROR,
            },
        },
        "example_call": {"path": {"section": "url_settings"}},
    },
    {
        "key": "get_seo_configuration_document_root",
        "slug": "list-document-root-files",
        "title": "List document root files",
        "method": "GET",
        "path": BASE + "/document_root",
        "summary": "Returns up to 100 document root files per call, with paging details.",
        "description": "Returns the files the site serves from fixed paths, such as a site verification file or `ads.txt`. The files are under `items`, with a `pagination` block. Each row gives the file's `config_key`, which [Delete a document root file](" + DELETE_FILE_PAGE + ") takes as `config_key`, and its `file_name` and `file_path`. Send `limit` and `offset` to page through the files.",
        "parameters": [LIMIT, OFFSET, FIELD_METADATA_IGNORED],
        "responses": {
            "200": {
                "description": "A page of document root files and the `pagination` block.",
                "schema": {"type": "object", "properties": {
                    "items": {"type": "array", "items": ref("SeoDocumentRootFile")},
                    "pagination": ref("SeoCollectionPagination"),
                }},
                "example": {"items": SAMPLE_DOCUMENT_ROOT_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": PAGING_400,
        },
        "example_call": {"query": "limit=100"},
    },
    {
        "key": "upload_seo_configuration_document_root",
        "slug": "upload-a-document-root-file",
        "title": "Upload a document root file",
        "method": "POST",
        "path": BASE + "/document_root",
        "summary": "Uploads a file to the document root and returns it with its `config_key`.",
        "description": "Send the file as `multipart/form-data`, in a part named `file`. The file name must have an extension. Returns the new file under `document_root_file`, with the `config_key` that [Delete a document root file](" + DELETE_FILE_PAGE + ") takes. The response has no `Location` header.",
        "multipart": True,
        "body": {"schema": {"type": "object", "required": ["file"], "properties": {
            "file": {"type": "string", "format": "binary", "description": "The file to upload. Its name must have an extension, such as `.txt`."},
        }}},
        "responses": {
            "201": {
                "description": "The uploaded file.",
                "schema": {"type": "object", "properties": {"document_root_file": ref("SeoDocumentRootFile")}},
                "example": {"document_root_file": UPLOADED_FILE},
            },
            "400": {
                "description": "No `file` part was sent: the call is rejected with `400 invalid_request`, and `errors[0]` names `file`. Or the file name has no extension: the message is `file name must include an extension`, and `errors[0].code` is `invalid_file`.",
                "schema": COLLECTION_ERROR,
                "example": collection_error(400, "file name must include an extension", "validation_failed", [
                    {"field": "file", "code": "invalid_file", "message": "file name must include an extension", "provided": "verification"},
                ]),
            },
        },
        "example_call": {"file": "verification.txt"},
    },
    {
        "key": "delete_seo_configuration_document_root_file",
        "slug": "delete-a-document-root-file",
        "title": "Delete a document root file",
        "method": "DELETE",
        "path": BASE + "/document_root/{config_key}",
        "summary": "Deletes a document root file by its `config_key` and returns `204` with no body.",
        "description": "Deletes the file and returns `204` with no body. The file leaves the listing. Pass the file's `config_key`, such as `seo-upload-6`, not its `file_name`. No call restores a deleted file.",
        "parameters": [CONFIG_KEY],
        "responses": {
            "204": {"description": "Deleted. No body."},
            "404": {
                "description": "No file has that `config_key`.",
                "schema": COLLECTION_ERROR,
                "example": collection_error(404, "document root file not found: seo-upload-999999", "not_found"),
            },
        },
        "example_call": {"path": {"config_key": "seo-upload-6"}},
    },
    {
        "key": "get_seo_configuration_redirects",
        "slug": "list-redirects",
        "title": "List redirects",
        "method": "GET",
        "path": BASE + "/redirects",
        "summary": "Returns up to 100 redirects per call, with paging details.",
        "description": "Returns the redirects under `items`, not under a key named `redirects`, with a `pagination` block. Each row gives the redirect's `id`, which the other redirect calls take as `redirect_id`, and its `source_url` and `destination_url`. Send `limit` and `offset` to page through the redirects.",
        "parameters": [LIMIT, OFFSET, FIELD_METADATA_IGNORED],
        "responses": {
            "200": {
                "description": "A page of redirects and the `pagination` block.",
                "schema": {"type": "object", "properties": {
                    "items": {"type": "array", "items": ref("SeoRedirect")},
                    "pagination": ref("SeoCollectionPagination"),
                }},
                "example": {"items": SAMPLE_REDIRECT_ROWS, "pagination": SAMPLE_PAGINATION},
            },
            "400": PAGING_400,
        },
        "example_call": {"query": "limit=100"},
    },
    {
        "key": "create_seo_configuration_redirect",
        "slug": "create-a-redirect",
        "title": "Create a redirect",
        "method": "POST",
        "path": BASE + "/redirects",
        "summary": "Creates a redirect and returns it with its `id`, which the other calls take as `redirect_id`.",
        "description": "Send `source_url` and `destination_url` as the body itself, with no wrapping key; a body wrapped in `redirect` is accepted too. Both fields are required. Returns the new redirect under `redirect`, with the `id` that the other redirect calls take as `redirect_id`, and a `Location` header that gives its path. A `source_url` that another redirect already has is rejected with `409`.",
        "body": {"schema": ref("SeoRedirectInput"), "example": {"source_url": "/old-page", "destination_url": "https://your-store.example.com/new-page"}},
        "responses": {
            "201": {"description": "The new redirect. The `Location` header gives its path.", "schema": REDIRECT_RESPONSE, "example": {"redirect": NEW_REDIRECT}},
            "400": {
                "description": "A required field is missing: without `destination_url` the call is rejected with `400 invalid_request`, and `errors[0].field` is `destination_url` (`Destination URL is required`). Or a URL is not valid (`Please enter a valid URL`, code `invalid_url`), both URLs resolve to the same URL (`Source and Destination resolve to the same URL`, code `invalid_reference`), or the body includes the redirect's `id` field (`id is taken from the URL path, not the body`, code `unknown_field`).",
                "schema": COLLECTION_ERROR,
            },
            "409": {
                "description": "Another redirect already has that `source_url`. The message is `a redirect for that Source URL already exists`, and `error` is `duplicate`.",
                "schema": COLLECTION_ERROR,
                "example": collection_error(409, "a redirect for that Source URL already exists", "duplicate", [
                    {"field": "source_url", "code": "duplicate", "message": "a redirect for that Source URL already exists", "provided": "/old-page"},
                ]),
            },
        },
        "example_call": {},
    },
    {
        "key": "get_seo_configuration_redirect",
        "slug": "retrieve-a-redirect",
        "title": "Retrieve a redirect",
        "method": "GET",
        "path": BASE + "/redirects/{redirect_id}",
        "summary": "Returns the redirect whose `id` you pass as `redirect_id`.",
        "description": "Returns one redirect under the `redirect` key, with the same three fields a listing row has: `id`, `source_url` and `destination_url`. If no redirect has that `redirect_id`, including one you deleted, the call returns `404 not_found`.",
        "parameters": [LISTED_REDIRECT_ID],
        "responses": {
            "200": {"description": "The redirect.", "schema": REDIRECT_RESPONSE, "example": {"redirect": SAMPLE_REDIRECT_ROWS[0]}},
            "404": {
                "description": "No redirect has that `redirect_id`. The message is `redirect not found: <redirect_id>`, and `error.code` is `not_found`.",
                "schema": SECTION_ERROR,
                "example": section_error("not_found", "redirect not found: 99999999", [], "a31f2acf-3ee8-4ef9-b1d9-eb1abf236b61"),
            },
        },
        "example_call": {"path": {"redirect_id": 16}},
    },
    {
        "key": "patch_seo_configuration_redirect",
        "slug": "update-a-redirect",
        "title": "Update a redirect",
        "method": "PATCH",
        "path": BASE + "/redirects/{redirect_id}",
        "summary": "Changes a redirect's `source_url` or `destination_url` and returns the updated redirect.",
        "description": "Send only the fields that change, as the body itself, such as a new `destination_url`. A field you leave out keeps its stored value. Returns the redirect as it now stands, under `redirect`.",
        "parameters": [REDIRECT_ID],
        "body": {"schema": ref("SeoRedirectUpdate"), "example": {"destination_url": "https://your-store.example.com/newer-page"}},
        "responses": {
            "200": {"description": "The updated redirect.", "schema": REDIRECT_RESPONSE, "example": {"redirect": MOVED_REDIRECT}},
        },
        "example_call": {"path": {"redirect_id": 280}},
    },
    {
        "key": "delete_seo_configuration_redirect",
        "slug": "delete-a-redirect",
        "title": "Delete a redirect",
        "method": "DELETE",
        "path": BASE + "/redirects/{redirect_id}",
        "summary": "Deletes a redirect permanently and returns `204` with no body.",
        "description": "Deletes the redirect and returns `204` with no body. After that, [Retrieve a redirect](" + RETRIEVE_REDIRECT_PAGE + ") returns `404` for its `redirect_id`. No call restores a deleted redirect.",
        "parameters": [REDIRECT_ID],
        "responses": {
            "204": {"description": "Deleted. No body."},
        },
        "example_call": {"path": {"redirect_id": 280}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def tokens(values, description):
    return {"type": "array", "items": {"type": "string", "enum": values}, "description": description}


def template_block(content, title_tokens, description_tokens):
    return {"type": "object", "description": "The indexing setting and the title and description templates for " + content + ".", "properties": {
        "disable_indexing": flag("Stop search engines indexing your " + content + ". Defaults to `false`."),
        "title_template": tokens(title_tokens, "The tokens that build the title, in order. Any other token is rejected with `400` (`invalid_enum`), and a value that is not an array with `invalid_type`."),
        "description_template": tokens(description_tokens, "The tokens that build the meta description, in order."),
    }}


SCHEMAS = {
    "SeoConfiguration": {"type": "object", "description": "The three settings sections and the rows of `document_root`. The rows of `redirects` are inside `url_settings`.", "properties": {
        "global_store_settings": ref("SeoGlobalStoreSettings"),
        "custom_code": ref("SeoCustomCode"),
        "document_root": ref("SeoDocumentRootRows"),
        "url_settings": ref("SeoUrlSettings"),
    }},
    "SeoConfigurationInput": {"type": "object", "description": "The settings sections you can write, by name. `document_root` and `redirects` have their own calls.", "properties": {
        "global_store_settings": ref("SeoGlobalStoreSettings"),
        "custom_code": ref("SeoCustomCode"),
        "url_settings": ref("SeoUrlSettingsInput"),
    }},
    "SeoGlobalStoreSettings": {"type": "object", "description": "The store name, the title separator, and the title and description templates for pages, products and categories.", "properties": {
        "store_name": {"type": "string", "description": "The store name that the `{site_name}` token puts in titles. Required: an empty value is rejected with `400` (`Site Name is required`)."},
        "title_separator": {"type": "string", "enum": TITLE_SEPARATORS, "description": "The title separator. Required. Any other value is rejected with `400` (`invalid_enum`)."},
        "pages": ref("SeoPagesTemplates"),
        "products": ref("SeoProductsTemplates"),
        "categories": ref("SeoCategoriesTemplates"),
    }},
    "SeoPagesTemplates": template_block("pages", ["{title}", "{site_name}", "{current_year}"], ["{site_title}"]),
    "SeoProductsTemplates": template_block("products", ["{title}", "{site_name}", "{current_year}", "{price}", "{category}"], ["{site_title}", "{primary_category}", "{description}"]),
    "SeoCategoriesTemplates": template_block("categories", ["{title}", "{site_name}", "{current_year}", "{category}"], ["{site_title}", "{primary_category}", "{description}"]),
    "SeoCustomCode": {"type": "object", "description": "Code the storefront adds to every page: `header` in `<head>`, `footer` before `</body>`.", "properties": {
        "header": ref("SeoCustomCodeBlock"),
        "footer": ref("SeoCustomCodeBlock"),
    }},
    "SeoCustomCodeBlock": {"type": "object", "properties": {
        "enabled": flag("Add this block's code to every page. Defaults to `false`."),
        "code": {"type": "string", "description": "Raw HTML or JavaScript. `field_metadata` lists it as requiring its block's `enabled`."},
    }},
    "SeoUrlSettings": {"type": "object", "description": "The two URL settings, and the rows of `redirects`.", "properties": {
        "regenerate_url_on_item_update": flag("Change an item's URL when its name or title changes. Defaults to `false`."),
        "auto_redirect_on_url_change": flag("Change redirection when an item's URL changes. Defaults to `false`."),
        "redirects": dict(ref("SeoRedirectRows"), description="The rows of `redirects`, without paging details. Read-only here: use the redirect calls to add, change or delete them."),
    }},
    "SeoUrlSettingsInput": {"type": "object", "description": "The two settings of `url_settings` you can write. `redirects` is not one of them.", "properties": {
        "regenerate_url_on_item_update": flag("Change an item's URL when its name or title changes. Defaults to `false`."),
        "auto_redirect_on_url_change": flag("Change redirection when an item's URL changes. Defaults to `false`."),
    }},
    "SeoRedirectRows": {"type": "object", "properties": {"items": {"type": "array", "items": ref("SeoRedirect")}}},
    "SeoDocumentRootRows": {"type": "object", "description": "The rows of `document_root`, without paging details.", "properties": {"items": {"type": "array", "items": ref("SeoDocumentRootFile")}}},
    "SeoDocumentRootFile": {"type": "object", "properties": {
        "config_key": {"type": "string", "description": "The file's key, assigned by the store, such as `seo-upload-6`. Pass it as `config_key` in a path. It is not the file name."},
        "file_name": {"type": "string", "description": "The name of the uploaded file."},
        "file_path": {"type": "string", "description": "The file's path: `seo-upload/` followed by the file name."},
    }},
    "SeoRedirect": {"type": "object", "properties": {
        "id": {"type": "integer", "description": "The redirect's id, assigned by the store. Pass it as `redirect_id` in a path."},
        "source_url": {"type": "string", "description": "The URL that is redirected, such as `/old-page`. No two redirects can have the same `source_url`."},
        "destination_url": {"type": "string", "description": "The URL the redirect goes to."},
    }},
    "SeoRedirectInput": {"type": "object", "required": ["source_url", "destination_url"], "properties": {
        "source_url": {"type": "string", "description": "Required. A valid URL that no other redirect has."},
        "destination_url": {"type": "string", "description": "Required. A valid URL that does not resolve to the same URL as `source_url`."},
    }},
    "SeoRedirectUpdate": {"type": "object", "description": "Send only the fields that change.", "properties": {
        "source_url": {"type": "string", "description": "The new URL to redirect."},
        "destination_url": {"type": "string", "description": "The new URL the redirect goes to."},
    }},
    "SeoCollectionPagination": {"type": "object", "properties": {
        "total": {"type": "integer", "description": "The number of rows in the collection."},
        "limit": {"type": "integer", "description": "The page size the store applied. At most `100`."},
        "offset": {"type": "integer", "description": "The number of rows skipped before this page."},
        "has_previous": {"type": "boolean"},
        "has_next": {"type": "boolean"},
    }},
    "SeoGroupMeta": {"type": "object", "description": "One entry per part of the configuration. Only [Get SEO configuration](" + GET_PAGE + "), [Update SEO configuration](" + PATCH_PAGE + ") and [Replace SEO configuration sections](" + PUT_PAGE + ") return it.", "properties": {
        "global_store_settings": ref("SeoSectionMeta"),
        "custom_code": ref("SeoSectionMeta"),
        "document_root": ref("SeoSectionMeta"),
        "url_settings": ref("SeoSectionMeta"),
    }},
    "SeoSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "`setting` for the three settings sections, `collection` for `document_root` and `redirects`."},
        "writable": {"type": "boolean", "description": "`true` for the three settings sections. `false` for `document_root` and `redirects`, even though you can add and delete their rows."},
        "href": {"type": "string", "description": "The part's own path, such as `/api/v4/admin/settings/seo_configuration/url_settings`."},
        "redirects": dict(ref("SeoSectionMeta"), description="Only in the `url_settings` entry: the entry for `redirects`."),
    }},
    "SeoFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Has the same nesting as the settings, with a `SeoFieldMetadataEntry` in place of each value."},
    "SeoFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes: `string`, `enum`, `enum_list`, `boolean` or `text`."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field does."},
        "required": {"type": "boolean", "description": "Whether the field must have a value."},
        "writable": {"type": "boolean", "description": "Whether a write can set the field."},
        "deprecated": {"type": "boolean"},
        "default": {"description": "The field's default value."},
        "allowed_values": {"type": "array", "items": {"type": "string"}, "description": "The values the field accepts, for an `enum` or `enum_list` field."},
        "labels": {"type": "object", "additionalProperties": {"type": "string"}, "description": "A label for each allowed value, for an `enum` field."},
        "requires": {"type": "string", "description": "The field this one depends on, such as `header.enabled`."},
    }},
    "SeoConfigurationError": {"type": "object", "description": "The error from the redirect and document root writes, and from writes to `/seo_configuration`.", "properties": {
        "status": {"type": "string", "description": "`error`."},
        "code": {"type": "integer", "description": "The HTTP status."},
        "message": {"type": "string"},
        "error": {"type": "string", "description": "A machine-readable reason, such as `not_found`, `duplicate` or `malformed_json`."},
        "errors": {"type": "array", "description": "One entry per rejected field, when the error is about a field.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field that was rejected."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `invalid_url` or `duplicate`."},
            "message": {"type": "string"},
            "provided": {"description": "The rejected value, when the store includes it."},
        }}},
    }},
    "SeoConfigurationSectionError": {"type": "object", "description": "The error from `/seo_configuration/{section}`, and from reads of the redirects and the document root, such as a `redirect_id` that no redirect has or a `limit` that is not accepted.", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field or paging value. Empty when the error is not about a value you sent.", "items": {"type": "object", "properties": {
                "field": {"type": ["string", "null"], "description": "The field that was rejected, such as `global_store_settings.title_separator`. `null` for a rejected paging value."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `invalid_enum`, `invalid_boolean` or `invalid_integer`."},
                "message": {"type": ["string", "null"]},
                "value": {"description": "The value you sent, when the store includes it."},
            }}},
            "request_id": {"type": "string", "description": "A value that identifies this request."},
        }},
    }},
}
