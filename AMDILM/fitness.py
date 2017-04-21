__author__ = 'gokul'

import threading
import Queue

qLock = threading.Lock()
scores = Queue.Queue(100)
scoreLock = threading.Lock()

class Sequence (threading.Thread):
    def __init__(self, threadID, DNASeq, motif):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.DNAseq = DNASeq
        self.motif = motif
    def run(self):
        #print "Starting " + self.name , self.motif
        self.score = Max_Match(self.motif, self.DNAseq)
        qLock.acquire()
        scores.put(self.score)
        qLock.release()
        #print "Finished "+self.name, "with score ", self.score

def Match(P, Tk):
    sum = 0
    for i in range(0, len(Tk)):
        if (P[i] == Tk[i]):      #Compare function
            sum += 1
    return sum

def Max_Match(P, Seq):
    Max = -1
    for i in range(1, len(Seq) - len(P) + 2):
        score = Match(P, Seq[(i-1):(len(P)-1+i)])
        if (Max < score):
            Max = score
    #print(Max)
    return(Max)

def Score(P, S):
    """

    :rtype : int
    """
    scoreLock.acquire()
    sequenceObjList = list()
    finalScore = 0
    i = 0
    #scores = Queue.Queue(len(S)+1)
    for sequence in S:
        #print(sequence, P)
        obj = Sequence(i, sequence, P)
        obj.start()
        sequenceObjList.append(obj)
        i += 1

    #print("before Join")
    for obj in sequenceObjList:
        obj.join()
    #print("after join")
    while not scores.empty():
        finalScore += scores.get()
    returnScore = finalScore
    #print("return score ", returnScore)
    scoreLock.release()
    return(returnScore)
