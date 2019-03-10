from kioku.DB.DB_handler import DB_handler
from kioku import japanese_dataBaseFormat
import kioku.configuration as configuration

class  Japanese_DB_handler(DB_handler):

	def __init__(self, arg):

		config_data = configuration.getConfiguration()		
		if not config_data : return None 
		db_path = config_data.get('kioku', 'db_path')
		base_format = japanese_dataBaseFormat.get_baseFormat()
		super().__init__(db_path, base_format)


