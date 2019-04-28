import logging
from kioku.DB.DB_handler import DB_handler
from kioku.DB import japanese_dataBaseFormat
import kioku.configuration as configuration
from kioku.DB.Query import Query
from kioku.japanese import japanese_helpers


log = logging.getLogger()

class  Japanese_DB_handler(DB_handler):

    def __init__(self):

        config_data = configuration.getConfiguration()      
        if not config_data : return None 
        db_path = config_data.get('kioku', 'db_path')
        base_format = japanese_dataBaseFormat.get_baseFormat()
        super().__init__(db_path, base_format)


    # TODO : NOT WORKING ANYMORE, MULTIPLE JOIN ON SINGLE QUERY? 
    def list_word_by_kanjis(self, kanji) : 
        f = self.base_format
        q = Query().select(f.vocab, f.vocab.word)
        q.join_left(f.vocab.id, f.word_kanjis.word_id)
        q.join_left(f.word_kanjis.kanji_id , f.kanjis.id)
        q.where().equal(f.kanjis.name, kanji)

        data = self.executeQuery(q)
        wordList = tuple([item[0] for item in data])
        return wordList

    def list_word_by_categorie(self, categorie_name) : 
        f = self.base_format
        q = Query().select(f.vocab, f.vocab.word)
        q.join_left(f.vocab.categorie, f.categories.id)
        q.where().equal(f.categories.name, categorie_name)

        data = self.executeQuery(q)
        wordList = tuple([item[0] for item in data])
        return wordList

    def add_categories(self, *categorie_list, silent = False) : 
        table = self.base_format.categories
        field = self.base_format.categories.name
        self._add_to_db_index(table, field, categorie_list, silent)

    def add_tags(self, *tag_list, silent = False) :
        table = self.base_format.tags
        field = self.base_format.tags.name
        self._add_to_db_index(table, field, tag_list, silent)

    def add_kanjis(self, *kanjis_list, silent = False) :
        table = self.base_format.kanjis
        field = self.base_format.kanjis.name
        self._add_to_db_index(table, field, kanjis_list, silent)

    def _add_to_db_index(self, table, field, list_of_index_entries, silent = False):

        data_order = (field,)
        formatted_data = [(entry,) for entry in set(list_of_index_entries)]

        existing_list = self.select(table, field)
        duplicate_set = set(existing_list) & set(formatted_data)
        valid_set = set(formatted_data) - set(existing_list)

        if not silent and duplicate_set : 
            log.warning('following data already exists in table/field : ' +table()+ '/'+ field() + ' and will not be added.')
            for data in duplicate_set: 
                log.warning(data[0] + ' already exists.') 
        self.add(table, data_order, *tuple(valid_set))

    # data expected : 
    # ('word', 'prononciation', 'meaning','categorie','tag', 'example')
    def add_vocab(self, *vocab_list, mendatory_prononciation = True) :
        data_order = ('word', 'prononciation', 'core_prononciation',
            'meaning','example','categorie','tag')

        # 1) listing existing categorie, tag to ensure foreign key constraints * 
        existing_cat_tuple = self.list(self.base_format.categories, self.base_format.categories.name)
        existing_tag_tuple = self.list(self.base_format.tags, self.base_format.tags.name)

        # TODO NOT CHECKING UNICITY / NOT NULL ? 

        # 2) rejecting empty mendatory fields, checking foreign key constraints 
        #    else : listing kanjis and generating core pronomciation.
        #           and listing them to update kanjis/core_prononciation tables 
        error_list = []
        vocab_tmp_entries_list = []
        kanjis_detected_set = set()
        core_p_detected_set = set()
        for vocab in vocab_list : 
            word, prononciation, meaning, categorie, tag, example = vocab
            valid = True
            # 1 : first : checking validity of single data.
            if not word : 
                log.error('missing word for entries with prononciation : '+ str(prononciation))
                error_list.append(vocab)
                valid = False 
            if not meaning : 
                log.error('missing meaning for word : '+ str(word))
                error_list.append(vocab)
                valid = False
            if categorie and categorie not in existing_cat_tuple : 
                log.error("can't add "+ word + ", categorie " + categorie + " does not exists.")
                error_list.append(vocab)
                valid = False
            if tag and tag not in existing_tag_tuple : 
                log.error("can't add "+ word + ", tags " + tag + " does not exists.")
                error_list.append(vocab)
                valid = False
            # 2 generating core pronomciation, extracting kanjis. 
            if valid :
                # generating core prononciation
                # if not prononciation : hiragana_word = word 
                # else : hiragana_word = prononciation
                hiragana_word = word if not prononciation else prononciation # TODO word?
                hiragana_word = japanese_helpers.convertKanaToHiragana(hiragana_word)
                valid_hiragana = japanese_helpers.is_word_kana(hiragana_word)
                if not valid_hiragana : 
                    log.error('prononciation / word not in kana : '+ str(word))
                    error_list.append(vocab)
                    if mendatory_prononciation : 
                        error_list.append(vocab)
                    core_prononciation = None
                else : 
                    core_prononciation = japanese_helpers.gen_core_prononciation(hiragana_word)
                    core_p_detected_set.add(core_prononciation)

                # listing kanjis present in the word
                kanjis_tuple = japanese_helpers.list_kanjis(word)
                kanjis_detected_set.update(set(kanjis_tuple))
                vocab_tmp_entry = (word, prononciation, core_prononciation, meaning, example, categorie, tag, kanjis_tuple)
                vocab_tmp_entries_list.append(vocab_tmp_entry)

        if error_list or not valid: 
            log.error('errors detected in vocab list for following etnries, db not updated : ')
            for error in error_list : 
                log.error(str(error))
            return False

        # 3) updating kanjis / core_prononciations tables *********************
        existing_kanjis_set = set(self.list(self.base_format.kanjis, self.base_format.kanjis.name))
        existing_core_p_set = set(self.list(self.base_format.core_prononciations, self.base_format.core_prononciations.name))

        kanjis_to_add_tuple = tuple([(k, ) for k in kanjis_detected_set - existing_kanjis_set])
        core_p_to_add_list = tuple([(p, )for p in core_p_detected_set - existing_core_p_set])

        self.add(self.base_format.kanjis, (self.base_format.kanjis.name,), *kanjis_to_add_tuple)
        self.add(self.base_format.core_prononciations , (self.base_format.core_prononciations.name,), *core_p_to_add_list)

        # 4) generating the entries that will be add to the database. *********

        # following dicts used to get matching id for cat / tag / core_p / kanjis. 
        existing_cat_dict = self._get_index_as_dict(self.base_format.categories)
        existing_tag_dict = self._get_index_as_dict(self.base_format.tags)
        existing_core_p_dict = self._get_index_as_dict(self.base_format.core_prononciations)
        existing_kanjis_dict = self._get_index_as_dict(self.base_format.kanjis)

        vocab_final_entries_list = []
        word_kanjis_tmp_entries_dict = {} # < word > : list of kanjis id. 

        # generating final entries for table vocab and tmp entries for word kanjis. 
        for tmp_entry in vocab_tmp_entries_list : 
            word, prononciation, core_prononciation, meaning, example, categorie, tag, kanjis_list = tmp_entry
            core_prononciation_id = existing_core_p_dict[core_prononciation]
            categorie_id = existing_cat_dict[categorie]
            tag_id = existing_tag_dict[tag] if tag else None # TODO ; shall be equal to None. 
            word_kanjis_tmp_entries_dict[word] = [existing_kanjis_dict[kanji] for kanji in kanjis_list]
            vocab_final_entries_list.append((word, prononciation, core_prononciation_id, meaning, example, categorie_id, tag_id))

        # 5) updating vocab table. 
        data_order = ('word', 'prononciation', 'core_prononciation','meaning','example','categorie','tag')
        self.add(self.base_format.vocab , data_order, *vocab_final_entries_list)

        # 6) updating word_kanjis tables. 
        word_id_dict = self._get_index_as_dict(self.base_format.vocab, self.base_format.vocab.word)
        word_kanjis_final_entries_list = []
        for word, kanjis_id_tuple in word_kanjis_tmp_entries_dict.items() : 
            for kanji_id in kanjis_id_tuple : 
                word_kanjis_final_entries_list.append((word_id_dict[word],kanji_id))
        data_order = (self.base_format.word_kanjis.word_id, self.base_format.word_kanjis.kanji_id)
        self.add(self.base_format.word_kanjis , data_order, *
            word_kanjis_final_entries_list)

        return True

    def _get_index_as_dict(self, tableObject, field_to_set_as_key = None) :
        if not field_to_set_as_key : field_to_set_as_key = tableObject.name 
        item_to_get = [field_to_set_as_key, tableObject.id]
        data_as_dict = {id : name for (id, name) in self.select(tableObject, *item_to_get)}
        return data_as_dict

    