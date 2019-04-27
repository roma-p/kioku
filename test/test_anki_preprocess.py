import unittest, os, gc, logging
from context import kioku
from kioku.anki_preprocess import csv_tag_cat_preprocess

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

testDir = 'test/anki_preprocess/'
original_csv = testDir + 'testJap1.csv'
patched_csv = testDir + 'testJap1_patched.csv'

class TestAnKipreprocess(unittest.TestCase) : 

	def test_list_cat_tag_from_csv(self) : 	
		jap_cat = csv_tag_cat_preprocess.list_cat_tag_from_csv(original_csv)

	def test_patch_cat_tag_csv(self) : 
		correctionDict = {'categories':{'judgment' : {'judgmented'}}}
		csv_tag_cat_preprocess.patch_cat_tag_csv(original_csv, patched_csv, correctionDict)
		jap_cat = csv_tag_cat_preprocess.list_cat_tag_from_csv(patched_csv)


if __name__ == '__main__':
    unittest.main()