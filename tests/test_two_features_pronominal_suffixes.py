import os
import pytest

from tf.fabric import Fabric
data_path = '/home/runner/work/sp/sp/tf'
data_version = '1.5.5'
TF = Fabric(locations=os.path.join(data_path, data_version))
api = TF.load('''
    otype g_prs prs_gn
''')
api.loadLog()
api.makeAvailableIn(globals())

F, L = api.F, api.L 


def test_lexemes_verb_ending():
    allowed_combinations_g_prs_prs_gn = {('+J', 'unknown'), 
        ('+HW', 'm'), ('+KM', 'm'),
        ('+H', 'f'), (']H]', 'NA'), ('+NW', 'unknown'), 
        ('+W', 'm'), ('+KN', 'f'), ('+', 'unknown'), 
        ('+MW', 'm'), ('+KH', 'm'), ('+NH', 'f'), 
        ('+HN', 'f'), ('+K', 'm'), ('+NJ', 'unknown'),
        ('+W', 'unknown'), ('+M', 'm'), ('+K', 'f'), 
        ('+HM', 'm')}
    assert all([(F.g_prs.v(w), F.prs_gn.v(w)) in allowed_combinations_g_prs_prs_gn
        for w in F.otype.s('word') 
        if F.g_prs.v(w) not in {'absent', ''}])