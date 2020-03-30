
class SearchResult() : 

    def __init__(self, search_input, results_list = []): 
        self.search_input = search_input
        self.results_by_pertinence = results_list

    def add_search_result(search_result) : 
        self.results_by_pertinence.append(search_result)

    def get_ordered_search_result(self) : 
        return sorted(
            self.results_by_pertinence, 
            key = lambda x : x.pertinence)

    def __repr__(self) : 
        _str = 'SearchResult for input ' + self.search_input
        _str += ' ('+str(len(self.results_by_pertinence))+'), ' 
        for result in self.results_by_pertinence : 
            _str += repr(result)
        return _str


class SingleSearchResult() : 
    def __init__(self, pertinence = 3): 
        self.pertinence = pertinence
        # 0 : most important
        # 1 : high
        # 2 : medium 
        # 3 : low

class WordSearchResult(SingleSearchResult) : 
    def __init__(self, id, word, prononciation, meaning, pertinence = 3, *kanjis):
        super().__init__(pertinence)
        self.id   = id
        self.word = word 
        self.prononciation = prononciation 
        self.meaning = meaning 
        self.kanjis  = kanjis

    def __repr__(self) : 
        _str =  'WordSearchResult of pertinence = ' + str(self.pertinence)
        _str += ', word : ' + self.word
        _str += ', id : ' + self.id
        _str += ', prononciation : ' + self.prononciation
        _str += ', meaning : ' + str(self.meaning)
        _str += ', kanjis are : '
        for kanji in self.kanjis : _str += kanji+', '
        return _str[:-1] + '; '

class WordListSearchResult(SingleSearchResult) : 
    
    def __init__(self, *words_data_list, pertinence = 3):
        """
        word_data_list_format : 
            (<word>, <prononciation>, <meaning>)
        """
        super().__init__(pertinence)
        self.word_list = self._creating_word(*words_data_list)

    def __repr__(self) : 
        _str =  'WordListSearchResult of pertinence = ' + str(self.pertinence) + ', '
        _str += str(len(self.word_list)) + ' words listed :'
        for word in self.word_list : 
            _str += repr(word)
        return _str+'; '


    def _creating_word(self, *words_data_list) :
        r = []
        for (id, word, prononciation, meaning) in words_data_list : 
            word_item = WordItem(id, word, prononciation, meaning)
            r.append(word_item)
        return r

# useless is it not ?
class WordItem() : 
    def __init__(self, id, word, prononciation, meaning) : 
        self.id  = id
        self.word = word 
        self.prononciation = prononciation
        self.meaning = meaning

    def __repr__(self) : 
        _str = 'word : ' + self.word 
        _str += ', id : ' + self.id
        _str += ', prononciation : ' + self.prononciation
        _str += ', meaning : ' + self.meaning + '; '
        return _str

class SelectorResult(SingleSearchResult) : 
    
    valid_selector_type = {
    'categorie', 
    'tag', 
    'core_prononciation', 
    'kanji'
    }

    def __init__(self, selector_type, selector_value, *word_examples, pertinence = 3) :
        
        if selector_type not in self.valid_selector_type : 
            raise ValueError('valid selector types are : ' + set(self.valid_selector_type))
        super().__init__(pertinence)
        self.selector_type = selector_type
        self.selector_value = selector_value, 
        self.word_examples = word_examples

    def __repr__(self) : 
        _str = 'SelectorResult for selector type : ' + self.selector_type+', value : ' + self.selector_value + '; '
        return _str

