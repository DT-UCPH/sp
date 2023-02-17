import os
import pytest

from tf.fabric import Fabric
data_path = '/home/runner/work/sp/sp/tf'
data_version = '1.5.5'
TF = Fabric(locations=os.path.join(data_path, data_version))
api = TF.load('''
    otype g_prs prs_gn prs_ps
''')
api.loadLog()
api.makeAvailableIn(globals())

F, L = api.F, api.L 


def test_combinations_of_g_prs_and_prs_gn():
    allowed_combinations_g_prs_prs_gn = {('+J', 'unknown'), 
        ('+HW', 'm'), ('+KM', 'm'),
        ('+H', 'f'), (']H]', 'NA'), 
        ('+NW', 'unknown'), ('+W', 'm'), 
        ('+KN', 'f'), ('+', 'unknown'), 
        ('+MW', 'm'), ('+KH', 'm'), 
        ('+NH', 'f'), ('+HN', 'f'), 
        ('+K', 'm'), ('+NJ', 'unknown'),
        ('+W', 'unknown'), ('+M', 'm'), 
        ('+K', 'f'), ('+HM', 'm')}
    assert all([(F.g_prs.v(w), F.prs_gn.v(w)) in allowed_combinations_g_prs_prs_gn
        for w in F.otype.s('word') 
        if F.g_prs.v(w) not in {'absent', ''}])

def test_combinations_of_g_prs_and_prs_ps():
    allowed_combinations_g_prs_prs_ps = {('+W', 'p3'), 
    ('+K', 'p2'), ('+J', 'p1'), ('+NJ', 'p1'), 
    ('+KM', 'p2'), ('+', 'p1'), ('+NH', 'p3'), 
    ('+M', 'p3'), ('+MW', 'p3'), ('+HN', 'p3'), 
    ('+KN', 'p2'), ('+NW', 'p1'), ('+HW', 'p3'), 
    ('+KH', 'p2'), ('+HM', 'p3'), ('+H', 'p3'), 
    ('+W', 'p1')}
    assert all([(F.g_prs.v(w), F.prs_ps.v(w)) in allowed_combinations_g_prs_prs_ps
        for w in F.otype.s('word') 
        if F.g_prs.v(w) not in {'absent', ''}])