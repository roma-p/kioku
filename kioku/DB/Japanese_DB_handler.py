from kioku.DB.DB_handler import DB_handler
from kioku import japanese_dataBaseFormat

class  Japanese_DB_handler(DB_handler):

	def __init__(self, arg):
		super().__init__(arg)
		self.base_format = japanese_dataBaseFormat.baseFormat()


