import os
import re
import pytest

from tf.fabric import Fabric

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TF_FOLDER = 'tf'
latest_data_folder = sorted(os.listdir(os.path.join(ROOT_DIR, TF_FOLDER)))[-1]

TF = Fabric(locations=os.path.join(ROOT_DIR, TF_FOLDER, latest_data_folder))
api = TF.load('''
    otype g_cons lex g_pfm g_vbs g_lex g_vbe g_nme g_uvf g_prs sp vt ps nu gn prs_nu prs_ps prs_gn
''')
api.loadLog()
api.makeAvailableIn(globals())

F, L = api.F, api.L


def test_lexemes_verb_ending():
    assert all([F.lex.v(w)[-1] == '[' for w in F.otype.s('word') if F.sp.v(w) == 'verb'
                   and F.lex.v(w) !='absent'])

def test_lexemes_advb_conj_prep_pron_nega_inrg_intj_ending():
    assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') 
               if F.sp.v(w) in {'advb', 'conj', 'art', 'prep', 'prps', 'prde', 'prin', 'intj', 'nega', 'inrg'}])
    
def test_lexemes_subs_adjv_ending():
    assert all([F.lex.v(w)[-1] == '/' for w in F.otype.s('word') 
               if F.sp.v(w) in {'subs', 'nmpr', 'adjv'}])

