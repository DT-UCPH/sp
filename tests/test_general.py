
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

    
def test_lexemes_nouns_adjv_ending():
    assert all([F.lex.v(w)[-1] == '/' for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr', 'adjv'} 
               and F.lex.v(w) !='absent'])

def test_lexemes_verb_ending():
    assert all([F.lex.v(w)[-1] == '[' for w in F.otype.s('word') if F.sp.v(w) == 'verb'
                   and F.lex.v(w) !='absent'])

def test_lexemes_advb_conj_prep_pron_nega_inrg_ending():
    assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') 
               if F.sp.v(w) in {'advb', 'conj', 'art', 'prep', 'prps','prde','prin', 'intj', 'nega', 'inrg'}
               and F.lex.v(w) !='absent'])

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
    assert all({not F.g_pfm.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb', 'absent'}})

def test_expected_verbal_stem_beginning():
    assert all({F.g_vbs.v(w)[0] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})

def test_expected_verbal_stem_ending():
    assert all({F.g_vbs.v(w)[-1] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})

def test_unexpected_verbal_stem():
    assert all({not F.g_vbs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb','absent'}})

def test_expected_prs_beginning():
    assert all({F.g_prs.v(w)[0] == '+' for w in F.otype.s('word') if F.g_prs.v(w) and F.g_prs.v(w) !='absent'})

def test_unexpected_prs():
    assert all({not F.g_prs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'subs','verb','prep','inrg','intj','adjv','absent'}})

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
    assert all({F.g_pfm.v(w) in {'','!!','!H!','!T!'} and F.g_vbe.v(w) in {'[','[H','[J','[JN','[N','[T','[TH','[TJ',
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
