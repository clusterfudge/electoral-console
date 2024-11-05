#!/usr/bin/env python3
import json
from pathlib import Path


def assemble_results():
    base_dir = Path("scrapers")
    result = {"states": {}}

    # Walk through all state directories
    for state_dir in base_dir.iterdir():
        if not state_dir.is_dir():
            continue

        latest_file = state_dir / "latest.json"
        if latest_file.exists():
            try:
                with open(latest_file, "r") as f:
                    state_data = json.load(f)
                    state_name = state_dir.name.replace("_", " ")
                    result["states"][state_name] = state_data
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {latest_file}")
                continue

    # Write assembled results
    with open("current_results.json", "w") as f:
        json.dump(result, f, indent=2)


if __name__ == "__main__":
    assemble_results()
