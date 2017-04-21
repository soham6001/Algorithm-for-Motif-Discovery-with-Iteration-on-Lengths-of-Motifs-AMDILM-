#!/usr/bin/python
# File: sum_primes.py
# Author: VItalii Vanovschi
# Desc: This program demonstrates parallel computations with pp module
# It calculates the sum of prime numbers below a given integer in parallel
# Parallel Python Software: http://www.parallelpython.com

import pp
import threading

scoreLock = threading.Lock()

def Max_Match(P, Seq):
    Max = -1
    #print("In new job")
    for i in range(1, len(Seq) - len(P) + 2):
        score = 0 #fitness.Match(P, Seq[(i-1):(len(P)-1+i)])
        Tk = Seq[(i-1):(len(P)-1+i)]
        for i in range(0, len(Tk)):
            if (P[i] == Tk[i]):
                score += 1
        if (Max < score):
            Max = score
    #print(Max)
    return(Max)

def Score(P, S):
    """

    :rtype : int
    """
    #scoreLock.acquire()
    #print "In score method with P length", len(P)
    finalScore = 0
    # tuple of all parallel python servers to connect with
    #ppServers = ("127.0.0.1",)

    ppservers = ()

    ncpus = 4 #pp.Server.get_ncpus()
    job_server = pp.Server(ncpus, ppservers=ppservers)

    jobs = [(input, job_server.submit(Max_Match, (P, input,))) for input in S]
    for input, job in jobs:
        finalScore += job()
    returnScore = finalScore
    job_server.destroy()
    #print "returning score ", returnScore
    #scoreLock.release()

    return returnScore
