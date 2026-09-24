# API reference generator

Builds `api-reference/openapi.json` and the pages under `api-reference/<module>/`. This folder is
listed in `.mintignore`, so it is never published.

```bash
cd tools
python build_reference.py
```

| File | What it holds |
| --- | --- |
| `customers.py` | The Customers endpoints: paths, parameters, bodies, responses and notes, as measured against a live store and recorded in the SDKs' `ENDPOINTS.md`. |
| `snippets/<sdk>.json` | One file per SDK: the client setup and one sample per endpoint. Every sample was compiled or type-checked against that SDK's `development` branch. |
| `build_reference.py` | Writes the spec, one page per endpoint and the module overview. |

An endpoint is documented only when all seven SDKs have a sample for it: the build fails if any
`snippets/<sdk>.json` is missing or lacks an endpoint. Do not edit the generated files under
`api-reference/` by hand; change the inputs here and rebuild.

The knowledge base build (`webcommander-docs-kb/build.py`) reads `customers.py` too, so its
endpoint table and these pages always list the same endpoints.
