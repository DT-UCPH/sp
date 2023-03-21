"""
This test will not run on github, because it needs data that are not in the github repo.
Tests whether the text in TF is the same as a transcription of the original word files.
"""
import logging
import os
import pytest

from utils import make_transcriptions

from tf.app import use
A = use('dt-ucph/sp', checkout='clone', version='2.4')
F, L, T = A.api.F, A.api.L, A.api.T

WORD_FILES_FOLDER = './utils/hebrew_files'

BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
WORD_FILES = ['SP-1-Genesis.docx', 'SP-2-Exodus.docx', 'SP-3-Lev.docx', 'SP-4-Num.docx', 'SP-5-Deut.docx']


logging.basicConfig(
    filename='./logs/test_sp_texts.log',
    level = logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


def get_verse_transcriptions():
    """Make dict with transcription of each verse"""
    transcriber = make_transcriptions.SPTextTranscriber(BOOKS, WORD_FILES, WORD_FILES_FOLDER)
    text_dict = transcriber.verse_texts
    logging.info(f'The word files contain {len(text_dict)} verses.')
    return text_dict


@pytest.fixture(scope='module')
def verse_transcriptions(module):
    yield get_verse_transcriptions()


def test_sp_bib_texts(verse_transcriptions):
    try:
        idx = 0
        book_set = set()
        for ve in F.otype.s('verse'):
            verse_text = ''.join([F.g_cons.v(w) + F.trailer.v(w) for w in L.d(ve, 'word')]).strip().replace('F', 'C').replace('_', ' ')
            bo, ch, ve = T.sectionFromNode(ve)
            if bo not in book_set:
                logging.info(f'Testing the book of {bo}')
                book_set.add(bo)
            assert verse_transcriptions[(bo, ch, ve)] == verse_text
            idx += 1
        logging.info('Testing test_sp_texts: SUCCES')
        logging.info(f'Tested {idx} verses')
    except AssertionError as err:
        logging.error(f'Testing texts of SP books, transcription not equal to TF data in {bo} {ch} {ve}')
        logging.error(f'Word transcription: {verse_transcriptions[(bo, ch, ve)]}')
        logging.error(f'TF transcription: {verse_text}')
        
if __name__ == '__main__':

    verse_transcriptions = get_verse_transcriptions()
    test_sp_bib_texts(verse_transcriptions)
