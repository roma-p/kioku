from collections import defaultdict
import logging

log = logging.getLogger() 

class Query() :

    def __init__(self): 
        self._sectionList = []
        self._shall_exist = defaultdict(list)
        self._lastTableName = ''

    def __call__(self) : 
        return self._generate_str()

    # select ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def select(self, tableName, *itemToGet) : 
        tableName = _getDataElementName(tableName)
        itemToGet = _formatData(*itemToGet)
        self._sectionList.append(_str_select('SELECT', tableName, itemToGet))
        self._shall_exist[tableName] += itemToGet
        self._lastTableName = tableName
        return self

    def select_distinct() :

        table = _getDataElementName(table)
        itemToGet = _formatData(*itemToGet)
        self._sectionList.append(_str_select('SELECT DISTINCT', tableName, itemToGet))
        self._shall_exist[table] += itemToGet
        self._lastTableName = tableName
        return self

    def count() : pass

    def add(): 
        return self
    
    def delete() :
        return self

    def update() : 
        return self

    def where(self):
        self._sectionList.append('WHERE')
        return self

    def and_(self) : 
        self._sectionList.append('AND')
        return self

    def or_(self) : 
        self._sectionList.append('OR')
        return self

    # equality operator '''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def equal(self, field, value) :
        str_r = self._condition('=', field, value)
        self._sectionList.append(str_r)
        return self

    def not_equal(self, field, value) : 
        str_r = self._condition('!=', field, value)
        self._sectionList.append(str_r)
        return self

    def less_than(self, field, value) : 
        str_r = self._condition('<', field, value)
        self._sectionList.append(str_r)
        return self

    def greater_than(self, field, value) : 
        str_r = self._condition('>', field, value)
        self._sectionList.append(str_r)
        return self

    def in_(self, field, valuesTuple) : 
        if not self._add_shall_exist_field_from_last_table(field) : 
            return None
        str_query = field + ' IN ' + str(tuple(valuesTuple))
        self._sectionList.append(str_query)
        return self

    def is_null(self, field) :
        if not self._add_shall_exist_field_from_last_table(field) : 
            return None
        str_query = field + ' IS NULL'        
        self._sectionList.append(str_query)
        return self

    def _condition(self, conditionner, field, value) :
        field = _getDataElementName(field)
        value,  = _format_value_from_type(value)
        if not value : return None
        if not self._add_shall_exist_field_from_last_table(field) : 
            return None
        str_query = field + conditionner + str(value)
        return str_query

    #  '''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def order_by(self, field) :
        field = _getDataElementName(field)
        if not self._add_shall_exist_field_from_last_table(field) : 
            return None
        str_query = 'ORDER BY ' + field
        self._sectionList.append(str_query)
        return self

    # join ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # TO DO : JOIN DOESNT WORK THIS WAY 
    # NEED TO UPDATE LAST TABLE NAME AS TABLE B. 
    # CONDITIONS AFTER CHANGES TOO, LOL. 

    def join_left(self, table_B, field_A, field_B) :
        table_B, field_A, field_B = _formatData(table_B, field_A, field_B) 
        if not self._add_shall_exist_field_from_last_table(field_A) : 
            return None
        self._shall_exist[table_B].append(field_B)
        table_A = self._lastTableName
        str_query = 'LEFT JOIN ' + table_B + ' ON ' + table_A + '.' + field_A + ' = ' +  table_B + '.' + field_B
        self._shall_exist = {}
        self._lastTableName = None
        self._sectionList.append(str_query)
        return self

    def _add_shall_exist_field_from_last_table(self, field) : 
        if self._lastTableName == None : 
            log.warning("query won't be able to check base consistency")
            return True
        elif not len(self._lastTableName) :
            log.error('error in formatting your query...')
            return False
        self._shall_exist[self._lastTableName].append(field)
        return True


    # generate string '''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def _generate_str(self) : 
        return ' '.join(self._sectionList)

    def get_shall_exit_tables_fields(self) : 
        return self._shall_exist

# *****************************************************************************
def _format_value_from_type(*valueList) : 
    errors = []
    updated_values = []
    status = True
    for value in valueList :
        if isinstance(value, int): 
            value = str(value)
            updated_values.append(value)
        elif isinstance(value, str): 
            value = "'"+value+"'"
            updated_values.append(value)
        else : 
            log.error('wrong type for '+str(value)+ ' expected int or str.')
            status = False
    if status : return updated_values
    else : return None
    

def _str_select(selectType, tableName, itemToGet) : 
    selector = ''
    for item in itemToGet : selector+= item +', '
    selector = selector[:-2]+' '
    sqlrequest = "SELECT " + selector + "FROM " + tableName
    return sqlrequest

def _getDataElementName(object) : 
    '''
    if object is a string, return string,
    othewise return the output of the its __call__ : 
    intented to be use for Table / Field objects of DB_format
    which returns their _name parameter when called. 
    '''
    if isinstance(object, str) : return object
    else : return object()

def _formatData(*tablesAndFields) :
    r_tablesAndFields = tuple([_getDataElementName(item) for item in tablesAndFields])
    return r_tablesAndFields




