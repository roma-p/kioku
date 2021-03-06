import logging
import DB.database_format_register as r
log = logging.getLogger() 

class DB_format():
    """
    
    ****************

    DB Format is used to describe the format of an SQLite database. 
    The object can eihter be constructed by a dictionnay describing format, or created empty. 
    DB Format can be updated after creation : tables / fields can be added / modified / removed. 

    DB Format object is used by DB_Handler class to : 

    - generate / maintain database
    - check sql queries validity before execution 
    - provide easy to use description of the database for the user.

    DB Fromt object is used by Query class to  construct sql queries. 

    DB Format input dictionnary format example below. 
    certain keys of this dictionnary are fixed in kioku.DB.database_format_register: 
    
    - the different supported type
    - the different supported keys 
    - the different supported constraints
    - couple of other stuff such as 'version', 'id' ... see database_format_registers

    ****************

    import kioku.DB.database_format_register as r

    db_input_example = {
        'table_1' : {
            r.id() : True, 
            r.date() : True, 
            'field_1_1' : {
                r.type() : r.type_text(), 
                r.constraints() : (r.constraints_unique(), r.constraints_not_null())
            },
            'field_1_2' : {
                r.type() : r.type_integer() 
            }   
        }
        'table_2 : {
            r.id() : True, 
            'field_2_1' : {
                r.type() : r.type_integer()
            },
            'field_2_2' : {
                r.type() : r.type_integer()
            },
            r.key_foreign() : {
                'field_2_1' : ('table_1', 'id'),
                'field_2_2' : ('table_1', 'table_1_2') 
            }
        }, 
        'version' : 1.0
    }

    ****************


    notes on this example : 

    1) setting r.id() True on a table automatically declare an index as such : 
    
    r.id() = {
        r.type() : r.type_integer(), 
        r.key() : r.key_primary(), 
        r.constraints() : {r.constraints_autoincrement(), r.constraints_unique()}
    }

    2) setting r.date() True on a table automatically declare a date field as such : 
    
    r.date() = {
        r.type =  r.type_text()
    }

    ****************

    For a complete example of DB_format dictionnary, see : 
    kioku.japanese.japanese_dataBaseFormat.py

    ****************

    DB_handler automatically modified its attributes, 
    Every table / field object data is accessible as such : 

    dbf = DB_format('test', db_input_example)
    dbf.table_1.list_field() # return every field object.
    dbf.table_1() # calling the table itself returns its name : 'table_1'
    dbf.table_1.field_1_1.fieldType # return 'INTEGER' (as its the value of r.type_interger())
    dbf.table_1.field_1_2() # same behaviour as Table object : return field name : 'field_1_2'


    """
    def __init__(self, dbFormatName, **dbFormatDict):
        
        self.dbFormatName = dbFormatName
        self._version = 0
        self._tableList = [] 
        # list of tubple  (<table name>, <table field>) that shall exist for foreign keys to be relevant
        # usedto check overall consistency, when constructing data format using dictionnary
        self._shallExist = []

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

    @property
    def version(self) : return self._version

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

    def get_field(self, tableName, fieldName) :
        table = self.get_table(tableName)
        if not table : 
            log.error('non existing table '+tableName+' has no field '+fieldName)
            return None
        field_match_list = [field for field in table.list_field() if field() == fieldName]
        len_list = len(field_match_list)
        if not len_list : 
            log.error('no field "'+fieldName+'" found in '+table())
            return None
        elif len_list > 1 : 
            log.error('multiple fields ('+str(len_list)+') with same name found in '+field())
            return None
        else : 
            return field_match_list[0]

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

    def add_foreign_key(self, child_table, child_field, parent_table, parent_field) : 
        table = self.get_table(child_table)
        if not table : 
            log.error("could'nt add foreign key on non existing table "+child_table)
            return False
        self._add_data_shall_exists(parent_table, parent_field)
        self._add_data_shall_exists(child_table, child_field)
        foreign_key = ForeignKey(child_field, parent_table, parent_field)
        table.add_foreign_key(foreign_key)
        return True

    def _gen_db_format_from_dict(self, dataBaseData) :

        for tableName, tableData in dataBaseData.items() :
            if tableName ==  r.version() :
                self._version = tableData
            else :  
                fieldNames = [key for key in tableData.keys() if key not in (r.id(), r.date(), r.key_foreign())]
                for fieldName in fieldNames : 
                    if not Field.check_field_as_dict(fieldName, tableData[fieldName]) : 
                        log.error('errors on field description, aborting')
                        return False
                _id = tableData[r.id()] if r.id() in tableData.keys() else False
                _date = tableData[r.date()] if r.date() in tableData.keys() else False
                s = self.add_table(tableName, _id, _date)
                if not s : 
                    log.error('error creating table '+tableName)
                    return False
                for fieldName in fieldNames : 
                    fieldData = tableData[fieldName]
                    _type = fieldData[r.type()]
                    key = fieldData[r.key()] if r.key() in fieldData.keys() else None
                    constraints = fieldData[r.constraints()] if r.constraints() in fieldData.keys() else ()
                    s = self.add_field(tableName, fieldName, _type, key, *constraints)
                    if not s : 
                        log.error('error creating field '+ fieldName+' in table '+tableName)
                        return False
                if r.key_foreign() in tableData.keys() : 
                    for child_field, (parent_table, parent_field) in tableData[r.key_foreign()].items() : 
                        s = self.add_foreign_key(tableName, child_field, parent_table, parent_field)
                        if not s : 
                            log.error('error creating foreign keys  constraints on table '+tableName)
                            return False
        status = self._check_shall_exist()
        return status

    def _add_data_shall_exists(self, tableName, fieldName) :
        self._shallExist.append((tableName, fieldName))

    def _check_shall_exist(self) : 
        missing_fields = []
        for (tableName, fieldName) in self._shallExist : 
            field = self.get_field(tableName, fieldName)
            if not field : 
                missing_fields.append((tableName, fieldName))
        if missing_fields : 
            log.error('some foreign keys are referencing non existing table/fields')
            return False
        return True

