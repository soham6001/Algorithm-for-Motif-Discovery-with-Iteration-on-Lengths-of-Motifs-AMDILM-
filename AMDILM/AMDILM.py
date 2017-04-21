__author__ = 'gokul'
import initialization
import fitness
import ParallelProcessing
import gaOperations
import sys
import os
import multiprocessing
from random import randint
from matplotlib import pyplot as plt

cpuCount = multiprocessing.cpu_count()

#Write logic to get command line arguments
BioSeqDir = str(sys.argv[1]) #Directory where sequence files are placed
assert os.path.isdir(BioSeqDir), "Error: you have to give location of the Biological Sequnce files as first parameter."
maxL=int(sys.argv[2])
assert maxL > 3 and maxL < 100, "Error: Motif length given as more than 50"
maxLoop=int(sys.argv[3])#
assert maxLoop > 0, "Error: Value of third parameter should be greater than 0"
pm = float(sys.argv[4])
assert pm >= 0 and pm <= 1 , "Fourth parameter: Probability of Mutation should be between 0 and 1"
checkNum = 0
if (pm == 0):
    checkNum = -1
    UpperLimit = 0
else:
    UpperLimit = 1/pm - 1
BioSeq = initialization.readDNASequences(BioSeqDir)
assert len(BioSeq) > 0, "Error: There are no files under mentioned directory. Note that files should have extensions *.fas, *.fq, *.fastq"

L=3
P = list([[''],[''],['']])
Score = list([[0],[0],[0]]) #First 3 sequence are empty
P.append(initialization.initSequneceList(['A','C','G','T']))
Score.append(initialization.initSequenceScore(P[3], SequenceList=BioSeq))
HighestFitnessScore = list([0,0,0,max(Score[3])])
while L <= maxL:
    Score.append([0])
    P.append([])
    HighestFitnessScore.append(0)
    for i in range(0,64):
        Score[L+1].append(0)     #Will be overwritten with correct value on line 47
        P[L+1].append('') #Will be overwritten with correct value on line 48
        Pcap,flag = gaOperations.addition(P[L][i],BioSeq)
        PtiltScore = 0
        PcapScore = 0
        for loop in range(0, maxLoop):
            Pcap_prev = gaOperations.deletion(Pcap,flag)
            if L > 3 :
                Ptilt = Pcap_prev
                if (checkNum == randint(0, UpperLimit)):
                    #print("Mutated",L,i,loop)
                    Ptilt = gaOperations.mutation(Pcap_prev)
                Ptilt_next,dummyFlag = gaOperations.addition(Ptilt,BioSeq)
            else:
                Ptilt_next,dummyFlag = gaOperations.addition(Pcap_prev,BioSeq)
            PtiltScore = ParallelProcessing.Score(Ptilt_next, BioSeq)
            PcapScore = ParallelProcessing.Score(Pcap, BioSeq)
            if (PcapScore < PtiltScore):
                PcapScore = PtiltScore
                Pcap = Ptilt_next
        Score[L+1][i] = PcapScore
        P[L+1][i] = Pcap
    HighestFitnessScore[L+1] = max(Score[L+1])
    L = L+1

SD = [ (HighestFitnessScore[n+1] - 2 * HighestFitnessScore[n] + HighestFitnessScore[n-1]) for n in range(4, maxL)]
# for n in range(4,maxL):
#     SD[n] = HighestFitnessScore[n+1] - 2 * HighestFitnessScore[n] + HighestFitnessScore[n-1]
# minSD = min(SD)
# i = len(SD) - 1
# for val in SD[::-1]:
#     i -= 1
#     if(val == minSD):
#         break
# i = i+4
i = SD.index(min(SD)) + 4
print("Highest Fitness Score Array: ",HighestFitnessScore)
print("Second Difference Array: ", SD)
print("Optimal Length: ", i)
print("Optimal Motifs: ", P[i])
print("Highest Fitness Score: ", HighestFitnessScore[i])#fitness.Score(P[i], BioSeq))
print("Optimal Scores: ", Score[i])

print("Optimal Motif: ", P[i][Score[i].index(HighestFitnessScore[i])])

SDx = range(4,maxL)
HFSx = range(0, len(HighestFitnessScore))
plt.figure(1)
plt.plot(SDx, SD)
plt.figure(2)
plt.plot(HFSx[3:], HighestFitnessScore[3:] )

plt.show()