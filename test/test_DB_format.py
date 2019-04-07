import unittest, os, gc, logging
from context import kioku
from kioku.DB import database_format_register as r
from kioku.DB.DB_format import DB_format

log = logging.getLogger() 

simple_text_field = {r.type() : r.type_text()}
simple_int_field = {r.type() : r.type_integer()}


db_format_correct = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'simplified_p' : simple_text_field,
        'meaning' : simple_text_field, 
        'exemple' : simple_text_field, 
        'categorie' : simple_text_field, 
        'tag' : simple_text_field, 
    }, 
    'categorie' : {
        r.id() : True,
        'name' : simple_text_field  
    },
    'tag' : {
        r.id() : True,
        'name' : simple_text_field  
    }
}

db_format_wrong_1 = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'simplified_p' : {r.type() : 'WRONG'},
    }
}

db_format_wrong_2 = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'simplified_p' : {'WRONG' : 'WRONG'},
    }
}

db_fkeys_correct = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'meaning' : simple_text_field, 
        'categorie' : simple_int_field,
        'tag' : simple_int_field,
        r.key_foreign() : {
            'tag' : ('tag', r.id()),
            'categorie' : ('categorie', r.id())
            } 
    }, 
    'categorie' : {
        r.id() : True,
        'name' : simple_text_field  
    },
    'tag' : {
        r.id() : True,
        'name' : simple_text_field  
    } 
}

db_fkeys_wrong = {
    'vocab' : { 
        r.id() : True,
        r.date() : True,
        'word' : simple_text_field, 
        'prononciation' : simple_text_field, 
        'meaning' : simple_text_field, 
        'categorie' : simple_int_field,
        'tag' : simple_int_field,
        r.key_foreign() : {
            'tag' : ('tag', r.id()),
            'categorie' : ('categorie', r.id())
            } 
    }, 
    'categorie' : {
        r.id() : True,
        'name' : simple_text_field  
    }
}

class TestDB_format(unittest.TestCase) : 

    def test_DB_format_attributes(self):
        db_format = DB_format('db_format_test')

        s = db_format.add_table('table1', True, True)
        self.assertTrue(s)
        s = db_format.add_table('table1')
        self.assertFalse(s)

        table1 = db_format.get_table('table1')
        self.assertEqual(table1(), 'table1')
        self.assertEqual(set(table1.list_field_names()), {'id', 'date'})
        self.assertEqual(db_format.table1.id.key, r.key_primary())

        s = db_format.add_field(db_format.table1, 'field1', r.type_text(), r.key_primary(), r.constraints_autoincrement(), r.constraints_unique())
        self.assertTrue(s)

        self.assertEqual(db_format.table1.field1(), 'field1')
        self.assertEqual(db_format.table1.field1.fieldType, r.type_text())
        self.assertEqual(db_format.table1.field1.key, r.key_primary())
        self.assertEqual(set(db_format.table1.field1.constraints), {r.constraints_unique(), r.constraints_autoincrement()})

        
        s = db_format.add_table('table2')
        db_format.add_field(db_format.table2, 'field2', r.type_text())

        self.assertEqual(set(db_format.list_tables_names()), {'table1', 'table2'})
        self.assertEqual(set(db_format.table1.list_field_names()), {'id', 'date', 'field1'})

    def test_DB_format_from_dict(self) : 

        db_format = DB_format('db_format_correct', **db_format_correct)

        for tableName in db_format_correct.keys() : 
            self.assertIn(tableName, db_format.list_tables_names())

        for field in db_format_correct['vocab'].keys() :
            self.assertIn(field, db_format.vocab.list_field_names())

        self.assertEqual(db_format.categorie.name.fieldType, r.type_text())
        self.assertEqual(db_format.vocab.tag.fieldType, r.type_text())

    def test_DB_format_from_dict_error(self) : 
        for wrong_input in (db_format_wrong_1, db_format_wrong_2) : 
            try : 
                a = DB_format('wrong', **wrong_input)
            except ValueError : 
                a = None
            finally : 
                self.assertEqual(a, None)
    
    def test_foreign_keys(self) : 
        db_format = DB_format('db_format', **db_fkeys_correct)
        self.assertNotEqual(db_format, None)
        self.assertEqual(db_format.list_tables_names(), ('vocab', 'categorie', 'tag'))
        self.assertEqual(db_format.list_field_names('vocab'), ('id', 'date', 'word', 'prononciation', 'meaning', 'categorie', 'tag'))

        fkeys_tuple = db_format.vocab.list_foreign_keys()
        fkey_to_check = None
        for key in fkeys_tuple : 
            if key.child_field == 'tag' : 
                fkey_to_check = key
        self.assertNotEqual(fkey_to_check, None)
        self.assertEqual(fkey_to_check.parent_table, 'tag')
        self.assertEqual(fkey_to_check.parent_field, 'id')

        try : 
            db_format = DB_format('wrong', **db_fkeys_wrong)
        except ValueError : 
            a = None
        finally : 
            self.assertEqual(a, None)




if __name__ == '__main__': unittest.main()