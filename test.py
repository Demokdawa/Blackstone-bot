import re

word_set = ["encule", "pute", "salope", "saloppe", "connard", "pd", "nique", "petasse", "batar", "batard",
                "connasse", "enculé", "pédé", "put*", "sallope", "salloppe", "conard", "battar", "battard", "trouduc",
                "pétasse", "fdp", "tamer", "tg", "ftg", "fuck", "merde", "fck", "putain", "s\'lope", "puta", "con",
                "cons"]

phrasetest = r'FF14 c\'est un peux **** genre de système con batard entre wow et ****'

regex = re.compile(r'\b(%s)\b' % '|'.join(word_set))

if regex.search(phrasetest) is not None:
    print('bad words detected')
    corrected = regex.sub('lapin', phrasetest)
    print(corrected)
else:
    print('no problem bro')
    print(phrasetest)





