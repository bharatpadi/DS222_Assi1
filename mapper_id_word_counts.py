#!/usr/bin/env python 

#with open('/home/kishna.bharat/full_devel.txt') as f:
import sys

for line in sys.stdin:
    line = line.strip()
    key,value = line.split('\t',1)
    print ('{0}\t{1}'.format(key, value))	
