#!/usr/bin/env python3
"""
Check Doremidik transcription against yiddishculturaldictionary.org (YCD).

CSV output:
  1. Yiddish word
  2. Provided transcription
  3. YCD Doremidik form (exact or similar form, or "not found")
  4. Analysis based on YCD principles
"""

import re, csv, unicodedata
from pathlib import Path

DICT_TXT  = "yiddishculturaldictionary.org.txt"
TEXT_FILE = "text-and-transcription.txt"
OUTPUT    = "transcription_check.csv"

HEB_RE   = re.compile(r'[א-תְ-ׇיִ-פֿװ-״]')
YID_TOK  = re.compile(r'[א-תְ-ׇיִ-פֿװ-״־⁠]+')
TRANS_TOK = re.compile(r"[a-zA-ZÀ-ɏə:\-']+")
SOFIT    = str.maketrans('ךםןףץ', 'כמנפצ')

# doremidik in Hebrew characters for pattern matching
DOR_LABEL = 'דרומדיק'

# Expected first Latin character for each Hebrew initial letter.
# Used to detect cross-contamination in the single-word index entries.
_HEB_FIRST = {
    'א': set('aeiouáàéèíìóòúùäëïöüə'),
    'ב': {'b', 'v'},
    'ג': {'g'},
    'ד': {'d'},
    'ה': {'h'},
    'ו': {'v', 'w'},
    'ז': {'z'},
    'ח': {'k', 'h'},
    'ט': {'t'},
    'י': {'y', 'i', 'j'},
    'כ': {'k', 'h'},
    'ל': {'l'},
    'מ': {'m'},
    'נ': {'n'},
    'ס': {'s'},
    'ע': set('aeiouáàéèíìóòúùäëïöüə'),
    'פ': {'p', 'f'},
    'צ': {'t'},
    'ק': {'k'},
    'ר': {'r'},
    'ש': {'s'},
    'ת': {'t', 's'},
}
_LEAD_ACCENT = re.compile(r'^[áàéèíìóòúùäëïöü]+', re.I)


def _translit_compatible(heb_key, translit):
    if not heb_key or not translit:
        return True
    expected = _HEB_FIRST.get(heb_key[0])
    if not expected:
        return True
    t = _LEAD_ACCENT.sub('', translit.lower())
    return t[:1] in expected


