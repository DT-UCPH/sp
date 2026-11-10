"""
Make data version 7.5.0 from 7.4.1: add the readings of the Tal & Florentin edition as variants.

Source: Moshe Florentin and Abraham Tal, The Samaritan Pentateuch: An English Translation with a
Parallel Annotated Hebrew Text (Open Book Publishers, 2024, https://doi.org/10.11647/OBP.0415,
CC BY-NC 4.0). Its Hebrew text is MS Nablus 6 (1204 CE), with gaps filled from other manuscripts.
The CACCHT text (MS Dublin CBL 751 + MS Garizim 1) is NOT changed: the T&F readings are added as
annotations on the CACCHT word nodes.

Input: scripts/tal_florentin/results/differences.tsv and versification.tsv, made against 7.4.1 by
scripts/tal_florentin/compare.py (see the README there).

New features
- word  var_ft_utf8  T&F reading of the differing stretch, Hebrew script ('-' = no words in T&F)
- word  var_ft       the same in the transliteration of g_cons_raw (ש = C, no final forms)
- word  var_ft_type  kind of difference (plene_defective, conjunction_waw, ...)
- word  var_ft_span  number of CACCHT word nodes the reading replaces, starting at this node;
                     0 = the T&F words stand after this word and CACCHT has nothing there
- verse verse_ft     T&F chapter:verse under which the words of this verse stand, where it differs

The four scribal colophons at the end of Exodus-Deuteronomy that T&F print are not added.
Slots, nodes and all existing features do not change.
"""
import csv
import os
import unicodedata

from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = os.path.join(ROOT_DIR, 'tf')
DIFF_DIR = os.path.join(ROOT_DIR, 'scripts', 'tal_florentin', 'results')
OLD_VERSION = '7.4.1'
NEW_VERSION = '7.5.0'

SKIP_META = {'dateWritten', 'writtenBy'}

TYPES = {
    'plene/defective': 'plene_defective',
    'conjunction waw': 'conjunction_waw',
    'article he': 'article_he',
    'guttural interchange': 'guttural_interchange',
    'aleph plus/minus': 'aleph_plus_minus',
    'final he/yod': 'final_he_yod',
    'word division': 'word_division',
    'plus T&F': 'plus_ft',
    'plus CACCHT': 'plus_caccht',
    'other': 'other',
}
SKIPPED_TYPES = {'colophon (T&F only)'}

TRANSLIT = dict(zip('אבגדהוזחטיכךלמםנןסעפףצץקרשת',
                    '>BGDHWZXVJKKLMMNNS<PPYYQRCT'))

SOURCE = ('Moshe Florentin and Abraham Tal, The Samaritan Pentateuch: An English Translation with a '
          'Parallel Annotated Hebrew Text, Open Book Publishers 2024, https://doi.org/10.11647/OBP.0415 '
          '(CC BY-NC 4.0); Hebrew text MS Nablus 6, gaps filled from other manuscripts')

FEATURE_META = {
    'var_ft_utf8': ('str', 'word', 'Reading of the Tal & Florentin edition where it differs from this text, '
                    'in Hebrew script; stands on the first word node of the differing stretch '
                    '(see var_ft_span); "-" means T&F have no words here'),
    'var_ft': ('str', 'word', 'Reading of the Tal & Florentin edition (as var_ft_utf8) in the '
               'transliteration of g_cons_raw'),
    'var_ft_type': ('str', 'word', 'Kind of difference between this text and the Tal & Florentin reading '
                    '(var_ft_utf8), classified mechanically'),
    'var_ft_span': ('int', 'word', 'Number of word nodes, starting at this one, that the Tal & Florentin reading '
                    '(var_ft_utf8) replaces; 0 means the T&F words stand after this word'),
    'verse_ft': ('str', 'verse', 'Chapter:verse under which the words of this verse stand in the Tal & Florentin '
                 'edition, where this differs from the verse number here'),
}


def read_metadata(path):
    """Read the @-header of a .tf file, without the fields that Text-Fabric writes itself."""
    meta = {}
    with open(path, encoding='utf8') as f:
        for line in f:
            if not line.startswith('@'):
                break
            key, _, value = line[1:].rstrip('\n').partition('=')
            if key in {'node', 'edge', 'config'} or key in SKIP_META:
                continue
            meta[key] = value
    meta['version'] = NEW_VERSION
    return meta


def translit(hebrew):
    return ' '.join(''.join(TRANSLIT[c] for c in word) for word in hebrew.split())


