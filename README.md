# WebCommander API and SDK documentation

Source of the WebCommander API and SDK reference site, built with [Mintlify](https://mintlify.com).
The reference covers the WebCommander REST API and its seven SDKs: Python, JavaScript, PHP, Java,
.NET, Dart and Go.

## Layout

| Path | What it holds |
| --- | --- |
| `docs.json` | Site configuration and navigation |
| `introduction.mdx`, `installation.mdx`, `authentication.mdx` | Hand-written guide pages |
| `<module>.mdx` | Generated overview page for each module |
| `api-reference/` | Generated endpoint pages and `openapi.json` |
| `snippets/` | Generated client setup snippets used by the Authentication page |
| `tools/` | The reference generator and its inputs; never published |

## Regenerate the reference

The overview pages, endpoint pages, `openapi.json`, snippets and the API reference navigation are
generated. Edit the inputs under `tools/` and rebuild instead of editing the output; see
[tools/README.md](tools/README.md).

```bash
cd tools
python build_reference.py
```

## Preview and check

```bash
npm i -g mint
mint dev
mint broken-links
```
