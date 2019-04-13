import database_format_register as r
import DB_format


def get_baseFormat() : return baseFormat
def get_vocab_required_col() : return ('word', 'prononciation', 'tag', 'categorie', 'example', 'meaning')

simple_int_field = {r.type() : r.type_integer()}
simple_text_field = {r.type() : r.type_text()}
unique_text_field = {
	r.type() : r.type_text(), 
	r.constraints() : (r.constraints_unique(),)
	}

# add not null constraints. 
baseFormat = {
	'vocab' : {	
		r.id() : True,
		r.date() : True,
		'word' : unique_text_field, 
		'prononciation' : simple_text_field, 
		'core_prononciation' : simple_int_field,
		'meaning' : simple_text_field, 
		'exemple' : simple_text_field, 
		'categorie' : simple_int_field, 
		'tag' : simple_int_field, 
		r.key_foreign() : {
		    'tag' : ('tags', 'id'),
		    'categorie' : ('categories', 'id')
		    } 
	}, 
	'categories' : {
		r.id() : True,
		'name' : unique_text_field	
	},
	'tags' : {
		r.id() : True,
		'name' : unique_text_field	
	}, 
	'kanjis' : {
		r.id() : True,
		'name' : unique_text_field	
	},
	'core_prononciations' : {
		r.id() : True,
		'name' : unique_text_field	
	},
	'word_kanjis' : {
		r.id() : True,
		'word_id' : {r.type() : r.type_integer()}, 
		'kanjis_id' : {r.type() : r.type_integer()},
	},
	'version' : 1.0
}
