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
GUIDE_PAGES = ["introduction", "installation", "api-application", "authentication", "authentication-legacy", "prepare-a-new-store"]
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


IMPORT_LINE = {
    "python": re.compile(r"(import|from) \S"),
    "js": re.compile(r"import \S"),
    "php": re.compile(r"(use|require) \S"),
    "java": re.compile(r"import \S"),
    "dotnet": re.compile(r"using [\w.]+;$"),
    "dart": re.compile(r"import \S"),
}
PROGRAM_FILES = {"python": "main.py", "js": "main.mjs", "php": "main.php", "java": "Main.java",
                 "dotnet": "Program.cs", "dart": "main.dart", "go": "main.go"}


def split_imports(sdk, code):
    """Splits the import lines at the top of a sample or setup from the code below them."""
    if sdk == "go":
        block = re.match(r"\s*import \((.*?)\n\)\n", code, re.S)
        if not block:
            return [], code.strip("\n")
        return [line.strip() for line in block.group(1).splitlines() if line.strip()], code[block.end():].strip("\n")
    lines = code.strip("\n").splitlines()
    imports = []
    while lines and (not lines[0].strip() or IMPORT_LINE[sdk].match(lines[0])):
        line = lines.pop(0)
        if line.strip():
            imports.append(line)
    return imports, "\n".join(lines).strip("\n")


def indent(code, prefix):
    return "\n".join(prefix + line if line.strip() else "" for line in code.splitlines())


def used(name, code):
    return re.search(r"(?<![\w.])%s\b" % re.escape(name), code) is not None


def python_program(imports, code, complete):
    standard = sorted({line for line in imports if "webcommander" not in line})
    sdk = sorted({line for line in imports if "webcommander" in line})
    return "\n\n".join(part for part in ["\n".join(standard), "\n".join(sdk), code] if part)


def js_program(imports, code, complete):
    names = {}
    for line in imports:
        found = re.match(r"import \{(.*)\} from '(.*)';$", line)
        if not found:
            raise SystemExit("cannot merge the JavaScript import: " + line)
        listed = names.setdefault(found.group(2), [])
        listed += [name.strip() for name in found.group(1).split(",") if name.strip() not in listed]
    order = sorted(names, key=lambda source: (not source.startswith("node:"), source))
    return "\n".join("import {%s} from '%s';" % (", ".join(names[source]), source) for source in order) + "\n\n" + code


def php_program(imports, code, complete):
    requires = "\n".join(line for line in imports if line.startswith("require"))
    uses = "\n".join(sorted({line for line in imports if line.startswith("use ")}))
    return "\n\n".join(part for part in ["<?php" if complete else "", requires, uses, code] if part)


def java_program(imports, code, complete):
    kept = "\n".join(sorted({line for line in imports if used(line.rstrip(";").rsplit(".", 1)[1], code)}))
    if not complete:
        return kept + "\n\n" + code
    return (kept + "\n\npublic class Main {\n    public static void main(String[] args) throws Exception {\n"
            + indent(code, " " * 8) + "\n    }\n}")


def dotnet_program(imports, code, complete):
    return "\n".join(dict.fromkeys(imports)) + "\n\n" + code


def dart_program(imports, code, complete):
    groups = [sorted({line for line in imports if "'dart:" in line}), sorted({line for line in imports if "'dart:" not in line})]
    head = "\n\n".join("\n".join(group) for group in groups if group)
    if not complete:
        return head + "\n\n" + code
    return head + "\n\nFuture<void> main() async {\n" + indent(code, "  ") + "\n}"


def go_program(imports, code, complete):
    def name(spec):
        parts = spec.split()
        return parts[0] if len(parts) == 2 else parts[-1].strip('"').rsplit("/", 1)[-1]
    kept = [spec for spec in dict.fromkeys(imports) if used(name(spec), code)]
    standard = sorted(spec for spec in kept if "." not in spec.split()[-1].split("/")[0])
    other = sorted(spec for spec in kept if spec not in standard)
    block = "\n".join("\t" + spec if spec else "" for spec in standard + ([""] if standard and other else []) + other)
    head = "import (\n" + block + "\n)"
    if not complete:
        return head + "\n\n" + code
    return "package main\n\n" + head + "\n\nfunc main() {\n" + indent(code, "\t") + "\n}"


