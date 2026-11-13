"""Extract the Hebrew running text of Tal & Florentin's SP edition from the PDF.

Usage: python extract_tf.py PDF OUT_JSON

Writes OUT_JSON               {"Genesis 1:1": ["בראשית", ...], ...}
and    <OUT_JSON>_pages.json  {"Genesis 1:1": [pdf page (1-based), printed page], ...}
and    <OUT_JSON>_meta.json   PDF title, SHA-256, pymupdf version
"""
import hashlib
import json
import os
import re
import sys
import collections
import pymupdf

PDF = sys.argv[1]
OUT = sys.argv[2]

BOOKS = {'בראשית': 'Genesis', 'שמות': 'Exodus', 'ויקרא': 'Leviticus',
         'במדבר': 'Numbers', 'דברים': 'Deuteronomy'}
HEB_NUM = {c: v for c, v in zip('אבגדהוזחטיכלמנסעפצקרשת',
                                [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400])}
HEB_WORD = re.compile(r'[א-ת]+')


def heb_num(s):
    return sum(HEB_NUM.get(c, 0) for c in s)


doc = pymupdf.open(PDF)
first, last = 103, None
for pn in range(103, doc.page_count):
    if doc[pn].get_text().lstrip().startswith(tuple(str(i) for i in range(10))) and 'Endnotes' in doc[pn].get_text()[:60]:
        last = pn
        break
last = last or doc.page_count

verses = collections.OrderedDict()
pages = {}
book = chap = verse = None
oddities = []

for pn in range(first, last):
    # printed page number: the digits-only span in the body font at 10pt
    printed = next((s['text'].strip() for b in doc[pn].get_text('dict')['blocks'] for l in b.get('lines', [])
                    for s in l['spans'] if s['font'] == 'CharisSIL' and round(s['size'], 1) == 10.0
                    and s['text'].strip().isdigit()), '')
    items = []  # (y, x, kind, text, color)
    for b in doc[pn].get_text('rawdict')['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                f, sz = s['font'], round(s['size'], 1)
                t = ''.join(c['c'] for c in s['chars'])
                if not f.startswith('SBLHebrew'):
                    continue
                x0, y0, x1, y1 = s['bbox']
                yc = (y0 + y1) / 2
                if f == 'SBLHebrew,Bold' and sz == 18.0:
                    items.append([yc, x1, 'book', t, s['color']])
                elif f == 'SBLHebrew,Bold' and sz == 13.5:
                    items.append([yc, x1, 'chap', t, s['color']])
                elif f == 'SBLHebrew' and sz in (9.0, 6.3) and re.search(r'\d', t):
                    # verse numbers, incl. "[20]", sub-verses "[א]18" (merged into 18);
                    # Hebrew letters here are commandment numbers, not text; "10–1" marks a transposed block
                    if re.search(r'\d\s*–\s*\d', t):
                        continue
                    items.append([yc, x1, 'verse', re.search(r'\d+', t).group(), s['color']])
                elif sz == 13.5:
                    # split into words using character positions, so that the stored
                    # order of the span (visual or logical) does not matter
                    word, xs = '', []
                    for c in s['chars'] + [{'c': ' ', 'bbox': (0, 0, 0, 0)}]:
                        if HEB_WORD.fullmatch(c['c']):
                            word += c['c']
                            xs.append((c['bbox'][0] + c['bbox'][2]) / 2)
                        else:
                            if word:
                                items.append([yc, sum(xs) / len(xs), 'text', word, s['color']])
                            word, xs = '', []
    # group into lines by vertical centre
    items.sort(key=lambda it: it[0])
    lines = []
    for it in items:
        if lines and abs(lines[-1][0][0] - it[0]) < 4:
            lines[-1].append(it)
        else:
            lines.append([it])
    for line in lines:
        line.sort(key=lambda it: -it[1])  # right to left
        for y, x, kind, t, color in line:
            if kind == 'book':
                book = BOOKS[t.strip()]
                chap, verse = None, None
            elif kind == 'chap':
                if HEB_WORD.fullmatch(t.strip()) and heb_num(t.strip()) == (chap or 0) + 1:
                    chap, verse = heb_num(t.strip()), None
                else:
                    oddities.append(('bold', pn, t))
                    words = HEB_WORD.findall(t)
                    if verse is not None:
                        verses[f'{book} {chap}:{verse}'].extend(reversed(words))
            elif kind == 'verse':
                verse = int(t.strip())
                key = f'{book} {chap}:{verse}'
                verses.setdefault(key, [])
                pages.setdefault(key, [pn + 1, printed])
            else:
                words = HEB_WORD.findall(t)
                if not words:
                    continue
                if verse is None:
                    oddities.append(('noverse', pn, t))
                    continue
                verses[f'{book} {chap}:{verse}'].extend(words)

base = os.path.splitext(OUT)[0]
meta = {'pdf': os.path.basename(PDF), 'title': doc.metadata.get('title'), 'author': doc.metadata.get('author'),
        'sha256': hashlib.sha256(open(PDF, 'rb').read()).hexdigest(), 'pymupdf_version': pymupdf.VersionBind,
        'pdf_pages_used': [first + 1, last], 'n_verses': len(verses),
        'n_graphic_words': sum(map(len, verses.values()))}
json.dump(verses, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(pages, open(base + '_pages.json', 'w', encoding='utf-8'), indent=0)
json.dump(meta, open(base + '_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('pages', first, last, 'verses', len(verses), 'words', sum(map(len, verses.values())))
for o in oddities[:80]:
    print(o)
print('oddities', len(oddities))
