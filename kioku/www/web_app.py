import logging
from bottle import Bottle, run, view, template
from DB.Japanese_DB_handler import Japanese_DB_handler
from Selector import Categorie, Tag, Kanjis, Core_P


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
    data += list_selector_id(selector.sub_url, selector_number, selector_list)
    return data

@app.route('/selectors/<selector>/<selector_id>')
def selector_single_page(selector, selector_id): 

    selector = get_selector_from_url(selector)
    if not selector : return 'prout' 
    vocab_list = selector.get_vocab_from_selector(selector_id)

    data = header_kioku()
    data += header_selector(selector.selector_id, selector_id)
    data += list_vocabulary(vocab_list)

    return data


@app.route('/words/<word_id>')
def word_page(word_id): 

    jpDB= Japanese_DB_handler()
    word_data = jpDB.get_word_info(word_id)
    print(word_data)

    if not word_data : return 'prout'

    data = header_kioku()



# RENDERING WEB ***************************************************************
# *****************************************************************************

# contains the app name and a search field. 
@view('header_kioku')
def header_kioku() : 
    return template('header_kioku')

# selector are : kanjis / tag / categories etc...
@view('header_selector')
def header_selector(selector, selector_id) :
    return template('header_selector', selector = selector, selector_id = selector_id)

# used to display a list a vocab, vocab list is a list of tuple ordered as such : 
# (word, prononciation, meaning, example)
@view('list_vocabulary')
def list_vocabulary(vocab_list) : 
    return template('list_vocabulary', vocab_list = vocab_list)

@view('list_selector_id')
def list_selector_id(selector, number, selector_id_list) :
    return template('list_selector_id', selector = selector, 
        number = number, selector_id_list = selector_id_list)

@view('word_page')
def word_page(word_data) : 
    pass

# UTILS ***********************************************************************
# *****************************************************************************

def gen_url_selector_dict() : 
    global selector_set
    return {selector.sub_url : selector for selector in selector_set}

def get_selector_from_url(url) : 
    return next((selector for selector in selector_set if selector.sub_url == url), None)
    

run(app, host='localhost', port=8080)




