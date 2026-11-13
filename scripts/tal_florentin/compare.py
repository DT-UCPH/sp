"""Align Tal & Florentin (MS Nablus 6) with CACCHT (MS Dublin CBL 751) chapter by chapter.

Usage: python compare.py results/tf_verses.json results/caccht_verses.json results

Reads the outputs of extract_tf.py and extract_caccht.py (incl. their _pages/_nodes/_meta files)
and writes OUTDIR/differences.md, OUTDIR/differences.tsv and OUTDIR/versification.tsv.
"""
import collections
import csv
import json
import os
import sys
from difflib import SequenceMatcher

A_FILE, B_FILE, OUTDIR = sys.argv[1:4]
A_BASE, B_BASE = os.path.splitext(A_FILE)[0], os.path.splitext(B_FILE)[0]


def load(path):
    return json.load(open(path, encoding='utf-8'))


tf, tf_pages, tf_meta = load(A_FILE), load(A_BASE + '_pages.json'), load(A_BASE + '_meta.json')
cc, cc_nodes, cc_meta = load(B_FILE), load(B_BASE + '_nodes.json'), load(B_BASE + '_meta.json')

BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
FINALS = str.maketrans('ךםןףץ', 'כמנפצ')
GUTTURALS = set('אהחע')

TYPES = collections.OrderedDict([
    ('plene/defective', 'The words differ only in a word-internal mater lectionis ו or י.'),
    ('conjunction waw', 'One edition has the conjunction ו prefixed, the other not.'),
    ('article he', 'One edition has a prefixed ה (article or interrogative), the other not.'),
    ('guttural interchange', 'Same length; the words differ only in the gutturals א/ה/ח/ע.'),
    ('aleph plus/minus', 'The words differ only in the presence of a (non-initial) א.'),
    ('final he/yod', 'The words differ only in a final ה versus final י (after removing internal matres).'),
    ('word division', 'Same letters, divided differently into words (e.g. בהר גריזים / בהרגריזים).'),
    ('plus T&F', 'Word(s) present only in Tal & Florentin.'),
    ('plus CACCHT', 'Word(s) present only in CACCHT.'),
    ('colophon (T&F only)', 'Scribal book-end colophon (…קצים…) printed by T&F, not part of CACCHT.'),
    ('probable CACCHT error', 'Reading in CACCHT that looks like a data-entry error.'),
    ('other', 'Any other difference (morphology, different lexeme, metathesis, several words, …).'),
])


def chapters(verses, nodes=None):
    out = collections.OrderedDict()
    for ref, words in verses.items():
        bk_ch = ref.rsplit(':', 1)[0]
        ns = nodes[ref]['words'] if nodes else [None] * len(words)
        out.setdefault(bk_ch, []).extend((w, ref, n) for w, n in zip(words, ns))
    return out


def skel(w):
    """Word without word-internal matres lectionis waw/yod (first and last letter kept)."""
    w = w.translate(FINALS)
    if len(w) <= 2:
        return w
    return w[0] + w[1:-1].replace('ו', '').replace('י', '') + w[-1]


def classify(a, b):
    if a and 'קצים' in a and not b:
        return 'colophon (T&F only)'
    if not a:
        return 'plus CACCHT'
    if not b:
        return 'plus T&F'
    ja, jb = ''.join(a), ''.join(b)
    if ja.translate(FINALS) == jb.translate(FINALS):
        return 'word division'
    if a == ['לך'] and b == ['ך']:
        return 'probable CACCHT error'
    if len(a) == len(b) and all(skel(x) == skel(y) for x, y in zip(a, b)):
        return 'plene/defective'
    if len(a) == len(b) == 1:
        x, y = a[0].translate(FINALS), b[0].translate(FINALS)
        if x == 'ו' + y or y == 'ו' + x:
            return 'conjunction waw'
        if x == 'ה' + y or y == 'ה' + x:
            return 'article he'
        if len(x) == len(y) and all(p == q or (p in GUTTURALS and q in GUTTURALS) for p, q in zip(x, y)):
            return 'guttural interchange'
        if skel(x)[:-1] == skel(y)[:-1] and {x[-1], y[-1]} <= set('הי'):
            return 'final he/yod'
        if x[0] + x[1:].replace('א', '') == y[0] + y[1:].replace('א', ''):
            return 'aleph plus/minus'
    return 'other'


