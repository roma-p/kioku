baseFormat = {
	'vocab' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'word' : {'type' : 'text'}, 
		'prononciation' : {'type' : 'text'}, 
		'simplified_p' : {'type' : 'text'},
		'meaning' : {'type' : 'text'}, 
		'exemple' : {'type' : 'text'}, 
		'categorie' : {'type' : 'text'}, 
		'tag' : {'type' : 'text'}, 
		'date' : {'type' : 'text'}
	}, 
	'categorie' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'name' : {'type' : 'text'}	
	},
	'tag' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'name' : {'type' : 'text'}	
	}, 
	'kanjis' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'name' : {'type' : 'text'}	
	},
	'simplified_p' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'name' : {'type' : 'text'}	
	},
	'word_kanjis' : {
		'id' : {
			'type' : 'INTEGER', 
			'key' : 'PRIMARY KEY', 
			'constraints' : ['AUTOINCREMENT', 'UNIQUE']
		},
		'word_id' : {'type' : 'INTEGER'}, 
		'kanjis' : {'type' : 'text'},
	},	
}