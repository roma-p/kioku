#from .context.kioku.DB_handler import DB_handler
import unittest, os
from shutil import copyfile
from context import kioku
from kioku.DB_handler import DB_handler

empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"

class TestDB_Handler(unittest.TestCase) :

	def setUp(self):
		copyfile(original_db, working_db)
	def tearDown(self):
		# os.remove(working_db)
		pass

	def test_lol(self):
		db_handler = DB_handler(working_db)
		db_handler_2 = DB_handler(working_db)
			
		# checking singleton. 
		self.assertEqual(id(db_handler), id(db_handler_2))

		lol = [
			("n_cat", "n_tag", "n_word", "n_hastuon", "n_meaning", "n_exemple")
		]

		db_handler.add("vocab",*lol)

		del(db_handler)
		del(db_handler_2)

if __name__ == '__main__':
    unittest.main()