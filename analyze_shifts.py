import json
import re

with open("dictionary_index.json", "r", encoding="utf-8") as f:
    index = json.load(f)

# Sample some entries and look for patterns
patterns = []
for word, entries in index.items():
    for entry in entries:
        # Look for [standard] and דרומדיק: [sy]
        # Example: "סוף יאָר [sòf-yór], דרומדיק: [(sòf-yú:ə(r]."
        match = re.search(r"\[([^\]]+)\].*?דרומדיק:\s*\[([^\]]+)\]", entry)
        if match:
            std, sy = match.groups()
            patterns.append((word, std, sy))

# Print a subset of interesting ones
print(f"Found {len(patterns)} explicit SY shift entries.")
for p in patterns[:50]:
    print(f"Word: {p[0]} | Std: {p[1]} | SY: {p[2]}")
