import json
import re

INPUT = "finance_dataset_final.json"
OUTPUT = "finance_dataset_clean.json"
REPORT = "removed_samples.json"

BAD_PATTERNS = [
    "J3 SU1S UN3 P0UP33",
    "admin:",
    "password",
    "pass:",
    "api_key",
    "bearer",
    "ssh",
    "vpn",
    "aws",
    "secret",
    "token",
    "docker login",
    "root:",
    "X-Compliance-Token",
]

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

clean = []
removed = []

for item in data:
    text = json.dumps(item, ensure_ascii=False).lower()

    is_bad = any(pattern.lower() in text for pattern in BAD_PATTERNS)

    # garde seulement les samples au bon format
    has_instruction = "instruction" in item
    has_output = "output" in item

    if is_bad or not has_instruction or not has_output:
        removed.append(item)
    else:
        clean.append({
            "instruction": item["instruction"].strip(),
            "input": item.get("input", "").strip(),
            "output": item["output"].strip()
        })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)

with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(removed, f, ensure_ascii=False, indent=2)

print(f"Total initial: {len(data)}")
print(f"Conservés: {len(clean)}")
print(f"Supprimés: {len(removed)}")