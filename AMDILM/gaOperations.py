import random
from fitness import Score
from random import randint


def addition(p, s):
    randomChar = random.choice(['A', 'C', 'G', 'T'])
    pDash = list(p)
    pDash.append(randomChar)
    pDoubleDash = list(p)
    pDoubleDash.insert(3, randomChar)

    if Score(pDash, s) > Score(pDoubleDash, s):
        return (pDash, True)
    else:
        return (pDoubleDash, False)

def deletion(p, flag):
    seq = list(p)
    if flag:
        seq.pop()
    else:
        del seq[3]
        #seq.pop(0)
    return seq

def mutation(p):
    randomChar = random.choice(['A', 'C', 'G', 'T'])
    seq = list(p)
    index = randint(3, len(p)-1)
    seq[index] = randomChar
    return seq