import os, datetime, logging, configparser
import sqlite3
import functools
import helpers as helpers
import DB.database_format_register as r
from DB.DB_format import DB_format
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
        
    """
    DB_handler is a singleton class to handle a sqlite database.

    argument to construct it are : 
    - db_path : path to the sqlite database file. 
    - base_format : an input dictionnary to construct DB_format object
                    (see doc of this class for more info.)

    DB_handler handle the connection to the sqlite database : 
    (storing the result of sqlite3.connect in DB_handler.kiokuDB)

    - If sqlite file given in db_path does exists, it will connect upon creation
    - If not, user can generate the databse using DB_handler.generateDB().
    - The dataase will be created according base_format, and DB_handler will connect to it. 
    - Connection will be close upon destruction of DB_handler (might need to collect gc)
    - foreign keys are enabled by default (can be changed using DB_handler.enable_foreign_keys)

    DB_handler offers services so user doesn't have to manage sqlite library himself
    cursors, commits ... 

    DB_handler provides simple services by itself to : 

    - fetching data using methods :  select(), list(), count()
    - modifying data using : add / delete / replace / update 
    
    all those methods can take **conditions argument, conditions usage is limited,
    passing following dictionnary as **conditions : 
    {'field_1' = 'value_1', 'field_2' : 'value_2', 'field_3' : 'value_3'}
    will generated the following sql query : 
    'WHERE field_1=value_1 AND field_2=value_2 AND field_3=value_3'
    So you can't use OR / != / IN etc... neither construct intracated queries. 

    To process more refined process on DB_handler, user have to construct a Query object
    DB_handler can use Query object to process database using the executeQuery() method. 

    DB_handler.base_format : DB_format object
    DB_handler.kiokuDB : the sqlite object if user needs to perform operation not possible with current services. 
    DB_handler.db_path : path to the sqlite database file.

    for implementation example see : kioku.DB.japanese_DB_handler and unit tests. 

    """    
    def __init__(self, db_path, base_format):

        self.kiokuDB = None     
        if not os.path.exists(db_path):
            log.warning("DB not found on "+db_path)
        else : 
            self.kiokuDB = sqlite3.connect(db_path)
            self.enable_foreign_keys()
        try : 
            self.base_format = DB_format('format', **base_format)
        except ValueError: 
            log.error('error in DB format : could not init DB_handler')
            raise ValueError
        self.db_path = db_path

    # TODO : gc.cllect? why not? can it annoy users? 
    def __del__(self):

            self.kiokuDB.commit()
            self.kiokuDB.close()
            del(self.kiokuDB)

    # Public method ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' 

    def enable_foreign_keys(self, b_ = True) :
        """
        enable or disable foreign keys constraint on database
        :parameter _b : bool, True to enable, False to disable.
        """

        val = 'ON' if b_  else 'OFF'
        command = 'PRAGMA foreign_keys='+val+';'
        cursor = self.kiokuDB.cursor()
        cursor.execute(command) 
        r =  cursor.fetchall()
        self.kiokuDB.commit()   

    def select(self, table, *itemToGet, **conditions):
        """
        fetch data of given fields <itemToGet> on table <tables>
        conditions works as defined in class doc. 

        : param table : either the table name (str) or the DB_format Table object
        : param itemToGet : either field name (str) or DB_format Field object
        : param conditions : keys argument as field name, values as expected value for this field.

        : return : a list of tuple ordered as itemtoGet is. 

        example from unit tests : 
        
        a = db_handler.select("vocab", "word", 'prononciation', categorie = "a_cat", tag = "c_tag")
        a -> (('word_2', 'prononciation_2'),('word_3', 'prononciation_3'))

        """

        itemToGet, conditions = _formatData(*itemToGet, **conditions)
        table = _getDataElementName(table)

        if not self._check_select(table, *itemToGet, **conditions):
            return None
        data = self._req_select(table, *itemToGet, **conditions)
        if data == None :
            log.error("error selecting"+selector+" from table "+table)
            return
        return data

    def list(self, table, fieldToGet, **conditions) :
        """
        list all values of a given field <fieldToGet> of the given table <table>
        conditions works as defined in class doc.

        : param table : either the table name (str) or the DB_format Table object
        : param fieldToGet : either field name (str) or DB_format Field object
        : return : tuple of all values of the field. 

        example from unit tests (for japanese db handler) : 
        categories_tuple = jpDB.list(jpDB.base_format.categories , jpDB.base_format.categories.name)
        categories_tuple -> ('cat_1', 'cat_2', 'cat_3')        

        """

        _tmp, conditions = _formatData(table, fieldToGet, **conditions)
        table, fieldToGet = _tmp
        data = self.select(table, fieldToGet, **conditions)
        treated_data = [singleData[0] for singleData in data]
        return tuple(treated_data)

    def count(self, table, **conditions):
        """
        count rows in table <table> matching <conditions>
        conditions works as defined in class doc.

        : param table : either the table name (str) or the DB_format Table object
        : param conditions : keys argument as field name, values as expected value for this field.
        : return : number (int) of rows

        example from unit tests : 

        a = db_handler.count("vocab", categorie = "a_cat")
        self.assertEqual(a, 2)

        """

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

        example from unit tests : 
        data = [
            ("a_cat", "a_tag", "word_1", "prononciation_1", "a_meaning", "a_exemple"),
            ("a_cat", "c_tag", "word_2", "prononciation_2", "a_meaning", "a_exemple"),
            ("b_cat", "c_tag", "word_3", "prononciation_3", "b_meaning", "b_exemple"),        
        ]
        dataOrder = ('categorie', 'tag', 'word', 'prononciation', 'meaning', 'exemple')
        db_handler.add("vocab", dataOrder, *data)

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
        """
        delete row of a table matching conditions. 
        conditions works as defined in class doc.
        
        : param table : either the table name (str) or the DB_format Table object
        : param conditions : keys argument as field name, values as expected value for this field.
        
        example from unit tests :
        db_handler.delete('vocab', tag = 'e_tag')

        """

        _tmp, conditions = _formatData(table, **conditions)
        table = _tmp[0]
        self._req_del(table, **conditions)
        self.kiokuDB.commit()

    def replace(self, table, fieldReplaced, originalValue, newValue, **conditions): 
        """
        replace every value <originalValue> by <newValue> in the <fieldReplaced> of table <table>
        conditions works as defined in class doc.

        : param table : either the table name (str) or the DB_format Table object
        : param fieldReplaced : either field name (str) or DB_format Field object
        : param originalValue : value to replace, type depends on the type of the field. 
        : param newValue : value to be replaced with, type depends on the type of the field. 
        : param conditions : keys argument as field name, values as expected value for this field.

        example from unit tests :
        db_handler.replace('vocab', 'tag', 'c_tag', 'd_tag')

        """

        _tmp, conditions = _formatData(table, fieldReplaced, **conditions)
        table, fieldReplaced = _tmp
        conditions[fieldReplaced] = originalValue
        self._req_update(table, fieldReplaced, newValue, **conditions)
        self.kiokuDB.commit()


    # TODO : How different from replace method ? 
    def update(self, table, updated_field, updated_value, **conditions): 
        _tmp, conditions = _formatData(table, updated_field, **conditions)
        table, updated_field = _tmp     
        self._req_update(table, updated_field, updated_value, **conditions)
        self.kiokuDB.commit()

    def executeQuery(self, queryObject) : 
        """
        execute sql query based on the Query object : <queryObject> 
        the query that will be executed is queryObject()
        before execution, will perform consistency check with its database format. 
        : param queryObject : Query object. 

        """

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
            try : 
                cursor.execute(result)
            except sqlite3.IntegrityError as err:
                log.error('integrity error in database on request: ')
                log.error(result)
                log.error(err) 
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
            # corrected_pottential_single_tuple = tuple([item if item != None else 'NULL' for item in pottential_single_tuple])
            if len(pottential_single_tuple) == 1 : 
                str_data.append(str(pottential_single_tuple).replace(',', ''))
            else : 
                str_data.append(str(pottential_single_tuple))
        
        str_data[1] = str_data[1].replace("None", "NULL")
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
            condition_str += condition_id + "='"+str(condition_value) + "' AND "
        condition_str = condition_str[:-5]
        return condition_str

    # generate DB  ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def generateDB(self) :

        """
        will generate sqlite database file according DB_handler.base_format at DB_handler.db_path
        If path does not exist, exit. If sqlite file already exists. exit. 

        : return : True / False according success or not of generation. 

        """ 

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
        self.enable_foreign_keys()
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

        #TODO TEST U. 
        for key in table.list_foreign_keys() : 
            command += r.key_foreign() +' ('+key.child_field+')' + ' REFERENCES '+ key.parent_table+'('+key.parent_field+'), ' 
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

