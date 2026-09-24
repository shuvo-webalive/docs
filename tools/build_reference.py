"""Builds the API reference: api-reference/openapi.json and one page per endpoint.

Endpoint facts come from customers.py. Code samples come from snippets/<sdk>.json, one file
per SDK, each compiled against that SDK. An endpoint is written only when all seven SDKs
have a sample for it; the build fails otherwise.
"""

import json
import pathlib
import re
import sys

import customers

TOOLS = pathlib.Path(__file__).resolve().parent
DOCS = TOOLS.parent
OUT = DOCS / "api-reference"
SDKS = [
    ("python", "python", "Python"),
    ("js", "javascript", "JavaScript"),
    ("php", "php", "PHP"),
    ("java", "java", "Java"),
    ("dotnet", "csharp", ".NET"),
    ("dart", "dart", "Dart"),
    ("go", "go", "Go"),
]
STORE_ADDRESS = re.compile(r"[a-z0-9-]+\.mywebcommander\.com", re.I)


def load_snippets():
    loaded = {}
    missing = []
    for sdk, _, _ in SDKS:
        path = TOOLS / "snippets" / (sdk + ".json")
        if not path.is_file():
            missing.append(sdk)
            continue
        loaded[sdk] = json.loads(path.read_text(encoding="utf-8"))
    return loaded, missing


def curl(endpoint):
    path = endpoint["path"].replace("{customer_id}", "123")
    url = "$WC_BASE_URL/api/v4" + path
    query = {
        "list_customers": "?limit=20&status=active",
        "count_customers": "?status=active",
        "check_email": "?email=jane@example.com",
        "list_store_credit_adjustments": "?limit=20",
    }.get(endpoint["key"], "")
    lines = ["curl -X %s \"%s%s\" \\" % (endpoint["method"], url, query),
             "  -H \"Authorization: Bearer $ACCESS_TOKEN\""]
    if endpoint["key"] == "export_customers":
        lines[-1] += " \\"
        lines.append("  -o customers.xlsx")
    elif endpoint.get("multipart"):
        lines[-1] += " \\"
        lines.append("  -F \"file=@customers.csv\"")
    elif endpoint.get("body"):
        lines[-1] += " \\"
        lines.append("  -H \"Content-Type: application/json\" \\")
        body = json.dumps(endpoint["body"]["example"], indent=2)
        lines.append("  -d '%s'" % body.replace("\n", "\n  "))
    return "\n".join(lines)


def without_path_example(parameter):
    if parameter.get("in") != "path":
        return parameter
    schema = {k: v for k, v in parameter.get("schema", {}).items() if k != "example"}
    return dict({k: v for k, v in parameter.items() if k != "example"}, schema=schema)


def operation(endpoint, snippets):
    samples = [{"lang": "bash", "label": "cURL", "source": curl(endpoint)}]
    for sdk, lang, label in SDKS:
        samples.append({"lang": lang, "label": label, "source": snippets[sdk]["endpoints"][endpoint["key"]]["code"]})
    op = {
        "tags": [customers.TAG],
        "summary": endpoint["title"],
        "operationId": endpoint["key"],
        "description": endpoint["description"],
        "parameters": [without_path_example(p) for p in endpoint.get("parameters", [])],
        "responses": {},
        "x-codeSamples": samples,
    }
    if endpoint.get("body"):
        media = "multipart/form-data" if endpoint.get("multipart") else "application/json"
        op["requestBody"] = {"required": True, "content": {media: {"schema": endpoint["body"]["schema"]}}}
    for status, response in endpoint["responses"].items():
        entry = {"description": response["description"]}
        if "schema" in response:
            content = {"schema": response["schema"]}
            if "example" in response:
                content["example"] = response["example"]
            entry["content"] = {response.get("content_type", "application/json"): content}
        elif int(status) >= 400:
            entry["content"] = {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}
        op["responses"][status] = entry
    return op


TOKEN_CURL = """curl -X POST "$WC_BASE_URL/api/v4/oauth2/token" \\
  -H "Content-Type: application/json" \\
  -d '{
    "grant_type": "client_credentials",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "redirect_uri": "YOUR_REDIRECT_URI",
    "auth_string": "YOUR_AUTH_STRING"
  }'"""


