import abc
import logging
from DB.Japanese_DB_handler import Japanese_DB_handler
from www import www_config

log = logging.getLogger()

class Selector(abc.ABC) : 
    selector_type = None
    sub_url = None
    parent_url = 'selectors'

    def __call__(self) : return self.selector_type

    # return : - tuple of tuple (selector_type : number of words associated)
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

    # generate the sub url to a selector type list. 
    # eg : /selectors/categories
    @classmethod
    def gen_url_to_selector_type(cls) : 
        return '/' + Selector.parent_url + '/' + cls.sub_url

    # generate the sub url to a precise selector id
    # eg : a precise categorie
    # will be like : /selectors/categories/time

    #TODO  store url in static so not generated every time. 
    @classmethod
    def gen_url_to_selector_id(cls, selector_id) :
        return '/' + Selector.parent_url + '/' + cls.sub_url + '/' + selector_id



class Categorie(Selector) : 
    selector_type = 'categorie'
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
    selector_type = 'tag'
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
    selector_type = 'kanji'
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
            vocab_list = jpDB.list_word_by_kanjis(selector_id, *item_to_get)
            return vocab_list


class Core_P(Selector) : 
    selector_type = 'core_prononciation'
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



