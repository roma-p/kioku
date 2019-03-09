import logging
from kioku.japanese import japanese_helpers_data

log = logging.getLogger()

# CHECKING TYPE OF CHARACTER --------------------------------------------------
# *****************************************************************************

def is_cjk(character):
	return any([start <= ord(character) <= end for start, end in
	            [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
	             (63744, 64255), (65072, 65103), (65381, 65500),
	             (131072, 196607)]
	            ])

def is_kanjis(character): return _checking_range(character, unicode_range_kanjis())
def is_hiragana(character) : return _checking_range(character, unicode_range_hiragana())
def is_katagana(character) : return _checking_range(character, unicode_range_katakana())
def is_kana(character) : return is_hiragana(character) or is_katagana(character)

def list_kanjis(word) : 
	return tuple([character for character in word if is_kanjis(character)])

def unicode_range_hiragana() : return 12352, 12447
def unicode_range_katakana() : return 12448, 12543
def unicode_range_kanjis() : return 19968, 40879

def _checking_range(character, range) : 
	return any([start <= ord(character) <= end for start, end in [range]])


# TRANSLATION, OPERATION ON KANAS ---------------------------------------------
# *****************************************************************************

def convertKanaToHiragana(word) : 
	translated_word = [] # TODO : NOT USE A LIST. 
	for character in word : 
		if is_katagana(character) :
			translated_word.append(japanese_helpers_data.katakana_hiragana[character])
		elif is_hiragana(character) : 
			translated_word.append(character)
		else : 
			log.error("can't translate '"+ word +"' to hiragana... words need to be in kana to do so.")
			return None
	return ''.join(translated_word)


# TODO : if u last character, will be bug U, to delete to i guess

def gen_core_prononciation(word) : 
	word = convertKanaToHiragana(word)
	if not word : 
		log.error("could't generate core prononciation of "+word)
	newWord = []
	for character in word : 
		# deleting accentuation 
		if character in japanese_helpers_data.accentation_character : 
			pass
		else : 
			_character = ''
			# geting rid of ten ten. 
			if character in japanese_helpers_data.nigoru_match.keys() : 
				_character = japanese_helpers_data.nigoru_match[character]
			else : _character = character

			# other simplification (shi -> chi / yo,ya,yu)
			if _character in japanese_helpers_data.other_simplification.keys(): 
				newWord.append(japanese_helpers_data.other_simplification[_character])
			else : newWord.append(_character)

	# deleting trailing kanas. 
	if newWord[-1] in japanese_helpers_data.trailing_character : 
		newWord = newWord[:-1]
	return ''.join(newWord)
