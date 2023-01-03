import logging
import pytest

from tf.app import use
A = use('DT-UCPH/sp:hot', hoist=globals())

logging.basicConfig(
    filename='./logs/test_data_sp.log',
    level = logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def test_lexemes_nouns_ending():
    try:
        assert all([F.lex.v(w)[-1] == '/' for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr'} 
                    and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_nouns_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_nouns_ending: there is at least one word without '/' at the end")
        
def test_lexemes_adjv_ending():
    try:
        assert all([F.lex.v(w)[-1] == '/' for w in F.otype.s('word') if F.sp.v(w) == 'adjv'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_adjv_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_adjv_ending: there is at least one word without '/' at the end")
        
def test_lexemes_verb_ending():
    try:
        assert all([F.lex.v(w)[-1] == '[' for w in F.otype.s('word') if F.sp.v(w) == 'verb'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_verbs_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_verbs_ending: there is at least one word without '[' at the end")
        
def test_lexemes_advb_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'advb'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_advb_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_advb_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_conj_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'conj'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_conj_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_conj_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_art_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'art'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_art_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_art_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_prep_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'prep'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_prep_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_prep_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_pron_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) in {'prps','prde','prin'}
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_pron_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_pron_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_intj_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'intj'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_intj_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_intj_ending: there is at least one word with '/' or '[' at the end")

def test_lexemes_nega_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'nega'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_nega_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_nega_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_inrg_ending():
    try:
        assert all([F.lex.v(w)[-1] not in {'/','['} for w in F.otype.s('word') if F.sp.v(w) == 'inrg'
                   and F.lex.v(w) !='absent'])
        logging.info("Testing lexemes_inrg_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_inrg_ending: there is at least one word with '/' or '[' at the end")


def test_nominal_ending():
    try:
        assert all({F.g_nme.v(w) for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr', 'adjv'}})
        logging.info("Testing nominal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing nominal_ending: there is at least one noun, proper noun or adjective without nominal ending")

def test_expected_nominal_ending():
    try:
        assert all({F.g_nme.v(w)[0] == '/' for w in F.otype.s('word') if F.sp.v(w) in {'subs','nmpr', 'adjv'}
                     and F.g_nme.v(w) and F.g_nme.v(w) !='absent'})
        logging.info("Testing expexted_nominal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_nominal_ending: there is at least one word without '/' in the nominal ending")
        
def test_unexpected_nominal_ending():
    try:
        assert all({not F.g_nme.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'subs','nmpr', 'adjv','verb'}  and F.g_nme.v(w) != 'absent'})
        logging.info("Testing unexpexted_nominal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpected_nominal_ending: there is at least one unexpected word with a nominal ending")

def test_verbal_ending():
    try:
        assert all({F.g_vbe.v(w) for w in F.otype.s('word') if F.sp.v(w) in {'verb'}})
        logging.info("Testing verbal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing verbal_ending: there is at least one verb without verbal ending")
        
def test_expected_verbal_ending():
    try:
        assert all({F.g_vbe.v(w)[0] == '[' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                    and F.g_vbe.v(w) and F.g_vbe.v(w) !='absent'})
        logging.info("Testing expexted_verbal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_verbal_ending: there is at least one verb without verbal ending")
        
def test_unexpected_verbal_ending():
    try:
        assert all({not F.g_vbe.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb','absent'} and F.g_vbe.v(w) != 'absent'})
        logging.info("Testing unexpexted_verbal_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpexted_verbal_ending: there is at least one non-verb with a verbal ending")
                    
def test_expected_preformative_beginning():
    try:
        assert all({F.g_pfm.v(w)[0] == '!' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                    and F.g_pfm.v(w) and F.g_pfm.v(w) !='absent'})
        logging.info("Testing expexted_preformative_beginning: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_preformative_beginning: there is at least one preformative without initial !")
        
def test_expected_preformative_ending():
    try:
        assert all({F.g_pfm.v(w)[-1] == '!' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                    and F.g_pfm.v(w) and F.g_pfm.v(w) !='absent'})
        logging.info("Testing expexted_preformative_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_preformative_ending: there is at least one preformative without final !")
        
def test_unexpected_preformative():
    try:
        assert all({not F.g_pfm.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb', 'absent'}})
        logging.info("Testing unexpexted_verbal_preformative: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpexted_verbal_preformative: there is at least one non-verb with a verbal preformative")

def test_expected_verbal_stem_beginning():
    try:
        assert all({F.g_vbs.v(w)[0] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                    and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})
        logging.info("Testing expexted_verbal_stem_beginning: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_verbal_stem_beginning: there is at least one verbal stem without initial ]")
        
def test_expected_verbal_stem_ending():
    try:
        assert all({F.g_vbs.v(w)[-1] == ']' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}
                    and F.g_vbs.v(w) and F.g_vbs.v(w) !='absent'})
        logging.info("Testing expexted_verbal_stem_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing expexted_verbal_stem_ending: there is at least one preformative without final ]")
        
def test_unexpected_verbal_stem():
    try:
        assert all({not F.g_vbs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'verb','absent'}})
        logging.info("Testing unexpexted_verbal_stem: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpexted_verbal_stem: there is at least one non-verb with a verbal stem")

def test_expected_prs_beginning():
    try:
        assert all({F.g_prs.v(w)[0] == '+' for w in F.otype.s('word') if F.g_prs.v(w) and F.g_prs.v(w) !='absent'})
        logging.info("Testing expected_prs_beginning: SUCCES")
    except AssertionError as err:
        logging.error("Testing expected_prs_beginning: there is at least one pronominal suffix without initial +")
        
def test_unexpected_prs():
    try:
        assert all({not F.g_prs.v(w) for w in F.otype.s('word') if F.sp.v(w) not in {'subs','verb','prep','inrg','intj','adjv','absent'}})
        logging.info("Testing unexpected_prs: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpected_prs: there is at least one unexpected word with a pronominal suffix")

def test_unexpected_verbal_tense():
    try:
        assert all({F.vt.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) not in {'verb'}})
        logging.info("Testing unexpected_verbal_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpected_verbal_tense: there is at least one non-verb with verbal tense")
        
def test_expected_verbal_tense():
    try:
        assert all({F.vt.v(w) != 'NA' for w in F.otype.s('word') if F.sp.v(w) in {'verb'}})
        logging.info("Testing expected_verbal_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing expected_verbal_tense: there is at least one verb without verbal tense")
        
def test_perf_tense():
    try:
        assert all({F.vt.v(w) == 'perf' for w in F.sp.s('verb') if not F.g_pfm.v(w) and not F.g_nme.v(w)
                    and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing perf_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing perf_tense: there is at least one verb without expected perfect tense")
        
def test_perf_tense_morphemes():
    try:
        assert all({not F.g_pfm.v(w) and not F.g_nme.v(w) for w in F.sp.s('verb') if F.vt.v(w) == 'perf' 
     and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing perf_tense_morphemes: SUCCES")
    except AssertionError as err:
        logging.error("Testing perf_tense_morphemes: there is at least one perfect verb without expected morphemes")
        
def test_impf_tense():
    try:
        assert all({F.vt.v(w) in {'impf','wayq'} for w in F.sp.s('verb') if F.g_pfm.v(w)
                    and F.g_pfm.v(w) not in {'!!','!H!'} and not F.g_nme.v(w) and F.sp.v(w) != 'absent'
                    and F.vt.v(w) != 'absent'})
        logging.info("Testing impf_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing impf_tense: there is at least one verb without expected imperfect/wayq tense")
        
def test_impf_tense_morphemes():
    try:
        assert all({F.g_pfm.v(w) and not F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w) for w in F.sp.s('verb')
                         if F.vt.v(w) in {'impf','wayq'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing impf_tense_morphemes: SUCCES")
    except AssertionError as err:
        logging.error("Testing impf_tense_morphemes: there is at least one impf/wayq verb without expected morphemes")
        
def test_impv_tense():
    try:
        assert all({F.vt.v(w) == 'impv' for w in F.sp.s('verb') if F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w)
                    and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing impv_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing impv_tense: there is at least one verb without expected imperative tense")
        
def test_impv_tense_morphemes():
    try:
        assert all({F.g_pfm.v(w) in {'!!','!H!'} and not F.g_nme.v(w) for w in F.sp.s('verb')
                     if F.vt.v(w) == 'impv' and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing impv_tense_morphemes: SUCCES")
    except AssertionError as err:
        logging.error("Testing impv_tense_morphemes: there is at least one imperative verb without expected morphemes")
        
def test_infinitive_tense():
    try:
        assert all({F.vt.v(w) in {'infc','infa'} for w in F.sp.s('verb') if F.g_pfm.v(w) in {'!!','!H!'}
                    and F.g_nme.v(w) and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing infinitive_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing infinitive_tense: there is at least one verb without expected infinitive tense")
        
def test_infinitive_tense_morphemes():
    try:
        assert all({F.g_pfm.v(w) in {'!!','!H!','!M!'} and F.g_nme.v(w) for w in F.sp.s('verb')
                     if F.vt.v(w) in {'infc','infa'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing infinitive_tense_morphemes: SUCCES")
    except AssertionError as err:
        logging.error("Testing infinitive_tense_morphemes: there is at least one infinitive verb without expected morphemes")
        
def test_participle_tense():
    try:
        assert all({F.vt.v(w) in {'infc','ptca','ptcp'} for w in F.sp.s('verb') if F.g_pfm.v(w) in {'','!M!'}
                    and F.g_nme.v(w) and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing participle_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing participle_tense: there is at least one verb without expected particple tense")

def test_participle_tense_morphemes():
    try:
        assert all({F.g_pfm.v(w) in {'','!M!'} and F.g_nme.v(w) for w in F.sp.s('verb')
                 if F.vt.v(w) in {'ptca','ptcp'} and F.sp.v(w) != 'absent' and F.vt.v(w) != 'absent'})
        logging.info("Testing participle_tense: SUCCES")
    except AssertionError as err:
        logging.error("Testing participle_tense: there is at least one participle without expected morphemes")

def test_expected_person():
    try:
        assert all({F.ps.v(w) in {'p1','p2','p3','unknown'} for w in F.otype.s('word') if F.sp.v(w) in {'verb','prps'}
                  and F.ps.v(w) != 'absent'})
        logging.info("Testing expected_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing expected_person: there is at least one word with wrong grammatical person")
        
def test_unexpected_person():
    try:
        assert all({F.ps.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) not in {'verb','prps'}})
        logging.info("Testing unexpected_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpected_person: there is at least one word with unexpected grammatical person")
        
def test_first_person():
    try:
        assert all({F.g_pfm.v(w) in {'','!>!','!N!'} and F.g_vbe.v(w) in {'[', '[H', '[NW', '[TJ'} for w in F.sp.s('verb')
                    if F.ps.v(w) == 'p1'})
        logging.info("Testing first_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing first_person: there is at least one first person verb with wrong morphemes")
        
def test_second_person():
    try:
        assert all({F.g_pfm.v(w) in {'','!!','!H!','!T!'} and F.g_vbe.v(w) in {'[','[H','[J','[JN','[N','[T','[TH','[TJ',
                '[TM','[TN','[W','[WN'} for w in F.sp.s('verb') if F.ps.v(w) == 'p2'})
        logging.info("Testing second_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing second_person: there is at least one second person verb with wrong morphemes")
        
def test_third_person():
    try:
        assert all({F.g_pfm.v(w) in {'','!J!','!T!'} and F.g_vbe.v(w) in {'[','[H','[HN','[NH','[T','[TH','[W','[WN'} 
                     for w in F.sp.s('verb') if F.ps.v(w) == 'p3'})
        logging.info("Testing third_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing third_person: there is at least one third person verb with wrong morphemes")

def test_unknown_person():
    try:
        assert all({F.g_pfm.v(w) in {'','!!','!H!','!M!'} and F.g_vbe.v(w) in {'['} and F.g_nme.v(w) 
                    in {'/','/H','/J','/JM','/T','/TJ','/WT'} for w in F.otype.s('word') if F.ps.v(w) == 'unknown'})
        logging.info("Testing unknown_person: SUCCES")
    except AssertionError as err:
        logging.error("Testing unknown_person: there is at least one unknown word person with wrong morphemes")
        
def test_first_person_sfx():
    try:
        assert all({F.g_prs.v(w) in {'+','+J','+NJ','+NW','+W'} for w in F.otype.s('word') if F.prs_ps.v(w) == 'p1'})
        logging.info("Testing first_person_sfx: SUCCES")
    except AssertionError as err:
        logging.error("Testing first_person_sfx: there is at least one first person sfx with wrong morphemes")
        
def test_second_person_sfx():
    try:
        assert all({F.g_prs.v(w) in {'+K','+KH','+KM','+KN'} for w in F.otype.s('word') if F.prs_ps.v(w) == 'p2'})
        logging.info("Testing second_person_sfx: SUCCES")
    except AssertionError as err:
        logging.error("Testing second_person_sfx: there is at least one second person sfx with wrong morphemes")
        
def test_third_person_sfx():
    try:
        assert all({F.g_prs.v(w) in {'+H','+HM','+HN','+HW','+M','+MW','+NH','+W'} for w in F.otype.s('word') 
                    if F.prs_ps.v(w) == 'p3'})
        logging.info("Testing third_person_sfx: SUCCES")
    except AssertionError as err:
        logging.error("Testing third_person_sfx: there is at least one third person sfx with wrong morphemes")
        
def test_expected_number():
    try:
        assert all({F.nu.v(w) in {'sg','du','pl','unknown'} for w in F.otype.s('word') if F.sp.v(w) 
                    in {'subs','nmpr','adjv','verb','prps','prde','prin'} and F.nu.v(w) != 'absent'})
        logging.info("Testing expected_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing expected_number: there is at least one word with wrong grammatical number")
        
def test_unexpected_number():
    try:
        assert all({F.nu.v(w) == 'NA' for w in F.otype.s('word') if F.sp.v(w) 
                    not in {'subs','nmpr','adjv','verb','prps','prde','prin'} and F.nu.v(w) != 'absent'})
        logging.info("Testing unexpected_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing unexpected_number: there is at least one word with unexpected grammatical number")
        
def test_singular_number():
    try:
        assert all({F.g_pfm.v(w) in {'','!!','!>!','!H!','!J!','!M!','!T!'} and F.g_vbe.v(w) 
                    in {'','[','[H','[J','[JN','[T','[TH','[TJ'} and F.g_nme.v(w) in {'','/','/H','/J','/T'} 
                    for w in F.otype.s('word') if F.nu.v(w) == 'sg'})
        logging.info("Testing singular_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing singular_number: there is at least one singular word with wrong morphemes")
        
def test_dual_number():
    try:
        assert all({not F.g_pfm.v(w) and not F.g_vbe.v(w) and F.g_nme.v(w) in {'/J','/JM','/TJ','/TJM'} 
     for w in F.otype.s('word') if F.nu.v(w) == 'du'})
        logging.info("Testing dual_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing dual_number: there is at least one dual word with wrong morphemes")
        
def test_plural_number():
    try:
        assert all({F.g_pfm.v(w) in {'','!!','!H!','!J!','!M!','!N!','!T!'} and F.g_vbe.v(w) 
                    in {'','[','[H','[HN','[N','[NH','[NW','[TM','[TN','[W','[WN'}
                     and F.g_nme.v(w) in {'','/','/J','/JM','/M','/T','/TJ','/WT','/WTJ'}
                     for w in F.otype.s('word') if F.nu.v(w) == 'pl'})
        logging.info("Testing plural_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing plural_number: there is at least one plural word with wrong morphemes")

def test_unknown_number():
    try:
        assert all({F.g_pfm.v(w) in {'','!!','!H!'} and F.g_vbe.v(w) in {'','['} and F.g_nme.v(w) in {'','/','/H','/T','/WT'}
                     for w in F.otype.s('word') if F.nu.v(w) == 'unknown'})
        logging.info("Testing unknown_number: SUCCES")
    except AssertionError as err:
        logging.error("Testing unknown_number: there is at least one unknown word number with wrong morphemes")

if __name__ == "__main__":
    test_lexemes_nouns_ending()
    test_lexemes_adjv_ending()
    test_lexemes_verb_ending()
    test_lexemes_advb_ending()
    test_lexemes_conj_ending()
    test_lexemes_art_ending()
    test_lexemes_prep_ending()
    test_lexemes_pron_ending()
    test_lexemes_intj_ending()
    test_lexemes_nega_ending()
    test_lexemes_inrg_ending()
    test_nominal_ending()
    test_expected_nominal_ending()
    test_unexpected_nominal_ending()
    test_verbal_ending()
    test_expected_verbal_ending()
    test_unexpected_verbal_ending()
    test_expected_preformative_beginning()
    test_expected_preformative_ending()
    test_unexpected_preformative()
    test_expected_verbal_stem_beginning()
    test_expected_verbal_stem_ending()
    test_unexpected_verbal_stem()
    test_expected_prs_beginning()
    test_unexpected_prs()
    test_unexpected_verbal_tense()
    test_expected_verbal_tense()
    test_perf_tense()
    test_perf_tense_morphemes()
    test_impf_tense()
    test_impf_tense_morphemes()
    test_impv_tense()
    test_impv_tense_morphemes()
    test_infinitive_tense()
    test_infinitive_tense_morphemes()
    test_participle_tense()
    test_participle_tense_morphemes()
    test_expected_person()
    test_unexpected_person()
    test_first_person()
    test_second_person()
    test_third_person()
    test_unknown_person()
    test_first_person_sfx()
    test_second_person_sfx()
    test_third_person_sfx()
    test_expected_number()
    test_unexpected_number()
    test_singular_number()
    test_dual_number()
    test_plural_number()
    test_unknown_number()