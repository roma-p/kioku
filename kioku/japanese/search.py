import logging
from DB.Query import Query
from japanese import japanese_helpers
from japanese.Japanese_DB_handler import Japanese_DB_handler
from japanese.SearchResult import WordSearchResult, WordListSearchResult, SelectorResult, SearchResult

log = logging.getLogger()
examples_limit = 5

_jpdb_object = None
def _jpdb() : 
    global _jpdb_object 
    if not _jpdb_object : _jpdb_object = Japanese_DB_handler()
    return _jpdb_object

# SEARCHING ***************************************************************

# input -> string without space. OHTERWISE return error for the moment
# !!! if single kanjis different behaviour : list words with kanjis.  

def search_web_app(input) :
    j = _jpdb()
    _input = _process_search_input(input)
    if not _input : return None
    if len(_input) == 1 and japanese_helpers.is_kanjis(_input) : 
        search_result_list = search_kanji(_input)
    else : 
        search_result_list = search_normal(_input)
    if search_result_list : 
        return SearchResult(_input, search_result_list)
    # if one kanjis : search by kanjis 
    # if egnlish or japanese : nothing to do, can't proceed through that.
    # if more thant one kanjis character, words and stuff.

def search_kanji(input) :
    j = _jpdb() 
    f = j.base_format
    vocab_field_to_get = (f.vocab.id, f.vocab.word, 
                          f.vocab.prononciation, f.vocab.meaning)
    search_result_list = []

    q = Query().select(f.vocab, *vocab_field_to_get)
    q.where().equal(f.vocab.word, input)
    data = j.executeQuery(q)
    perfect_matches = list(data) if data else None
    
    if perfect_matches : 
        for match in perfect_matches : 
            id, word, prononciation, meaning  = match
            # if there is a word which consists of a single kanji, display it first.
            search_result_list.append(WordSearchResult(id, word, prononciation, 
                                                        meaning = 0))

    kanji_existence = j.check_kanjis_existence(input)
    if kanji_existence : 
        # if kanji exists, display it right after pottential word in one kanji.

        q = Query().select(f.kanjis, f.kanjis.id)
        q.where().equal(f.kanjis.name, input)
        d = j.executeQuery(q)
        kanji_id = d[0][0]

        examples = _create_examples(j.list_word_by_kanjis, input) 
        search_result_list.append(SelectorResult('kanji',
                                                kanji_id,
                                                input, 
                                                pertinence = 1, 
                                                *examples))
    word_list = j.list_word_by_kanjis(input, *vocab_field_to_get)
    # and belowm list of words using this kanjis
    search_result_list.append(WordListSearchResult(*word_list, pertinence = 2))
    return search_result_list

def search_normal(input) : 
    j = _jpdb()
    word_output = search_word(input)
    categorie_output = search_categorie(input)
    tag_output = search_tag(input)
    core_p_output = search_core_p(input)
    # settings pertinence of every search results objects. 
    for search_result in word_output : 
        # if words match perfectly to input, higher pertinence
        if isinstance(search_result, WordSearchResult) :
            search_result.pertinence = 0
        # if list of appromixation pertience is lower that maybe a categorie matching perfectly  
        if isinstance(search_result, WordListSearchResult): 
            search_result.pertinence = 2
    selector_result_list = []
    if categorie_output : selector_result_list.append(categorie_output)
    if tag_output : selector_result_list.append(tag_output) 
    if core_p_output : selector_result_list.append(core_p_output) 
    for search_result in selector_result_list :
        search_result.pertinence = 1  
    return word_output + selector_result_list

def search_word(input) :
    """
    TODO 
    """
    j = _jpdb()
    f = j.base_format
    field_to_get = (f.vocab.id, f.vocab.word,
                    f.vocab.prononciation, f.vocab.meaning)
    _input = _process_search_input(input)
    if not _input : return None
    _tmp_output = {
    f.vocab.word() : (), 
    f.vocab.prononciation() : (), 
    f.vocab.meaning() : (),
    }
    is_japanese = japanese_helpers.is_word_japanese(_input)
    is_kana = False if not is_japanese else japanese_helpers.is_word_kana(_input)
    if is_japanese : 
        _tmp_output[f.vocab.word()] = j.list_vocab_by_approximative_field(
            f.vocab.word, _input, *field_to_get)
    if is_kana : 
        _tmp_output[f.vocab.prononciation()] = j.list_vocab_by_approximative_field(
                                                    f.vocab.prononciation, 
                                                    _input, *field_to_get)
    _tmp_output[f.vocab.meaning()] = j.list_vocab_by_approximative_field(
                                                    f.vocab.meaning, 
                                                    _input, *field_to_get)
    kanjis_in_word = search_kanjis_in_words(input)
    _perfect_match_list = []
    _approximation_data_list = []
    for key, value in _tmp_output.items() : 
        if  value : 
            perfect_matches, approximation_list=value
            if perfect_matches : _perfect_match_list+=perfect_matches
            if approximation_list : _approximation_data_list+=approximation_list
    searchResultsList = []
    for _perfect_match_data in _perfect_match_list : 
        id, word, prononciation, meaning = _perfect_match_data
        searchResultsList.append(
                            WordSearchResult(id, word, prononciation, 
                                            meaning, *kanjis_in_word))
    searchResultsList.append(WordListSearchResult(*_approximation_data_list))
    return searchResultsList

