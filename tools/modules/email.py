"""The Email endpoint, as recorded against a live store in the SDKs' ENDPOINTS.md."""

TAG = "Email"
SLUG = "email"
BASE = "/admin/email/send"
ICON = "envelope"

OVERVIEW_DESCRIPTION = "Send an email from your store to up to 100 addresses, with your own HTML or text, or from a plugin's template."
INTRO = "The Email API has one endpoint, and you can call it from all seven SDKs. Its path is `/api/v4/admin/email/send`."

WARNING = (
    "**Each sender can send to 500 addresses a day.** Every address in `recipients`, `cc` and `bcc`\n"
    "  counts. Past the limit, a valid send is rejected with `429` and the code `rate_limited` until\n"
    "  00:00 UTC, and the `Retry-After` header gives the seconds left. The SDKs' automatic retries do not\n"
    "  wait that long, so the call still fails. A send rejected with `400` does not count toward the limit,\n"
    "  and an invalid body still gets `400` after the limit is reached."
)

NOTES = [
    "**Send the fields at the top level of the body, in camelCase.** Write `htmlContent` and\n"
    "  `contentType`, not `html_content` or `content_type`. The store ignores any field it does not know,\n"
    "  snake_case spellings included, without an error. A body wrapped in `email` is rejected with `400`,\n"
    "  with `recipients` and `htmlContent` reported as `required`.",
    "**Send your own content or a plugin's template, not both.** For your own content, send\n"
    "  `htmlContent`. You can add `contentType`: `html`, `text` or `text/html`. For a template, send its\n"
    "  `identifier`, its variables in `data`, and the `plugin_uuid` header. A body with both\n"
    "  `htmlContent` and `identifier` is rejected with `400` and the code `conflicting_value`.",
    "**The `plugin_uuid` header switches the call to plugin authentication.** With an installed\n"
    "  plugin's uuid in the header, the store authenticates the call as that plugin, so an admin access\n"
    "  token gets `401`, even on an `htmlContent` send. A template send needs the plugin's own access\n"
    "  token. Leave the header out when you send your own content. A `plugin_uuid` field in the body is\n"
    "  ignored: only the header counts.",
    "**One call sends to at most 100 addresses.** `recipients`, `cc` and `bcc` together hold at most\n"
    "  100 addresses; more is rejected with `400` and the code `too_many`. Each invalid address is\n"
    "  named in `details`, such as `recipients[1]` or `cc[0]`, with the code `invalid_email`.",
    "**`POST` is the only method, and the store keeps no copy of the email.** `GET`, `HEAD`, `PUT`,\n"
    "  `PATCH` and `DELETE` are rejected with `405` and the header `Allow: POST, OPTIONS`. There is\n"
    "  nothing to read back or delete after a send.",
]

PLUGIN_UUID = {
    "name": "plugin_uuid",
    "in": "header",
    "required": False,
    "description": "Only for a template send: the uuid of the installed plugin that owns the template in `identifier`. Send the header name exactly as `plugin_uuid`, with an underscore. With this header the store authenticates the call as the plugin, so an admin access token gets `401`, even on an `htmlContent` send. A uuid no plugin has is rejected with `400` and the message `Plugin not found`. A `plugin_uuid` field in the body is ignored.",
    "schema": {"type": "string", "example": "3f2b8c1e-5a4d-4e7b-9c6f-1d2e3a4b5c6d"},
}

ERROR_REF = {"$ref": "#/components/schemas/EmailError"}
RESULT_REF = {"$ref": "#/components/schemas/EmailSendResult"}

SEND_BODY = {
    "recipients": ["customer@example.com"],
    "cc": ["orders@example.com"],
    "subject": "Your order has shipped",
    "htmlContent": "<p>Your order is on its way.</p>",
    "contentType": "text/html",
}

SENT = {
    "status": "success",
    "accepted": ["customer@example.com"],
    "rejected": [],
    "cc": ["orders@example.com"],
    "bcc": [],
}

VALIDATION_400 = (
    "The body is not valid, and nothing is sent. `error.code` is `invalid_request`, and `details` names each problem in `field`, with the reason in `code`: "
    "`recipients`, `subject` or `htmlContent` is missing (`required`); an address is not a valid email (`invalid_email`, with `field` such as `recipients[1]`, `cc[0]` or `bcc[0]`); "
    "`recipients`, `cc` and `bcc` hold more than 100 addresses together (`too_many`, on `recipients`); "
    "`contentType` is not `html`, `text` or `text/html` (`invalid_value`); "
    "`cc` is not a list, an address is not a string, or `data` is not an object (`invalid_type`); "
    "`htmlContent` and `identifier` are both sent (`conflicting_value`, on `identifier`); "
    "or `identifier` is sent without the `plugin_uuid` header (`required`, on `plugin_uuid`, message `plugin_uuid header is required to send by identifier`). "
    "A missing `subject` is reported only when the body has `htmlContent` or `identifier`. "
    "An empty body `{}` returns the message `request body is empty`, and a `plugin_uuid` header no plugin has returns `Plugin not found`."
)

