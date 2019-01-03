import os 
import logging
import sqlite3
import functools
log = logging.getLogger() 

base_format = {
	"vocab" : ('categorie','tag','word','prononciation','meaning','exemple'),
	"categorie" : ("name"),
	"tag" : ("name")
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
		
	def __init__(self, path_DB):
		if not os.path.exists(path_DB):
			log.critical("DB not found on "+path_DB)
			return None
		self.kiokuDB = sqlite3.connect(path_DB)

	def __del__(self):
			self.kiokuDB.commit()
			self.kiokuDB.close()
			del(self.kiokuDB)

	def select(self, selector, base, *itemToGet, **condition):
		r = _req_select(selector, base, **condition)
		if r == None :
			log.error("error selecting"+selector+" from base "+base)
			return
		cursor = self.kiokuDB.cursor()
		data_to_fetch = [i for i,data in enumerate(base_format[base]) if data in itemToGet]
		_data = [[row[i] for i in data_to_fetch] for row in cursor.fetchall()]
		if len(data_to_fetch) ==1 : data = [item[0] for item in _data]
		else : data = _data
		return data

	def count(self, base, **condition):
		_req_select(None, base, condition)
		cursor = self.kiokuDB.cursor()
		return cursor.fetchone()[0]

	def add(self, base, *dataList):
		for formatted_data in (self.format_entry(base, row) for row in dataList):
			print(base)
			print(formatted_data)
			self._req_add(base, **formatted_data)
		self.kiokuDB.commit()

	def sqlR(func):
		@functools.wraps(func)
		def executing_R(self, base, *args, **kwargs):
			result = func(self, base, *args, **kwargs)
			if result == None:
				return
			cursor = self.kiokuDB.cursor()
			if isinstance(result, tuple):
				str_request, data_request = result
				cursor.execute(str_request, data_request)
			elif isinstance(result, str): 
				cursor.execute(result)
			return result
		return executing_R

	@sqlR
	def _req_select(self, selector, base, **condition):
		if selector == "" : 
			selector= "COUNT(*)"
		sqlrequest = "SELECT " + selector + " FROM " + base
		if condition :
			sqlrequest += "WHERE "+condition.keys()[0] + "="+condition.values()[0]
		return sqlrequest

	@sqlR
	def _req_add(self, base, **formatted_data):
		print(base)
		if not check_baseType(base): return None
		if base not in base_format.keys():
			log.error("base :"+base+"not found.")
		sqlrequest = "INSERT INTO "+base+str(base_format[base])+" VALUES "+str(tuple([":"+item for item in base_format[base]]))
		print(sqlrequest)
		return sqlrequest, formatted_data


	def format_entry(self, base, row) :
		if not check_baseType(base): return None
		expected_len = len(base_format[base])
		given_len = len(row)
		if expected_len != given_len: 
			log.error("format not matching, expected: "+str(expected_len), "got: "+given_len)
			return None
		formatted_data = {key : value for key, value in zip(base_format[base], row)}
		return formatted_data






