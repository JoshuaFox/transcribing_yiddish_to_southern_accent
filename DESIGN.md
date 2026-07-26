 The Logic Pipeline

  1. Dictionary Ingestion and Normalization (The JSON Index)
  Instead of reading a 22MB HTML file on every run, sy_transcriber.py parses the Yiddish Cultural Dictionary once. It normalizes the orthography by decomposing YIVO ligatures (like װ to וו) and stripping all diacritics (nikkud). It extracts the Standard and Southern
  Yiddish (דרומדיק) phonetic brackets and saves this to a highly efficient dictionary_index.json.

  2. Context Retrieval and Stemming
  When given a Yiddish sentence, the script does not blindly throw the text at the LLM. It extracts each word, normalizes it, and queries the JSON index. 
   * Exact Match: It first looks for the exact word.
   * Stemming: If the exact word (e.g., an inflected form like זײַנע) is not found, the script applies a Yiddish stemming algorithm, stripping common grammatical suffixes (-עס, -ענער, -ן, etc.) to find the base root (e.g., זיין) and retrieve its phonetic context.

  3. Initial SY Generation (Avoiding "Blind" Standard Shifts)
  The LLM generates the first draft of the SY transcription using a carefully crafted prompt. The logic explicitly avoids applying simplistic 1-to-1 shifts from Standard Yiddish, because a single Standard spelling can represent entirely different historical phonemes. 
   * Priority 1 (Dictionary Context): If the word or its stemmed root is in the provided dictionary context, the LLM must use that exact Southern Yiddish realization.
   * Priority 2 (Etymological Inference): If the word is not in the dictionary, the LLM applies established SY sound changes (which we previously derived by analyzing the dictionary). Crucially, the prompt instructs the LLM to use etymological clues (Germanic vs.
     Semitic/Loshn Koydesh) to resolve ambiguities—for example, knowing that a Semitic Kamatz (אָ) shifts to [u:] while a short Germanic אָ might behave differently.

  4. The Self-Correction Phase (Using "Sat" as a Guide)
  Because zero-shot LLM generation can sometimes hallucinate shifts or misparse Hebrew roots, sy_evaluator.py introduces a self-correction pass. 
   * It feeds the LLM the Original Yiddish, the Initial SY generation, and the provided Sat transcription (after orthographically normalizing the Sat IPA to match the dictionary style).
   * The LLM acts as an editor: it checks if Sat offers a more accurate lexical pronunciation or catches a missed dialectal shift. If the Initial SY contains a clear error, it adopts the Sat correction. If both are valid but simply represent different sub-dialects of
     Southern Yiddish, it retains the dictionary-based SY. (It outputs these corrections to stdout).

  5. Final Comparative Analysis
  Finally, the script performs a critical evaluation of the delta between the Final Corrected SY and the Sat transcription. It outputs a Markdown report (Transcription_Analysis.md) explaining the genuine phonetic differences, explicitly pointing out where underlying
  sound rules appear to have been broken, whether due to different lexical choices (like a prefix variant), errors in the original Sat text, or alternative dialectal realizations.