def search_kanjis_in_words(input) : 
    """
    execute _process_search_input to check input. 
    if japanese : will return every kanji in the word if those exists in the database. 
    """
    j = _jpdb()
    _input = _process_search_input(input)
    if not _input or not japanese_helpers.is_word_japanese(_input) : return None
    kanjis_in_word = japanese_helpers.list_kanjis(input)
    kanjis_in_db = [kanji for kanji in kanjis_in_word 
                    if j.check_kanjis_existence(kanji)]
    diff = set(kanjis_in_word) - set(kanjis_in_db)
    if diff : 
        log.error('following kanjis not found in DB : ')
        for kanji in diff : 
            log.error(kanji)
    return kanjis_in_db

def search_categorie(input) : 
    """
    execute _process_search_input to check input. 
    search categorie corresponding to that input, 
    but only look for categories beeing exactly equalt to input 
    categories can be either in english / french / japanese. 
    """
    j = _jpdb()
    _input = _process_search_input(input)
    if not _input : return None
    f = j.base_format
    q = Query().select(f.categories, f.categories.id, f.categories.name)
    q.where().equal(f.categories.name, _input)
    categorie_data = j.executeQuery(q)

    if categorie_data: 
        cat_id, cat_name = categorie_data[0]
        examples = _create_examples(j.list_word_by_categorie, cat_name)
        return SelectorResult('categorie', cat_id, cat_name, *examples)

def search_tag(input) :
    """
    execute _process_search_input to check input. 
    search tag corresponding to that input, 
    but only look for tags beeing exactly equalt to input 
    tags can be either in english / french / japanese. 
    """
    j = _jpdb()
    _input = _process_search_input(input)
    if not _input : return None
    f = j.base_format
    q = Query().select(f.tags, f.tags.id, f.tags.name)
    q.where().equal(f.tags.name, _input)
    tag_data = j.executeQuery(q)

    if tag_data:
        tag_id, tag_name = tag_data[0]
        examples = _create_examples(j.list_word_by_tag, tag_name)
        return SelectorResult('tag', tag_id, tag_name, *examples)        


def search_core_p(input) : 
    """
    execute _process_search_input to check input. 
    if kana, generate core_prononciation and list words with that core_p
    if just one word affected to that core_p, not relevant to return it, return None
    else return the core prononciation. 
    """
    j = _jpdb()
    _input = _process_search_input(input)
    if not _input or not japanese_helpers.is_word_kana(_input) : return None
    core_p = japanese_helpers.gen_core_prononciation(_input)
    if not core_p : return None
    word_list = j.list_word_by_core_prononciation(core_p, 
                                                j.base_format.vocab.word)
    if len(word_list) > 1 : 

        q = Query().select(f.core_prononciations, f.tacore_prononciationsgs.id)
        q.where().equal(f.core_prononciations.name, core_p)
        core_p_id = j.executeQuery(q)[0][0]

        examples = _create_examples(j.list_word_by_core_prononciation, core_p) 
        return SelectorResult('core_prononciation',core_p_id, core_p, *examples)
    return None

def _create_examples(jpdb_method, input):
    global examples_limit
    j = _jpdb()
    f = j.base_format
    field_to_get = (f.vocab.id, f.vocab.word)
    return jpdb_method(input, *field_to_get, limit = examples_limit)

def _process_search_input(input) :
    """
    checking consistency of input recevied from search field
    for now : only accept one word as input, (will delete leading and trailing spaces). 
    TODO : a cache !!!
    """
    _input = input.strip()
    if ' ' in _input : 
        log.error('at the moment, search feature only accept ONE word')
        return None
    else : 
        return _input
