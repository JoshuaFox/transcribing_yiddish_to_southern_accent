# Change log — Doremdik transcription

**Standard:** Yiddish Cultural Dictionary (YCD), **דרומדיק only**. Vowel length in Central Yiddish (CY = Doremdik) comes from the L.O.K.SH.N Guide to Vowel Length (`LOKSHN-length.pdf`) and its companion database (`Companion database for L.O.K.SH.N Guide to Vowel Length.xlsx`). Where YCD gives a Doremdik form, it wins. Where YCD is silent, the guide decides. Recent loans, foreign names and coinages are not shifted.

## Files and passes

| File | What it is |
|---|---|
| `FullTranscription0.txt` | Earliest version (formerly `FullTranscription.txt`, restored from git). |
| `FullTranscription1.txt` | Original transcription used as the base for pass 1 (unchanged). |
| `FullTranscription2.txt` | Output of pass 1 (50 changes). Word-for-word identical to the earlier `FullTranscription_corrected.txt`. |
| `FullTranscription3.txt` | Output of pass 2 (259 changes). |
| `FullTranscription4.txt` | Output of pass 3 (15 changes: voicing assimilation, plus one correction). |
| `FullTranscription5.txt` | Output of pass 4 (41 changes: prefix assimilation and devoiced אַז/איז/ביז). |
| `FullTranscription7.txt` | Output of pass 5 (7 changes: word-final devoicing). **Current version.** (There is no `FullTranscription6.txt`.) |

**Method (all passes).** Every transcription word was aligned to its Yiddish word in `FullTextEnglishAndYiddish.txt`, comparing same-numbered paragraphs. Each word was checked against the YCD `[std], דרומדיק: [dor]` pairs (26,712 mined; `dictionary_index.json`) and the rules in `DoremdikRules.md`. Pass 2 also looked up each word in the L.O.K.SH.N database, with prefixes and endings stripped. The database has 2,816 words, and 1,662 text tokens matched. The guide's rules were applied to the rest.

**How length shows in Doremdik spelling** (LOKSHN p.2):
- Stressed short [o] = `o`; long [o] = `u(:)`.
- Short [e] = `e`; long [e] = `ey`.
- Short [i]/[u] = `i`; long [i]/[u] = `i:`.

So length is not only a colon. It also decides `o` vs `u`, and `e` vs `ey`.

---

## Pass 5: FullTranscription5 → FullTranscription7 (7 word-tokens)

Scope: word-final devoicing of ordinary words. The rule and the YCD counts are in `VoicingAssimilationReport.md` §6.

In YCD's Doremdik forms, a final ב, בֿ, ד, ג, ז or װ becomes voiceless (`vèg` → `vèyk`). The exception: when the next sound is a voiced obstruent (b, d, g, z) or v, it stays voiced. This holds across a space as well as inside compounds (kept : devoiced is 73 : 2 before a voiced obstruent, 26 : 3 before v). Before a voiceless consonant, the final consonant is devoiced.

| ¶ | Yiddish | was | now | reason | YCD evidence |
|---|---|---|---|---|---|
| 14 | ערד באַ… | `eyrt bays` | `eyrd bays` | b follows; keep voiced | `liməd zkhis`, `hakuvəd boyray` |
| 11 | רינג דרײַ | `rink dra:` | `ring dra:` | d follows; keep voiced | `aveg geybm`, `masəg gvil` |
| 13 | װעג גלײַך | `veyk gla:kh` | `veyg gla:kh` | g follows; keep voiced | `breyg vasər` |
| 12 | ראַנד װאַלד | `rant valt` | `rand valt` | v follows; keep voiced | `laməd vuf` (14 : 1) |
| 7 | װאַלד װאָס | `valt vu:s` | `vald vu:s` | v follows; keep voiced | as above |
| 11 | קרײַז פֿון | `kra:z fin` | `kra:s fin` | voiceless f follows; devoice | `kras sht…` |
| 8 | מקריבֿ קרבנות | `makrəv kórbu:nəs` | `makrəf kórbu:nəs` | voiceless k follows; devoice | `khayəv-kórəs` → `khà:yəf-kú:rəs` |

**Not changed:**
- The other 55 devoiced finals (before a pause, a vowel, a sonorant or a voiceless consonant).
- Finals kept voiced before a voiced consonant: `halb-gəzéyənə`, `khoyshəd gəveyn`, `lav-dáfkə`, `váld-dakh`, `zúg-dorf`, `kra:z vi`.
- ב/ז before a vowel or sonorant, where YCD keeps them voiced or is split: `oyb`, `va:b`, `bloyz`, `nú:mənloz`, `gru:z`, `miz`.
- The name `hàseg` and the invented `zug`.

---

## Pass 4: FullTranscription4 → FullTranscription5 (41 word-tokens)

This pass resolves the "open" items from pass 3. The full table is in `VoicingAssimilationReport.md` §5.

- **אױס־, נאָך־, אַװעק־, צוריק־ + ג are now assimilated, following YCD (15 tokens).**
  - `ó:sg-` → `ó:zg-` (8): YCD has 40 assimilated to 3 not, e.g. `ó:(u)z-gèybm`, `ó(u)əz-gəprift`.
  - `núkhg-` → `núghg-` (2): YCD has `nugh-gèybm`, 5 to 0.
  - `avékg-` → `avégg-` (3): YCD has `aveg-geybm`, 6 to 1.
  - `tsiríkg-` → `tsirígg-` (2): by analogy with אַװעק־.
