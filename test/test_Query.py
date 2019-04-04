import unittest, os, gc, logging
from context import kioku
from kioku.DB.Query import Query

log = logging.getLogger() 

class TestQuery(unittest.TestCase) : 

	def test_Query(self) : 
		q = Query().select('table1', 'field1')
		q.where().equal('field2', 'value1')
		q.and_().in_('field3', (1,2,3,4))
		q.order_by('field3')

		print(q())
		#print(q._sectionList)
		print('o'*50)
		q2 = Query().select('table1', 'field1')
		q2.join_left('table2', 'id1', 'id2')
		q2.where().is_null('field2')


if __name__ == '__main__': unittest.main()