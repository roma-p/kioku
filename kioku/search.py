import os, logging
from kioku.DB_handler import DB_handler

log = logging.getLogger()
db_handler = DB_handler()

tag_cat = ('tag', 'categorie')

def listByType(tag = None, categorie = None) : 
	for base in [tag, categorie] : 
		if base : 
			if baseName not in tag_cat : 
				log.error('allowed base name are : '+baseName)
				return
	else : 
		return db_handler.select()


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
