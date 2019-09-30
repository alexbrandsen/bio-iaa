#!/usr/bin/env python

"""

Script that calculates Cohen's Kappa and F1 (inter rater agreement) for any number of BIO files
BIO files need to be exactly the same length

Usage: python bio-iaa-pairwise.py [folder containing bio files] 


"""

import sys
import re
from nltk.metrics import *
from sklearn.metrics import f1_score
import itertools
from os import listdir

# get average of a list 
def Average(lst): 
    return sum(lst) / len(lst)

kappasAllTokens = []
kappasAnnotatedTokens = []
fMeasures = []

folder = sys.argv[1]

files = listdir(folder)
for L in range(0, len(files)+1):
    for subset in itertools.combinations(files, 2):

        bio1lines = [line.rstrip('\n') for line in open(folder+'/'+subset[0])]
        bio2lines = [line.rstrip('\n') for line in open(folder+'/'+subset[1])]

        triples = []
        triplesNoO = []
        bio1labels = []
        bio2labels = []

        for i in range(0, len(bio1lines)):
            if len(bio1lines[i]):
                line1 = bio1lines[i].split(' ')
                line2 = bio2lines[i].split(' ')
                if bio1lines[i][-1:] is not 'O' or bio2lines[i][-1:] is not 'O':
                    triplesNoO.append(['bio1',i,line1[1]])
                    triplesNoO.append(['bio2',i,line2[1]])
                triples.append(['bio1',i,line1[1]])
                triples.append(['bio2',i,line2[1]])    
            bio1labels.append(line1[1])
            bio2labels.append(line2[1])

        t = AnnotationTask(data=triples)
        result = t.kappa()
        print(subset[0]+" - "+subset[1]+": Cohen's Kappa on all tokens: "+str(result))
        kappasAllTokens.append(result)

        t = AnnotationTask(data=triplesNoO)
        result = t.kappa()
        print(subset[0]+" - "+subset[1]+": Cohen's Kappa on annotated tokens only: "+str(result))
        kappasAnnotatedTokens.append(result)

        
        f = f1_score(bio1labels, bio2labels, average='micro')
        print(subset[0]+" - "+subset[1]+": F-measure: "+str(f))
        fMeasures.append(f)
        
        print('-----------------')


kappasAllTokens_avg = Average(kappasAllTokens)      
kappasAnnotatedTokens_avg = Average(kappasAnnotatedTokens)      
f1_avg = Average(fMeasures)      

print("Average Cohen's Kappa on all tokens: "+str(kappasAllTokens_avg))
print("Average Cohen's Kappa on annotated tokens only: "+str(kappasAnnotatedTokens_avg))
print("Average F1: "+str(f1_avg))