def read_tsv(name):
    with open(os.path.join(DIFF_DIR, name), encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


FINALS = str.maketrans('ךםןףץ', 'כמנפצ')


def graphic_words(F, L):
    """The CACCHT text as graphic words, as in tal_florentin/extract_caccht.py:
    a list of (text, [word nodes]), and for every word node the indices of its graphic words.
    A graphic word can consist of several word nodes (ו, ה, ב ... are separate nodes), and a
    compound name (one node, g_cons_utf8 with a space) gives several graphic words."""
    words, of_node = [], {}
    for v in F.otype.s('verse'):
        cur = ['', []]
        for w in L.d(v, 'word'):
            for k, part in enumerate(clean_marks(F.g_cons_utf8.v(w) or '').split(' ')):
                if k:
                    words.append(cur)
                    cur = ['', []]
                cur[0] += part
                cur[1].append(w)
            if F.trailer.v(w) and not F.trailer.v(w).strip():
                words.append(cur)
                cur = ['', []]
        words.append(cur)
    words = [(t, ns) for t, ns in words if t]
    for i, (_, ns) in enumerate(words):
        for n in ns:
            of_node.setdefault(n, []).append(i)
    return words, of_node


def clean_marks(s):
    return unicodedata.normalize('NFD', s).replace('ׁ', '').replace('ׂ', '')


def variant_features(F, T, L, diffs):
    feats = {f: {} for f in ('var_ft_utf8', 'var_ft', 'var_ft_type', 'var_ft_span')}
    words, of_node = graphic_words(F, L)
    for d in diffs:
        if d['type'] in SKIPPED_TYPES:
            continue
        nodes = [int(n) for n in d['word_nodes'].split()]
        tf_words = d['tal_florentin'].split()
        if nodes:
            assert nodes == list(range(nodes[0], nodes[-1] + 1)), d
            assert all(F.otype.v(n) == 'word' for n in nodes), d
            # all graphic words that (partly) consist of these nodes; the difference itself must be
            # one contiguous stretch of them. Graphic words of the same nodes outside the difference
            # (other parts of a compound name) are kept, so that the reading covers whole nodes.
            idx = sorted({i for n in nodes for i in of_node[n]})
            assert idx == list(range(idx[0], idx[-1] + 1)), d
            texts = [words[i][0].translate(FINALS) for i in idx]
            target = [w.translate(FINALS) for w in d['caccht'].split()]
            offsets = [k for k in range(len(texts) - len(target) + 1) if texts[k:k + len(target)] == target]
            assert len(offsets) == 1, (d, texts)
            k = offsets[0]
            before = [words[i][0] for i in idx[:k]]
            after = [words[i][0] for i in idx[k + len(target):]]
            tf_words = before + tf_words + after
            anchor, span = nodes[0], len(nodes)
        else:
            anchor, span = int(d['after_word_node']), 0
            # the T&F words must stand after a whole node, not inside a compound name
            assert words[of_node[anchor][-1]][1][-1] == anchor, d
        assert F.otype.v(anchor) == 'word', d
        assert '{} {}:{}'.format(*T.sectionFromNode(anchor)) == d['ref_caccht'], d
        assert anchor not in feats['var_ft_type'], d
        reading = ' '.join(tf_words) or '-'
        feats['var_ft_utf8'][anchor] = reading
        feats['var_ft'][anchor] = '-' if reading == '-' else translit(reading)
        feats['var_ft_type'][anchor] = TYPES[d['type']]
        feats['var_ft_span'][anchor] = span
    return feats


def verse_feature(F, T, versif):
    verse_ft = {}
    for r in versif:
        v = int(r['verse_node'])
        book, chapter, _ = T.sectionFromNode(v)
        assert F.otype.v(v) == 'verse' and '{} {}:{}'.format(*T.sectionFromNode(v)) == r['ref_caccht'], r
        refs = []
        for ref in r['ref_tf'].split(', '):
            bk, cv = ref.rsplit(' ', 1)
            assert bk == book, r
            refs.append(cv)
        verse_ft[v] = ', '.join(refs)
    return verse_ft


if __name__ == '__main__':
    old_location = os.path.join(TF_FOLDER, OLD_VERSION)
    feature_names = sorted(f[:-3] for f in os.listdir(old_location) if f.endswith('.tf') and f != '.tf')
    data_features = [f for f in feature_names if f not in {'otype', 'oslots', 'otext'}]

    TF = Fabric(locations=old_location, silent='deep')
    api = TF.load(' '.join(data_features), silent='deep')
    F, E, T = api.F, api.E, api.T
    L = api.L

    node_features = {'otype': {n: F.otype.v(n) for n in range(1, F.otype.maxNode + 1)}}
    for feat in data_features:
        node_features[feat] = dict(getattr(F, feat).items())
    oslots = {n: set(E.oslots.s(n)) for n in range(F.otype.maxSlot + 1, F.otype.maxNode + 1)}

    diffs, versif = read_tsv('differences.tsv'), read_tsv('versification.tsv')
    new = variant_features(F, T, L, diffs)
    new['verse_ft'] = verse_feature(F, T, versif)
    for feat, values in new.items():
        assert feat not in node_features
        node_features[feat] = values

    n_skipped = sum(d['type'] in SKIPPED_TYPES for d in diffs)
    assert len(new['var_ft_type']) + n_skipped == len(diffs) == 1078, (len(new['var_ft_type']), len(diffs))
    assert len(new['verse_ft']) == 58, len(new['verse_ft'])
    print(f"{len(new['var_ft_type'])} variants added ({n_skipped} colophons skipped), "
          f"{len(new['verse_ft'])} verses with T&F verse numbers")

    meta_data = {f: read_metadata(os.path.join(old_location, f'{f}.tf')) for f in feature_names}
    for feat, (value_type, node_type, description) in FEATURE_META.items():
        meta_data[feat] = {'valueType': value_type, 'description': description,
                           'source': SOURCE, 'licence': 'CC BY-NC 4.0',
                           'licenceUrl': 'https://creativecommons.org/licenses/by-nc/4.0/',
                           'version': NEW_VERSION}

    TF.save(
        nodeFeatures=node_features,
        edgeFeatures={'oslots': oslots},
        metaData=meta_data,
        location=TF_FOLDER,
        module=NEW_VERSION,
    )
