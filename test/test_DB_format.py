import unittest, os, gc, logging
from context import kioku
from kioku.DB import database_format_register as r
from kioku.DB.DB_format import DB_format

log = logging.getLogger() 

class TestDB_format(unittest.TestCase) : 

	def test_DB_format_attributes(self):
		db_format = DB_format('db_format_test')

		s = db_format.add_table('table1', True, True)
		self.assertTrue(s)
		s = db_format.add_table('table1')
		self.assertFalse(False)

		table1 = db_format.get_table('table1')
		self.assertEqual(table1(), 'table1')
		self.assertEqual(set(table1.list_field_names()), {'id', 'date'})
		self.assertEqual(db_format.table1.id.key, r.key_primary())

		db_format.add_field(db_format.table1, 'field1', r.type_text(), r.key_primary(), r.constraints_autoincrement(), r.constraints_unique())
		
		self.assertEqual(db_format.table1.field1(), 'field1')
		self.assertEqual(db_format.table1.field1.fieldType, r.type_text())
		self.assertEqual(db_format.table1.field1.key, r.key_primary())
		self.assertEqual(set(db_format.table1.field1.constraints), {r.constraints_unique(), r.constraints_autoincrement()})



if __name__ == '__main__': unittest.main()