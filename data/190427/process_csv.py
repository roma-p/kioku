import unittest, os, gc, logging
from context import kioku
from kioku.anki_preprocess import csv_tag_cat_preprocess

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

data_dir = 'data/190427/'
original_dir = data_dir + 'original/'
patched_dir  = data_dir + 'patched/'

csv_existing_cat, csv_new_cat, csv_existing_tag, csv_new_tag = csv_tag_cat_preprocess.list_cat_tag_from_csv_dir(original_dir)

#print(sorted(list(csv_new_tag)))

correction_dict = {
	'categories' : {
		'circulation' : {'circulation '}, 
		'colour' : {'color'},
		'invitation' : {'invitation '},
		'judgment' : {'judgement'},
		'location' : {'loca','location '},
		'lot' : {'lot '},
		'mental' : {'mental '},
		'surprise' : {'surpise','surprised'}
	}, 
	'tags' : {
		'TODO' : {'!!','??','Up ???','coom'}
	}
}

log.info('patching CSV : ')
log.info(' ')
csv_tag_cat_preprocess.patch_cat_tag_csv_dir(original_dir, patched_dir, correction_dict)
log.info('patched.')
csv_existing_cat, csv_new_cat_, csv_existing_tag, csv_new_tag_ = csv_tag_cat_preprocess.list_cat_tag_from_csv_dir(patched_dir, log_info = True)

print(sorted(list(csv_new_cat_)))
print(sorted(list(csv_new_tag_)))