class Table(): 

    def __init__(self, tableName, _id = False, _date = False):
        self._name = tableName
        self._fieldList = []
        self._foreignKeyList = []
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
            field = Field(fieldName, fieldType, key, constraints, parent_table = self)
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

    def add_foreign_key(self, foreign_key) : 
        self._foreignKeyList.append(foreign_key)

    def list_field(self) : return tuple(self._fieldList)
    def list_field_names(self) : return tuple([field() for field in self._fieldList])
    def list_foreign_keys(self) : return tuple(self._foreignKeyList)

    def get_field(self, fieldName) : 
        field_match_list = [field for field in self.list_field() if field() == fieldName]
        len_list = len(field_match_list)
        if not len_list : 
            log.error('no field "'+fieldName+'" found in '+table())
            return None
        elif len_list > 1 : 
            log.error('multiple fields ('+str(len_list)+') with same name found in '+field())
            return None
        else : 
            return field_match_list[0]


class Field(): 

    # MAGIC METHODS '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def __init__(self, fieldName, fieldType, key=None, constraints = (), parent_table = None):
        if not Field._checkFieldData(fieldType, key, constraints) : 
            log.error("could'nt construct Field object "+fieldName)
            raise ValueError()

        self._name = fieldName
        self._fieldType = fieldType
        self._key = key
        self._constraints = constraints
        self._parent_table = parent_table

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
    @property
    def parent_table(self) : return self._parent_table

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

class ForeignKey(): 
    def __init__(self, child_field, parent_table, parent_field):
        self._child_field = child_field
        self._parent_table = parent_table
        self._parent_field = parent_field

    def __call__(self) : 
        return True

    # PROPERTIES ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    @property
    def child_field(self) : return self._child_field
    @property
    def parent_table(self) : return self._parent_table
    @property
    def parent_field(self) : return self._parent_field


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


