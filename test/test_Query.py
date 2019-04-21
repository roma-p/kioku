import unittest, os, gc, logging
from context import kioku
from kioku.DB.Query import Query
from kioku.DB.DB_format import DB_format
import kioku.DB.database_format_register as r


log = logging.getLogger() 

class TestQuery(unittest.TestCase) : 

    def test_Query(self) : 



        f = DB_format('format')
        f.add_table('table1')
        f.add_table('table2')
        f.add_field('table1', 'field1', r.type_integer())
        f.add_field('table1', 'field2', r.type_integer())
        f.add_field('table1', 'field3', r.type_integer())
        f.add_field('table1', 'id1', r.type_integer())
        f.add_field('table2', 'id2', r.type_integer())
        f.add_field('table2', 'field4', r.type_integer())



        q_exepcted = "SELECT table1.field1, table1.field2 FROM table1 WHERE table1.field2='value1' AND table1.field3 IN (1, 2, 3, 4) ORDER BY table1.field3"
        check_expected = {
            'table1' : {'field1', 'field2', 'field3'}
        }

        q = Query().select(f.table1, f.table1.field1, f.table1.field2)
        q.where().equal(f.table1.field2, 'value1')
        q.and_().in_(f.table1.field3, (1,2,3,4))
        q.order_by( f.table1.field3)

        self.assertEqual(q(), q_exepcted)
        self.assertTrue( _checkDBFormat(q.get_shall_exit_tables_fields(), check_expected))

        q2 = Query().select(f.table1, f.table1.field1)
        q2.join_left(f.table1.id1, f.table2.id2)
        q2.where().is_null(f.table2.field4)

#       TODO probably false ....
#       TODO : change defautl type of Query shqll exist stuff from list to set.          
#        self.assertEqual(q(), q_exepcted)


def _checkDBFormat(dictToCheck, dictChecker) : 
    s = True
    dictToCheck_key_set = set(dictToCheck.keys())
    dictChecker_key_set = set(dictChecker.keys())
    if not _checkSet(dictToCheck_key_set, dictChecker_key_set) : 
        return False
    else : 
        for tableName, fieldList in dictToCheck.items() : 
            if not _checkSet(set(fieldList), set(dictChecker[tableName])) : 
                log.error('error detected in '+tableName)
                s = False
    return s

def _checkSet(setToCheck, setChecker) : 
    missing = setToCheck - setChecker
    plus = setChecker - setToCheck

    s = True
    if missing : 
        log.error('missing values :'+str(missing))
        s = False
    if plus : 
        log.error('values not expected :'+str(missing))
        s = False
    return s

if __name__ == '__main__': unittest.main()