PROGRAMS = {"python": python_program, "js": js_program, "php": php_program, "java": java_program,
            "dotnet": dotnet_program, "dart": dart_program, "go": go_program}


def program(sdk, parts, complete=False):
    """Joins code parts in order with their imports merged at the top. A complete program also gets
    what its language needs to compile on its own, such as a main function."""
    imports, codes = [], []
    for part in parts:
        part_imports, part_code = split_imports(sdk, part)
        imports += part_imports
        codes.append(part_code)
    return PROGRAMS[sdk](imports, "\n\n".join(code for code in codes if code), complete) + "\n"


def operation(module, endpoint, snippets, setups):
    samples = [{"lang": "bash", "label": "cURL", "source": curl(endpoint)}]
    for sdk, lang, label in SDKS:
        code = program(sdk, [setups[sdk]["client"], snippets[sdk]["endpoints"][endpoint["key"]]["code"]])
        samples.append({"lang": lang, "label": label, "source": code})
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


CURL_SETUP_NEW = """curl -X POST "$WC_AUTH_BASE_URL/api/v1/oauth/token" \\
  -H "Content-Type: application/x-www-form-urlencoded" \\
  --data-urlencode "grant_type=client_credentials" \\
  --data-urlencode "client_id=$WC_CLIENT_ID" \\
  --data-urlencode "client_secret=$WC_CLIENT_SECRET\""""

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


def spec(areas, snippets, setups, schemas, renames):
    paths = {}
    tags = []
    for area in areas:
        for module in area["modules"]:
            tags.append({"name": module.TAG})
            for endpoint in module.ENDPOINTS:
                op = operation(module, endpoint, snippets[module.NAME], setups)
                op = json.loads(rename_refs(json.dumps(op), renames[module.NAME]))
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
            "securitySchemes": {"bearerAuth": {"type": "http", "scheme": "bearer", "description": "An access token from your Hykmah base URL (new sign-in) or from your store (legacy sign-in). See Authentication (New) and Authentication (Legacy). The SDKs get and renew it for you."}},
            "schemas": schemas,
        },
    }


def page(endpoint):
    note = ("The SDK samples get their client from credentials your app registers once when it starts, as shown in "
            "[Authentication (New)](/authentication#set-up-a-client). To try the call here, click **Try it**, set `store` to your store's host name and paste an access token. "
            "Get the token as shown in [Authentication (New)](/authentication#calling-the-api-directly), or in "
            "[Authentication (Legacy)](/authentication-legacy#calling-the-api-directly) if your store signs in with a redirect URI and an auth string.")
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
        "<Note>%s</Note>" % note,
        "",
    ])


def badge(method):
    return ('<span style={{fontFamily: "var(--font-mono, monospace)", fontSize: "0.72rem", fontWeight: 700, '
            'letterSpacing: "0.02em", color: "%s"}}>%s</span>' % (METHOD_COLOURS[method], method))


def code_group(setups, field, curl_tab=None, complete=False):
    tabs = ["<CodeGroup>"]
    if curl_tab:
        tabs += ["```bash cURL", curl_tab, "```", ""]
    for sdk, lang, label in SDKS:
        tabs += ["```%s %s" % (lang, label), program(sdk, [setups[sdk][field]], complete).rstrip(), "```", ""]
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
        "Register your credentials once when your app starts, as shown in",
        "[Authentication (New)](/authentication), or in [Authentication (Legacy)](/authentication-legacy) if your store",
        "signs in with a redirect URI and an auth string. Every SDK sample on these pages then gets its client in one line.",
        "With cURL, send the access token in an `Authorization` header: `Authorization: Bearer $ACCESS_TOKEN`.",
        "",
    ]
    if getattr(module, "NOTES", None):
        lines += ["## Things to know", ""] + ["- " + note for note in module.NOTES] + [""]
    return "\n".join(lines)


