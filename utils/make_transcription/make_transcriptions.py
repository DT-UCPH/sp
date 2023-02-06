"""
Running the script creates ETCBC transcriptions of the original word files.
Make sure the word files are in the folder utils/make_transcriptions/hebrew_files.
"""
import os

import docx

WORD_FILES_FOLDER = './hebrew_files'
TRANSCRIPTIONS_FOLDER = '../../tests/transcriptions'

alphabet_dict = {'א': '>',
                              'ב': 'B',
                              'ג': 'G',
                              'ד': 'D',
                              'ה': 'H',
                              'ו': 'W',
                              'ז': 'Z',
                              'ח': 'X',
                              'ט': 'V',
                              'י': 'J',
                              'כ': 'K',
                              'ך': 'K',
                              'ל': 'L',
                              'מ': 'M',
                              'ם': 'M',
                              'נ': 'N',
                              'ן': 'N',
                              'ס': 'S',
                              'ע': '<',
                              'פ': 'P',
                              'ף': 'P',
                              'צ': 'Y',
                              'ץ': 'Y',
                              'ק': 'Q',
                              'ר': 'R',
                              'ש': 'C',
                              'ת': 'T'}
                              
book_names = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']
word_file_names = ['SP-1-Genesis.docx', 'SP-2-Exodus.docx', 'SP-3-Lev.docx', 'SP-4-Num.docx', 'SP-5-Deut.docx']


class Verse:
    """
    Verse class contains basic info of single verse.
    """
    def __init__(self, book, chapter, verse):
        self.book = book
        self.chapter = str(chapter)
        self.verse = verse
        self.verse_text = '\t'.join([self.book, self.chapter, self.verse]) + '\t'


class SPTextTranscriber:
    """
    Makes a transcription of original word files that contain the text
    in Hebrew script.
    
    """
    def __init__(self, book_name, word_file_name):
        self.book_name = book_name
        self.word_file_name = word_file_name
        self.word_files_folder = WORD_FILES_FOLDER
        self.verse_texts = []
        
        self.chapter = 0
        self.path = os.path.join(self.word_files_folder, self.word_file_name)
        self.word_file_text = self.get_word_file_text(self.path)
        
    def get_word_file_text(self, filename):
        """
        Function reads the whole text of one word file.
        Returns text of file as single string.
        """
        doc = docx.Document(filename)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    
    def parse_word_file_text(self):
        """
        Parses the Hebrew text and makes transcription.
        Text is stored in list self.verse_texts.
        This text is a string with book, chapter verse, and transliteration (tab separated).
        
        """
        verse = Verse(self.book_name, '0', '0')
        for word in self.word_file_text.split():
            # If verse num is 1, a new chapter starts, there is a strange exception after Exodus 29:46, there a chapter starts at verse 11,
            # because Exo 30:1-10 has been moved to 26:35.
            if word.isnumeric() and (word == '1' or (self.book_name == 'Exodus' and verse.chapter == '29' and verse.verse == '46')):
                if verse.chapter != '0':
                    self.verse_texts.append(verse.verse_text.strip())
                self.chapter += 1
                verse = Verse(self.book_name, self.chapter, word)

            # Check for every sign whether it is a digit if there are verse numbers with letters in it in the TF dataset. 
            #elif any(sign.isnumeric() for sign in word):
            elif word.isnumeric():
                if verse.chapter != '0':
                    
                    self.verse_texts.append(verse.verse_text.strip())
                verse = Verse(self.book_name, self.chapter, word)
            else:
                word_transcription = ''.join([alphabet_dict.get(char, '') for char in word])
                if word_transcription:
                    verse.verse_text += (word_transcription + ' ')
        self.verse_texts.append(verse.verse_text.strip())
        
        
class TranscriptionSaver:
    def __init__(self, book, verse_texts):
        self.transcription_folder = TRANSCRIPTIONS_FOLDER
        self.book = book
        self.verse_texts = verse_texts
        self.file_name = f'SP_{book}.trans'
        self.path = os.path.join(self.transcription_folder, self.file_name)
        
    def save_text(self):
        with open(self.path, 'w', encoding='utf8') as f:
            for verse_text in self.verse_texts:
                f.write(verse_text + '\n')
				
				
if __name__ == '__main__':
    for book, file_name in zip(book_names, word_file_names):
        try:
            transcriber = SPTextTranscriber(book, file_name)
        except FileNotFoundError as e:
            print(e)
        transcriber.parse_word_file_text()
        try:
            saver = TranscriptionSaver(book, transcriber.verse_texts)
            saver.save_text()
        except FileNotFoundError as e:
            print(e)
            print('Make sure there is a subfolder "transcriptions" in the folder "tests"')