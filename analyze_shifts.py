import json
import re
import datetime

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

# Generate timestamped filename
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"shift_mapping_details_{ts}.txt"

print(f"Found {len(patterns)} explicit SY shift entries.")
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Found {len(patterns)} explicit SY shift entries.\n")
    for p in patterns[:50]:
        line = f"Word: {p[0]} | Std: {p[1]} | SY: {p[2]}"
        print(line)
        f.write(line + "\n")

print(f"Results written to {output_file}")
