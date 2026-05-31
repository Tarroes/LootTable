#!/usr/bin/env python3
"""LootTable CLI

Simulates loot drops with weighted rarity tables and seedable runs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def weighted_choice(rng, choices: Iterable[Tuple[Any, float]]):
	"""Return a single element chosen from choices where each is (value,weight)."""
	elems = []
	cum = []
	total = 0.0
	for value, weight in choices:
		if weight <= 0:
			continue
		elems.append(value)
		total += float(weight)
		cum.append(total)
	if not elems:
		raise ValueError("No choices with positive weight")
	r = rng.random() * total
	for i, c in enumerate(cum):
		if r < c:
			return elems[i]
	return elems[-1]


def load_table(path: Path) -> Dict[str, Any]:
	data = json.loads(path.read_text(encoding="utf8"))
	if "rarities" not in data:
		raise ValueError("Table JSON must contain a top-level 'rarities' object")
	return data


def simulate_once(rng, table: Dict[str, Any], count: int = 1) -> List[Dict[str, str]]:
	rarities = table["rarities"]
	rarity_choices = [(name, info.get("weight", 1)) for name, info in rarities.items()]
	drops = []
	for _ in range(count):
		rarity_name = weighted_choice(rng, rarity_choices)
		items = rarities[rarity_name].get("items", {})
		if isinstance(items, dict):
			item_choices = [(iname, iinfo.get("weight", 1) if isinstance(iinfo, dict) else 1)
							for iname, iinfo in items.items()]
		elif isinstance(items, list):
			item_choices = [(iname, 1) for iname in items]
		else:
			raise ValueError("'items' must be an object or list")
		item = weighted_choice(rng, item_choices)
		drops.append({"rarity": rarity_name, "item": item})
	return drops


def run(args: argparse.Namespace) -> int:
	rng = __import__("random").Random(args.seed)
	table_path = Path(args.table)
	if not table_path.exists():
		print(f"Table file not found: {table_path}", file=sys.stderr)
		return 2
	table = load_table(table_path)

	results = []
	for i in range(args.runs):
		drops = simulate_once(rng, table, count=args.count)
		entry = {"run": i + 1, "drops": drops}
		results.append(entry)

	if args.format == "json":
		out = json.dumps(results, indent=2)
		if args.output:
			Path(args.output).write_text(out, encoding="utf8")
		else:
			print(out)
	else:
		for entry in results:
			print(f"Run {entry['run']}: ")
			for d in entry["drops"]:
				print(f"  - {d['item']} ({d['rarity']})")
			print()

	return 0


def build_parser() -> argparse.ArgumentParser:
	p = argparse.ArgumentParser(prog="loottable", description="Simulate loot drops from weighted rarity tables")
	p.add_argument("--table", "-t", default="tables/default_table.json", help="Path to table JSON")
	p.add_argument("--seed", "-s", type=int, default=None, help="Seed for RNG (int). If omitted, uses system randomness")
	p.add_argument("--runs", "-r", type=int, default=1, help="Number of simulated runs")
	p.add_argument("--count", "-c", type=int, default=1, help="Number of drops per run")
	p.add_argument("--format", "-f", choices=("text", "json"), default="text", help="Output format")
	p.add_argument("--output", "-o", help="Write output to file (JSON only when used with --format json)")
	return p


def main(argv: List[str] | None = None) -> int:
	parser = build_parser()
	args = parser.parse_args(argv)
	return run(args)


if __name__ == "__main__":
	raise SystemExit(main())

