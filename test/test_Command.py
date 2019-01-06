import unittest, os, gc, logging, glob
from context import kioku
from kioku import configuration
from kioku import command
from kioku.DB_handler import DB_handler


logging.basicConfig() 

log = logging.getLogger()
log.setLevel(logging.DEBUG)

testDir = 'test/command/'

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
		
		for file in glob.glob(testDir+'*.db') : 
			os.remove(file)



		pass


	def test_kiokuInit(self):

		status = command.init_kioku()
		self.assertEqual(status, True, 'error initializing kioku when db not existing.')
		self.assertEqual(os.path.exists(self.data.get('kioku', 'db_path')), True, msg='DB not creating as expected.')
		status = command.init_kioku()
		self.assertEqual(status, True, 'error reading conf when already initialized.')

		pass

	def test_backup_DB(self): 
		pass



if __name__ == '__main__':
    unittest.main()