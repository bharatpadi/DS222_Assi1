#!/usr/bin/env python 

#with open('/home/kishna.bharat/full_devel.txt') as f:
import sys
import math
import ast
'''
map_ = {1:'28', 2:'48',3:'43',4:'49',5:'24',6:'25',7:'26',8:'27',9:'20',10:'21',11:'22',12:'23',13:'46',14:'47',15:'44',16:'45',17:'42',18:'29',19:'40',20:'41',21:'1',22:'0',23:'3',24:'2',25:'5',26:'4',27:'7',28:'6',29:'9',30:'8',31:'39',32:'38',33:'11',34:'10',35:'13',36:'12',37:'15',38:'14',39:'17',40:'16',41:'19',42:'32',43:'31',44:'30',45:'37',46:'36',47:'35',48:'34',49:'33',50:'18'}
'''

def sumdict(dict1, dict2):
    #for k in dict1:
	#print dict1[k], dict2[k]
    summed = {k: float(dict1[k]) + float(dict2[k]) for k in dict1}
    return summed

def sumdictlist(dict1, dict2):
    #for k in dict1:
        #print dict1[k], dict2[k]
    summed = {k: float(dict1[k]) + float(dict2[k]) for k in dict1}
    return summed


def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


def getlabels(s):
	for i, c in enumerate(s):
		if c == '[':
			return s[i+1:-1].split()


acc_counter = 0
tot_counter = 0

last_key = None
sigma_prob = {}
for line in sys.stdin:
	line = line.strip()
	key, value = line.split('\t',1)
	this_key, log_prob_class_count = key.split('_',1)
	log_prob_class_count = log_prob_class_count[1:-1].translate(None, ',').split()
	log_prob_class_count = {str(v): k for v, k in enumerate(log_prob_class_count)}
	log_prob_word_count = ast.literal_eval(value)
	if this_key == last_key:
		#print this_key
		#print sigma_prob, '-------', log_prob_word_count
		sigma_prob = sumdict(sigma_prob, log_prob_word_count)
	else:
		if last_key:
			#print tot_counter
			#print sigma_prob, '*****', log_prob_class_count
			sigma_prob = sumdict(sigma_prob, log_prob_class_count)
			pred_label = keywithmaxval(sigma_prob)
			labels = getlabels(last_key)
			#print (pred_label, labels, last_key)
			if pred_label in labels:
				acc_counter += 1
			tot_counter += 1
		last_key = this_key
		sigma_prob = log_prob_word_count

if last_key == this_key:
	sigma_prob = sumdict(sigma_prob, log_prob_class_count)
	pred_label = keywithmaxval(sigma_prob)
	labels = getlabels(last_key)
	if pred_label in labels:
		acc_counter += 1
	tot_counter += 1

print ('{0}\t{1}'.format(acc_counter, tot_counter))









	
	