def token_operation():
    return {
        "tags": ["Authentication"],
        "summary": "Get an access token",
        "operationId": "get_access_token",
        "description": "Exchanges your store's credentials for an access token. Send the token as `Authorization: Bearer ACCESS_TOKEN` on every other call. The SDKs make this call for you and renew the token before it expires.",
        "security": [],
        "requestBody": {"required": True, "content": {"application/json": {
            "schema": {"type": "object", "required": ["grant_type", "client_id", "client_secret", "redirect_uri", "auth_string"], "properties": {
                "grant_type": {"type": "string", "enum": ["client_credentials"], "description": "Choose `client_credentials` from the list."},
                "client_id": {"type": "string", "description": "Your integration's client ID."},
                "client_secret": {"type": "string", "description": "The secret paired with the client ID."},
                "redirect_uri": {"type": "string", "description": "The redirect URI registered for your integration."},
                "auth_string": {"type": "string", "description": "Decides which user the token acts as."},
            }},
            "example": {"grant_type": "client_credentials", "client_id": "YOUR_CLIENT_ID", "client_secret": "YOUR_CLIENT_SECRET", "redirect_uri": "YOUR_REDIRECT_URI", "auth_string": "YOUR_AUTH_STRING"},
        }}},
        "responses": {
            "201": {"description": "The access token.", "content": {"application/json": {"schema": {"type": "object", "properties": {
                "access_token": {"type": "string", "description": "Send this as `Authorization: Bearer ACCESS_TOKEN`."},
                "expires_in": {"type": "integer", "description": "Seconds until the token expires."},
                "refresh_token": {"type": "string", "description": "Exchanged for a new access token when this one expires."},
            }}}}},
            "401": {"description": "The credentials were not accepted.", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}},
        },
        "x-codeSamples": [{"lang": "bash", "label": "cURL", "source": TOKEN_CURL}],
    }


TOKEN_PAGE = """---
title: "Get an access token"
description: "Exchange your store's credentials for the token every other call needs."
openapi: "POST /oauth2/token"
---

Every call to the API needs an access token. Request one here with your store's credentials, then send
it as `Authorization: Bearer ACCESS_TOKEN`. The SDKs make this call for you, so you only need it for
cURL, another HTTP client, or to try the API on this site.

<Steps>
  <Step title="Enter your store and credentials">
    Click **Try it**, set `store` to your store's host name (without `https://`), choose
    `client_credentials` for `grant_type`, and fill in your client ID, client secret, redirect URI
    and auth string.
  </Step>
  <Step title="Send the request">
    The response holds `access_token`.
  </Step>
  <Step title="Use the token">
    On any other endpoint, click **Try it**, set the same `store`, and paste the token into
    **Authorization**.
  </Step>
</Steps>

<Warning>
  Calls you make here run against your real store: creating, changing and deleting data is real.
  Requests are sent through Mintlify's servers. Use test data, and never share your credentials.
</Warning>
"""


def spec(snippets):
    paths = {"/oauth2/token": {"post": token_operation()}}
    for endpoint in customers.ENDPOINTS:
        paths.setdefault(endpoint["path"], {})[endpoint["method"].lower()] = operation(endpoint, snippets)
    return {
        "openapi": "3.1.0",
        "info": {"title": "WebCommander API", "version": "v4"},
        "servers": [{
            "url": "https://{store}/api/v4",
            "variables": {"store": {"default": "your-store.example.com", "description": "Your store's host name, without https://."}},
        }],
        "security": [{"bearerAuth": []}],
        "tags": [{"name": "Authentication"}, {"name": customers.TAG}],
        "paths": paths,
        "components": {
            "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer", "description": "An access token from `POST /api/v4/oauth2/token`. The SDKs get and renew it for you."}},
            "schemas": customers.SCHEMAS,
        },
    }


def sdk_call(snippet):
    found = re.search(
        r"([A-Za-z_$][\w$]*(?:\(\))?(?:\s*(?:\.|::|->)\s*[A-Za-z_$][\w$]*(?:\(\))?)*)\s*(\.|::|->)\s*"
        + re.escape(snippet["function"]) + r"\s*\(", snippet["code"])
    if not found:
        raise SystemExit("cannot find the %s call in its sample" % snippet["function"])
    return re.sub(r"\s+", "", found.group(1)) + found.group(2) + snippet["function"] + "()"


def page(endpoint, snippets):
    rows = ["| %s | `%s` |" % (label, sdk_call(snippets[sdk]["endpoints"][endpoint["key"]]))
            for sdk, _, label in SDKS]
    return "\n".join([
        "---",
        "title: \"%s\"" % endpoint["title"],
        "description: \"%s\"" % endpoint["summary"].replace("\"", "'"),
        "openapi: \"%s %s\"" % (endpoint["method"], endpoint["path"]),
        "---",
        "",
        endpoint["description"],
        "",
        "## SDK method",
        "",
        "| SDK | Call |",
        "| --- | --- |",
    ] + rows + [
        "",
        "<Note>Each call above gives you the response body documented on this page. The SDK samples use a client you set up once, as shown in [Authentication](/authentication#set-up-a-client). To try the call here, click **Try it**, set `store` to your store's host name and paste an access token from [Get an access token](/api-reference/authentication/get-an-access-token).</Note>",
        "",
    ])


METHOD_COLOURS = {"GET": "#0f7b6c", "POST": "#2563eb", "PUT": "#b45309", "DELETE": "#c2410c"}

CURL_SETUP = """curl -X POST "$WC_BASE_URL/api/v4/oauth2/token" \\
  -H "Content-Type: application/json" \\
  -d '{
    "grant_type": "client_credentials",
    "client_id": "'"$WC_CLIENT_ID"'",
    "client_secret": "'"$WC_CLIENT_SECRET"'",
    "redirect_uri": "'"$WC_REDIRECT_URI"'",
    "auth_string": "'"$WC_AUTH_STRING"'"
  }'"""


