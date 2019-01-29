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

def check_baseType(baseName) :
	if baseName not in base_format.keys():
		log.error("base :"+baseName+" not existing.")
		return False
	return True


class Singleton(type) :

    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DB_handler(metaclass=Singleton):
		

	def __init__(self, db_path = ''):
	 
		if not db_path : 
			config_data = configuration.getConfiguration()		
			if not config_data : return None 
			db_path = config_data.get('kioku', 'db_path')
		if not os.path.exists(db_path):
			log.critical("DB not found on "+db_path)
			return None
		self.db_path = db_path
		self.kiokuDB = sqlite3.connect(db_path)


	def __del__(self):

			self.kiokuDB.commit()
			self.kiokuDB.close()
			del(self.kiokuDB)
			self._instances = {}

	# Public method ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

	def select(self, base, *itemToGet, **conditions):
		if not self._check_select(base, *itemToGet, **conditions):
			return None
		data = self._req_select(base, *itemToGet, **conditions)
		if data == None :
			log.error("error selecting"+selector+" from base "+base)
			return
		return data


	def count(self, base, **conditions):
		r = self._req_select(base, **conditions)
		return r[0][0]


	def add(self, base, *dataList):

		for data in dataList :
			if base == "vocab" : 
				now = datetime.datetime.now()
				data += (str(now.year)+'.'+str(now.month)+'.'+str(now.day)+'.'+str(now.hour)+':'+str(now.minute),)
			if not self._check_entry(base, data):
				log.error("failed adding to base "+base+" data : "+str(data))
				return None
			self._req_add(base, *data)
		self.kiokuDB.commit()


	# checkers ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


	def _check_entry(self, base, row) :
		if not check_baseType(base): return False
		expected_len = len(base_format[base])
		given_len = len(row)
		if expected_len != given_len: 
			log.error("format not matching, expected: "+str(expected_len) + " got: "+str(given_len))
			return False
		return True

	def _check_select(self, base, *itemToGet, **conditions):
		if not check_baseType(base): return False
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
			if result == None:
				return
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
		if conditions :
			sqlrequest += " WHERE "
			for condition_id, condition_value in conditions.items() : 
				sqlrequest += condition_id + "='"+condition_value + "' AND "
			sqlrequest = sqlrequest[:-5]
		return sqlrequest


	@sqlR
	def _req_add(self, base, *dataList):

		if not check_baseType(base): return None
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

	def _req_del(self, base, **conditions): 

		if not check_baseType(base): return None
		sqlrequest = "DELETE FROM "+base
		if conditions : 
			sqlrequest += " WHERE "
			#for condition








