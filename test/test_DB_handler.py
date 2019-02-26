#from .context.kioku.DB_handler import DB_handler
import unittest, os, gc, logging
from shutil import copyfile
from context import kioku
from kioku.DB_handler import DB_handler
from kioku import database_format_register as r

empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"
gen_db = empty_db+ "gen_db.sqlite"

logging.basicConfig() 

log = logging.getLogger()
log.setLevel(logging.DEBUG)


base_format = {
	'vocab' : {
		**r.table_id_index(),
		'word' : {r.type() : r.type_text()}, 
		'prononciation' : {r.type() : r.type_text()},
		'meaning' : {r.type() : r.type_text()}, 
		'exemple' : {r.type() : r.type_text()}, 
		'categorie' : {r.type() : r.type_text()}, 
		'tag' : {r.type() : r.type_text()}, 
		**r.table_date()
	}, 
	'tag' : {
		**r.table_id_index(),
		'name' : {r.type() : r.type_text()}	
	}
}



class Fake_DB_handler(DB_handler):
	def __init__(self, arg):
		super().__init__(arg)
		self.base_format = base_format
	

class TestDB_Handler(unittest.TestCase) :


	def setUp(self):
		copyfile(original_db, working_db)


	def tearDown(self):
		gc.collect()
		for path in [working_db, gen_db] : 
			if os.path.exists(path) :
				os.remove(path)


	def test_dbHandler(self):
		db_handler_a = Fake_DB_handler(working_db)
		db_handler = Fake_DB_handler()

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

		del(db_handler)
		db_handler = Fake_DB_handler()

	def test_gendb(self) : 
		db_handler = Fake_DB_handler()
		db_handler.db_path = gen_db
		db_handler.generateDB()



if __name__ == '__main__':
    unittest.main()