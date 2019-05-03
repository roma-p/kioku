from collections import defaultdict
import logging

log = logging.getLogger() 

class Query() :

    def __init__(self): 
        self._sectionList = []
        self._shall_exist = defaultdict(set)
        self._mainTable = ''

    def __call__(self) : 
        return self._generate_str()

    # select ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def select(self, mainTableObject, *fieldToSelect, count_field = None) : 
        self._sectionList.append(self._str_select('SELECT', mainTableObject, fieldToSelect, count_field = count_field))
        self._shall_exist[mainTableObject()] = set()
        self.update_shall_exist(*fieldToSelect)
        self._mainTable = mainTableObject()
        return self

    def _str_select(self, selectType, mainTableObject, fieldToGet, count_field = None) : 
        selector = ''
        for field in fieldToGet : selector+= field.parent_table()+'.'+field()+', '
        if count_field : 
            selector += self._count_str(count_field)+', '
        selector = selector[:-2]+' '
        sqlrequest = "SELECT " + selector + "FROM " + mainTableObject()
        return sqlrequest


    # ?? KEY WORD ARG? BUT IN CASES OF ALIAS?
    # def select_distinct() :

    #     table = _getDataElementName(table)
    #     itemToGet = _formatData(*itemToGet)
    #     self._sectionList.append(_str_select('SELECT DISTINCT', tableName, itemToGet))
    #     self._shall_exist[table] += itemToGet
    #     self._lastTableName = tableName
    #     return self

    def count(self, field) : 
        self._sectionList.append(self._count_str(field))
        return self

    def _count_str(self, field) : 
        self.update_shall_exist(field)
        field_str = _format_string_from_fieldObject(field)
        rqt = ('COUNT ('+field_str+')')
        return rqt

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
        self.update_shall_exist(field) 
        field_str = _format_string_from_fieldObject(field)
        str_query = field_str + ' IN ' + str(tuple(valuesTuple))
        self._sectionList.append(str_query)
        return self

    def is_null(self, field) :
        self.update_shall_exist(field) 
        field_str = _format_string_from_fieldObject(field)
        str_query = field_str + ' IS NULL'        
        self._sectionList.append(str_query)
        return self

    def _condition(self, conditionner, field, value) :
        
        value,  = _format_value_from_type(value)
        if not value : return None
        self.update_shall_exist(field)
        field_str = _format_string_from_fieldObject(field)
        str_query = field_str + conditionner + str(value)
        return str_query

    #  '''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def group_by(self, field) : 
        self.update_shall_exist(field) 
        field_str = _format_string_from_fieldObject(field)
        str_query = 'GROUP BY ' + field_str
        self._sectionList.append(str_query)
        return self

    def order_by(self, field) :
        self.update_shall_exist(field) 
        field_str = _format_string_from_fieldObject(field)
        str_query = 'ORDER BY ' + field_str
        self._sectionList.append(str_query)
        return self

    def order_by_count(self, field) : 
        self.update_shall_exist(field) 
        count_str = self._count_str(field)
        str_query = 'ORDER BY '+ count_str
        self._sectionList.append(str_query)
        return self        

    def asc(self) : 
        self._sectionList.append('ASC')
        return self

    def desc(self) : 
        self._sectionList.append('DESC')
        return self

    def limit(self, limit, offset = None) : 
        str_sql = 'LIMIT '+str(limit)
        if offset : str_sql += " OFFSET "+str(offset)        
        self._sectionList.append(str_query)
        return self


    # join ''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def join_left(self, left_field, right_field) : 
        self.update_shall_exist(left_field, right_field)
        right_table_str = right_field.parent_table()
        left_field_str = _format_string_from_fieldObject(left_field)
        right_field_str = _format_string_from_fieldObject(right_field)
        str_query = 'LEFT JOIN ' + right_table_str + ' ON ' + left_field_str + ' = ' +  right_field_str
        self._sectionList.append(str_query)
        return self

    # generate string '''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def _generate_str(self) : 
        return ' '.join(self._sectionList)

    def get_shall_exit_tables_fields(self) : 
        return self._shall_exist

    def update_shall_exist(self, *fieldObjectList) : 
        for fieldObject in fieldObjectList : 
            self._shall_exist[fieldObject.parent_table()].add(fieldObject())

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

def _format_string_from_fieldObject(fieldObject) : 
    return fieldObject.parent_table() + '.' + fieldObject()



