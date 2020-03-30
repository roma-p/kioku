import logging
from www import www_config
from japanese.Japanese_DB_handler import Japanese_DB_handler

class Word() : 
    parent_url = 'words'

    @classmethod
    def gen_url_to_word(cls, word_id) :
        return '/' + cls.parent_url + '/' + str(word_id)

    @classmethod
    def gen_url_to_words(cls) :
        return '/' + cls.parent_url

    def get_word_data(word_id) : 
        jpDB= Japanese_DB_handler()
        return jpDB.get_word_info(word_id)        
