import database_format_register as r

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

