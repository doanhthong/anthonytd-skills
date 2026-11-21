#!/usr/bin/env python3
"""Serve a markdown file or folder to your tailnet as rendered HTML.

Usage: serve.py PATH [--port N] [--host IP]

- PATH is a .md file or a directory. A file opens directly; a directory gets an index.
- Binds to this machine's Tailscale IPv4 only, so nothing leaks onto LAN or Wi-Fi.
- Pages reload in the browser when the file changes.
- Stdlib only. Rendering happens in the browser (marked + highlight.js + mermaid from a CDN).
"""
import argparse
import html
import json
import os
import posixpath
import shutil
import socket
import subprocess
import sys
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

MD_EXT = (".md", ".markdown", ".mdx")

PAGE = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github.min.css" media="(prefers-color-scheme: light)">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/styles/github-dark.min.css" media="(prefers-color-scheme: dark)">
<style>
  body {{ margin: 0; background: #fff; }}
  @media (prefers-color-scheme: dark) {{ body {{ background: #0d1117; }} }}
  .markdown-body {{ box-sizing: border-box; max-width: 900px; margin: 0 auto; padding: 24px 16px 64px; }}
  .crumb {{ font-size: 13px; opacity: .6; margin-bottom: 16px; }}
</style></head>
<body><article class="markdown-body">
<div class="crumb"><a href="/">index</a> / {crumb}</div>
<div id="content">Loading…</div>
</article>
<script id="src" type="text/plain">{source}</script>
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@highlightjs/cdn-assets@11/highlight.min.js"></script>
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  mermaid.initialize({{ startOnLoad: false, theme: dark ? "dark" : "default" }});
  const src = document.getElementById("src").textContent;
  const el = document.getElementById("content");
  el.innerHTML = marked.parse(src, {{ gfm: true }});
  el.querySelectorAll("pre code.language-mermaid").forEach(c => {{
    const d = document.createElement("div"); d.className = "mermaid"; d.textContent = c.textContent;
    c.parentElement.replaceWith(d);
  }});
  try {{ el.querySelectorAll("pre code").forEach(c => hljs.highlightElement(c)); }} catch (e) {{ console.error(e); }}
  mermaid.run().catch(console.error);
  // Live reload: poll mtime.
  let mtime = {mtime};
  setInterval(async () => {{
    try {{
      const r = await fetch("/__mtime?p=" + encodeURIComponent(location.pathname));
      const m = await r.json();
      if (m.mtime && m.mtime !== mtime) location.reload();
    }} catch (e) {{}}
  }}, 1500);
</script></body></html>"""

INDEX = """<!doctype html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
<style>
  body {{ margin: 0; background: #fff; }}
  @media (prefers-color-scheme: dark) {{ body {{ background: #0d1117; }} }}
  .markdown-body {{ box-sizing: border-box; max-width: 900px; margin: 0 auto; padding: 24px 16px 64px; }}
</style></head>
<body><article class="markdown-body"><h1>{title}</h1><ul>{items}</ul></article></body></html>"""


def tailscale_info():
    """Return (ipv4, magicdns_name) for this machine, or (None, None)."""
    exe = shutil.which("tailscale") or "/Applications/Tailscale.app/Contents/MacOS/Tailscale"
    try:
        out = subprocess.run([exe, "status", "--json"], capture_output=True, text=True, timeout=5)
        data = json.loads(out.stdout)
        self_ = data.get("Self", {})
        ips = [ip for ip in self_.get("TailscaleIPs", []) if ":" not in ip]
        name = (self_.get("DNSName") or "").rstrip(".") or None
        return (ips[0] if ips else None), name
    except Exception:
        return None, None


def free_port(host, start):
    for port in range(start, start + 50):
        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # match HTTPServer
            try:
                s.bind((host, port))
                return port
            except OSError:
                continue
    sys.exit(f"No free port in {start}-{start + 49}")


def make_handler(root):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=root, **kw)

        def log_message(self, fmt, *args):
            sys.stderr.write(f"{self.client_address[0]} {fmt % args}\n")

        def safe_path(self, url_path):
            """Map URL path to a file under root. None if it escapes root."""
            rel = posixpath.normpath(urllib.parse.unquote(url_path)).lstrip("/")
            full = os.path.realpath(os.path.join(root, rel))
            if full != root and not full.startswith(root + os.sep):
                return None
            return full

        def send_html(self, body, code=200):
            data = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/__mtime":
                p = urllib.parse.parse_qs(parsed.query).get("p", ["/"])[0]
                full = self.safe_path(p)
                mtime = os.path.getmtime(full) if full and os.path.isfile(full) else 0
                body = json.dumps({"mtime": mtime}).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            full = self.safe_path(parsed.path)
            if full is None:
                self.send_error(403)
                return
            if os.path.isdir(full):
                self.send_html(self.render_index(full, parsed.path))
                return
            if os.path.isfile(full) and full.lower().endswith(MD_EXT) and "raw" not in parsed.query:
                self.send_html(self.render_md(full, parsed.path))
                return
            super().do_GET()  # images, raw files, etc.

        def render_md(self, full, url_path):
            with open(full, encoding="utf-8", errors="replace") as f:
                src = f.read()
            # Keep the source inert inside <script type="text/plain">.
            src = src.replace("</script", "<\\/script")
            return PAGE.format(
                title=html.escape(os.path.basename(full)),
                crumb=html.escape(url_path.lstrip("/")),
                source=src,
                mtime=json.dumps(os.path.getmtime(full)),
            )

        def render_index(self, full, url_path):
            base = url_path if url_path.endswith("/") else url_path + "/"
            items = []
            if full != root:
                items.append('<li><a href="../">../</a></li>')
            for dirpath, dirnames, filenames in os.walk(full):
                dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d != "node_modules")
                for name in sorted(filenames):
                    if name.lower().endswith(MD_EXT):
                        rel = os.path.relpath(os.path.join(dirpath, name), full)
                        href = base + urllib.parse.quote(rel.replace(os.sep, "/"))
                        items.append(f'<li><a href="{href}">{html.escape(rel)}</a></li>')
            if len(items) == (0 if full == root else 1):
                items.append("<li><em>No markdown files here.</em></li>")
            title = html.escape(os.path.basename(full) or full)
            return INDEX.format(title=title, items="\n".join(items))

    return Handler


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="markdown file or directory")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--host", help="bind address (default: this machine's Tailscale IPv4)")
    args = ap.parse_args()

    target = os.path.realpath(os.path.expanduser(args.path))
    if not os.path.exists(target):
        sys.exit(f"Not found: {args.path}")
    root = target if os.path.isdir(target) else os.path.dirname(target)
    start = "/" if os.path.isdir(target) else "/" + urllib.parse.quote(os.path.basename(target))

    ts_ip, ts_name = tailscale_info()
    host = args.host or ts_ip
    if not host:
        sys.exit("Tailscale IP not found. Is Tailscale running? (`tailscale up`) Or pass --host.")
    port = free_port(host, args.port)

    server = ThreadingHTTPServer((host, port), make_handler(root))
    print(f"Serving {target}", flush=True)
    if ts_name:
        print(f"  http://{ts_name}:{port}{start}", flush=True)
    short = ts_name.split(".")[0] if ts_name else None
    if short:
        print(f"  http://{short}:{port}{start}", flush=True)
    print(f"  http://{host}:{port}{start}", flush=True)
    print("Ctrl-C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
