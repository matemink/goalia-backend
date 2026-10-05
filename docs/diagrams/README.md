# Architecture overview

[Interactive map](https://matemink.github.io/goalia-backend/) ·
[Diagram source](overview.architecture.json)

The map follows GET /api/matches through request-time refresh, raw-match caching and prediction enrichment in one Python process.
Source links are pinned in `meta.repository.revision`; the diagram is a
snapshot of inspected code, not a runtime validation result.

Generated with [Archify v3.0.1](https://github.com/tt-a1i/archify/tree/v3.0.1)
(MIT; see [license](LICENSE.archify.txt)). Archify is an optional documentation
tool; the runtime and CI builds do not depend on it.

To refresh the map, inspect the affected runtime paths, update the JSON and its
source revision, then run from the repository root with Node.js 18+ and an
external checkout of Archify v3.0.1:

```bash
node /path/to/archify/skills/archify/bin/archify.mjs finalize architecture \
  docs/diagrams/overview.architecture.json docs/diagrams/overview.html \
  --repo-root . --quality showcase --json \
  --out-dir .archify/review
```

Require passing validation, artifact and browser checks. Open the HTML and
export **SVG · Light** and **SVG · Dark** as `overview-light.svg` and
`overview-dark.svg`. Inspect both exports and update them in the same commit
as the JSON and HTML. The project README uses these images.

The Pages workflow publishes the checked HTML and these assets from `main`;
it does not regenerate the map or publish runtime logs.
