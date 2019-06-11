import unittest, os, gc, logging, sys
from context import kioku
from kioku.japanese.Japanese_DB_handler import Japanese_DB_handler
from kioku.japanese import japanese_dataBaseFormat
from kioku.japanese import search
from kioku import configuration

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

test_dir = 'test/jp_db/'
approximation_db = test_dir + 'approximation_db.sqlite'

sys.path.append('kioku/etc/kioku/config.ini')

class TestSearch(unittest.TestCase) : 

    def setUp(self) : 
        self.connect_to_correct_DB()

    def monkey_patch_JPDB_init(self, db_path, base_format) : 
        def init_patched(self) :
            super(Japanese_DB_handler, self).__init__(db_path, base_format)          
        Japanese_DB_handler.__init__ = init_patched
        return Japanese_DB_handler()

    def patchConfigPath(self) : 
        def path() : return 'kioku/etc/kioku/config.ini'
        configuration.path = path

    def connect_to_correct_DB(self, db_path = approximation_db) : 
        self.patchConfigPath()
        base_format = japanese_dataBaseFormat.get_baseFormat()
        return self.monkey_patch_JPDB_init(db_path, base_format)

    def test_kanji(self) : 
        print('meeeerde')
        a = search.search_kanji('瀬')

    def test_search_normal(self) : 
        a = search.search_normal('ない')
        # print(a)
        a = search.search_normal('つまらない')
        # print(a)
        a = search.search_normal('time')
        # print(a)
        a = search.search_normal('short')
        # print(a)

    def test_search_web_app(self): 
        a = search.search_web_app('瀬')
        print(a)

if __name__ == '__main__': unittest.main()