A, B = chapters(tf), chapters(cc, cc_nodes)
diffs, verse_map = [], collections.OrderedDict()
for ch in B:
    a, b = A.get(ch, []), B[ch]
    # final/non-final letter forms are normalised for matching: CACCHT renders compound
    # names joined by "_" (e.g. BN_<MJ) as "בנ עמי", with a non-final letter
    sm = SequenceMatcher(None, [w.translate(FINALS) for w, _, _ in a],
                         [w.translate(FINALS) for w, _, _ in b], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for i, j in zip(range(i1, i2), range(j1, j2)):
                verse_map.setdefault(b[j][1], collections.Counter())[a[i][1]] += 1
            continue
        if op == 'replace' and (i2 - i1) == (j2 - j1) and (i2 - i1) > 1:
            pairs = [((i, i + 1), (j, j + 1)) for i, j in zip(range(i1, i2), range(j1, j2))]
        else:
            pairs = [((i1, i2), (j1, j2))]
        for (x1, x2), (y1, y2) in pairs:
            aw, bw = [w for w, _, _ in a[x1:x2]], [w for w, _, _ in b[y1:y2]]
            ref_b = b[y1][1] if y1 < y2 else b[max(y1 - 1, 0)][1]
            ref_a = a[x1][1] if x1 < x2 else (a[max(x1 - 1, 0)][1] if a else '')
            word_nodes = sorted({n for _, _, ns in b[y1:y2] for n in ns})
            # for a T&F plus: the CACCHT word node after which the T&F words stand
            after_node = b[y1 - 1][2][-1] if y1 == y2 and y1 > 0 else None
            diffs.append({'ref_caccht': ref_b, 'ref_tf': ref_a,
                          'page_tf': tf_pages.get(ref_a, ['', ''])[1],
                          'type': classify(aw, bw),
                          'tal_florentin': ' '.join(aw), 'caccht': ' '.join(bw),
                          'verse_node': cc_nodes[ref_b]['verse'],
                          'word_nodes': ' '.join(map(str, word_nodes)),
                          'after_word_node': after_node or ''})

versif = [(cref, ', '.join(sorted(m, key=lambda r: int(r.rsplit(':', 1)[1]))), cc_nodes[cref]['verse'])
          for cref, m in verse_map.items() if set(m) != {cref}]

# ---------------------------------------------------------------- TSV output
os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, 'differences.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(diffs[0]), delimiter='\t')
    w.writeheader()
    w.writerows(diffs)
with open(os.path.join(OUTDIR, 'versification.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['ref_caccht', 'ref_tf', 'verse_node'])
    w.writerows(versif)

# ---------------------------------------------------------------- Markdown output
n_diff_verses = len({d['ref_caccht'] for d in diffs})
by_type_book = collections.Counter((d['type'], d['ref_caccht'].split()[0]) for d in diffs)
by_type = collections.Counter(d['type'] for d in diffs)
by_book = collections.Counter(d['ref_caccht'].split()[0] for d in diffs)

md = []
md.append('# Differences between the running texts of Tal & Florentin (2024) and the CACCHT Samaritan Pentateuch\n')
md.append('This file lists every difference between the consonantal Hebrew text printed in Moshe Florentin and '
          'Abraham Tal, *The Samaritan Pentateuch: An English Translation with a Parallel Annotated Hebrew Text* '
          '(Open Book Publishers, 2024, https://doi.org/10.11647/OBP.0415), and the CACCHT Text-Fabric dataset of '
          'the Samaritan Pentateuch (https://github.com/DT-UCPH/sp, https://doi.org/10.5281/zenodo.7734632). '
          'It is generated by `compare.py`; do not edit it by hand.\n')

md.append('## Sources and versions\n')
md.append('| | Tal & Florentin (T&F) | CACCHT SP dataset |')
md.append('|---|---|---|')
md.append(f"| Manuscript | MS Nablus 6 (C), 1204 CE; gaps filled from St Petersburg P.177, Cambridge Add 714, "
          f"Oxford Bodl. Sam c2, BL Or 5036, Princeton Garrett and the Abisha scroll (Intro §4.1.2) | {cc_meta['manuscripts']} |")
md.append(f"| Version | PDF `{tf_meta['pdf']}`, SHA-256 `{tf_meta['sha256']}` | dataset version **{cc_meta['dataset_version']}** "
          f"(`{cc_meta['tf_dir']}`), git commit `{cc_meta['git_commit']}` |")
md.append(f"| Software | PyMuPDF {tf_meta['pymupdf_version']} | Text-Fabric {cc_meta['text_fabric_version']} |")
md.append(f"| Text used | Hebrew column, PDF pages {tf_meta['pdf_pages_used'][0]}–{tf_meta['pdf_pages_used'][1]} "
          f"| features `g_cons_utf8` + `trailer` of `word` nodes |")
md.append(f"| Verses | {tf_meta['n_verses']} (sub-verses such as [א]18 counted with their verse) | {cc_meta['n_verses']} |")
md.append(f"| Graphic words | {tf_meta['n_graphic_words']} | {cc_meta['n_graphic_words']} |")
md.append('')

md.append('## How to reproduce\n')
md.append('From the folder `scripts/tal_florentin` of the CACCHT repository (https://github.com/DT-UCPH/sp) at commit '
          f"`{cc_meta['git_commit'][:7]}`, with the T&F PDF (free download via the DOI above) saved there as "
          '`tal_florentin_SP.pdf` (the PDF is not in the repository):\n')
md.append('```')
md.append('pip install pymupdf text-fabric')
md.append('python extract_tf.py tal_florentin_SP.pdf results/tf_verses.json')
md.append(f"python extract_caccht.py ../../tf/{cc_meta['dataset_version']} results/caccht_verses.json")
md.append('python compare.py results/tf_verses.json results/caccht_verses.json results')
md.append('```\n')
md.append('Check that the SHA-256 of the PDF matches the value above. The same output files '
          '(`differences.md`, `differences.tsv`, `versification.tsv`) should then be produced.\n')

md.append('## Method\n')
md.append('1. **T&F.** The Hebrew running text is taken from the PDF by font: SBL Hebrew 13.5 pt (text), '
          '9 pt (verse numbers), bold 13.5 pt (chapter numbers) and bold 18 pt (book titles). Footnotes, running '
          'heads and the English translation are ignored. Words are ordered right to left by the position of their '
          'characters on the page. Punctuation and paragraph marks (`:>— —`) are dropped. Colouring (red = '
          'difference from MT) is ignored. Sub-verse numbers ([א]18, [ב]18 …) are counted with the main verse; the '
          'Hebrew letters numbering the commandments in the Decalogue are not text.')
md.append('2. **CACCHT.** For every verse, the `g_cons_utf8` values of the `word` nodes are concatenated with their '
          '`trailer`. Morphemes such as ו, ה, ב are separate word nodes in CACCHT, so one graphic word can consist '
          'of several nodes. Shin/sin dots are removed.')
md.append('3. **Alignment.** The graphic words of each chapter are aligned with Python’s `difflib.SequenceMatcher` '
          '(no autojunk). Final and non-final letter forms count as equal, because CACCHT writes compound names as '
          'e.g. `BN_<MJ` → בנ עמי. Because alignment is per chapter, different verse division does not create false '
          'textual differences; it is listed separately at the end.')
md.append('4. **Classification.** Every non-matching stretch is classified with the rules below, in this order. '
          'The types are mechanical, not a philological judgement.\n')

md.append('### Types of difference\n')
md.append('| Type | Definition |')
md.append('|---|---|')
for t, desc in TYPES.items():
    md.append(f'| {t} | {desc} |')
md.append('')

md.append('### How to read the tables\n')
md.append('- **CACCHT ref**: book chapter:verse in CACCHT; **T&F ref**: verse number under which the words stand in '
          'T&F, with the printed page on which that verse begins.')
md.append('- **CACCHT word node(s)**: the Text-Fabric `word` nodes that make up the CACCHT reading. For a word that '
          'only T&F has, “after *n*” gives the CACCHT word node after which the T&F words stand.')
md.append('- **Verse node**: the CACCHT `verse` node. In Text-Fabric, `T.text(n)` or `F.g_cons_utf8.v(n)` shows the '
          'text of a node.')
md.append('- — = no text in that edition.\n')

md.append('## Summary\n')
md.append(f"Of {len(cc)} CACCHT verses, **{len(cc) - n_diff_verses}** are identical in T&F and **{n_diff_verses}** "
          f"contain at least one difference. There are **{len(diffs)}** differences in all. Versification differs "
          f"for {len(versif)} CACCHT verses.\n")
md.append('| Type | ' + ' | '.join(BOOKS) + ' | Total |')
md.append('|---|' + '---:|' * (len(BOOKS) + 1))
for t in TYPES:
    if by_type[t]:
        md.append(f'| {t} | ' + ' | '.join(str(by_type_book[(t, bk)]) for bk in BOOKS) + f' | {by_type[t]} |')
md.append('| **Total** | ' + ' | '.join(f'**{by_book[bk]}**' for bk in BOOKS) + f' | **{len(diffs)}** |')
md.append('')

md.append('## Differences\n')
num = 0
for bk in BOOKS:
    rows = [d for d in diffs if d['ref_caccht'].split()[0] == bk]
    md.append(f'### {bk} ({len(rows)})\n')
    md.append('| No. | CACCHT ref | T&F ref (p.) | Type | Tal & Florentin | CACCHT | CACCHT word node(s) | Verse node |')
    md.append('|---:|---|---|---|---|---|---|---:|')
    for d in rows:
        num += 1
        cref = d['ref_caccht'].split(' ', 1)[1]
        tref = d['ref_tf'].split(' ', 1)[1] if d['ref_tf'] else ''
        tref = f"{tref} ({d['page_tf']})" if d['page_tf'] else tref
        nodes = d['word_nodes'] or (f"after {d['after_word_node']}" if d['after_word_node'] else '—')
        md.append(f"| {num} | {cref} | {tref} | {d['type']} | {d['tal_florentin'] or '—'} | "
                  f"{d['caccht'] or '—'} | {nodes} | {d['verse_node']} |")
    md.append('')

md.append('## Versification differences\n')
md.append('CACCHT verses whose words stand under a different verse number in T&F. These are numbering differences, '
          'not textual ones. Most are in the Decalogue: T&F number the Samaritan addition on Mount Gerizim as '
          'sub-verses of Exod 20:12 and Deut 5:16 (following MT numbering), where CACCHT counts them as separate verses.\n')
md.append('| CACCHT ref | T&F ref | Verse node |')
md.append('|---|---|---:|')
for cref, tref, vnode in versif:
    md.append(f'| {cref} | {tref} | {vnode} |')
md.append('')

with open(os.path.join(OUTDIR, 'differences.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(md))

print('verses with a difference', n_diff_verses, 'of', len(cc), '| differences', len(diffs),
      '| versification', len(versif))
print(dict(by_type))
