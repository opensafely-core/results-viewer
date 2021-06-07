import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(loader=PackageLoader("osview"), autoescape=select_autoescape())


def render(ctx, template="workspace.html"):
    tmpl = env.get_template(template)
    return tmpl.render(ctx)


def csv_to_html(path, urlpath):
    html_path = path.with_suffix(".html")
    html_urlpath = urlpath.with_suffix(".html")

    limit = 100
    i = 0

    def islice(iterator):
        nonlocal i
        while i < limit:
            try:
                yield next(iterator)
            except StopIteration:
                return
            i += 1

    with path.open() as f:
        rows = csv.reader(f)
        headers = next(rows)
        html = render(dict(rows=islice(rows), headers=headers), "table.html")

    truncated = i == limit
    html_path.write_text(html)

    return html_urlpath, truncated


def parse_files(manifest, workspace):
    # merge file list into specific actions
    actions = manifest["actions"]
    for action_name, action in actions.items():
        action_log = f"metadata/{action_name}.log"
        log_path = workspace / action_log
        action["files"] = {
            action_log: { 
                "path": action_log,
                "type": "log",
                "exists": log_path.exists(),
                "filesize": log_path.stat().st_size if log_path.exists() else 0,
                "classes": ["action_log", "log"],
            }
        }

    for name, data in manifest["files"].items():
        created_by_action = data["created_by_action"]
        path = workspace / name

        data["path"] = path
        data["type"] = path.suffixes[0].lstrip(".")
        data["classes"] = [data["type"]]

        if path.exists():
            data["exists"] = True
            data["filesize"] = path.stat().st_size

            # build preview
            if data["type"] == "csv":
                html, truncated = csv_to_html(path, Path(name))
                data["html"] = html
                data["truncated"] = truncated
        else:
            data["exists"] = False
            data["filesize"] = 0
            data["classes"].append("not-exist")

        actions[created_by_action]["files"][name] = data

    manifest["current_time"] = str(datetime.utcnow())


def main(argv=sys.argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "workspace",
        nargs="?",
        default=Path(os.getcwd()),
        type=Path,
        help="workspace directory to use",
    )
    args = parser.parse_args()
    print(args.workspace)

    manifest_path = args.workspace / "metadata" / "manifest.json"

    if not manifest_path.exists():
        sys.exit(f"{manifest_path} does not exist")

    try:
        manifest = json.loads(manifest_path.read_bytes())
    except Exception as exc:
        sys.exit(f"Could not read json from {manifest_path}: {exc}")

    parse_files(manifest, args.workspace)
    html = render(manifest)

    html_path = args.workspace / "index.html"
    html_path.write_text(html)