def norm_yid(s):
    s = unicodedata.normalize('NFKC', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.translate(SOFIT).strip()


def strip_len(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('ə', 'e')
    return re.sub(r'[:()\[\]!? ]', '', s).lower().strip()


def strip_len_keep_colon(s):
    """Like strip_len but preserves ':' so vowel length is compared."""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = s.replace('ə', 'e')
    return re.sub(r'[()\[\]!? ]', '', s).lower().strip()


print("Loading dictionary...")
raw_dict  = Path(DICT_TXT).read_text(encoding='utf-8')

# ── build index line-by-line ──────────────────────────────────────────────────
#
# Process each line of the dictionary separately.  This prevents the pattern from
# spanning two unrelated entries that happen to appear on consecutive lines.
#
# On each line we look for:
#   YIDDISH_PHRASE [std_translit] ... doremidik: [dor_translit]
# and also:
#   YIDDISH_PHRASE [std_translit]   (no doremidik form)
#
# The doremidik: must appear on THE SAME LINE as the [std_translit].

_LINE_DOR_RE = re.compile(
    r'([א-תְ-ׇיִ-פֿװ-״ ⸗\-\'"]{1,80}?)'
    r'\s*\[([^\]\n]{1,80})\]'
    r'[^[\n]{0,200}?'
    r'דרומדיק:\s*\[([^\]\n]{1,80})\]',
    re.UNICODE,
)

_LINE_STD_RE = re.compile(
    r'([א-תְ-ׇיִ-פֿװ-״ ⸗\-\'"]{1,60}?)'
    r'\s*\[([a-zA-ZÀ-ɏə\-:|() \']{1,80})\]',
    re.UNICODE,
)

# index: norm_key -> list of (phrase, dor, word_count)
# Only entries with a Doremidik form are indexed.
index = {}

def _wc(phrase):
    return max(1, len(YID_TOK.findall(phrase)))

def _add(phrase, dor):
    wc = _wc(phrase)
    for tok in YID_TOK.findall(phrase):
        key = norm_yid(tok)
        if len(key) < 2:
            continue
        index.setdefault(key, []).append(
            (phrase.strip(), dor.strip(), wc)
        )

print("Building index (line by line)...")
for line in raw_dict.splitlines():
    for m in _LINE_DOR_RE.finditer(line):
        _add(m.group(1), m.group(3))

print(f"  {len(index)} unique word-forms with Doremidik variants")


def _clean_translit(t):
    """Strip accents and length marks for length comparison."""
    return re.sub(r'[áàéèíìóòúùäëïöü:()\[\] ]', '', t, flags=re.I)


def _last_letter_ok(key, t):
    """Check last Hebrew consonant is roughly reflected in transliteration end."""
    if not key or not t:
        return True
    last_heb = key[-1]
    tc = _clean_translit(t).rstrip('-|')
    if not tc:
        return True
    tl = t.rstrip().lower()  # original for vowel endings
    if last_heb == 'נ':
        return tc[-1] in ('n', 'm')
    if last_heb == 'כ':  # after sofit ך → כ
        return tc.endswith('kh') or tc.endswith('k') or tc[-1] == 'h'
    if last_heb == 'פ':  # after sofit ף → פ
        return tc[-1] in ('p', 'f')
    if last_heb == 'מ':  # after sofit ם → מ
        return tc[-1] in ('m', 'n')
    if last_heb == 'ו':  # vov at word end = usually a vowel sound
        return tl[-1] in ('u', 'o', 'i', 'e', 'a', 'y')
    return True


def _translit_ok(key, t):
    """True if transliteration t is plausibly correct for the Hebrew key.

    Checks:
    1. First Latin character matches the Hebrew first letter phonetically.
    2. Stripped length ≤ 2.0 chars per Hebrew letter.
    3. Last letter of transliteration reflects the Hebrew final consonant.
    """
    if not _translit_compatible(key, t):
        return False
    if '|' in t:
        return False  # phrase-level separator — this is a phrase transliteration
    clean = _clean_translit(t)
    if len(clean) < 2:
        return False  # too short to be a real word transliteration
    if len(key) > 0 and len(clean) / len(key) >= 2.0:
        return False
    if not _last_letter_ok(key, t):
        return False
    return True


def _best_exact(entries, key):
    """Return the best compatible exact single-word match, or None."""
    candidates = []
    for e in entries:
        phrase, dor, wc = e
        if wc != 1 or norm_yid(phrase) != key:
            continue
        if not _translit_ok(key, dor):
            continue
        pipes = dor.count('|')
        hyphens = len(re.findall(r'-[a-zA-ZÀ-ɏ]', dor))
        candidates.append((pipes, hyphens, len(dor), e))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][3]


def _phrase_key_is_first(phrase, key):
    """True if the searched key is the first Yiddish word token in the phrase."""
    toks = YID_TOK.findall(phrase)
    return bool(toks) and norm_yid(toks[0]) == key


def _best_phrase(entries, key, phrase_ok=None):
    """Return best phrase match where key appears first and has ≤4 words."""
    eligible = [
        e for e in entries
        if e[2] <= 4 and _phrase_key_is_first(e[0], key)
        and (phrase_ok is None or phrase_ok(e[0]))
    ]
    dor_hits = [
        (e[2], i, e) for i, e in enumerate(eligible)
        if _translit_compatible(key, e[1])
    ]
    return sorted(dor_hits)[0][2] if dor_hits else None


def lookup(yid_word):
    """Returns (dor_form, dor_raw, exact, headword).

    dor_form : Doremidik form string, or None if not found.
    dor_raw  : same as dor_form (kept for compatibility with expand_dor calls).
    exact    : True when a single-word exact dictionary match exists.
    headword : YCD phrase where the form was found, or None.
    """
    key = norm_yid(yid_word)
    if len(key) < 2 or key not in index:
        return (None, None, False, None)

    RAFE = 'ֿ'
    fe_initial = (
        len(yid_word) >= 2 and
        yid_word[0] == 'פ' and
        RAFE in yid_word[:3]
    )

    def _ok_for_word(t):
        if not _translit_ok(key, t):
            return False
        if fe_initial:
            t2 = _LEAD_ACCENT.sub('', t.lower())
            if t2[:1] == 'p':
                return False
        return True

    entries = index[key]
    exact = _best_exact(entries, key)
    if exact:
        phrase, dor, wc = exact
        if _ok_for_word(dor):
            return (dor, dor, True, phrase)

    KAMETS = 'ָ'
    PATAKH = 'ַ'
    has_kamets = KAMETS in yid_word
    has_patakh = PATAKH in yid_word

    def _phrase_nikud_ok(phrase):
        if has_kamets and PATAKH in phrase and KAMETS not in phrase:
            return False
        if has_patakh and KAMETS in phrase and PATAKH not in phrase:
            return False
        return True

    phrase_e = _best_phrase(entries, key, _phrase_nikud_ok)
    if phrase_e:
        phrase, dor, wc = phrase_e
        if _ok_for_word(dor):
            return (dor, dor, False, phrase)

    return (None, None, False, None)


# ── phonological rules (all derived from YCD) ────────────────────────────────
#
# RULE 1 — kamets-alef (alef+kamets, written alef U+05D0 + U+05B8):
#   Standard [o] → Doremidik [u] or [u:]
#   YCD (line 4076): "אין די דרומדיקע דיאַלעקטן: אָדער [o] אָדער [u] ([u:])"
#   Examples: זאָגן [zogn]→[zugn], זאָטל→[zu:tl], זכרון→[zeku:rn],
#             אַלעמאָל [alemol]→[alemu:l], תמיד [tomed]→[tumet]
#
# RULE 2 — yud-beys / tsere (ײ ligature or double yod יי or tsere ֵ):
#   Standard [ey] → Doremidik [ay]
#   YCD: א″ב [alev-beys]→[alev-bays]; אשת⸗אישניק [eyshes]→[ayshes]
#   EXCEPTION: Hebrew-component words with tsere → [a:] not [ay]:
#   YCD: טענה [tayne]→[ta:ne]
#
# RULE 3 — פֿון: Standard [fun] → Doremidik [fin]
#   YCD: "פון א ביז ב [funalef|biz-beyz], doremidik: [finalef|biz-bays]"
#
# RULE 4 — אוּן (conjunction): Standard [un] → Doremidik [in]
#   Derived from vov-class vowel shift; confirmed by text-and-transcription.txt
#
# RULE 5 — אויף: Standard/NE [af] → Doremidik [of]
#   YCD: "iberloyzn oyf hefker [af-hefker], doremidik: [(of-(h)efker]"
#

def ortho_note(yid_word, trans):
    notes = []
    p = trans.lower()
    nw = norm_yid(yid_word)

    if 'אָ' in yid_word:   # kamets-alef
        if 'u' in p:
            notes.append(
                'kamets-alef (RULE 1): [u/u:] consistent with Doremidik '
                '(YCD: zaogn [zogn]→[zugn], alemol [mol]→[mu:l])')
        else:
            notes.append(
                'kamets-alef present: expected Doremidik [u/u:] per RULE 1 '
                '(YCD: zaogn [zogn]→[zugn]); provided lacks [u]')

    if re.search(r'[ײ]|יי', yid_word):    # yud-beys
        if 'ay' in p:
            notes.append(
                'yud-beys (RULE 2): [ay] consistent with Doremidik '
                '(YCD: alef-beys [beyz]→[bays])')
        elif 'ey' in p:
            notes.append(
                'yud-beys present: expected Doremidik [ay]; '
                'provided has [ey] (RULE 2)')

    if nw in ('פונ', 'פנ'):               # fun — use norm_yid forms (medial letters)
        if p.startswith('fin'):
            notes.append('fun (RULE 3): [fin] correct Doremidik (YCD: fin-alef|biz-bays)')
        else:
            notes.append('fun (RULE 3): expected [fin]; has [' + p + '] (YCD: doremidik: [fin-alef|biz-bays])')

    if nw == 'אונ':                        # un
        if p == 'in':
            notes.append('un (RULE 4): [in] consistent with Doremidik (cf. fun→fin)')
        elif p == 'un':
            notes.append('un (RULE 4): expected Doremidik [in]; has [un]')

    if nw == 'אויפ':                       # oyf — norm_yid form (medial pe)
        if 'of' in p:
            notes.append('oyf (RULE 5): [of] correct Doremidik (YCD: oyf hefker [af]→[of])')
        elif 'af' in p:
            notes.append('oyf (RULE 5): expected Doremidik [of]; has [af]')

    return '; '.join(notes)


def vowel_diff(p, d):
    r = []
    if 'ay' in d and 'ey' in p:
        r.append('RULE 2: Doremidik has [ay]; provided has [ey]')
    if 'ey' in d and 'ay' in p:
        r.append('RULE 2: Doremidik has [ey]; provided has [ay]')
    if 'fin' in d and 'fun' in p:
        r.append('RULE 3: Doremidik [fin]; provided has [fun]')
    if re.search(r'\bin\b', d) and re.search(r'\bun\b', p):
        r.append('RULE 4: Doremidik [in]; provided has [un]')
    dv = re.sub(r'[^aeiou]', '', strip_len(d))
    pv = re.sub(r'[^aeiou]', '', strip_len(p))
    if dv and pv and dv != pv:
        if 'u' in dv and 'o' in pv:
            r.append('RULE 1: Doremidik has [u]; provided has [o]')
        elif 'u' in pv and 'o' in dv:
            r.append('RULE 1: provided [u] consistent with Doremidik')
    return r


def analyze(provided, dor, exact):
    if not (exact and dor):
        return ''
    dor_variants = [
        normalize_stress(exp)
        for raw_var in re.split(r',\s*', dor)
        for exp in expand_dor(raw_var.strip())
    ]
    prov_norm = normalize_stress(provided)
    if any(strip_len_keep_colon(dv) == strip_len_keep_colon(prov_norm) for dv in dor_variants):
        return 'exact Doremidik match'
    if any(strip_len(dv) == strip_len(prov_norm) for dv in dor_variants):
        return 'matches Doremidik (vowel length may differ)'
    return f'differs from Doremidik [{_display_dor(dor)}]'


# ── parenthetical expansion ───────────────────────────────────────────────────

_INT_OPT = re.compile(r'\(([^)]*)\)')   # interior (X) → optional X


def _expand_interior(form):
    """Recursively expand interior (X) optional groups → list of strings."""
    m = _INT_OPT.search(form)
    if not m:
        return [form]
    before, opt, after = form[:m.start()], m.group(1), form[m.end():]
    results = []
    for v in (before + after, before + opt + after):
        results.extend(_expand_interior(v))
    # deduplicate while preserving order
    seen_e: set = set()
    return [x for x in results if not (x in seen_e or seen_e.add(x))]  # type: ignore


def expand_dor(form):
    """Expand all optional-element notations in a Doremidik form.

    Handles two YCD notations:
      • Interior optional  –  b(ə)áys  →  báys, bəáys
      • Initial optional   –  h)akhlú:tə)  →  akhlú:tə, hakhlú:tə
        (YCD writes X)rest) to mean optional initial X)
    """
    if not form:
        return []
    # Strip phrase-level pipe separators – take only the first segment
    form = form.split('|')[0].strip()

    # Detect initial-optional pattern: X)rest) at start of string
    m_init = re.match(r'^([A-Za-zÀ-ɏə:]+)\)(.+)\)$', form)
    if m_init:
        init, rest = m_init.group(1), m_init.group(2)
        bases = [rest, init + rest]
    else:
        bases = [form]

    results = []
    for b in bases:
        results.extend(_expand_interior(b))

    seen_e: set = set()
    return [x for x in results if not (x in seen_e or seen_e.add(x))]  # type: ignore


# ── stress-mark normalization ─────────────────────────────────────────────────
# Rules (user-specified):
#   1 non-schwa vowel  → no accent
#   2 non-schwa vowels → acute on one (unambiguous only when an accent already present)
#   3+ vowels          → acute + grave (only normalize when both already present)
# Schwa (ə) is excluded from the vowel count.

_VOWEL_SET   = set('aeiouáàéèíìóòúù')
_ACUTE_SET   = set('áéíóú')
_GRAVE_SET   = set('àèìòù')
_GRAVE_TO_ACUTE = str.maketrans('àèìòù', 'áéíóú')
_STRIP_ACCENT   = str.maketrans('áàéèíìóòúù', 'aaeeiioouu')


def _vowel_count(s):
    return sum(1 for c in s if c in _VOWEL_SET)


def normalize_stress(form):
    """Normalize accent marks on expanded Doremidik forms per vowel-count rules."""
    n = _vowel_count(form)
    if n == 1:
        # Single non-schwa vowel: stress is implied, no diacritic needed
        return form.translate(_STRIP_ACCENT)
    if n == 2:
        has_acute = any(c in _ACUTE_SET for c in form)
        has_grave = any(c in _GRAVE_SET for c in form)
        if has_grave and not has_acute:
            # Grave marks the stressed vowel; promote to acute
            return form.translate(_GRAVE_TO_ACUTE)
        return form
    # 3+ vowels: leave as-is unless both accents already present (unambiguous)
    return form


_INIT_OPT_RE = re.compile(r'^([A-Za-zÀ-ɏə:]+)\)(.+)\)$')


def _display_dor(raw):
    """Convert internal X)rest) initial-optional notation to readable (X)rest."""
    m = _INIT_OPT_RE.match(raw)
    return f'({m.group(1)}){m.group(2)}' if m else raw


def _strip_no_stress(s):
    """Strip accent diacritics and length colons for stress-blind comparison."""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[: ]', '', s).lower()


def _strip_stress_keep_length(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return s.replace(' ', '').lower()


def analyze_no_stress(provided, expanded_parts):
    """Return 'match' if provided matches any expanded variant after stress-stripping."""
    pn = _strip_no_stress(provided)
    return 'match' if any(_strip_no_stress(dv) == pn for dv in expanded_parts) else ''


# ── secondary index: Latin transcription → entries ───────────────────────────
# Used as fallback when Hebrew-key lookup finds nothing.
# Keys are _strip_no_stress of each expanded Doremidik variant.

print("Building transcription index...")
trans_index: dict = {}
for _key, _entries in index.items():
    for _phrase, _dor, _wc in _entries:
        if _wc != 1 or '|' in _dor:   # phrase entries cause false positives
            continue
        for _raw_var in re.split(r',\s*', _dor):
            for _exp in expand_dor(_raw_var.strip()):
                _nk = _strip_no_stress(_exp)
                if _nk and len(_nk) >= 3:
                    trans_index.setdefault(_nk, []).append((_phrase, _dor, _wc))
print(f"  {len(trans_index)} normalized transcription keys")


def lookup_by_trans(galkhes):
    """Return (dor_raw, headword_phrase) by matching normalized galkhes against
    expanded+accent-stripped Doremidik variants. Returns (None, None) if no match."""
    nk = _strip_no_stress(galkhes)
    if not nk or len(nk) < 3 or nk not in trans_index:
        return (None, None)
    # Prefer single-word entries; break ties by shortest phrase
    best = sorted(trans_index[nk], key=lambda e: (e[2], len(e[0])))[0]
    return (best[1], best[0])


# ── read pre-aligned input CSV ────────────────────────────────────────────────
# text-and-transcription.txt is now a CSV with columns:
#   Section, Serial, Oysyes, Galkhes, Connection
# Alignment and compound labelling are already done in the input.

print("Reading input CSV...")
rows = []
seen_oysyes: set = set()
with open(TEXT_FILE, encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    next(reader)  # skip header row
    for in_row in reader:
        if len(in_row) < 4:
            continue
        section       = in_row[0].strip()
        serial        = in_row[1].strip()
        oysyes        = in_row[2].strip()
        galkhes       = in_row[3].strip()
        _conn_raw = in_row[4].strip() if len(in_row) > 4 else ''
        _conn_map = {
            'first element of compound word':  '1st',
            'middle element of compound word': 'middle',
            'second element of compound word': 'last',
        }
        connection = _conn_map.get(_conn_raw, _conn_raw)

        if len(norm_yid(oysyes)) < 2:
            continue
        if oysyes in seen_oysyes:
            continue
        seen_oysyes.add(oysyes)

        dor_form, dor_t, exact, headword = lookup(oysyes)
        trans_found = False
        if not dor_form:
            dor_t_fb, hw_fb = lookup_by_trans(galkhes)
            if dor_t_fb:
                dor_form = dor_t_fb
                dor_t    = dor_t_fb
                headword = hw_fb
                exact    = True
                trans_found = True

        col_analysis = analyze(galkhes, dor_t, exact)
        if trans_found:
            note = 'found via transcription match'
            col_analysis = (col_analysis + '; ' + note) if col_analysis else note

        ycd_dor_raw = dor_form or ''
        ycd_dor_display = _display_dor(ycd_dor_raw) if ycd_dor_raw else ''

        expanded_parts: list = []
        if ycd_dor_raw:
            for raw_var in re.split(r',\s*', ycd_dor_raw):
                for exp in expand_dor(raw_var.strip()):
                    expanded_parts.append(normalize_stress(exp))
        expanded_dor = ', '.join(expanded_parts)

        col_no_stress = analyze_no_stress(galkhes, expanded_parts)

        pn_keep_len = _strip_stress_keep_length(galkhes)
        if any(_strip_stress_keep_length(dv) == pn_keep_len for dv in expanded_parts):
            continue

        rows.append([
            section, serial, oysyes, galkhes, connection,
            ycd_dor_display, expanded_dor, headword or '', col_no_stress, col_analysis,
        ])

def _category(r):
    # r: [section, serial, oysyes, galkhes, connection, ycd_dor, expanded, headword, no_stress, analysis]
    ycd_dor, analysis = r[5], r[9]
    found = bool(ycd_dor)
    if found and 'differs from Doremidik' in analysis:
        return 'a'
    if found and analysis == 'exact Doremidik match':
        return 'c'
    if found:
        return 'b'
    if analysis:
        return 'd'
    return 'e'


_CAT_ORDER = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}


def _sort_key(r):
    cat = _category(r)
    try:
        sec = int(r[0])
    except ValueError:
        sec = 0
    try:
        ser = int(r[1])
    except ValueError:
        ser = 0
    return (_CAT_ORDER[cat], sec, ser)


rows.sort(key=_sort_key)

# Prepend category column
rows = [[_category(r)] + r for r in rows]


with open(OUTPUT, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow([
        'category', 'section', 'serial', 'oysyes', 'galkhes', 'compound_position',
        'ycd_doremidik', 'expanded_doremidik', 'ycd_headword', 'analysis_no_stress', 'analysis',
    ])
    w.writerows(rows)

print(f"Written {len(rows)} rows -> {OUTPUT}")
