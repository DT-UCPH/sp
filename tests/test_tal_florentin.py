"""Tests for the Tal & Florentin variant features (var_ft_utf8, var_ft, var_ft_type, var_ft_span, verse_ft).

The main test rebuilds the running text of Tal & Florentin from the CACCHT words and the variant
features, and compares it with the text extracted from the T&F PDF
(scripts/tal_florentin/results/tf_verses.json), chapter by chapter.
"""
import collections
import json
import os
import unicodedata

import pytest
from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = os.path.join(ROOT_DIR, 'tf')
TF_VERSES = os.path.join(ROOT_DIR, 'scripts', 'tal_florentin', 'results', 'tf_verses.json')
latest = sorted(os.listdir(TF_FOLDER), key=lambda v: tuple(int(p) for p in v.split('.')))[-1]

TF = Fabric(locations=os.path.join(TF_FOLDER, latest), silent='deep')
api = TF.load('g_cons_utf8 trailer var_ft_utf8 var_ft var_ft_type var_ft_span verse_ft', silent='deep')
F, L, T = api.F, api.L, api.T

FINALS = str.maketrans('ךםןףץ', 'כמנפצ')
TYPES = {'plene_defective', 'conjunction_waw', 'article_he', 'guttural_interchange', 'aleph_plus_minus',
         'final_he_yod', 'word_division', 'plus_ft', 'plus_caccht', 'other'}
TRANSLIT = dict(zip('אבגדהוזחטיכךלמםנןסעפףצץקרשת', '>BGDHWZXVJKKLMMNNS<PPYYQRCT'))


def letters(s):
    return unicodedata.normalize('NFD', s).replace('ׁ', '').replace('ׂ', '')


def node_text(w):
    """The CACCHT text of one word node, with a space after it if its trailer is a space."""
    text = letters(F.g_cons_utf8.v(w) or '')
    return text + (' ' if F.trailer.v(w) and not F.trailer.v(w).strip() else '')


def rebuild_ft():
    """{'Book chapter': [graphic words]} of T&F, rebuilt from CACCHT + var_ft_*."""
    chapters = collections.OrderedDict()
    for v in F.otype.s('verse'):
        book, chapter, _ = T.sectionFromNode(v)
        words = L.d(v, 'word')
        text, i = '', 0
        while i < len(words):
            w = words[i]
            span = F.var_ft_span.v(w)
            if span is None:
                text += node_text(w)
                i += 1
            elif span == 0:
                text += node_text(w).rstrip() + ' ' + F.var_ft_utf8.v(w) + ' '
                i += 1
            else:
                last = words[i + span - 1]
                reading = F.var_ft_utf8.v(w)
                text += ('' if reading == '-' else reading) + node_text(last)[len(node_text(last).rstrip()):]
                i += span
        chapters.setdefault(f'{book} {chapter}', []).extend(text.split())
    return chapters


def test_variants_only_on_words():
    for feat in ('var_ft_utf8', 'var_ft', 'var_ft_type', 'var_ft_span'):
        assert {F.otype.v(n) for n, _ in getattr(F, feat).items()} == {'word'}, feat


def test_variant_features_on_same_nodes():
    nodes = {n for n, _ in F.var_ft_utf8.items()}
    for feat in ('var_ft', 'var_ft_type', 'var_ft_span'):
        assert {n for n, _ in getattr(F, feat).items()} == nodes, feat


def test_var_ft_type_values():
    assert {v for _, v in F.var_ft_type.items()} == TYPES


def test_var_ft_is_transliteration_of_var_ft_utf8():
    for n, v in F.var_ft_utf8.items():
        expected = '-' if v == '-' else ' '.join(''.join(TRANSLIT[c] for c in w) for w in v.split())
        assert F.var_ft.v(n) == expected, n


def test_var_ft_span_stays_in_verse():
    for n, span in F.var_ft_span.items():
        verse = L.u(n, 'verse')[0]
        assert all(L.u(m, 'verse')[0] == verse and F.otype.v(m) == 'word' for m in range(n, n + max(span, 1))), n
        assert all(F.var_ft_span.v(m) is None for m in range(n + 1, n + span)), n


def test_insertions_and_omissions():
    for n, span in F.var_ft_span.items():
        if span == 0:
            assert F.var_ft_type.v(n) == 'plus_ft', n
        if F.var_ft_utf8.v(n) == '-':
            assert F.var_ft_type.v(n) == 'plus_caccht', n


def test_verse_ft_only_on_verses():
    assert {F.otype.v(n) for n, _ in F.verse_ft.items()} == {'verse'}


@pytest.mark.skipif(not os.path.exists(TF_VERSES), reason='T&F extraction not available')
def test_round_trip_tal_florentin_text():
    """CACCHT + variant features must give exactly the T&F text (without the book-end colophons)."""
    tf_verses = json.load(open(TF_VERSES, encoding='utf-8'))
    expected = collections.OrderedDict()
    for ref, words in tf_verses.items():
        expected.setdefault(ref.rsplit(':', 1)[0], []).extend(words)
    rebuilt = rebuild_ft()
    colophon_chapters = {'Exodus 40', 'Leviticus 27', 'Numbers 36', 'Deuteronomy 34'}
    assert set(rebuilt) == set(expected)
    for ch, words in expected.items():
        got = [w.translate(FINALS) for w in rebuilt[ch]]
        exp = [w.translate(FINALS) for w in words]
        if ch in colophon_chapters:
            # T&F end the book with a scribal colophon (…קצים…) that is not part of CACCHT
            assert exp[:len(got)] == got, ch
            assert 'קצימ' in exp[len(got):], ch
        else:
            assert got == exp, ch
