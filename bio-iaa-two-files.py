#!/usr/bin/env python

"""

Script that calculates Cohen's Kappa (inter rater agreement) for 2 BIO files
BIO files need to be exactly the same length

Usage: python bio-kappa.py [bio file 1] [bio file 2] 


"""

import sys
import re
from sklearn.metrics import f1_score
from nltk.metrics import *

bio1 = sys.argv[1]
bio2 = sys.argv[2]
if len(sys.argv) > 3:
    excludeOlabels = False
else:
    excludeOlabels = True

bio1lines = [line.rstrip('\n') for line in open(bio1)]
bio2lines = [line.rstrip('\n') for line in open(bio2)]

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
print("Cohen's Kappa on all tokens: "+str(result))

t = AnnotationTask(data=triplesNoO)
result = t.kappa()
print("Cohen's Kappa on annotated tokens only: "+str(result))

f = f1_score(bio1labels, bio2labels, average='micro')
print("F-measure: "+str(f))




