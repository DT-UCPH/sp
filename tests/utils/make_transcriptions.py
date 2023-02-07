"""
Running the script creates ETCBC transcriptions of the original word files.
Make sure the word files are in the folder utils/make_transcriptions/hebrew_files.
"""
import os
import docx

WORD_FILES_FOLDER = './utils/hebrew_files'

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


class Verse:
    """
    Verse class contains basic info of single verse.
    """
    def __init__(self, book, chapter, verse):
        self.book = book
        self.chapter = chapter
        self.verse = verse
        self.verse_text = ''


class SPTextTranscriber:
    """
    Makes a transcription of original word files that contain the text
    in Hebrew script.
    
    """
    def __init__(self, book_names, word_file_names, word_files_folder):
        self.book_names = book_names
        self.word_file_names = word_file_names
        self.word_files_folder = WORD_FILES_FOLDER
        self.verse_texts = {}
        
        self.chapter = 0

        for book_name, word_file_name in zip(self.book_names, self.word_file_names):
            path = os.path.join(self.word_files_folder, word_file_name)
            self.word_file_text = self.get_word_file_text(path)
            self.parse_word_file_text(book_name)
            self.chapter = 0

    @staticmethod
    def get_word_file_text(filename):
        """
        Function reads the whole text of one word file.
        Returns text of file as single string.
        """
        doc = docx.Document(filename)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    
    def parse_word_file_text(self, book_name):
        """
        Parses the Hebrew text and makes transcription.
        Text is stored in list self.verse_texts.
        This text is a string with book, chapter verse, and transliteration (tab separated).
        """
        verse = Verse(book_name, 0, 0)
        for word in self.word_file_text.split():
            # If verse num is 1, a new chapter starts, there is a strange exception after Exodus 29:46, there a chapter starts at verse 11,
            # because Exo 30:1-10 has been moved to 26:35.
            if word.isnumeric() and (word == '1' or (book_name == 'Exodus' and verse.chapter == 29 and verse.verse == 46)):
                if verse.chapter != 0:
                    self.verse_texts[(verse.book, verse.chapter, verse.verse)] = verse.verse_text.strip()
                self.chapter += 1
                verse = Verse(book_name, self.chapter, int(word))

            # Check for every sign whether it is a digit if there are verse numbers with letters in it in the TF dataset. 
            #elif any(sign.isnumeric() for sign in word):
            elif word.isnumeric():
                if self.chapter != 0:
                    self.verse_texts[(verse.book, verse.chapter, verse.verse)] = verse.verse_text.strip()
                verse = Verse(book_name, self.chapter, int(word))
            else:
                word_transcription = ''.join([alphabet_dict.get(char, '') for char in word])
                if word_transcription:
                    verse.verse_text += (word_transcription + ' ')
        self.verse_texts[(verse.book, verse.chapter, verse.verse)] = verse.verse_text.strip()

