#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

def new_encode(line):
    new_l = []
    
    for w in line.split():
        i = 0
        for c in w:
            if len(w)==1:
                new_l.append(c)
            elif i == len(w) - 1:
                new_l.append("#" + c)
            elif i == 0:
                new_l.append(c + "#")
            else:
                new_l.append("#" + c + "#")
            i += 1
    print("<s> " + " ".join(new_l) + " </s>")
    

  
  
for line in sys.stdin:
    new_encode(line)

#/share/apps/NYUAD/srilm/1.6.0/bin/i686-gcc4/ngram-count -unk -order 8 kndiscount1 -kndiscount2 -kndiscount3 -kndiscount4 -kndiscount5 -kndiscount6 -kndiscount7 -kndiscount8 -text encoded_msa.txt -lm msa_model.lm


