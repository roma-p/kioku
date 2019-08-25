import sys, os, csv 
import logging
import sqlite3, datetime, configparser
from shutil import copyfile
from japanese.Japanese_DB_handler import Japanese_DB_handler
import configuration as configuration
import helpers as helpers

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# def _parseConf(): 
#     """
#     return the sections 'kioku' of configuration data 
#     """
#     config_data = configuration.get_configuration()
#     if not config_data : return None
#     return config_data

def _getCsvConf(): pass


def _generateFileName(path, fileName, suffix = ''):
    """
    return string as path + fileName + suffix + current time. 
    """
    now_str = helpers.format_now()
    if suffix : suffix = '_'+ suffix
    return path + '/' + fileName + '_' + now_str + suffix + ".csv"

def _is_cjk(character):
    """"
    Checks whether character is CJK.

        >>> _is_cjk(u'\u33fe')
        True
        >>> _is_cjk(u'\uFE5F')
        False

    :param character: The character that needs to be checked.
    :type character: char
    :return: bool
    """
    return any([start <= ord(character) <= end for start, end in
                [(4352, 4607), (11904, 42191), (43072, 43135), (44032, 55215),
                 (63744, 64255), (65072, 65103), (65381, 65500),
                 (131072, 196607)]
                ])

def _delTrailingSpaces(string): return string.lstrip(' ')

def parse(inputFile, outputDir):

    # getting configuration and BD. 
    db_handler = Japanese_DB_handler()
    #config_data = _parseConf()
    config_data = configuration.get_configuration()
    if not config_data :
        log.error("couldn't find get configuration data")
        return 

    copyfile(inputFile, _generateFileName(config_data.input_files_bk, 'input'))

    f = db_handler.base_format
    existing_kanjis = db_handler.list(f.vocab, f.vocab.word)

    potentialErrors = []
    newEntriesList = []

    # Parsing input file. 
    with open(inputFile, 'r') as fin:
        for row in csv.reader(fin, delimiter='	'):
            # usefull to just get half of the list
            # but question are not necessrely before awnser
            # we forced japanese as row[0]

            word = row[0]
            meaning = row[1]
            prononciation = row[2] if row[2] else ''
            exemple = ''

            if word not in existing_kanjis :
                newEntriesList.append(['','',word, prononciation, meaning, exemple])
            else :
                log.error('already exists : '+word)

    nb_of_files = len(newEntriesList)//100
    if len(newEntriesList)%100 != 0 :
        nb_of_files += 1

    outputDir += '/'
    for nb in range(1, nb_of_files+1, 1):
        fileName = _generateFileName(outputDir, "int", str(nb))
        with open(fileName, 'w') as fout:
            writer = csv.writer(fout, delimiter= '	')
            writer.writerow(['categorie','tag','word','prononciation','meaning','exemple'])
            for entry in newEntriesList[100 * (nb - 1) : 100 * nb] : 
                writer.writerow(entry)

    fileName = _generateFileName(outputDir, "int", '_pottentialErrors')
    with open(fileName, 'w') as fout:
        writer = csv.writer(fout, delimiter= '	')
        for error in potentialErrors:
            writer.writerow(error)
            log.error(error)
    return 

if __name__ == '__main__':
    inputFile = sys.argv[1]
    outputDir = sys.argv[2]
    log.info(inputFile)
    log.info(outputDir)
    parse(inputFile, outputDir)

