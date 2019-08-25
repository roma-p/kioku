import logging
from bottle import Bottle, run, view, template, request, static_file
from japanese.Japanese_DB_handler import Japanese_DB_handler
from japanese import search
from japanese.SearchResult import WordSearchResult, WordListSearchResult, SelectorResult
from Selector import Categorie, Tag, Kanjis, Core_P
from Word import Word
from www import www_config


# CONST ***********************************************************************
# *****************************************************************************

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
 
app = Bottle()
selector_set = {Categorie, Tag, Kanjis, Core_P}

# TODO : Del this ! selector type already defined in selector object...
# seriously ...
search_type_to_selector = {
    'tag' : Tag, 
    'categorie' : Categorie, 
    'kanji' : Kanjis, 
    'core_prononciation' : Core_P
}

application_title = 'kioku 記憶'
main_css = '/main.css'

# PAGES ***********************************************************************
# *****************************************************************************

@app.route('/')
@view('main_page')
def main_page() :
    name = application_title
    css_file = main_css
    body = template('main_page', body = header_kioku())
    data = page_base_structure(name, css_file, body)
    return data

@app.route('/selectors/<selector>')
def selector_list_page(selector):


    selector = get_selector_from_url(selector)
    if not selector : return 'prout'
    selector_list, selector_number = selector.get_selector_list_data()

    name = application_title + ': ' + selector.sub_url
    css_file = main_css    
    body = header_kioku()
    body += list_selector_id(selector, selector_number, selector_list)
    data = page_base_structure(name, css_file, body)

    return data

@app.route('/selectors/<selector>/<selector_id>')
def selector_single_page(selector, selector_id): 

    selector = get_selector_from_url(selector)
    if not selector : return 'prout' 
    vocab_list = selector.get_vocab_from_selector(selector_id)

    name = application_title + ', ' + selector.selector_type + ': ' + selector_id
    css_file = main_css 
    
    body = header_kioku()
    body += header_selector(selector, selector_id)
    body += list_vocabulary(www_config.get_vocab_format_as_string(), vocab_list)

    data = page_base_structure(name, css_file, body)

    return data

@app.route('/words/<word_id>')
def word_page(word_id): 

    word_data = Word.get_word_data(word_id)
    if not word_data : return 'prout'

    name = application_title + ': ' + word_id
    css_file = main_css 
    body = header_kioku()
    body += word_page(word_data)

    data = page_base_structure(name, css_file, body)

    return data

@app.route('/search', method = 'GET')
def search_page(): 
    if not request.GET.input : return 'NON'
    search_input = request.GET.input
    search_result = search.search_web_app(search_input)

    name = application_title + ' search results : ' + search_input
    css_file = main_css

    body = header_kioku()
    body += header_search(search_input)
    for single_result in search_result.get_ordered_search_result() : 
        if type(single_result) not in select_results_template.keys() : 
            log.error('unknownType')
        else : 
            body += select_results_template[type(single_result)](search_input, single_result)

    data = page_base_structure(name, css_file, body)

    return data

# distributing static files. 
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='www/static/')


# RENDERING WEB ***************************************************************
# *****************************************************************************

@view('base_structure')
def page_base_structure(page_name, css_file, body) : 
    return template('base_structure', page_name = page_name, css_file = css_file, body = body)


# contains the app name and a search field. 
@view('header_kioku')
@view('link')
def header_kioku() :
    global application_title

    title = template('link', text = application_title, url = '/')
    selector_link_list = [create_selector_type_link(selector) 
        for selector in selector_set]
    return template('header_kioku', title = title,  selector_link_list  = selector_link_list)

# selector are : kanjis / tag / categories etc...
@view('header_selector')
def header_selector(selector, selector_id) :
    selector_link = create_selector_type_link(selector)
    # return 'prout'
    return template('header_selector', selector = selector_link, selector_id = selector_id)

@view('header_search')
def header_search(search_input) :
    return template('header_search', search_input = search_input)

