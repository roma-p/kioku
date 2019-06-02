from japanese.Japanese_DB_Handler import Japanese_DB_handler

vocab_format = None
def get_vocab_format(): 
    global vocab_format
    if not vocab_format :
        f = Japanese_DB_handler().base_format
        vocab_format = (f.vocab.word,f.vocab.prononciation,f.vocab.meaning,f.vocab.example)
    return vocab_format
