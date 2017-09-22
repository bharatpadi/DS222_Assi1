#!/usr/bin/env python 

#with open('/home/kishna.bharat/full_devel.txt') as f:
import sys
#import numpy

last_key = None

#dict_id = {}
list_id = []
counts = None
for line in sys.stdin:
	line = line.strip()
	this_key, value = line.split('\t',1)
	if this_key == last_key:
		if value[0] == 'c':
			#dict_id["counts"] = value
			counts = value
		elif this_key[0] != '~':
			#print 'x',value
			temp1,temp2, id_, labels = value.split('_',3)
			#dict_id[id_] = labels
			list_id.append(id_+labels)
	else:
		if last_key:
			
			#for d_key, d_value in dict_id.iteritems():
				#if d_value[0] != 'c':
					#print ('{0}\t{1}'.format(d_key + d_value, dict_id["counts"]))
			for d_key in list_id:
				print ('{0}\t{1}'.format(d_key, counts))
		#dict_id = {}
		list_id = []
		last_key = this_key
		#print last_key, value
		if value[0] == 'c':
			#dict_id["counts"] = value
			counts = value
		elif this_key[0] != '~':
			temp1,temp2, id_, labels = value.split('_',3)
			#dict_id[id_] = labels
			list_id.append(id_+labels)

if this_key == last_key:
	for d_key in list_id:
		print ('{0}\t{1}'.format(d_key, counts))
'''
	for d_key, d_value in dict_id.iteritems():
		if d_value[0] != 'c':
			print ('{0}\t{1}'.format(d_key + d_value, dict_id["counts"]))
'''