# used to display a list a vocab, vocab list is a list of tuple ordered as such : 
# (word, prononciation, meaning, example)
@view('list_vocabulary')
def list_vocabulary(vocab_format, vocab_list) : 
    linked_vocab_id_list = []
    for vocab in vocab_list : 
        word_id, *rest = vocab
        linked_vocab_id_list.append((create_word_id_link(word_id), *rest))
    return template('list_vocabulary', vocab_format = vocab_format, vocab_list = linked_vocab_id_list)

@view('list_selector_id')
def list_selector_id(selector, number, selector_id_list) :

    linked_selector_id_list = []
    for selector_id, selector_id_occurence in selector_id_list : 
        linked_selector_id_list.append((
            create_selector_id_link(selector, selector_id) if selector_id else selector_id,
            selector_id_occurence
            ))

    return template('list_selector_id', selector = selector.sub_url, 
        number = number, selector_id_list = linked_selector_id_list)

@view('word_page')
def word_page(word_data) :

    if word_data['kanjis'] : 
        kanjis_data = [create_selector_id_link(Kanjis, kanji) for kanji in word_data['kanjis'] if kanji]
    else : kanjis_data = None

    if word_data['tag'] and len(word_data['tag']): #TODO surdegueu, pb dans la BDD
        tag_data = create_selector_id_link(Tag, word_data['tag'])
    else : tag_data = None

    if word_data['categorie']: 
        categorie_data = create_selector_id_link(Categorie, word_data['categorie'])
    else : categorie_data = None

    return template(
        'word_page', 
        word =  word_data['word'], 
        prononciation = word_data['prononciation'], 
        meaning = word_data['meaning'], 
        example = word_data['example'], 
        categorie = categorie_data, 
        tag =  tag_data, 
        kanjis = kanjis_data, 
        )

@view('link')
def create_selector_id_link(selector, selector_id) : 
    url = selector.gen_url_to_selector_id(selector_id)
    return template('link', text = selector_id, url = url)

@view('link')
def create_selector_type_link(selector) : 
    url = selector.gen_url_to_selector_type()
    text = selector.selector_type
    return template('link', text = text, url = url)

@view('link')
def create_word_id_link(word_id) : 
    url = Word.gen_url_to_word(word_id)
    text = word_id
    return template('link', text = text, url = url)

@view('search_result_word')
def search_result_word(input, wordSearchResult) : 
    data = search_result_header('word', input)
    kanji_data = [create_word_id_link(Kanjis, kanji) for kanji in wordSearchResult.kanjis]
    data += template('search_result_word', 
        word = wordSearchResult.word, 
        prononciation = wordSearchResult.prononciation,
        meaning = wordSearchResult.meaning, 
        kanjis = kanji_data)
    return data

def search_result_word_list(input, wordListSearchResult) : 
    word_data = [(item.word, item.prononciation, item.meaning) for item in wordListSearchResult.word_list]
    data = search_result_header('approximations', input)
    data += list_vocabulary(www_config.get_short_vocab_format_as_string(), word_data)
    # data += template('search_result_word_list', vocab_list = word_data)
    return data

def search_result_selector(input, selectorSearchResult) :
    selector = search_type_to_selector[selectorSearchResult.selector_type]
    linked_selector = create_selector_id_link(selector, input)
    examples_data = [create_word_id_link(word) for word in selectorSearchResult.word_examples]
    data = search_result_header(selectorSearchResult.selector_type, linked_selector, examples_list = examples_data)
    # TODO : MISSING STUFF
    return data

@view('search_result_header')
def search_result_header(result_type, result_value, examples_list = None) : 
    return template('search_result_header', result_type = result_type, result_value = result_value, examples_list = examples_list)


select_results_template  = {
    WordSearchResult : search_result_word,
    WordListSearchResult : search_result_word_list,
    SelectorResult : search_result_selector
}


# UTILS ***********************************************************************
# *****************************************************************************


def get_selector_from_url(url) : 
    return next((selector for selector in selector_set if selector.sub_url == url), None)
    

run(app, host='localhost', port=8080, reloader = True)




