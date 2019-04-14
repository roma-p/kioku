import unittest, os, gc, logging
from context import kioku
from kioku.DB.Japanese_DB_handler import Japanese_DB_handler
from kioku.DB import japanese_dataBaseFormat

log = logging.getLogger()

test_dir = 'test/jp_db/'
japanese_db_path = test_dir + 'japanese_db.sqlite'


japanese_vocab = [
    ('ふと',None,'accidentellement,  par hasard,  soudainement','suddenly','short',None),
    ('青春','せいしゅん','Adolescence, jeunesse, vertes années','people',None,None),
    ('器用','きよう','Adroit','meal',None,None),
    ('指輪','ゆびわ','Anneau','cloth',None,None),
    ('持ってくる','もってくる','Apporter','bring','composed',None),
    ('態度','たいど','Attitude','character',None, None),
    ('手前','てまえ','Avant, de ce côté','location',None,None),
    ('結構な','けっこう','Beau, bien, réussi','judgment',None,None),
    ('真っ白な','まっしろ','Blanc immaculé','color',None,None),
    ('真っ青', 'まっさお','Bleu foncé','color',None,None),
    ('穏やか','おだやか','Calme, gentil, tranquille','character',None,None),
    ('長閑な','のどか','Calme, serein','character',None,None)
]

cat_list = ('suddenly','people','meal','cloth','bring','character','location','judgment','color','color','character','character')
tag_list = ('short', 'composed')

class TestJapanese_DB_handler(unittest.TestCase) : 

    def setUp(self) : 

        def init_patched(self) :
            db_path = japanese_db_path
            base_format = japanese_dataBaseFormat.get_baseFormat()
            super(Japanese_DB_handler, self).__init__(db_path, base_format)          
        Japanese_DB_handler.__init__ = init_patched

        jpDB = Japanese_DB_handler()
        jpDB.generateDB()

    def tearDown(self) : 
        jpDB = Japanese_DB_handler()
        del(jpDB)
        gc.collect()
        for path in [japanese_db_path] : 
            if os.path.exists(path) :
                os.remove(path)

    def test_add_categories_tags_kanjis(self) : 

        # TO DO : WESH UN STATUS OU BIEN ?

        jpDB = Japanese_DB_handler()
        
        cat_list = ('cat_1', 'cat_2', 'cat_3')
        jpDB.add_categories(*cat_list)
        cat_in_DB = jpDB.list(jpDB.base_format.categories , jpDB.base_format.categories.name)
        self.assertEqual(set(cat_list), set(cat_in_DB))

        jpDB.add_tags('tag_1', 'tag_2')
        jpDB.add_tags('tag_3', 'tag_2')
        jpDB.add_tags('tag_1')

        tag_set = {'tag_1', 'tag_2', 'tag_3'}
        self.assertEqual(set(tag_in_DB), tag_set)

        jpDB.add_kanjis('kanji_1', 'kanji_2', 'kanji_2')
        kanjis_set = {'kanji_1', 'kanji_2'}
        kanjis_in_DB = jpDB.list(jpDB.base_format.kanjis, jpDB.base_format.kanjis.name)
        self.assertEqual(set(kanjis_in_DB), kanjis_set)


        print('pppppppp')

    def test_add_vocab(self) : 
        jpDB = Japanese_DB_handler() 
        jpDB.add_categories(*cat_list)
        jpDB.add_tags(*tag_list)
        print('pppppppppp')
        jpDB.add_vocab(*japanese_vocab)




if __name__ == '__main__': unittest.main()