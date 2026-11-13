"""Check the Codex marketplace and plugin files before a release (run by CI and by hand: python scripts/validate.py)."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
problems = []


def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        problems.append(f"{path}: {error}")
        return {}


market = load(".agents/plugins/marketplace.json")
for key in ("name", "plugins"):
    if key not in market:
        problems.append(f".agents/plugins/marketplace.json: missing {key}")
for entry in market.get("plugins", []):
    source = (entry.get("source") or {}).get("path", "")
    if ".." in source or not (ROOT / source).is_dir():
        problems.append(f"marketplace plugin {entry.get('name')}: source path {source!r} is not a folder in this repo")
        continue
    folder = pathlib.Path(source)
    manifest = load(folder / "plugin.json")
    if manifest.get("name") != entry.get("name"):
        problems.append(f"{source}: plugin.json name {manifest.get('name')!r} differs from the marketplace entry {entry.get('name')!r}")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(manifest.get("name", ""))):
        problems.append(f"{source}: plugin name must be kebab-case")
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
        problems.append(f"{source}: plugin.json version must look like 1.2.3")
    interface = ((manifest.get("extensions") or {}).get("com.openai") or {}).get("interface") or {}
    for key in ("composerIcon", "logo"):
        path = interface.get(key)
        if path and (not str(path).startswith("./") or not (ROOT / folder / path).is_file()):
            problems.append(f"{source}: interface.{key} {path!r} must be a ./ path to a file in the plugin")
    for name, server in load(folder / "mcp.json").get("mcpServers", {}).items():
        if not str(server.get("url", "")).startswith("https://"):
            problems.append(f"{source}/mcp.json: server {name} must use an https:// URL")
        if "Authorization" in json.dumps(server) or "pf_" in json.dumps(server):
            problems.append(f"{source}/mcp.json: server {name} must not carry credentials")
    for skill in (ROOT / folder / "skills").glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match or not re.search(r"^name:\s*\S", match.group(1), re.M) or not re.search(r"^description:\s*\S", match.group(1), re.M):
            problems.append(f"{skill.relative_to(ROOT)}: frontmatter needs name and description")
        elif re.search(r"^name:\s*(\S+)", match.group(1), re.M).group(1) != skill.parent.name:
            problems.append(f"{skill.relative_to(ROOT)}: name should match its folder")

if problems:
    print("\n".join("FAIL " + p for p in problems))
    sys.exit(1)
print("ok: marketplace, plugin manifest, MCP server and skills")
