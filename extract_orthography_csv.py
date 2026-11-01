"""
Extract Yiddish orthography -> transliteration pairs from dictionary_index.json.

Output CSV columns:
  1. Yiddish orthography
  2. Transliteration
  3. Notes — dialect label and/or "uncertain" marker if applicable

Covers:
  - Standard (unmarked) transliterations
  - דרומדיק (Southern) dialect forms
  - צפונדיק (Northern) dialect forms
  - Alternate forms introduced by editorial notes like {מער פאָרמעל:} [translit]
  - Non-headword words that appear in the index (including CONTEXT/SYNONYM matches)
  - Uncertain forms (marked with ? or unbalanced parentheses)
"""

import json
import re
import csv

INPUT  = "dictionary_index.json"
OUTPUT = "yiddish_transliteration.csv"

# ── constants / helpers ───────────────────────────────────────────────────────

_HAS_HEBREW = re.compile(r'[\u05d0-\u05ea\ufb1d-\ufb4e]')

# Leading noise to strip from Yiddish phrase candidates
_LEADING = re.compile(r'^[\s,;=:\\|!.()\[\]″′⸗–—​\xa0]+')
# Trailing noise to strip
_TRAILING = re.compile(r'[\s,;=:()\[\]″′⸗–—​\xa0]+$')

# Numbered/lettered list markers like "(2)", "(א)", "2)"
_LIST_PREFIX = re.compile(r'^\s*(?:\(\s*[\dא-ת]+\s*\)|\d+\))\s*')

# Alternative-list separator — take only the last element
_ALT_SEP = re.compile(r'\\+')

# Dialect/label-only patterns that should not be captured as headwords.
# We normalise these out of the text before running the pair regex.
# Note: דרומדיק: and צפונדיק: are handled by _PAIR, so we exclude them here.
# We only strip labels that appear WITHOUT a Yiddish headword before them
# (i.e., they are pure dialect-label annotations we already captured).
_LABEL_PATTERN = re.compile(
    r'(?:צפ|אויך|ליטוויש|גאַליציאַניש|ליטוואַקיש):\s*\[[^\]]+\]'
)

# Bare-text (non-brace) qualifier labels that appear inline before [translit].
# These should be stripped so _PAIR does not capture them as Yiddish headwords.
# Examples: "מער פאָרמעל: [alpí]", "טייל ד″מ: [ív-gèybm]", "ל″ר: -ים [khatéysəm]"
_BARE_LABEL_PATTERN = re.compile(
    r'(?:'
    r'מער פאָרמעל'           # more formal
    r'|נאָכמער פאָרמעל'       # even more formal
    r'|טייל ד\u2033מ'        # some SE dialect
    r'|ל\u2033ר:\s*-\S+'     # plural suffix: -ים etc.
    r'|ל\u2033נ:\s*-\S+'     # feminine suffix
    r'|ל\u2033ז:\s*-\S+'     # masculine suffix
    r'|אויך:\s*-\S+'         # also: suffix variant
    r')'
    r'\s*:?\s*'
)

# When "; דרומדיק:" or "; צפונדיק:" appears, the ; belongs to the same pair
_SEMI_DIALECT = re.compile(r';\s*(?=(?:דרומדיק|צפונדיק):)')

_UNCERTAIN_MARKS = re.compile(r'[?]')

MAX_YIDDISH_LEN = 80  # characters; longer = explanatory phrase, not a headword

# Dialect labels used in notes column
DIALECT_LABELS = {
    'standard': '',
    'dormedk':  'דרומדיק',   # Southern
    'tsofndik': 'צפונדיק',   # Northern
}


def _unbalanced_parens(s):
    depth = 0
    for c in s:
        if c == '(':
            depth += 1
        elif c == ')':
            if depth == 0:
                return True
            depth -= 1
    return depth != 0


def strip_notes(text):
    """Remove editorial {…} notes."""
    return re.sub(r'\{[^}]*?\}', '', text, flags=re.DOTALL)


def clean_yiddish(s):
    s = re.sub(r'\s+', ' ', s)
    if _ALT_SEP.search(s):
        # Take only the last alternative (after the last \)
        s = _ALT_SEP.split(s)[-1]
    s = _LEADING.sub('', s)
    s = _TRAILING.sub('', s)
    s = _LIST_PREFIX.sub('', s).strip()
    return s


# Strings that look like Yiddish but are really dialect/metadata labels, not headwords.
# These appear as the "Yiddish" capture group when _PAIR matches a standalone
# "דרומדיק: [translit]" or "צפונדיק: [translit]" fragment in Full text,
# or when bare-text qualifiers like "מער פאָרמעל: [translit]" are matched.
_SKIP_AS_HEADWORD = {
    'דרומדיק:', 'דרומדיק', 'צפונדיק:', 'צפונדיק',
    'ל″ר:', 'ל″ר', 'ל″י:', 'ל″י', 'ל″נ:', 'ל″נ', 'ל″ז:', 'ל″ז', 'ל″ע:', 'ל″ע',
    'ד″מ:', 'ד″מ', 'צ', 'ד',
    # Yiddish words used as alternative/formal markers, not real headwords
    'צי',            # "or" — introduces alternative transliteration
    'אויך',          # "also"
}


