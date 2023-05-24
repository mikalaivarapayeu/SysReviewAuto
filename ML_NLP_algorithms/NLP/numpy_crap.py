#import pandas as pd
import numpy as np
import scispacy
import spacy
nlp = spacy.load("en_core_sci_md")
import csv
import re
from spacy.matcher import Matcher
#from spacy.vectors import Vectors
#from scipy import spatial
from spacy.matcher import PhraseMatcher

###################################################################################
#############################################crap##################################
###################################################################################
for token in sentence:
    print(f"{token.text:{15}} {token.pos_:{5}}  {token.dep_:{10}}")
spacy.explain('acl')

###################################################################################
#############################################chunk_txt_file########################
###################################################################################
file_name = '/txt_files/methods_250220.txt'
#file_chunk = []
with open(file_name, 'r+', newline='', encoding="utf-8") as f:
    '''for i in range(0,50):
        s = f.readline().rstrip()
        file_chunk.append(nlp(s))'''
    content = f.readlines()

###################################################################################
###########################################articles_removal########################
###################################################################################
def space_removal(sent):
    if isinstance(sent,str):
        sent = nlp(sent)
    space_r = ''
    for token in sent:
        if token.pos_ != 'SPACE':
            space_r = space_r+' '+token.text
    space_r = nlp(space_r.lstrip())
    return space_r


def del_parentesis(sent):
    i = 0
    par = False
    par_ind = []
    s = []
    for token in sent:
        if token.text in ['(','[','{']:
            par = True
            par_ind.append(i)
        if token.text in [')',']','}']:
            par = False
            par_ind.append(i)
        if token.text not in [')',']','}'] and par == False:
            s.append(token.text)
    s = ' '.join(s)
    i += 1
    return s, par_ind, sent

nlp_content = [nlp(s.replace('\t', ' ').rstrip()) for s in content]


###################################################################################
#############################svo_extraction########################################
###################################################################################
matcher = Matcher(nlp.vocab)
#matcher.add('SVO',None,svopattern1,svopattern2,svopattern3,svopattern4,svopattern5,svopattern6,svopattern7)
matcher.remove('SVO')


def svo_extraction(sent,matcher):
    svomatcher = matcher(nlp.vocab)
    svopattern1 = [{'POS': {'IN': ['NOUN', 'DET', 'PRON']}}, {'LEMMA': {'IN':['be','have']},'OP': '?'}, {'POS': {'IN':['ADV','PART']}, 'OP': '?'}, {'POS': {'IN':['VERB','AUX']}}]
    svopattern2 = [{'POS': {'IN':['NOUN','DET','AUX','PRON','PROPN']}},{'POS':{'IN':['PART','ADV','NUM']}, 'OP':'?'},{'DEP':{'IN':['cop','aux','ROOT']}}]
    svopattern3 = [{'POS': 'DET'}, {'LEMMA': 'have'}, {'POS': 'PART', 'OP': '?'}, {'LEMMA': 'be'}]
    svopattern4 = [{'DEP': {'IN': ['cop', 'nsubj']}}, {'DEP': {'IN': ['cop', 'ROOT']}}]
    svopattern5 = [{'DEP': 'ROOT'}]
    #svopattern5 = [{'POS': {'IN': ['AUX', 'DET']}}, {'POS': 'VERB'}]
    svomatcher.add('SVO', None, svopattern1, svopattern2, svopattern3, svopattern4, svopattern5)
    sent_split = []
    if isinstance(sent,str):
        sent = nlp(sent)
    svo = svomatcher(sent)
    for match_id, start, end in svo:
        # string_id = nlp.vocab.strings[match_id]  # Get string representation
        sent_split.append((start, end, 1))
    svomatcher.remove('SVO')
    return sent_split,sent

###################################################################################
##########################spacy_phrase_matcher#####################################
###################################################################################
def multi_stop_word(sent, matcher):
    multw_stl =[]
    phr_matcher = matcher(nlp.vocab)
    mv_list = ['in addition', 'just as', 'as if', 'as soon as', 'even though', 'so that', 'on the other hand',
               'in contrast', 'as a result', 'for example', 'for instance', 'in accordance with', 'according to',
               'in spite of', 'in order that', 'even if', 'as well','as well as']
    mv_stw = [nlp(item) for item in mv_list]
    phr_matcher.add('MultiStopWordList', None, *mv_stw)
    #sent = nlp(sent)
    matches = phr_matcher(sent)
    # gen_set.add(i)
    if matches:
        for match_id, start, end in matches:
            # string_id = nlp.vocab.strings[match_id]  # Get string representation
            multw_stl.append(start,end,2) # The matched span
            # match_set.add(i)
    phr_matcher.remove('MultiStopWordList')
    return multw_stl, sent

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
#########################sentence_to_TSV_file######################################
###################################################################################
def tsv_writer(lst):
    file_name = '/txt_files/chunk_label010421.tsv'
    with open(file_name,'a+', newline='', encoding="utf-8") as f:
        f = csv.writer(f, delimiter = '\t', )
        red_sent = []
        for word in lst:
            phrase = word[0]+' '+word[1]
            red_sent.append(phrase)
        f.writerow(red_sent)
    return


def gen_tsv_writer(ls):
    file_name = '/txt_files/sent_label020721.tsv'
    with open(file_name,'a+', newline='', encoding="utf-8") as f:
        f = csv.writer(f, delimiter = '\t',)
        ls = ls.replace('\t',' ')
        row_to_write = []
        row_to_write.append(ls)
        row_to_write.append(0)
        #print(row_to_write)
        f.writerow(row_to_write)
    return


