"""Check local Markdown links and standalone documentation boundaries."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)\)")
FENCES = re.compile(r"^```[^\n]*\n.*?^```\s*$", re.MULTILINE | re.DOTALL)
PRIVATE_PATH = re.compile(r"/(?:data|home|Users)/[^\s`<>]+")


def check(root: Path) -> list[str]:
    root = root.resolve()
    failures = []
    for path in sorted(root.rglob("*.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        content = path.read_text(encoding="utf-8")
        label = path.relative_to(root)
        if PRIVATE_PATH.search(content):
            failures.append(f"{label}: machine-specific absolute path")
        if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", content):
            failures.append(f"{label}: maintained documentation must be English")
        if any(line.rstrip() != line for line in content.splitlines()):
            failures.append(f"{label}: trailing whitespace")
        for raw in LINK.findall(FENCES.sub("", content)):
            parsed = urlsplit(raw.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith("/"):
                failures.append(f"{label}: absolute local link: {raw}")
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            try:
                target.relative_to(root)
            except ValueError:
                failures.append(f"{label}: link escapes repository: {raw}")
                continue
            if not target.is_file():
                failures.append(f"{label}: missing file target: {raw}")
                continue
            if parsed.fragment and target.suffix == ".md":
                anchors = set()
                counts = {}
                for heading in re.findall(r"^#{1,6}\s+(.+)$", FENCES.sub("", target.read_text()), re.MULTILINE):
                    slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                    index = counts.get(slug, 0)
                    anchors.add(f"{slug}-{index}" if index else slug)
                    counts[slug] = index + 1
                if unquote(parsed.fragment) not in anchors:
                    failures.append(f"{label}: missing heading anchor: {raw}")
    return failures


def main() -> int:
    failures = check(ROOT)
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    if failures:
        return 1
    print("Standalone documentation links and boundaries passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