- **אָפּ־ + ג: `úpg-` → `úbg-` (9).** This follows YCD's majority form, `ub-geybm` (30 to 22).
- **דורך־ + ג: `dórəkhg-` → `dórəghg-` (3).** YCD is split 2 to 2. Like נאָך־, the prefix ends in a fricative, and fricative-final prefixes assimilate. YCD has `adórəgh-gevàykt`.
- **אַז / איז / ביז / ס׳איז (14).** YCD writes `as`, `is`, `bis` before a pause or a voiceless consonant (`az` → `as` 16 of 18, all phrase-final; `bis pí:rəm`), and keeps `z` before vowels and voiced sounds (`az hú:rəs`, `iz bay`, `biz bays`). The same rule is applied here: as ×6, is ×6, bis ×1, sis ×1. The other 59 tokens stay `az`/`iz`/`biz`/`siz`.

**Still deliberately unchanged:**
- final devoicing of content words (`kra:z`, `gru:z`, `bloyz`, `miz`, `nú:mənloz`);
- `n→m`;
- `ksá:f-yadn`, `əgeygn`.

---

## Pass 3: FullTranscription3 → FullTranscription4 (15 word-tokens)

Scope: regressive voicing assimilation. The full inventory, the rule and the YCD counts are in `VoicingAssimilationReport.md`. The rule followed here: YCD's Doremdik writes voicing assimilation **inside a word and before endings** almost without exception (ג+ט → `kt` 62 : 0; ־ות+דיק → `-əzdik` 320 : 2; ח/כ + voiced → `gh` 184 : 28). Pass 3 fixes the words that broke this rule, plus one consonant error.

| ¶ | Yiddish | was | now | reason | YCD evidence |
|---|---|---|---|---|---|
| 1, 10 | מקדשים | `bòtay-mikdú:shəm` | `bòtay-migdú:shəm` | ק+ד → `gd` | `bays-(h)amigdəsh` |
| 13, 14 | מיקדש | `bays-míkdəsh` | `bays-mígdəsh` | ק+ד → `gd` | `bays-(h)amigdəsh` |
| 1 | אױפֿגעשװעבט | `ó:vgəshveybt` | `ó:vgəshveypt` | ב+ט → `pt` | `gəléypt`, `dərléypt` |
| 3, 9 | ליגט | `ligt` | `likt` | ג+ט → `kt`; ¶11 already had `likt` | 62 `kt` : 0 `gt` |
| 12 | געזאָגט | `gəzu:gt` | `gəzu:kt` | ג+ט → `kt`; the other 5 tokens already had `gəzu:kt` | `gəzúkt` |
| 11 | דערװעגט | `dərveygt` | `dərveykt` | ג+ט → `kt` | `dervéykt-kàyt` |
| 14 | געפּרוּװט | `gəpri:vt` | `gəpri:ft` | װ+ט → `ft` | `məprift`, `ó(u)əz-gəprift` |
| 5 | חושכדיקע | `khóyshəkhdikə` | `khóyshəghdikə` | כ+ד → `ghd`, like `bərághvəzdikə` and `tághbiləs` | 184 `gh` : 28 `kh` |
| 11 | גוססדיק | `góysəsdik` | `góysəzdik` | ־ס+דיק → `zd`, like the six other `-əzdik` words | 320 : 2 |
| 9 | האַדקע | `hadkə` | `hatkə` | ד+ק → `tk` inside a word | `shatkhú:nəs` (שדכנות) |
| 13 | קרײַזטורעם | `krá:ztirəm` | `krá:stirəm` | ז+ט → `st` at a compound boundary | `dervékt-kàyt`, `yí:(ə)t-kày` |
| 11 | מאַזשעװאַטע | `mashəvátə` | `mazhəvátə` | **Not assimilation.** The spelling has זש before a vowel, so `zh`; nothing triggers devoicing | — |

**Not changed in pass 3, at your request:**
- The corner cases `ksá:f-yadn` and `əgeygn`.
- Final devoicing and `n→m` (`hobm`).

**Open, needs your decision** (resolved in pass 4). These prefixes disagree with YCD, but were left because the request was to fix only inconsistencies within the transcription:
- `ó:sgə-` (8 tokens; YCD `ó:zgə-`, 40 : 3).
- `núkhgə-` (2; YCD `nughgə-`, 5 : 0).
- `avékgə-` (3; YCD `aveggə-`, 6 : 1).
- `tsiríkgə-` (2; by analogy with אַװעק־).
- YCD's final devoicing in `az`/`biz`/`iz` (`as` 22 : 2).

`úpgə-` and `dórəkhgə-` are acceptable as written, because YCD gives both forms.

---

## Pass 2: FullTranscription2 → FullTranscription3 (259 word-tokens)

Pass 2 found no new errors introduced by pass 1. All 50 pass-1 changes agree with the guide (`ort`/`dort` short, `ú:n-` long, `sóf` short, `farbórgənə` short, etc.). Every pass-2 error was already in `FullTranscription1.txt`. Pass 1 had treated vowel length as unknowable from YCD and left it alone.

### L1. Short [o] is /ɔ/ = `o`, not `u` (174)

