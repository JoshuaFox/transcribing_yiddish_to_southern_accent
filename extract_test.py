import json
import re

with open('dictionary_index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = set()
for k, v in data.items():
    for line in v:
        lines.add(line)

# Let's extract
# We want to find: Yiddish text, possibly with punctuation, followed by [transliteration]
# But exclude labels like "דרומדיק:" or "{לומדיש:}"

def extract(text):
    results = []
    # Replace labels
    text = re.sub(r'\{.*?\}', '', text)
    # Split by semicolons or other major delimiters? 
    # Actually, we can just find: (Yiddish words) followed by [trans]
    # Yiddish words: [\u0590-\u05FF]+ optionally separated by spaces or hyphens.
    # To avoid "דרומדיק:", we can explicitly ignore it or strip it.
    
    # A chunk is something like "האָבן צרות פון [tsórəs], דרומדיק: [tsú:rəs]"
    chunks = re.split(r'[;]', text)
    for chunk in chunks:
        # find the main yiddish phrase
        # it's usually at the start of the chunk, ending before the first '['
        m = re.search(r'([א-ת\s\-\'״".,()\\/]+)\[(.*?)\]', chunk)
        if m:
            yid = m.group(1).strip()
            # remove known labels
            yid = re.sub(r'דרומדיק:?', '', yid).strip()
            yid = re.sub(r'צפונדיק:?', '', yid).strip()
            yid = re.sub(r'\(.*?\)', '', yid).strip() # remove (די), etc.
            yid = yid.strip(':,.-/\\| ')
            if yid:
                results.append((yid, m.group(2).strip()))
                
        # What about the dialects?
        for dialect_match in re.finditer(r'(דרומדיק|צפונדיק):\s*\[(.*?)\]', chunk):
            dialect = dialect_match.group(1)
            trans = dialect_match.group(2)
            if m and yid:
                results.append((yid, trans))
                
    return results

for i, line in enumerate(list(lines)[:30]):
    print("LINE:", line)
    print("EXTRACTED:", extract(line))
    print()

