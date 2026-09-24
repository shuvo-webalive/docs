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


def operation(endpoint, snippets):
    samples = [{"lang": "bash", "label": "cURL", "source": curl(endpoint)}]
    for sdk, lang, label in SDKS:
        samples.append({"lang": lang, "label": label, "source": snippets[sdk]["endpoints"][endpoint["key"]]["code"]})
    op = {
        "tags": [customers.TAG],
        "summary": endpoint["title"],
        "operationId": endpoint["key"],
        "description": endpoint["description"],
        "parameters": endpoint.get("parameters", []),
        "responses": {},
        "x-codeSamples": samples,
    }
    if endpoint.get("body"):
        media = "multipart/form-data" if endpoint.get("multipart") else "application/json"
        content = {"schema": endpoint["body"]["schema"]}
        if "example" in endpoint["body"]:
            content["example"] = endpoint["body"]["example"]
        op["requestBody"] = {"required": True, "content": {media: content}}
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


def spec(snippets):
    paths = {}
    for endpoint in customers.ENDPOINTS:
        paths.setdefault(endpoint["path"], {})[endpoint["method"].lower()] = operation(endpoint, snippets)
    return {
        "openapi": "3.1.0",
        "info": {"title": "WebCommander API", "version": "v4"},
        "servers": [{
            "url": "https://{store}/api/v4",
            "variables": {"store": {"default": "your-store.example.com", "description": "Your store's host name."}},
        }],
        "security": [{"bearerAuth": []}],
        "tags": [{"name": customers.TAG}],
        "paths": paths,
        "components": {
            "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer", "description": "An access token from `POST /api/v4/oauth2/token`. The SDKs get and renew it for you."}},
            "schemas": customers.SCHEMAS,
        },
    }


def page(endpoint):
    return "\n".join([
        "---",
        "title: \"%s\"" % endpoint["title"],
        "description: \"%s\"" % endpoint["summary"].replace("\"", "'"),
        "openapi: \"%s %s\"" % (endpoint["method"], endpoint["path"]),
        "---",
        "",
        endpoint["description"],
        "",
        "<Note>The SDK samples assume a client set up once, as shown in [Authentication](/authentication#set-up-a-client).</Note>",
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
        "Fifteen endpoints, available in all seven SDKs. Every path is under `/api/v4/admin/customers`.",
        "",
        "<Warning>",
        "  Paths take the customer's `customer_id`. A customer also carries an `internal_id`, which is a",
        "  second id space over the same records: sending it by mistake can return a **different customer",
        "  with a `200`** rather than a `404`. Check the record you get back is the one you asked for.",
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
        "Every sample on these pages starts from that client. With cURL, send the access token as",
        "`Authorization: Bearer $ACCESS_TOKEN`.",
        "",
        "## Things to know",
        "",
        "- **Listings are capped at 20 rows a page.** A larger `limit` is accepted and the cap is echoed back",
        "  in `pagination.limit`. Page with `page` or `offset`.",
        "- **A new customer cannot sign in until it is active.** Without `status: \"active\"` a customer is",
        "  created `awaiting_verification`, and change-password answers `401` for it.",
        "- **The export is every customer.** Its parameters switch columns on and off; they do not filter rows.",
        "- **Errors share one shape:** `status`, `code` and `message`, plus `error` and a per-field `errors`",
        "  list when the API gives them.",
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
        (OUT / "customers" / (endpoint["slug"] + ".mdx")).write_text(page(endpoint), encoding="utf-8")
    (DOCS / "customers.mdx").write_text(overview(), encoding="utf-8")
    (DOCS / "snippets").mkdir(exist_ok=True)
    (DOCS / "snippets" / "client-setup.mdx").write_text(client_setup(snippets), encoding="utf-8")
    print("Built the overview, %d endpoint pages and openapi.json" % len(customers.ENDPOINTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
