import unittest, os, gc, logging
from context import kioku
from kioku.DB.Japanese_DB_handler import Japanese_DB_handler

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

jpDB = Japanese_DB_handler()
stat_dict = jpDB.get_db_stat()

indent = '  '

for stat_dict_key in ['vocab_number', 'categories_number', 'tags_number', 'kanjis_number'] : 
    table_name = stat_dict_key.split('_')[0]
    log.info(str(stat_dict[stat_dict_key]) + ' ' + table_name)
for stat_dict_key in ['most_used_categories', 'most_used_tags', 'most_used_kanjis', 'most_used_core_p'] : 
    table_name = stat_dict_key.split('-')[-1]
    log.info('most used '+table_name+ ' are : ')
    for (data_id, data_usage_count) in stat_dict[stat_dict_key] : 
        if data_id : 
            log.info(indent + data_id + ' : ' + str(data_usage_count))

# all_kanjis_list = jpDB.list_kanjis_by_usage()
# relevant_kanjis_list = [item for item in all_kanjis_list if item[1] != 1]
# for item in relevant_kanjis_list : 
#   log.info(item)