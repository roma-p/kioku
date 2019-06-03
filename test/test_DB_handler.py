#from .context.kioku.DB_handler import DB_handler
import unittest, os, gc, logging
from shutil import copyfile
from context import kioku
from kioku.DB.DB_handler import DB_handler
from kioku.DB.Query import Query
from kioku.DB import database_format_register as r

empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"
gen_db = empty_db + "gen_db.sqlite"
query_db = empty_db + "query_db.sqlite"

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

simple_text_field = {r.type() : r.type_text()}
simple_int_field = {r.type() : r.type_integer()}

# HOW TO PASS CONTRAINTS THROUGH DICT ?
# NOT WORKING !!!

base_format = {
    'vocab' : {
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field,
        'meaning' : simple_text_field, 
        'exemple' : simple_text_field, 
        'categorie' : simple_text_field, 
        'tag' : simple_text_field, 
    }, 
    'tag' : {
        r.id() : True,
        'name' : simple_text_field  
    }
}

base_format_2 = {
    'vocab' : {
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field,
        'meaning' : simple_text_field, 
        'exemple' : simple_text_field, 
        'categorie' : simple_text_field, 
        'tag' : simple_text_field, 
    }, 
    'tag' : {
        r.id() : True,
        'name' : simple_text_field  
    },
    'word_kanjis' : {
        r.id() : True,
        'word_id' : {r.type() : r.type_integer()}, 
        'kanjis' : simple_text_field,
    },  
}

db_fkeys_correct = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'meaning' : simple_text_field, 
        'categorie' : simple_int_field,
        'tag' : simple_int_field,
        r.key_foreign() : {
            'tag' : ('tags', 'id'),
            'categorie' : ('categories', 'id')
            } 
    }, 
    'categories' : {
        r.id() : True,
        'name' : simple_text_field  
    },
    'tags' : {
        r.id() : True,
        'name' : simple_text_field  
    } 
}

class Fake_DB_handler(DB_handler):
    def __init__(self, arg):
        super().__init__(arg)
    