def test_nominal_ending():
    assert all({F.g_nme.v(w) for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr', 'adjv'}})

def test_expected_nominal_ending():
    assert all({F.g_nme.v(w)[0] == '/' for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr', 'adjv'}
                 and F.g_nme.v(w) and F.g_nme.v(w) !='absent'})

def test_unexpected_nominal_ending():
    assert all({not F.g_nme.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'subs','nmpr', 'adjv','verb'}  and F.g_nme.v(w) != 'absent'})

def test_verbal_ending():
    assert all({F.g_vbe.v(w) for w in F.otype.s('word') if F.sp.v(w) in {'verb'}})

def test_expected_verbal_ending():
    assert all({F.g_vbe.v(w)[0] == '[' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_vbe.v(w) and F.g_vbe.v(w) !='absent'})

def test_unexpected_verbal_ending():
    assert all({not F.g_vbe.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb','absent'} and F.g_vbe.v(w) != 'absent'})
      
def test_expected_preformative_beginning():
    assert all({F.g_pfm.v(w)[0] == '!' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_pfm.v(w) and F.g_pfm.v(w) !='absent'})

def test_expected_preformative_ending():
    assert all({F.g_pfm.v(w)[-1] == '!' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_pfm.v(w) and F.g_pfm.v(w) !='absent'})

def test_unexpected_preformative():
    assert all({not F.g_pfm.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb'}})

def test_expected_verbal_stem_beginning():
    assert all({F.g_vbs.v(w)[0] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})

def test_expected_verbal_stem_ending():
    assert all({F.g_vbs.v(w)[-1] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})

def test_unexpected_verbal_stem():
    assert all({not F.g_vbs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb','absent'}})

def test_uvf_beginning():
    assert all({F.g_uvf.v(w)[0] == '~' for w in F.otype.s('word') if F.g_uvf.v(w)})

def test_uvf_H():
    assert all({F.sp.v(w) in {'advb', 'nmpr', 'subs'} for w in F.otype.s('word') if F.g_uvf.v(w) == '~H'})

def test_uvf_J():
    assert all({F.sp.v(w) in {'adjv','subs'} or F.vt.v(w) in {'infc','ptca','ptcp'} for w in F.otype.s('word') if F.g_uvf.v(w) == '~J'})

def test_uvf_N():
    assert all({F.sp.v(w) in {'verb','subs','intj','inrg'} for w in F.otype.s('word') if F.g_uvf.v(w) == '~N' and F.g_prs.v(w)})

def test_expected_prs_beginning():
    assert all({F.g_prs.v(w)[0] == '+' for w in F.otype.s('word') if F.g_prs.v(w)})

def test_unexpected_prs():
    assert all({not F.g_prs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'subs','verb','prep','inrg','intj','adjv','absent'}})

def test_morphemes_combined():
    assert all({re.sub('[\]\[\!\/\+\~]','',f'{F.g_pfm.v(w)}{F.g_vbs.v(w)}{F.g_lex.v(w)}{F.g_vbe.v(w)}{F.g_nme.v(w)}{F.g_uvf.v(w)}{F.g_prs.v(w)}') == F.g_cons.v(w)
                for w in F.otype.s('word') if F.lex.v(w) != 'absent'})

def test_unexpected_verbal_tense():
    assert all({F.vt.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) not in {'verb'}})

def test_expected_verbal_tense():
    assert all({F.vt.v(w) != 'NA' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}})

def test_perf_tense():
    assert all({F.vt.v(w) == 'perf' for w in F.sp.s('verb') if not F.g_pfm.v(w) and not F.g_nme.v(w)
                    and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_perf_tense_morphemes():
     assert all({not F.g_pfm.v(w) and not F.g_nme.v(w) for w in F.sp.s('verb') if F.vt.v(w) == 'perf'
                and F.sp.v(w) != 'absent' 
                and F.vt.v(w) != 'absent'})

def test_impf_tense():
    assert all({F.vt.v(w) in {'impf','wayq'} for w in F.sp.s('verb') 
                if F.g_pfm.v(w)
                and F.g_pfm.v(w) not in {'!!','!H!'} 
                and not F.g_nme.v(w) 
                and F.sp.v(w) != 'absent'
                and F.vt.v(w) != 'absent'})

def test_impf_tense_morphemes():
    assert all({F.g_pfm.v(w) and not F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w) for w in F.sp.s('verb')
                     if F.vt.v(w) in {'impf','wayq'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_impv_tense():
    assert all({F.vt.v(w) == 'impv' for w in F.sp.s('verb') if F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w)
                and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_impv_tense_morphemes():
    assert all({F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w) for w in F.sp.s('verb')
                if F.vt.v(w) == 'impv' and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_infinitive_tense():
    assert all({F.vt.v(w) in {'infc','infa'} for w in F.sp.s('verb') if F.g_pfm.v(w) in {'!!','!H!'}
                and F.g_nme.v(w) and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_infinitive_tense_morphemes():
    assert all({F.g_pfm.v(w) in {'!!','!H!','!M!'} and F.g_nme.v(w) for w in F.sp.s('verb')
                 if F.vt.v(w) in {'infc','infa'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_participle_tense():
    assert all({F.vt.v(w) in {'infc','ptca','ptcp'} for w in F.sp.s('verb') if F.g_pfm.v(w) in {'','!M!'}
                and F.g_nme.v(w) and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_participle_tense_morphemes():
    assert all({F.g_pfm.v(w) in {'','!M!'} and F.g_nme.v(w) for w in F.sp.s('verb')
             if F.vt.v(w) in {'ptca','ptcp'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})

def test_expected_person():
    assert all({F.ps.v(w) in {'p1','p2','p3','unknown'} for w in F.otype.s('word') if F.sp.v(w) in {'verb','prps'}
              and F.ps.v(w) != 'absent'})

def test_unexpected_person():
    assert all({F.ps.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) not in {'verb','prps'}})

def test_first_person():
    assert all({F.g_pfm.v(w) in {'','!>!','!N!'} and F.g_vbe.v(w) in {'[', '[H', '[NW', '[TJ'} for w in F.sp.s('verb')
                if F.ps.v(w) == 'p1'})

def test_second_person():
    assert all({F.g_pfm.v(w) in {'','!!','!H!','!T!'} and F.g_vbe.v(w) in {'[','[H','[J','[JN','[N','[NH','[T','[TH','[TJ',
            '[TM','[TN','[W','[WN'} for w in F.sp.s('verb') if F.ps.v(w) == 'p2'})

def test_third_person():
    assert all({F.g_pfm.v(w) in {'','!J!','!T!'} and F.g_vbe.v(w) in {'[','[H','[HN','[NH','[T','[TH','[W','[WN'} 
                 for w in F.sp.s('verb') if F.ps.v(w) == 'p3'})

def test_unknown_person():
    assert all({F.g_pfm.v(w) in {'','!!','!H!','!M!'} and F.g_vbe.v(w) in {'['} and F.g_nme.v(w) 
                in {'/','/H','/J','/JM','/T','/TJ','/WT'} for w in F.otype.s('word') if F.ps.v(w) == 'unknown'})

def test_first_person_sfx():
    assert all({F.g_prs.v(w) in {'+','+J','+NJ','+NW','+W'} for w in F.otype.s('word') if F.prs_ps.v(w) == 'p1'})

def test_second_person_sfx():
    assert all({F.g_prs.v(w) in {'+K','+KH','+KM','+KN'} for w in F.otype.s('word') if F.prs_ps.v(w) == 'p2'})

def test_third_person_sfx():
    assert all({F.g_prs.v(w) in {'+H','+HM','+HN','+HW','+M','+MW','+NH','+W'} for w in F.otype.s('word') 
                if F.prs_ps.v(w) == 'p3'})

def test_expected_number():
    assert all({F.nu.v(w) in {'sg','du','pl','unknown'} for w in F.otype.s('word') if F.sp.v(w) 
                in {'subs','nmpr','adjv','verb','prps','prde','prin'} and F.nu.v(w) != 'absent'})

def test_unexpected_number():
    assert all({F.nu.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) 
                not in {'subs','nmpr','adjv','verb','prps','prde','prin'} and F.nu.v(w) != 'absent'})

def test_singular_number():
    assert all({F.g_pfm.v(w) in {'','!!','!>!','!H!','!J!','!M!','!T!'} and F.g_vbe.v(w) 
                in {'','[','[H','[J','[JN','[T','[TH','[TJ'} and F.g_nme.v(w) in {'','/','/H','/J','/T'} 
                for w in F.otype.s('word') if F.nu.v(w) == 'sg'})

def test_dual_number():
    assert all({not F.g_pfm.v(w) and not F.g_vbe.v(w) and F.g_nme.v(w) in {'/J','/JM','/TJ','/TJM'} 
         for w in F.otype.s('word') if F.nu.v(w) == 'du'})

def test_plural_number():
    assert all({F.g_pfm.v(w) in {'','!!','!H!','!J!','!M!','!N!','!T!'} and F.g_vbe.v(w) 
                    in {'','[','[H','[HN','[N','[NH','[NW','[TM','[TN','[W','[WN'}
                     and F.g_nme.v(w) in {'','/','/J','/JM','/M','/T','/TJ','/WT','/WTJ'}
                     for w in F.otype.s('word') if F.nu.v(w) == 'pl'})
 
def test_unknown_number():
    assert all({F.g_pfm.v(w) in {'','!!','!H!'} and F.g_vbe.v(w) in {'','['} and F.g_nme.v(w) in {'','/','/H','/T','/WT'}
                for w in F.otype.s('word') if F.nu.v(w) == 'unknown'})

def test_singular_number_sfx():
    assert all({F.g_prs.v(w) in {'+','+H','+HW','+J','+K','+KH','+NJ','+W'} for w in F.otype.s('word') 
                if F.prs_nu.v(w) == 'sg'})

def test_plural_number_sfx():
    assert all({F.g_prs.v(w) in {'+HM','+HN','+KM','+KN','+M','+MW','+NH','+NW','+W'} for w in F.otype.s('word') 
                if F.prs_nu.v(w) == 'pl'})

def test_expected_gender():
    assert all({F.gn.v(w) in {'m','f','unknown'} for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr','adjv','verb','prps','prde','prin'}
              and F.ps.v(w) != 'absent'})

def test_unexpected_gender():
    assert all({F.gn.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) 
                not in {'subs','nmpr','adjv','verb','prps','prde','prin'} and F.gn.v(w) != 'absent'})

def test_masculine_gender():
    assert all({F.g_pfm.v(w) in {'','!!','!J!','!T!','!M!','!H!'} and F.g_vbe.v(w) in {'','[','[W','[WN','[H','[T','[TH','[TM'}
                 and F.g_nme.v(w) in {'','/','/J','/JM','/M','/T','/TJ','/WT'} for w in F.otype.s('word') if F.gn.v(w) == 'm'})

def test_feminine_gender():
    assert all({F.g_pfm.v(w) in {'','!!','!J!','!T!','!M!'} and F.g_vbe.v(w) in {'','[','[H','[HN','[J','[JN','[N','[NH','[T','[TH','[TJ','[TN'}
                  and F.g_nme.v(w) in {'','/','/H','/J','/JM','/T','/TJ','/TJM','/WT','/WTJ'} for w in F.otype.s('word') if F.gn.v(w) == 'f'})

def test_unknown_gender():
    assert all({F.g_pfm.v(w) in {'','!!','!>!','!H!','!N!'} and F.g_vbe.v(w) in {'','[','[H','[NW','[TJ','[W'}
                  and F.g_nme.v(w) in {'','/','/H','/J','/JM','/T','/TJ','/WT'} for w in F.otype.s('word') if F.gn.v(w) == 'unknown'})

def test_masculine_gender_sfx():
    assert all({F.g_prs.v(w) in {'+HM','+HW','+K','+KH','+KM','+M','+MW','+W'} for w in F.otype.s('word') if F.prs_gn.v(w) == 'm'})

def test_feminine_gender_sfx():
    assert all({F.g_prs.v(w) in {'+H','+HN','+K','+KN','+NH'} for w in F.otype.s('word') if F.prs_gn.v(w) == 'f'})