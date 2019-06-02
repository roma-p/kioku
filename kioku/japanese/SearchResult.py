
class SearchResult() : 

	def __init__(self, search_input): 
		self.search_input = search_input
		self.results_by_pertinence = []

	def add_search_result(search_result) : 
		self.results_by_pertinence.append(search_result)

	def get_ordered_search_result() : pass

class SingleSearchResult() : 
	def __init__(self, pertience = 3): 
		self.pertinence = pertience

		# 0 : most important
		# 1 : high
		# 2 : medium 
		# 3 : low

class WordSearchResult(SingleSearchResult) : 
	def __init__(self, word, prononciation, meaning, pertience = 3, *kanjis):
		super.__init__(pertience)
		self.word = word 
		self.prononciation = prononciation 
		self.meaning = meaning 
		self.kanjis = kanjis 

class WordListSearchResult(SingleSearchResult) : 
	
	def __init__(self, *approximations_data_list, pertience = 3):
		"""
		approximation_data_list_format : 
			(<word>, <prononciation>, <meaning>)
		"""

		super.__init__(pertience)
		self.approximation_list = self._creating_approximation(*approximations_data_list)

	def _creating_approximation(*approximations_data_list) :
		for (word, prononciation, meaning) in approximations_data_list : 
			word_item = WordItem(word, prononciation, meaning)
			self.approximation_list.append(word_item)

class WordItem() : 
	def __init__(self, word, prononciation, meaning) : 
		self.word = word 
		self.prononciation = prononciation
		self.meaning = meaning

class SelectorResult() : 
	
	valid_selector_type = {
	'categorie', 
	'tag', 
	'core_prononciation', 
	'kanji'
	}

	def __init__(self, selector_type, selector_value, pertience = 3) :
		
		if selector_type not in valid_selector_type : 
			raise ValueError('valid selector types are : ' + set(self.valid_selector_type))
		super.__init__(pertience)
		self.selector_type = selector_type
		self.selector_value = selector_value

