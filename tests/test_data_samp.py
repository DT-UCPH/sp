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