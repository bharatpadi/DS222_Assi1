#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 19:31:31 2017

@author: bharatp
"""
import numpy as np
import time
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
from sklearn import preprocessing

start = time.time()

class Node:
    tot_words = 1 #total number of words
    def __init__(self, k, classes, wc):
        self.l_child = None
        self.r_child = None
        self.w_count = wc #number of times the word appeared
        self.key = k #word
        self.class_count = np.zeros((50), dtype = int) #array maintaining class word count
        self.class_count[classes] += 1
        
def binary_insert(root, node, classes):# classes: a list containing labels of classes to which the word belongs
    if root is None:
        root = node
    else:
        if root.key > node.key:
            if root.l_child is None:
                root.l_child = node
                Node.tot_words += 1
            else:
                binary_insert(root.l_child, node, classes)
        elif root.key < node.key:
            if root.r_child is None:
                root.r_child = node
                Node.tot_words += 1
            else:
                binary_insert(root.r_child, node, classes)
        else:
            root.w_count += 1
            root.class_count[classes] += 1 #incrementing class count
    
def tree_search_iterative(root, k):
    while(root != None and k != root.key):
        if k < root.key:
            root = root.l_child
        else:
            root = root.r_child
    return root

def process_data(raw_review):
    review_text = BeautifulSoup(raw_review).get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    s_words = stopwords.words("english")
    s_words.append('en')
    stops = set(s_words)
    meaningful_words = [w for w in words if ((not w in stops) and (len(w) > 2))]
    return( " ".join( meaningful_words ))

def get_data_and_label_list(fname):
    labels =[]
    content = []
    with open(fname) as f:
        for i,line in enumerate(f):
                label, cont = line.rstrip().split('\t')
                content.append(cont)
                labels.append(label.strip().split(','))
    return content, labels

def get_clean_data(raw_data):
    clean_data = []
    for i in xrange( 0, len(raw_data)):
        if( (i+1)%5000 == 0 ):
            print "Review %d of %d\n" % (i+1, len(raw_data))                                                                    
        clean_data.append(process_data(raw_data[i]).split())
    return clean_data

def get_unique_labels(labels_list):
    unique_labels = []
    for label in labels_list:
        for l in label:
            if l not in unique_labels:
                unique_labels.append(l)
    return unique_labels

train_file_path = '/home/bharatp/Desktop/Sem3/ML_with_LargeDatasets/Ass1/DBPedia.full/full_train.txt'
train_file_data, train_file_labels = get_data_and_label_list(train_file_path)
train_file_clean = get_clean_data(train_file_data)
unique_labels = get_unique_labels(train_file_labels)
n_labels = len(unique_labels)
import time
start = time.time()
le = preprocessing.LabelEncoder()
le.fit(unique_labels)

temp_label = le.transform(train_file_labels[0])
root = Node(train_file_clean[0][0], temp_label, 0)

for i, words in enumerate(train_file_clean):
    labels = train_file_labels[i]
    for word in words:
        node_labels = le.transform(labels)
        temp_node = Node(word, node_labels, 1)
        binary_insert(root, temp_node, node_labels)    
end = time.time()
print end-start

test_file_path = '/home/bharatp/Desktop/Sem3/ML_with_LargeDatasets/Ass1/DBPedia.full/full_test.txt'
test_file_data, test_file_labels = get_data_and_label_list(test_file_path)
test_file_clean = get_clean_data(test_file_data)

dev_file_path = '/home/bharatp/Desktop/Sem3/ML_with_LargeDatasets/Ass1/DBPedia.full/full_devel.txt'
dev_file_data, dev_file_labels = get_data_and_label_list(dev_file_path)
dev_file_clean = get_clean_data(dev_file_data)

class_word_count = np.zeros((n_labels,), dtype = float) #number of words in each class
class_count = np.zeros((n_labels,), dtype = float)#number of times each class appears

def get_class_count(labels_):
    global class_count
    for label in labels_:
        label_encoded = le.transform(label)
        class_count[label_encoded] += 1

get_class_count(train_file_labels)

log_prob_class_count = np.log(class_count * 1.0 / np.sum(class_count))

def get_class_word_count(root):
    global class_word_count
    if root != None:
       get_class_word_count(root.l_child)
       class_word_count += root.class_count
       #print np.sum(class_word_count)
       get_class_word_count(root.r_child)
       
get_class_word_count(root)
max_ = np.amax(class_word_count)
w_const = 1.0/max_

#print class_word_count
class_word_count +=  w_const#for laplace smoothing

def get_accuracy(test_file, test_labels):
    acc = 0.0
    for i, words in enumerate(test_file):
        labels = le.transform(test_labels[i])
        log_prob_word_in_class = np.zeros((n_labels,))
        for word in words:
            word_node = tree_search_iterative(root, word)
            if word_node is None:
                word_class_count = np.zeros((n_labels,)) + w_const
            else:
                word_class_count = word_node.class_count + w_const
            #log_prob_word_in_class += np.log(word_class_count * 1.0 / np.sum(word_class_count))
            #log_prob_word_in_class += np.log(np.multiply(word_class_count, word_class_count * 1.0 / np.sum(word_class_count)) * 1.0 / class_word_count)
            
            log_prob_word_in_class += np.log(word_class_count * 1.0 / class_word_count)
        log_prob_word_in_class += log_prob_class_count
        pred_class = np.argmax(log_prob_word_in_class)
        #print log_prob_word_in_class
        #print pred_class, labels
        if pred_class in labels:
            acc += 1
    return acc/i#, log_prob_word_in_class

start = time.time()
test_acc = get_accuracy(test_file_clean,test_file_labels)
end = time.time()
print 'Time:', end - start    

dev_acc = get_accuracy(dev_file_clean, dev_file_labels)
    
train_acc = get_accuracy(train_file_clean, train_file_labels)

end = time.time()

print test_acc, dev_acc#, train_acc

print 'Time:', end - start    
    
min_ = 10000
for i, l in enumerate(test_file_clean):
        #if i == 17798:
    if len(l) < min_:
        min_ = len(l)
        temp = i
        #print l
        #print test_file_labels[i]
        #print len(l)
print temp
print test_file_clean[temp]
print test_file_labels[temp]


        
    
    
'''   
    
class_count1 = [5316, 2782, 4958, 3336, 3840, 4176, 5375, 3681, 3979, 6748, 7712, 8819, 5260, 6433, 7351, 
               15928, 22678, 12808, 3546, 3322, 6554, 5460, 2916, 13894, 12044, 4999, 5011, 5041, 3555, 3072, 
               10729, 9023, 2806, 3618, 2842, 2298, 2302, 2494, 6305, 12255, 5425, 8654, 4418, 5441, 9097, 2866, 2740, 3568, 119, 582]

    
c_c = np.array(class_count1)
    
    
    
class_word_count1= {'28':111664, '48':4693, '43':142183, '49':5960, '24':536802, '25':228151, '26':316965, 
    '27':167563, '20':389010, '21':260220, '22':97087, '23':598340, '46':115265, '47':89434, '44':277890, '45':172263, '42':84555, 
    '29':72404, '40':94333, '41':65805, '1':125174, '0':485552, '3':189707, '2':317938, '5':260700, '4':242524, '7':236941, '6':349445, 
    '9':411029, '8':244163, '39':177924, '38':251865, '11':448036, '10':509563, '13':305800, '12':351141, '15':662535, '14':377386, '17':420163, 
    '16':1072175, '19':208993, '32':162123, '31':322282, '30':325248, '37':64741, '36': 70781, '35':100736, '34':110975, '33':166081, '18':138738}
    
 
    
7923[0]	c{'c36': 14, 'c40': 1, 'c37': 1, 'c47': 1, 'c19': 6, 'c18': 18, 'c39': 3, 
'c38': 12, 'c13': 7, 'c12': 52, 'c11': 13, 'c10': 25, 'c17': 78, 'c16': 176, 'c15': 100, 
'c14': 12, 'c44': 1, 'c23': 2, 'c46': 4, 'c35': 6, 'c9': 13, 'c8': 8, 'c34': 19, 'c3': 11, 
'c2': 221, 'c1': 7, 'c0': 179, 'c7': 16, 'c6': 44, 'c5': 4, 'c4': 9, 'c22': 10, 'c45': 1, 'c20': 29, 
'c21': 6, 'c26': 6, 'c41': 2, 'c24': 3, 'c25': 45, 'c31': 4, 'c28': 2, 'c29': 1, 'c49': 1, 'c43': 1, 'c32': 3}



7923[0]	c{'c36': 18, 'c4': 67, 'c37': 13, 'c41': 4, 'c19': 56, 'c18': 54, 'c39': 36, 'c38': 77,
    'c26': 61, 'c13': 62, 'c12': 164, 'c11': 126, 'c10': 157, 'c17': 180, 'c30': 52, 'c15': 251, 'c14': 93, 'c22': 33, 'c23': 99,
    'c21': 44, 'c20': 366, 'c35': 66, 'c9': 63, 'c8': 98, 'c34': 35, 'c3': 49, 'c2': 92, 'c1': 10, 'c0': 254, 'c7': 56, 
    'c6': 118, 'c5': 70, 'c27': 22, 'c44': 43, 'c45': 31, 'c46': 59, 'c47': 28, 'c40': 14, 'c42': 9, 'c24': 94, 'c25': 87, 
    'c31': 38, 'c28': 17, 'c29': 8, 'c48': 5, 'c16': 405, 'c33': 22, 'c43': 104, 'c32': 42}



7923[0]	c{'c36': 2, 'c18': 2, 'c38': 3, 'c13': 17, 'c12': 3, 'c11': 7, 'c10': 2, 'c17': 5, 'c30': 3, 'c15': 20,
    'c14': 7, 'c47': 3, 'c3': 2, 'c0': 1, 'c7': 2, 'c6': 1, 'c5': 2, 'c4': 12, 'c44': 2, 'c46': 3, 'c21': 14, 
    'c41': 19, 'c25': 7, 'c31': 3, 'c28': 4, 'c29': 1, 'c16': 29}
    
word_node = tree_search_iterative(root, 'mara')
'''
    
    