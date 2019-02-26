

# ENUM OF POSSIBLE OPTIONS FOR THE SQLITE TABLES

def type() : return 'type'  
def type_text() : return 'TEXT'
def type_integer() : return 'INTEGER'

def key() : return 'key'
def key_primary() : return 'PRIMARY KEY'

def constraints() : return 'constraints'
def constraints_autoincrement() : return 'AUTOINCREMENT'
def constraints_unique() : return 'UNIQUE'


# HELPER : COMMON TABLE CONFIGURATIONS.  

def table_id_index() : 
	return {
		'id' : {
		type() : type_integer(), 
		key() : key_primary(), 
		constraints() : [constraints_autoincrement(), constraints_unique()]
		}
	}

def table_date() : 
	return { 
		'date' : {
			type() : type_text()
		}
	}
