import os
import re
import sys
import datetime
import json
from sy_transcriber import SYTranscriber
from google.genai import types

def get_timestamped_filename(base, ext):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{ts}{ext}"

def check_lookup():
    # Initialize transcriber (uses Vertex AI via default credentials)
    transcriber = SYTranscriber()
    input_file = "EnglishOysyesGalkhes.txt"
    output_file = get_timestamped_filename("check_dict_lookup", ".txt")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    triplets = []
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            triplets.append({
                'eng': lines[i], 
                'yid': lines[i+1], 
                'sat': lines[i+2]
            })
    
    report = ["### Dictionary Lookup Failure Analysis ###\n"]
    
    # Process tokens and verify dictionary plausibility
    for triplet in triplets:
        yid_text = triplet['yid']
        sat_text = triplet['sat']
        
        # This will trigger the cached LLM filtering for the whole paragraph at once
        transcriber.get_context_for_text(yid_text)
        
        tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4\u05BE]+", yid_text)
        
        for token in tokens:
            # Check if we have filtered (relevant) entries in the cache for this word
            relevant_entries = []
            if hasattr(transcriber, '_context_cache') and token in transcriber._context_cache:
                relevant_entries = transcriber._context_cache[token]
            
            if not relevant_entries:
                continue
                
            for raw_entry in relevant_entries:
                # Extract the דרומדיק (SY) result from the entry
                sy_result = None
                match = re.search(r"דרומדיק:\s*\[([^\]]+)\]", raw_entry)
                if match:
                    sy_result = match.group(1)
                
                if not sy_result:
                    continue
                
                prompt = f"""
Analyze the quality of a dictionary lookup for Yiddish to South Yiddish (SY) transcription.

Word: {token}
Dictionary Entry Found: {raw_entry}
Extracted SY from Dictionary: {sy_result}
Sentence Context: {yid_text}
Sat Reference (Gold Standard Hint): {sat_text}

TASK:
1. Determine if 'Extracted SY' is a plausible transcription for '{token}' in this context.
2. If it is WRONG, explain WHY.

Output format:
PLAUSIBILITY: [YES/NO]
ANALYSIS: [Short explanation]
"""
                try:
                    response = transcriber.client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.1)
                    )
                    analysis = response.text.strip()
                    if "PLAUSIBILITY: NO" in analysis:
                        entry_report = (
                            f"Word: {token}\n"
                            f"Lookup Result: {sy_result}\n"
                            f"Raw Entry: {raw_entry}\n"
                            f"{analysis}\n"
                            f"{'-'*40}\n"
                        )
                        report.append(entry_report)
                        print(f"Detected failure for word: {token}")
                except Exception as e:
                    print(f"Error analyzing '{token}': {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    print(f"\nAnalysis complete. Results written to: {output_file}")

if __name__ == "__main__":
    check_lookup()
