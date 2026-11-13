"""Build graphic-word verse texts from the CACCHT SP Text-Fabric data.

Usage: python extract_caccht.py TF_DIR OUT_JSON

Writes OUT_JSON                {"Genesis 1:1": ["בראשית", ...], ...}
and    <OUT_JSON>_nodes.json   {"Genesis 1:1": {"verse": node, "words": [[word nodes], ...]}, ...}
and    <OUT_JSON>_meta.json    dataset version, git commit, Text-Fabric version
"""
import json
import os
import subprocess
import sys
from importlib.metadata import version
from tf.fabric import Fabric

TF_DIR, OUT = sys.argv[1], sys.argv[2]
BASE = os.path.splitext(OUT)[0]
TF = Fabric(locations=TF_DIR, silent='deep')
api = TF.load('trailer g_cons_utf8 book chapter verse', silent='deep')
F, T, L = api.F, api.T, api.L


def clean(s):
    return (s.replace('ׁ', '').replace('ׂ', '')
            .replace('שׁ', 'ש').replace('שׂ', 'ש'))


verses, nodes = {}, {}
for v in F.otype.s('verse'):
    bk, ch, vs = T.sectionFromNode(v)
    tokens, tok_nodes = [''], [[]]
    for w in L.d(v, 'word'):
        # compound names (g_cons "BN_<MJ") contain a space in g_cons_utf8: they become two
        # graphic words that both point to the same word node
        for k, part in enumerate(clean(F.g_cons_utf8.v(w) or '').split(' ')):
            if k:
                tokens.append('')
                tok_nodes.append([])
            tokens[-1] += part
            tok_nodes[-1].append(w)
        if (F.trailer.v(w) or '').strip() == '' and F.trailer.v(w):
            tokens.append('')
            tok_nodes.append([])
    pairs = [(t, n) for t, n in zip(tokens, tok_nodes) if t]
    ref = f'{bk} {ch}:{vs}'
    verses[ref] = [t for t, _ in pairs]
    nodes[ref] = {'verse': v, 'words': [n for _, n in pairs]}

try:
    repo = os.path.dirname(os.path.dirname(os.path.abspath(TF_DIR)))
    commit = subprocess.run(['git', '-C', repo, 'rev-parse', 'HEAD'],
                            capture_output=True, text=True).stdout.strip()
except OSError:
    commit = ''
meta = {'tf_dir': TF_DIR.replace('\\', '/'),
        'dataset_version': os.path.basename(os.path.normpath(TF_DIR)),
        'git_commit': commit,
        'text_fabric_version': version('text-fabric'),
        'manuscripts': 'MS Dublin Chester Beatty Library 751 (Gen 1-Deut 32:36) + MS Garizim 1 (Deut 32:36b-34)',
        'n_verses': len(verses), 'n_graphic_words': sum(map(len, verses.values()))}

json.dump(verses, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
json.dump(nodes, open(BASE + '_nodes.json', 'w', encoding='utf-8'), indent=0)
json.dump(meta, open(BASE + '_meta.json', 'w', encoding='utf-8'), indent=1)
print(meta)
