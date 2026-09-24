"""Builds the API reference: api-reference/openapi.json, the endpoint pages, each module's overview
page, the client setup snippet and the API reference part of the docs.json navigation.

Modules are listed in modules.json. Each module's endpoint facts live in modules/<module>.py, and its
code samples in snippets/<sdk>/<module>.json, one file per SDK, each compiled against that SDK. An
endpoint is written only when all seven SDKs have a sample for it; the build fails otherwise.
"""

import importlib.util
import json
import pathlib
import re
import sys

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
METHOD_COLOURS = {"GET": "#0f7b6c", "POST": "#2563eb", "PUT": "#b45309", "PATCH": "#7a5af8",
                  "DELETE": "#c2410c", "HEAD": "#475467"}


def load_module(name):
    spec = importlib.util.spec_from_file_location("reference_" + name, TOOLS / "modules" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.NAME = name
    return module


def load_areas():
    listing = json.loads((TOOLS / "modules.json").read_text(encoding="utf-8"))
    return [dict(area, modules=[load_module(name) for name in area["modules"]]) for area in listing["areas"]]


def load_json(path, problems, what):
    if not path.is_file():
        problems.append("no %s (%s)" % (what, path.relative_to(TOOLS)))
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def curl(endpoint):
    call = endpoint.get("example_call", {})
    path = endpoint["path"]
    for name, value in call.get("path", {}).items():
        path = path.replace("{%s}" % name, str(value))
    query = call.get("query", "")
    if isinstance(query, dict):
        query = "&".join("%s=%s" % (key, value) for key, value in query.items())
    url = "$WC_BASE_URL/api/v4" + path + ("?" + query if query else "")
    method = endpoint["method"]
    lines = ["curl %s\"%s\" \\" % ("-I " if method == "HEAD" else "-X %s " % method, url),
             "  -H \"Authorization: Bearer $ACCESS_TOKEN\""]
    body = call.get("body", endpoint.get("body", {}).get("example"))
    if call.get("output"):
        lines[-1] += " \\"
        lines.append("  -o %s" % call["output"])
    elif endpoint.get("multipart"):
        lines[-1] += " \\"
        lines.append("  -F \"file=@%s\"" % call.get("file", "file"))
    elif body is not None:
        lines[-1] += " \\"
        lines.append("  -H \"Content-Type: application/json\" \\")
        lines.append("  -d '%s'" % json.dumps(body, indent=2).replace("\n", "\n  "))
    return "\n".join(lines)


def without_path_example(parameter):
    if parameter.get("in") != "path":
        return parameter
    schema = {k: v for k, v in parameter.get("schema", {}).items() if k != "example"}
    return dict({k: v for k, v in parameter.items() if k != "example"}, schema=schema)


def operation(module, endpoint, snippets):
    samples = [{"lang": "bash", "label": "cURL", "source": curl(endpoint)}]
    for sdk, lang, label in SDKS:
        samples.append({"lang": lang, "label": label, "source": snippets[sdk]["endpoints"][endpoint["key"]]["code"]})
    op = {
        "tags": [module.TAG],
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

CURL_SETUP = """curl -X POST "$WC_BASE_URL/api/v4/oauth2/token" \\
  -H "Content-Type: application/json" \\
  -d '{
    "grant_type": "client_credentials",
    "client_id": "'"$WC_CLIENT_ID"'",
    "client_secret": "'"$WC_CLIENT_SECRET"'",
    "redirect_uri": "'"$WC_REDIRECT_URI"'",
    "auth_string": "'"$WC_AUTH_STRING"'"
  }'"""


def prefixed_schemas(areas):
    """Merge every module's schemas; a name already taken by an earlier module gets the module's prefix."""
    merged, renames = {}, {}
    for area in areas:
        for module in area["modules"]:
            mapping = {}
            for name, schema in module.SCHEMAS.items():
                if name in merged and merged[name] != schema:
                    mapping[name] = "".join(part.capitalize() for part in module.NAME.split("_")) + name
            renames[module.NAME] = mapping
            for name, schema in module.SCHEMAS.items():
                merged[mapping.get(name, name)] = json.loads(rename_refs(json.dumps(schema), mapping))
    return merged, renames


def rename_refs(text, mapping):
    for old, new in mapping.items():
        text = text.replace('"#/components/schemas/%s"' % old, '"#/components/schemas/%s"' % new)
    return text


def spec(areas, snippets, schemas, renames):
    paths = {"/oauth2/token": {"post": token_operation()}}
    tags = [{"name": "Authentication"}]
    for area in areas:
        for module in area["modules"]:
            tags.append({"name": module.TAG})
            for endpoint in module.ENDPOINTS:
                op = json.loads(rename_refs(json.dumps(operation(module, endpoint, snippets[module.NAME])), renames[module.NAME]))
                paths.setdefault(endpoint["path"], {})[endpoint["method"].lower()] = op
    return {
        "openapi": "3.1.0",
        "info": {"title": "WebCommander API", "version": "v4"},
        "servers": [{
            "url": "https://{store}/api/v4",
            "variables": {"store": {"default": "your-store.example.com", "description": "Your store's host name, without https://."}},
        }],
        "security": [{"bearerAuth": []}],
        "tags": tags,
        "paths": paths,
        "components": {
            "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer", "description": "An access token from `POST /api/v4/oauth2/token`. The SDKs get and renew it for you."}},
            "schemas": schemas,
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
    note = ("Each call above gives you the response body documented on this page. The SDK samples use a client you set up once, "
            "as shown in [Authentication](/authentication#set-up-a-client). To try the call here, click **Try it**, set `store` "
            "to your store's host name and paste an access token from "
            "[Get an access token](/api-reference/authentication/get-an-access-token).")
    if endpoint.get("body") and not endpoint.get("multipart"):
        note += " To send a raw JSON body instead of filling in fields, copy the cURL sample and edit its `-d` payload."
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
        "<Note>%s</Note>" % note,
        "",
    ])


