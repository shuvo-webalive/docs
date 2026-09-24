# API reference generator

Builds `api-reference/openapi.json`, every module's endpoint pages under `api-reference/<module>/`,
each module's overview page (`<module>.mdx` at the docs root), `snippets/client-setup.mdx` (the client
setup the Authentication page imports), and the **API reference** part of the `docs.json` navigation.
This folder is listed in `.mintignore`, so it is never published.

```bash
cd tools
python build_reference.py
```

| Path | What it holds |
| --- | --- |
| `modules.json` | The areas and modules to publish, in sidebar order. Add a module here to publish it. |
| `modules/<module>.py` | One module's facts: `TAG`, `SLUG`, `BASE`, overview text (`INTRO`, `WARNING`, `NOTES`), `ENDPOINTS` (paths, parameters, bodies, responses, plain-language wording, `example_call` for the cURL sample) and `SCHEMAS`. Written from the SDKs' `ENDPOINTS.md`, which records live-store measurements. |
| `modules/customers_copy.json` | The reviewed plain-language wording for Customers, applied by `modules/customers.py`. |
| `snippets/<sdk>/setup.json` | That SDK's client setup. |
| `snippets/<sdk>/<module>.json` | One sample per endpoint, compiled or type-checked against that SDK's `development` branch. |
| `build_reference.py` | Writes everything listed above. |

The build fails when:

- any SDK is missing a sample for any endpoint of a published module (an endpoint is documented only
  when all seven SDKs have it),
- endpoint keys repeat across modules,
- the spec contains a store address.

Two modules may use the same schema name; the later one is prefixed with its module name. Do not edit
generated files by hand; change the inputs here and rebuild.

The knowledge base build (`webcommander-docs-kb/build.py`) reads `modules/<module>.py` too, so its
endpoint tables and these pages always list the same endpoints.
