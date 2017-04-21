import DNAFileReader as FR
import fitness

__author__ = 'gokul'

def initSequneceList(chars):
    ls = list()
    for x in chars:
        for y in chars:
            for z in chars:
                ls.append([x,y,z])
    return(ls)

def initSequenceScore(motifList, SequenceList):
    score = list()
    for p in motifList:
        score.append(fitness.Score(p, SequenceList))
    return(score)

def readDNASequences(directoryName):
    print("In readSequences")
    return FR.getSequences(directoryName)