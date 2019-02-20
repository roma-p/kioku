import os, datetime, logging, configparser
import sqlite3
import functools
import kioku.configuration as configuration
log = logging.getLogger() 

base_format = {
	"vocab" : ('categorie','tag','word','prononciation','meaning','exemple','date'),
	"categorie" : (("name",)),
	"tag" : (("name",))
	}


def check_table(tableName) :
	if tableName not in base_format.keys():
		log.error("base :"+tableName+" not existing.")
		return False
	return True


class Singleton(type) :

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB_handler(metaclass=Singleton):
		

	def __init__(self, db_path = '', base_format = None):
	 
		if not db_path : 
			config_data = configuration.getConfiguration()		
			if not config_data : return None 
			db_path = config_data.get('kioku', 'db_path')
		if not os.path.exists(db_path):
			log.critical("DB not found on "+db_path)
			return None
		self.base_format = base_format
		self.db_path = db_path
		self.kiokuDB = sqlite3.connect(db_path)



	def __del__(self):

			self.kiokuDB.commit()
			self.kiokuDB.close()
			del(self.kiokuDB)
			self._instances = {}

	# Public method ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

	def select(self, table, *itemToGet, **conditions):
		if not self._check_select(table, *itemToGet, **conditions):
			return None
		data = self._req_select(table, *itemToGet, **conditions)
		if data == None :
			log.error("error selecting"+selector+" from table "+table)
			return
		return data


	def list(table, fieldToGet, **conditions) : 
		data = self.select(table, fieldToGet, **conditions)
		treated_data = [singleData[0] for singleData in data]
		return tuple(treated_data)


	def count(self, table, **conditions):
		r = self._req_select(table, **conditions)
		return r[0][0]


	def add(self, table, *dataList):

		for data in dataList :
			if table == "vocab" : 
				now = datetime.datetime.now()
				data += (str(now.year)+'.'+str(now.month)+'.'+str(now.day)+'.'+str(now.hour)+':'+str(now.minute),)
			if not self._check_entry(table, data):
				log.error("failed adding to table "+table+" data : "+str(data))
				return None
			self._req_add(table, *data)
		self.kiokuDB.commit()


	def delete(self, table, **conditions): 
		self._req_del(table, **conditions)
		self.kiokuDB.commit()


	def replace(self, table, fieldReplaced, originalValue, newValue, **conditions): 
		conditions[fieldReplaced] = originalValue
		self._req_update(table, fieldReplaced, newValue, **conditions)
		self.kiokuDB.commit()


	def update(self, table, updated_field, updated_value, **conditions): 
		self._req_update(table, updated_field, updated_value, **conditions)
		self.kiokuDB.commit()


	# getter ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def list_tables(self) : 
		return self.base_format.keys()

	def list_rows(self, tableName) : 
		if tableName not in self.base_format.keys() : 
			log.error('no table "'+tableName+'" found.')
			return None
		else : 
			return self.base_format[tableName].keys()


	# checkers ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	def _check_entry(self, base, row) :
		if not check_table(base): return False
		expected_len = len(base_format[base])
		given_len = len(row)
		if expected_len != given_len: 
			log.error("format not matching, expected: "+str(expected_len) + " got: "+str(given_len))
			return False
		return True

	def _check_select(self, base, *itemToGet, **conditions):
		if not check_table(base): return False
		shallExist = list(itemToGet) + list(conditions.keys())
		missing = [item for item in shallExist if item not in base_format[base]]
		if len(missing)>0 : 
			log.error("missing row in base "+base+" :"+str(missing))
			return False
		return True


	# executing request  ''''''''''''''''''''''''''''''''''''''''''''''''''''''


	def sqlR(func):
		@functools.wraps(func)
		def executing_R(self, base, *args, **kwargs):
			result = func(self, base, *args, **kwargs)
			if result == None:return
			cursor = self.kiokuDB.cursor()
			cursor.execute(result)
			r =  cursor.fetchall()
			return tuple(r)
		return executing_R



	@sqlR
	def _req_select(self, base, *itemToGet, **conditions):
		
		if itemToGet == () : 
			selector= "COUNT(*)"
		else : 
			selector = ''
			for item in itemToGet : selector+= item +', '
			selector = selector[:-2]+' '
		sqlrequest = "SELECT " + selector + " FROM " + base
		if conditions : sqlrequest += self._format_conditions(**conditions)
		return sqlrequest


	@sqlR
	def _req_add(self, base, *dataList):

		if not check_table(base): return None
		if base not in base_format.keys():
			log.error("base :"+base+"not found.")

		# handling pottential sql syntax error due to tuple of len 1 
		str_data = []
		for pottential_single_tuple in [base_format[base], dataList] : 
			if len(pottential_single_tuple) == 1 : 
				str_data.append(str(pottential_single_tuple).replace(',', ''))
			else : 
				str_data.append(str(pottential_single_tuple))
		sqlrequest = "INSERT INTO "+base+str_data[0]+" VALUES "+str_data[1]
		return sqlrequest


	@sqlR
	def _req_del(self, base, **conditions): 

		if not check_table(base): return None
		sqlrequest = "DELETE FROM "+base
		if conditions : sqlrequest += self._format_conditions(**conditions)
		return sqlrequest

	@sqlR
	def _req_update(self, base, updated_field, updated_value, **conditions): 

		if not check_table(base): return None
		if updated_field not in base_format[base] : return None
		sqlrequest = "UPDATE " + base + " SET " + updated_field + " = '" + updated_value+"'"
		if conditions : sqlrequest += self._format_conditions(**conditions)
		return sqlrequest


	def _format_conditions(self, **conditions) : 
		condition_str = " WHERE "
		for condition_id, condition_value in conditions.items() : 
			condition_str += condition_id + "='"+condition_value + "' AND "
		condition_str = condition_str[:-5]
		return condition_str


	# generate DB  ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def generateDB(self) : 
		dbName = self.db_path.split('/')[-1]
		dirPath = self.db_path.split(dbName)[0]
		if not os.path.exists(dirPath):
        	log.error('path not found :' + dirPath)
        	return False
		elif os.path.exists(self.db_path):
        	log.error('Database already exists :' + self.db_path)
        	return False

	    log.info('generating new empty kioku db.')
    	kioku = sqlite3.connect(self.db_path)
    	cursor = kioku.cursor()

    	# TODO  TRY CATCH <<< 
    	for tableName, tableData in self.base_format.items(): 
    		cursor.execute(self._generateDB(tableName, tableData))
    	return True

    def _generateDB(self, tableName, tableData) : 

    	command = 'CREATE TABLE IF NOT EXISTS '+tableName+'('
    	for field_name, field_data in tableData.items(): 
    		command+=  field_name + ' ' + field_data['type']
    		if key in field_data.keys() : 
    			command += field_data['key']
    		if constraints in field_data['keys'] : 
    			for constraint in constraints : 
    				command += constraint
    	return command 


