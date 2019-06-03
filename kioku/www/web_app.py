import logging
from bottle import Bottle, run, view, template
from japanese.japanese.Japanese_DB_handler import Japanese_DB_handler
from Selector import Categorie, Tag, Kanjis, Core_P
from Word import Word


# CONST ***********************************************************************
# *****************************************************************************

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
 
app = Bottle()
selector_set = {Categorie, Tag, Kanjis, Core_P}

# PAGES ***********************************************************************
# *****************************************************************************


# -> To factorize with every selector list pages. 
# -> all of it in a subwebpage /selector. 

@app.route('/selectors/<selector>')
def selector_list_page(selector):

    selector = get_selector_from_url(selector)
    if not selector : return 'prout'
    selector_list, selector_number = selector.get_selector_list_data()

    data = header_kioku()
    data += list_selector_id(selector, selector_number, selector_list)
    return data

@app.route('/selectors/<selector>/<selector_id>')
def selector_single_page(selector, selector_id): 

    selector = get_selector_from_url(selector)
    if not selector : return 'prout' 
    vocab_list = selector.get_vocab_from_selector(selector_id)
    data = header_kioku()
    data += header_selector(selector, selector_id)
    data += list_vocabulary(vocab_list)

    return data


@app.route('/words/<word_id>')
def word_page(word_id): 

    word_data = Word.get_word_data(word_id)
    if not word_data : return 'prout'

    data = header_kioku()
    data += word_page(word_data)

    return data


# RENDERING WEB ***************************************************************
# *****************************************************************************

# contains the app name and a search field. 
@view('header_kioku')
def header_kioku() : 
    return template('header_kioku')

# selector are : kanjis / tag / categories etc...
@view('header_selector')
def header_selector(selector, selector_id) :
    selector_link = create_selector_type_link(selector)
    # return 'prout'
    return template('header_selector', selector = selector_link, selector_id = selector_id)

# used to display a list a vocab, vocab list is a list of tuple ordered as such : 
# (word, prononciation, meaning, example)
@view('list_vocabulary')
def list_vocabulary(vocab_list) : 
    linked_vocab_id_list = []
    for vocab in vocab_list : 
        word_id, *rest = vocab
        linked_vocab_id_list.append((create_word_id_link(word_id), *rest))
    return template('list_vocabulary', vocab_list = linked_vocab_id_list)

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


# UTILS ***********************************************************************
# *****************************************************************************


def get_selector_from_url(url) : 
    return next((selector for selector in selector_set if selector.sub_url == url), None)
    

run(app, host='localhost', port=8080)




