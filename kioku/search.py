import os, logging
from kioku.DB_handler import DB_handler

log = logging.getLogger()

tag_cat = ('tag', 'categorie')

def listByType(tag = None, categorie = None) : 

	db_handler = DB_handler()

	conditions = {
	'tag' : tag, 
	'categorie' : categorie 
	}

	conditions_treated = {}
	for _type, _name in conditions : 
		if _name : 
			if _name not in db_handler.list(_type, 'name'): 
				log.warning('trying to list using non existing '+ _type+' "'+_name+'"')
			conditions_treated[_type] = _name
	
	return db_handler.select('vocab')


def listTypes(baseName):
	if baseName not in tag_cat : 
		log.error('allowed base name are : '+baseName)
		return
	output_dict = {}
	for type_name in db_handler.select(baseName, name): 
		output_dict[type_name] : _countvocabByType(baseName, )
	return output_dicttype_name


def _countvocabByType(type_name, type_id): 
	if type_name not in tag_cat : 
		log.error('allowed base name are : '+baseName)
		return
	return db_handler.count('vocab', type_name=type_id)
