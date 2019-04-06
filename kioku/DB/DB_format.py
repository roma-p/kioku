import logging
import kioku.DB.database_format_register as r
log = logging.getLogger() 

class DB_format():
	"""docstring for DB"""
	def __init__(self, dbFormatName, **dbFormatDict):
		
		self.dbFormatName = dbFormatName
		self._tableList = []

		if dbFormatDict : 
			try : 	
				s = self._gen_db_format_from_dict(dbFormatDict)
			except ValueError : 
				s = False
			if not s : 
				raise ValueError()

		# TODO : SHALL UPDATES ITSLEF UPON MODIDIFACTION USING METHODS. 
		# OR just have a version row. 
		self._dbFormatDict = dbFormatDict

	def list_tables(self): return tuple(self._tableList)
	def list_tables_names(self) : return tuple([table() for table in self._tableList])

	def list_field_names(self, tableName) :
		table = self.get_table(tableName)
		if not table : return None
		else : return table.list_field_names() 

	def get_table(self, tableName) : 
		table_match_list = [table for table in self._tableList if table() == tableName]
		len_list = len(table_match_list)
		if not len_list : 
			log.error('no table "'+tableName+'" found in '+self.dbFormatName)
			return None
		elif len_list > 1 : 
			log.error('multiple tables ('+str(len_list)+') with same name found in '+self.dbFormatName)
			return None
		else : 
			return table_match_list[0]

	def add_table(self, tableName, id = False, date = False) : 
		if tableName in self.list_tables_names() : 
			log.error(tableName + ' table already exists in DB format: ' + self.dbFormatName)
			return False
		table = Table(tableName, id, date)
		self._tableList.append(table)
		add_attr_to_instance(self, table, tableName)
		return True

	# TO DO  either tableName or table Object. 
	def add_field(self, _table, fieldName, type, key = None, *constraints) : 

		if isinstance(_table, Table) : table = _table
		elif isinstance(_table, str) : table = self.get_table(_table)
		else : 
			log.error("couldn't resolve type of first argument, shall be Table or str")
			return False
		if table not in self.list_tables() : 
			log.error('no table '+tableName+'in db format '+self.dbFormatName)
			return False
		s = table.add_field(fieldName, type, key, *constraints)
		return s 

	def add_fields(self, tableName, *fieldData) : 
		if tableName not in self.list_tables_names() : 
			log.error('no table '+tableName+'in db format '+self.dbFormatName)
			return False
		global_status = True
		table = self.get_table(tableName)
		for singleFieldData in fieldData : 
			s = table.add_field(fieldData)
			if not s : 
				log.error('error adding field : '+str(singleFieldData))
				global_status = False
		return global_status

	def _gen_db_format_from_dict(self, dataBaseData) :

		for tableName, tableData in dataBaseData.items() : 
			fieldNames = [key for key in tableData.keys() if key not in (r.id(), r.date())]
			for fieldName in fieldNames : 
				if not Field.check_field_as_dict(fieldName, tableData[fieldName]) : 
					log.error('erros on field description, aborting')
					return False
			_id = tableData[r.id()] if r.id() in tableData.keys() else False
			_date = tableData[r.date()] if r.date() in tableData.keys() else False
			s = self.add_table(tableName, _id, _date)
			if not s : return False
			for fieldName in fieldNames : 
				fieldData = tableData[fieldName]
				s = self.add_field(tableName, fieldName, **fieldData)
				if not s : return False
		return True


class Table(): 

	def __init__(self, tableName, _id = False, _date = False):
		self._name = tableName
		self._fieldList = []
		try : 
			if _id : self.add_id()
			if _date : self.add_date()
		except ValueError : 
			log.error('error instanciating table '+self._name)
			raise ValueError

	def __call__(self) : 
		return self._name

	def add_field(self, fieldName, fieldType, key = None, *constraints) : 
		if fieldName in [field() for field in self._fieldList] : 
			log.error(fieldName + ' table already exists in Table: ' + self._name)
			return False		
		try : 
			field = Field(fieldName, fieldType, key, constraints)
		except ValueError:
			log.error('error adding field '+fieldName+' on table '+self._name)
			return False
		self._fieldList.append(field)
		add_attr_to_instance(self, field, fieldName)
		return True

	def add_id(self) : 
		# TO DO : dans register a priori. 
		self.add_field(r.id(), r.type_integer(), r.key_primary(), 
			r.constraints_autoincrement(), r.constraints_unique())
	def add_date(self) : 
		self.add_field(r.date(), r.type_text())

	def list_field(self) : return tuple(self._fieldList)
	def list_field_names(self) : return tuple([field() for field in self._fieldList])

class Field(): 

	# MAGIC METHODS '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	def __init__(self, fieldName, fieldType, key=None, constraints = ()):
		if not Field._checkFieldData(fieldType, key, constraints) : 
			log.error("could'nt construct Field object "+fieldName)
			raise ValueError()

		self._name = fieldName
		self._fieldType = fieldType
		self._key = key
		self._constraints = constraints

	def __call__(self) : 
		return self._name

	# PROPERTIES ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	@property
	def fieldName(self) : return self._name
	@property
	def fieldType(self) : return self._fieldType
	@property
	def key(self) : return self._key
	@property
	def constraints(self) : return self._constraints

	# CHEKER ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

	@staticmethod
	def check_field_as_dict(fieldName, fieldData) : 
		keys = fieldData.keys() 
		s1 = True
		s2 = True
		if r.type() not in keys : 
			log.error('missing '+r.type()+' for field : '+fieldName)
			s1 = False
		for key in keys : 
			if key not in r.valid_keys() : 
				log.error('unknown field option for '+fieldName+' : '+key)
				s2 = False
		if not s2 : 
			log.info('valid field option are: '+str(r.valid_keys()))
		return s1 and s2

	@staticmethod
	def _checkFieldData(fieldType, key, constraints):
		s1 = Field._check_type(fieldType)
		if not key : s2 = True
		else : s2 = Field._check_key(key)

		s3 = True
		if constraints : 
			for constraint in constraints : 
				_s = Field._check_constraints(constraint)
				if not _s : s3 = False
		return s1 & s2 & s3

	def _check_type(_type) : return _checkInIterable(_type, r.type_list())
	def _check_key(_key) : return _checkInIterable(_key, r.key_list())
	def _check_constraints(_constraints) : 
		return _checkInIterable(_constraints, r.constraints_list())


# *****************************************************************************

def _checkInIterable(value, iterable) : 
	if value in iterable : 
		return True
	log.error(str(value)+' not in '+str(iterable))
	return False

def add_attr_to_class(cls, attr, attr_name, attr_doc_strings = None) : 
	attr.__name__ = attr_name 
	if attr_doc_strings : 
		attr.__doc__  = attr_doc_strings
	setattr(cls, attr_name, attr)

def add_attr_to_instance(self, attr, attr_name, attr_doc_strings = None) : 
	attr.__name__ = attr_name 
	if attr_doc_strings : 
		attr.__doc__  = attr_doc_strings
	setattr(self, attr_name, attr)


