import os
import re
import sys
import json
import argparse
from sy_transcriber import SYTranscriber
from google.genai import types

class TechniqueTester:
    def __init__(self):
        self.transcriber = SYTranscriber()
        # Expanded mapping for naive hardcoded rules to cover all Yiddish letters
        self.rules = {
            # Vowels (Standard -> SY shifts)
            'אָ': 'u', 'אַ': 'a', 'ו': 'i', 'י': 'i', 'יי': 'ay', 'וי': 'u:',
            'ע': 'e', 'ײַ': 'ay', 'וּ': 'i', 'יִ': 'i',
            # Consonants
            'א': '', 'ב': 'b', 'בֿ': 'v', 'ג': 'g', 'ד': 'd', 'ה': 'h', 
            'װ': 'v', 'ז': 'z', 'זש': 'zh', 'ח': 'kh', 'ט': 't', 
            'כּ': 'k', 'כ': 'kh', 'ך': 'kh', 'ל': 'l', 'מ': 'm', 'ם': 'm',
            'נ': 'n', 'ן': 'n', 'ס': 's', 'פּ': 'p', 'פֿ': 'f',
            'פ': 'f', 'ף': 'f', 'צ': 'ts', 'ץ': 'ts', 'ק': 'k', 'ר': 'r',
            'ש': 'sh', 'שׂ': 's', 'תּ': 't', 'ת': 's', '־': '-', ' ': ' '
        }

    def hardcoded_rules(self, word):
        """Technique 1: Naive letter-to-sound mapping. Strips remaining Hebrew."""
        # Decompose ligatures first
        word = word.replace('װ', 'וו').replace('ױ', 'וי').replace('ײ', 'יי')
        res = ""
        i = 0
        while i < len(word):
            found = False
            # Try 2-char matches (with nikud)
            if i + 1 < len(word) and word[i:i+2] in self.rules:
                res += self.rules[word[i:i+2]]
                i += 2
                found = True
            elif word[i] in self.rules:
                res += self.rules[word[i]]
                i += 1
                found = True
            
            if not found:
                # If still a Hebrew char, skip it to avoid leaks
                if not ('\u0590' <= word[i] <= '\u05FF'):
                    res += word[i]
                i += 1
        return res

    def dictionary_lookup(self, word):
        """Technique 2: Search for explicit דרומדיק entry."""
        norm = self.transcriber.normalize_yiddish(word)
        if norm in self.transcriber.word_index:
            for entry in self.transcriber.word_index[norm]:
                match = re.search(r"דרומדיק:\s*\[([^\]]+)\]", entry)
                if match: return match.group(1)
        return "N/A"

    def llm_standalone(self, word, sentence_context):
        """Technique 3: LLM transcription WITHOUT Sat focus. Latin characters only."""
        prompt = f"""
Transcribe this Yiddish word into South Yiddish (SY) Latin-based phonetic orthography.
CRITICAL: Use ONLY Latin characters (a-z) and punctuation. Do NOT return Yiddish/Hebrew characters.

Context: {sentence_context}
Word: {word}

Return ONLY the transcription in brackets [transcription].
"""
        try:
            response = self.transcriber.client.models.generate_content(
                model='gemini-3.6-flash', contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            m = re.search(r"\[([^\]]+)\]", response.text)
            out = m.group(1) if m else response.text.strip()
            # Final safety strip of Hebrew chars
            return re.sub(r'[\u0590-\u05FF]', '', out)
        except: return "Error"

    def llm_sat_informed(self, word, sentence_context, sat_ref):
        """Technique 4: LLM transcription WITH Sat reference focus. Latin characters only."""
        prompt = f"""
Transcribe this Yiddish word into South Yiddish (SY) Latin-based phonetic orthography.
Use the reference transcription ('Sat') to help inform dialectal details.
CRITICAL: Use ONLY Latin characters (a-z) and punctuation. Do NOT return Yiddish/Hebrew characters.

Yiddish Context: {sentence_context}
Sat Reference: {sat_ref}
Word to transcribe: {word}

Return ONLY the transcription in brackets [transcription].
"""
        try:
            response = self.transcriber.client.models.generate_content(
                model='gemini-3.6-flash', contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            m = re.search(r"\[([^\]]+)\]", response.text)
            out = m.group(1) if m else response.text.strip()
            # Final safety strip of Hebrew chars
            return re.sub(r'[\u0590-\u05FF]', '', out)
        except: return "Error"

def parse_input(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    triplets = []
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            triplets.append({'eng': lines[i], 'yid': lines[i+1], 'sat': lines[i+2]})
    return triplets

def main():
    tester = TechniqueTester()
    input_file = "EnglishOysyesGalkhes.txt"
    triplets = parse_input(input_file)
    
    # Process first paragraph for the table
    target = triplets[0]
    print(f"\nProcessing: {target['yid']}")
    print(f"Sat Reference: {target['sat']}\n")
    
    tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4\u05BE]+", target['yid'])
    
    col_w = 15
    header = f"| {'Yiddish':<10} | {'1. Rules':<{col_w}} | {'2. Dict':<{col_w}} | {'3. LLM-Plain':<{col_w}} | {'4. LLM-Sat':<{col_w}} |"
    sep = "|" + "-"*12 + "|" + ("-"*(col_w+2) + "|") * 4
    print(header)
    print(sep)

    for token in tokens:
        t1 = tester.hardcoded_rules(token)
        t2 = tester.dictionary_lookup(token)
        t3 = tester.llm_standalone(token, target['yid'])
        t4 = tester.llm_sat_informed(token, target['yid'], target['sat'])
        
        print(f"| {token:<10} | {t1:<{col_w}} | {t2:<{col_w}} | {t3:<{col_w}} | {t4:<{col_w}} |")

if __name__ == "__main__":
    main()