LOKSHN p.4 rules (13 V+{p,k,f,ts,s,kh}; 11 V+{m,n,l}+C; 9 Vr+C; exception lists `דאָזיק`, `לאָזן`, `־לאָז`, `אָבער`, `גאָט`; 2 Slavic), key verb `האָבן` (p.5: short in all inflected forms; only the infinitive and gerund are long), and database entries `האָט`, `כאָטש`, `װאָלט`, `זאָלן`, `אָדער` (= or), `אָפֿט`, `גאָלדן`, `שלאָס`, `פֿאָלק`, `דאָרף`, `פּאַװאָליע`. YCD agrees where it has the word: `vos-hòt`→`vus-òt`, `zòl-gót`→`zòl-gót`, `lòz`→`lòz`/`lòs`, `fólk`, `góld`. YCD’s Doremdik `hubm` occurs only in infinitive entries (`hòbm-bətókhn`→`h)ùbm-bətúkhn)`), which the guide also makes long; every האָבן in this text is finite. The two YCD rows that looked like long אָדער are the month אדר (Adar), not “or”.

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| האָט | `hut` | `hot` | 65 | 1:3, 1:34, 1:152, 1:182, 2:2, 2:23, 2:33, 2:39, 2:121, 2:135 … |
| האָבן | `hubm` | `hobm` | 34 | 1:88, 2:65, 3:55, 3:67, 3:74, 5:31, 5:51, 5:57, 5:77, 7:80 … |
| אָבער | `ubər` | `obər` | 11 | 2:89, 3:52, 5:146, 6:19, 6:76, 7:96, 7:144, 9:45, 12:166, 14:45 … |
| אָדער | `u:dər` | `odər` | 6 | 2:21, 2:27, 2:144, 3:159, 3:167, 11:121 |
| װאָלטן | `vultn` | `voltn` | 6 | 6:72, 8:30, 11:114, 11:230, 14:128, 14:155 |
| כאָטש | `khutsh` | `khotsh` | 5 | 2:17, 7:59, 7:155, 10:131, 14:172 |
| זאָל | `zul` | `zol` | 5 | 5:70, 6:38, 11:78, 14:167, 14:252 |
| װאָלט | `vult` | `volt` | 4 | 6:63, 7:61, 9:155, 11:141 |
| דאָרף | `durf` | `dorf` | 3 | 8:38, 8:159, 11:102 |
| דאָזיקן | `dúzikn` | `dózikn` | 2 | 5:18, 8:73 |
| אָדער | `udər` | `odər` | 2 | 5:134, 14:71 |
| דאָזיקע | `dúzikə` | `dózikə` | 2 | 6:3, 12:47 |
| געלאָזט | `gəluzt` | `gəlozt` | 2 | 6:127, 11:24 |
| געװאָלט | `gəvult` | `gəvolt` | 2 | 11:232, 12:174 |
| לאָזן | `luzn` | `lozn` | 2 | 13:166, 14:285 |
| גאָלדן | `guldn` | `goldn` | 1 | 1:31 |
| שטאָציקע | `shtútsikə` | `shtótsikə` | 1 | 1:84 |
| קאַיאָר | `kayúr` | `kayór` | 1 | 2:62 |
| אָפּלאָז | `úplus` | `úplos` | 1 | 3:64 |
| שלאָס | `shlus` | `shlos` | 1 | 4:85 |
| געשאָקלט | `gəshuklt` | `gəshoklt` | 1 | 5:32 |
| ס׳ | `svult` | `svolt` | 1 | 5:42 |
| גאָטלאָזיקע | `gútlùzikə` | `gótlòzikə` | 1 | 5:164 |
| שטימלאָזע | `shtímluzə` | `shtímlozə` | 1 | 5:294 |
| שׂכללאָזע | `sáykhlluzə` | `sáykhllozə` | 1 | 5:297 |
| פֿאַרלאָזט | `farlúzt` | `farlózt` | 1 | 6:86 |
| געשלאָסן | `gəshlusn` | `gəshlosn` | 1 | 7:216 |
| ס׳ | `s’hut` | `s’hot` | 1 | 9:13 |
| אָט | `ut` | `ot` | 1 | 9:51 |
| אָנגעבאָטן | `ú:ngəbutn` | `ú:ngəbotn` | 1 | 9:62 |
| סאָק | `suk` | `sok` | 1 | 9:66 |
| װאָלקנס | `vulkns` | `volkns` | 1 | 9:181 |
| נאָמענלאָז | `nú:mənluz` | `nú:mənloz` | 1 | 10:139 |
| פֿאָלק | `fulk` | `folk` | 1 | 11:88 |
| פּאַװאָליע | `pàvúliə` | `pàvóliə` | 1 | 11:238 |
| פֿרימאָרגן | `frímurgn` | `frímorgn` | 1 | 12:77 |
| אָפֿט | `uft` | `oft` | 1 | 12:163 |
| אָפֿטלעכע | `uftləkhə` | `oftləkhə` | 1 | 13:77 |

### L2. Short perfect stems (17)

