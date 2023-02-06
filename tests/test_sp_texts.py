"""
Tests whether the text in TF is the same as a transcription of the original word files.
Note that at this moment only Genesis is tested.
"""
import logging
import os
import pytest

TRANSCRIPTIONS_FOLDER = './transcriptions'


from tf.app import use
A = use('dt-ucph/sp:hot', hoist=globals())

logging.basicConfig(
    filename='./logs/test_sp_texts.log',
    level = logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def get_verse_transcriptions():
    """Make dict with transcription of each verse"""
    file_names = ['SP_Genesis.trans']
    text_dict = {}
    for file_name in file_names:
        with open(os.path.join(TRANSCRIPTIONS_FOLDER, file_name), 'r') as f:
            for line in f:
                bo, ch, ve, text = line.split('\t')
                text_dict[(bo, int(ch), ve)] = text.strip()
    return text_dict

@pytest.fixture(scope='module')
def verse_transcriptions(module):
    yield get_verse_transcriptions()
    
def test_sp_bib_texts(verse_transcriptions):
    try:
        for ve in F.otype.s('verse'):
            verse_text = ''.join([F.g_cons.v(w) + F.trailer.v(w) for w in L.d(ve, 'word')]).strip().replace('F', 'C').replace('_', ' ')
            bo, ch, ve = T.sectionFromNode(ve)
            
            assert verse_transcriptions[(bo, ch, ve)] == verse_text
        logging.info("Testing test_sp_texts: SUCCES")
    except AssertionError as err:
        logging.error(f"Testing texts of SP books, transcription not equal to TF data in {bo} {ch} {ve}")
        logging.error(f"Word transcription: {verse_transcriptions[(bo, ch, ve)]}")
        logging.error(f"TF transcription:   {verse_text}")
        
if __name__ == "__main__":

    verse_transcriptions = get_verse_transcriptions()
    test_sp_bib_texts(verse_transcriptions)
