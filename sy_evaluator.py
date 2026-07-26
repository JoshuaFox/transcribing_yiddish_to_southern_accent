import sys
import os
import re
import json
from sy_transcriber import SYTranscriber

def parse_input_file(file_path):
    """
    Parses the EnglishOysyesGalkhes.txt file.
    Assumes repeating triplets: English, Yiddish, Galkhes Transcription.
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    triplets = []
    for i in range(0, len(lines), 3):
        if i+2 < len(lines):
            triplets.append({
                'english': lines[i],
                'yiddish': lines[i+1],
                'galkhes': lines[i+2]
            })
    return triplets

def convert_galkhes_to_ycd(text):
    """
    Converts purely orthographic/IPA symbols to the YCD transcription style.
    """
    replacements = {
        'ʃ': 'sh', 'ʒ': 'zh', 'tʃ': 'tsh', 'dʒ': 'dzh', 'x': 'kh',
        'j': 'y', 'ɪ': 'i', 'ʊ': 'u', 'ɛ': 'e', 'ɔ': 'o', 'ŋ': 'ng', 'ː': ':'
    }
    for k in sorted(replacements.keys(), key=len, reverse=True):
        text = text.replace(k, replacements[k])
    return text

def get_sy_transcription(transcriber, text):
    out = transcriber.transcribe(text)
    if not out: return ""
    match = re.search(r'\[(.*?)\]', out, re.DOTALL)
    return match.group(1) if match else out

def self_correct_sy(yiddish, initial_sy, sat_ycd, transcriber):
    """
    Compares the generated SY to Sat and corrects errors in SY.
    Returns the corrected SY and a string describing changes.
    """
    prompt = f"""
You are an expert editor of Yiddish dialectal transcriptions.
We have an initial Southern Yiddish (SY) transcription generated from a dictionary, and a reference transcription ('Sat') from another source.

Yiddish Text: {yiddish}
Initial SY: {initial_sy}
Sat Reference (normalized): {sat_ycd}

TASK:
1. Identify errors in 'Initial SY' by comparing it to 'Sat Reference' and the original Yiddish. 
2. 'Sat' may have more accurate lexical pronunciations or specific dialectal details that 'SY' missed or hallucinated.
3. However, 'Initial SY' is based on the Yiddish Cultural Dictionary. Only correct 'SY' if 'Sat' provides a clearly superior or more traditional Southern Yiddish realization for that specific word/context.
4. If a word in SY was generated correctly but is different from Sat, keep SY.
5. If SY has a clear error (missed shift, wrong vowel, hallucination), correct it to the version suggested by 'Sat' or the underlying rules.

Return the corrected transcription in brackets [CORRECTED_TEXT].
Following the brackets, list each specific correction made and why (in English).
"""
    try:
        response = transcriber.client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt
        )
        full_text = response.text.strip()
        match = re.search(r'\[(.*?)\]', full_text, re.DOTALL)
        corrected = match.group(1) if match else initial_sy
        changes = full_text.split(']', 1)[1].strip() if ']' in full_text else "No changes detected."
        return corrected, changes
    except Exception as e:
        return initial_sy, f"Error in correction: {e}"

def analyze_differences(yiddish, sat_ipa, sat_ycd, sy, transcriber):
    prompt = f"""
Analyze the differences between two phonetic transcriptions of the following Yiddish text.
'Sat' is the existing transcription.
'SY' is the final, corrected Southern Yiddish transcription.

Yiddish Text: {yiddish}
Sat (SY Style): {sat_ycd}
SY (Final): {sy}

TASK:
1. Explain genuine phonetic/dialectal differences between Sat and SY.
2. Identify rule-breaking cases or lexical variations.
Output as a word-by-word table in English.
"""
    try:
        response = transcriber.client.models.generate_content(model='gemini-3.6-flash', contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error in analysis: {e}"

def main():
    input_file = "EnglishOysyesGalkhes.txt"
    output_interleaved = "EnglishOysyesGalkhes_SY.txt"
    output_analysis = "Transcription_Analysis.md"
    max_paragraphs = 3 # Small sample for demo
    
    transcriber = SYTranscriber()
    triplets = parse_input_file(input_file)[:max_paragraphs]
    
    full_output, analysis_results = [], []
    
    for i, triplet in enumerate(triplets):
        print(f"--- Processing Paragraph {i+1} ---")
        initial_sy = get_sy_transcription(transcriber, triplet['yiddish'])
        sat_ycd = convert_galkhes_to_ycd(triplet['galkhes'])
        
        print(f"Correction Phase for P{i+1}...")
        final_sy, corrections = self_correct_sy(triplet['yiddish'], initial_sy, sat_ycd, transcriber)
        
        if corrections and "No changes" not in corrections:
            print(f"CORRECTIONS MADE:\n{corrections}\n")
        else:
            print("No corrections needed.\n")

        # Interleaved Output (5 lines per paragraph)
        full_output.extend([
            f"Eng: {triplet['english']}",
            f"Yid: {triplet['yiddish']}",
            f"Sat (IPA): {triplet['galkhes']}",
            f"Sat (SY Style): {sat_ycd}",
            f"SY: {final_sy}",
            ""
        ])
        
        print("Final Analysis...")
        analysis = analyze_differences(triplet['yiddish'], triplet['galkhes'], sat_ycd, final_sy, transcriber)
        analysis_results.append(f"## Paragraph {i+1}\n\n{analysis}\n\n---\n")

    with open(output_interleaved, 'w', encoding='utf-8') as f:
        f.write("\n".join(full_output))
    with open(output_analysis, 'w', encoding='utf-8') as f:
        f.write("\n".join(analysis_results))
    print(f"Done! Interleaved: {output_interleaved}, Analysis: {output_analysis}")

if __name__ == "__main__":
    main()