ENDPOINTS = [
    {
        "key": "send_email",
        "slug": "send-an-email",
        "title": "Send an email",
        "method": "POST",
        "path": BASE,
        "summary": "Sends an email to up to 100 addresses and returns the accepted and rejected addresses.",
        "description": "Send `recipients` and `subject` at the top level of the body, with either `htmlContent` or a plugin template's `identifier` and `data`. The call returns `200` once every message is sent, with the recipients in `accepted` and the copied addresses in `cc` and `bcc`. An address you send twice, in any letter case, gets one email. Each sender can send to 500 addresses a day; past that, the call is rejected with `429` until 00:00 UTC.",
        "parameters": [PLUGIN_UUID],
        "body": {"schema": {"$ref": "#/components/schemas/EmailInput"}, "example": SEND_BODY},
        "responses": {
            "200": {
                "description": "Every message was sent. `status` is `success`, `accepted` lists the recipients, `cc` and `bcc` list the copied addresses, and `rejected` is empty. Spaces around each address are trimmed, and an address you sent twice, in any letter case, appears once, in the form you sent first.",
                "schema": RESULT_REF,
                "example": SENT,
            },
            "400": {"description": VALIDATION_400, "schema": ERROR_REF},
            "401": {"description": "You sent the `plugin_uuid` header of an installed plugin with an admin access token. The header makes the store authenticate the call as that plugin, so the admin token is rejected, even on an `htmlContent` send. Leave the header out, or send the plugin's own access token.", "schema": ERROR_REF},
            "413": {"description": "The body is larger than 1048576 bytes. `error.code` is `invalid_request` and the message is `The request body is larger than 1048576 bytes.`", "schema": ERROR_REF},
            "429": {"description": "This sender has reached its limit of 500 addresses for the day. `error.code` is `rate_limited`, the message is `The daily email limit of 500 addresses is reached; try again after 00:00 UTC.`, and `details[0]` has `field` `recipients` and `code` `daily_limit_reached`. The `Retry-After` header gives the seconds until 00:00 UTC. Send again after that time.", "schema": ERROR_REF},
            "502": {"description": "The mail server failed the send. `status` is `failed`, `accepted` is empty, and `rejected` lists each address as an object with `email` and `reason` `send_failed`.", "schema": RESULT_REF},
        },
        "example_call": {"body": SEND_BODY},
    },
]

ADDRESS_LIST = {"type": "array", "items": {"type": "string", "format": "email"}}

SCHEMAS = {
    "EmailInput": {"type": "object", "required": ["recipients", "subject"], "description": "Send these fields at the top level of the body, in camelCase as shown. Send `htmlContent` or `identifier`, not both. The store ignores any other field, snake_case spellings such as `html_content` and a `plugin_uuid` field included.", "properties": {
        "recipients": dict(ADDRESS_LIST, description="Required. The addresses to send to. `recipients`, `cc` and `bcc` together hold at most 100 addresses. Spaces around an address are trimmed, and an address you list twice, in any letter case, is sent once."),
        "cc": dict(ADDRESS_LIST, description="Addresses to copy. They count toward the 100-address limit of a call and the 500-address daily limit. A value that is not a list is rejected with `400`."),
        "bcc": dict(ADDRESS_LIST, description="Addresses to blind-copy. They count toward the 100-address limit of a call and the 500-address daily limit."),
        "subject": {"type": "string", "description": "Required. The email's subject line."},
        "htmlContent": {"type": "string", "description": "The email's content: HTML, or plain text when `contentType` is `text`. Required unless you send `identifier`. Sending both is rejected with `400`. The whole body must stay within 1048576 bytes."},
        "contentType": {"type": "string", "enum": ["html", "text", "text/html"], "description": "How the store reads `htmlContent`: `html`, `text` or `text/html`. Any other value is rejected with `400`."},
        "identifier": {"type": "string", "description": "The identifier of a plugin's email template, such as `order-shipped`. Send it with `data` and the `plugin_uuid` header, and leave out `htmlContent`."},
        "data": {"type": "object", "description": "The template's variables, as an object of any shape, such as `{\"order_no\": \"1001\"}`. A value that is not an object is rejected with `400`."},
    }},
    "EmailSendResult": {"type": "object", "description": "The result of a send. Each list holds the addresses trimmed, and an address you sent twice, in any letter case, once.", "properties": {
        "status": {"type": "string", "enum": ["success", "failed"], "description": "`success` when every message was sent (`200`), or `failed` when the mail server failed the send (`502`)."},
        "accepted": {"type": "array", "items": {"type": "string"}, "description": "The recipients the email was sent to. Empty when `status` is `failed`."},
        "rejected": {"type": "array", "items": {"$ref": "#/components/schemas/EmailRejection"}, "description": "The addresses the store could not send to, one object each. Empty when `status` is `success`."},
        "cc": {"type": "array", "items": {"type": "string"}, "description": "The addresses you sent in `cc`."},
        "bcc": {"type": "array", "items": {"type": "string"}, "description": "The addresses you sent in `bcc`."},
    }},
    "EmailRejection": {"type": "object", "description": "One address the store could not send to.", "properties": {
        "email": {"type": "string", "description": "The address."},
        "reason": {"type": "string", "description": "Why the send to this address failed, such as `send_failed` when the mail server failed the send."},
    }},
    "EmailError": {"type": "object", "properties": {"error": {"type": "object", "properties": {
        "code": {"type": "string", "description": "A machine-readable reason, such as `invalid_request` or `rate_limited`."},
        "message": {"type": "string", "description": "What went wrong, such as `Plugin not found` or `request body is empty`."},
        "details": {"type": "array", "description": "One entry per rejected field, or an empty list.", "items": {"type": "object", "properties": {
            "field": {"type": "string", "description": "The field that was rejected, such as `subject`, `recipients[1]` or `plugin_uuid`."},
            "code": {"type": "string", "description": "Why it was rejected, such as `required`, `invalid_email`, `too_many` or `daily_limit_reached`."},
            "message": {"type": ["string", "null"], "description": "The reason in words."},
            "value": {"description": "The value involved, when the API includes it."},
        }}},
        "request_id": {"type": "string", "description": "Identifies this request."},
    }}}},
}
