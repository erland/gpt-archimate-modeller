#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from identity import next_id, load_counters, save_counters

def main():
    if len(sys.argv) != 3:
        print("Usage: allocate_id.py <id-counters.yaml> <PREFIX>")
        return 2
    path = Path(sys.argv[1])
    prefix = sys.argv[2].upper()
    data = load_counters(path)
    counters = data.setdefault("counters", {})
    if prefix not in counters:
        print(f"Unknown prefix: {prefix}")
        return 1
    new_id = next_id(counters, prefix)
    save_counters(path, data)
    print(new_id)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
