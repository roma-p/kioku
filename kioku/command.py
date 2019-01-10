import logging, sys, os, datetime
import configparser, sqlite3
from shutil import copyfile
import kioku.ankiParser as ankiParser
import kioku.configuration as configuration
from kioku.DB_handler import DB_handler
import kioku.db_generation as db_generation
import kioku.db_update as db_update
import kioku.helpers as helpers


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
		log.error('backuped done but init process failed somehow.')
	return status


def update_DB(input_data) :


	# Checking ---------------------------------------------------------------
	status = True
	if not os.path.exists(input_data) : 
		log.error('file / path not found :' + input_data )
		status = False
	config_data = configuration.getConfiguration()
	if not config_data : 
		log.error('configuration data loading failed.')
		status = False

	if not status : 
		log.error('DB not updated.')
		return status

	#TODO : need a way to check csv file integrity before modifying DB...

	# Updating databse --------------------------------------------------------
	if input_data[-3:] == 'csv' : 
		db_update.add(input_data)
		bk_list = [input_data]

	else : 
		fileList = db_update.add_multiple(input_data)
		bk_list = fileList

	# Backup of files ---------------------------------------------------------
	for file in bk_list :
		file_bk_name = _name_intermediate_file(file)
		print(file_bk_name
			)
		if not file_bk_name : 
			log.error('could not backup file : ' + original_file)
		else : 
			copyfile(file, file_bk_name)
			log.info('data file backuped at : ' + file_bk_name)


intermediate_files_bk = ''

def _name_intermediate_file(original_file): 

	global intermediate_files_bk
	if not intermediate_files_bk : 
		if not _get_intermediate_files_bk_path() : 
			return ""
	original_name = os.path.basename(original_file)
	now_str = helpers.format_now()
	new_file_name = intermediate_files_bk + '/' + original_name
	return new_file_name


def _get_intermediate_files_bk_path(): 
	
	global intermediate_files_bk
	intermediate_files_bk = configuration.getConfiguration().get('kioku', 'intermediate_files_bk')
	if not intermediate_files_bk : 
		log.error('did not find path to store data file "intermediate_files_bk" in configuration file.')
		return False
	return True



