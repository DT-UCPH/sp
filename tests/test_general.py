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
