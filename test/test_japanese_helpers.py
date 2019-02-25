import unittest, logging
from context import kioku
from kioku import japanese_helpers

logging.basicConfig()

log = logging.getLogger()
log.setLevel(logging.DEBUG)

hiragana_list = ['こ', 'ご', 'さ', 'ざ', 'し', 'じ']
katakana_list = ['ッ', 'ツ', 'ヅ', 'テ', 'デ', 'ト']
kanjis_list = ['偀', '偁', '偂', '偃', '偄', '偅']

mixed_kanjis_kana = '注目の有料ニュース'
mixed_kana = 'ベトナムから'

pronciation_core = {
	'がっこう' : 'かこ',
}

class Testjapanese_helpers(unittest.TestCase): 

	def test_characterType(self) : 
		for character in hiragana_list : 
			self.assertTrue(japanese_helpers.is_hiragana(character))
			self.assertFalse(japanese_helpers.is_katagana(character))
			self.assertFalse(japanese_helpers.is_kanjis(character))
		for character in katakana_list : 
			self.assertFalse(japanese_helpers.is_hiragana(character))
			self.assertTrue(japanese_helpers.is_katagana(character))
			self.assertFalse(japanese_helpers.is_kanjis(character))
		for character in kanjis_list : 
			self.assertFalse(japanese_helpers.is_hiragana(character))
			self.assertFalse(japanese_helpers.is_katagana(character))
			self.assertTrue(japanese_helpers.is_kanjis(character))

	def test_list_kanjis(self) : 
		kanjis_list = japanese_helpers.list_kanjis(mixed_kanjis_kana)
		self.assertEqual(kanjis_list, ('注','目','有','料'))

	def test_convertKanatToHiragana(self): 
		self.assertIsNone(japanese_helpers.convertKanaToHiragana(mixed_kanjis_kana))
		self.assertEqual(japanese_helpers.convertKanaToHiragana(mixed_kana), 'べとなむから')

	def test_gen_core_prononciation(self) : 
		for real_prononciation, core_prononciation in pronciation_core.items() : 
			self.assertEqual(japanese_helpers.gen_core_prononciation(real_prononciation), core_prononciation)

if __name__ == '__main__':
    unittest.main()