class TestDB_Handler(unittest.TestCase) :

    def setUp(self):
        copyfile(original_db, working_db)

    def tearDown(self):
        gc.collect()
        for path in [working_db, gen_db, query_db] : 
        # for path in [working_db, query_db] : 
            if os.path.exists(path) :
                os.remove(path)

    def test_dbHandler(self):
        db_handler_a = DB_handler(working_db, base_format)
        db_handler = DB_handler()

        # checking singleton. 
        self.assertEqual(id(db_handler), id(db_handler_a))

        lol = [
            ("a_cat", "a_tag", "word_1", "hastuon_1", "a_meaning", "a_exemple"),
            ("a_cat", "c_tag", "word_2", "hastuon_2", "a_meaning", "a_exemple"),
            ("b_cat", "c_tag", "word_3", "hastuon_3", "b_meaning", "b_exemple"),        
        ]

        dataOrder = ('categorie', 'tag', 'word', 'prononciation', 'meaning', 'exemple')
        db_handler.add("vocab", dataOrder, *lol)
        a = db_handler.select("vocab", "word", "categorie")
        b = db_handler.select("vocab", "word", categorie = "a_cat")
        c = db_handler.select("vocab", "word", 'prononciation', categorie = "a_cat", tag = "c_tag")

        self.assertEqual(a, (('word_1', 'a_cat'), ('word_2', 'a_cat'), ('word_3', 'b_cat')))
        self.assertEqual(b, (('word_1',), ('word_2',)))
        self.assertEqual(c, (('word_2', 'hastuon_2'),))

        d = db_handler.count("vocab", categorie = "a_cat")
        self.assertEqual(d, 2)



        a = [(('lol'),)] #uhm ... not ugly at all. 
        db_handler.add('tag', ('name',), *a)
        a = db_handler.select('tag', 'name')

        # testing update / replace / delete.
        db_handler.replace('vocab', 'tag', 'c_tag', 'd_tag')
        a = db_handler.select('vocab', 'word', tag = 'd_tag')
        self.assertEqual(set(a), {('word_2',), ('word_3',)})    
        db_handler.update('vocab', 'tag', 'e_tag', tag = 'd_tag', categorie = 'b_cat')
        a = db_handler.select('vocab', 'word', tag = 'e_tag')       
        self.assertEqual(set(a), {('word_3',)})
        db_handler.delete('vocab', tag = 'e_tag')
        a = db_handler.select('vocab', 'word', tag = 'e_tag')
        self.assertEqual(a, ())

        lol = [("word_r", "r_cat", "r_tag"),]
        dataOrder = ('word', 'categorie', 'tag')
        db_handler.add("vocab", dataOrder, *lol)
        a = db_handler.select('vocab', 'word', 'categorie', 'tag', tag = 'r_tag')
        self.assertEqual(set(a), {('word_r', 'r_cat', 'r_tag')})

        f = db_handler.base_format
        conditions = {f.vocab.tag() : 'r_tag'}
        a = db_handler.select(f.vocab, f.vocab.word, f.vocab.categorie, f.vocab.tag, **conditions)
        self.assertEqual(set(a), {('word_r', 'r_cat', 'r_tag')})
        del(db_handler)

    def test_gendb(self) : 
       db_handler = DB_handler(gen_db, base_format)
       db_handler.generateDB() 
       self.assertTrue(os.path.exists(gen_db))
       lol = [("a_cat", "a_tag", "word_1", "hastuon_1", "a_meaning", "a_exemple"),]
       dataOrder = ('categorie', 'tag', 'word', 'prononciation', 'meaning', 'exemple')
       db_handler.add("vocab", dataOrder, *lol)
       a = db_handler.select("vocab", "word", categorie = "a_cat")
       self.assertEqual(a, (('word_1',),))
       del(db_handler)


    def test_gendb_fkey(self) : 

       db_handler = DB_handler(gen_db, db_fkeys_correct)
       db_handler.generateDB() 
       self.assertTrue(os.path.exists(gen_db))

       vocab_list = [
           ("a_cat", "a_tag", "word_1", "hastuon_1"),
           ("a_cat", "b_tag", "word_2", "hastuon_2"),
           ("b_cat", "c_tag", "word_3", "hastuon_3"),        
       ]

       vocab_list = [
           (1, 1000000, "word_1", "hastuon_1"),

       ]

       data_order = ('categorie', 'tag', 'word', 'prononciation')

       cat_list = (('a_cat',),)
       tag_list = (('a_tag',),('b_tag',),)
       db_handler.add('tags', ['name'], *tag_list)
       db_handler.add('categories', ['name'], *cat_list)
       db_handler.add('vocab', data_order, *vocab_list)

       del(db_handler)


    def test_query(self) : 
        db_handler = DB_handler(query_db, base_format_2)
        db_handler.generateDB() 
        data_1 = [
            ("a_cat", "a_tag", "word_1", "hastuon_1", "a_meaning", "a_exemple"),
            ("a_cat", "c_tag", "word_2", "hastuon_2", "a_meaning", "a_exemple"),
            ("b_cat", "c_tag", "word_3", "hastuon_3", "b_meaning", "b_exemple"),        
        ]
        dataOrder_1 = ('categorie', 'tag', 'word', 'prononciation', 'meaning', 'exemple')
        db_handler.add("vocab", dataOrder_1, *data_1)
        data_2 = [
            (1, 'kanjis_1'), 
            (1, 'kanjis_2'),
            (2, 'kanjis_2'),
            (2, 'kanjis_3'), 
            (3, 'kanjis_4')
        ]
        dataOrder_2 = ('word_id', 'kanjis')
        db_handler.add('word_kanjis', dataOrder_2, *data_2)

        db_f = db_handler.base_format
        q = Query().select(db_f.vocab, db_f.vocab.word, db_f.vocab.prononciation)
        q.where().equal(db_f.vocab.tag, 'a_tag')
        q.or_().equal(db_f.vocab.categorie, 'a_cat')

        data = db_handler.executeQuery(q)
        self.assertEqual(data, (('word_1', 'hastuon_1'), ('word_2', 'hastuon_2')))

        q = Query().select(db_f.vocab, db_f.vocab.word)
        q.join_left(db_f.vocab.id, db_f.word_kanjis.word_id)
        q.where().not_equal(db_f.word_kanjis.kanjis, 'kanjis_2')

        q = Query().select(db_f.word_kanjis, db_f.vocab.word)
        q.join_left(db_f.word_kanjis.word_id , db_f.vocab.id)
        q.where().equal(db_f.word_kanjis.kanjis, 'kanjis_2')

        data = db_handler.executeQuery(q)
        self.assertEqual(data, (('word_1',), ('word_2',)))      

        q = Query().select(db_f.word_kanjis, db_f.vocab.word)
        q.join_left(db_f.word_kanjis.word_id , db_f.vocab.id)
        q.where().equal(db_f.word_kanjis.kanjis, 'kanjis_4')

        data = db_handler.executeQuery(q)
        self.assertEqual(data, (('word_3',),))      
        
        del(db_handler)



if __name__ == '__main__':
    unittest.main()