#from .context.kioku.DB_handler import DB_handler
import unittest, os, gc, logging
from shutil import copyfile
from context import kioku
from kioku.DB_handler import DB_handler

empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"

logging.basicConfig() 

log = logging.getLogger()
log.setLevel(logging.DEBUG)

class TestDB_Handler(unittest.TestCase) :


	def setUp(self):
		copyfile(original_db, working_db)


	def tearDown(self):
		gc.collect()
		os.remove(working_db)


	def test_dbHandler(self):
		db_handler_a = DB_handler(working_db)
		db_handler = DB_handler()

		# checking singleton. 
		self.assertEqual(id(db_handler), id(db_handler_a))

		lol = [
			("a_cat", "a_tag", "word_1", "hastuon_1", "a_meaning", "a_exemple"),
			("a_cat", "c_tag", "word_2", "hastuon_2", "a_meaning", "a_exemple"),
			("b_cat", "c_tag", "word_3", "hastuon_3", "b_meaning", "b_exemple"),		
		]

		db_handler.add("vocab",*lol)
		a = db_handler.select("vocab", "word", "categorie")
		b = db_handler.select("vocab", "word", categorie = "a_cat")
		c = db_handler.select("vocab", "word", 'prononciation', categorie = "a_cat", tag = "c_tag")

		self.assertEqual(a, (('word_1', 'a_cat'), ('word_2', 'a_cat'), ('word_3', 'b_cat')))
		self.assertEqual(b, (('word_1',), ('word_2',)))
		self.assertEqual(c, (('word_2', 'hastuon_2'),))

		d = db_handler.count("vocab", categorie = "a_cat")
		self.assertEqual(d, 2)

		a = [(('lol'),)]
		db_handler.add('tag', *a)
		a = db_handler.select('tag', 'name')

		del(db_handler)
		db_handler = DB_handler()

if __name__ == '__main__':
    unittest.main()