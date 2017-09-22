#!/usr/bin/env python

import sys

last_word = None
last_class = None
running_total = 0
class_counts = []
class_labels = {}
tot_class_count = 0
class_tot_count = []
end_flag = 0
last_class1 = None
running_tot1 = 0
end_flag1 = 0
tilde_flag = 0

for input_line in sys.stdin:
	input_line = input_line.strip()
	if input_line[0] == '~':
		if input_line[1] == '~':
			if end_flag == -1:
				if last_class1 == this_class1:
					print ('{0}\t{1}'.format('~' + last_class1, running_tot1))
			elif end_flag1 == -1:
				if last_class == this_class:
					print ('{0}\t{1}'.format(last_word, 'c'+str(class_labels)))
			end_flag = 1
			value = int(input_line.split('\t',1)[1])
			tot_class_count += value
		else:
			end_flag = -1
			if end_flag1 == -1:
				if last_word == this_word:
					#class_counts.append([last_class,running_total])
					#print ('{0}\t{1}'.format(last_word, running_total))
					print ('{0}\t{1}'.format(last_word,'c'+str(class_labels)))
			end_flag1 = 1
			this_class1, value  = input_line[1:].split('\t',1)
			value = int(value)
			if this_class1 == last_class1:
				running_tot1 += value
			else:
				if last_class1:
					print ('{0}\t{1}'.format('~' + last_class1, running_tot1))
				running_tot1 = value
				last_class1 = this_class1
	else:
		#temp = input_line.split("\t",1)
		#class_labels = {}
		end_flag1 = -1
		this_word, value_temp = input_line.split("\t",1)
		value, this_class = value_temp.split('_',1)
		value = int(value)
		#this_word, this_class  = this_key.split('_',1)
		if this_word == last_word:
			if class_labels.has_key(this_class):
				class_labels[this_class] += value
			else:
				class_labels[this_class] = value
				#last_class = this_class
			#if this_class == last_class:
			#	running_total += value
			#else:
			#	class_counts.append([last_class,running_total])	
			#	running_total = value
			#	last_class = this_class
		else:
			#class_counts.append([last_class,running_total])
			if last_word:
				print ('{0}\t{1}'.format(last_word,'c'+ str(class_labels)))
			#class_counts = []
			class_labels.clear()
			class_labels[this_class] = value
			#class_counts.append([this_class, value])
			#running_total = value
			last_word = this_word
			last_class = this_class

	#if last_word == this_word:
	#	print ('{0}\t{1}'.format(last_word, running_total))


if end_flag == 1:
	print ('{0}\t{1}'.format('~~class_x_totcount',tot_class_count))
elif end_flag1 == 1:
	print ('{0}\t{1}'.format('~' + last_class1, running_tot1))
else:
	if last_word == this_word:
		print ('{0}\t{1}'.format(last_word, 'c'+str(class_labels)))




