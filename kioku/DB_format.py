import logging
import database_format_register as r
log = logging.getLogger() 

class DB_format():
	"""docstring for DB"""
	def __init__(self, dbFormatName, **dbFormatDict):
		
		self.dbFormatName = dbFormatName
		self.tableDict = {}
		
		if dbFormatDict : 
			s = self._gen_db_format_from_dict(dbFormatDict)
			if not s : raise ValueError()

	def add_table(tableName, id = False, date = False) : 
		if tableName in tableDict.keys() : 
			log.error(tableName ' table already exists in DB format: ' + self.dbFormatName)
			return False
		table = Table(tableName, id, date)
		tableDict[tableName] = table
		add_attr_to_class(cls, table, tableName)
		return True

	def add_field(tableName, fieldName, fieldType, key = None, *constraints) : 
		if tableName not in self.tableDict.keys() : 
			log.error('no table '+tableName+'in db format '+self.dbFormatName)
			return False
		s = self.tableDict[tableName].add_field(fieldName, fieldType, key, constraints)
		return s 

	def add_fields(tableName, *fieldData) : 
		if tableName not in self.tableDict.keys() : 
			log.error('no table '+tableName+'in db format '+self.dbFormatName)
			return False
		global_status = True
		table = self.tableDict[tableName]
		for singleFieldData in fieldData : 
			s = table.add_field(fieldData)
			if not s : 
				log.error('error adding field : '+str(singleFieldData))
				global_status = False
		return global_status

	def _gen_db_format_from_dict(self, dataBaseData) :
		for tableName, tableData in dataBaseData.items() : 
			fieldNames = [key for key in tableData.keys() if key not in (r.id(), r.date())]
			if not Field.check_field_as_dict(fieldName, tableData[fieldName]) : 
				log.error('erros on field description, aborting')
				return False
			
			_id = tableData[r.id()] if r.id() in tableData.keys() else False
			_date = tableData[r.date()] if r.date() in tableData.keys() else False
			s = self.add_table(tableName, _id, _date)
			
			if not s : return False

			for field in fieldNames : 
				fieldData = tableData[fieldName]
				s = self.add_field(fieldName, fieldData)
				if not s : return False

		return True


class Table(): 
	def __init__(self, tableName, id = False, date = False):
		self.tableName = tableName
		self._fieldDict = {}

	def add_field(self, fieldName, fieldType, key = None, *constraints) : 
		if fieldName in _fieldDict.keys() : 
			log.error(fieldName ' table already exists in Table: ' + self.tableName)
			return False		
		try : 
			field = Field(fieldName, fieldType, key, constraints)
		except ValueError:
			log.error('error adding field '+fieldName+' on table '+self.tableName)
			return False

		self._fieldDict[fieldName] = field
		add_attr_to_class(cls, field, fieldName)
		return True

	def add_id(self) : 
		self.add_field(r.id(), r.type_integer(), r.key_primary(), r.constraints_autoincrement(), r.constraints_unique())
	def add_date(self) : 
		self.add_field(r.date(), r.type_text())

	def list_field(self) : return self._fieldDict.keys()


class Field(): 

	def __init__(self, fieldName, fieldType, key=None, *constraints):
		if not _checkFieldData(fieldType, key, constraints) : 
			log.error("could'nt construct Field object "+fieldName)
			raise ValueError()

		self.fieldName = fieldName
		self.fieldType = fieldType
		self.key = key
		self.constraints = constraints

	@staticmethod
	def check_field_as_dict(fieldName, fieldData) : 
		keys = fieldData.keys() 
		s1 = True
		s2 = True
		if r.type() not in keys : 
			log.error('missing '+r.type+' for field : '+fieldName)
			s1 = False
		for key in keys : 
			if key not in r.valid_keys() : 
				log.error('unknown field option for '+fieldName+' : '+key)
				s2 = False
		if not s2 : 
			log.info('valid field option are: '+str(r.valid_keys()))
		return s1 and s2

	def _checkFieldData(fieldType, key, *constraints):
		s1 = _check_type(fieldType)
		if not key : s2 = True
		else : s2 = _check_key(key)

		s3 = True
		if constraints : 
			for constraint in constraints : 
				_s = _check_constraints(constraint)
				if not _s : s3 = False
		return s1 && s2 && s3

	def _checkInIterable(value, iterable) : 
		if valueToCheck in iterable : 
			return True
		log.error(value ' not in '+str(iterable))
		return False

	def _check_type(_type) : return _checkInIterable(_type, r.type_list())
	def _check_key(_key) : return _checkInIterable(_key, r.key_list())
	def _check_constraints(_constraints) : return _checkInIterable(_constraints, r.constraints_list())


# *****************************************************************************


def add_attr_to_class(cls, attr, attr_name, attr_doc_strings = None) : 
	attr.__name__ = attr_name 
	if attr_doc_strings : 
		attr.__doc__  = attr_doc_strings
	setattr(cls, attr_name, attr)