LOKSHN p.5: past participles with [o] where the infinitive has a different vowel are short: `געװאָרן` (װערן), `געקראָכן` (קריכן), `געװאָנדן` (װינדן), `געטראָפֿן` (טרעפֿן), `געװאָרפֿן` (װאַרפֿן), `דערשראָקן` (דערשרעקן), `(באַ)האָנגען` (הענגען).

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| געװאָרן | `gəvurn` | `gəvorn` | 7 | 1:17, 6:8, 8:175, 11:199, 12:37, 12:51, 14:137 |
| געקראָכן | `gəkrukhn` | `gəkrokhn` | 2 | 11:62, 12:137 |
| אַרומגעהאָנגען | `arímgəhùngən` | `arímgəhòngən` | 1 | 1:126 |
| אַנידערגעװאָרפֿן | `anídərgəvùrfm` | `anídərgəvòrfm` | 1 | 2:150 |
| געװאָנדן | `gəvundn` | `gəvondn` | 1 | 3:89 |
| אַראָפּגעװאָרפֿן | `arú:pgəvùrfm` | `arú:pgəvòrfm` | 1 | 9:87 |
| דערשראָקענע | `dərshrukənə` | `dərshrokənə` | 1 | 12:14 |
| דערשראָקן | `dərshrukn` | `dərshrokn` | 1 | 12:129 |
| באַהאָנגען | `bahúngən` | `bahóngən` | 1 | 14:15 |
| געטראָפֿן | `gətrufm` | `gətrofm` | 1 | 14:234 |

### L3. Adverbial נאָך is short (11)

LOKSHN minimal pair `נאָך (אַ ביסל)` short vs `(דער)נאָך` / prefix `נאָכ־` long; database: נאָך “still; more” short, “after” long. YCD shows both (`nokh` 7, `nukh` 5). Changed only where it means still / yet / another / even more; `nukh` kept for “after” (¶3 *afílə nukh dər ershtər*, ¶13 *nukh dem*) and in the `núkh-` prefixes.

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| נאָך | `nukh` | `nokh` | 11 | 1:21, 3:12, 3:20, 5:191, 7:222, 8:52, 10:29, 11:15, 12:143, 13:130 … |

### L4. Long [e] is `ey` (32)

