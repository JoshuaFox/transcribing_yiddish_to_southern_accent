import os
import sys
import json
import re
import argparse
import datetime
from bs4 import BeautifulSoup
from google import genai
from google.genai import types

class SYTranscriber:
    STYLE_GUIDE = """
SOUTH YIDDISH STYLE GUIDE & RULES:

1. VOWEL SHIFT PRIORITY (CASCADE):
   - PRIORITY 1: Dictionary/Loshn-Koydesh (LK) markings (e.g. 'khóyshəd', 'khalel').
   - PRIORITY 2: Style Guide Shifts (Rules below).
   - PRIORITY 3: Sat Reference (Base vowel quality).
   - **CRITICAL**: If Rule 1 says [o]->[u], you MUST change Sat's 'hot' to 'hut' and 'ober' to 'uber'.

2. Vowel Shifts (Standard -> SY):
   - Standard [o] (אָ) -> SY [u] (e.g., 'hot' -> 'hut', 'kholem' -> 'khulem', 'hot' -> 'hut').
   - Standard [u] (ו) -> SY [i] or [i:] (e.g., 'fun' -> 'fin', 'shul' -> 'shi:l').
   - Standard [ey] (יי) -> SY [ay] (e.g., 'geyn' -> 'gayn').
   - Standard [ay] (ײַ) -> SY [a:] (e.g., 'dray' -> 'dra:').
   - **[oy] (וי)**: ONLY shift [oy] to [u:] if explicitly shown in Dictionary/LK context. Otherwise, keep Sat's [oy] (e.g., 'hoykh', 'royt').
   - **NO DOUBLE-SHIFTING**: Do not shift [o]->[u]->[i]. One shift only.

3. PRESERVE DICTIONARY AND REFERENCE MARKINGS: 
   - NEVER drop stress marks (á, é, í, ó, ú, à, ù) or length marks (:).
   - Omit parentheses: Use 'ú:n' instead of 'ú:(ə)n'.

4. PREFIXES & SUFFIXES:
   - Prefix אױפֿ- MUST be 'of-'. Prefix אַרױס- MUST be 'aró:s-' or 'arós-'.
   - Suffix -ונג (-ung) MUST be '-ink'. Suffix -ונגס- (-ungs-) MUST be '-inks-'.
   - Suffix -עניש (-enish) MUST NOT shift to '-ink'; keep it as '-enish' or '-ənish'.
   - Use 'dus' (neuter) for '-enish' nouns.

5. CLITICS & PREPOSITIONS:
   - צו (tsu) MUST be 'tsi' (before consonants) or 'ts' (before vowels). NEVER use 'tsáf'.
   - קײן (keyn) MUST be 'kayn'. NEVER truncate to 'ka'.

6. MORPHOPHONEMICS:
   - Neutralize Geminates: Use 'ng' or 'ngk', never 'ngg' (e.g. 'gegangen' -> 'gəgangən').
   - Use 'sh', 'ts', 'kh', 'y'. Use 'kh' for 'ch' in 'hekhster'.
   - Consistency: 'az' (not 'as').
"""

    def __init__(self, dict_html_path="dictionary.html", index_path="dictionary_index.json"):
        self.dict_html_path = dict_html_path
        self.index_path = index_path
        self.word_index = {}
        
        # Initialize Vertex AI Gemini Client
        try:
            self.client = genai.Client(vertexai=True)
        except Exception as e:
            print(f"Warning: Could not initialize Vertex AI Gemini client: {e}. Transcription will fail.", file=sys.stderr)
            self.client = None
            
        self._load_index()

    def _assert_no_yiddish(self, text, label="Output"):
        """Raises an exception if Yiddish/Hebrew characters are found in the text."""
        if not text: return
        hebrew_chars = re.findall(r'[\u0590-\u05FF]', text)
        if hebrew_chars:
            raise ValueError(f"CRITICAL ERROR: {label} contains Yiddish characters: {''.join(set(hebrew_chars))} in '{text}'")

    def normalize_yiddish(self, text):
        """
        Normalizes Yiddish text for lookup:
        1. Decomposes ligatures and precomposed characters.
        2. Removes non-Hebrew characters except punctuation.
        3. Keeps pointing (nikud) but removes specific trope marks if any.
        """
        replacements = {
            'װ': 'וו', 'ױ': 'וי', 'ײ': 'יי',
            'ײַ': 'יי', 'ﬠ': 'ע', 'ﬡ': 'א', 'ﬢ': 'ד', 'ﬣ': 'ה',
            'ﬤ': 'כ', 'ﬥ': 'ל', 'ﬦ': 'ם', 'ﬧ': 'ר', 'ﬨ': 'ת',
            '﬩': '+', 'שׁ': 'ש', 'שׂ': 'ש', 'שּׁ': 'ש', 'שּׂ': 'ש',
            'אַ': 'א', 'אָ': 'א', 'וּ': 'ו', 'יִ': 'י', 'ײַ': 'יי'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        text = text.replace('אָ', 'א').replace('אַ', 'א').replace('יִ', 'י').replace('וּ', 'ו')
        return "".join(c for c in text if '\u0590' <= c <= '\u05FF' or c in " ,.?!-")

    def run_technique_comparison(self, word, sentence_context, sat_ref=None):
        """Runs multiple transcription techniques for a single word to provide diagnostics."""
        norm = self.normalize_yiddish(word)
        dict_match = "N/A"
        if norm in self.word_index:
            for entry in self.word_index[norm]:
                m = re.search(r"דרומדיק:\s*\[([^\]]+)\]", entry)
                if m: 
                    dict_match = m.group(1)
                    break

        prompt = f"""
Analyze the transcription of the word '{word}' in context.
Context: {sentence_context}
{f"Sat Reference: {sat_ref}" if sat_ref else ""}
Dictionary Lookup: {dict_match}

{self.STYLE_GUIDE}

Identify:
1. Which technique (Dictionary vs Rule-based vs Sat-Informed) is most accurate here.
2. If there's a discrepancy, explain why (e.g. 'Dictionary entry is for a different sense', 'LLM corrected a missing shift').
Return a JSON object: {{"best": "transcription", "reason": "short explanation"}}
"""
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash', contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            clean_json = re.sub(r'```json\n?|\n?```', '', response.text).strip()
            return json.loads(clean_json)
        except:
            return {"best": dict_match if dict_match != "N/A" else "Error", "reason": "Fallback"}

    def analyze_pipeline_performance(self, triplets_data):
        """Generates a guide for pipeline improvement based on a batch of transcriptions."""
        summary_prompt = f"""
You are a lead linguist and pipeline engineer. 
Review these recent transcriptions and their refinements.
{json.dumps(triplets_data, ensure_ascii=False, indent=2)}

TASK:
1. Identify systematic errors (e.g. 'The engine consistently misses shift X in words of type Y').
2. Identify dictionary gaps (e.g. 'Word Z is common but missing from index').
3. Propose specific improvements to the 'SOUTH YIDDISH STYLE GUIDE' or the indexing logic.

Output a 'Pipeline Diagnostics & Improvement Guide' in Markdown.
"""
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash', contents=summary_prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            return response.text.strip()
        except Exception as e:
            return f"Failed to generate diagnostics: {e}"

    def sanitize_phonetics(self, text):
        """
        Deterministic post-processing to clean up phonetic artifacts:
        1. Neutralizes geminates (ngg -> ng).
        2. Strips grave accents (ì, ù) and redundant parentheses.
        3. Enforces clitic rules (keyn -> kayn).
        """
        if not text: return ""
        
        # Strip grave accents and parentheses noise
        text = text.replace('ì', 'i').replace('ù', 'u').replace('è', 'e').replace('à', 'a').replace('ò', 'o')
        text = re.sub(r'\((.*?)\)', r'\1', text) # Remove parentheses but keep content (e.g. (ə) -> ə)
        
        # Neutralize geminates
        text = text.replace('ngg', 'ng').replace('nk-k', 'nk')
        
        # Enforce clitic/preposition rules that LLM might still miss
        text = re.sub(r'\bka\b', 'kayn', text)
        text = re.sub(r'\btsaf\b', 'tsi', text)
        
        return text.strip()

    def rough_phonetic_match(self, yiddish, transcription):
        """
        Roughly checks if a Yiddish word matches a transcription.
        Used to avoid mis-associating 'statue' with '[a ponem]'.
        """
        if not transcription: return False
        # Remove non-alphabetic chars from transcription, keep '
        trans = re.sub(r'[^a-z\']', '', transcription.lower())
        if not trans: return True # Can't tell
        
        # Yiddish to rough latin mapping including vowels
        mapping = {
            'א': 'a', 'אָ': 'o', 'אַ': 'a', 'ב': 'b', 'וו': 'v', 'װ': 'v', 'ג': 'g', 'ד': 'd', 'ה': 'h',
            'ו': 'u', 'ז': 'z', 'ח': 'kh', 'ט': 't', 'י': 'i', 'יי': 'ey', 'ײ': 'ey', 'וי': 'oy', 'ױ': 'oy',
            'כ': 'kh', 'ל': 'l', 'מ': 'm', 'נ': 'n', 'ס': 's', 'ע': 'e', 'פּ': 'p', 'פֿ': 'f',
            'צ': 'ts', 'ק': 'k', 'ר': 'r', 'ש': 'sh', 'ת': 's'
        }
        
        # Decompose ligatures for better mapping
        yid = yiddish.replace('װ', 'וו').replace('ױ', 'וי').replace('ײ', 'יי')
        rough_yid = ""
        i = 0
        while i < len(yid):
            if i + 1 < len(yid) and yid[i:i+2] in mapping:
                rough_yid += mapping[yid[i:i+2]]
                i += 2
            else:
                rough_yid += mapping.get(yid[i], '')
                i += 1
        
        # Check first 2-3 significant phonemes
        rough_yid = re.sub(r'[^a-z]', '', rough_yid)
        if len(trans) >= 3 and len(rough_yid) >= 3:
             return trans[:2] == rough_yid[:2] or trans[:3] == rough_yid[:3]
        if len(trans) >= 2 and len(rough_yid) >= 2:
            return trans[0] == rough_yid[0] and (trans[1] == rough_yid[1] or trans[1] in 'aeiou' or rough_yid[1] in 'aeiou')
        if len(trans) >= 1 and len(rough_yid) >= 1:
            return trans[0] == rough_yid[0]
        return True

    def _load_index(self):
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r', encoding='utf-8') as f:
                self.word_index = json.load(f)
            return

        if not os.path.exists(self.dict_html_path):
            print(f"Warning: {self.dict_html_path} not found. Cannot build index.", file=sys.stderr)
            return

        print(f"Building STRICT index from {self.dict_html_path}... this may take a moment.", file=sys.stderr)
        with open(self.dict_html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            paragraphs = soup.find_all('p')
            
        # Common particles that should NEVER match complex multi-word entries
        function_word_blacklist = {
            'די', 'און', 'איז', 'אין', 'דער', 'דאָס', 'אַ', 'צו', 'מיט', 'פֿון', 
            'ער', 'זיך', 'דאָ', 'װאָס', 'װי', 'אָבער', 'אַז', 'נאָך', 'צי', 'נישט',
            'דעם', 'האָט', 'האָבן', 'זײ', 'זענען', 'אַן'
        }

        for p in paragraphs:
            p_text = p.get_text().strip()
            if not p_text: continue
            
            # Split paragraph into sub-segments by semicolon to avoid bridging unrelated entries
            segments = re.split(r';', p_text)
            
            # HEADWORD EXTRACTION (from the first segment usually)
            headword_zone = re.split(r'[\[\(\,]', segments[0])[0].strip()
            # Clean headword zone from common article markers like (אַ\דער)
            headword_zone = re.sub(r'\([^\)]+\)', '', headword_zone).strip()
            head_tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4]+", headword_zone)
            
            for segment in segments:
                # Transcription Extraction
                transcription_matches = list(re.finditer(r"([\u0590-\u05FF\u05F3\u05F4 ]+)\s*\[([^\]]+)\](?:.*?)(דרומדיק|אויך):\s*\[([^\]]+)\]", segment))
                
                for m in transcription_matches:
                    words_in_entry, std_trans, marker_type, sy_trans = m.groups()
                    words_in_entry = words_in_entry.strip()
                    if not words_in_entry: continue
                    
                    # If multiple words, take the last one as the primary match for the brackets
                    primary_word = words_in_entry.split()[-1]
                    norm_word = self.normalize_yiddish(primary_word)
                    
                    # Phonetic sanity check
                    if not self.rough_phonetic_match(primary_word, std_trans):
                        # Try the word before it if any
                        if ' ' in words_in_entry:
                             primary_word = words_in_entry.split()[-2]
                             if not self.rough_phonetic_match(primary_word, std_trans):
                                 continue
                        else:
                            continue

                    # SYNONYM CHECK: If the matched word is NOT a headword and not a phrase starting with a headword, 
                    # it might be a synonym. We should still index it, but be careful.
                    is_headword = any(self.normalize_yiddish(h) == norm_word for h in head_tokens)
                    is_phrase_of_headword = any(words_in_entry.startswith(h) for h in head_tokens)
                    
                    # Rule 1: A function word MUST be the ONLY headword to get indexed from an entry.
                    if norm_word in function_word_blacklist:
                        if not head_tokens or len(head_tokens) > 1 or head_tokens[0] != primary_word:
                             # Also check for phrases like "צו אים"
                             if words_in_entry not in head_tokens:
                                 continue

                    if norm_word not in self.word_index:
                        self.word_index[norm_word] = []
                    
                    # Cleaning: Remove artifacts and stray parentheses/brackets
                    sy_trans = sy_trans.strip()
                    sy_trans = re.sub(r'[\(\)\[\]]', '', sy_trans)
                    
                    is_phrase = ' ' in sy_trans or '|' in sy_trans or '-' in sy_trans
                    is_direct = not is_phrase and len(head_tokens) == 1 and head_tokens[0] == words_in_entry
                    
                    marker = "DIRECT_MATCH" if is_direct else "CONTEXT_MATCH"
                    
                    if not is_headword and not is_phrase_of_headword:
                        marker = "SYNONYM_MATCH"

                    # Special Case: 'צו' homograph noun (tsav) vs preposition (tsu)
                    if primary_word == 'צו':
                        if 'tsav' in std_trans.lower():
                            marker = "HOMOGRAPH_NOUN_MATCH"
                        elif 'tsu' in std_trans.lower():
                            marker = "FUNCTION_WORD"

                    # Special Case: 'זכר' homograph
                    if primary_word == 'זכר':
                         if 'zokher' in std_trans.lower():
                             marker = "HOMOGRAPH_YIDDISH_MALE"
                         elif 'zekher' in std_trans.lower():
                             marker = "DIRECT_MATCH" # This is the trace/memory one

                    # Special Case: 'חלל' homograph
                    if primary_word == 'חלל':
                         if 'khalal' in std_trans.lower():
                             marker = "DIRECT_MATCH" # Space/cosmos
                         else:
                             marker = "HOMOGRAPH_CORPSE_MATCH"

                    # Preference for "דורך" -> dor(ə)kh over der(ə)kh
                    if primary_word == 'דורך':
                        if 'dor' in sy_trans:
                            marker = "DIRECT_MATCH"
                        elif 'der' in sy_trans:
                            marker = "CONTEXT_MATCH" # Lower priority than dor(e)kh

                    # Article handling: strip leading articles from transcription if not in Yiddish word
                    if not (words_in_entry.startswith("אַ ") or words_in_entry.startswith("אַן ")) and (sy_trans.startswith("a-") or sy_trans.startswith("an-") or sy_trans.startswith("a ") or sy_trans.startswith("an ")):
                        sy_trans = re.sub(r'^(?:a|an)[- ]', '', sy_trans)

                    entry_data = f"{marker}: {words_in_entry} -> דרומדיק: [{sy_trans}] | Full: {p_text}"
                    
                    if entry_data not in self.word_index[norm_word]:
                        self.word_index[norm_word].append(entry_data)

            # FALLBACK: If a headword is NOT explicitly matched in segments, 
            # index it to the paragraph but with lower priority
            for word in head_tokens:
                norm_word = self.normalize_yiddish(word)
                if norm_word in function_word_blacklist: continue
                
                if norm_word not in self.word_index:
                    self.word_index[norm_word] = []
                
                # Only fallback if we don't have enough direct matches
                if len(self.word_index[norm_word]) < 2:
                    if p_text not in self.word_index[norm_word]:
                        self.word_index[norm_word].append(p_text)

        # Optimization: Sort and limit
        for word in self.word_index:
            # Priority: FUNCTION_WORD > DIRECT_MATCH > CONTEXT_MATCH > Fallback (no marker) > SYNONYM_MATCH > HOMOGRAPH_*
            def sort_key(x):
                if x.startswith("FUNCTION_WORD"): return 0
                if x.startswith("DIRECT_MATCH"): return 1
                if x.startswith("CONTEXT_MATCH"): return 2
                if " -> דרומדיק: [" not in x: return 3
                if x.startswith("SYNONYM_MATCH"): return 4
                if x.startswith("HOMOGRAPH"): return 5
                return 6
                
            self.word_index[word].sort(key=lambda x: (sort_key(x), len(x)))
            self.word_index[word] = list(dict.fromkeys(self.word_index[word]))[:5]

        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.word_index, f, ensure_ascii=False, indent=2)
        print(f"Strict index built and saved to {self.index_path}", file=sys.stderr)

    def get_context_for_text(self, text):
        """
        Extracts dictionary entries and uses the LLM to filter for relevance.
        Caches results to avoid redundant LLM calls for frequent words.
        """
        if not hasattr(self, '_context_cache'):
            self._context_cache = {}

        tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4\u05BE]+", text)
        raw_candidates = {}
        
        suffixes = ['ענער', 'ענע', 'ער', 'ען', 'עס', 'נע', 'ע', 'ן', 'ס']
        
        for token in tokens:
            if token in self._context_cache:
                continue
                
            norm_word = self.normalize_yiddish(token)
            
            # Gather candidates (exact + stemming)
            matches = self.word_index.get(norm_word, []).copy()
            for suffix in suffixes:
                if norm_word.endswith(suffix) and len(norm_word) > len(suffix) + 1:
                    stem = norm_word[:-len(suffix)]
                    matches.extend(self.word_index.get(stem, []))
            
            if matches:
                matches = list(set(matches))
                if len(matches) == 1:
                    # If only one candidate, assume it's relevant (reduces LLM calls)
                    self._context_cache[token] = matches
                else:
                    raw_candidates[token] = matches

        if not raw_candidates:
            # Format results using the cache
            result_lines = []
            relevant_tokens = set(tokens)
            for word, entries in self._context_cache.items():
                if word in relevant_tokens and entries:
                    result_lines.append(f"Relevant Dictionary Entries for '{word}':")
                    for entry in entries:
                        result_lines.append(f"  - {entry}")
            return "\n".join(result_lines)

        if not raw_candidates:
            return ""

        # Use LLM to filter candidates for actual relevance to the sentence
        context_prompt = f"""
You are an expert in Yiddish lexicography and dialectology. 
We have a sentence and a list of potential dictionary entries for words in that sentence.

Sentence: {text}

Candidates:
{json.dumps(raw_candidates, ensure_ascii=False, indent=2)}

TASK:
1. Identify which dictionary entries are TRULY relevant to the word's meaning and grammatical role in this sentence.
2. Resolve HOMOGRAPHS and SYNONYMS:
   - 'FUNCTION_WORD': High-priority entries for common particles/prepositions (e.g., 'צו' meaning to). These are usually the correct choice for grammatical words.
   - 'HOMOGRAPH_NOUN_MATCH': These are entries for rare nouns that share a spelling with common particles (e.g., 'צו' meaning turtle). They are usually WRONG for prepositions.
   - 'SYNONYM_MATCH': These entries are for synonyms, NOT the target word itself. The transcription usually belongs to the synonym. Use ONLY if the target word is not found elsewhere or you can deduce its pronunciation.
   - Example: 'צו' can be a preposition ('to'), a noun ('turtle'), or a particle. Match the role in the sentence.
   - Example: 'האָבן' as an auxiliary verb often has different stress/vowel patterns than the main verb.
3. Handle MULTIPLE VARIANTS: 
   - If an entry lists multiple Southern Yiddish (דרומדיק) variants, pick the one that most closely matches the context or is most standard for Central South Yiddish.
   - If 'אויך:' (also) is listed, it might be a valid variant.
4. Clean and Extract:
   - For a candidate like "DIRECT_MATCH: סטאַטוע -> דרומדיק: [státuə]", return just the transcription "[státuə]" or a cleaned version of the entry.
   - If the entry is for a phrase (e.g. "אָן אַ שיעור"), but the target word is just "שיעור", try to isolate the transcription for "שיעור" ([shí:ər]) if possible.
   - Strip leading articles (a-, an-) if they are not part of the word's usage in the sentence.
5. Accuracy Check:
   - Verify that the transcription matches the word phonetically. If a word starts with 'b' and the transcription starts with 'k', it's likely a mismatch.

Return the filtered candidates as a JSON object: {{"word": ["cleaned/relevant entry 1", ...]}}
Ensure the results are concise and directly useful for transcription.
Return ONLY the JSON.
"""

        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=context_prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            # Clean response text from markdown code blocks
            clean_json = re.sub(r'```json\n?|\n?```', '', response.text).strip()
            filtered_new = json.loads(clean_json)
            self._context_cache.update(filtered_new)
        except Exception as e:
            print(f"Context filtering failed: {e}. Using raw candidates.", file=sys.stderr)
            self._context_cache.update(raw_candidates)

        # Format results using the cache
        result_lines = []
        # We only want to output entries for words in the CURRENT text block
        relevant_tokens = set(tokens)
        for word, entries in self._context_cache.items():
            if word in relevant_tokens and entries:
                result_lines.append(f"Relevant Dictionary Entries for '{word}':")
                for entry in entries:
                    result_lines.append(f"  - {entry}")
        
        return "\n".join(result_lines)

    def transcribe(self, text, explain=False, quiet=False):
        context_str = self.get_context_for_text(text)
        
        if explain:
            prompt = f"""
You are an expert in Yiddish dialectology, specifically South Yiddish (SY) as represented in the Yiddish Cultural Dictionary (yiddishculturaldictionary.org).
Your task is to transcribe the given Yiddish text into South Yiddish phonetic orthography.

CONTEXT:
The following entries are from the dictionary and provide examples of correct SY transcriptions (marked as 'דרומדיק: [...]'). Use these as your primary source of truth.

{self.STYLE_GUIDE}

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

{self.STYLE_GUIDE}

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
            
            # Assert no Yiddish in the transcription result (ignoring bracketed context if explain=True)
            if not explain:
                match = re.search(r'\[(.*?)\]', result, re.DOTALL)
                val_text = match.group(1) if match else result
                self._assert_no_yiddish(val_text, "Initial SY")
            
            if not quiet:
                print(result)
            return result
        except Exception as e:
            if isinstance(e, ValueError): raise e
            print(f"Error during transcription: {e}", file=sys.stderr)
            return None

    def convert_galkhes_to_ycd(self, text):
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

    def self_correct_sy(self, yiddish, initial_sy, sat_ycd=None):
        """
        Compares the generated SY to Sat (if available) and corrects errors in SY using the LLM.
        """
        if sat_ycd:
            prompt = f"""
