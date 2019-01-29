import unittest, os, gc, logging, glob, datetime
from context import kioku
from shutil import copyfile
from kioku import configuration
from kioku import command
from kioku.DB_handler import DB_handler
import kioku.db_update as db_update


logging.basicConfig() 
log = logging.getLogger()
log.setLevel(logging.DEBUG)

empty_db = "test/empty_db/"
original_db = empty_db + "original.sqlite"
working_db = empty_db + "working.sqlite"
testDir = 'test/command/'
config_path = testDir + "config.ini"
config_path_2 = testDir + "config-update.ini"
inputFile = testDir + 'testJap1.csv'
inputDir = testDir + 'inputDir'
bkDir = testDir + "db_bk/"


class TestDB_Handler(unittest.TestCase) :

	def setUp(self):

		# monkey patching configuration for test purpose. 
		def path_patched() : return config_path
		configuration.path = path_patched
		self.data = configuration.getConfiguration()

		# creating working DB.
		copyfile(original_db, working_db)


	def tearDown(self):
		db_handler = DB_handler()
		del(db_handler)
		print(DB_handler._instances)
		gc.collect()

		for file in [working_db, testDir + 'kioku1.db'] : 
			if os.path.exists(file) :
				os.remove(file)

		pathToRemove = [
			self.data.get('kioku', 'db_bk'), 
			self.data.get('kioku', 'intermediate_files_bk') 
		]
		
		for path in pathToRemove:		
			if os.path.exists(path) : 
				for file in glob.glob(path+'/*', recursive=True) : 
					os.remove(file)


	def test_kiokuInit(self):

		status = command.init_kioku()
		self.assertEqual(status, True, 'error initializing kioku when db not existing.')
		self.assertEqual(os.path.exists(self.data.get('kioku', 'db_path')), True, msg='DB not created as expected.')
		status = command.init_kioku()
		self.assertEqual(status, True, 'error reading conf when already initialized.')


	def test_backup_DB(self):
		
		bk_name = "db_bk_test.db"
		status = command.backup_DB(bk_name)
		
		self.assertEqual(status, False, msg='non existing DB has been backuped.')
		status = command.init_kioku()
		self.assertEqual(status, True, msg='could not even initialize kioku to test backup...')
		status = command.backup_DB(bk_name)
		self.assertEqual(status, True, msg='backup process failed.')
		self.assertEqual(os.path.exists(self.data.get('kioku', 'db_bk')+"/"+bk_name), True, msg='DB backup has not been created as expected.')


	def test_reset_DB(self):
		
		status = command.init_kioku()
		self.assertEqual(status, True, msg='could not even initialize kioku to test reset...')
		status = command.reset_DB()
		self.assertEqual(status, True, msg='reset process failed.')
		bk_name = self.data.get('kioku', 'db_bk') + '/' + os.path.basename(self.data.get('kioku', 'db_path'))[:-3] + command.reset_suffix
		self.assertEqual(len(glob.glob(bk_name+'*')), 1, msg="backup name not found...")
		self.assertEqual(os.path.exists(self.data.get('kioku', 'db_path')), True, msg=' new DB not created as expected.')
		

	def init_db_update_test(self) : 

		configuration.reset()
		def path_patched() : return config_path_2
		configuration.path = path_patched
		db_handler = DB_handler()
		db_handler.__init__()
		return db_handler


	def test_update_add(self) : 

		db_handler = self.init_db_update_test()
		command.update_DB(inputFile)
		kanjis_list = db_handler.select('vocab', 'word')
		self.assertGreater(len(kanjis_list), 0)
		self.assertEqual(os.path.exists(configuration.getConfiguration().get('kioku', 'intermediate_files_bk')+'/testJap1.csv'), True)

	def test_update_multiple(self) : 

		db_handler = self.init_db_update_test()
		command.update_DB(inputDir)
		kanjis_list = db_handler.select('vocab', 'word')
		self.assertGreater(len(kanjis_list), 0)
		for i in range(1,4) : 	
			self.assertEqual(os.path.exists(configuration.getConfiguration().get('kioku', 'intermediate_files_bk')+'/testJap'+str(i)+'.csv'), True)


if __name__ == '__main__':
    unittest.main()