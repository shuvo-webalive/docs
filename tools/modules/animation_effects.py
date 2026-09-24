"""The Animation effects settings endpoints, as recorded against a live store in the SDKs' ENDPOINTS.md."""

import copy

TAG = "Animation effects"
SLUG = "animation-effects"
BASE = "/admin/settings/animation_effects"
ICON = "wand-magic-sparkles"

SECTIONS = ["preloader_design", "widget_transition", "page_transition", "image_lazy_effect", "page_skeleton"]

GET_PAGE = "/api-reference/animation-effects/get-animation-effects-settings"

OVERVIEW_DESCRIPTION = "Read and change your store's page preloader, widget and page transitions, image lazy loading and checkout page skeleton."
INTRO = "The Animation effects API has five endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/settings/animation_effects`."

WARNING = (
    "Every write body must be wrapped in a key, and the key depends on the path. On `/animation_effects`,\n"
    "  wrap the fields in `animation_effects` and then in the section name. On `/animation_effects/{section}`,\n"
    "  wrap them in the section's own name only, such as `widget_transition`. A body without the right\n"
    "  wrapper is rejected with `400 invalid_request`: the message is `animation_effects wrapper required`\n"
    "  on the first path and `request body must be wrapped in a '<section>' object` on the second."
)

NOTES = [
    "**The settings are split into five sections.** `preloader_design` controls the loader shown while a\n"
    "  page loads, and when and where it shows. `widget_transition` controls whether widgets fade in, and\n"
    "  for how long. `page_transition` controls the animation between pages and when it plays. `image_lazy_effect` controls\n"
    "  which pages lazy-load images, and the loader and placeholder they show. `page_skeleton` has one\n"
    "  field, `checkout_page_skeleton`. Read or write all five through `/animation_effects`, or one through\n"
    "  `/animation_effects/{section}`. An unknown section returns `404 not_found`.",
    "**`PATCH` is the only way to write, and it changes only the fields you send.** Fields you leave out\n"
    "  keep their stored values, and so does every section you leave out. One body sent to\n"
    "  `/animation_effects` can change several sections at once. Sending the settings back exactly as a\n"
    "  read returned them also returns `200`. `PUT`, `POST` and `DELETE` are rejected on\n"
    "  `/animation_effects` and on each of the five section paths with `405 method_not_allowed` and an\n"
    "  `Allow: GET, HEAD, PATCH, OPTIONS` header.",
    "**Add `field_metadata=true` to a read to get the rules for every field except `custom_loader`.** The\n"
    "  settings are still returned with it. Each entry gives the field's `type` and `ui_label`, and every\n"
    "  field except `preloader_custom_page` and `content_image_lazy_load_background` gives a `default`.\n"
    "  Every `enum` field lists its `allowed_values`, every `integer` and `decimal` field gives its `min`\n"
    "  and `max`, and `preloader_hide_after_time` and `preloader_custom_page` name the field they depend on\n"
    "  in `depends_on`. A write that sends a value outside `allowed_values`, or outside `min` and `max`, is\n"
    "  rejected with `400 invalid_request`. On `/animation_effects` the block is keyed by section; on a\n"
    "  section it is keyed by field name.",
    "**Two `preloader_design` fields differ between a read and a write.** A read returns each page in\n"
    "  `preloader_custom_page` as the page's `id` and `name`, such as `{\"id\": 70, \"name\": \"Category\"}`. A\n"
    "  write takes the pages' ids, such as `[70, 1]`, and also accepts the records a read returns. An empty list\n"
    "  while `preloader_page` is `custom`, or a page `id` that matches no page, is rejected with\n"
    "  `400 invalid_request`. `custom_loader` is in every read but cannot be written: a body that names only\n"
    "  `custom_loader` is rejected with `400 invalid_request` and the message\n"
    "  `no recognized animation_effects fields in body`.",
    "**Animation effects writes have their own rate limit.** If you send eleven writes with no pause,\n"
    "  within about 0.8 seconds, the eleventh is rejected with `429` and a `Retry-After` header that counts\n"
    "  down the time left before writes are accepted again. It is separate from the page settings limit:\n"
    "  after you use it up, a shopping cart settings write still succeeds, and the reverse. Reads showed\n"
    "  no limit: forty reads within about 1.2 seconds were all accepted. A retry before `Retry-After`\n"
    "  has passed counts as another write, so wait until then before you write again.",
]

