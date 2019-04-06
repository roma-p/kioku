import os, datetime, logging, configparser
import sqlite3
import functools
import kioku.helpers as helpers
import kioku.DB.database_format_register as r
from kioku.DB.DB_format import DB_format
from collections import defaultdict
from weakref import WeakValueDictionary
log = logging.getLogger() 


class Singleton(type) :

    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # This variable declaration is required to force a
            # strong reference on the instance.
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DB_handler(metaclass=Singleton):
        

    def __init__(self, db_path, base_format):

        self.kiokuDB = None     
        if not os.path.exists(db_path):
            log.warning("DB not found on "+db_path)
        else : 
            self.kiokuDB = sqlite3.connect(db_path)
        try : 
            self.base_format = DB_format('format', **base_format)
        except ValueError: 
            log.error('error in DB format : could not init DB_handler')
            raise ValueError
        self.db_path = db_path

    def __del__(self):

            self.kiokuDB.commit()
            self.kiokuDB.close()
            del(self.kiokuDB)

    # Public method ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

    # TODO : SUPPORT INNER JOINT... Select with where statement
    # select with INNER JOIN / LEFT JOIN STATEMENT. 
    def select(self, table, *itemToGet, **conditions):

        itemToGet, conditions = _formatData(*itemToGet, **conditions)
        table = _getDataElementName(table)

        if not self._check_select(table, *itemToGet, **conditions):
            return None
        data = self._req_select(table, *itemToGet, **conditions)
        if data == None :
            log.error("error selecting"+selector+" from table "+table)
            return
        return data

    def list(table, fieldToGet, **conditions) :
        _tmp, conditions = _formatData(table, fieldToGet, **conditions)
        table, fieldToGet = _tmp
        data = self.select(table, fieldToGet, **conditions)
        treated_data = [singleData[0] for singleData in data]
        return tuple(treated_data)

    def count(self, table, **conditions):
        _tmp, conditions = _formatData(table, **conditions)
        table = _tmp[0]
        r = self._req_select(table, **conditions)
        return r[0][0]

    def add(self, table, dataOrder, *dataList):

        """
        add data to the given table.
        : parameter table : name of the table to add data to. 
        : parameter dataOrder : tuple of the name of the row 
                                which data zill be added to, in the 
                                order of the data of <dataList>
        : parameter dataList : list of tuple of data to add to the base
                                in the order described in dataOrder.
        """
        table = _getDataElementName(table)
        dataOrder, _ = _formatData(*dataOrder)

        fieldList = self.base_format.list_field_names(table)
        if not fieldList : return None

        missing= [rowName for rowName in dataOrder if rowName not in fieldList] 
        if len(missing) : 
            log.error('unknown row name for table '+table+' :'+str(missing))
            return None

        now_str = ''
        if r.date() in fieldList : 
            now_str = helpers.format_now()
            dataOrder+= (r.date(),)
            _dataList = []
            for data in dataList : 
                data += (now_str,)
                _dataList.append(data)
            dataList = _dataList

        for data in dataList :
            if len(data) != len(dataOrder) : 
                log.error("failed adding to table "+table+" data : "+str(data) + "as "+str(dataOrder)+', too few or not enough data.')
                return None
            self._req_add(table, dataOrder, *data)
        self.kiokuDB.commit()

    def delete(self, table, **conditions):
        _tmp, conditions = _formatData(table, **conditions)
        table = _tmp[0]
        self._req_del(table, **conditions)
        self.kiokuDB.commit()

    def replace(self, table, fieldReplaced, originalValue, newValue, **conditions): 
        _tmp, conditions = _formatData(table, fieldReplaced, **conditions)
        table, fieldReplaced = _tmp
        conditions[fieldReplaced] = originalValue
        self._req_update(table, fieldReplaced, newValue, **conditions)
        self.kiokuDB.commit()

    def update(self, table, updated_field, updated_value, **conditions): 
        _tmp, conditions = _formatData(table, updated_field, **conditions)
        table, updated_field = _tmp     
        self._req_update(table, updated_field, updated_value, **conditions)
        self.kiokuDB.commit()

    def execute(self, queryObject) : 
        if not self._check_query_object(queryObject) : 
            return None
        return self._req_execute_query(queryObject)


    # checkers ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def _check_select(self, tableName, *itemToGet, **conditions):
        
        fieldList = self.base_format.list_field_names(tableName)
        if not fieldList : return False
        shallExist = list(itemToGet) + list(conditions.keys())
        missing = [item for item in shallExist if item not in fieldList]
        if len(missing)>0 : 
            log.error("missing row in base "+tableName+" :"+str(missing))
            return False
        return True

    def _check_query_object(self, queryObject) : 
        missingTables = []
        missingFields = defaultdict(list)

        db_tables_list = self.base_format.list_tables_names()

        for table, fieldList in queryObject.get_shall_exit_tables_fields().items() : 
            if table not in db_tables_list: 
                missingTables.append(table)
            else : 
                db_fields_list = self.base_format.list_field_names(table)
                for field in fieldList : 
                    if field not in db_fields_list : 
                        missingFields[field].append(field)
        status = True
        if missingTables : 
            log.error('tables in query not existing in database.')
            for table in missingTables : 
                log.error('table not found in database : ' + str(table))
            status = False
        if missingFields : 
            log.error('fields in query not existing in database.')
            for table, fieldList in missingFields.items() : 
                log.error('missing fields :' + ', '.join(fieldList) + ' in table ' + table)
            status = False
        return status

    # executing request  ''''''''''''''''''''''''''''''''''''''''''''''''''''''


    def sqlR(func):
        @functools.wraps(func)
        def executing_R(self, tableName, *args, **kwargs):
            result = func(self, tableName, *args, **kwargs)
            if result == None:return
            cursor = self.kiokuDB.cursor()
            cursor.execute(result)
            r =  cursor.fetchall()
            return tuple(r)
        return executing_R

    @sqlR
    def _req_select(self, table, *itemToGet, **conditions):
        
        if itemToGet == () : 
            selector= "COUNT(*)"
        else : 
            selector = ''
            for item in itemToGet : selector+= item +', '
            selector = selector[:-2]+' '
        sqlrequest = "SELECT " + selector + " FROM " + table
        if conditions : sqlrequest += self._format_conditions(**conditions)
        return sqlrequest

    @sqlR
    def _req_add(self, table, dataOrder, *dataList):

        # handling pottential sql syntax error due to tuple of len 1 
        str_data = []
        for pottential_single_tuple in [dataOrder, dataList] : 
            if len(pottential_single_tuple) == 1 : 
                str_data.append(str(pottential_single_tuple).replace(',', ''))
            else : 
                str_data.append(str(pottential_single_tuple))

        sqlrequest = "INSERT INTO "+table+str_data[0]+" VALUES "+str_data[1]
        return sqlrequest

    @sqlR
    def _req_del(self, table, **conditions): 

        if table not in self.base_format.list_tables_names() : return None
        sqlrequest = "DELETE FROM "+table
        if conditions : sqlrequest += self._format_conditions(**conditions)
        return sqlrequest

    @sqlR
    def _req_update(self, table, updated_field, updated_value, **conditions): 

        fieldList = self.base_format.list_field_names(table)
        if not fieldList : return None
        if updated_field not in fieldList : return None
        sqlrequest = "UPDATE " + table + " SET " + updated_field + " = '" + updated_value+"'"
        if conditions : sqlrequest += self._format_conditions(**conditions)
        return sqlrequest

    @sqlR
    def _req_execute_query(self, queryObject) : 
        return queryObject()

    def _format_conditions(self, **conditions) : 
        condition_str = " WHERE "
        for condition_id, condition_value in conditions.items() : 
            if not condition_value : condition_value = 'NULL'
            condition_str += condition_id + "='"+condition_value + "' AND "
        condition_str = condition_str[:-5]
        return condition_str

    # generate DB  ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def generateDB(self) : 

        #self.kiokuDB.close()

        dbName = self.db_path.split('/')[-1]
        dirPath = self.db_path.split(dbName)[0]
        if not os.path.exists(dirPath):
            log.error('path not found :' + dirPath)
            return False
        elif os.path.exists(self.db_path):
            log.error('Database already exists :' + self.db_path)
            return False

        log.info('generating new empty kioku db.')
        self.kiokuDB = sqlite3.connect(self.db_path)
        cursor = self.kiokuDB.cursor()

        # TODO  TRY CATCH <<< 
        for table in self.base_format.list_tables(): 
            cursor.execute(self._generateDB(table))

        self.kiokuDB.commit()

        return True

    
    def _generateDB(self, table) : 

        command = 'CREATE TABLE IF NOT EXISTS '+table()+'('
        for field in table.list_field(): 
            command+=  field() + ' ' + field.fieldType+' '
            if field.key : 
                command += field.key + ' ' 
            if field.constraints : 
                for constraint in field.constraints : 
                    command += constraint+' '
            command = command[:-1] + ', '
        command = command[:-2] + ')'
        return command 

# *****************************************************************************

def _getDataElementName(object) : 
    '''
    if object is a string, return string,
    othewise return the output of the its __call__ : 
    intented to be use for Table / Field objects of DB_format
    which returns their _name parameter when called. 
    '''
    if isinstance(object, str) : return object
    else : return object()

def _formatData(*tablesAndFields, **conditions) :
    r_tablesAndFields = tuple([_getDataElementName(item) for item in tablesAndFields])
    if conditions : 
        r_conditions = {_getDataElementName(key) : value 
                            for key, value in conditions.items()}
    else : r_conditions = {}
    return r_tablesAndFields, r_conditions

