from japanese.Japanese_DB_handler import Japanese_DB_handler

vocab_format = None
vocab_short_format = None

def get_vocab_format(): 
    global vocab_format
    if not vocab_format :
        f = Japanese_DB_handler().base_format
        vocab_format = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning,f.vocab.example)
    return vocab_format

def get_vocab_format_as_string(): 
    return (item() for item in get_vocab_format())

def get_short_vocab_format_as_string() : 
    global vocab_short_format
    if not vocab_short_format :
        f = Japanese_DB_handler().base_format
        vocab_short_format = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning)
    return (item() for item in vocab_short_format)

