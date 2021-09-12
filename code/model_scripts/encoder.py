
# MIT License

# Copyright 2021 New York University Abu Dhabi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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


