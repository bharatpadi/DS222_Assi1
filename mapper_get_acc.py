#!/usr/bin/env python 

#with open('/home/kishna.bharat/full_devel.txt') as f:
import sys
import math
import ast 

class_count = [5316, 2782, 4958, 3336, 3840, 4176, 5375, 3681, 3979, 6748, 7712, 8819, 5260, 6433, 7351, 15928, 22678, 12808, 3546, 3322, 6554, 5460, 2916, 13894, 12044, 4999, 5011, 5041, 3555, 3072, 10729, 9023, 2806, 3618, 2842, 2298, 2302, 2494, 6305, 12255, 5425, 8654, 4418, 5441, 9097, 2866, 2740, 3568, 119, 582]

class_word_count = ast.literal_eval("{'28':111664, '48':4693, '43':142183, '49':5960, '24':536802, '25':228151, '26':316965, '27':167563, '20':389010, '21':260220, '22':97087, '23':598340, '46':115265, '47':89434, '44':277890, '45':172263, '42':84555, '29':72404, '40':94333, '41':65805, '1':125174, '0':485552, '3':189707, '2':317938, '5':260700, '4':242524, '7':236941, '6':349445, '9':411029, '8':244163, '39':177924, '38':251865, '11':448036, '10':509563, '13':305800, '12':351141, '15':662535, '14':377386, '17':420163, '16':1072175, '19':208993, '32':162123, '31':322282, '30':325248, '37':64741, '36': 70781, '35':100736, '34':110975, '33':166081, '18':138738}")


tot_class_count = 298176

max_ = max(class_word_count.values())
smooth_const = (1.0/max_)

log_prob_class_count = [math.log(x*1.0 / tot_class_count) for x in class_count]

for line in sys.stdin:
	line = line.strip()
	key,value = line.split('\t',1)
	w_count = ast.literal_eval(value[1:])
	w_prob = {}
	for dic_key in class_word_count:
		if 'c'+dic_key in w_count:
			w_prob[dic_key] = math.log((int(w_count['c'+dic_key])+smooth_const)*1.0/(int(class_word_count[dic_key])+smooth_const))
		else:
			w_prob[dic_key] = math.log(1.0*smooth_const/(int(class_word_count[dic_key])+smooth_const))
	print ('{0}\t{1}'.format(key + '_' + str(log_prob_class_count), w_prob))

