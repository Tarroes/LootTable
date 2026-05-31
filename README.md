LootTable CLI
=============

Simulate loot drops for tabletop campaigns using weighted rarity tables and seedable runs.

Quick start
-----------

Run a few simulations with the included default table:

```bash
python3 main.py --seed 42 --runs 3 --count 4
```

Options
-------

- `--table, -t`: Path to a table JSON file (default `tables/default_table.json`)
- `--seed, -s`: Integer seed for RNG for reproducible runs
- `--runs, -r`: Number of runs to simulate
- `--count, -c`: Number of drops per run
- `--format, -f`: `text` (default) or `json`
- `--output, -o`: Write output to file (useful with `--format json`)

Table format
------------

The table JSON must contain a top-level `rarities` object. Each rarity is an object with a
`weight` and `items`. `items` may be a list of names or an object mapping item names to weights.

Example (included at `tables/default_table.json`):

```json
{
  "rarities": {
    "Common": { "weight": 60, "items": {"Potion": 10, "Gold Coin": 5, "Dagger": 1} },
    "Uncommon": { "weight": 25, "items": ["Ring", "Scroll"] },
    "Rare": { "weight": 10, "items": {"Gem": 1, "Magic Sword": 1} },
    "Legendary": { "weight": 5, "items": {"Ancient Artifact": 1} }
  }
}
```

License
-------

Public domain. Use and adapt freely.
