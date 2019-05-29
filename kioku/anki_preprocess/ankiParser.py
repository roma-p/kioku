import sys, os, csv 
import sqlite3, datetime, configparser
from shutil import copyfile
from DB_handler import DB_handler
import configuration as configuration
import helpers as helpers


def _parseConf(): 
    """
    return the sections 'kioku' of configuration data 
    """
    config_data = configuration.getConfiguration()
    if not config_data : return None
    return config_data._sections['kioku']

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

    
    db_handler = DB_handler()
    config_data = _parseConf()

    copyfile(inputFile, _generateFileName(config_data['input_files_bk'], 'input'))

    existing_kanjis = db_handler.select("vocab", "word")

    potentialErrors = []
    newEntriesList = []

    # Parsing input file. 
    with open(inputFile, 'r') as fin:
       for row in csv.reader(fin, delimiter='	'):
            # usefull to just get half of the list
            # but question are not necessrely before awnser
            if row[2] == 'Card 1':

                # separating French from Japanese
                if _is_cjk(row[0][0]):
                    japanese = row[0]
                    french = row[1]
                else:
                    japanese = row[1]
                    french = row[0]

                # 3 cases :
                # 1, juste kana
                # 2, a bunch of kanji and kana prononciation
                # 3, 2 + a sentence exemple.

                # 1) no kanjis
                if '  ' not in japanese:
                    word = japanese
                    prononciation = ''
                    exemple = ''

                else:
                    potentialKanjis, afterKanjis = japanese.split(' ', 1)

                    # remove trailing spaces.
                    afterKanjis = _delTrailingSpaces(afterKanjis)

                    if afterKanjis[:2] == 'する':
                        potentialKanjis += ' (する)'
                        afterKanjis = _delTrailingSpaces(afterKanjis[2:])

                    if afterKanjis[:2] == 'な ':
                        potentialKanjis+= ' (な)'
                        afterKanjis = _delTrailingSpaces(afterKanjis[1:])

                    # x) Potentials errors : Full phrase.
                    if len(potentialKanjis) > 7:
                        log.error('potential error :' + potentialKanjis)
                        potentialErrors.append(row)

                    # 2) just kanjis and prononciation
                    elif '   ' not in afterKanjis:
                        word = potentialKanjis
                        prononciation = _delTrailingSpaces(afterKanjis)
                        exemple = ''

                    # 3) kanjis prononciation and exemple
                    else:
                        word = potentialKanjis
                        prononciation, exemple = afterKanjis.split('  ', 1)
                        prononciation = _delTrailingSpaces(prononciation)
                        exemple = _delTrailingSpaces(exemple)


                if word not in existing_kanjis :
                    newEntriesList.append(['','',word, prononciation, french, exemple])
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