def badge(method):
    return ('<span style={{fontFamily: "var(--font-mono, monospace)", fontSize: "0.72rem", fontWeight: 700, '
            'letterSpacing: "0.02em", color: "%s"}}>%s</span>' % (METHOD_COLOURS[method], method))


def client_setup(setups):
    tabs = ["<CodeGroup>", "```bash cURL", CURL_SETUP, "```", ""]
    for sdk, lang, label in SDKS:
        tabs += ["```%s %s" % (lang, label), setups[sdk]["setup"].rstrip(), "```", ""]
    tabs.append("</CodeGroup>")
    return "\n".join(tabs) + "\n"


def short_path(module, path):
    tail = module.BASE[module.BASE.rfind("/"):]
    return path.replace(module.BASE, "…" + tail, 1)


def overview(module):
    rows = ["| [%s](/api-reference/%s/%s) | %s | `%s` | %s |" % (
        endpoint["title"], module.SLUG, endpoint["slug"], badge(endpoint["method"]),
        short_path(module, endpoint["path"]), endpoint["summary"]) for endpoint in module.ENDPOINTS]
    lines = [
        "---",
        "title: \"%s\"" % module.TAG,
        "sidebarTitle: \"Overview\"",
        "description: \"%s\"" % module.OVERVIEW_DESCRIPTION.replace("\"", "'"),
        "---",
        "",
        module.INTRO,
        "",
    ]
    if getattr(module, "WARNING", None):
        lines += ["<Warning>", "  " + module.WARNING, "</Warning>", ""]
    lines += [
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
    ]
    if getattr(module, "NOTES", None):
        lines += ["## Things to know", ""] + ["- " + note for note in module.NOTES] + [""]
    return "\n".join(lines)


def module_pages(module):
    return [module.SLUG] + ["api-reference/%s/%s" % (module.SLUG, endpoint["slug"]) for endpoint in module.ENDPOINTS]


def navigation(areas):
    groups = [{"group": "Authentication", "icon": "key", "expanded": False,
               "pages": ["api-reference/authentication/get-an-access-token"]}]
    for area in areas:
        modules = area["modules"]
        if len(modules) == 1 and modules[0].TAG == area["name"]:
            groups.append({"group": area["name"], "icon": area["icon"], "expanded": False, "pages": module_pages(modules[0])})
        else:
            groups.append({"group": area["name"], "icon": area["icon"], "expanded": False, "pages": [
                {"group": module.TAG, "expanded": False, "pages": module_pages(module)} for module in modules]})
    return groups


def main():
    areas = load_areas()
    problems = []
    setups = {sdk: load_json(TOOLS / "snippets" / sdk / "setup.json", problems, "%s setup" % sdk) for sdk, _, _ in SDKS}
    snippets = {}
    for area in areas:
        for module in area["modules"]:
            snippets[module.NAME] = {}
            for sdk, _, _ in SDKS:
                data = load_json(TOOLS / "snippets" / sdk / (module.NAME + ".json"), problems, "%s samples for %s" % (sdk, module.NAME))
                snippets[module.NAME][sdk] = data
                if data is None:
                    continue
                for endpoint in module.ENDPOINTS:
                    if endpoint["key"] not in data.get("endpoints", {}):
                        problems.append("%s has no sample for %s.%s" % (sdk, module.NAME, endpoint["key"]))
    if problems:
        print("Build failed: an endpoint is documented only when all seven SDKs have a sample.")
        for problem in problems:
            print("  - " + problem)
        return 1

    keys = [endpoint["key"] for area in areas for module in area["modules"] for endpoint in module.ENDPOINTS]
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        print("Build failed: endpoint keys are not unique across modules: %s" % ", ".join(duplicates))
        return 1
    schemas, renames = prefixed_schemas(areas)
    document = json.dumps(spec(areas, snippets, schemas, renames), indent=2, ensure_ascii=False)
    if STORE_ADDRESS.search(document):
        print("Build failed: the spec contains a store address")
        return 1
    OUT.mkdir(exist_ok=True)
    (OUT / "openapi.json").write_text(document + "\n", encoding="utf-8")
    count = 0
    for area in areas:
        for module in area["modules"]:
            (OUT / module.SLUG).mkdir(parents=True, exist_ok=True)
            for endpoint in module.ENDPOINTS:
                (OUT / module.SLUG / (endpoint["slug"] + ".mdx")).write_text(page(endpoint, snippets[module.NAME]), encoding="utf-8")
                count += 1
            (DOCS / (module.SLUG + ".mdx")).write_text(overview(module), encoding="utf-8")
    (OUT / "authentication").mkdir(exist_ok=True)
    (OUT / "authentication" / "get-an-access-token.mdx").write_text(TOKEN_PAGE, encoding="utf-8")
    (DOCS / "snippets").mkdir(exist_ok=True)
    (DOCS / "snippets" / "client-setup.mdx").write_text(client_setup(setups), encoding="utf-8")

    docs_json = json.loads((DOCS / "docs.json").read_text(encoding="utf-8"))
    for group in docs_json["navigation"]["groups"]:
        if group["group"] == "API reference":
            group["pages"] = navigation(areas)
    (DOCS / "docs.json").write_text(json.dumps(docs_json, indent=2) + "\n", encoding="utf-8")

    modules = sum(len(area["modules"]) for area in areas)
    print("Built %d modules, %d endpoint pages, their overviews and openapi.json" % (modules, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
