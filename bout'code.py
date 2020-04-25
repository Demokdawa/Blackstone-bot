wordList = ['match', 'boxers', 'pro']
sentence = "protect matches with pro boxers"


def censor(s, w):
    rval = ''

    for i in s.split(' '):
        for j in w:
            replaced = False
            if j == i:
                replaced = True
                rval += f"{'*' * len(i)} "
                break
            else:
                pass
        if not replaced:
            rval += f"{i} "

    return rval


print(censor(sentence, wordList))

-----------------------------------------------------------------------

wordList = {
    'match': 'box',
    'boxers': 'brawlers',
    'pro': 'con'
}
sentence = "protect matches with pro boxers"


def censor(s, w):
    rval = ''

    for i in s.split(' '):
        for k, v in w.items():
            replaced = False
            if k == i:
                replaced = True
                rval += f"{v} "
                break
            else:
                pass
        if not replaced:
            rval += f"{i} "

    return rval


print(censor(sentence, wordList))