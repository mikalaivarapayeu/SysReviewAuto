#import pandas as pd
import numpy as np
import scispacy
import spacy
nlp = spacy.load("en_core_sci_md")
import csv
import re
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
#from spacy.vectors import Vectors
#from scipy import spatial
import csv
import random
###################################################################################
#############################################crap##################################
###################################################################################
for token in sentence:
    print(f"{token.text:{15}} {token.pos_:{5}}  {token.dep_:{10}}")

spacy.explain('acl')
###################################################################################
##################################reading and writing_files########################
###################################################################################
file_name = '/txt_files/methods_250220.txt'
file_data = []
with open(file_name, 'r+', newline='', encoding="utf-8") as f:
    csv_reader = csv.reader(f, delimiter = '\t')
    for sent in csv_reader:
        file_data.append(sent)

random.shuffle(file_data)

print(file_data)

file_name_w = '/project/ML_NLP_algorithms/txt_files/sent_type.tsv'
def tsv_writer(sent, file_name_writer):
    with open(file_name_w, 'a+', newline='', encoding="utf-8") as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerow(sent)
    return


###################################################################################
########################processing_sentences#######################################
###################################################################################

nlp_content = [nlp(s.replace('\t', ' ').rstrip()) for s in content]
no_par_1 = [del_parentesis(sen) for sen in nlp_content]


x = [2,999,1,9,999,1,8,999,1,2,999,999,999,5,999,999,999,999,1,999,999,1,3,2,999,999,1]

brac = []
phrase = []
phrases = []
inside = 'off'
for i in range(len(x), 0, -1):
    #print(x[i-1])
    if x[i-1] == 1 and inside == 'off':
        inside = 'on'
        phrase.append(x[i - 1])
        print(i-1,' ',x[i-1])
        print(inside)
    elif x[i-1] == 1 and inside == 'on':
        brac.append(x[i-1])
        inside = 'active'
        print(i-1,' ',x[i-1])
        print(inside)
    elif x[i-1] == 999 and inside == 'active':
        brac.append(x[i - 1])
        print(i-1,' ',x[i-1])
        print(inside)
    elif x[i-1] == 999 and inside == 'on':
        phrase.append(x[i - 1])
        print(i - 1, ' ', x[i - 1])
        print(inside)
    elif x[i-1] == 5 and inside == 'active':
        brac.append(x[i - 1])
        #brac.reverse()
        phrases.append(brac)
        brac = []
        inside = 'on'
        print(i-1,' ',x[i-1])
        print(inside)
    elif x[i-1] != 999 and inside  in ['on','off']:
        phrase.append(x[i-1])
        #phrase.reverse()
        phrases.append(phrase)
        phrase = []
        inside = 'off'
        print(i-1,' ',x[i-1])
        print(inside)
        print('Here')

phrases.reverse()
print(phrases)



