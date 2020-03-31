import logging
from DB.DB_handler import DB_handler
from japanese import japanese_dataBaseFormat
import configuration as configuration
from DB.Query import Query
from japanese import japanese_helpers
from japanese.VocabContainer import VocabContainer

log = logging.getLogger()

class  Japanese_DB_handler(DB_handler):

    def __init__(self):
        config_data = configuration.get_configuration()      
        if not config_data : return None 
        db_path = config_data.db_path
        base_format = japanese_dataBaseFormat.get_baseFormat()
        super().__init__(db_path, base_format)

    # GETTING DATA ************************************************************
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # LISTING VOCABULARY ******************************************************

    ## TODO : correct with copy paste madness. 

    def list_word_by_kanjis(self, kanji, *fieldToGet, limit = None): 
        f = self.base_format
        if not self._check_field(fieldToGet, f.vocab) : return None
        q = Query().select(f.vocab, *fieldToGet)
        q.join_left(f.vocab.id, f.word_kanjis.word_id)
        q.join_left(f.word_kanjis.kanji_id , f.kanjis.id)
        q.where().equal(f.kanjis.name, kanji)
        if limit : q.limit(limit)
        data = self.executeQuery(q)
        return data

    def list_word_by_core_prononciation(self, core_p, *fieldToGet, limit=None): 
        f = self.base_format
        if not self._check_field(fieldToGet, f.vocab) : return None
        q = Query().select(f.vocab, *fieldToGet)
        q.join_left(f.vocab.core_prononciation, f.core_prononciations.id)
        q.where().equal(f.core_prononciations.name, core_p)
        if limit : q.limit(limit)
        data = self.executeQuery(q)
        return data

    def list_word_by_categorie(self, categorie_name, *fieldToGet, limit=None): 
        f = self.base_format
        if not self._check_field(fieldToGet, f.vocab) : return None
        q = Query().select(f.vocab, *fieldToGet)
        q.join_left(f.vocab.categorie, f.categories.id)
        q.where().equal(f.categories.name, categorie_name)
        if limit : q.limit(limit)
        data = self.executeQuery(q)
        return data

    def list_word_by_tag(self, tag_name, *fieldToGet, limit=None): 
        f = self.base_format
        if not self._check_field(fieldToGet, f.vocab) : return None
        q = Query().select(f.vocab, *fieldToGet)
        q.join_left(f.vocab.tag, f.tags.id)
        q.where().equal(f.tags.name, tag_name)
        if limit : q.limit(limit)
        data = self.executeQuery(q)
        return data

    def list_all_words(self, *fieldToGet, limit=None): 
        f = self.base_format
        if not self._check_field(fieldToGet, f.vocab) : return None
        q = Query().select(f.vocab, *fieldToGet)                
        if limit : q.limit(limit)
        data = self.executeQuery(q)
        return data

    def get_item_by_id(self, table_object, id, *fieldToGet):
        if not self._check_field(fieldTocheck, table_object): return None
        q = Query().select(table_object, *fieldToGet)
        q.where().equal(table_object.id, id)
        data = self.executeQuery(q)
        if data : return data[0]

    def _check_field(self, fieldTocheck, table_object): 
        err_set = set()
        if not fieldTocheck : 
            log.error('no field to select!')
            return False
        for field in fieldTocheck :
            if field.parent_table() != table_object(): 
                err_set.add(field)
        if err_set : 
            log.error('following fields are not in vocab table, cant proceed')
            for field in err_set : log.error(field())
            return False
        return True

    # FETCHING SINGLE WORD INFO ***********************************************

    def get_word_info(self, id): 

        f = self.base_format
        field_to_get = (
            f.vocab.word,
            f.vocab.prononciation, 
            f.vocab.meaning, 
            f.vocab.example, 
            f.vocab.date, 
            f.core_prononciations.name, 
            f.categories.name, 
            f.tags.name)
        q = Query().select(f.vocab, *field_to_get)
        q.join_left(f.vocab.core_prononciation, f.core_prononciations.id)
        q.join_left(f.vocab.categorie, f.categories.id)
        q.join_left(f.vocab.tag, f.tags.id)
        q.where().equal(f.vocab.id , id)

        data = self.executeQuery(q)

        if not data : return None
        else : data = data[0] # words are unique, only one instance possible. 

        output = {
            'id'   : id,
            'word' : data[0],
            'prononciation' : data[1],
            'meaning' : data[2],
            'example' : data[3],
            'date' : data[4],
            'core_prononciation' : data[5],
            'categorie' : data[6],
            'tag' : data[7]
        }

        output['kanjis'] = self.get_kanjis_in_word(data[0])

        return output

    def get_kanjis_in_word(self, word): 

        f = self.base_format
        q = Query().select(f.vocab, f.kanjis.name)
        q.join_left(f.vocab.id, f.word_kanjis.word_id)
        q.join_left(f.word_kanjis.kanji_id, f.kanjis.id)
        q.where().equal(f.vocab.word, word)

        data = self.executeQuery(q)
        kanjis_tuple = tuple([item[0] for item in data])

        return kanjis_tuple


    # LISTING CRITERIUM ********************************************************

    def list_kanjis_by_usage(self, limit = None, offset = None): 
        f = self.base_format
        q = Query().select(f.word_kanjis, f.kanjis.name,
                            count_field=f.word_kanjis.word_id)
        q.join_left(f.word_kanjis.kanji_id, f.kanjis.id)
        q.group_by(f.word_kanjis.kanji_id)
        q.order_by_count(f.word_kanjis.word_id).desc()
        if limit : 
            q.limit(limit, offset)
        data = self.executeQuery(q)
        return data
        #q = Query().select(f.kanjis, f.kanjis.name).count(f.word_kanjis)
        #q,

    def list_categorie_by_usage(self, limit = None, offset = None): 
        f = self.base_format
        q = Query().select(f.vocab, f.categories.name, 
                            count_field=f.vocab.categorie)
        q.join_left(f.vocab.categorie, f.categories.id)
        q.group_by(f.vocab.categorie)
        q.order_by_count(f.vocab.id).desc()
        if limit : 
            q.limit(limit, offset)
        data = self.executeQuery(q)
        return data

    def list_tag_by_usage(self, limit = None, offset = None) :
        f = self.base_format
        q = Query().select(f.vocab, f.tags.name, count_field = f.vocab.id)
        q.join_left(f.vocab.tag, f.tags.id)
        q.group_by(f.vocab.tag)
        q.order_by_count(f.vocab.id).desc()
        if limit : 
            q.limit(limit, offset)
        data = self.executeQuery(q)
        return data        

    def list_core_p_by_usage(self, limit = None, offset = None):
        f = self.base_format
        q = Query().select(f.vocab, f.core_prononciations.name, 
                            count_field=f.vocab.id)
        q.join_left(f.vocab.core_prononciation, f.core_prononciations.id)
        q.group_by(f.vocab.core_prononciation)
        q.order_by_count(f.vocab.id).desc()
        if limit : 
            q.limit(limit, offset)
        data = self.executeQuery(q)
        return data        

    def list_vocab_by_approximative_field(self, key_field, key_value, 
                                        *field_to_get): 
        """
        retrieve data from vocab table, where its key_field IS or CONTAINS key_value
        (but does not auto correct typo, yet)
        returns fields listed in field_to_get
        data are ordered as such : first the perfect match if it exsists
        then data ordered by number of character in addition to key_value

        nota : will not checked for language coherence : 
            - if key_field is 'word' and 'key_value' is in english, 
            will return empty without raising error. 
            - if key_field is 'prononciation' but key_value contains kanjis, 
            will return empty without raising error. 
        so to avoid useless request on database, better check key_field and key_value
        before using this method. s

        : param key_field : a Field object of DB_format, from Japanese_DB_handler.base_format.vocab
        : param key_value : the value of key_field you want to retrieve. 
        : paran *field_to_get : list of Field object of DB_format you want to retrieve, 
                                fields has to be from Japanese_DB_handler.base_format.vocab
        : return : tuple of data fetched that match key_value, sorted as explained before. 

        """

        f = self.base_format


        # TODO : WARNING : what happens if we put field to get twice ? 
        # SQL ? IS THERE FIELDS somewhere ?

        # adding key_field to field_to_get 
        # so field_to_get index in data fetched will be O
        all_field_to_get = (key_field, *field_to_get)


        # 0) checks : 
        # -----------
        # - key_field and field_to_get are fields of Japanese_DB_handler.base_format.vocab


        wrong_field_list = [field for field in all_field_to_get 
            if field.parent_table() != f.vocab()]

        if wrong_field_list : 
            log.error('trying to get field that does not exists in ' 
                + f.vocab() + ':')
            for field in wrong_field_list : 
                log.error(f.vocab() + ' has no field : ' + str(field))
            return None


        # 1) selecting perfect match : 
        # ----------------------------
        q = Query().select(f.vocab, *all_field_to_get)
        q.where().equal(key_field, key_value)
        data = self.executeQuery(q)
        perfect_matches = list(data) if data else None


        # 2) selecting 'like' : 
        # ---------------------

        # TODO : first check key_value + %
        # then search % keyval % but not like key val & 
        # mot commancant par ce caractere la, mieux aue tout grouper independamment de sa position . 

        q = Query().select(f.vocab, *all_field_to_get)
        q.where().like(key_field, '%'+key_value+'%')
        q.and_().not_equal(key_field, key_value)
        data = self.executeQuery(q)
        approximations = list(data) if data else None


        # 3) sorting / presenting data : 
        # ------------------------------

        if perfect_matches : perfect_matches = tuple([data[1:] for data in 
                                                        perfect_matches])

        # sorting data
        if approximations : approximations.sort(key = lambda x:len(x[0]))

        # removing first field (key_field added at beguining of method)
        approximations = tuple([data[1:] for data in approximations]) \
            if approximations else None


        return perfect_matches, approximations

    # CHECKING EXISTENCE ******************************************************

    def check_categorie_existence(self, categorie_name): 
        if categorie_name in dict(self.list_categorie_by_usage()).keys(): 
            return True
        else : return False

    def check_tag_existence(self, tag_name): 
        if tag_name in dict(self.list_tag_by_usage()).keys() : 
            return True
        else : return False

    def check_kanjis_existence(self, kanjis_name): 
        if kanjis_name in dict(self.list_kanjis_by_usage()).keys() : 
            return True
        else : return False

    def check_core_p_existence(self, core_p_name): 
        if core_p_name in dict(self.list_core_p_by_usage()).keys() : 
            return True
        else : return False

    def check_word_existence(self, word): 
        if not japanese_helpers.is_word_japanese(word) : return False
        q = Query().select(self.base_format.vocab, self.base_format.vocab.word)
        q.where().equal(self.base_format.vocab.word, word)
        word = self.executeQuery(queryObject)
        return True if word else False

    # ADDIND DATA *************************************************************
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def add_categories(self, *categorie_list, silent = False): 
        table = self.base_format.categories
        field = self.base_format.categories.name
        self._add_to_db_index(table, field, categorie_list, silent)

    def add_tags(self, *tag_list, silent = False):
        table = self.base_format.tags
        field = self.base_format.tags.name
        self._add_to_db_index(table, field, tag_list, silent)

    def add_kanjis(self, *kanjis_list, silent = False):
        table = self.base_format.kanjis
        field = self.base_format.kanjis.name
        self._add_to_db_index(table, field, kanjis_list, silent)

    def _add_to_db_index(self, table, field, 
                        list_of_index_entries, 
                        silent = False):

        data_order = (field,)
        formatted_data = [(entry,) for entry in set(list_of_index_entries) 
                            if entry and len(entry.strip())]

        existing_list = self.select(table, field)
        duplicate_set = set(existing_list) & set(formatted_data)
        valid_set = set(formatted_data) - set(existing_list)

        if not silent and duplicate_set : 
            log.warning('following data already exists in table/field : ' 
                +table()+ '/'+ field() + ' and will not be added.')
            for data in duplicate_set: 
                log.warning(data[0] + ' already exists.') 
        self.add(table, data_order, *tuple(valid_set))

    def edit_tag(self, previous_name, new_name): 
        if previous_name not in self.list_tag_by_usage(): 
            log.error("no tag found with name: "+previous_name)
            return False
        self.update(f.tags, f.tags.name, 
            new_name, name=previous_name)
        return True

    def edit_cat(self, previous_name, new_name): 
        if previous_name not in self.list_categorie_by_usage(): 
            log.error("no categorie found with name: "+previous_name)
            return False
        self.update(f.categories, f.categories.name, 
            new_name, name=previous_name)
        return True

    def del_tag(self, tag_name): 
        f = self.base_format
        return _del_tag_or_cat(f.vocab.tag, f.tags, tag_name)

    def del_cat(self, cat_name): 
        f = self.base_format
        return _del_tag_or_cat(f.vocab.categorie, f.categories, cat_name)

    def _del_tag_or_cat(self, vocab_field, table, item_name): 
        f = self.base_format
        q = Query().select(table, table.id)
        q.where().equal(table.name, item_name)
        data = self.executeQuery(q)
        if not data : 
            log.error("no item named "+item_name+" found in "+ table())
            return False
        item_id = data[0][0]
        self.delete(table, name=item_name)
        self.update(f.vocab, vocab_field, None, id=item_id)
        return True

    # data expected : 
    # ('word', 'prononciation', 'meaning','categorie','tag', 'example')

    # TODO !! empty tag / categories shant be added to database. 

    def add_vocab(self, *vocab_list, mendatory_prononciation = True):
        data_order = ('word', 'prononciation', 'core_prononciation',
            'meaning','example','categorie','tag')

        # 1) listing existing categorie, tag to ensure foreign key constraints * 
        existing_cat_tuple = self.list(self.base_format.categories, 
                                        self.base_format.categories.name)
        existing_tag_tuple = self.list(self.base_format.tags, 
                                        self.base_format.tags.name)

        # TODO NOT CHECKING UNICITY / NOT NULL ? 

        # 2) rejecting empty mendatory fields, checking foreign key constraints 
        #    else : listing kanjis and generating core pronomciation.
        #           and listing them to update kanjis/core_prononciation tables 
        error_list = []
        warning_list = []

        vocab_container_list = []
        kanjis_detected_set = set()
        core_p_detected_set = set()
        word_set = set()

        for vocab in vocab_list : 
            word, prononciation, meaning, categorie, tag, example = vocab

            status = self._add_word_basic_checks(
                existing_cat_tuple,
                existing_tag_tuple,
                word, meaning, 
                categorie, tag)

            if not status : 
                error_list.append(vocab)
            elif word in word_set : 
                log.error('duplicate item found : word ' + word + '.' )
                warning_list.append(vocab)
            else : 

                vocab_container = self._add_word_gen_vocab_container(
                    word, meaning, prononciation, 
                    categorie, tag, example)

                if not vocab_container:
                    error_list.append(vocab)
                else: 
                    word_set.add(word)
                    core_p_detected_set.add(vocab_container.core_P)
                    kanjis_detected_set.update(set(vocab_container.kanjis))
                    vocab_container_list.append(vocab_container)

        if warning_list : 
            log.warning('following entries were ignored because of an error : ')
            for warning in warning_list : 
                log.warning(str(warning))

        if error_list: 
            log.error('errors detected in vocab list for following etnries, db not updated : ')
            for error in error_list : 
                log.error(str(error))
            return False

        # 3) updating kanjis / core_prononciations tables *********************
        existing_kanjis_set = set(self.list(
                                        self.base_format.kanjis, 
                                        self.base_format.kanjis.name))
        existing_core_p_set = set(self.list(
                                        self.base_format.core_prononciations, 
                                        self.base_format.core_prononciations.name))

        kanjis_to_add_tuple = tuple([(k, ) for k in kanjis_detected_set 
                                        - existing_kanjis_set])
        core_p_to_add_list = tuple([(p, ) for p in core_p_detected_set 
                                        - existing_core_p_set])

        self.add(self.base_format.kanjis, 
                    (self.base_format.kanjis.name,), 
                    *kanjis_to_add_tuple)
        self.add(self.base_format.core_prononciations , 
                    (self.base_format.core_prononciations.name,), 
                    *core_p_to_add_list)

        # 4) generating the entries that will be add to the database. *********

        # following dicts used to get matching id for cat / tag / core_p / kanjis. 
        existing_cat_dict = self._get_index_as_dict(self.base_format.categories)
        existing_tag_dict = self._get_index_as_dict(self.base_format.tags)
        existing_core_p_dict = self._get_index_as_dict(self.base_format.core_prononciations)
        existing_kanjis_dict = self._get_index_as_dict(self.base_format.kanjis)
        word_id_dict = self._get_index_as_dict(self.base_format.vocab, 
                                               self.base_format.vocab.word)

        vocab_final_entries_list = []
        word_kanjis_tmp_entries_dict = {} # < word > : list of kanjis id. 

        # generating final entries for table vocab and tmp entries for word kanjis. 
        for vc in vocab_container_list : 
            #word, prononciation, core_prononciation, meaning, example, categorie, tag, kanjis_list = tmp_entry
            core_p_id = existing_core_p_dict[vc.core_p]
            tag_id    = existing_tag_dict[vc.tag]       if vc.tag else None         # TODO ; shall be equal to None. 
            cat_id    = existing_cat_dict[vc.categorie] if vc.categorie else None

            word_kanjis_tmp_entries_dict[vc.word] = [existing_kanjis_dict[kanji] 
                                                        for kanji in vc.kanjis]
            vocab_final_entries_list.append((
                vc.word,
                vc.prononciation, 
                core_p_id,
                vc.meaning, 
                vc.example,
                cat_id,
                tag_id))

        # 5) updating vocab table. 
        data_order = (
            'word',
            'prononciation',
            'core_prononciation',
            'meaning',
            'example',
            'categorie',
            'tag')
        
        self.add(
            self.base_format.vocab,
            data_order,
            *vocab_final_entries_list)

        # 6) updating word_kanjis tables. 

        word_kanjis_final_entries_list = []
        for word, kanjis_id_tuple in word_kanjis_tmp_entries_dict.items() : 
            for kanji_id in kanjis_id_tuple : 
                word_kanjis_final_entries_list.append(
                                                (word_id_dict[word],
                                                kanji_id))
        data_order = (self.base_format.word_kanjis.word_id, 
                      self.base_format.word_kanjis.kanji_id)
        self.add(
            self.base_format.word_kanjis,
            data_order,
            *word_kanjis_final_entries_list)
        return True

    def add_single_word(self, word, prononciation, meaning, 
                        example   = None, 
                        categorie = None, 
                        tag       = None):
        return self.add_vocab((
            word,
            prononciation, 
            meaning, 
            categorie, 
            tag, 
            example))

    # word_id : integer id of vocab table.
    def update_word(self, word_id, **updated_fields):
        f = self.base_format
        
        valid_fields = (
            f.vocab.word, 
            f.vocab.prononciation,
            f.vocab.meaning, 
            f.vocab.categorie, 
            f.vocab.tag, 
            f.vocab.example)

        word_data = self.get_item_by_id(
            f.vocab, 
            word_id, 
            *valid_fields)

        if not word_data: 
            log.error('no word found at id '+str(word_id))
            return False

        updated_data = {}
        for field, orig_data in zip(valid_fields, word_data): 
            if field() in updated_fields.keys(): 
                updated_data[field] = updated_fields[field()]
            else : 
                updated_data[field] = orig_data

        existing_cat_tuple = self.list(self.base_format.categories, 
                                        self.base_format.categories.name)
        existing_tag_tuple = self.list(self.base_format.tags, 
                                        self.base_format.tags.name)            

        if not self._add_word_basic_checks(
                existing_cat_tuple,
                existing_tag_tuple, 
                updated_data[f.vocab.word], 
                updated_data[f.vocab.meaning],
                updated_data[f.vocab.categorie],
                updated_data[f.vocab.tag]) : 
            log.error("can't update word info for " + str(word_id))
            return False

        err_mess = 'error during update process of word at id '+ str(word_id)

        if not self.del_word(word_id) : 
            log.error(err_mess)
            return False

        if not self.add_single_word(
                updated_data[f.vocab.word], 
                updated_data[f.vocab.prononciation], 
                updated_data[f.vocab.meaning],
                updated_data[f.vocab.categorie],
                updated_data[f.vocab.tag],
                updated_data[f.vocab.example]): 
            log.error(err_mess)
            return False

        return True

    # word_id = int, id of vocab id. 
    def del_word(self, word_id):
        f = self.base_format
        word_data = self.get_item_by_id(f.vocab, word_id, f.vocab.word)
        if not word_data: 
            log.error('no word found at id '+str(word_id))
            return False
        self.delete(f.vocab, id=word_id)
        self.delete(f.word_kanjis, word_id=word_id)
        return True

    def _add_word_basic_checks(
            existing_cat_tuple, 
            existing_tag_tuple, 
            word=None,
            meaning=None,
            categorie=None,
            tag=None): 

        valid = True
        if not word : 
            log.error('missing word for entries with prononciation : '
                + str(prononciation))
            valid = False 
        if not meaning : 
            log.error('missing meaning for word : '+ str(word))
            valid = False
        if categorie and categorie not in existing_cat_tuple : 
            log.error("can't add "+ word + ", categorie " 
                + categorie + " does not exists.")
            valid = False
        if tag and tag not in existing_tag_tuple : 
            log.error("can't add "+ word + ", tags " + tag
                + " does not exists.")
            valid = False
        return valid

    def _add_word_gen_vocab_container(
            self, word, meaning, 
            prononciation=None,
            categorie=None,
            tag=None,
            example=None): 

        # generating core prononciation
        # if not prononciation : hiragana_word = word 
        # else : hiragana_word = prononciation

        hiragana_word  = word if not prononciation else prononciation
        hiragana_word  = japanese_helpers.convertKanaToHiragana(hiragana_word)
        valid_hiragana = japanese_helpers.is_word_kana(hiragana_word)

        # TODO : wird if, to investigate...
        if not valid_hiragana : 
            log.error('prononciation / word not in kana : '+ str(word))
            if mendatory_prononciation : 
                error_list.append(vocab)
            core_prononciation = None
            return None
       
        core_p = japanese_helpers.gen_core_prononciation(hiragana_word)
        kanjis_tuple = japanese_helpers.list_kanjis(word)

        return VocabContainer(
            word=word,
            prononciation=prononciation, 
            core_p=core_p,
            meaning=meaning,
            example=example,
            categorie=categorie,
            tag=tag,
            kanjis=kanjis_tuple)

    def _get_index_as_dict(self, tableObject, field_to_set_as_key = None):
        if not field_to_set_as_key : field_to_set_as_key = tableObject.name 
        item_to_get = [field_to_set_as_key, tableObject.id]
        data_as_dict = {id : name for (id, name) in 
                            self.select(tableObject, *item_to_get)}
        return data_as_dict


    # DB STAT *****************************************************************
    # '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    def get_db_stat(self): 
        row_limit = 10 
        stat_dict = {}
        stat_dict['vocab_number'] = self.count(self.base_format.vocab)
        stat_dict['categories_number'] = self.count(self.base_format.categories)
        stat_dict['tags_number'] = self.count(self.base_format.tags)
        stat_dict['kanjis_number'] = self.count(self.base_format.kanjis)
        stat_dict['core_p_number'] = self.count(
                                        self.base_format.core_prononciations)
        stat_dict['most_used_categories'] = self.list_categorie_by_usage(
                                                limit = row_limit)
        stat_dict['most_used_tags'] = self.list_tag_by_usage(
                                                limit = row_limit)
        stat_dict['most_used_kanjis'] = self.list_kanjis_by_usage(
                                                limit = row_limit)
        stat_dict['most_used_core_p'] = self.list_core_p_by_usage(
                                                limit = row_limit)
        return stat_dict






