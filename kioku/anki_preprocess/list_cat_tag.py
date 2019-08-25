import logging
import os
import sys
import csv
from japanese.Japanese_DB_handler import Japanese_DB_handler
import configuration as configuration

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

output_dir = sys.argv[1]
if not os.path.exists(output_dir) : 
    log.error('directory not found : ' + str(output_dir))
    sys.exit(1)

jpDB = Japanese_DB_handler()
f = jpDB.base_format
config_data = configuration.get_configuration()

if not config_data :
    log.error("couldn't find get configuration data")
    sys.exit(1)

cat_dir = {}
tag_dir = {}

cat_list = jpDB.list_categorie_by_usage()
tag_list = jpDB.list_tag_by_usage()

for cat, _  in cat_list :
    if not cat : continue
    cat_dir[cat] = [data[0] for data in jpDB.list_word_by_categorie(cat, f.vocab.word, limit = 5)]

for tag, _ in tag_list : 
    if not tag : continue
    tag_dir[tag] = [data[0] for data in jpDB.list_word_by_tag(tag, f.vocab.word, limit = 5)]

def _write_csv(file_name, data_dict) : 
    output_path = output_dir + '/' + file_name
    with open(output_path, 'w') as fout :
        writer = csv.writer(fout, delimiter = '	') 
        for name, examples in data_dict.items() :
            line = [name, *examples]
            writer.writerow(line)

_output_list = (
    (cat_dir, 'categorie_index.csv'),
    (tag_dir, 'tag_index.csv'),
    )

for data_dict, file_name in _output_list : 
    _write_csv(file_name, data_dict)