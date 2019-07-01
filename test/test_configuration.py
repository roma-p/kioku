import unittest, os, gc, logging
from context import kioku
from kioku import configuration

log = logging.getLogger()

class TestDB_format(unittest.TestCase) : 

    def test_config_relative(self) : 
        configuration.CFG_INI_PATH = "test/configuration/config-test.ini"
        cfg = configuration.get_configuration()
        self.assertIn('test/configuration/kioku1.db', cfg.db_path)

if __name__ == '__main__': unittest.main()