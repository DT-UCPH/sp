"""
Make data version 7.3.0 from 7.2.12 with two text repairs:

1. Exodus 19:24: the word K is corrected to LK (imperative of HLK[).
   A new sign slot for the lamed is inserted, so all nodes from that slot onward shift by one.
2. Genesis 17:13: the interjection H (lex H>) gets its missing realized lexeme (g_lex H),
   in line with the other occurrences of H> written as H.
"""
import os

from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = os.path.join(ROOT_DIR, 'tf')
OLD_VERSION = '7.2.12'
NEW_VERSION = '7.3.0'

SKIP_META = {'dateWritten', 'writtenBy'}


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


old_location = os.path.join(TF_FOLDER, OLD_VERSION)
feature_names = sorted(f[:-3] for f in os.listdir(old_location) if f.endswith('.tf') and f != '.tf')
data_features = [f for f in feature_names if f not in {'otype', 'oslots', 'otext'}]

TF = Fabric(locations=old_location, silent='deep')
api = TF.load(' '.join(data_features), silent='deep')
F, E, L, T = api.F, api.E, api.L, api.T

# Locate the words to repair and check that they are what we expect.
exo_word = L.d(T.nodeFromSection(('Exodus', 19, 24)), 'word')[4]
gen_word = L.d(T.nodeFromSection(('Genesis', 17, 13)), 'word')[0]
assert F.g_cons.v(exo_word) == 'K' and F.lex.v(exo_word) == 'HLK['
assert F.g_cons.v(gen_word) == 'H' and F.lex.v(gen_word) == 'H>' and F.g_lex.v(gen_word) == ''

# The lamed is inserted before the slot of the kaf.
kaf_slot = L.d(exo_word, 'sign')[0]
assert F.sign.v(kaf_slot) == 'ך'
new_slot = kaf_slot
containers = set(L.u(kaf_slot))


def shift(n):
    return n + 1 if n >= new_slot else n


# Node and edge structure
otype = {shift(n): F.otype.v(n) for n in range(1, F.otype.maxNode + 1)}
otype[new_slot] = F.otype.slotType

oslots = {}
for n in range(F.otype.maxSlot + 1, F.otype.maxNode + 1):
    slots = {shift(s) for s in E.oslots.s(n)}
    if n in containers:
        slots.add(new_slot)
    oslots[shift(n)] = slots

node_features = {'otype': otype}
for feat in data_features:
    node_features[feat] = {shift(n): v for n, v in getattr(F, feat).items()}

# Text repairs
node_features['sign'][new_slot] = 'ל'

exo_new = shift(exo_word)
node_features['g_cons'][exo_new] = 'LK'
node_features['g_cons_raw'][exo_new] = 'LK'
node_features['g_cons_utf8'][exo_new] = 'לך'
node_features['g_lex'][exo_new] = 'LK'
node_features['g_lex_utf8'][exo_new] = 'לך'
node_features['ETCBC_parsing'][exo_new] = '!!(HLK['
node_features['mt_feat'][exo_new] = 'True'

gen_new = shift(gen_word)
node_features['g_lex'][gen_new] = 'H'
node_features['g_lex_utf8'][gen_new] = 'ה'

meta_data = {f: read_metadata(os.path.join(old_location, f'{f}.tf')) for f in feature_names}

TF.save(
    nodeFeatures=node_features,
    edgeFeatures={'oslots': oslots},
    metaData=meta_data,
    location=TF_FOLDER,
    module=NEW_VERSION,
)
