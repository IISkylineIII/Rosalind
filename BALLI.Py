import sys
import queue
import numpy as np
from copy import deepcopy

class SpectralDictProb:
    def __init__(self):
        massList = self.AminoAcidMassList()
        sVector, threshold, maxScore = self.readFromFile()
        p = self.dictProb(sVector, threshold, maxScore, massList)
        print(p)
        f = open('result.txt', 'w')
        f.write(str(p))
        f.close()
        
    def AminoAcidMassList(self):
        massTable = '''
G 57
A 71
S 87
P 97
V 99
T 101
C 103
I 113
L 113
N 114
D 115
K 128
Q 128
E 129
M 131
H 137
F 147
R 156
Y 163
W 186'''
        mass = massTable.split()
        return [int(mass[i+1]) for i in range(0, len(mass), 2)]

    def readFromFile(self):
        f = open('rosalind_ba11i (3).txt', 'r')
        data = []
        for line in f:
            data.append(line.strip().split())
        sVector = [0] + list(map(int, data[0]))
        threshold = int(data[1][0])
        maxScore = int(data[2][0])
        return sVector, threshold, maxScore
    
    def dictProb(self, sVector, threshold, maxScore, massList):
        prob = dict()
        prob[(0, 0)] = 1
        p = sum([self.getProb(len(sVector)-1, t, sVector, massList, prob) for t in range(threshold, maxScore+1)])
        return p
    
    def getProb(self, i, t, sVector, massList, prob):
        if (i, t) in prob:
            return prob[(i, t)]
        if i < 0 or t < 0:
            prob[(i, t)] = 0
            return 0
        p = sum([self.getProb(i-m, t-sVector[i], sVector, massList, prob)/20 for m in massList])
        prob[(i, t)] = p
        return p

if __name__ == "__main__":
    SpectralDictProb()
