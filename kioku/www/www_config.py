from japanese.Japanese_DB_handler import Japanese_DB_handler

db_format    = None
vocab_format = None
vocab_short_format = None

def _get_DB_format(): 
    global db_format
    if not db_format: db_format = Japanese_DB_handler().base_format
    return db_format

def get_vocab_format(): 
    global vocab_format
    if not vocab_format :
        f = _get_DB_format()
        vocab_format = (f.vocab.word,f.vocab.prononciation,
                        f.vocab.meaning,f.vocab.example)
    return vocab_format

def get_vocab_format_as_string(): 
    return (item() for item in get_vocab_format())

def get_short_vocab_format_as_string() : 
    global vocab_short_format
    if not vocab_short_format :
        f = _get_DB_format()
        vocab_short_format = (f.vocab.word,f.vocab.prononciation,
                              f.vocab.meaning)
    return (item() for item in vocab_short_format)

def get_vocab_format_including_id(): 
    tmp = list(get_vocab_format())
    tmp.insert(0, _get_DB_format().vocab.id)
    return tuple(tmp)
