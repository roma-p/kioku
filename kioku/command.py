import logging, sys, os, datetime
import configparser, sqlite3
from shutil import copyfile
import kioku.ankiParser as ankiParser
import kioku.configuration as configuration
from kioku.DB_handler import DB_handler
import kioku.db_generation as db_generation


log = logging.getLogger()

def init_kioku() : 

	db_path = configuration.getConfiguration().get('kioku', 'db_path')
	if not os.path.exists(db_path) : 
		log.warning("database not found at : " + db_path)
		log.warning("instanciating a fresh one.")
		status = db_generation.generateDB(db_path)
		if not status : return False

	db_handler = DB_handler()
	if not db_handler: return False
	return True


def backup_DB(backupName) : 
	
	if backupName[-3:] != '.db':
		log.error('backup files are .db')
		return False
	config_data = configuration.getConfiguration()		
	
	if not config_data : 
		log.error('no config data found...')
		return False

	db_path = config_data.get('kioku', 'db_path')
	db_bk = config_data.get('kioku', 'db_bk')
	backup_path = db_bk + '/' + backupName
	
	status = True
	for path in (db_path, db_bk) : 
		if not os.path.exists(path): 
			status = False
			log.error('Path not found : ' + path)
	if not status : return status
	
	copyfile(db_path, backup_path)
	return status


reset_suffix = '_backup_'

def reset_DB() : 

	global reset_suffix
	status = True
	config_data = configuration.getConfiguration()
	db_path = config_data.get('kioku', 'db_path')
	db_bk = config_data.get('kioku', 'db_bk')

	for path in (db_path, db_bk) : 
		if not os.path.exists(path): 
			status = False
			log.error('Path not found : ' + path)
	if not status : return status

	bdd_name = db_path.split('/')[-1].split('.db')[0]
	now = datetime.datetime.now()
	backup_fullpath = db_bk + '/' + bdd_name + reset_suffix + str(now.year) +'.' + str(now.month) + '.' + str(now.day) + '.' + str(now.hour) + ':' + str(now.minute) + '.db'
	os.rename(db_path, backup_fullpath)
	log.info('current BDD saved as : '+ backup_fullpath)
	

	status = init_kioku()
	if not status : 
		log.error("backuped done but init process failed somehow.")
	return status


def update() : 
	pass



