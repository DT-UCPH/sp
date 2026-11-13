"""
Make data version 7.4.1 from 7.4.0.

Fill in unreadable characters (U+FFFD) in phono_transcr.

phono_transcr comes from a decoding of the scan of Ben-Hayyim's vocalised transcription of the
Samaritan Pentateuch (Literary and Oral Tradition IV). U+FFFD marks a glyph that the decoder could
not read. It is NOT an encoding error, so it cannot be repaired by re-reading a source file.

A word is filled in automatically only when all of these hold:
- the value has at least one readable character besides the U+FFFD;
- other words with the same g_cons and ETCBC_parsing have readable phono_transcr values;
- exactly one of those values matches, with each U+FFFD standing for exactly one glyph
  (a base character with its combining marks, or a combining mark alone);
- that value is also the most frequent value for that g_cons + ETCBC_parsing, and not a tie.

The rest are left as they are and listed for reading by eye in the scan
(scripts/phono_fffd_review.py). Slots, nodes and all other features do not change.
"""
import collections
import os
import re

from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = os.path.join(ROOT_DIR, 'tf')
OLD_VERSION = '7.4.0'
NEW_VERSION = '7.4.1'

SKIP_META = {'dateWritten', 'writtenBy'}
FFFD = '�'
# One glyph: a base character with its combining marks, or combining marks alone.
GLYPH = r'(?:[^̀-ͯ�][̀-ͯ]*|[̀-ͯ]+)'


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


def fffd_pattern(value):
    """A regex that matches readable values in which every U+FFFD of value is one glyph."""
    return re.compile('^' + GLYPH.join(re.escape(part) for part in value.split(FFFD)) + '$')


def propose_fills(F):
    """Return {word: (old value, new value)} for the words that can be filled in automatically,
    and {word: (reason, candidates)} for the others."""
    forms = collections.defaultdict(collections.Counter)
    for w in F.otype.s('word'):
        value = F.phono_transcr.v(w)
        if value and FFFD not in value:
            forms[(F.g_cons.v(w), F.ETCBC_parsing.v(w))][value] += 1

    fills, rest = {}, {}
    for w in F.otype.s('word'):
        value = F.phono_transcr.v(w) or ''
        if FFFD not in value:
            continue
        known = forms[(F.g_cons.v(w), F.ETCBC_parsing.v(w))]
        if not value.strip(FFFD):
            rest[w] = ('only unreadable characters', known.most_common(3))
            continue
        pattern = fffd_pattern(value)
        candidates = [(form, n) for form, n in known.most_common() if pattern.match(form)]
        if not candidates:
            rest[w] = ('no matching form elsewhere', known.most_common(3))
        elif len(candidates) > 1:
            rest[w] = ('more than one matching form', candidates)
        else:
            top = known.most_common(2)
            dominant = top[0][0] == candidates[0][0] and (len(top) == 1 or top[1][1] < top[0][1])
            if dominant:
                fills[w] = (value, candidates[0][0])
            else:
                rest[w] = ('matching form is not the most frequent one', candidates + known.most_common(2))
    return fills, rest


if __name__ == '__main__':
    old_location = os.path.join(TF_FOLDER, OLD_VERSION)
    feature_names = sorted(f[:-3] for f in os.listdir(old_location) if f.endswith('.tf') and f != '.tf')
    data_features = [f for f in feature_names if f not in {'otype', 'oslots', 'otext'}]

    TF = Fabric(locations=old_location, silent='deep')
    api = TF.load(' '.join(data_features), silent='deep')
    F, E = api.F, api.E

    node_features = {'otype': {n: F.otype.v(n) for n in range(1, F.otype.maxNode + 1)}}
    for feat in data_features:
        node_features[feat] = dict(getattr(F, feat).items())
    oslots = {n: set(E.oslots.s(n)) for n in range(F.otype.maxSlot + 1, F.otype.maxNode + 1)}

    fills, rest = propose_fills(F)
    phono = node_features['phono_transcr']
    for w, (old, new) in fills.items():
        assert phono[w] == old, (w, phono[w], old)
        assert FFFD not in new
        phono[w] = new

    remaining = sum(FFFD in (v or '') for v in phono.values())
    # Counts measured on 7.4.0: 1,099 words with U+FFFD, 429 filled in, 670 left for review.
    assert len(fills) == 429, len(fills)
    assert remaining == len(rest) == 670, (remaining, len(rest))
    print(f'{len(fills)} words filled in, {remaining} words with U+FFFD left for review')

    meta_data = {f: read_metadata(os.path.join(old_location, f'{f}.tf')) for f in feature_names}

    TF.save(
        nodeFeatures=node_features,
        edgeFeatures={'oslots': oslots},
        metaData=meta_data,
        location=TF_FOLDER,
        module=NEW_VERSION,
    )
