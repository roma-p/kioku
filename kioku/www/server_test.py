from bottle import Bottle, run, view, template
from japanese.Japanese_DB_Handler import Japanese_DB_handler
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
 
app = Bottle()
 
# @app.route('/')
# @view('template.tpl')
# def hello():
#     context = {'title': "Max est le plus beau"}
#     return (context)


stat_list_names = {
    'categories' : ('most_used_categories', 'categories_number'),
    'tags' : ('most_used_tags', 'tags_number'),
    'kanjis' : ('most_used_kanjis','kanjis_number'),
    'core prononciation' : ('most_used_core_p', 'core_p_number')
}


@app.route('/test')
@view('list_test.tpl')
def hello():
    jpDB = Japanese_DB_handler() 
    stat_dict = jpDB.get_db_stat()
    output = ''
    for list_name, list_info in stat_list_names.items() :
        most_used, number = list_info
        output += template('list_test', rows=stat_dict[most_used], list_name=list_name, number = stat_dict[number])
    return output


@app.route('/categories')
@view('full_list.tpl')
def categories_page(): 
    jpDB = Japanese_DB_handler() 
    data = jpDB.list_categorie_by_usage()
    output = template('full_list', rows=data, list_name='categories')
    return output

 
@app.route('/')
def stat_test():
    jpDB = Japanese_DB_handler() 
    print(jpDB)
    print(jpDB.base_format)
    stat_dict = jpDB.get_db_stat()
    return str(dict(stat_dict['most_used_categories']))


@app.route('/categories_old/<categorie_id>')
@view('categorie')
def categorie_page(categorie_id) : 

    jpDB = Japanese_DB_handler()
    f = jpDB.base_format
    checked_cat_id = categorie_id if jpDB.check_categorie_existence(categorie_id) else None

    if checked_cat_id :
        item_to_get = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning,f.vocab.example)
        vocab_rows = jpDB.list_word_by_categorie(categorie_id, *item_to_get)
    else : 
        vocab_rows = ()

    output = template('categorie', name = checked_cat_id, rows = vocab_rows)
    return output

@view('vocab_list')
def render_vocab_list(vocab_list) : 
    return template('vocab_list', rows = vocab_list)

@app.route('/categories_old/<categorie_id>')
@view('categorie')
def categorie_page(categorie_id) : 

    jpDB = Japanese_DB_handler()
    f = jpDB.base_format
    checked_cat_id = categorie_id if jpDB.check_categorie_existence(categorie_id) else None

    if checked_cat_id :
        item_to_get = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning,f.vocab.example)
        vocab_rows = jpDB.list_word_by_categorie(categorie_id, *item_to_get)
    else : 
        vocab_rows = ()

    output = template('categorie', name = checked_cat_id, rows = vocab_rows)
    return output

run(app, host='localhost', port=8081)


