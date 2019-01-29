import unittest, os, gc, glob, logging
from context import kioku
from shutil import copyfile
import kioku.db_update as db_update
from kioku.DB_handler import DB_handler
import kioku.configuration as configuration

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"
config_path = "test/db_update/config.ini"
inputFile_1 = 'test/db_update/testJap1.csv'
inputFile_2 = 'test/db_update/testJap2.csv'

class TestDB_Handler(unittest.TestCase):


	def setUp(self): 

		# monkey patching configuration for test purpose. 
		def path_patched(): return config_path
		configuration.path = path_patched
		self.data = configuration.getConfiguration()
		
		# creating working DB.
		copyfile(original_db, working_db)


	def tearDown(self):
		# deconnection from database. 
		db_handler = DB_handler()
		del(db_handler)
		# removing database file. 
		gc.collect()
		os.remove(working_db)
		# removing backup files.
		backup_dir = self.data.get('kioku', 'intermediate_files_bk')
		for file in glob.glob(backup_dir + '*.csv') : 
			os.remove(file)


	def test_add(self):
		db_handler = DB_handler()
		print(db_handler)
		print(db_handler.db_path)
		db_update.add(inputFile_1)
		kanjis_list = db_handler.select('vocab', 'word')
		len_kanjis = len(kanjis_list)
		self.assertEqual(len_kanjis, len(set(kanjis_list)), msg='all duplicate are not well detected in file itself...')
		
		db_update.add(inputFile_2)
		kanjis_list_a = db_handler.select('vocab', 'word')

		checkingset = {
			('もう時間でずよ',),
			('ぼやぼや',),
			('びっくり する',),
			('ぼろぼろ',),
			('ぶるぶる',),
			('ほら',),
			('ほっつき歩く',)
			}

		self.assertEqual((set(kanjis_list_a) - set(kanjis_list)), checkingset)


if __name__ == '__main__':
    unittest.main()