You are an expert editor of Yiddish dialectal transcriptions.
We have an initial Southern Yiddish (SY) transcription and a reference transcription ('Sat').

{self.STYLE_GUIDE}

Yiddish Text: {yiddish}
Initial SY: {initial_sy}
Sat Reference (normalized): {sat_ycd}

TASK:
1. Identify errors in 'Initial SY' by comparing it to 'Sat Reference', the original Yiddish, and the Style Guide.
2. The 'Sat Reference' is HIGHLY ACCURATE for base vowel qualities (like when to keep 'oy' vs shift to 'u:'). Use the Sat Reference as your base text.
3. ONLY modify the Sat Reference to apply specific South Yiddish Style Guide rules (like -ung -> -ink, 'of' prefix, borrowing bypass) or to match explicit Dictionary markings.
4. CRITICAL: NEVER drop stress marks (e.g., á, ú) or length colons (:) that appear in the Sat Reference or the Dictionary. 
5. Ensure the output is consistent and follows YCD style.

Return the final corrected transcription inside brackets, like this: [corrected transcription].
After the brackets, list each specific correction made and the reason (in English).
"""
        else:
            prompt = f"""
You are an expert editor of Yiddish dialectal transcriptions.
We have an initial Southern Yiddish (SY) transcription.

{self.STYLE_GUIDE}

