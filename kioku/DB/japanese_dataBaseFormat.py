import database_format_register as r
import DB_format

# Make an object DatabaseFormat that automatically generate methods 
# So user can do : 
# DBHandler.format.TableName.tbField() <- this is proper, no what i'm doing. 
# Generate and update the dict below while adding new rows and stuff ...


baseFormat = {
	'vocab' : {	
		**r.table_id_index(),
		'word' : {r.type() : r.type_text()}, 
		'prononciation' : {r.type() : r.type_text()}, 
		'simplified_p' : {r.type() : r.type_text()},
		'meaning' : {r.type() : r.type_text()}, 
		'exemple' : {r.type() : r.type_text()}, 
		'categorie' : {r.type() : r.type_text()}, 
		'tag' : {r.type() : r.type_text()}, 
		**r.table_date()
	}, 
	'categorie' : {
		**r.table_id_index(),
		'name' : {r.type() : r.type_text()}	
	},
	'tag' : {
		**r.table_id_index(),
		'name' : {r.type() : r.type_text()}	
	}, 
	'kanjis' : {
		**r.table_id_index(),
		'name' : {r.type() : r.type_text()}	
	},
	'simplified_p' : {
		**r.table_id_index(),
		'name' : {r.type() : r.type_text()}	
	},
	'word_kanjis' : {
		**r.table_id_index(),
		'word_id' : {r.type() : r.type_integer()}, 
		'kanjis' : {r.type() : r.type_text()},
	},	
}

def get_baseFormat() : return baseFormat
def get_vocab_required_col() : return ('word', 'prononciation', 'tag', 'categorie', 'example', 'meaning')

japaneseFormat = DB_format('japanese_format')
japanese_format.addTable('vocab', id = True, date = True)
vocab_data = (
	('word', r.type_text()),
	('prononciation', r.type_text()),
	('simplified_p', r.type_text()),
	('meaning', r.type_text()),
	('exemple', r.type_text()),
	('categorie', r.type_text()),
	('tag', r.type_text())
	)
japanese_format.addFields('vocab', vocab_data) 

japanese_format.addTable('categorie')
japanese_format.addField('categorie', 'name', r.type_text()) 

japanese_format.addTable('tag')
japanese_format.addField('tag', 'name', r.type_text()) 

japanese_format.addTable('kanjis')
japanese_format.addField('kanjis', 'name', r.type_text()) 

japanese_format.addTable('simplified_p')
japanese_format.addField('simplified_p', 'name', r.type_text()) 

japanese_format.addTable('word_kanjis')
japanese_format.addField('word_kanjis', 'word_id', r.type_integer()) 
japanese_format.addField('word_kanjis', 'kanjis', r.type_text()) 

simple_text_field = {r.type() : r.type_text()}

baseFormat_2 = {
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
	}, 
	'kanjis' : {
		r.id() : True,
		'name' : simple_text_field	
	},
	'simplified_p' : {
		r.id() : True,
		'name' : simple_text_field	
	},
	'word_kanjis' : {
		r.id() : True,
		'word_id' : {r.type() : r.type_integer()}, 
		'kanjis' : simple_text_field,
	},	
}

japaneseFormat_2 = DB_format('japanese_format', baseFormat_2)
