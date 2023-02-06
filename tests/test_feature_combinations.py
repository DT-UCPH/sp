import logging
import pytest

from tf.app import use
A = use('DT-UCPH/sp:hot', hoist=globals())

logging.basicConfig(
    filename='./logs/test_feature_combinations_sp.log',
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
        