"""The Search settings endpoints, written from the SDKs' ENDPOINTS.md."""

import copy

TAG = "Search settings"
SLUG = "search-settings"
BASE = "/admin/settings/search_settings"
ICON = "magnifying-glass"

SECTIONS = ["searchable_content", "search_fields", "synonyms"]

GET_PAGE = "/api-reference/search-settings/get-search-settings"
PATCH_PAGE = "/api-reference/search-settings/update-search-settings"
GET_SECTION_PAGE = "/api-reference/search-settings/get-a-search-settings-section"
PUT_SECTION_PAGE = "/api-reference/search-settings/replace-a-search-settings-section"

SECTION_READ = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read: `searchable_content`, `search_fields` or `synonyms`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "search_fields"},
}

SECTION_WRITE = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to write: `searchable_content`, `search_fields` or `synonyms`. A change to `synonyms` triggers an Elasticsearch reindex that cannot be undone.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "search_fields"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in all three sections, keyed by section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields, keyed by field name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_SEARCHABLE_CONTENT = {
    "placeholder_text": "Search",
    "product": {"enabled": True, "display_heading": "Product", "excluded": [{"id": 4, "name": "Gift Card"}]},
    "product_categories": {
        "enabled": True, "hide_parent_category": True, "display_heading": "Product Categories",
        "excluded": [{"id": 16, "name": "Clearance"}],
    },
    "blog": {"enabled": True, "display_heading": "Blog Posts", "excluded": [{"id": 13, "name": "Store News"}]},
    "other_pages": {"enabled": True, "display_heading": "Other Pages", "excluded": [{"id": 4, "name": "Home - Copy"}]},
}

SAMPLE_SEARCH_FIELDS = {
    "match_keywords_exactly": False,
    "match_full_sentences": False,
    "fields": [
        {"field": "title", "priority": 1},
        {"field": "tags", "priority": 2},
        {"field": "category", "priority": 3},
        {"field": "description", "priority": 4},
        {"field": "sku", "priority": 5},
        {"field": "brand", "priority": 6},
    ],
}

SAMPLE_SYNONYMS = {
    "groups": [
        {"keywords": ["mobile", "phone", "telephone"]},
        {"keywords": ["shoe", "footwear", "sneaker"]},
    ],
}

SAMPLE_SETTINGS = {
    "searchable_content": SAMPLE_SEARCHABLE_CONTENT,
    "search_fields": SAMPLE_SEARCH_FIELDS,
    "synonyms": SAMPLE_SYNONYMS,
}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_SEARCH_SETTINGS = {"search_settings": SAMPLE_SETTINGS, "group_meta": SAMPLE_GROUP_META}

PATCHED_SEARCH_SETTINGS = copy.deepcopy(SAMPLE_SEARCH_SETTINGS)
PATCHED_SEARCH_SETTINGS["search_settings"]["searchable_content"]["placeholder_text"] = "Search products"
PATCHED_SEARCH_SETTINGS["search_settings"]["search_fields"]["match_keywords_exactly"] = True

REPLACED_SETTINGS = copy.deepcopy(SAMPLE_SETTINGS)
REPLACED_SETTINGS["searchable_content"]["placeholder_text"] = "Search products"

PATCHED_SEARCH_FIELDS = dict(copy.deepcopy(SAMPLE_SEARCH_FIELDS), match_keywords_exactly=True)

SAMPLE_REINDEX_STATUS = {
    "state": "completed",
    "started_at": "2026-08-31T12:42:58Z",
    "finished_at": "2026-08-31T12:43:08Z",
    "error": None,
}


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

SEARCH_SETTINGS_RESPONSE = {"type": "object", "properties": {
    "search_settings": ref("SearchSettings"),
    "group_meta": ref("SearchSettingsGroupMeta"),
}}

SECTION_PROPERTIES = {
    "searchable_content": ref("SearchableContent"),
    "search_fields": ref("SearchFields"),
    "synonyms": ref("Synonyms"),
}

SECTION_RESPONSE = {
    "type": "object",
    "description": "Holds only the key of the section named in the path.",
    "properties": SECTION_PROPERTIES,
}

TITLE_NOT_FIRST = error_example(
    "invalid_request", "search_fields.fields: the 'title' field must have priority 1",
    [{"field": "search_fields.fields", "code": "invalid_value", "message": "the 'title' field must have priority 1"}],
    "f3a9c1d2-6b4e-4f8a-9c2d-1e5b7a3f0c64",
)

