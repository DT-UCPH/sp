import os
import pytest

from tf.fabric import Fabric
data_path = '/home/runner/work/sp/sp/tf/1.5.5'
TF = Fabric(locations=data_path)
api = TF.load('''
    otype lex
''')
api.loadLog()
api.makeAvailableIn(globals())


def test_equality():
    print('Current WD', os.getcwd())
    assert 1 == 1

def test_inequality():
    assert 1 == 2
    
def test_lexemes_nouns_ending():
    assert all([F.lex.v(w)[-1] == '/' for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr'} 
               and F.lex.v(w) !='absent'])
