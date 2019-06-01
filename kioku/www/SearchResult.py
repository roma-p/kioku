
class SearchResult() : 

	def __init__(self, search_input): 
		self.search_input = search_input
		self.results_by_pertinence = []



class SingleResult() : 

	def __init__(self, result_field, ordered_results): 
		self.result_table = result_table # ex : kanjis, words etc...
		self.ordered_results = ordered_results