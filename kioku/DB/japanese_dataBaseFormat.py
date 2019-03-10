import database_format_register as r
import DB_format


def get_baseFormat() : return baseFormat
def get_vocab_required_col() : return ('word', 'prononciation', 'tag', 'categorie', 'example', 'meaning')

simple_text_field = {r.type() : r.type_text()}

baseFormat = {
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
