"""Check that scenario/data/assets.csv matches the force tables in the team packets.

Usage: python3 tools/check_assets.py
The packets are scenario/<side id>-packet.md, one per [[side]] in game.toml. Exits
non-zero if IDs differ between the packets and the CSV, if a CSV row is missing an asset
name, role, or limitation, if its `side` is not a team's label or its ID doesn't start
with that team's prefix, if its `cell` (optional) is not one of that team's cells, or if
a split counter's `parts` count doesn't match its list of zones (Z8;Z10).
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from game import GAME  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SIDES = {s["label"]: s for s in GAME["side"]}
PACKETS = {s["label"]: ROOT / "scenario" / f"{s['id']}-packet.md" for s in GAME["side"]}
CSV_PATH = ROOT / "scenario" / "data" / "assets.csv"
ROW_ID = re.compile(r"^\|\s*\**([%s]-\d{2})\**\s*\|" % "".join(s["prefix"] for s in GAME["side"]), re.MULTILINE)
REQUIRED = ("asset", "role", "limitation")


def main() -> int:
    problems = []

    packet_ids = {}
    for side, path in PACKETS.items():
        if not path.exists():
            problems.append(f"{path.relative_to(ROOT)}: missing (one packet per [[side]] in game.toml)")
            continue
        for asset_id in ROW_ID.findall(path.read_text(encoding="utf-8")):
            packet_ids[asset_id] = side

    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    csv_ids = {}
    for row in rows:
        asset_id = row["id"]
        if asset_id in csv_ids:
            problems.append(f"{asset_id}: duplicate row in CSV")
        csv_ids[asset_id] = row["side"]
        side = SIDES.get(row["side"])
        if not side:
            problems.append(f"{asset_id}: side '{row['side']}' is not a team label in game.toml ({', '.join(SIDES)})")
        elif not asset_id.startswith(side["prefix"] + "-"):
            problems.append(f"{asset_id}: {side['label']} asset IDs start with {side['prefix']}-")
        cell = (row.get("cell") or "").strip()
        if side and cell and cell not in [c["id"] for c in side["cells"]]:
            problems.append(f"{asset_id}: cell '{cell}' is not one of {side['label']}'s cells in game.toml")
        for field in REQUIRED:
            if not row[field].strip():
                problems.append(f"{asset_id}: empty '{field}' in CSV")
        parts = row.get("parts", "").strip()
        if parts and (not parts.isdigit() or int(parts) < 2):
            problems.append(f"{asset_id}: 'parts' must be blank or 2 or more, not '{parts}'")
        elif row.get("part_asset", "").strip() and not parts:
            problems.append(f"{asset_id}: 'part_asset' is set but 'parts' is blank")
        elif ";" in row["zone"] and len(row["zone"].split(";")) != int(parts or 1):
            problems.append(f"{asset_id}: {len(row['zone'].split(';'))} zones listed but parts is '{parts or 1}'")

    for asset_id in sorted(packet_ids.keys() - csv_ids.keys()):
        problems.append(f"{asset_id}: in {packet_ids[asset_id]} packet but not in CSV")
    for asset_id in sorted(csv_ids.keys() - packet_ids.keys()):
        problems.append(f"{asset_id}: in CSV but not in any packet")
    for asset_id in sorted(packet_ids.keys() & csv_ids.keys()):
        if packet_ids[asset_id] != csv_ids[asset_id]:
            problems.append(f"{asset_id}: side is {csv_ids[asset_id]} in CSV but {packet_ids[asset_id]} in packet")

    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(csv_ids)} assets match across packets and CSV.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
