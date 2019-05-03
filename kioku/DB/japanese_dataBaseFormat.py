# import database_format_register as r
# import DB_format

from kioku.DB import database_format_register as r
from kioku.DB.DB_format import DB_format


def get_baseFormat() : return baseFormat

# TODO : DELETE THIS, WHERE TO PUT IT? 
def get_vocab_required_col() : return ('word', 'prononciation', 'tag', 'categorie', 'example', 'meaning')

simple_int_field = {r.type() : r.type_integer()}
not_null_int_field = {
	r.type() : r.type_integer(),
	r.constraints() : (r.constraints_not_null(),)
	}
simple_text_field = {r.type() : r.type_text()}
unique_text_field = {
	r.type() : r.type_text(), 
	r.constraints() : (r.constraints_unique(),)
	}
unique_not_null_text_field = {
	r.type() : r.type_text(), 
	r.constraints() : (r.constraints_unique(), r.constraints_not_null())
	}
not_null_text_field = {
	r.type() : r.type_text(), 
	r.constraints() : (r.constraints_not_null(),)
	}

# add not null constraints. 
baseFormat = {
	'vocab' : {	
		r.id() : True,
		r.date() : True,
		'word' : unique_not_null_text_field, 
		'prononciation' : simple_text_field, 
		'core_prononciation' : simple_int_field,
		'meaning' : not_null_text_field, 
		'example' : simple_text_field, 
		'categorie' : not_null_int_field, 
		'tag' : simple_int_field, 
		r.key_foreign() : {
		    'tag' : ('tags', 'id'),
		    'categorie' : ('categories', 'id')
		    } 
	}, 
	'categories' : {
		r.id() : True,
		'name' : unique_not_null_text_field	
	},
	'tags' : {
		r.id() : True,
		'name' : unique_not_null_text_field	
	}, 
	'kanjis' : {
		r.id() : True,
		'name' : unique_not_null_text_field	
	},
	'core_prononciations' : {
		r.id() : True,
		'name' : unique_not_null_text_field	
	},
	'word_kanjis' : {
		r.id() : True,
		'word_id' : not_null_int_field, 
		'kanji_id' : not_null_int_field,
	},
	'version' : 1.0
}