Database long [e]; LOKSHN rules 7 (Vr+# long, 100%), 8 (er + dental/V), 15 (eb), 16 (Germanic e+g). YCD agrees where present: `vèrn`→`vèyrn` (89×), `hérn`→`héy(ə)rn`, `èrd`→`èyə(r)t`, `shtérn`→`shtéyrn`, `shtétl`→`shtéytl`, `kérn`→`kéyrn`. This reverses earlier hand-edits from `ey` to `e` (`vern`, `gertnər`, `shtetl`, `aher`).

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| ערד | `ert` | `eyrt` | 4 | 14:57, 14:177, 14:225, 14:272 |
| געהערט | `gəhert` | `gəheyrt` | 3 | 3:129, 10:16, 12:10 |
| װערן | `vern` | `veyrn` | 3 | 11:117, 14:170, 14:182 |
| גערטנער | `gertnər` | `geyrtnər` | 1 | 1:63 |
| אױפֿגעשװעבט | `ó:vgəshvebt` | `ó:vgəshveybt` | 1 | 1:155 |
| אױפֿרעגנדיקע | `ó:frègndikə` | `ó:frèygndikə` | 1 | 1:172 |
| אומערדישער | `ìmérdishər` | `ìméyrdishər` | 1 | 2:119 |
| ערנצט | `erntst` | `eyrntst` | 1 | 3:27 |
| שטערן | `shtern` | `shteyrn` | 1 | 4:71 |
| מעגלעך | `megləkh` | `meygləkh` | 1 | 5:144 |
| אױפֿרעגנדיקן | `ó:frègndikn` | `ó:frèygndikn` | 1 | 5:263 |
| איבערקלערנדיק | `íbərklèrndik` | `íbərklèyrndik` | 1 | 6:107 |
| אומדערקלערטע | `imdərklértə` | `imdərkléyrtə` | 1 | 7:69 |
| אַהער | `aher` | `aheyr` | 1 | 7:112 |
| נערן | `nern` | `neyrn` | 1 | 7:157 |
| שטערן | `shtèrn` | `shtèyrn` | 1 | 7:272 |
| צוגעהערט | `tsígəhert` | `tsígəheyrt` | 1 | 8:27 |
| גענערט | `gənert` | `gəneyrt` | 1 | 8:95 |
| עמעצער | `emətsər` | `eymətsər` | 1 | 9:82 |
| אָפּגעקערט | `úpgəkert` | `úpgəkeyrt` | 1 | 11:145 |
| געהעריקן | `gəhérikn` | `gəhéyrikn` | 1 | 12:6 |
| װערט | `vert` | `veyrt` | 1 | 12:40 |
| שטעטל | `shtetl` | `shteytl` | 1 | 13:137 |
| פֿאַרװערטן | `farvértn` | `farvéyrtn` | 1 | 13:238 |
| שװער | `shver` | `shveyr` | 1 | 14:131 |

### L5. Long [i]/[u] is `i:` (23)

Database long: `זוכן`, `רופֿן`, `שפּירן`, `פֿליסן`, `פּרוּװן`, `שמועס`, `אַהין`, `פֿוס`→`פֿיס`; LOKSHN rule 13 exception `טיף` (long); rule 4 V+{V,#} long (`גלי`); loshn-koydesh rule 2 V+V long (`שקיעה`, `נבֿיאיש`). YCD agrees: `zúkh`→`zí:kh`, `úf-ruf`→`ó:(u)f-rì:f`, `shmúəs`→`shmí:əs`. The text already writes long i with `:` (`li:bləkh`, `gi:khər`, `fri:ər`, `ri:rt`), so these follow its own convention.

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| שקיעה | `shkíə` | `shkí:ə` | 4 | 2:114, 3:18, 4:12, 6:55 |
| װוּאַהין | `vìahín` | `vìahí:n` | 2 | 4:42, 5:205 |
| שמועות | `shmiəs` | `shmi:əs` | 2 | 7:70, 9:135 |
| שקיעה | `shkiə` | `shkí:ə` | 1 | 1:39 |
| אומבאַזוכטן | `ìmbazíkhtn` | `ìmbazí:khtn` | 1 | 1:134 |
| אױפֿגערופֿן | `ó:vgərifn` | `ó:vgəri:fn` | 1 | 2:41 |
| נבֿיאיש | `nəvíish` | `nəví:ish` | 1 | 2:69 |
| טיפֿערן | `tifərn` | `ti:fərn` | 1 | 6:123 |
| אָפּרופֿן | `úprufm` | `úpri:fm` | 1 | 8:32 |
| נאָכגעשפּירט | `núkhgəshpirt` | `núkhgəshpi:rt` | 1 | 8:81 |
| דורכשמועס | `dórəkhshmiəs` | `dórəkhshmi:əs` | 1 | 9:102 |
| פֿליסט | `flist` | `fli:st` | 1 | 11:37 |
| פֿיס | `fis` | `fi:s` | 1 | 11:180 |
| גלי | `gli` | `gli:` | 1 | 12:66 |
| באַזוכט | `bazíkht` | `bazí:kht` | 1 | 13:19 |
| נאָכשפּירנדיקע | `núkhshpirəndìkə` | `núkhshpi:rəndìkə` | 1 | 13:89 |
| אױסגעזוכט | `ó:sgəzikht` | `ó:sgəzi:kht` | 1 | 13:228 |
| געפּרוּװט | `gəprivt` | `gəpri:vt` | 1 | 14:266 |

### L6. Short [u] in a loshn-koydesh word (1)

Database `משונה` short; YCD `məshínə-dikə`.

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| משונהדיקע | `məshí:nədikə` | `məshínədikə` | 1 | 8:196 |

### L7. אָפּ־ is `úp-` (1)

YCD `óp-`→`úp-` (92 of 101); LOKSHN lists `אָפּ־/אַראָפּ` as long exceptions. `ópgrintn` (¶7) was the only `óp-` left in the text.

| Yiddish | was | now | count | ¶:word# |
|---|---|---|---|---|
| אָפּגרונטן | `ópgrintn` | `úpgrintn` | 1 | 7:273 |

### Conflicts and judgement calls in pass 2 (not changed)

- **נאָר `nur` (10×): YCD vs the guide.**
  - The guide and database say short (`nor`).
  - YCD has `נאָר װאָדען [nòr|vòdén], דרומדיק: [nù:ə(r)|vù:dé(y)n]`.
  - YCD wins, so `nur` stays. Change it to `nor` if you prefer the guide.
- **ערשט `ershtər`.** The database says long. YCD has both `è(y)rshtə(r)` and `érshtə(r)`, so `ershtər` stays.
- **Words attested with both lengths** (database `*`): `dərmunt` (דערמאָנען), `tsentər`, `ó:sgəlernt` (לערנען), `tumər` (טאָמער), `víkhərndikər`. Left as written.
- **Unstressed function words are never long** (LOKSHN p.2; p.7 pronoun table). `er`, `dem`, `dər`, `di`, `im`, `ir`, `zi`, `vi` are right when unstressed. Only a stressed use would take `eyə(r)`, `deym`, `di:`, etc.
- **Database false matches**, checked by hand and left alone:
  - `béytndik` (בעטן "ask", long): correct.
  - `zeyt` ("sees", long): correct.
  - `net` ("neat", short): correct.
  - `tsətribm` (short perfect of טרײַבן): correct.
  - `dinəm` (דין "thin", short): correct.
  - `ertər` (plural of אָרט, short): correct.
- **`tsəridərt`** (צערודערט). The database's `רודערן` ("row") is long. It is not certain that צערודערט ("agitated") is the same word, so it was not changed.
- **אָפּ־ written `úp-` without a colon.** The guide says long. YCD writes `úp-`, and the `u` already carries the length, so it was left as is.
- **Names, loans and coinages.** No length shifts were applied (`últar`, `kuránəs`, `zugn`, `sultán`, `tunéln`, `plyushtsh`, `urnəs`, `kontúrn`, `históryə`, …). The guide notes that newer loans keep `u` and short `o`.
- **YCD check of Hebrew-origin words.** No errors beyond L6. The remaining differences were length colons only (e.g. `brú:khə` vs YCD `brúkhə`), and the guide confirms these vowels as long.

---

## Pass 1: FullTranscription1 → FullTranscription2 (50 word-tokens)

| ¶ | word # | Yiddish | was | now | rule |
|---|---|---|---|---|---|
| 1 | 155 | אױפֿגעשװעבט | `ó:fgəshvebt` | `ó:vgəshvebt` | R2 |
| 1 | 157 | רירנדיקײט | `rírndikà:t` | `rírndikàyt` | R6 |
| 1 | 177 | אָרט | `urt` | `ort` | R10 |
| 2 | 41 | אױפֿגערופֿן | `ó:fgərifn` | `ó:vgərifn` | R2 |
| 2 | 117 | שײנקײט | `sháynka:t` | `sháynkayt` | R6 |
| 2 | 143 | אָרט, | `urt,` | `ort,` | R10 |
| 2 | 151 | אָנסופֿיק | `únsòyfik` | `ú:nsòyfik` | R12 |
| 2 | 154 | אָרט | `urt` | `ort` | R10 |
| 3 | 8 | אױפֿגעװעקט | `ó:fgəvekt` | `ó:vgəvekt` | R2 |
| 3 | 31 | פֿאַרבאָרגענע | `farbúrgənə` | `farbórgənə` | R10 |
| 3 | 165 | פֿאַרבאָרגענעם | `farbúrgənəm` | `farbórgənəm` | R10 |
| 4 | 1 | סוף | `súf` | `sóf` | R9 |
| 4 | 3 | סוף | `suf` | `sof` | R9 |
| 4 | 34 | אָנגענומען | `úngənimən` | `ú:ngənimən` | R12 |
| 4 | 60 | אָרט | `urt` | `ort` | R10 |
| 5 | 157 | אָנגעהױבן | `úngəhoybm` | `ú:ngəhoybm` | R12 |
| 5 | 185 | אָרטיקע | `úrtikə` | `órtikə` | R10 |
| 5 | 194 | סוף | `súf` | `sóf` | R9 |
| 5 | 289 | אומגעהײַערע | `imgəháyərə` | `imgəhá:ərə` | R7 |
| 6 | 23 | אָנגענומען | `úngənimən` | `ú:ngənimən` | R12 |
| 6 | 118 | הונדערט | `hindərt` | `híndət` | R4 |
| 7 | 18 | פֿינצטערהײט | `fíntstərha:t` | `fíntstərhayt` | R6 |
| 8 | 26 | װײַלע | `vaylə` | `va:lə` | R7 |
| 8 | 112 | סוף | `súf` | `sóf` | R9 |
| 8 | 114 | סוף | `suf` | `sof` | R9 |
| 8 | 124 | אױפֿגעדעקט | `o:fgədəkt` | `o:vgədəkt` | R2 |
| 8 | 130 | אומגעהײַערקײט | `imgəháyərikà:t` | `imgəhá:ərikàyt` | R7 |
| 9 | 62 | אָנגעבאָטן | `úngəbutn` | `ú:ngəbutn` | R12 |
| 9 | 98 | אָנגעהױבן | `úngəhoybm` | `ú:ngəhoybm` | R12 |
| 10 | 39 | כּתבֿ | `ksáv` | `ksá:f` | R5 |
| 10 | 61 | בײַגעקומען | `báygəkimən` | `bá:gəkimən` | R7 |
| 10 | 76 | כּתבֿ | `ksáv` | `ksá:f` | R5 |
| 10 | 112 | אַרױפֿגעקלעטערט | `aró:fgəklètərt` | `aró:vgəklètərt` | R2 |
| 11 | 90 | אומגעהײערע | `imgəháyərə` | `imgəhá:ərə` | R7 |
| 11 | 140 | דאָרט | `durt` | `dort` | R10 |
| 11 | 154 | אָרט | `urt` | `ort` | R10 |
| 11 | 198 | אױפֿגעשטעלט | `ó:fgəshtelt` | `ó:vgəshtelt` | R2 |
| 12 | 3 | אָנגעלײגט | `úngəlaykt` | `ú:ngəlaykt` | R12 |
| 12 | 7 | אָרט, | `urt,` | `ort,` | R10 |
| 12 | 145 | הױז, | `hoyz,` | `hó:əs,` | R3 |
| 13 | 66 | הונדערט | `híndərt` | `híndət` | R4 |
| 13 | 78 | פֿאַראַנענקײט | `faránənkà:t` | `faránənkàyt` | R6 |
| 13 | 169 | אָרט. | `urt.` | `ort.` | R10 |
| 13 | 237 | אַרױפֿגעגאַנגען | `aró:fgəgàngən` | `aró:vgəgàngən` | R2 |
| 14 | 42 | בנוגע | `bənoygəyə` | `bənəgáyə` | R11 |
| 14 | 60 | שװאַכינקערהײט | `shvàkhínkərha:t` | `shvàkhínkərhayt` | R6 |
| 14 | 126 | אַרױפֿגײן | `aró:fgàyn` | `aró:vgàyn` | R2 |
| 14 | 136 | אַרױפֿגעצױגן | `aró:fgətsòygn` | `aró:vgətsòygn` | R2 |
| 14 | 220 | אױפֿן | `ofm` | `ofn` | R1 |
| 14 | 244 | כּתבֿ | `ksáv` | `ksá:f` | R5 |

### Evidence per rule (pass 1)

- **R1** — (not applied to בשום־אױפֿן/אופֿן `bəshím-oyfm`, which is Hebrew אופן — YCD `bəshúm|óyfm`→`bəshím|óyfm`; nor to `ofm` before a labial, `ofm bakántn`) אויף as preposition: [af]/[afn] → דרומדיק [of]/[ofn] (YCD: אויף [af], דרומדיק: [of] \ אויפן [afn], דרומדיק: [ofn]; "glá:kh|ofn-órt")
- **R2** — אויף- prefix before voiced g: [úv-gèbm] → דרומדיק [ó:(u)(ə)v-gèybm]; [úv-gənùmən] → [ó:(ə)v-gənìmən]; אַרויפגיין → [aró:(u)(ə)v-gàyn] (YCD: f→v before g; stays f before t/r/k/s)
- **R3** — הויז [hóyz] → דרומדיק [hó:(u)(ə)s] / compound [hò:(u)(ə)s] (YCD הויז entries)
- **R4** — הונדערט [húndərt] → דרומדיק [(h)índət] / [híndət-khàylək] (YCD)
- **R5** — כתב [ksáv] → דרומדיק [ksá(:)f] / [ksá:f] (YCD)
- **R6** — -קײט / -הײט suffixes: Std `-keyt`/`-heyt` → `-kàyt`/`-hayt` (ey→ay; 327 pairs for -kayt, 25 of 28 for -heyt: `ərhéyt`→`ərháyt`, `farbòrg(ə)nərhéyt`→`farbòrg(ə)nə(r)háyt`); so `-kà:t`, `-ha:t` → `-kàyt`, `-hayt`
- **R7** — ײַ → [a:] in native words (word-final, before r, before C) — applied only to `vaylə`, `baygəkimən`, `imgəhá:ərə`; **not** to the names `skay`, `nárgay`: [tnáy]-type finals → [a:] (YCD: tnáy→tná:, frày→frà:, hágay…); אומגעהײַער → [ìm-gəhá:(y)ə(r]; בײַ- (Germanic) → [ba:]
- **R9** — סוף [sof] keeps [o]: [àynsóf] → [àynsóf]; [ònasóf] → [ù(:)(ə)nasóf] (second element stays sóf)
- **R10** — Std `o` stays `o` before **r + t/b/d/s/v/g/k** (YCD: -rt 15/15, -rb 26/26, -rd 5/5, -rs 4/4, -rg 1/1, -rk 9/10) but goes to `u` before `-rn` (109/111) and `-rl` (11/11): applied to אָרט (`urt`→`ort`), דאָרט (`durt`→`dort`), פֿאַרבאָרגענע (`farbúrgənə`→`farbórgənə`, YCD `farbòrg(ə)nə(r)háyt`). Examples: [afn-órt] → [ofn-órt]; [àfanórt] → [òfanórt]; ווארט [vòrt] → [vòr(ə)t] [afn-órt] → [ofn-órt]; [àfanórt] → [òfanórt]; ווארט [vòrt] → [vòr(ə)t]
- **R11** — בנוגע [bənógəyə]-type → דרומדיק [bən(ə)gáyə] (YCD בנוגע)
- **R12** — Stressed אָנ- prefix [ón-]/[ón] → דרומדיק [ú:n-] with length marked (YCD: ón-dèynk → ú:n-dèynk; óngèbm → ú:ngèybm; ón|úf-hèr → ú:(ə)n|ó:(u)f-hèyə(r))

---

## Structural problems (not Doremdik forms — need your decision)

- **¶4 and ¶5 (rechecked after your edit; both lines are now complete).** ¶4: 88 Yiddish words ↔ 88 transcription words, every word aligned by initial letter, no gaps; it now ends `…dem óniksənəm shlus fin di groysə.` ¶5 is its own line: 311 Yiddish tokens ↔ 308 transcription words. Two of the three differences are not omissions: `svult` = ס׳ + װאָלט and `siz` = ס׳ + איז (clitics written as one word). The third is a real omission: Yiddish "…זינט צײַט האָט זיך אָנגעהױבן **זענען** אַמאָל אַריבער און צוריק…" has no `zenən` in your line (`…úngəhoybm mu:l aríbər in tsirík…`; the aligner shows it as a mismatch at `mu:l`/`און`). I did not add it. Only lines 4 and 5 were re-aligned and re-corrected; all other lines are unchanged from the first run.
- **¶8 word order differs from the current Yiddish.** Yiddish: "…װוּ סע דערצײלט װעגן אַ קרײַז גרױסע מאָכיקע שטײנער אין דעם װאָס איז אַ מאָל געװען אַ פּאָליאַנע פֿון עלטערע און נאָך שױן לאַנג פֿאַרגעסענע גרױליקע אײַנװױנערס". Transcription: "vi sə dərtsaylt veygn eltərə in nukh shoyn lank fargésənə gróylikə á:nvoynərs ə kra:z groysə mókhikə shtaynər vu:s iz ə mu:l gəveyn ə polyánə". Looks like an older draft of the translation.
- **¶8 `gəveyn kórbu:nəs`** in the Yiddish is "מקריבֿ געװען קרבנות"; your file now has "kórbu:nəs gəveyn" (your recent edit). Word order differs from the Yiddish.
- **¶14** Yiddish has "דער חכם" after "ברזַי"; transcription has no matching "dər khu:khəm" at that spot. Also "וכּמה" ↔ transcription "və kamə" has a different order from the Yiddish "כּמה וכּמה".

## Checked and deliberately left unchanged (both passes)

- **`dorəkh` / `dorəkhn` (דורך, preposition).** YCD: `דורך [du(r)kh], דרומדיק: [der(ə)kh]; אויך: [dor(ə)kh]`. Your `dorəkh` is the YCD "also" variant, so it is valid; `der(ə)kh` is listed first. For the prefix דורכ- YCD gives `dór(ə)kh-` (so `adórəkhgəgàngən`, `dórəkhgangən` are right).
- **`ma:nsəs`** (מעשׂיות): YCD has both `má:səs` and `má:(n)səs`; yours is valid.
- **Hyphenation/stress only** (e.g. `bəshú:ləmdik`, `màmú:shəzdik`): not changed. (`məshí:nədikə` was corrected in pass 2, L6.)
- **Hebrew-origin `oy` words** (`khóyshəkh`, `móyrə`, `sóydəs`, `óyləm`, `khóysəm`, `hóykhə`): YCD keeps `oy` — correct as written.
- **`ofm` vs `ofn`:** YCD has `ofmá:(n)` (אויף מײַן) so `ofm` is legitimate before a labial; I changed it only for אױפֿן ("on the…") where YCD has `ofn`.
- **Words with no Doremdik form in YCD** were left alone in pass 1. In pass 2 they were checked against the L.O.K.SH.N guide and database. The **e / ey** split is a length distinction (short [e] = `e`, long [e] = `ey`), so pass 2 restored `ey` where the guide or YCD shows a long vowel (L4). Words neither source covers keep your spelling.
- **Loan-word/proper-name `o` for אָ** (`rándolf`, `fontánən`, `kòlonádəs`, `dèmon`, `históryə`, `tserəmónyə`, `grotéskə`) left as `o`: YCD shows stressed loan `o` staying (`protsént`, `mənòritét`), but has no entry for these words.
- **`khalóyməs` (חלומות)**: YCD only has the singular `khóləm`→`khú:ləm`; the plural with `oy` is unverified. Not changed.
- **`kórbu:nəs`, `zəku:rn`, `sáku:nəs`** etc.: consistent with YCD `kórbm`→`kórbm`, `zəkórn`→`zəkú:rn`, `sakónə`→`sakú:nə`.
- **Recent loans, names and coinages: no sound shifts (R8 withdrawn; R7 withdrawn for names).** Doremdik applies its shifts to inherited and long-assimilated vocabulary; recently borrowed words keep their source vowels. Not shifted: the place and person names `últar`, `kuránəs`, `nárgay`, `skay`, the invented creature `zugn`/`zug` (Zoogs), and loans `sultán`, `tunéln`, `plyushtsh`, `urnəs` (none has a YCD entry). With those withdrawn, the u→i rule (R8) changes nothing in the text: the remaining `u`s (`hut`, `hubm`, `nukh`, `vult`, `gəvurn`, …) are the *result* of Std `o`→`u`, and the native Std-`u` words (`fun`, `un`, `úm-`, `úntər`) are already written `fin`, `in`, `ím-`, `íntər`.
- **Function words and prefixes checked against YCD (see `DoremdikRules.md` §2 and §6):** `fin`, `in`, `tsi`, `intər`, `ím-`, `ú:n-`, `úp-`, `á:n-` (אײַן-), `ará:n`, `aró:s`, `aró:f`, `arúp`, `arím`, `avék`, `dórəkh-`, `ibər`, `far`, `dər`, `bə`, `veygn`, `kayn`, `za:n`, `du:s`, `vu:s` all agree with YCD's Doremdik forms; nothing in these needed changing. Not changed because YCD gives no clear rule: `az` (YCD `as` in 23/25 phrase examples; context unrecoverable), `biz` (`bis` in only 6/17), `nukh`/`nokh` (both attested), unstressed `ba:` for בײַ (YCD `ba`; no בײַם data).
- **Pass 1, final re-check.** Re-aligned all 14 paragraphs against the Yiddish and re-ran every rule. Corrections to my own earlier output: (a) `bəshím-oyfm` in ¶14 had been changed to `bəshím-ofn`; it is בשום־אופן (Hebrew `oyfm`), so it is restored to `oyfm`. (b) `ofm bakántn` (¶14) restored to `ofm` (assimilation before the labial `b`, consistent with the note above). (c) ¶8 `imgəháyərikà:t` had lost its ײַ→`a:` step; it is now `imgəhá:ərikàyt`. (d) `o:fgədəkt` keeps its original unstressed `o:` (now `o:vgədəkt`), not `ó:vgədəkt`. New: `-ha:t` → `-hayt` (¶7 `fíntstərhayt`, ¶14 `shvàkhínkərhayt`), `durt` → `dort`, `farbúrgənə(m)` → `farbórgənə(m)`.
- **Left alone on purpose (pass 1):** `yú:rhindərt` (YCD writes `hìndə(r)t` with optional r, so `-hindərt` is acceptable) and `ba:` for בײַ (see above). `durf` and `gəvúrfm` were left in pass 1 but corrected in pass 2 (`dorf`, `gəvòrfm`; L1/L2).
- **Source oddities (not transcription errors):** the Yiddish ¶14 spells בשום־אױפֿן with `oy`, while ¶2 spells בשום־אופֿן; ¶11 אומגעהײערע lacks the pasekh that ¶5 and ¶8 have (I treated it as אומגעהײַערע, as in the other two); ¶5 has no `zenən` for זענען (before אַמאָל); ¶8 and ¶14 word-order mismatches listed in §3 are unchanged.