SECTION = {
    "name": "section",
    "in": "path",
    "required": True,
    "description": "The section to read or write: `preloader_design`, `widget_transition`, `page_transition`, `image_lazy_effect` or `page_skeleton`.",
    "schema": {"type": "string", "enum": SECTIONS, "example": "widget_transition"},
}

FIELD_METADATA_BY_SECTION = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes every field in all five sections except `custom_loader`, keyed by section. The settings and `group_meta` are still returned.",
    "schema": {"type": "boolean", "example": True},
}

FIELD_METADATA_BY_FIELD = {
    "name": "field_metadata",
    "in": "query",
    "description": "Send `true` to also get `field_metadata`, which describes each of the section's fields except `custom_loader`, keyed by field name. The section's settings are still returned.",
    "schema": {"type": "boolean", "example": True},
}

SAMPLE_PRELOADER_DESIGN = {
    "enable_preloader": True,
    "enable_custom_preloader": False,
    "preloader_preset": "spinning_dots",
    "preloader_size": 30,
    "preloader_background_opacity": 0.5,
    "background_preloader": "#ffffff",
    "preloader_hide_condition": "auto",
    "preloader_show_time_condition": "on_every_load",
    "preloader_hide_after_time": 0.5,
    "preloader_page": "custom",
    "preloader_custom_page": [{"id": 70, "name": "Category"}, {"id": 1, "name": "Home-default"}],
    "custom_loader": {"enabled": False, "file_name": None, "file_url": None},
}

SAMPLE_WIDGET_TRANSITION = {"widget_smooth_render": False, "widget_smooth_render_duration": 1000}

SAMPLE_PAGE_TRANSITION = {
    "page_transition_animation_type": "none",
    "transition_animation_duration": 0.8,
    "animation_before_entering_new_page": False,
    "animation_after_entering_new_page": False,
}

SAMPLE_IMAGE_LAZY_EFFECT = {
    "preloader_image_lazy_effect_preset": "none",
    "product_details_page_image_lazy_effect": False,
    "flying_cart_image_lazy_effect": False,
    "product_list_image_lazy_effect": False,
    "property_list_image_lazy_effect": False,
    "property_details_page_image_lazy_effect": False,
    "blog_list_image_lazy_effect": False,
    "blog_details_page_image_lazy_effect": False,
    "lazy_loader_size": 30,
    "background_lazy_loader": "#ffffff",
    "content_image_lazy_load_background": "rgb(223 223 223) linear-gradient(180deg, rgb(128 141 151 / 0%), rgb(22 44 60 / 30%))",
}

SAMPLE_PAGE_SKELETON = {"checkout_page_skeleton": False}

SAMPLE_GROUP_META = {
    section: {"kind": "setting", "writable": True, "href": "/api/v4" + BASE + "/" + section}
    for section in SECTIONS
}

SAMPLE_ANIMATION_EFFECTS = {
    "animation_effects": {
        "preloader_design": SAMPLE_PRELOADER_DESIGN,
        "widget_transition": SAMPLE_WIDGET_TRANSITION,
        "page_transition": SAMPLE_PAGE_TRANSITION,
        "image_lazy_effect": SAMPLE_IMAGE_LAZY_EFFECT,
        "page_skeleton": SAMPLE_PAGE_SKELETON,
    },
    "group_meta": SAMPLE_GROUP_META,
}

PATCHED_ANIMATION_EFFECTS = copy.deepcopy(SAMPLE_ANIMATION_EFFECTS)
PATCHED_ANIMATION_EFFECTS["animation_effects"]["page_transition"]["animation_before_entering_new_page"] = True
PATCHED_ANIMATION_EFFECTS["animation_effects"]["image_lazy_effect"]["blog_list_image_lazy_effect"] = True

PATCHED_WIDGET_TRANSITION = dict(SAMPLE_WIDGET_TRANSITION, widget_smooth_render=True)


def error_example(code, message, details, request_id):
    return {"error": {"code": code, "message": message, "details": details, "request_id": request_id}}


def ref(name):
    return {"$ref": "#/components/schemas/" + name}


ERROR = ref("Error")

RATE_LIMITED = {"description": "Too many writes in a short time. The `Retry-After` header says how long until you can write again."}

ANIMATION_EFFECTS_RESPONSE = {"type": "object", "properties": {
    "animation_effects": ref("AnimationEffectsSettings"),
    "group_meta": ref("AnimationEffectsGroupMeta"),
}}

SECTION_RECORDS = {
    "preloader_design": ref("PreloaderDesign"),
    "widget_transition": ref("WidgetTransition"),
    "page_transition": ref("PageTransition"),
    "image_lazy_effect": ref("ImageLazyEffect"),
    "page_skeleton": ref("PageSkeleton"),
}

