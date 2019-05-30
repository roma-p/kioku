import abc
import logging
from DB.Japanese_DB_handler import Japanese_DB_handler
from www import www_config

log = logging.getLogger()

class Selector(abc.ABC) : 
    selector_id = None
    sub_url = None

    def __call__(self) : return self.selector_id

    # return : - tuple of tuple (selector_id : number of words associated)
    #          - total number selectors
    @abc.abstractmethod    
    def get_selector_list_data(): 
        return

    # return : a list of vocab associated to the given selector id. 
    # return () if no vocabulary is associated to this selector,
    # return None if selector does not exist. 
    @abc.abstractmethod    
    def get_vocab_from_selector(): 
        return


class Categorie(Selector) : 
    selector_id = 'categorie'
    sub_url = 'categories'    

    def get_selector_list_data() : 
        jpDB = Japanese_DB_handler()
        sel_list = jpDB.list_categorie_by_usage()
        sel_number = jpDB.count(jpDB.base_format.categories)
        return sel_list, sel_number

    def get_vocab_from_selector(selector_id) : 
        jpDB = Japanese_DB_handler()
        selector_id = selector_id if jpDB.check_categorie_existence(selector_id) else None
        if selector_id : 
            item_to_get = www_config.get_vocab_format()
            vocab_list = jpDB.list_word_by_categorie(selector_id, *item_to_get)
            return vocab_list


class Tag(Selector) : 
    selector_id = 'tag'
    sub_url = 'tags'    

    def get_selector_list_data() : 
        jpDB = Japanese_DB_handler()
        sel_list = jpDB.list_tag_by_usage()
        sel_number = jpDB.count(jpDB.base_format.tags)
        return sel_list, sel_number

    def get_vocab_from_selector(selector_id) : 
        jpDB = Japanese_DB_handler()
        selector_id = selector_id if jpDB.check_tag_existence(selector_id) else None
        if selector_id : 
            # item_to_get = www_config.get_vocab_format()
            f = Japanese_DB_handler().base_format
            item_to_get = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning,f.vocab.example)

            vocab_list = jpDB.list_word_by_tag(selector_id, *item_to_get)
            return vocab_list


class Kanjis(Selector) : 
    selector_id = 'kanji'
    sub_url = 'kanjis'    

    def get_selector_list_data() : 
        jpDB = Japanese_DB_handler()
        sel_list = jpDB.list_kanjis_by_usage()
        sel_number = jpDB.count(jpDB.base_format.kanjis)
        return sel_list, sel_number

    def get_vocab_from_selector(selector_id) : 
        jpDB = Japanese_DB_handler()
        selector_id = selector_id if jpDB.check_kanjis_existence(selector_id) else None
        if selector_id : 
            item_to_get = www_config.get_vocab_format()
            log.error(selector_id)
            log.error(item_to_get)
            vocab_list = jpDB.list_word_by_kanjis(selector_id, *item_to_get)
            return vocab_list


class Core_P(Selector) : 
    selector_id = 'core_prononciation'
    sub_url = 'core_prononciations'    

    def get_selector_list_data() : 
        jpDB = Japanese_DB_handler()
        sel_list = jpDB.list_core_p_by_usage()
        sel_number = jpDB.count(jpDB.base_format.core_prononciations)
        return sel_list, sel_number

    def get_vocab_from_selector(selector_id) : 
        jpDB = Japanese_DB_handler()
        selector_id = selector_id if jpDB.check_core_p_existence(selector_id) else None
        if selector_id : 
            item_to_get = www_config.get_vocab_format()
            vocab_list = jpDB.list_word_by_core_prononciation(selector_id, *item_to_get)
            return vocab_list



