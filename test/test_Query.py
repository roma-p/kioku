import unittest, os, gc, logging
from context import kioku
from kioku.DB.Query import Query

log = logging.getLogger() 

class TestQuery(unittest.TestCase) : 

    def test_Query(self) : 

        q_exepcted = "SELECT field1, field2 FROM table1 WHERE field2='value1' AND field3 IN (1, 2, 3, 4) ORDER BY field3"
        check_expected = {
            'table1' : {'field1', 'field2', 'field3'}
        }

        q = Query().select('table1', 'field1', 'field2')
        q.where().equal('field2', 'value1')
        q.and_().in_('field3', (1,2,3,4))
        q.order_by('field3')

        self.assertEqual(q(), q_exepcted)
        self.assertTrue( _checkDBFormat(q.get_shall_exit_tables_fields(), check_expected))


        q2 = Query().select('table1', 'field1')
        q2.join_left('table2', 'id1', 'id2')
        q2.where().is_null('field2')
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