def is_valid_yiddish(s):
    if not _HAS_HEBREW.search(s):
        return False
    if len(s.strip()) < 2 or len(s.strip()) > MAX_YIDDISH_LEN:
        return False
    # Reject if clearly a metadata fragment
    if 'Full:' in s or 'MATCH' in s:
        return False
    # Reject strings that are purely a dialect/grammar label
    if s.strip() in _SKIP_AS_HEADWORD:
        return False
    # Reject if ends with ':' and contains only a known label word (e.g. "דרומדיק:")
    stripped = s.strip().rstrip(':').strip()
    if stripped in _SKIP_AS_HEADWORD:
        return False
    return True


def is_valid_translit(s):
    s = s.strip()
    # Reject empty or single-letter phoneme labels
    return bool(s) and not re.fullmatch(r'[a-zA-Z]', s)


def build_note(dialect_label, uncertain):
    """Combine dialect label and uncertainty into a note string."""
    parts = []
    if dialect_label:
        parts.append(dialect_label)
    if uncertain:
        parts.append('uncertain')
    return '; '.join(parts)


# ── main pair extractor ───────────────────────────────────────────────────────

# Core pattern capturing:
#   group 1 — Yiddish text (no ; [ ] { } < >)
#   group 2 — [standard transliteration]
#   group 3 — optional דרומדיק: [southern transliteration]
#   group 4 — optional צפונדיק: [northern transliteration]
#
# The optional gaps use [^;{]*? so they do NOT cross semicolons.
# Semicolons before dialect labels are pre-normalised to commas by _SEMI_DIALECT.
_PAIR = re.compile(
    r'([^;\[\]{}<>]+?)'
    r'\s*\[([^\]]+)\]'
    r'(?:[^;{]*?'
    r'דרומדיק:?\s*\[([^\]]+)\]'   # colon is optional in some entries
    r')?'
    r'(?:[^;{]*?'
    r'צפונדיק:?\s*\[([^\]]+)\]'
    r')?'
)

# Secondary pattern: {editorial note:} [translit], צפונדיק/דרומדיק: [translit]
# Used when the Yiddish comes from elsewhere in the segment.
_NOTE_BRACKET = re.compile(
    r'\{[^}]*\}:?\s*\[([^\]]+)\]'
    r'(?:[^;{]*?'
    r'(?:דרומדיק|צפונדיק):?\s*\[([^\]]+)\]'
    r')?'
)

# Additional standalone dialect forms that appear in the middle of a segment
# after an already-matched Yiddish phrase — e.g. ", צי [alternate]"
_TSI_ALT = re.compile(r'[,\s]צי\s*\[([^\]]+)\]')


def extract_pairs(text, base_uncertain=False):
    """
    Yield (yiddish, transliteration, note) from a text block.
    Standard, דרומדיק, and צפונדיק forms are all emitted.
    Note is a string like '' | 'uncertain' | 'דרומדיק' | 'דרומדיק; uncertain'.
    """
    text = _SEMI_DIALECT.sub(', ', text)        # "; דרומדיק:" / "; צפונדיק:" → ","

    # ── Process editorial-note-only transliterations before stripping notes ──
    # These are segments like "{מער פאָרמעל:} [ahàr(ə)n-(h)akóyhən], צפונדיק: [...]"
    # The Yiddish form is implied by the surrounding context; we use the key word
    # for these via the caller — here we yield them with the yiddish=None sentinel.
    for nm in _NOTE_BRACKET.finditer(text):
        standard = nm.group(1).strip()
        dialect  = nm.group(2).strip() if nm.group(2) else None
        if is_valid_translit(standard):
            unc = base_uncertain or _UNCERTAIN_MARKS.search(standard) or _unbalanced_parens(standard)
            yield None, standard, build_note('', bool(unc)), 'note_bracket'
        if dialect and is_valid_translit(dialect):
            unc = base_uncertain or _UNCERTAIN_MARKS.search(dialect) or _unbalanced_parens(dialect)
            yield None, dialect, build_note('', bool(unc)), 'note_bracket'

    # ── Strip notes then process normal pairs ──────────────────────────────
    text = strip_notes(text)
    text = _LABEL_PATTERN.sub('', text)     # remove dialect label+translit noise
    text = _BARE_LABEL_PATTERN.sub('', text)  # remove inline bare qualifier labels

    for seg in (s.strip() for s in text.split(';') if s.strip()):
        if seg.startswith('['):
            continue
        for m in _PAIR.finditer(seg):
            raw_yid  = m.group(1)
            standard = m.group(2).strip()
            southern = m.group(3).strip() if m.group(3) else None
            northern = m.group(4).strip() if m.group(4) else None

            yiddish = clean_yiddish(raw_yid)
            if not is_valid_yiddish(yiddish):
                continue

            if is_valid_translit(standard):
                unc = base_uncertain \
                      or bool(_UNCERTAIN_MARKS.search(standard)) \
                      or _unbalanced_parens(standard)
                yield yiddish, standard, build_note('', unc), 'pair'

            if southern and is_valid_translit(southern):
                unc = base_uncertain \
                      or bool(_UNCERTAIN_MARKS.search(southern)) \
                      or _unbalanced_parens(southern)
                yield yiddish, southern, build_note(DIALECT_LABELS['dormedk'], unc), 'pair'

            if northern and is_valid_translit(northern):
                unc = base_uncertain \
                      or bool(_UNCERTAIN_MARKS.search(northern)) \
                      or _unbalanced_parens(northern)
                yield yiddish, northern, build_note(DIALECT_LABELS['tsofndik'], unc), 'pair'

            # Also check for ", צי [alternate]" right after this match
            remainder = seg[m.end():]
            for alt in _TSI_ALT.finditer(remainder):
                alt_t = alt.group(1).strip()
                if is_valid_translit(alt_t):
                    unc = base_uncertain or bool(_UNCERTAIN_MARKS.search(alt_t)) or _unbalanced_parens(alt_t)
                    yield yiddish, alt_t, build_note('', unc), 'pair'


