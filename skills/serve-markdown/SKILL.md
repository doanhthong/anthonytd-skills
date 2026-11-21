---
name: serve-markdown
description: Serve a markdown file or folder as rendered HTML to other devices on the user's Tailscale tailnet (phone, tablet, another laptop). GitHub styling, code highlighting, mermaid diagrams, live reload on save. Use when the user wants to "view this markdown on my phone", "share this doc on tailscale", "serve this .md", "open the plan on my iPad", or invokes /serve-markdown.
---

# Serve Markdown

Run `scripts/serve.py` on a `.md` file or a folder. It binds to this machine's Tailscale IP only, so only tailnet devices can reach it.

## Steps

1. Resolve the path. If the user didn't name one, use the markdown file you just wrote or discussed. If none, ask.
2. Start the server in the background (it runs until stopped):
   ```sh
   python3 <skill-dir>/scripts/serve.py <path> [--port 8765]
   ```
   Use your harness's background mode (e.g. `run_in_background`). Don't block on it.
3. Read the first lines of output and give the user the URLs. Prefer the MagicDNS one:
   ```
   http://<machine>.<tailnet>.ts.net:8765/plan.md
   http://<machine>:8765/plan.md
   http://100.x.y.z:8765/plan.md
   ```
4. When the user is done, stop the background process.

## Behavior

| Input | Result |
|---|---|
| A file | Opens that file. The whole parent folder is reachable, so relative images and links work. |
| A folder | Index of every `.md` under it (skips dotfolders, `node_modules`). |
| `?raw` on any URL | Raw markdown. |

- Port taken → tries the next one (up to +49). Read the printed URL, don't assume 8765.
- Edits to the file reload the open page within ~2s.
- Rendering runs in the viewer's browser and loads marked, highlight.js, and mermaid from jsDelivr. The viewing device needs internet.

## Troubleshooting

- **"Tailscale IP not found"** → Tailscale isn't running. Ask the user to run `tailscale up`.
- **URL times out on the other device** → that device isn't on the tailnet, or an ACL blocks the port. Try the `100.x` URL to rule out DNS.
- **Need HTTPS or a stable URL** → suggest `tailscale serve --bg <port>` in front of it. That publishes `https://<machine>.<tailnet>.ts.net/`. Don't run it unasked: it changes the user's Tailscale config.
