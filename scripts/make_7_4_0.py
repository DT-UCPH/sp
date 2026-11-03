"""
Make data version 7.4.0 from 7.3.0.

Phase A of the Schorch improvement plan: feature-only corrections in Genesis, based on
Schorch, *Die Vokale des Gesetzes* I (2004), ch. 3.4. Slots and nodes do not change.

A1  verbal stem (vs) that still followed MT
A2  lexeme corrections
A3  lexeme + part of speech
A4  >T versus >T== ("with")
A5  person/gender/number
A6  ETCBC_parsing consistency: the `]]` stem formative where g_vbs is `]]`,
    stray `:a` on active participles, and the missing preformative in Gen 33:13 JD<.

The old value of every changed feature is asserted before it is changed.
Word nodes that change get mt_feat ''. Every change based on Schorch gets a grammar_note: the
page in Schorch (2004) where the reason for the change is given, with a short summary of that reason. The *_utf8 twins of lex, g_lex and the
morpheme features are derived from the changed transliteration values.
"""
import os
import re

from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = os.path.join(ROOT_DIR, 'tf')
OLD_VERSION = '7.3.0'
NEW_VERSION = '7.4.0'

SKIP_META = {'dateWritten', 'writtenBy'}

MORPHEME_FEATURES = ['g_pfm', 'g_vbs', 'g_vbe', 'g_nme', 'g_uvf', 'g_prs']

