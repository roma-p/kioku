import logging, os, glob, shutil
import csv
from shutil import copyfile
from tempfile import NamedTemporaryFile
from japanese.Japanese_DB_handler import Japanese_DB_handler
import configuration as configuration

log = logging.getLogger()
fields = ['categorie', 'tag', 'word', 'prononciation', 'meaning', 'example']
# LISTING CATEGORIES / TAGS from csv files ************************************
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def list_cat_tag_from_csv_dir(directory, log_info = False) :
    if not os.path.exists(directory) : 
        log.error('directory do not exist : '+ directory)
        return
    input_file_list = glob.glob(directory + '/*.csv')
    if not input_file_list : 
        log.error('no csv file found in ' + directory)
        return
    return list_cat_tag_from_csv_files(*input_file_list, log_info = False)

def list_cat_tag_from_csv(input_file, log_info = False) : 
    if not os.path.exists(input_file) : 
        log.error('file do not exist : ' + input_file)
        return
    return list_cat_tag_from_csv_files(input_file, log_info = False)

def list_cat_tag_from_csv_files(*input_file_list, log_info = False) : 
    csv_all_cat = set() # all cat found in csv
    csv_all_tag = set() # all tag found in csv 
    csv_existing_cat = set() # cat found in csv files already existing in DB.
    csv_existing_tag = set() # tag found in csv files already existing in DB.
    csv_new_cat = set() # new cat found in at least on csv file.
    csv_new_tag = set() # new tag found in at least on csv file.

    jpDB = Japanese_DB_handler()
    f = jpDB.base_format

    jpDB_cat = set(jpDB.select(f.categories, f.categories.name))
    jpDB_tag = set(jpDB.select(f.tags, f.tags.name))


    for input_file in input_file_list : 
        found_cat, found_tag = _list_cat_tag_process_single_file(input_file)         
        csv_all_cat.update(found_cat)
        csv_all_tag.update(found_tag)

    csv_existing_cat = csv_all_cat & jpDB_cat
    csv_existing_tag = csv_all_tag & jpDB_tag

    csv_new_cat = csv_all_cat - csv_existing_cat
    csv_new_tag = csv_all_tag - csv_existing_tag

    if log_info : 
    	_log_separator('categories')
    	log.info('1 : existing categories : ') 
    	_log_set(csv_existing_cat)
    	log.info('          ')
    	log.info('2 : existing categories : ') 
    	_log_set(csv_new_cat)
    	log.info('          ')
    	_log_separator('tags')
    	log.info('1 : existing tags : ') 
    	_log_set(csv_existing_tag)
    	log.info('          ')
    	log.info('2 : existing tags : ') 
    	_log_set(csv_new_tag)
    	log.info('          ')

    return csv_existing_cat, csv_new_cat, csv_existing_tag, csv_new_tag

def _list_cat_tag_process_single_file(input_file) : 
    found_cat = set()
    found_tag = set()
    delimiter = _get_delimiter() # cqnt work with tab in python. 

    with open (input_file, 'r') as fout : 
        # TODO : DELIMITER IN CONFIGURATION !
        for row in csv.reader(fout, delimiter = '	'): 
            if 'ERROR' not in row[1] : 
                if row[0] not in ['categorie', ''] : found_cat.add(row[0])
                if row[1] not in ['tag', ''] : found_tag.add(row[1])
    return found_cat, found_tag

def _log_separator(text) : 
    len_of_line = 80 
    half_sep_len = (len_of_line - 2 - len(text)) // 2
    last = (len_of_line - 2 - len(text)) % 2 
    log.info('*' * half_sep_len + ' ' + text + ' ' + '*' * half_sep_len + '*' * last)
    log.info('-' * len_of_line)
    log.info(' ')

def _log_set(setTolog) : 
    if not setTolog : 
        log.info('None found...')
    else : 
        for item in sorted(list(setTolog)) : 
            log.info(item)


# PATCHING CATEGORIES TAG of csv files ****************************************
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def patch_cat_tag_csv_dir(input_directory, output_directory, correction_dict) : 

    status = True
    for directory in (input_directory, output_directory) : 
        if not os.path.exists(directory) : 
            log.error('directory not found : ' + directory)
            status = False
    if not status : return False

    input_files = glob.glob(input_directory + '/*.csv')
    if not input_files : 
        log.error('no csv found in directory : '+ input_directory)
        return False

    input_output_file_list = []
    for input_file in input_files : 
        input_output_file_list.append((input_file, output_directory + '/' + os.path.basename(input_file)))
    
    patch_cat_tag_csv_files(*input_output_file_list, **correction_dict)
    return True
    
def patch_cat_tag_csv(input_file, output_file, correction_dict) :
    if not os.path.exists(input_file) : 
        log.error('file not found : '+input_file)
        return False
    patch_cat_tag_csv_files((input_file, output_file), **correction_dict)
    return True

# input_output_file_list : list of tuple (input_file, output_file)
# correction_dict =  'categories' : {[<cat_to_correct_to>] = <list of categorie that shall be corrected from>},
#                    'tags'       : {[<tag_to_correct_to>] = <list of tag       that shall be corrected from>},
def patch_cat_tag_csv_files(*input_output_file_list, **correction_dict) : 

    inverted_correction_dict = _invert_correction_dict(correction_dict)
    for (input_file, output_file) in input_output_file_list : 
        patch_cat_tag_process_single_file(input_file, output_file, **inverted_correction_dict)

def patch_cat_tag_process_single_file(input_file, output_file, **inverted_correction_dict) : 

    delimiter = _get_delimiter()
    copyfile(input_file, output_file)
    temp_file = NamedTemporaryFile(mode='w', delete=False)

    with open(output_file, 'r') as csv_file, temp_file : 

        reader = csv.DictReader(csv_file,  fieldnames=fields, delimiter = '	')
        writer = csv.DictWriter(temp_file, fieldnames=fields, delimiter = '	')            


        for row in reader : 
            # patching categorie and tag if required. 
            if row['categorie'] not in inverted_correction_dict['categories'].keys() : categorie = row['categorie']
            else : 
                categorie = inverted_correction_dict['categories'][row['categorie']]
            if row['tag'] not in inverted_correction_dict['tags'].keys() : tag = row['tag']
            else : tag = inverted_correction_dict['tags'][row['tag']]

            # other entries left as such. 
            new_row = {
                'categorie' : categorie, 
                'tag' : tag, 
                'word' : row['word'],
                'prononciation' : row['prononciation'], 
                'meaning' : row['meaning'], 
                'example' : row['example']                
            }
            writer.writerow(new_row)
    
    shutil.move(temp_file.name, output_file)
    log.info('processed : '+ input_file + ', saved at: ' + output_file)

# TODO set, not list. 
def _invert_correction_dict(correction_dict) : 

    inverted_dict = {
    'categories' : {}, 
    'tags' : {}
    }

    for _type in ('categories', 'tags') : 
        if _type in correction_dict.keys() : 
            for to_correct_to, list_to_correct in correction_dict[_type].items() : 
                for item in list_to_correct :  
                    inverted_dict[_type][item] = to_correct_to
    return inverted_dict

# HELPERS '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def _get_delimiter() : 
    return configuration.get_configuration().csv_delimiter
