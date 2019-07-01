import csv, glob, logging, os
from japanese.Japanese_DB_handler import Japanese_DB_handler
from japanese import japanese_dataBaseFormat
import configuration as configuration

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def add_vocab_fromCsv_dir(csv_dir, add_categories = False, add_tags = False) : 

    if not os.path.exists(csv_dir) : 
        log.error('directory do not exist : '+ csv_dir)
        return
    input_file_list = glob.glob(csv_dir + '/*.csv')
    if not input_file_list : 
        log.error('no csv file found in ' + csv_dir)
        return

    return _add_vocab_fromCsv_dir(input_file_list, add_categories, add_tags)


def _add_vocab_fromCsv_dir(csv_file_list, add_categories, add_tags) : 

    cat_in_csv = set()
    tag_in_csv = set()
    vocab_entries = set()

    error_entries = []

    fields = ['categorie', 'tag', 'word', 'prononciation', 'meaning', 'example']
    delimiter = _get_delimiter()
    delimiter = "	"

    for file in csv_file_list : 
        with open(file, 'r') as csv_file : 
            reader = csv.DictReader(csv_file, fieldnames = fields, delimiter = delimiter)
            for row in reader : 
                if row['tag'] != 'tag' : 
                    if "ERROR" in row['tag'] : 
                        error_entries.append(_format_row(row))
                    else : 
                        cat_in_csv.add(row['categorie'])    
                        tag_in_csv.add(row['tag'])
                        vocab_entries.add(_format_row(row))

    jpDb = Japanese_DB_handler()

    if add_categories : 
        jpDb.add_categories(*tuple(cat_in_csv), silent = True)
    if add_tags : 
        jpDb.add_tags(*tuple(tag_in_csv), silent = True)
    status = jpDb.add_vocab(*tuple(vocab_entries))

    return status, error_entries

def _format_row(row) : 
    formatted_tuple = (
            row['word'],
            row['prononciation'],
            row['meaning'],
            row['categorie'],
            row['tag'],
            row['example']
        )
    return formatted_tuple

# HELPERS '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def _get_delimiter() : 
    return configuration.get_configuration().csv_delimiter
