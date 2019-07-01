import os
import logging
import configparser

log = logging.getLogger()

_configuration_object = None

# /!\ to move expected configuration file, 
# please modifiy either config_ini_path or config_ini path method.
CFG_INI_PATH = "etc/kioku/config.ini"
DEFAULT_USER_DIR = "etc/kioku/"
CFG_PATHS_DICT = {
    'db_path' : 'kioku1.db',
    'db_bk' : 'db_bk/',
    'input_files_bk' : 'savedFiles/inputFiles_bk/',
    'intermediate_files_bk' : 'savedFiles/intermediate_files_bk/'
}

def reset() : 
    global config_data
    config_data = None

def get_configuration() : 
    global _configuration_object
    if not _configuration_object : 
        config_ini_data = _get_config_ini_data()
        _configuration_object = Configuration()
        config_data_user_dir = config_ini_data.get('kioku', 'user_dir')
        user_dir = _get_user_dir_path(config_data_user_dir)
        for attribute_name, partial_path in CFG_PATHS_DICT.items() : 
            complete_path = user_dir + '/' +  partial_path
            setattr(Configuration, attribute_name, complete_path)
        Configuration.csv_delimiter = config_ini_data.get('kioku', 'csv_delimiter')
    return _configuration_object

# -----------------------------------------------------------------------------

def _get_config_ini_data() : 
    path = _get_config_ini_path()
    if not os.path.exists(path):
        log.error('config not found on :'+ path)
        return None
    else : 
        config_data = configparser.ConfigParser()
        config_data.read(path)
    return config_data

def _get_config_ini_path() :  
    return _resolve_relative(CFG_INI_PATH)

def _get_user_dir_path(user_dir) : 
    if not os.path.isabs(user_dir) : return _resolve_relative(user_dir)
    else : return user_dir

def _resolve_relative(path) :
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)

# -----------------------------------------------------------------------------

class Configuration() : 
    def __init__(self) : 
       db_path = None
       db_bk = None
       input_files_bk = None
       intermediate_files_bk  = None
       csv_delimiter = None


    def __str__(self) : 
        _str = "configuration data : \n"

        for attributes_name, attribute_value in Configuration.__dict__.items() : 
            if isinstance(attribute_value, str) : 
                _str += attributes_name + ' : ' + attribute_value + '\n'
        return _str



