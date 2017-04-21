__author__ = 'gokul'

import HTSeq
import glob

FASTA = 1
FASTQ = 2

def readFile(filename, fileType):
    """

    :rtype : return type is DNA Sequence as a list of characters
    """
    fasta_file = "" #dummy initialization
    if (fileType == FASTA):
        fasta_file = HTSeq.FastaReader(filename)
    elif (fileType == FASTQ):
        fasta_file = HTSeq.FastqReader(filename)
    sequence = ""
    for read in fasta_file:
        sequence += read.seq
    return(map(lambda x:x.upper(),list(sequence)))

def fastaFileNames(dirPath):
    """

    :rtype : list of Strings i.e. fileNames
    """
    return glob.glob(dirPath+"/*.fas")

def fastqFileNames(dirPath):
    """

    :rtype : list of Strings i.e. fileNames ending with *.fq and *.fastq
    """
    return glob.glob(dirPath+"/*.fq")+glob.glob(dirPath+"/*.fastq")

def getSequences(dirPath):
    """

    :rtype : list of lists #list of Sequences in specified directory
    """
    print("In get Sequences")
    sequences = list()
    for file in fastaFileNames(dirPath):
        sequences.append(readFile(file, FASTA))
    for file in fastqFileNames(dirPath):
        sequences.append(readFile(file, FASTA))
    return sequences
