import logging
from japanese.Japanese_DB_Handler import Japanese_DB_handler
from japanese.SearchResult import WordSearchResult, WordListSearchResult, SelectorResult, SearchResult

_jpdb_object = None
def _jpdb() : 
    global _jpdb_object 
    if not _jpdb_object : _jpdb_object = Japanese_DB_handler()
    return _jpdb_object

# SEARCHING ***************************************************************

# input -> string without space. OHTERWISE return error for the moment
# !!! if single kanjis different behaviour : list words with kanjis.  

def search_web_app(input, *field_to_get) :
    j = _jpdb()
    _input = Japanese_DB_handler._process_search_input(input)
    if not _input : return None
    if len(_input) == 1 and japanese_helpers.is_kanjis(_input) : 
        search_result_list = j.search_kanji(_input)
    else : 
        search_result_list = j.search_normal(_input)
    if search_result_list : 
        return SearchResult(search_result_list)
    # if one kanjis : search by kanjis 
    # if egnlish or japanese : nothing to do, can't proceed through that.
    # if more thant one kanjis character, words and stuff.

def search_kanji(input) :
    j = _jpdb() 
    f = j.base_format
    field_to_get = (f.vocab.word, f.vocab._prononciation, f.vocab.meaning)
    search_result_list = []
    kanji_existence = j.check_kanjis_existence(kanji)
    if kanji_existence : 
        # if kanji exists, display it first. 
        search_result_list.append(SelectorResult('kanji', kanji, pertinence = 0))
    word_list = j.list_word_by_kanjis(input, field_to_get)
    search_result_list.append(WordListSearchResult(word_list, pertinence = 1))
    return search_result_list

def search_normal(input) : 
    j = _jpdb()
    word_output = j.search_word(input)
    categorie_output = j.search_categorie(input)
    tag_output = j.search_tag(input)
    core_p_output = j.search_core_p(input)
    # settings pertinence of every search results objects. 
    for search_result in word_output : 
        # if words match perfectly to input, higher pertinence
        if isinstance(search_result, WordSearchResult) :
            search_result.pertinence = 0
        # if list of appromixation pertience is lower that maybe a categorie matching perfectly  
        if isinstance(search_result, WordListSearchResult): 
            search_result.pertinence = 2
    selector_result_list = categorie_output + tag_output + core_p_output
    for search_result in selector_result_list :
        search_result.pertinence = 1  
    return word_output + selector_result_list

def search_word(input) :
    """
    TODO 
    """
    j = _jpdb()
    f = j.base_format
    field_to_get = (f.vocab.word, f.vocab._prononciation, f.vocab.meaning)
    _input = Japanese_DB_handler._process_search_input(input)
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
            f.vocab.prononciation, _input, *field_to_get)
    _tmp_output[f.vocab.meaning()] = j.list_vocab_by_approximative_field(
            f.vocab.meaning, _input, *field_to_get)
    kanjis_in_word = j.search_kanjis_in_words(input, f.kanjis.name)
    _perfect_match_list = []
    _approximation_data_list = []
    for key, value in _tmp_output.items() : 
        perfect_matches, approximation_list = value
        if perfect_matches : _perfect_match_list += perfect_matches
        if approximation_list : _approximation_data_list += approximation_list
    searchResultsList = []
    for _perfect_match_data in _perfect_match_list : 
        word, prononciation, meaning = _perfect_match_data
        perfect_match_list.append(WordSearchResult(word, prononciation, meaning *kanjis_in_word)
    searchResultsList.append(WordListSearchResult(_approximation_data_list)))
    return searchResultsList

def search_kanjis_in_words(input) : 
    """
    execute _process_search_input to check input. 
    if japanese : will return every kanji in the word if those exists in the database. 
    """
    j = _jpdb()
    _input = Japanese_DB_handler._process_search_input(input)
    if not _input or not japanese_helpers.is_word_japanese(_input) : return None
    kanjis_in_word = japanese_helpers.list_kanjis(word)
    kanjis_in_db = [kanji for kanji in kanjis_in_word if j.check_kanjis_existence(kanji)]
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
    _input = Japanese_DB_handler._process_search_input(input)
    if not _input : return None
    f = j.base_format
    q = Query().select(f.categories, f.categories.name)
    q.where().equal(f.categories.name, _input)
    return j.executeQuery(q)
    categorie = j.executeQuery(q)[0][0]
    return SelectorResult('categorie', categorie) if categorie else None

def search_tag(input) :
    """
    execute _process_search_input to check input. 
    search tag corresponding to that input, 
    but only look for tags beeing exactly equalt to input 
    tags can be either in english / french / japanese. 
    """
    j = _jpdb()
    _input = Japanese_DB_handler._process_search_input(input)
    if not _input : return None
    f = j.base_format
    q = Query().select(f.tags, f.tags.name)
    q.where().equal(f.tags.name, _input)
    tag = j.executeQuery(q)[0][0]
    return SelectorResult('tag', tag) if tag else None

def search_core_p(input) : 
    """
    execute _process_search_input to check input. 
    if kana, generate core_prononciation and list words with that core_p
    if just one word affected to that core_p, not relevant to return it, return None
    else return the core prononciation. 
    """
    j = _jpdb()
    _input = Japanese_DB_handler._process_search_input(input)
    if not _input or not japanese_helpers.is_word_kana(_input) : return None
    core_p = japanese_helpers.gen_core_prononciation(_input)
    if not core_p : return None
    word_list = list_word_by_core_prononciation(core_p, j.base_format.vocab.word)
    return core_p if len(word_list) > 1 else None
    if len(word_list) > 1 : return SelectorResult('core_prononciation', core_p)
    else : return None
    
def _process_search_input(input) :
    """
    checking consistency of input recevied from search field
    for now : only accept one word as input, (will delete leading and trailing spaces). 
    TODO : a cache !!!
    """
    _input = strip(input)
    if ' ' in _input : 
        log.error('at the moment, search feature only accept ONE word')
        return None
    else : 
        return _input