SECTION_INPUTS = dict(SECTION_RECORDS, preloader_design=ref("PreloaderDesignInput"))

ENDPOINTS = [
    {
        "key": "get_animation_effects",
        "slug": "get-animation-effects-settings",
        "title": "Get animation effects settings",
        "method": "GET",
        "path": BASE,
        "summary": "Returns all five settings sections and a `group_meta` block describing each one.",
        "description": "Returns every animation effects setting under `animation_effects`, with all five sections in full. Beside it, `group_meta` gives each section's `kind`, whether it is `writable`, and the `href` of its own path. Add `field_metadata=true` to also get the rules for every field except `custom_loader`, keyed by section.",
        "parameters": [FIELD_METADATA_BY_SECTION],
        "responses": {
            "200": {
                "description": "All five sections and `group_meta`.",
                "schema": {"type": "object", "properties": dict(ANIMATION_EFFECTS_RESPONSE["properties"], field_metadata=dict(
                    ref("AnimationEffectsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by section.",
                ))},
                "example": SAMPLE_ANIMATION_EFFECTS,
            },
        },
        "example_call": {"path": {}},
    },
    {
        "key": "patch_animation_effects",
        "slug": "update-animation-effects-settings",
        "title": "Update animation effects settings",
        "method": "PATCH",
        "path": BASE,
        "summary": "Changes the fields you send in one or more sections and returns all settings.",
        "description": "Send the fields to change inside `animation_effects`, grouped by section name. One body can change several sections at once. Only the fields you send change: other fields, and every section you leave out, keep their stored values. Returns all the settings after the change, with `group_meta`, as [Get animation effects settings](" + GET_PAGE + ") does.",
        "body": {
            "schema": {"type": "object", "required": ["animation_effects"], "properties": {
                "animation_effects": dict(ref("AnimationEffectsInput"), description="The fields to change, grouped by section. Send only the fields that change."),
            }},
            "example": {"animation_effects": {
                "page_transition": {"animation_before_entering_new_page": True},
                "image_lazy_effect": {"blog_list_image_lazy_effect": True},
            }},
        },
        "responses": {
            "200": {"description": "All the settings after the change, with `group_meta`.", "schema": ANIMATION_EFFECTS_RESPONSE, "example": PATCHED_ANIMATION_EFFECTS},
            "400": {
                "description": "The body is not wrapped in `animation_effects` (`animation_effects wrapper required`), has another key beside it (`unknown top-level field(s): <name>`), names a section or field that does not exist (`unknown_field`), sends a value the field does not accept (`invalid_boolean`, `invalid_enum` or `out_of_range`), or is not valid JSON (`Request body is not valid JSON`). The reason for each rejected field is in `details[].code`. For a rejected value, `details[].field` gives the section and the field, such as `page_transition.page_transition_animation_type`.",
                "schema": ERROR,
                "example": error_example("invalid_request", "page_transition.page_transition_animation_type: must be one of [none, fade_in_out, slide_in_out, zoom_in_out, flip]",
                                         [{"field": "page_transition.page_transition_animation_type", "code": "invalid_enum", "message": "must be one of [none, fade_in_out, slide_in_out, zoom_in_out, flip]", "value": "wobble"}],
                                         "3d8f1a6c-2b7e-4c91-9f4a-6e0d2c5b8a17"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {}},
    },
    {
        "key": "head_animation_effects",
        "slug": "get-animation-effects-settings-headers",
        "title": "Get animation effects settings headers",
        "method": "HEAD",
        "path": BASE,
        "summary": "Returns the headers for the animation effects settings, with no body.",
        "description": "Returns `200` with headers only and no body. The headers include `Content-Length: 0` and an `ETag`. Use it to check that the settings are reachable without downloading them.",
        "responses": {
            "200": {"description": "Headers only, including `Content-Length: 0` and an `ETag`. No body."},
        },
        "example_call": {"path": {}},
    },
    {
        "key": "get_animation_effects_section",
        "slug": "get-a-settings-section",
        "title": "Get a settings section",
        "method": "GET",
        "path": BASE + "/{section}",
        "summary": "Returns one settings section under its own key, such as `widget_transition`.",
        "description": "Returns one section, wrapped in the section's own name rather than in `animation_effects`, and without `group_meta`. Its values are the same as that section's in [Get animation effects settings](" + GET_PAGE + "). Add `field_metadata=true` to also get the rules for each of the section's fields except `custom_loader`, keyed by field name. An unknown section returns `404 not_found`.",
        "parameters": [SECTION, FIELD_METADATA_BY_FIELD],
        "responses": {
            "200": {
                "description": "The section under its own key.",
                "schema": {"type": "object", "description": "Holds only the key of the section you asked for, and `field_metadata` when you ask for it.", "properties": dict(SECTION_RECORDS, field_metadata=dict(
                    ref("AnimationEffectsFieldMetadata"),
                    description="Only when you send `field_metadata=true`. Keyed by field name.",
                ))},
                "example": {"widget_transition": SAMPLE_WIDGET_TRANSITION},
            },
            "404": {
                "description": "No section has that name. The message is `Unknown animation_effects section: <name>`.",
                "schema": ERROR,
                "example": error_example("not_found", "Unknown animation_effects section: bogus", [],
                                         "8a2c4e6f-1d3b-4f5a-9c7e-0b2d4f6a8c13"),
            },
        },
        "example_call": {"path": {"section": "widget_transition"}},
    },
    {
        "key": "patch_animation_effects_section",
        "slug": "update-a-settings-section",
        "title": "Update a settings section",
        "method": "PATCH",
        "path": BASE + "/{section}",
        "summary": "Changes the fields you send in one section and returns that section.",
        "description": "Send the fields to change, wrapped in the section's own name, such as `widget_transition`. A body wrapped in `animation_effects`, or not wrapped at all, is rejected with `400 invalid_request`. Only the fields you send change, and you get back the whole section under the same key, without `group_meta`. After a `400` on a section path, the next write on the same client to a different section is also rejected with `400`, and the message names the previous section.",
        "parameters": [SECTION],
        "body": {
            "schema": {"type": "object", "description": "Wrap the fields in the section named in the path. No other wrapper is accepted.", "properties": SECTION_INPUTS},
            "example": {"widget_transition": {"widget_smooth_render": True}},
        },
        "responses": {
            "200": {"description": "The whole section after the change, under its own key.", "schema": {"type": "object", "properties": SECTION_RECORDS},
                    "example": {"widget_transition": PATCHED_WIDGET_TRANSITION}},
            "400": {
                "description": "The body is not wrapped in the section's own name (`request body must be wrapped in a '<section>' object`), or sends a value the field does not accept, such as a number outside the field's `min` and `max` (`out_of_range`). For a rejected value, `details[].field` gives the section and the field, such as `widget_transition.widget_smooth_render_duration`. After a `400`, the next write on the same client to a different section is checked against the previous section's name, so it is rejected with `request body must be wrapped in a '<previous section>' object`. Send that write from a new client and it is checked correctly.",
                "schema": ERROR,
                "example": error_example("invalid_request", "widget_transition.widget_smooth_render_duration: must be between 0 and 1000",
                                         [{"field": "widget_transition.widget_smooth_render_duration", "code": "out_of_range", "message": "must be between 0 and 1000", "value": -1}],
                                         "5b7d9f1a-3c5e-4a7b-8d9f-2e4a6c8b0d35"),
            },
            "429": RATE_LIMITED,
        },
        "example_call": {"path": {"section": "widget_transition"}},
    },
]


def flag(description):
    return {"type": "boolean", "description": description}


def whole(description, minimum, maximum):
    return {"type": "integer", "minimum": minimum, "maximum": maximum, "description": description}


def decimal(description, minimum, maximum):
    return {"type": "number", "minimum": minimum, "maximum": maximum, "description": description}


def choice(values, description):
    return {"type": "string", "enum": values, "description": description}


def text(description):
    return {"type": "string", "description": description}


LOADER_PRESETS = [
    "none", "pulse_circle", "tube_spinner", "spinning_dots", "ripples", "infinite_spinner",
    "gears_spinner", "gear_spinner", "bouncing_squares", "bouncing_circles", "bouncing_ball",
]

PRELOADER_DESIGN_FIELDS = {
    "enable_preloader": flag("Show the preloader while a page loads."),
    "enable_custom_preloader": flag("Show your own uploaded loader instead of the preset in `preloader_preset`."),
    "preloader_preset": choice(LOADER_PRESETS, "The preset loader. `field_metadata` gives a label for each value under `options`, such as `Flying dots` for `pulse_circle`."),
    "preloader_size": whole("The loader's size in pixels, from `20` to `300`.", 20, 300),
    "preloader_background_opacity": decimal("The preloader's background opacity, from `0` to `1`.", 0, 1),
    "background_preloader": text("The preloader's background colour, as a hex or CSS colour, such as `#ffffff`."),
    "preloader_hide_condition": choice(["auto", "x_seconds"], "When the preloader hides: `auto`, or `x_seconds` to hide it after `preloader_hide_after_time` seconds."),
    "preloader_show_time_condition": choice(["on_every_load", "once_per_user_session_all", "once_per_user_session_per_single_page"],
                                            "When the preloader shows: `on_every_load`, `once_per_user_session_all` or `once_per_user_session_per_single_page`."),
    "preloader_hide_after_time": decimal("Seconds before the preloader hides, from `0.2` to `5`. Used when `preloader_hide_condition` is `x_seconds`.", 0.2, 5),
    "preloader_page": choice(["all", "custom"], "Which pages show the preloader: `all`, or `custom` for only the pages in `preloader_custom_page`."),
}

SCHEMAS = {
    "AnimationEffectsSettings": {"type": "object", "properties": SECTION_RECORDS},
    "AnimationEffectsInput": {"type": "object", "description": "Name only the sections and fields that change.", "properties": SECTION_INPUTS},
    "PreloaderDesign": {"type": "object", "description": "The loader shown while a page loads, and when and where it shows.", "properties": dict(
        PRELOADER_DESIGN_FIELDS,
        preloader_custom_page={"type": "array", "items": ref("PreloaderPage"), "description": "The pages that show the preloader when `preloader_page` is `custom`, each as the page's `id` and `name`. A write takes each page's `id`, and also accepts these records."},
        custom_loader=dict(ref("CustomLoader"), description="The uploaded loader file. Read-only."),
    )},
    "PreloaderDesignInput": {"type": "object", "description": "The `preloader_design` fields a write accepts. `custom_loader` is not one of them.", "properties": dict(
        PRELOADER_DESIGN_FIELDS,
        preloader_custom_page={
            "type": "array",
            "items": {"anyOf": [{"type": "integer", "description": "A page's `id`."}, ref("PreloaderPage")]},
            "description": "The ids of the pages that show the preloader, such as `[70, 1]`. A write also accepts the records a read returns, with each page's `id` and `name`. The list cannot be empty while `preloader_page` is `custom`, and a page `id` that matches no page is rejected with `400 invalid_request`. `field_metadata` lists the pages you can choose under `options`.",
        },
    )},
    "PreloaderPage": {"type": "object", "description": "One page that shows the preloader.", "properties": {
        "id": {"type": "integer", "description": "The page's `id`. A write sends this value in `preloader_custom_page`."},
        "name": {"type": "string", "description": "The page's name."},
    }},
    "CustomLoader": {"type": "object", "description": "The loader file uploaded for `enable_custom_preloader`. Read-only: `field_metadata` has no entry for it, and a write body that names only `custom_loader` is rejected with `400 invalid_request`.", "properties": {
        "enabled": {"type": "boolean", "description": "`true` when a loader file has been uploaded."},
        "file_name": {"type": ["string", "null"], "description": "The uploaded file's name, or `null` when there is none."},
        "file_url": {"type": ["string", "null"], "description": "The uploaded file's URL, or `null` when there is none."},
    }},
    "WidgetTransition": {"type": "object", "description": "Whether widgets fade in, and for how long.", "properties": {
        "widget_smooth_render": flag("Fade widgets in."),
        "widget_smooth_render_duration": whole("How long the fade takes, in milliseconds, from `0` to `1000`.", 0, 1000),
    }},
    "PageTransition": {"type": "object", "description": "The animation between pages, and when it plays.", "properties": {
        "page_transition_animation_type": choice(["none", "fade_in_out", "slide_in_out", "zoom_in_out", "flip"],
                                                 "The animation between pages: `none`, `fade_in_out`, `slide_in_out`, `zoom_in_out` or `flip`."),
        "transition_animation_duration": decimal("How long the animation takes, in seconds, from `0.3` to `5`.", 0.3, 5),
        "animation_before_entering_new_page": flag("Play the animation before entering a new page."),
        "animation_after_entering_new_page": flag("Play the animation after entering a new page."),
    }},
    "ImageLazyEffect": {"type": "object", "description": "Which pages lazy-load images, and the loader and placeholder they show.", "properties": {
        "preloader_image_lazy_effect_preset": choice(LOADER_PRESETS, "The preset lazy loader. It takes the same values as `preloader_design.preloader_preset`."),
        "product_details_page_image_lazy_effect": flag("Lazy-load images on the product details page."),
        "flying_cart_image_lazy_effect": flag("Lazy-load images in the flying cart popup."),
        "product_list_image_lazy_effect": flag("Lazy-load images on product list pages."),
        "property_list_image_lazy_effect": flag("Lazy-load images on property list pages."),
        "property_details_page_image_lazy_effect": flag("Lazy-load images on the property details page."),
        "blog_list_image_lazy_effect": flag("Lazy-load images on blog list pages."),
        "blog_details_page_image_lazy_effect": flag("Lazy-load images on the blog details page."),
        "lazy_loader_size": whole("The lazy loader's size in pixels, from `20` to `300`.", 20, 300),
        "background_lazy_loader": text("The lazy loader's background colour, as a hex or CSS colour, such as `#ffffff`."),
        "content_image_lazy_load_background": text("The CSS background of the image placeholder."),
    }},
    "PageSkeleton": {"type": "object", "description": "The checkout page skeleton setting. It is the section's only field.", "properties": {
        "checkout_page_skeleton": flag("Turn on the checkout page skeleton. A value that is not a boolean is rejected with `400 invalid_request`."),
    }},
    "AnimationEffectsGroupMeta": {"type": "object", "description": "One entry per section. Only [Get animation effects settings](" + GET_PAGE + ") and [Update animation effects settings](/api-reference/animation-effects/update-animation-effects-settings) return it.", "properties": {
        section: ref("AnimationEffectsSectionMeta") for section in SECTIONS
    }},
    "AnimationEffectsSectionMeta": {"type": "object", "properties": {
        "kind": {"type": "string", "description": "What the section is. `setting` for all five sections."},
        "writable": {"type": "boolean", "description": "Whether you can write to the section. `true` for all five sections."},
        "href": {"type": "string", "description": "The section's own path, such as `/api/v4/admin/settings/animation_effects/preloader_design`."},
    }},
    "AnimationEffectsFieldMetadata": {
        "type": "object",
        "description": "On [Get animation effects settings](" + GET_PAGE + ") it is keyed by section and then by field name. On a section it is keyed by field name. `custom_loader` has no entry.",
        "additionalProperties": {"anyOf": [
            ref("AnimationEffectsFieldMetadataEntry"),
            {"type": "object", "description": "One section's fields, keyed by field name.", "additionalProperties": ref("AnimationEffectsFieldMetadataEntry")},
        ]},
    },
    "AnimationEffectsFieldMetadataEntry": {"type": "object", "properties": {
        "type": {"type": "string", "enum": ["boolean", "integer", "decimal", "enum", "color", "text", "id_list"], "description": "The kind of value the field takes."},
        "ui_label": {"type": "string", "description": "The field's label."},
        "description": {"type": "string", "description": "More about the value the field takes, on some fields, such as `Hex or CSS color.`"},
        "default": {"description": "The field's default value. `preloader_custom_page` and `content_image_lazy_load_background` have none."},
        "allowed_values": {"type": "array", "items": {"type": "string"}, "description": "The values the field accepts, for an `enum` field."},
        "options": {"type": "array", "items": {"type": "object"}, "description": "For `preloader_preset` and `preloader_image_lazy_effect_preset`, a `value` and a `label` for each allowed value. For `preloader_custom_page`, each page you can choose, as the page's `id` and `name`."},
        "min": {"type": "number", "description": "The lowest value, for an `integer` or `decimal` field."},
        "max": {"type": "number", "description": "The highest value, for an `integer` or `decimal` field."},
        "depends_on": {"type": "string", "description": "The field this one depends on: `preloader_hide_condition` for `preloader_hide_after_time`, and `preloader_page` for `preloader_custom_page`."},
        "references": {"type": "string", "description": "The kind of record an `id_list` field points to: `page` for `preloader_custom_page`, which holds page ids."},
    }},
    "Error": {"type": "object", "properties": {
        "error": {"type": "object", "properties": {
            "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `not_found`."},
            "message": {"type": "string"},
            "details": {"type": "array", "description": "One entry per rejected field. Empty when the error is not about a field.", "items": {"type": "object", "properties": {
                "field": {"type": "string", "description": "The field that was rejected."},
                "code": {"type": "string", "description": "Why it was rejected, such as `unknown_field` or `invalid_enum`."},
                "message": {"type": "string"},
                "value": {"description": "The value you sent, when the API includes it."},
            }}},
            "request_id": {"type": "string", "description": "An id for this request."},
        }},
    }},
}
