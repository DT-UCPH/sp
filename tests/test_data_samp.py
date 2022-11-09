import logging
import pytest

from tf.app import use
samp = use('DT-UCPH/SamP:clone', checkout='clone', version='1.3')
sampF, sampT  = samp.api.F, samp.api.T

logging.basicConfig(
    filename='./logs/test_data_sp.log',
    level = logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def test_lexemes_nouns_ending():
    try:
        assert all([sampF.lex.v(w)[-1] == '/' for w in sampF.otype.s('word') if sampF.sp.v(w) in {'subs','nmpr'} 
                    and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_nouns_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_nouns_ending: there is at least one word without '/' at the end")
        
def test_lexemes_adjv_ending():
    try:
        assert all([sampF.lex.v(w)[-1] == '/' for w in sampF.otype.s('word') if sampF.sp.v(w) == 'adjv'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_adjv_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_adjv_ending: there is at least one word without '/' at the end")
        
def test_lexemes_verb_ending():
    try:
        assert all([sampF.lex.v(w)[-1] == '[' for w in sampF.otype.s('word') if sampF.sp.v(w) == 'verb'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_verbs_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_verbs_ending: there is at least one word without '[' at the end")
        
def test_lexemes_advb_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'advb'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_advb_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_advb_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_conj_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'conj'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_conj_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_conj_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_art_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'art'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_art_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_art_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_prep_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'prep'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_prep_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_prep_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_pron_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) in {'prps','prde','prin'}
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_pron_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_pron_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_intj_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'intj'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_intj_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_intj_ending: there is at least one word with '/' or '[' at the end")

def test_lexemes_nega_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'nega'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_nega_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_nega_ending: there is at least one word with '/' or '[' at the end")
        
def test_lexemes_inrg_ending():
    try:
        assert all([sampF.lex.v(w)[-1] not in {'/','['} for w in sampF.otype.s('word') if sampF.sp.v(w) == 'inrg'
                   and sampF.lex.v(w) !='absent'])
        logging.info("Testing lexemes_inrg_ending: SUCCES")
    except AssertionError as err:
        logging.error("Testing lexemes_inrg_ending: there is at least one word with '/' or '[' at the end")
        
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