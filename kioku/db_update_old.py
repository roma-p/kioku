import sqlite3
import csv
import glob
import logging
import os
import kioku.configuration as configuration # not useful, copy done in command module
from kioku.DB_handler import DB_handler
import kioku.search
from  kioku import japanese_dataBaseFormat as jFormat
from kioku.japanese import japanese_helpers

log = logging.getLogger()

## TODO : KANJIS CAT !!! AND ASSOCIATION OF DATA
## NEED TO LEARN MORE ABOUT OPTI:IWE BDD MANAGEMENT. 
## ALSO REFERENCE SIMILAR PRONOMCIATION 

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




# CAT SUIVANTE PR RENDRE LE SOFT PLUS UTILISABLE>>
# UN UPDATE UN DELETE...



def merge_cat_tag(source, dest, _type) :

    if _type not in search.tag_cat : 
        log.error('authorized types are "tag"/"cat", not : '+str(_type))
        return False

    errors = []
    type_list = search.listTypes(_type)
    for temp in (source, dest) : 
        if temp not in type_list : errors.append(temp)
    if errors : 
        for error in errors : log.error(error + 'not found in '+_type)
        return False

    
# /////////////////////// REFACTORING /////////////////////////////////////////


def add_vocab_from_csv(fileList) : 

    # data_order : name to id for vocab_data. 
    data_order, vocab_data = _getVocabFromFileList(fileList)
    exiting_word = DB_handler.list('vocab', 'word')
    exiting_tag  = DB_handler.list('tag', 'name')
    existing_cat = DB_handler.list('categorie', 'name')

    added_vocab = set()
    added_cat = set()
    added_tag = set()
    added_kanjis = set()
    added_simplified_p = set()

    detected_error = set()

    colName2Id = {} # field name to id in the database. 
    for i, colName in zip(len(range(len(data_order))), data_order) : 
        colName2Id[colName] = i 

    for data in vocab_data : 
        newRow = []

    pass

def _getVocabDataFromFile(filePath) : 
    # return dict for all vocab tables and a tab of order. 
    # specific of get fromDir


    # NON GLOB FQIT DANS COMMNAND. 
    pass

def _getVocabDataFromDir(dirPath) : 


    pass

def _getVocabFromFileList(fileList) :

    #vrai point d'entree
    word_set = {}
    vocab_set = {}
    data_order = jFormat.get_vocab_required_col()

    for file in fileList : 
        with open(file, 'r') as fout : 
            readerObj = csv.reader(fout, delimiter = '	')
            colFormat = _getColFormat(next(readerObj))
            if not colFormat : 
                log.error("couldn't figure out format of file : "+file)
                return None
            for row in readerObj : 
                if row[colFormat['word']] not in word_set + [''] :
                    word_set.append(row[colFormat['word']])
                    vocab_set.append(tuple(_format_row(row, data_order, col_format))) 
    return data_order, vocab_set

def _format_row(row, data_order, col_format) : 

    formatted_row = []
    for col in data_order : 
        col_id = col_format[col]
        formatted_row.append(row[col_id])
    return formatted_row

def _getColFormat(firstRowOfFile) : 

    required_col = jFormat.get_vocab_required_col()

    missingCol = set(required_col) - set(firstRowOfFile)
    extraCol = set(firstRowOfFile) - set(required_col)

    if len(missingCol) : 
        log.error('missing rows in file : '+str(missingCol))
        return None
    elif len(extraCol) : 
        log.warning("extra rows on file, won't be processed : "+str(extraCol)) 

    colName2Id = {}
    for i, colName in zip(range(len(firstRowOfFile)), firstRowOfFile) : 
        if colName in required_col : 
            colName2Id[colName] = i
    return colName2Id

def _filterExistingVocab()

    pass

def _addVocabToDatabase()


    # gen core pronomciation 
    # extraire et lister tout les kanjis


    pass

def fill_vocab(row) :

    jp =  Japanese_DB_handler()

    assocation = {
        jp.base_format.vocab.simpplified_p }
    pass


# HOW DO I ENSURE THAT MODIFYING A DATA WILL NOT CAUSE ENUMERATE TO BE WRONG. 

# -> called at every start of kioku?
# or called on event? 
# in a dict such as : method as key, value = every field filled with the method. 
# if new field detected, backup DB and then try to find the field in values 
# and execute the method stored as key. 
# 

# generate simplified_p of vocab table and MAJ simplified_p table
def update_simplified_p() : pass

    db_handler = DB_handler()
    f = db_handler.base_format
    condition  = {f.vocab.simplified_p = None}
    vocab_data = db_handler.select(f.vocab, f.vocab.id, f.vocab.word, f.vocab.pronomciation, **condition)
    existing_simplified_p_list = db_handler.list(f.simplified_p, f.name)

    simplified_p_parsed = {}
    for _id, _word, _prononciation in vocab_data : 
        _simplified_p = japanese_helpers.gen_core_prononciation(_prononciation) : 
        if not _simplified_p : 
            log.error("couldn't achieve simplified pronomciation for "+_word+" :" +_prononciation+" ("+_id+")")
        else : 
            db_handler.update(f.vocab, f.vocab.simplified_p, id = _id)
            simplified_p_parsed.add(_simplified_p)

    entries_to_add = simplified_p_parsed - set(existing_simplified_p_list)
    entries_to_dlt = set(existing_simplified_p_list) - simplified_p_parsed

    db_handler.add(f.simpplified_p, (f.simplified_p.name,), (entries_to_add))
    c = {f.simplified_p.name : entries_to_dlt}
    db_handler.delete(f.simplified_p, **c)

    #DB HANDLER SHALL HANDLE IN CONDITIONS / CHECK EMPTY. 

# MAJ categorie table
def update_categorie() : pass
    # diff entre set() de cat de vocab et set de la table cat
#  MAJ tag table
def update_tag() : pass
    # diff entre set() de cat de vocab et set de la table cat
#  MAJ kanjis and word_kanjis table
def update_kanjis() : pass 

def _update_enumarateTable(actual_state, state_to_achieve) : 
    pass

# Update method check this dictionnary. 
# Add method : first fiells the 'by hand' field
# then calls every of those methods. s

f = DB_handler.base_format
update_method = {
    update_simplified_p() : (f.vocab.simplified_p, f.simplified_p.name),
    update_categorie() : (f.categorie.name,),
    update_tag() : (f.tag.name,),
    update_kanjis() : (f.word_kanjis.word_id, f.word_kanjis.kanjis)
}



