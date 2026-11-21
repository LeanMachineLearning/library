#!/usr/bin/env python3
"""The roadmaps of LMLRoadmaps, as the plans the library site reads (evidence-core's `context`).

  python3 scripts/roadmaps.py --roadmaps LMLRoadmaps --out plans.json [--commit SHA]

Each roadmap is a directory of LMLRoadmaps/ with a README.md in the form the lml-roadmap skill sets:
a title (`# Roadmap: …`), an overview before the first section, then `## Layer N: Title` sections
of numbered items, each opening with its title in bold (`1. **Tracking.** …`). An item is named as
the roadmaps and the literature annotations name it: `<directory> <layer>.<number>`
(`Identification 5.2`). Writes a JSON list: {id, title, scope, url, layers: [{n, title, items:
[{id, title, text}]}]}.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TITLE = re.compile(r"^#\s+(?:Roadmap:\s*)?(.+?)\s*$")
LAYER = re.compile(r"^##\s+Layer\s+(\d+)\s*:\s*(.+?)\s*$")
SECTION = re.compile(r"^##\s+")
ITEM = re.compile(r"^(\d+)\.\s+\*\*(.+?)\*\*\s*(.*)$")


def parse(area: str, text: str) -> dict:
    lines = text.split("\n")
    title, scope, layers = area, [], []
    i = 0
    if lines and (m := TITLE.match(lines[0])):
        title, i = m.group(1), 1
    while i < len(lines) and not SECTION.match(lines[i]):
        scope.append(lines[i])
        i += 1
    layer = item = None
    for line in lines[i:]:
        if m := LAYER.match(line):
            layer = {"n": int(m.group(1)), "title": m.group(2), "items": []}
            layers.append(layer)
            item = None
        elif SECTION.match(line):
            layer = item = None
        elif layer is not None and (m := ITEM.match(line)):
            item = {"id": f"{area} {layer['n']}.{m.group(1)}", "title": m.group(2).rstrip(".").strip(),
                    "text": m.group(3)}
            layer["items"].append(item)
        elif item is not None:
            item["text"] += "\n" + line
    for layer in layers:
        for it in layer["items"]:
            it["text"] = re.sub(r"\n{3,}", "\n\n", "\n".join(l[3:] if l.startswith("   ") else l
                                                            for l in it["text"].split("\n"))).strip()
    return {"id": area, "title": title, "scope": "\n".join(scope).strip(), "layers": layers}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--roadmaps", type=Path, required=True, help="a checkout of LeanMachineLearning/LMLRoadmaps")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--commit", default="main", help="the checkout's commit, for links to the roadmaps")
    args = p.parse_args()
    base = args.roadmaps / "LMLRoadmaps"
    plans = []
    for readme in sorted(base.glob("*/README.md")):
        plan = parse(readme.parent.name, readme.read_text(encoding="utf-8"))
        plan["url"] = f"https://github.com/LeanMachineLearning/LMLRoadmaps/blob/{args.commit}/LMLRoadmaps/{readme.parent.name}/README.md"
        plans.append(plan)
    args.out.write_text(json.dumps(plans, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    items = sum(len(l["items"]) for r in plans for l in r["layers"])
    print(f"roadmaps: {len(plans)} roadmaps, {items} items → {args.out}")
    return 0 if plans else 1


if __name__ == "__main__":
    sys.exit(main())
