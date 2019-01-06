import unittest, os, gc, logging, glob, datetime
from context import kioku
from kioku import configuration
from kioku import command
from kioku.DB_handler import DB_handler


logging.basicConfig() 

log = logging.getLogger()
log.setLevel(logging.DEBUG)

testDir = 'test/command/'
bkDir = testDir + "db_bk/"


class TestDB_Handler(unittest.TestCase) :

	def setUp(self):

		# monkey patching configuration for test purpose. 
		def path_patched() : return "test/command/config.ini"
		configuration.path = path_patched
		self.data = configuration.getConfiguration()
		pass


	def tearDown(self):
#		gc.collect()
#		os.remove(working_db)
		for path in (testDir, bkDir):		
			for file in glob.glob(path+'*.db', recursive=True) : 
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
		print(bk_name)
		self.assertEqual(len(glob.glob(bk_name+'*')), 1, msg="backup name not found...")
		self.assertEqual(os.path.exists(self.data.get('kioku', 'db_path')), True, msg=' new DB not created as expected.')
		


if __name__ == '__main__':
    unittest.main()