Yiddish Text: {yiddish}
Initial SY: {initial_sy}

TASK:
1. Review the 'Initial SY' transcription for consistency and accuracy according to the South Yiddish Style Guide.
2. Correct any missed shifts, improper suffix realizations, or normalized stress marks.
3. Ensure no hyphens between identical vowels and other morphophonemic rules.

Return the final corrected transcription inside brackets, like this: [corrected transcription].
After the brackets, list each specific correction made and the reason (in English).
"""
        try:
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            full_text = response.text.strip()
            match = re.search(r'\[(.*?)\]', full_text, re.DOTALL)
            
            if match:
                corrected = match.group(1).strip()
                # Basic guard against literal placeholders
                if "corrected transcription" in corrected.lower():
                     corrected = initial_sy
                
                # Apply deterministic sanitization
                corrected = self.sanitize_phonetics(corrected)
                
                # Assert no Yiddish in final refined SY
                self._assert_no_yiddish(corrected, "Refined SY")
                
                changes = full_text.split(']', 1)[1].strip() if ']' in full_text else "Refinements applied."
            else:
                corrected = initial_sy
                changes = full_text
                
            return corrected, changes
        except Exception as e:
            if isinstance(e, ValueError): raise e
            print(f"Error in correction: {e}", file=sys.stderr)
            return initial_sy, f"Error in correction: {e}"

def parse_multilanguage_file(file_path):
    """
    Parses a file containing triplets: English, Yiddish, and a transcription.
    Returns a list of dictionaries with the triplet data.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    
    triplets = []
    # Data comes in triplets
    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            triplets.append({
                'english': lines[i],
                'yiddish': lines[i+1],
                'transcription': lines[i+2]
            })
    return triplets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transcribe Yiddish to South Yiddish (SY) with Diagnostics")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-t', '--text', type=str, help="Text to transcribe")
    group.add_argument('-f', '--file', type=str, help="File containing pure Yiddish text")
    group.add_argument('--multilanguage-file', type=str, help="File with English/Yiddish/Transcription triplets")
    
    args = parser.parse_args()
    transcriber = SYTranscriber()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if args.multilanguage_file:
        triplets = parse_multilanguage_file(args.multilanguage_file)
        base_name, ext = os.path.splitext(args.multilanguage_file)
        output_file = f"{base_name}_withSY_{ts}{ext}"
        report_file = f"SY_Transcription_Report_{ts}.md"
        
        batch_diagnostics = []
        
        with open(output_file, 'w', encoding='utf-8') as f_out, \
             open(report_file, 'w', encoding='utf-8') as f_rep:
            
            f_rep.write(f"# South Yiddish Transcription & Pipeline Report\nDate: {ts}\n\n")
            
            for i, triplet in enumerate(triplets):
                print(f"--- Processing {i+1}/{len(triplets)} ---")
                
                # 1. Initial SY
                initial_res = transcriber.transcribe(triplet['yiddish'], quiet=True)
                match = re.search(r'\[(.*?)\]', initial_res, re.DOTALL) if initial_res else None
                initial_sy = match.group(1) if match else (initial_res or "")
                
                # 2. Reference Sat
                sat_ycd = transcriber.convert_galkhes_to_ycd(triplet['transcription'])
                
                # 3. Refined SY
                refined_sy, corrections = transcriber.self_correct_sy(triplet['yiddish'], initial_sy, sat_ycd)
                
                # 4. Word-Level Technique Comparison (Sample words)
                tokens = re.findall(r"[\u0590-\u05FF\u05F3\u05F4\u05BE]+", triplet['yiddish'])
                word_diagnostics = []
                for token in tokens[:5]: # Diag for first 5 words per para
                    diag = transcriber.run_technique_comparison(token, triplet['yiddish'], sat_ycd)
                    word_diagnostics.append({"word": token, "diag": diag})
                
                batch_diagnostics.append({
                    "id": i+1,
                    "yiddish": triplet['yiddish'],
                    "initial": initial_sy,
                    "refined": refined_sy,
                    "sat": sat_ycd,
                    "corrections": corrections,
                    "word_diags": word_diagnostics
                })

                # Write output text
                f_out.write(f"{triplet['english']}\n{triplet['yiddish']}\n{triplet['transcription']}\n{sat_ycd}\n{refined_sy}\n\n")
                
                # Write to report
                f_rep.write(f"## Paragraph {i+1}\n")
                f_rep.write(f"**Yiddish**: {triplet['yiddish']}\n\n")
                f_rep.write(f"**Final SY**: `[{refined_sy}]`\n\n")
                f_rep.write(f"**Refinements**:\n{corrections}\n\n")
                f_rep.write("| Word | Technique Choice | Reason |\n| :--- | :--- | :--- |\n")
                for wd in word_diagnostics:
                    f_rep.write(f"| {wd['word']} | {wd['diag'].get('best','?')} | {wd['diag'].get('reason','?')} |\n")
                f_rep.write("\n---\n\n")

            # Final Pipeline Analysis
            print("Generating Pipeline Diagnostics...")
            global_diag = transcriber.analyze_pipeline_performance(batch_diagnostics)
            f_rep.write("# Pipeline Performance Summary & Improvement Guide\n")
            f_rep.write(global_diag)
            
        print(f"Results written to {output_file}")
        print(f"Diagnostic report written to {report_file}")

    else:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f: input_text = f.read()
        else:
            input_text = args.text
        
        initial_res = transcriber.transcribe(input_text, quiet=True)
        match = re.search(r'\[(.*?)\]', initial_res, re.DOTALL) if initial_res else None
        initial_sy = match.group(1) if match else (initial_res or "")
        
        refined_sy, corrections = transcriber.self_correct_sy(input_text, initial_sy)
        
        report_file = f"SY_Report_{ts}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(f"# SY Transcription Report\n\n**Input**: {input_text}\n\n**Result**: `[{refined_sy}]`\n\n**Detail**:\n{corrections}\n")
        
        print(f"Result: [{refined_sy}]")
        print(f"Report saved to {report_file}")