UNKNOWN_SECTION = error_example(
    "not_found", "Unknown search_settings section: bogus", [],
    "8d2e4f6a-1b3c-4d5e-8f7a-9b0c1d2e3f45",
)

SECTION_WRITE_400 = "The body is not wrapped in the section's own name. A body with no wrapper and a body wrapped in `search_settings` are both rejected with `invalid_request` and the message `request body must be wrapped in a '<section>' object`, where `<section>` is the section named in the path."

ENDPOINTS = [
    {
        "key": "get_search_settings",
        "slug": "get-search-settings",
        "title": "Get search settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all three search settings sections and a `group_meta` block describing each one.",
        "description": "Returns every search setting under `search_settings`, with all three sections in full: `searchable_content`, `search_fields` and `synonyms`. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get a description of every field, keyed by section. The response has no `ETag` header.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All three sections and `group_meta`. With `field_metadata=true`, a `field_metadata` key is added beside them.",
                "schema": {"type": "object", "properties": dict(SEARCH_SETTINGS_RESPONSE["properties"], field_metadata=dict(
                    ref("SearchSettingsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section.",
                ))},
                "example": SAMPLE_SEARCH_SETTINGS,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_search_settings",
        "slug": "update-search-settings",
        "title": "Update search settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change inside `search_settings`, grouped by section name. One body can name several sections. Only the fields you send change, at every level: other fields in the same block, and sections you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get search settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "required": ["search_settings"], "properties": {
                "search_settings": dict(ref("SearchSettings"), description="The fields to change, grouped by section. Send only the fields that change, and leave `synonyms` out unless you mean to change it: a change to `synonyms` triggers an Elasticsearch reindex."),
            }},
            "example": {"search_settings": {
                "searchable_content": {"placeholder_text": "Search products"},
                "search_fields": {"match_keywords_exactly": True},
            }},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": SEARCH_SETTINGS_RESPONSE, "example": PATCHED_SEARCH_SETTINGS},
            "400": {
                "description": "The body is not wrapped in `search_settings` (`request body must be wrapped in a 'search_settings' object`), is not valid JSON (`Request body is not valid JSON`), names a section or field that does not exist (`unknown_field`), or sends a value a field does not accept. For a rejected value, `details[].code` gives the reason: `invalid_boolean`, `invalid_type`, `invalid_reference`, `invalid_enum`, `out_of_range`, `duplicate`, `required` or `invalid_value`.",
                "schema": ERROR,
                "example": TITLE_NOT_FIRST,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "put_search_settings",
        "slug": "replace-search-settings",
        "title": "Replace search settings",
        "method": "PUT",
        "path": BASE,
        "summary": "Replaces all three sections with the body you send. Fields you leave out are reset.",
        "description": "Replaces all three sections with the body you send, wrapped in `search_settings`. Any field or section the body leaves out is reset to its default, `synonyms` included. So every call either resets `synonyms` or writes it, and a change to `synonyms` triggers an Elasticsearch reindex that cannot be undone. To change some fields, use [Update search settings](" + PATCH_PAGE + "); to replace one section, use [Replace a search settings section](" + PUT_SECTION_PAGE + "). Returns all the settings after the change, with `group_meta`.",
        "body": {
            "schema": {"type": "object", "required": ["search_settings"], "properties": {
                "search_settings": dict(ref("SearchSettings"), description="All three sections in full. Read them first with [Get search settings](" + GET_PAGE + "), change what you need, and send them all back."),
            }},
            "example": {"search_settings": REPLACED_SETTINGS},
        },
        "responses": {
            "200": {
                "description": "All the settings after the change, with `group_meta`.",
                "schema": SEARCH_SETTINGS_RESPONSE,
                "example": {"search_settings": REPLACED_SETTINGS, "group_meta": SAMPLE_GROUP_META},
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_search_settings",
        "slug": "check-search-settings",
        "title": "Check search settings",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the search settings, with no body.",
        "description": "Returns `200` with headers only and no body. The response has `Content-Length: 0` and no `ETag` header. Use it to check that the search settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0`. No `ETag` header and no body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_search_settings_section",
        "slug": "get-a-search-settings-section",
        "title": "Get a search settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one search settings section under its own key, such as `search_fields`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `search_settings`, and without `group_meta`. The section is the same as the one [Get search settings](" + GET_PAGE + ") returns for it. Add `field_metadata=true` to also get a description of each of the section's fields, keyed by field name. An unknown section returns `404`.",
        "parameters": [SECTION_READ, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key. With `field_metadata=true`, a `field_metadata` key is added beside it.",
                "schema": {"type": "object", "description": "Holds only the key of the section named in the path, and `field_metadata` when you ask for it.", "properties": dict(SECTION_PROPERTIES, field_metadata=dict(
                    ref("SearchSettingsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by field name.",
                ))},
                "example": {"search_fields": SAMPLE_SEARCH_FIELDS},
            },
            "404": {
                "description": "No section has that name. The message is `Unknown search_settings section: <section>`.",
                "schema": ERROR,
                "example": UNKNOWN_SECTION,
            },
        },
        "example_call": {"path": {"section": "search_fields"}},
    },
    {
        "key": "patch_search_settings_section",
        "slug": "update-a-search-settings-section",
        "title": "Update a search settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that whole section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `search_fields`. That is the only wrapper accepted: a body with no wrapper, or one wrapped in `search_settings`, is rejected with `400`. Only the fields you send change, at every level; the rest keep their stored values. Returns the whole section after the change, under its own key and without `group_meta`.",
        "parameters": [SECTION_WRITE],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path. No other wrapper is accepted.", "properties": SECTION_PROPERTIES},
            "example": {"search_fields": {"match_keywords_exactly": True}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": SECTION_RESPONSE, "example": {"search_fields": PATCHED_SEARCH_FIELDS}},
            "400": {"description": SECTION_WRITE_400, "schema": ERROR},
        },
        "example_call": {"path": {"section": "search_fields"}},
    },
    {
        "key": "put_search_settings_section",
        "slug": "replace-a-search-settings-section",
        "title": "Replace a search settings section",
        "method": "PUT",
        "path": BASE + "/{section}",
        "summary": "Replaces one section with the body you send. Fields you leave out are reset.",
        "description": "Replaces the section named in the path with the body you send, wrapped in the section's own name. Any field the body leaves out is reset to its default, so send the whole section: read it with [Get a search settings section](" + GET_SECTION_PAGE + "), change what you need, and send it all back. A body not wrapped in the section's own name is rejected with `400`. Returns the whole section after the change, under its own key and without `group_meta`.",
        "parameters": [SECTION_WRITE],
        "body": {
            "schema": {"type": "object", "description": "The whole section, wrapped in the section named in the path. Fields you leave out are reset to their defaults.", "properties": SECTION_PROPERTIES},
            "example": {"search_fields": PATCHED_SEARCH_FIELDS},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": SECTION_RESPONSE, "example": {"search_fields": PATCHED_SEARCH_FIELDS}},
            "400": {"description": SECTION_WRITE_400, "schema": ERROR},
        },
        "example_call": {"path": {"section": "search_fields"}},
    },
    {
        "key": "get_search_settings_reindex_status",
        "slug": "get-the-reindex-status",
        "title": "Get the reindex status",
        "method": "GET",
        "path": BASE + "/reindex_status",
        "summary": "Returns where the search reindex stands: its `state`, start and finish times, and any `error`.",
        "description": "Returns where the Elasticsearch reindex stands. The four fields `state`, `started_at`, `finished_at` and `error` sit at the top level of the response, not wrapped in any key, and there is no `group_meta`. A change to `synonyms` triggers this reindex. The path is read-only: an `OPTIONS` request on it returns `Allow: GET, HEAD, OPTIONS`.",
        "parameters": [{
            "name": "field_metadata",
            "in": "query",
            "description": "Accepted and ignored. With `field_metadata=true`, the response is the same four fields and gains no `field_metadata` key.",
            "schema": {"type": "boolean", "example": True},
        }],
        "responses": {
            "200": {
                "description": "The reindex status, not wrapped in any key.",
                "schema": ref("SearchReindexStatus"),
                "example": SAMPLE_REINDEX_STATUS,
            },
        },
        "example_call": {"path": {}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def content_group(description, owner, extra=None):
    properties = {"enabled": flag("Include this content type in search results. Defaults to `false`.")}
    properties.update(extra or {})
    properties["display_heading"] = {"type": "string", "maxLength": 50, "description": "The heading displayed for this content type. At most 50 characters: a longer heading is rejected with `400`."}
    properties["excluded"] = {"type": "array", "items": ref("SearchExcludedItem"), "description": "The items hidden from search results for this content type. A read returns each item as an `{id, name}` record, where `id` is " + owner + ". A write takes a list of those ids, or the same records. A value that is not a list, or an id that is not an integer, is rejected with `400`."}
    return {"type": "object", "description": description, "properties": properties}


SCHEMAS = {
    "SearchSettings": {"type": "object", "properties": {
        "searchable_content": ref("SearchableContent"),
        "search_fields": ref("SearchFields"),
        "synonyms": ref("Synonyms"),
    }},
    "SearchableContent": {"type": "object", "description": "The search box's placeholder text, and the content types the search covers.", "properties": {
        "placeholder_text": {"type": "string", "description": "The placeholder text in the search box."},
        "product": ref("SearchableContentGroup"),
        "product_categories": ref("SearchableProductCategories"),
        "blog": ref("SearchableContentGroup"),
        "other_pages": ref("SearchableContentGroup"),
    }},
    "SearchableContentGroup": content_group(
        "One content type the search covers: `product`, `blog` or `other_pages`.",
        "the product's `id` under `product`, the blog's `id` under `blog` and the page's `id` under `other_pages`",
    ),
    "SearchableProductCategories": content_group(
        "The `product_categories` content type. It has one field the other content types do not: `hide_parent_category`.",
        "the product category's `id`",
        {"hide_parent_category": flag("Hide the parent category in searched products. Defaults to `false`.")},
    ),
    "SearchExcludedItem": {"type": "object", "description": "One item hidden from search results.", "properties": {
        "id": {"type": "integer", "description": "The excluded item's `id`: the product's `id` under `product`, the product category's `id` under `product_categories`, the blog's `id` under `blog`, and the page's `id` under `other_pages`. A write can send these ids alone instead of records."},
        "name": {"type": "string", "description": "The excluded item's name."},
    }},
    "SearchFields": {"type": "object", "description": "How a query is matched, and which product fields it is matched against.", "properties": {
        "match_keywords_exactly": flag("Match keywords exactly. Defaults to `false`."),
        "match_full_sentences": flag("Match full sentences. Defaults to `false`."),
        "fields": {
            "type": "array",
            "items": ref("SearchFieldPriority"),
            "description": "The product fields a query is matched against, each with its priority. Each field and each priority may appear once, and `title` must be in the list at priority `1`. A list that breaks one of these rules is rejected with `400`.",
        },
    }},
    "SearchFieldPriority": {"type": "object", "description": "One product field and where it ranks.", "properties": {
        "field": {"type": "string", "enum": ["title", "category", "description", "tags", "sku", "brand"], "description": "The product field. Any other value is rejected with `400`."},
        "priority": {"type": "integer", "minimum": 1, "maximum": 10, "description": "Where the field ranks, from `1` to `10`. `title` must be `1`. A value outside `1` to `10` is rejected with `400`."},
    }},
    "Synonyms": {"type": "object", "description": "Groups of words that a search treats as synonyms of each other. Changing synonyms triggers an Elasticsearch reindex.", "properties": {
        "groups": {"type": "array", "items": ref("SynonymGroup"), "description": "The synonym groups."},
    }},
    "SynonymGroup": {"type": "object", "properties": {
        "keywords": {"type": "array", "minItems": 2, "items": {"type": "string"}, "description": "The words in the group. Each group needs at least two: a group with fewer is rejected with `400`."},
    }},
    "SearchSettingsGroupMeta": {"type": "object", "description": "One entry per section. Only [Get search settings](" + GET_PAGE + "), [Update search settings](" + PATCH_PAGE + ") and [Replace search settings](/api-reference/search-settings/replace-search-settings) return it.", "properties": {
        "searchable_content": ref("SearchSettingsSectionMeta"),
        "search_fields": ref("SearchSettingsSectionMeta"),
        "synonyms": ref("SearchSettingsSectionMeta"),
    }},
    "SearchSettingsSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for all three sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for all three sections."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/search_settings/search_fields`."},
    }},
    "SearchReindexStatus": {"type": "object", "description": "Where the Elasticsearch reindex stands.", "properties": {
        "state": {"type": "string", "description": "The reindex state, such as `idle` or `completed`."},
        "started_at": {"type": ["string", "null"], "format": "date-time", "description": "When the reindex started, or `null`."},
        "finished_at": {"type": ["string", "null"], "format": "date-time", "description": "When the reindex finished, or `null`."},
        "error": {"description": "The error the reindex reported, or `null`."},
    }},
    "SearchSettingsFieldMetadata": {"type": "object", "additionalProperties": True, "description": "Describes every field in the response and nothing else. It has the same nesting as the settings, with a `SearchSettingsFieldMetadataEntry` in place of each field. A list of rows, such as `search_fields.fields`, has one entry, and its `item` describes the fields of each row. On `/search_settings` it is keyed by section; on a section it is keyed by field name."},
    "SearchSettingsFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "description": "The kind of value the field takes: `boolean`, `string`, `integer`, `enum`, `id_list`, `string_list`, `object_list` or `group_list`."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "What the field holds, when the store gives a description."},
        "default": {"description": "The field's default value."},
        "max_length": {"type": "integer", "description": "The longest value accepted, for a `string` field. `50` for `display_heading`."},
        "allowed_values": {"type": "array", "items": {"type": "string"}, "description": "The values the field accepts, for an `enum` field."},
        "min": {"type": "integer", "description": "The lowest value, for an `integer` field."},
        "max": {"type": "integer", "description": "The highest value, for an `integer` field."},
        "item": {"type": "object", "additionalProperties": True, "description": "Describes each row's fields, for an `object_list` or `group_list` field."},
        "rules": {"type": "array", "items": {"type": "string"}, "description": "Rules the list must follow, such as `title required at priority 1` or `each group needs >= 2 keywords`."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request`, `not_found` or `method_not_allowed`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The path of the rejected field, such as `search_fields.fields`."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field`, `invalid_enum` or `duplicate`."},
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": {"type": "string", "description": "An identifier for this request."},
        }},
    }},
}

