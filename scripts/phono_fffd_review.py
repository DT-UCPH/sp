"""
List the words in phono_transcr that still contain U+FFFD (an unreadable glyph in the decoded
Ben-Hayyim transcription), with the place in the printed edition where they can be read by eye.

Usage: python scripts/phono_fffd_review.py [version] [Ben-Hayyim data folder]

Output: review/phono_fffd_<version>.tsv, one row per word, with
  node, book, chapter, verse, g_cons, lex, ETCBC_parsing, phono_transcr (now), why it was not filled
  in automatically, forms of the same g_cons + ETCBC_parsing elsewhere (form:count), the printed page,
  the PDF page and the line number in the Ben-Hayyim scan, and that printed line.
Fill in the column 'reading' by eye; empty means: not read yet.

The page and line are found by searching the word (with its U+FFFD) in the printed lines of the
verse, as recorded in the "physical lines" half of the decoded text files (see read_book). When it
is not found there, the columns are empty.
"""
import csv
import os
import re
import sys

from tf.fabric import Fabric

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_7_4_1 import ROOT_DIR, TF_FOLDER, propose_fills  # noqa: E402

VERSION = sys.argv[1] if len(sys.argv) > 1 else '7.4.1'
BH_DATA = sys.argv[2] if len(sys.argv) > 2 else 'C:/Users/geitb/Zurich/zurich_research/Kantor/wp2/data'
BH_FILES = {
    'Genesis': 'benhayyim_genesis_v2.txt',
    'Exodus': 'benhayyim_exodus_stageA.txt',
    'Leviticus': 'benhayyim_leviticus_stageA.txt',
    'Numbers': 'benhayyim_numbers_stageA.txt',
    'Deuteronomy': 'benhayyim_deuteronomy_stageA.txt',
}
PAGE = re.compile(r'^# ---- printed p\. (\d+) \(PDF (\d+)\)')
LINE = re.compile(r'^\s*(\d+)  (.*)$')
HEADING = re.compile(r'^# [A-Z]+ (\d+)\b')
VERSE = re.compile(r'^\[(\d+)[^\]]*\]\s*(.*)$')


def read_book(book):
    """Return the printed text of a book as one string, a list of (offset, printed page, PDF page,
    line number, line text) for its printed lines, and {(chapter, verse): (start, end)} offsets.

    The file holds the text twice: by chapter and verse, and as the printed lines. The verse
    numbers in the printed lines are themselves decoded and sometimes misread ([1 1], [1\ufffd]),
    so the verses are found by searching the start of each verse text in the printed text."""
    with open(os.path.join(BH_DATA, BH_FILES[book]), encoding='utf8') as f:
        lines = f.read().split('\n')
    split = next(i for i, l in enumerate(lines) if 'THE SAME TEXT AS PHYSICAL LINES' in l)

    verses, chapter = [], None
    for l in lines[:split]:
        m = HEADING.match(l)
        if m:
            chapter = int(m.group(1))
            continue
        m = VERSE.match(l)
        if m and chapter:
            verses.append(((chapter, int(m.group(1))), m.group(2)))

    printed, parts, offset, page, pdf = [], [], 0, None, None
    for l in lines[split:]:
        m = PAGE.match(l)
        if m:
            page, pdf = m.groups()
            continue
        m = LINE.match(l)
        if m and page is not None:
            printed.append((offset, page, pdf, int(m.group(1)), m.group(2)))
            parts.append(m.group(2))
            offset += len(m.group(2)) + 1
    text = ' '.join(parts)

    starts, cursor = [], 0
    for key, verse_text in verses:
        probe = verse_text[:25]
        pos = text.find(probe, cursor) if probe else -1
        if pos >= 0:
            starts.append((key, pos))
            cursor = pos + 1
    spans = {}
    for i, (key, pos) in enumerate(starts):
        end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        lo, hi = spans.get(key, (pos, end))  # a verse with sub-numbers ([15³]) gets one span
        spans[key] = (min(lo, pos), max(hi, end))
    return text, printed, spans


def locate(book_data, chapter, verse, value):
    """The printed line (page, PDF page, line number, text) in which value occurs within the verse,
    or the verse before or after it (the edition's verse division differs in places)."""
    text, printed, spans = book_data
    for v in (verse, verse + 1, verse - 1):
        if (chapter, v) not in spans:
            continue
        start, end = spans[(chapter, v)]
        pos = text.find(value, start, end + len(value))
        if pos >= 0:
            line = max((p for p in printed if p[0] <= pos), key=lambda p: p[0])
            return line[1:]
    return None


if __name__ == '__main__':
    api = Fabric(locations=os.path.join(TF_FOLDER, VERSION), silent='deep').load(
        'phono_transcr g_cons lex ETCBC_parsing', silent='deep')
    F, T = api.F, api.T
    fills, rest = propose_fills(F)
    assert not fills, f'{len(fills)} words can still be filled in automatically: run make_7_4_1.py first'

    index = {book: read_book(book) for book in BH_FILES}

    os.makedirs(os.path.join(ROOT_DIR, 'review'), exist_ok=True)
    out = os.path.join(ROOT_DIR, 'review', f'phono_fffd_{VERSION}.tsv')
    found = 0
    with open(out, 'w', encoding='utf8', newline='') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(['node', 'book', 'chapter', 'verse', 'g_cons', 'lex', 'ETCBC_parsing', 'phono_transcr',
                         'why not filled in', 'forms elsewhere', 'printed page', 'PDF page', 'line',
                         'printed line', 'reading'])
        for w in sorted(rest):
            book, chapter, verse = T.sectionFromNode(w)
            value = F.phono_transcr.v(w)
            reason, forms = rest[w]
            where = locate(index[book], chapter, verse, value)
            found += where is not None
            page, pdf, number, text = where or ('', '', '', '')
            writer.writerow([w, book, chapter, verse, F.g_cons.v(w), F.lex.v(w), F.ETCBC_parsing.v(w), value, reason,
                             ' '.join(f'{form}:{n}' for form, n in forms), page, pdf, number, text, ''])
    print(f'{len(rest)} words written to {out}; {found} located in the printed lines')
