import sqlite3
import csv
import glob
import logging
import os
import kioku.configuration as configuration # not useful, copy done in command module
from kioku.DB_handler import DB_handler
import kioku.search

log = logging.getLogger()

# input file qlreqdy format (position value as key)
def add(inputFile):
    
    config_data = configuration.getConfiguration()
    db_handler = DB_handler()
    
    existing_kanjis = list(db_handler.select("vocab", "word"))
    existing_category = list(db_handler.select("categorie", "name"))
    existing_tag = list(db_handler.select("tag", "name"))

    added_categorie = []    # used for detecting siblings and listing categorie to add
    added_tag = []          # used for detecting siblings and listing tag to add
    added_kanjis = []       # used for detecting siblings
    added_word = []         # listing entries to add
    
    error_entries = []         # errors are entries tagged with keyword 'ERROR'

    with open(inputFile, 'r') as fout:
        
        for row in csv.reader(fout, delimiter = '	'):
            if 'ERROR' in row[1] : 
                error_entries.append(row)
            else : 
                if row[0] not in ['categorie', ''] + existing_category + added_categorie : 
                    added_categorie.append(((row[0],)))
                if row[1] not in ['tag', ''] + existing_tag + added_tag : 
                    added_tag.append(((row[1],)))
                if row[2] != 'word' and row[2] not in existing_kanjis + added_kanjis :    
                    added_word.append(tuple(row))
                    added_kanjis.append(row[2])
        
        for base_name, data_list in zip(["categorie", "tag", "vocab"], [added_categorie, added_tag, added_word]) : 
            db_handler.add(base_name, *data_list)

    return error_entries


def add_multiple(inputDir) : 

    all_errors = []

    if not os.path.exists(inputDir):
        log.error('directory not found :' + inputDir)
        return
    elif len(glob.glob(inputDir + "/*.csv")) == 0:
        log.error('no csv found in ' + inputDir)
        return

    added_file = []
    for file in glob.glob(inputDir + "/*.csv"):
        log.info('adding data from : ' + file)
        errors = add(file)
        all_errors += errors
        added_file.append(file)

    return added_file, all_errors


def merge_cat_tag(source, dest, _type) :

    if _type not in search.tag_cat : 
        log.error('authorized types are "tag"/"cat", not : '+str(_type))
        return False

    type_list = search.listTypes(_type)

    errors = []
    for temp in (source, dest) : 
        if temp not in type_list : errors.append(temp)
    if errors : 
        for error in errors : log.error(error + 'not found in '+_type)
        return False

    











