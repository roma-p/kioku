

# ENUM OF POSSIBLE OPTIONS FOR THE SQLITE TABLES

def type() : return 'type'
def type_text() : return 'TEXT'
def type_integer() : return 'INTEGER'

# To do with decorators ....
def type_list() : return (type_text(), type_integer())


def key() : return 'key'
def key_primary() : return 'PRIMARY KEY'

# To do with decorators ....
def key_list() : return (key_primary())

def constraints() : return 'constraints'
def constraints_autoincrement() : return 'AUTOINCREMENT'
def constraints_unique() : return 'UNIQUE'

def constraints_list() : return (constraints_autoincrement(), constraints_unique())

def id() : return 'id'
def date() : return 'date'

def valid_keys() : return (type(), key(), constraints())

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