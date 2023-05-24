#############Importing Libraries#############
#import os
#from bs4 import BeautifulSoup
import re
import csv
#import requests
import random
import scispacy
import spacy
nlp = spacy.load("en_core_sci_md")
#from spacy.vectors import Vectors
#import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

###################################################################################
#############################################crap##################################
###################################################################################
for token in sentence:
    print(f"{token.text:{15}} {token.pos_:{5}}  {token.dep_:{10}}")

spacy.explain('acl:relcl ')
###################################################################################
#############################################chunk_txt_file########################
###################################################################################
file_name = '/txt_files/methods_270220.txt'
#file_chunk = []
with open(file_name, 'r+', newline='', encoding="utf-8") as f:
    '''for i in range(0,50):
        s = f.readline().rstrip()
        file_chunk.append(nlp(s))'''
    content = f.readlines()

nlp_content = [nlp(s.replace('\t', ' ').rstrip()) for s in content]

###################################################################################
##################################single_sentence##################################
###################################################################################
sentence = nlp(u'There were a few more self-reported adverse events in the pivmecillinam group than in the ibuprofen group, but the differences were not statistically significant.')
sentence = nlp(u'Subjects were enrolled in this prospective, randomized trial from February 1999 to June 2000.')
sentence = nlp(u' One in four of the first 200 patients enrolled were selected randomly for evaluation of circulating plasma levels of ascorbate and α-tocopherol at baseline and on days 1 , 3 , 5 , 7 , 14 , and 21 following admission.')
sentence = nlp(u'It has high inter- and intra-observer coefficients of reliability ( 0.94 ) and high test-retest reliability ( 0.95 ) [ 39 , 40 ].')
sentence = 'It has high inter- and intra-observer coefficients of reliability ( 0.94 ) and high test-retest reliability ( 0.95 ) [ 39 , 40 ].'
sentence = nlp(u'Legacy	Pediatrics	cares for a predominantly suburban, higher socio-economic status population.')
sentence = nlp(u'Participants were recruited through rheumatology, orthopaedic,	and	physical therapy clinics, as well as by word-of-mouth and newspaper advertisements	in the Hamilton, Ontario, Canada region between April and June 2015.')
###################################################################################
##################################stop_list########################################
###################################################################################
coordn_1 = ['and', 'but','or,','yet','nor','so',',',';',':']
coordn_2 = ['also','besides','furthermore','moreover','too','however','nevertheless','nonetheless','still','otherwise','accordingly','consequently','hence', 'therefore','thus']
subordn = ['after','although','as','because','before','how','if','since','that','than','though','unless','until','what','when','whenever','where', 'whether','wherever','which','while','who','whom','whose','likewise']
prep = ['in','for','at','from','on', 'during','over','below','with']
comb_slist = coordn_1+coordn_2+prep+subordn


###################################################################################
###########################################object_matcher###############################
########################################################################################
def svo_extraction(sent):
    pos_sbj = ['NOUN', 'DET', 'PRON', 'PROPN', 'AUX','PUNCT']
    dep_subj = ['cop', 'nsubj', 'expl', 'nmod', 'auxpass', 'conj', 'nsubjpass','punct','pobj','dep','amod','dobj']
    pos_verb = ['VERB', 'AUX']
    dep_verb = ['cop', 'aux', 'ROOT', 'acl:relcl','ccomp','auxpass','conj','xcomp']
    lemma_aux = ['be', 'have', 'would']
    svmod_pos = ['ADV', 'PART','NUM','DET']
    no_articles = ['A','a','An', 'an','the','The']
    svomatcher = Matcher(nlp.vocab)
    svopattern1 = [{'POS': {'IN': pos_sbj}, 'DEP': {'IN': dep_subj}}, {'LEMMA': {'IN': lemma_aux},'TEXT':{'NOT_IN': no_articles},'OP':'?'},
                   {'POS': {'IN':  svmod_pos},'TEXT':{'NOT_IN': no_articles}, 'OP': '?'},{'LEMMA': {'IN': lemma_aux},'OP':'?'}, {'POS':{'IN': pos_verb}, 'DEP':{'IN': dep_verb}},
                   {'POS': {'IN':  svmod_pos},'TEXT':{'NOT_IN': no_articles}, 'OP': '?'},{'POS':{'IN': pos_verb}, 'DEP':{'IN': dep_verb},'OP':'?'}]
    #svopattern5 = [{'POS': {'IN': ['AUX', 'DET']}}, {'POS': 'VERB'}]
    svomatcher.add('SVO', None, svopattern1)
    sent_split = []
    if isinstance(sent,str):
        sent = nlp(sent)
    svo = svomatcher(sent)
    for match_id, start, end in svo:
        # string_id = nlp.vocab.strings[match_id]  # Get string representation
        sent_split.append((start, end))
    svomatcher.remove('SVO')
    return sent_split,sent



###################################################################################
###########################################Work_area###############################
###################################################################################
for token in nlp_content[567]:
    print([f"{token.text:{15}} {token.pos_:{5}}  {token.dep_:{10}}"])




