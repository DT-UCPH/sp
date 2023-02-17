import os
import pytest

from tf.fabric import Fabric
data_path = '/home/runner/work/sp/sp/tf'
data_version = '1.5.5'
TF = Fabric(locations=os.path.join(data_path, data_version))
api = TF.load('''
    otype lex sp g_nme g_vbe g_pfm g_vbs g_prs vt ps nu prs_nu prs_ps
''')
api.loadLog()
api.makeAvailableIn(globals())

F, L = api.F, api.L 