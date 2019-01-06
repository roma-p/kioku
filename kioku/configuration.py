import os
import configparser

# to put as enclose. 
config_data = None

# /!\ to move expected configuration file, 
# please modifiy path method.
def path() : return "etc/kioku/config.ini"


def getConfiguration() : 

	global config_data
	if not config_data : 
		if not os.path.exists(path()):
			log.error('config not found on :'+ path())
			return None
		else : 
			config_data = configparser.ConfigParser()
			config_data.read(path())
	return config_data