# ── main extraction ───────────────────────────────────────────────────────────

_MATCH_RE = re.compile(
    r'(DIRECT_MATCH|CONTEXT_MATCH|SYNONYM_MATCH):\s*(.+?)'
    r'\s*->\s*דרומדיק:\s*\[([^\]]+)\]'
    r'(?:\s*\|\s*Full:\s*(.+))?$',
    re.DOTALL
)


def main():
    with open(INPUT, encoding='utf-8') as f:
        data = json.load(f)

    rows = []
    seen = set()

    def add(yiddish, translit, note):
        yiddish  = clean_yiddish(yiddish)
        translit = translit.strip()
        if not is_valid_yiddish(yiddish) or not is_valid_translit(translit):
            return
        key = (yiddish, translit)
        if key in seen:
            return
        seen.add(key)
        rows.append((yiddish, translit, note))

    for key_word, entries in data.items():
        for entry in entries:

            # ── structured MATCH entries ──────────────────────────────────────
            mm = _MATCH_RE.match(entry)
            if mm:
                match_type = mm.group(1)
                phrase     = clean_yiddish(mm.group(2))
                south      = mm.group(3).strip()
                full_text  = mm.group(4) or ''

                # CONTEXT_MATCH: transliteration is for the phrase as a whole,
                # not the individual key word → uncertain
                is_unc = (match_type == 'CONTEXT_MATCH') \
                         or _unbalanced_parens(south)

                if is_valid_yiddish(phrase) and is_valid_translit(south):
                    add(phrase, south,
                        build_note(DIALECT_LABELS['dormedk'], is_unc))

                for yid, translit, note, src in extract_pairs(full_text, base_uncertain=is_unc):
                    if yid is None:
                        # Note-bracket form: associate with the phrase
                        if is_valid_yiddish(phrase):
                            add(phrase, translit, note)
                    else:
                        add(yid, translit, note)

                continue  # don't re-process via generic path

            # ── generic entries ───────────────────────────────────────────────
            for yid, translit, note, src in extract_pairs(entry):
                if yid is None:
                    # Note-bracket form: associate with the index key word
                    if is_valid_yiddish(key_word):
                        add(key_word, translit, note)
                else:
                    add(yid, translit, note)

    rows.sort(key=lambda r: (r[0], r[1]))

    with open(OUTPUT, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Yiddish', 'Transliteration', 'Uncertain'])
        for yiddish, translit, note in rows:
            # Only emit דרומדיק forms (rows whose note contains דרומדיק or
            # rows from DIRECT_MATCH where the main [translit] IS the דרומדיק form).
            # The דרומדיק label was set in build_note() for all southern forms.
            if DIALECT_LABELS['dormedk'] not in note:
                continue
            uncertain_note = 'uncertain' if 'uncertain' in note else ''
            writer.writerow([yiddish, translit, uncertain_note])

    dormedk_rows = [r for r in rows if DIALECT_LABELS['dormedk'] in r[2]]
    total     = len(dormedk_rows)
    uncertain = sum(1 for r in dormedk_rows if 'uncertain' in r[2])
    certain   = total - uncertain

    print(f"Wrote {total} rows to {OUTPUT}  ({certain} certain, {uncertain} uncertain)")


if __name__ == '__main__':
    main()
