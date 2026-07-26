#!/usr/bin/env python3
import argparse
import sys
import re
import os
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

import json

class SYTranscriber:
    def __init__(self, dict_html_path="dictionary.html", index_path="dictionary_index.json"):
        """
        Initializes the transcriber. 
        It uses a cached JSON index if available, otherwise it builds one from dictionary.html.
        """
        self.dict_html_path = dict_html_path
        self.index_path = index_path
        self.word_index = {}
        
        self._load_index()

        # Initialize Vertex AI Gemini Client
        try:
            # Using defaults for project and location to see if it resolves 404
            self.client = genai.Client(vertexai=True)
        except Exception as e:
            print(f"Warning: Could not initialize Vertex AI Gemini client: {e}. Transcription will fail.", file=sys.stderr)
            self.client = None


    def normalize_yiddish(self, text):
        """
        Normalizes Yiddish text to a 'base' form to bridge orthographic gaps:
        1. Decomposes ligatures (װ -> וו, ײ -> יי, ײַ -> יי).
        2. Removes all nikkud (diacritics).
        3. Standardizes special characters.
        """
        if not text: return ""
        # Decompose ligatures
        text = text.replace('װ', 'וו').replace('ײ', 'יי').replace('ײַ', 'יי').replace('ייִ', 'יי')
        # Remove all Hebrew/Yiddish diacritics (U+0591 to U+05C7)
        text = re.sub(r'[\u0591-\u05C7]', '', text)
        # Remove punctuation/formatting that interferes with lookup
        text = re.sub(r'[־\-\'\"]', '', text)
        return text.strip()

    def _load_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.word_index = json.load(f)
            return

        if not os.path.exists(self.dict_html_path):
            print(f"Warning: {self.dict_html_path} not found. Cannot build index.", file=sys.stderr)
            return

        print(f"Building index from {self.dict_html_path}... this may take a moment.", file=sys.stderr)
        with open(self.dict_html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            paragraphs = soup.find_all('p')
            
        for p in paragraphs:
            p_text = p.get_text().strip()
            if not p_text: continue
            
            # Extract potential Yiddish words using Hebrew script range
            yiddish_words = set(re.findall(r"[\u0590-\u05FF]+", p_text))
            for word in yiddish_words:
                norm_word = self.normalize_yiddish(word)
                if len(norm_word) < 2: continue
                
                if norm_word not in self.word_index:
                    self.word_index[norm_word] = []
                
                if '[' in p_text and ']' in p_text:
                    if p_text not in self.word_index[norm_word]:
                        self.word_index[norm_word].append(p_text)

        # Optimization: Sort and limit
        for word in self.word_index:
            self.word_index[word].sort(key=lambda x: ("דרומדיק" not in x, len(x)))
            self.word_index[word] = list(dict.fromkeys(self.word_index[word]))[:3]

        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.word_index, f, ensure_ascii=False, indent=2)
        print(f"Index built and saved to {self.index_path}", file=sys.stderr)

    def get_context_for_text(self, text):
        """
        Quickly extracts relevant dictionary entries using the normalized index.
        Includes basic suffix-stripping to find roots for inflected words.
        """
        tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4\u05BE]+", text)
        contexts = {}
        
        # Common Yiddish suffixes to strip for stemming
        suffixes = ['ענער', 'ענע', 'ער', 'ען', 'עס', 'נע', 'ע', 'ן', 'ס']
        
        for token in tokens:
            norm_word = self.normalize_yiddish(token)
            
            # 1. Try exact match
            if norm_word in self.word_index and self.word_index[norm_word]:
                contexts[norm_word] = self.word_index[norm_word]
                continue
            
            # 2. Try stemming (suffix stripping)
            for suffix in suffixes:
                if norm_word.endswith(suffix) and len(norm_word) > len(suffix) + 1:
                    stem = norm_word[:-len(suffix)]
                    if stem in self.word_index and self.word_index[stem]:
                        # Store context under the original word for the LLM
                        contexts[norm_word] = self.word_index[stem]
                        break
                
        return contexts

    def transcribe(self, text, explain=False):
        if not self.client:
            print("ERROR: Gemini Client not initialized. Cannot transcribe.", file=sys.stderr)
            return
            
        contexts = self.get_context_for_text(text)
        
        context_str = ""
        for word, ctx_list in contexts.items():
            context_str += f"Word '{word}':\n"
            for c in ctx_list:
                context_str += f" - {c}\n"
            context_str += "\n"

        if explain:
            prompt = f"""
You are an expert in Yiddish dialectology, specifically South Yiddish (SY) as represented in the Yiddish Cultural Dictionary (yiddishculturaldictionary.org).
For every word in the following text, provide:
1. Hebrew orthography (the Yiddish word).
2. The transcription in SY phonetic orthography.
3. A detailed explanation of the transcription in ENGLISH.

Use these categories for explanation:
(a) Exact lookup in the provided dictionary context.
(b) Inferred from the dictionary by applying patterns seen in similar words (e.g., words with same etymological roots).
(c) General Southern Yiddish sound shift rules (see guide below).
(d) Context-specific rules (e.g., proper names, loanwords).

SOUND SHIFT GUIDE (Standard Orthography -> SY):
- Standard [o] (אָ) -> SY [u] (e.g., 'hot' -> 'hut', 'sof' -> 'suf'). Note: In some closed syllables or Semitic words, it may be long [u:].
- Standard [u] (ו) -> SY [i] or [i:] (e.g., 'fun' -> 'fin', 'shul' -> 'shi:l').
- Standard [ey] (יי) -> SY [ay] (e.g., 'geyn' -> 'gayn').
- Standard [oy] (וי) -> SY [u:] (e.g., 'boykh' -> 'bu:kh', 'koyl' -> 'ku:l').
- Standard [e] (ע) -> In SY, this often lengthens to [ey] before voiced consonants or in certain open syllables (e.g., 'mentsh' -> 'meyntsh').
- Standard [ay] (ײַ) -> Stays [ay] in SY (unlike Northern [ey]).

RESOLVING AMBIGUITY:
Standard Yiddish orthography is often the same for different historical vowels.
1. Use the Context: If the word or a close relative is in the Context, follow that transcription EXACTLY.
2. Etymological Clues: Semitic words (Loshn Koydesh) often have distinct SY shifts for vowels that look the same as Germanic ones in standard orthography (e.g., Vowel 42 vs 44).
3. Dialect Consistency: Southern Yiddish (Central Yiddish) is generally characterized by the "U for O" and "I for U" shifts.

Context from dictionary:
{context_str}

Text to transcribe:
{text}

Output as a formatted table or list. All explanations MUST be in English.
"""
        else:
            prompt = f"""
You are an expert in Yiddish dialectology, specifically South Yiddish (SY) as represented in the Yiddish Cultural Dictionary (yiddishculturaldictionary.org).
Your task is to transcribe the given Yiddish text into South Yiddish phonetic orthography.

GUIDELINES:
1. Use the phonetic orthography rules and formats exactly as demonstrated in the context entries.
2. For words explicitly found in the context with a "דרומדיק: [...]" entry, use that transcription.
3. For words NOT in the context, apply general South Yiddish (SY) vowel shifts:
   - Standard [ey] -> SY [ay] (e.g., geyn -> gayn, həfkéyrəs -> həfkáyrəs)
   - Standard [oy] -> SY [u:] or [u] (e.g., boykh -> bu:kh, kóyl -> kú:l)
   - Standard [u] -> SY [i] or [i:] (e.g., takhnúnəm -> takhní:nəm, gút -> gít)
   - Standard [o] -> SY [u] (e.g., akhlótə -> akhlú:tə, sóf -> súf)
   - Standard [i] -> SY [e] or [ey] in some contexts, but often remains [i].
4. Transcription style:
   - Use 'sh', 'ts', 'kh', 'e', 'a', 'i', 'u', 'y'.
   - Use colons for long vowels (e.g., [i:], [u:]).
   - Use dashes for compound words.
   - OPTIONAL SOUNDS: Where the dictionary shows optional sounds in parentheses (e.g., [gətí:(ə)n], [shó:(ə)l]), use the SHORT FORM by omitting the parenthetical sound (e.g., [gətí:n], [shó:l]).
   - Preserve punctuation and capitalization of names.
   - Return ONLY the transcription in brackets.

Context from dictionary:
{context_str}

Text to transcribe:
{text}

Return ONLY the phonetic transcription in brackets, preserving punctuation. Do not output conversational filler.
"""
        
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            result = response.text.strip()
            print(result)
            return result
        except Exception as e:
            print(f"Error during transcription: {e}", file=sys.stderr)
            return None

def parse_multilanguage_file(file_path):
    """
    Parses a file containing triplets: English, Yiddish, and a transcription.
    Returns a list of the Yiddish strings (the second line of each triplet).
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    yiddish_texts = []
    # Data comes in triplets
    for i in range(0, len(lines), 3):
        if i + 1 < len(lines):
            yiddish_texts.append(lines[i+1])
    return yiddish_texts

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe Yiddish to South Yiddish (SY)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', type=str, help="Text to transcribe")
    group.add_argument('-f', '--file', type=str, help="File containing pure Yiddish text")
    group.add_argument('--multilanguage-file', type=str, help="File with English/Yiddish/Transcription triplets")
    parser.add_argument('-e', '--explain', action='store_true', help="Enable explanation mode")
    
    args = parser.parse_args()
    
    transcriber = SYTranscriber()
    
    if args.multilanguage_file:
        yiddish_lines = parse_multilanguage_file(args.multilanguage_file)
        for line in yiddish_lines:
            transcriber.transcribe(line, explain=args.explain)
            print("-" * 20)
    else:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                input_text = f.read()
        else:
            input_text = args.text
        
        transcriber.transcribe(input_text, explain=args.explain)
