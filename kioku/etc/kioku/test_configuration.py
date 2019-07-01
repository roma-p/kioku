import unittest, os, gc, logging
from context import kioku
from kioku import configuration

log = logging.getLogger()

class TestDB_format(unittest.TestCase) : 

    def test_config_relative(self) : 
        configuration.CFG_INI_PATH = "test/configuration/config-test.ini"
        configuration = get_configuration()
        print(configuration)


if __name__ == '__main__': unittest.main()