# Lexemes that do not exist yet in 7.3.0.
NEW_LEXEMES = {
    'NKSP[': {'lex_utf8': 'נכספ[', 'gloss': 'long'},
    'XWV[': {'lex_utf8': 'חוט[', 'gloss': 'mend'},
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


old_location = os.path.join(TF_FOLDER, OLD_VERSION)
feature_names = sorted(f[:-3] for f in os.listdir(old_location) if f.endswith('.tf') and f != '.tf')
data_features = [f for f in feature_names if f not in {'otype', 'oslots', 'otext'}]

TF = Fabric(locations=old_location, silent='deep')
api = TF.load(' '.join(data_features), silent='deep')
F, E, L, T = api.F, api.E, api.L, api.T

node_features = {'otype': {n: F.otype.v(n) for n in range(1, F.otype.maxNode + 1)}}
for feat in data_features:
    node_features[feat] = dict(getattr(F, feat).items())
nf = node_features
oslots = {n: set(E.oslots.s(n)) for n in range(F.otype.maxSlot + 1, F.otype.maxNode + 1)}

# Lexicon lookups, so that a word that moves to an existing lexeme gets that lexeme's
# lex_utf8 and gloss.
LEX_UTF8, LEX_GLOSS = {}, {}
for w in F.otype.s('word'):
    LEX_UTF8.setdefault(F.lex.v(w), F.lex_utf8.v(w))
    LEX_GLOSS.setdefault(F.lex.v(w), F.gloss.v(w))
for lex, info in NEW_LEXEMES.items():
    assert lex not in LEX_UTF8, lex
    LEX_UTF8[lex] = info['lex_utf8']
    LEX_GLOSS[lex] = info['gloss']

# Transliteration -> Hebrew script, learned from the data. Every value maps one to one.
MORPHEME_UTF8 = {feat: {} for feat in MORPHEME_FEATURES}
for w in F.otype.s('word'):
    for feat in MORPHEME_FEATURES:
        value = getattr(F, feat).v(w)
        if value:
            utf8 = getattr(F, f'{feat}_utf8').v(w)
            assert MORPHEME_UTF8[feat].setdefault(value, utf8) == utf8, (feat, value)

LETTERS = {'>': 'א', 'B': 'ב', 'G': 'ג', 'D': 'ד', 'H': 'ה', 'W': 'ו', 'Z': 'ז', 'X': 'ח', 'V': 'ט', 'J': 'י',
           'K': 'כ', 'L': 'ל', 'M': 'מ', 'N': 'נ', 'S': 'ס', '<': 'ע', 'P': 'פ', 'Y': 'צ', 'Q': 'ק', 'R': 'ר',
           'C': 'שׁ', 'F': 'שׂ', 'T': 'ת'}
FINALS = {'K': 'ך', 'M': 'ם', 'N': 'ן', 'P': 'ף', 'Y': 'ץ'}


def g_lex_to_utf8(w):
    """g_lex in Hebrew script. As in the existing data, the last letter of g_lex gets its final form,
    unless the word is written together with the next one (empty trailer)."""
    g_lex = nf['g_lex'][w]
    chars = [LETTERS[c] for c in g_lex]
    attached = not nf['trailer'].get(w)
    if g_lex and not attached and g_lex[-1] in FINALS:
        chars[-1] = FINALS[g_lex[-1]]
    return ''.join(chars)


# Check g_lex_to_utf8 against the existing data.
mismatch = [w for w in F.otype.s('word')
            if F.g_lex.v(w) and all(c in LETTERS for c in F.g_lex.v(w)) and g_lex_to_utf8(w) != F.g_lex_utf8.v(w)]
assert not mismatch, (len(mismatch), [(w, F.g_lex.v(w), F.g_lex_utf8.v(w)) for w in mismatch[:10]])

changed_words = set()
grammar_notes = {}
SCHORCH = 'Schorch 2004'


def change(node, note=None, **feats):
    """Change features of a node. Each value is a pair (expected old value, new value).
    note is the grammar_note: where the reason for the change can be found."""
    if note is not None:
        assert grammar_notes.setdefault(node, note) == note, (node, grammar_notes[node], note)
    for feat, (old, new) in feats.items():
        current = nf[feat].get(node, '')
        current = '' if current is None else current
        assert current == old, f'{node} {T.sectionFromNode(node)} {feat}: expected {old!r}, found {current!r}'
        nf[feat][node] = new
        if feat == 'lex':
            nf['lex_utf8'][node] = LEX_UTF8[new]
            if 'gloss' not in feats:
                nf['gloss'][node] = LEX_GLOSS[new]
        elif feat in MORPHEME_FEATURES:
            if new:
                nf[f'{feat}_utf8'][node] = MORPHEME_UTF8[feat][new]
            else:
                nf[f'{feat}_utf8'].pop(node, None)
    if F.otype.v(node) == 'word':
        changed_words.add(node)
        if 'g_lex' in feats or any(f in feats for f in ['g_vbe', 'g_nme', 'g_uvf', 'g_prs']):
            nf['g_lex_utf8'][node] = g_lex_to_utf8(node)


# ---------------------------------------------------------------------------------------
# A1 Verbal stem
# ---------------------------------------------------------------------------------------
# Gen 3:16 >RBH: RBH piel in divine speech
change(406906, note=f'{SCHORCH}, pp. 95-96: RBH is read as piel in divine speech (MT hif)', vs=('hif', 'piel'), g_vbs=(']]', ''), ETCBC_parsing=('!>!]]RBH[', '!>!RBH['))
# Gen 8:10, 25:1 JSP: qal perfect (wayyosef read as perfect)
for w, note in ((409151, f'{SCHORCH}, p. 108: qal perfect instead of MT hif wayyiqtol; with I-Yod verbs the perfect '
                          'often replaces the wayyiqtol, and JSP is qal in the perfect and hif in the imperfect'),
                (417966, f'{SCHORCH}, p. 164: qal perfect instead of MT hif wayyiqtol, see p. 108 (ad Gen 8:10)')):
    change(w, note=note, vs=('hif', 'qal'), vt=('impf', 'perf'), g_pfm=('!J!', ''), g_vbs=(']]', ''), g_lex=('SP', 'JSP'),
           ETCBC_parsing=('!J!]](JSP[', 'JSP['))
# Gen 18:29 JSP: qal
change(413855, note=f'{SCHORCH}, p. 147: qal perfect instead of MT hif, see p. 108 (ad Gen 8:10)', vs=('hif', 'qal'), g_vbs=(']]', ''), ETCBC_parsing=(']]JSP[', 'JSP['))
# Gen 12:16 HJJVB (ā̊ʾīṭåb), Gen 48:2 JGD: hofal
change(411298, note=f'{SCHORCH}, pp. 120-121: passive of the causative stem (hof) instead of MT hif', vs=('hif', 'hof'))
change(432910, note=f'{SCHORCH}, p. 221: passive, the equivalent of the hof, instead of MT hif', vs=('hif', 'hof'))
# Gen 21:7 JNJQH: qal active participle
change(415244, note=f'{SCHORCH}, p. 153: qal active participle fem. sg. preceded by the interjection H (MT hif perfect)',
       vs=('hif', 'qal'), g_vbs=(']]', ''), ETCBC_parsing=(']]JN&JQ[/H', 'JN&JQ[/H'))
# qal -> piel:
#   Gen 21:6 JYXQ (YXQ always piel), 25:24 JML>W (ML> with time expressions), 31:27 NXBT,
#   32:17 <BRW, 38:17 CLXK (šal'lāk)
#   and the regular Samaritan piel of CLX, C>L and <BR (gemination or ē-prefix in phono_transcr):
#   Gen 19:10 JCLXW; C>L in 32:18, 37:15, 43:7 (perfect; the infinitive stays qal), 44:19;
#   <BR in 18:3, 30:32, 31:52 (x2), 33:14.
CLX_NOTE = (f'{SCHORCH}, p. 97 (ad Gen 3:22): CLX is always piel in the Samaritan tradition, except the qal passive '
            'participle in Gen 32:19 and 49:21; no separate entry for this verse')
C_L_NOTE = (f'{SCHORCH}, p. 164 (ad Gen 24:47): C>L is always piel in the Samaritan tradition, except the qal '
            'infinitive in Gen 43:7; no separate entry for this verse')
BR_NOTE = (f'{SCHORCH}, p. 119 (ad Gen 12:6): in Samaritan Hebrew <BR is more often piel than qal, without difference '
           'in meaning; no separate entry for this verse')
for w, note in ((415235, f'{SCHORCH}, p. 153: YXQ is only piel in the Samaritan tradition, see pp. 139-140 (ad Gen 17:17)'),
                (418345, f'{SCHORCH}, p. 167: ML> is always piel with time expressions'),
                (422454, f'{SCHORCH}, p. 181: piel of a secondary root NXB instead of MT XB>'),
                (423350, f'{SCHORCH}, p. 186: piel instead of MT qal, see p. 119 (ad Gen 12:6)'),
                (426727, f'{SCHORCH}, p. 199: piel instead of MT qal, see p. 97 (ad Gen 3:22)'),
                (414154, CLX_NOTE),
                (423373, C_L_NOTE), (426037, C_L_NOTE), (429838, C_L_NOTE), (430787, C_L_NOTE),
                (413391, BR_NOTE), (421623, BR_NOTE), (422963, BR_NOTE), (422974, BR_NOTE), (423916, BR_NOTE)):
    change(w, note=note, vs=('qal', 'piel'))

# ---------------------------------------------------------------------------------------
# A2 Lexemes
# ---------------------------------------------------------------------------------------
change(406752, note=f'{SCHORCH}, p. 93: RWX= "relief" (Tiberian rewaḥ), not RWX "wind"',
       lex=('RWX/', 'RWX=/'), ETCBC_parsing=('RWX/', 'RWX=/'))                      # Gen 3:8
change(409101, note=f'{SCHORCH}, p. 107: root QWL, a younger by-form of QLL, as in Gen 8:11',
       lex=('QLL[', 'QWL['), ETCBC_parsing=('QL(L[W', 'Q(WL[W'))                    # Gen 8:8
for w, note in ((409145, f'{SCHORCH}, p. 107: hif of XLL "begin" instead of MT XJL/XWL "wait"'),  # Gen 8:10
                (409186, f'{SCHORCH}, p. 108: hif of XLL "begin"; JXL is not attested in the Samaritan reading')):  # Gen 8:12
    change(w, note=note, lex=('XLL===[', 'XLL['), ETCBC_parsing=('!J!XL(L===[', '!J!]]XL(L['))
change(410474, note=f'{SCHORCH}, pp. 116-117: piel of BLH "destroy" instead of MT BLL "confuse"',
       lex=('BLL[', 'BLH['), g_lex=('BL', 'BLH'), g_vbe=('[H', '['),                 # Gen 11:7
       ETCBC_parsing=('!N!BL(L[H=', '!N!BLH['))
change(411712, note=f'{SCHORCH}, p. 124: hif of >HL, "he pitched the tent" (MT qal)',
       lex=('>WL[', '>HL['), ETCBC_parsing=('!J!]]>(WL[', '!J!]]>(HL['))            # Gen 13:18
for w, note in ((413018, f'{SCHORCH}, p. 138: MWL is always qal in Samaritan Hebrew (MT nif)'),  # Gen 17:10
                (413060, f'{SCHORCH}, pp. 138-139: both forms of the figura etymologica are qal of MWL, see ad Gen 17:10')):
    change(w, note=note, lex=('NML[', 'MWL['), ETCBC_parsing=('!!(NM&WL[/', '!!MWL[/'))
change(413613, note=f'{SCHORCH}, p. 144: ʾenūšam "angels", derived from >NWC, see ad Gen 18:2',
       lex=('>JC/', '>NWC/'), ETCBC_parsing=('>(J&N&WC/JM', '>NWC/JM'))             # Gen 18:16
change(415525, note=f'{SCHORCH}, p. 155: qal active participle of RBH "be great" ("a great one of the bow")',
       lex=('RBH=[', 'RBH['), ETCBC_parsing=('RB(H&J=[/', 'RB(H&J[/'))              # Gen 21:20
change(415526, note=f'{SCHORCH}, p. 155: QCT "bow" ("a great one of the bow")',
       lex=('QCT=/', 'QCT/'), ETCBC_parsing=('QCT=/', 'QCT/'))
change(423538, note=f'{SCHORCH}, pp. 187-188: root GW<, a secondary formation from NG< "touch"',
       lex=('GW<[', 'GW<=['), ETCBC_parsing=('!J!G(W<[', '!J!G(W<=['))              # Gen 32:26
change(424905, note=f'{SCHORCH}, p. 195: qal of SWK, a by-form of NSK',
       lex=('NSK[', 'SWK['), ETCBC_parsing=('!J!(NSK[', '!J!S(WK['))                # Gen 35:14
change(428056, note=f'{SCHORCH}, p. 202: derived from the root QWY "wake", see ad Gen 9:24',
       lex=('JQY[', 'QWY==['), ETCBC_parsing=('!J!(JQY[', '!J!Q(WY==['))            # Gen 41:7
change(433541, note=f'{SCHORCH}, p. 230: XLB= "fat", not XLB "milk"',
       lex=('XLB/', 'XLB=/'), ETCBC_parsing=('XLB/', 'XLB=/'))                      # Gen 49:12
change(433633, note=f'{SCHORCH}, p. 235: "shofar" (CWPR)',
       lex=('CPR/', 'CWPR/'), ETCBC_parsing=('CPR/', 'C(WPR/'))                     # Gen 49:21
# Gen 31:30: NKSP[ qal instead of KSP[ nifal
change(422519, note=f'{SCHORCH}, pp. 182-183: qal of the quadriliteral root NKSP, a secondary extension of KSP',
       lex=('KSP[', 'NKSP['), vs=('nif', 'qal'), g_vbs=(']N]', ''), g_lex=('KSP', 'NKSP'),
       ETCBC_parsing=('!!]N]KSP[/:a', '!!NKSP[/:a'))
change(422520, note=f'{SCHORCH}, pp. 182-183: qal of the quadriliteral root NKSP, a secondary extension of KSP',
       lex=('KSP[', 'NKSP['), vs=('nif', 'qal'), g_vbs=(']N]', ''), g_lex=('KSP', 'NKSP'),
       ETCBC_parsing=(']N]KSP[T', 'NKSP[T'))
# Gen 31:39 >XVNH (ʿāʾīṭinnå): XWV[ hifil instead of XV>[
change(422717, note=f'{SCHORCH}, p. 183: hif imperfect 1sg of the root XWV + suffix 3fs instead of MT XV>',
       lex=('XV>[', 'XWV['), ETCBC_parsing=('!>!XV(>[~N+H==', '!>!]]X(WV[~N+H=='))

# ---------------------------------------------------------------------------------------
# A3 Lexeme + part of speech
# ---------------------------------------------------------------------------------------
# Gen 3:9 >JKH "how", without suffix
change(406779, note=f'{SCHORCH}, p. 94: >JKH "how" (Tiberian ʾêkâ), without suffix',
       lex=('>J', '>JKH'), g_lex=('>J', '>JKH'), g_uvf=('~', ''), g_prs=('+KH', ''),
       prs_ps=('p2', 'NA'), prs_nu=('sg', 'NA'), prs_gn=('m', 'NA'), ETCBC_parsing=('>J~(N+K&H=', '>JKH'))
# Gen 14:20 MGN/ "shield" (as 15:1). Its phrase becomes a noun phrase.
change(412115, note=f'{SCHORCH}, p. 127: noun MGN "shield"; the verb MGN does not exist in the Samaritan tradition',
       lex=('MGN[', 'MGN/'), sp=('verb', 'subs'), vs=('hif', ''), vt=('perf', 'NA'), ps=('p3', 'NA'),
       gn=('m', 'unknown'), g_vbs=(']]', ''), g_vbe=('[', ''), g_nme=('', '/'), ETCBC_parsing=('MGN[', 'MGN/'))
change(L.u(412115, 'phrase')[0], note=f'{SCHORCH}, p. 127: phrase type and function follow from MGN as a noun',
       typ=('VP', 'NP'), function=('Pred', 'PreC'))
# Gen 16:8 >WJ interjection
change(412714, note=f'{SCHORCH}, p. 135: interjection >WJ (Tiberian ʾôy)',
       lex=('>J', '>WJ'), sp=('inrg', 'intj'), ETCBC_parsing=('>&WJ', '>WJ'))
# Gen 25:8, 25:17, 26:11, 26:20 <MW: "his people" (ʿammu)
AMMU_NOTE = f'No entry in Schorch: phono_transcr ʿammu, read as <M/ "his people" as in Gen 25:8 ({SCHORCH}, p. 165)'
for w, note in ((418092, f'{SCHORCH}, p. 165: noun <M/ in the singular, "his people", confirmed by the targumim'),
                (418231, f'{SCHORCH}, pp. 166-167: noun <M/ in the singular, "his people", see p. 165 (ad Gen 25:8)'),
                (418739, AMMU_NOTE), (418903, AMMU_NOTE)):
    change(w, note=note, lex=('<M', '<M/'), sp=('prep', 'subs'), nu=('NA', 'sg'), gn=('NA', 'm'), g_nme=('', '/'),
           ETCBC_parsing=('<M+W=', '<M/+W='))
# In 26:20 <MW is the whole phrase: "for his people quarrelled".
change(L.u(418903, 'phrase')[0], typ=('PP', 'NP'), function=('Cmpl', 'Subj'))
# Gen 30:3 BRKJ (birrūki): piel infinitive of BRK[ + 1sg instead of "knees"
change(421174, note=f'{SCHORCH}, p. 178: verbal noun of BRK piel, "for my blessing", not BRK "knee"',
       lex=('BRK/', 'BRK['), sp=('subs', 'verb'), vs=('', 'piel'), vt=('NA', 'inf'), ps=('NA', 'unknown'),
       nu=('du', 'unknown'), gn=('f', 'unknown'), g_pfm=('', '!!'), g_vbe=('', '['), g_nme=('/J', '/'),
       g_prs=('+', '+J'), ETCBC_parsing=('BRK/J=+(J', '!!BRK[/+J'))
# Gen 49:24 CM/ "name"
change(433667, note=f'{SCHORCH}, p. 236: noun CM "name" instead of MT "from there"',
       lex=('CM', 'CM/'), sp=('advb', 'subs'), nu=('NA', 'sg'), gn=('NA', 'm'), g_nme=('', '/'),
       ETCBC_parsing=('CM', 'CM/'))

# ---------------------------------------------------------------------------------------
# A4 >T versus >T==
# ---------------------------------------------------------------------------------------
change(421526, note=f'{SCHORCH}, p. 179: preposition >T== "with" instead of the MT object marker',
       lex=('>T', '>T=='), ETCBC_parsing=('>T+K=', '>T==+K='))                      # Gen 30:26
change(424076, note=f'{SCHORCH}, p. 192: preposition >T== "with", see ad Gen 19:33',
       lex=('>T', '>T=='), ETCBC_parsing=('>T+H==', '>T==+H=='))                    # Gen 34:2
change(410972, note=f'{SCHORCH}, p. 118: object marker + suffix after the hif of JY>, instead of MT "with"',
       lex=('>T==', '>T'), ETCBC_parsing=('>T==+M', '>T+M'))                        # Gen 11:31

# ---------------------------------------------------------------------------------------
# A5 Person, gender, number
# ---------------------------------------------------------------------------------------
# singular -> plural
change(406714, note=f'{SCHORCH}, p. 92: PRJ "fruit" in the plural',
       nu=('sg', 'pl'), ETCBC_parsing=('PRJ/+W=', 'PRJ/(J+W='))                     # Gen 3:6
change(432574, note=f'{SCHORCH}, p. 219: GWJH "body" in the plural',
       nu=('sg', 'pl'), g_nme=('/T', '/TJ'), g_uvf=('~J', ''),                       # Gen 47:18
       ETCBC_parsing=('GWJ(H/T~J+NW', 'GWJ(H/(WTJ+NW'))
ADMH_19 = f'{SCHORCH}, p. 220: >DMH "land" in the plural (three times in Gen 47:19)'
for w, note in ((432576, f'{SCHORCH}, p. 219: >DMH "land" in the plural'),                  # Gen 47:18
                (432584, ADMH_19), (432589, ADMH_19), (432596, ADMH_19)):                     # Gen 47:19
    change(w, note=note, nu=('sg', 'pl'), ETCBC_parsing=('>DM(H/T+NW', '>DM(H/(WT+NW'))
# plural -> singular
change(406550, note=f'{SCHORCH}, p. 89: <YM "bone" in the singular',
       nu=('pl', 'sg'), g_nme=('/J', '/'), g_prs=('+', '+J'),                        # Gen 2:23
       ETCBC_parsing=('<YM/J+(J', '<YM/+J'))
change(428102, note=f'{SCHORCH}, p. 203: XV> "sin" in the singular',
       nu=('pl', 'sg'), g_nme=('/J', '/'), g_prs=('+', '+J'),                        # Gen 41:9
       ETCBC_parsing=('XV>/J+(J', 'XV>/+J'))
change(431714, note=f'{SCHORCH}, pp. 215-216: BT "daughter" in the singular',
       nu=('pl', 'sg'), g_nme=('/TJ', '/T'), g_uvf=('', '~J'),                       # Gen 46:7
       ETCBC_parsing=('B(T&N/(WTJ+W=', 'B(T&N/T~J+W='))
BRKH_25 = f'{SCHORCH}, pp. 237-238: BRKH "blessing" in the singular (three times in Gen 49:25)'
BRKH_26 = f'{SCHORCH}, p. 239: BRKH "blessing" in the singular (twice in Gen 49:26), see pp. 237-238'
for w, note in ((433680, BRKH_25), (433684, BRKH_25), (433688, BRKH_25),                     # Gen 49:25
                (433692, BRKH_26), (433698, BRKH_26)):                                       # Gen 49:26
    change(w, note=note, nu=('pl', 'sg'), ETCBC_parsing=('BRK(H/(WT', 'BRK(H/T'))
change(433699, note=f'{SCHORCH}, p. 239: HR "mountain" in the singular',
       nu=('pl', 'sg'), g_nme=('/J', '/'), g_uvf=('', '~J'), ETCBC_parsing=('HR/J', 'HR/~J'))  # Gen 49:26
change(433702, note=f'{SCHORCH}, pp. 239-240: GB<H "hill" in the singular, as in Deut 33:15',
       nu=('pl', 'sg'), ETCBC_parsing=('GB<(H/(WT', 'GB<(H/T'))
# Gen 44:28 >MR: 3rd person masculine singular (qal passive)
change(430936, note=f'{SCHORCH}, p. 213: qal passive perfect 3ms ("it was said") instead of MT 1sg',
       ps=('p1', 'p3'), gn=('unknown', 'm'))
# Gen 8:7 JY> participle: masculine singular, without the stray :a
change(409080, note=f'{SCHORCH}, p. 106: participle (yāṣa) instead of the MT infinitive absolute',
       nu=('unknown', 'sg'), gn=('unknown', 'm'), ETCBC_parsing=('JY>[/:a', 'JY>[/'))
# Gen 37:7 NYBH participle: person unknown
change(425869, note=f'{SCHORCH}, p. 197: qal active participle, so person is unknown',
       ps=('p3', 'unknown'))

# ---------------------------------------------------------------------------------------
# A6 ETCBC_parsing consistency
# ---------------------------------------------------------------------------------------
change(411189, ETCBC_parsing=('NS<[/:a', 'NS<[/'))                                         # Gen 12:9, stray :a
change(423894, ETCBC_parsing=('JD<[', '!J!(JD<['))                                         # Gen 33:13, missing !J!

# Add the stem formative ]] to every parse that lacks it while g_vbs is ]].
# It goes directly after the preformative, as in !J!]](NGD[.
fixed_stem = 0
for w in F.otype.s('word'):
    parse = nf['ETCBC_parsing'][w]
    if nf['g_vbs'].get(w) == ']]' and not re.search(r'\][^\[\]]*\]', parse):
        assert T.sectionFromNode(w)[0] == 'Genesis'
        m = re.match(r'!.*?!', parse)
        pos = m.end() if m else 0
        change(w, ETCBC_parsing=(parse, f'{parse[:pos]}]]{parse[pos:]}'))
        fixed_stem += 1
# 78 parses lacked ]] in 7.3.0; four of them (409145, 409186, 412115, 422717) are handled above.
assert fixed_stem == 74, fixed_stem

for w in changed_words:
    nf['mt_feat'][w] = ''

# Only changed nodes have a grammar note, and every note refers to a page in Schorch.
# The ETCBC_parsing consistency fixes (A6) and the phrase in Gen 26:20 have no such reference, so no note.
assert set(grammar_notes) <= changed_words | {L.u(412115, 'phrase')[0]}, set(grammar_notes) - changed_words
assert all(re.search(r'Schorch 2004, pp?\. \d+', note) for note in grammar_notes.values())
assert len(grammar_notes) == 73, len(grammar_notes)  # 72 words + the phrase in Gen 14:20
node_features['grammar_note'] = grammar_notes

print(f'{len(changed_words)} words changed')

meta_data = {f: read_metadata(os.path.join(old_location, f'{f}.tf')) for f in feature_names}
meta_data['grammar_note'] = {
    **{k: v for k, v in meta_data['mt_feat'].items() if k != 'description'},
    'description': 'reason for a correction in version 7.4.0, with the page in Schorch, Die Vokale des Gesetzes I (2004)',
}

TF.save(
    nodeFeatures=node_features,
    edgeFeatures={'oslots': oslots},
    metaData=meta_data,
    location=TF_FOLDER,
    module=NEW_VERSION,
)
