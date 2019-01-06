#def path() : return "etc/kioku/config.ini"

# to put as enclose. 
config_data = None
path = "etc/kioku/config.ini"

def getConfiguration() : 

	if not config_data : 
		if not os.path.exists(path): 
			log.error('config not found on :'+ path)
			return None
		else : 
			config_data = configparser.SafeConfigParser()
			config_data.read(path)
	return config_data