def module_pages(module):
    return [module.SLUG] + ["api-reference/%s/%s" % (module.SLUG, endpoint["slug"]) for endpoint in module.ENDPOINTS]


def navigation(areas):
    groups = []
    for area in areas:
        modules = area["modules"]
        if len(modules) == 1 and modules[0].TAG == area["name"]:
            groups.append({"group": area["name"], "icon": area["icon"], "expanded": False, "pages": module_pages(modules[0])})
        else:
            groups.append({"group": area["name"], "icon": area["icon"], "expanded": False, "pages": [
                {"group": module.TAG, "expanded": False, "pages": module_pages(module)} for module in modules]})
    return groups


def write_programs(target, areas, snippets, setups):
    """Writes the registration and every sample, exactly as the pages show them, as programs that compile on their
    own, one folder each. Samples leave out the registration, so an import it provides cannot hide a missing one."""
    count = 0
    for sdk, _, _ in SDKS:
        for name, field in (("register_new", "register_hykmah"), ("register_legacy", "register"), ("register_both", "register_both")):
            folder = target / sdk / "authentication" / name
            folder.mkdir(parents=True, exist_ok=True)
            (folder / PROGRAM_FILES[sdk]).write_bytes(program(sdk, [setups[sdk][field]], complete=True).encode("utf-8"))
            count += 1
    for area in areas:
        for module in area["modules"]:
            for endpoint in module.ENDPOINTS:
                for sdk, _, _ in SDKS:
                    folder = target / sdk / module.NAME / endpoint["key"]
                    folder.mkdir(parents=True, exist_ok=True)
                    sample = snippets[module.NAME][sdk]["endpoints"][endpoint["key"]]["code"]
                    code = program(sdk, [setups[sdk]["client"], sample], complete=True)
                    (folder / PROGRAM_FILES[sdk]).write_bytes(code.encode("utf-8"))
                    count += 1
    print("Wrote %d programs to %s" % (count, target))
    return 0


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
    if len(sys.argv) == 3 and sys.argv[1] == "--programs":
        return write_programs(pathlib.Path(sys.argv[2]), areas, snippets, setups)
    schemas, renames = prefixed_schemas(areas)
    document = json.dumps(spec(areas, snippets, setups, schemas, renames), indent=2, ensure_ascii=False)
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
                (OUT / module.SLUG / (endpoint["slug"] + ".mdx")).write_text(page(endpoint), encoding="utf-8")
                count += 1
            (DOCS / (module.SLUG + ".mdx")).write_text(overview(module), encoding="utf-8")
    (DOCS / "snippets").mkdir(exist_ok=True)
    (DOCS / "snippets" / "client-setup.mdx").write_text(code_group(setups, "register_hykmah", CURL_SETUP_NEW, complete=True), encoding="utf-8")
    (DOCS / "snippets" / "client-setup-legacy.mdx").write_text(code_group(setups, "register", CURL_SETUP, complete=True), encoding="utf-8")
    (DOCS / "snippets" / "client-setup-both.mdx").write_text(code_group(setups, "register_both", complete=True), encoding="utf-8")
    (DOCS / "snippets" / "client-build.mdx").write_text(code_group(setups, "client"), encoding="utf-8")

    docs_json = json.loads((DOCS / "docs.json").read_text(encoding="utf-8"))
    for group in docs_json["navigation"]["groups"]:
        if group["group"] == "API reference":
            group["pages"] = navigation(areas)
        elif group["group"] == "Guides":
            for section in group["pages"]:
                if isinstance(section, dict) and section.get("group") == "Get started":
                    section["pages"] = list(GUIDE_PAGES)
    (DOCS / "docs.json").write_text(json.dumps(docs_json, indent=2) + "\n", encoding="utf-8")

    modules = sum(len(area["modules"]) for area in areas)
    print("Built %d modules, %d endpoint pages, their overviews and openapi.json" % (modules, count))
    return 0


if __name__ == "__main__":
    sys.exit(main())
