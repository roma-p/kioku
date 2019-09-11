kioku 記憶
----------

kioku is a japanese dictionnary build to list/sort vocabulary extracted from anki software in order to facilitate vocabulary study. It will also provides space repetition revision features despite those features not finalized yet. 

kioku was developped with python 3.0, bottle and sqlite3. 

demo version (using some of my own anki decks) available here : ///

**purpose**

> Anki is a free and open-source flashcard program that utilizes spaced repetition. Spaced repetition has been shown to increase rate of memorization.

https://en.wikipedia.org/wiki/Anki_(software)

>Spaced repetition is an evidence-based learning technique that is usually performed with flashcards. Newly introduced and more difficult flashcards are shown more frequently while older and less difficult flashcards are shown less frequently in order to exploit the psychological spacing effect. 

https://en.wikipedia.org/wiki/Spaced_repetition



purpose 
-------

I've been studying japanese / chinese for a few years now and I heavily relied on Anki for learning words and kanjis. But in the process, I struggled with two issuses : 

- When checking in a japanese dictionnary for synonyms or words using a given kanjis, I was overwhelmed by the amount of data I had to navigate around before finding what I wanted... 
- With my decks getting bigger and bigger (when I reached 3000 fashcards), I realized that I was often confusing mnemonics I used for similar cards because the interval of time between their respective revision was very long, despite the two cards were easy to confuse. I occured to me that  I needed cross-revision based on other criterium (eg : words with same/similar kanjis, with similar prononciations, adverbs etc..) in addition to the traditionnal Anki revision.

Therefore, kioku is aiming to provide user with : 

- a dictionnary only inlcuding data from user's anki decks, so user can easily navigate in a web interface every word he ever studied. IF IT IS IN THE DICTIONNARY, USER LEARNT IT, HE SHOULD KNOW IT. 
- an easy way to list those words by : 
    + tag (useally grammatical role)
    + categorie (usually semantic field)
    + kanjis in the word
    + similar prononciation. 
-  offers user features to ceate small flashcard decks based on one of the criterium above, or on the result of a search. 

**On similar prononciations**

I added this feature because I struggled quite a lot on remmembering words itonations. Every words is reduced to a 'core prononciation' : 
- dakuten are removed
- accentuation are also deleted : ぅ and っ
- trailing う are removed
- ょ, ゃ, ゅ, ち replaced by よ, や, ゆ, し

This way user can study words loosely prononced the same, for example 'かし' : 
- 価値 : かち   (Avoir du mérite)
- 火事 : かじ   (incendie)
- 合致 : がっち (agreement, concurrence, conformance, compliance)

If this feature can be overlooked in japanese, its utility seems way more striking in chinese. 

installation
------------

not done yet.

implementation 
--------------

- kioku does not use anki sqlite database but its own, so vocabulary has to be import to kioku. Anki deck are not yet directly importable, user have to use svc export of their vocab to do so. 
- database format is described as a python dictionnary in : japanese/japanese_databaseFormat.py 
- No framework were used to handle the sqlite DB. Instead a custom DB module was created to manage it. It can be used separatly from kioku. The module is 'DB', documented with pydoc. For example, please refers to japanese/Japanese_DB_handler.py (which implements DB/DB_handler.py)
- japanese related section of the program is isolated to simplify the implemtation of a another language