OVERVIEW_DESCRIPTION = "Read and change the content your store's search covers, the product fields it matches and its synonym groups, and check the reindex status."
INTRO = "The Search settings API has eight endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/search_settings`."
WARNING = (
    "**`PUT` replaces, so every field you leave out is reset to its default.** A `PUT`\n"
    "  of `search_fields` that sends only `match_keywords_exactly` returns `match_full_sentences` set to\n"
    "  `false` and `fields` cut to the single row `{\"field\": \"title\", \"priority\": 1}`. To change a few\n"
    "  fields, use `PATCH`. A `PUT` on `/search_settings` also resets or writes `synonyms`, and a change to\n"
    "  `synonyms` triggers an Elasticsearch reindex that cannot be undone."
)
NOTES = [
    "**The settings are split into three sections.** `searchable_content` sets the search box's\n"
    "  placeholder text and which content types the search covers: `product`, `product_categories`,\n"
    "  `blog` and `other_pages`, each with a list of items hidden from its results. `search_fields` sets\n"
    "  how a query is matched and which product fields it is matched against, by priority. `synonyms`\n"
    "  holds groups of words that a search treats as synonyms of each other. Read or write all three\n"
    "  through `/search_settings`, or one through `/search_settings/{section}`. Reading an unknown section\n"
    "  returns `404 not_found`.",
    "**`PATCH` changes only the fields you send, and `PUT` replaces.** `/search_settings` and each\n"
    "  section accept `GET`, `HEAD`, `PATCH` and `PUT`. A `PATCH` keeps the stored value of every field\n"
    "  you do not send, including other fields in the same nested block. `POST` and `DELETE` on\n"
    "  `/search_settings` are rejected with `405 method_not_allowed`, the message\n"
    "  `HTTP method not allowed for this endpoint.` and an `Allow: GET, HEAD, PATCH, PUT, OPTIONS` header.",
    "**Every write body is wrapped, and the key depends on the path.** On `/search_settings`, wrap the\n"
    "  fields in `search_settings` and then in the section name: a body with the section name at the top\n"
    "  level is rejected. On `/search_settings/{section}`, wrap them in the section's own name only, such as\n"
    "  `search_fields`: a body with no wrapper, or one wrapped in `search_settings`, is rejected. Both\n"
    "  return `400 invalid_request` and the message `request body must be wrapped in a '<name>' object`,\n"
    "  where `<name>` is the key the path expects.",
    "**An `excluded` list takes ids or records.** A read returns each excluded item as a record such as\n"
    "  `{\"id\": 4, \"name\": \"Gift Card\"}`. Its `id` is the product's `id` under `product`, the product\n"
    "  category's `id` under `product_categories`, the blog's `id` under `blog`, and the page's `id` under\n"
    "  `other_pages`. A write accepts a list of those ids or the same records, and both read back as\n"
    "  records. So you can `PUT` a `searchable_content` section exactly as you read it.",
    "**`search_fields.fields` has three rules.** Each `field` may appear once, each `priority` may appear\n"
    "  once, and `title` must be in the list at priority `1`. `field` is one of `title`, `category`,\n"
    "  `description`, `tags`, `sku` or `brand`, and `priority` is from `1` to `10`. A list that breaks a\n"
    "  rule is rejected with `400`. Add `field_metadata=true` to a read to get these rules and every other\n"
    "  field's limits, such as the 50-character `display_heading`.",
]
