import unittest, os, gc, logging
from context import kioku
from kioku import db_update
from kioku.japanese.Japanese_DB_handler import Japanese_DB_handler

csv_dir = 'data/190427/patched_3/'


jpDB = Japanese_DB_handler()
print(jpDB)
# if not os.path.exists(jpDB.db_path) : 
	# jpDB.generateDB()
# status, errors = db_update.add_vocab_fromCsv_dir(csv_dir, add_categories = True, add_tags = True)