def badge(method):
    return ('<span style={{fontFamily: "var(--font-mono, monospace)", fontSize: "0.72rem", fontWeight: 700, '
            'letterSpacing: "0.02em", color: "%s"}}>%s</span>' % (METHOD_COLOURS[method], method))


def client_setup(snippets):
    tabs = ["<CodeGroup>", "```bash cURL", CURL_SETUP, "```", ""]
    for sdk, lang, label in SDKS:
        tabs += ["```%s %s" % (lang, label), snippets[sdk]["setup"].rstrip(), "```", ""]
    tabs.append("</CodeGroup>")
    return "\n".join(tabs) + "\n"


def overview():
    rows = []
    for endpoint in customers.ENDPOINTS:
        rows.append("| [%s](/api-reference/customers/%s) | %s | `%s` | %s |" % (
            endpoint["title"], endpoint["slug"], badge(endpoint["method"]),
            endpoint["path"].replace("/admin/customers", "…/customers"), endpoint["summary"]))
    return "\n".join([
        "---",
        "title: \"Customers\"",
        "sidebarTitle: \"Overview\"",
        "description: \"Read, create, update and remove customers, and manage their addresses, passwords and store credit.\"",
        "---",
        "",
        "The Customers API has fifteen endpoints, and you can call every one from all seven SDKs. Every path starts with `/api/v4/admin/customers`.",
        "",
        "<Warning>",
        "  Paths take the customer's `customer_id`. Each customer also has an `internal_id`, a separate",
        "  number that no path takes. If you send an `internal_id` by mistake and it matches another",
        "  customer's `customer_id`, you get **that other customer with a `200`** instead of a `404`.",
        "  Check that the customer you get back is the one you asked for.",
        "</Warning>",
        "",
        "## At a glance",
        "",
        "| Endpoint | Method | Path | What it does |",
        "| --- | --- | --- | --- |",
    ] + rows + [
        "",
        "## Before you call",
        "",
        "Set up a client once with your store's credentials, as shown in [Authentication](/authentication).",
        "The SDK samples on these pages use that client. With cURL, send the access token in an",
        "`Authorization` header: `Authorization: Bearer $ACCESS_TOKEN`.",
        "",
        "## Things to know",
        "",
        "- **A listing returns at most 20 records per call.** A larger `limit` is not rejected, but you",
        "  still get at most 20, and `pagination.limit` shows `20`. To get more, send the next `page`",
        "  number or a higher `offset` for as long as `pagination.has_next` is `true`.",
        "- **A new customer cannot sign in until it is active.** If you create a customer without",
        "  `status: \"active\"`, it is created as `awaiting_verification` with no usable login, even if you",
        "  send a `password`, and changing its password fails with `401`. Send `status: \"active\"` with a",
        "  `password` to create a customer who can sign in.",
        "- **An export always contains every customer.** Its parameters choose columns, not customers: a",
        "  column is removed when its parameter is anything other than `1`, `true`, `on` or `yes`, so",
        "  `status=active` exports everyone and removes the `Status` column. Importing an export rewrites",
        "  every customer in the store, so build import files from only the customers you want to change.",
        "- **Every error response has the same fields:** `status`, `code` and `message`, plus `error` (a",
        "  machine-readable reason) and `errors` (one entry per rejected field) when the API provides them.",
        "",
    ])


def main():
    snippets, missing = load_snippets()
    problems = ["no samples for %s" % sdk for sdk in missing]
    for sdk, data in snippets.items():
        for endpoint in customers.ENDPOINTS:
            if endpoint["key"] not in data.get("endpoints", {}):
                problems.append("%s has no sample for %s" % (sdk, endpoint["key"]))
    if problems:
        print("Build failed: an endpoint is documented only when all seven SDKs have a sample.")
        for problem in problems:
            print("  - " + problem)
        return 1

    document = json.dumps(spec(snippets), indent=2, ensure_ascii=False)
    if STORE_ADDRESS.search(document):
        print("Build failed: the spec contains a store address")
        return 1
    (OUT / "customers").mkdir(parents=True, exist_ok=True)
    (OUT / "openapi.json").write_text(document + "\n", encoding="utf-8")
    for endpoint in customers.ENDPOINTS:
        (OUT / "customers" / (endpoint["slug"] + ".mdx")).write_text(page(endpoint, snippets), encoding="utf-8")
    (DOCS / "customers.mdx").write_text(overview(), encoding="utf-8")
    (OUT / "authentication").mkdir(exist_ok=True)
    (OUT / "authentication" / "get-an-access-token.mdx").write_text(TOKEN_PAGE, encoding="utf-8")
    (DOCS / "snippets").mkdir(exist_ok=True)
    (DOCS / "snippets" / "client-setup.mdx").write_text(client_setup(snippets), encoding="utf-8")
    print("Built the overview, %d endpoint pages and openapi.json" % len(customers.ENDPOINTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
