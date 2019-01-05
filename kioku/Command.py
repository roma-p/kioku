import logging, sys, os, datetime
import configparser, sqlite3
from ankiParser import ankiParser
import kioku.conf_path as conf_path
from db_handling import db_generation, DB_handler

log = logging.getLogger()


# to put as enclose. 
config_data = None


def getConfig_data() : 

	if not config_data : 
		if not os.path.exists(conf_path.path()): 
			log.error('config not found on :'+ conf_path.path())
			return None
		else : 
			config_data = configparser.SafeConfigParser()
			config_data.read(conf_path.path())
	return config_data


def init_kioku() : 

	db_path = getConfig_data().get('kioku', 'db_path')
	if not os.path.exists(db_path) : 
		log.warning("database not found at : " + db_path)
		log.warning("instanciating a fresh one.")
		status = db_generation.generateDB(db_path)
		if not status : return False

	db_handler = DB_handler()
	if not db_handler: return False
	return True


def backup_DB(backupName) : 
	
	if backupName[:-3] != '.db':
		log.error('backup files are .db')
		return
	config_data = getConfig_data()		
	db_path = config_data.get('kioku', 'db_path')
	db_bk = config_data.get('kioku', 'db_bk')
	backup_path = backupName + backupName
	copyfile(kioku_path, backup_path)


def reset_DB() : 

	config_data = getConfig_data()
	db_path = config_data.get('kioku', 'db_path')
	db_bk = config_data.get('kioku', 'db_bk')
	bdd_name = db_path.split('/')[-1].split('.db')[0]
	now = datetime.datetime.now()
	backup_fullpath = db_bk + '/' + bdd_name + '_backup_' +str(now.year)+'.'+str(now.month)+'.'+str(now.day)+'.'+str(now.hour)+':'+str(now.minute) + '.db'
	os.rename(kioku_path, backup_fullpath)
	log.info('current BDD saved as : '+backup_fullpath)
	init_Kioku()


def update() : 
	pass



