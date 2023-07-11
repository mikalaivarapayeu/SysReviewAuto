import json
import os
import project.raw_text_extraction.html_extraction.common_function as commons
from bson.objectid import ObjectId
import random

with open('Articles/RCT_corpus.tsv', encoding='utf-8') as f:
    lines = f.readlines()

sentences = []
for l in lines:
    l = l.strip().split('\t')[0]
    sentences.append(l)

print(len(sentences))

sent_dictionary = {
    "sentNumber": 1,
    "labelName": None,
    "isExtractable": "false",
    "isSelfContanined": "false",
    "sentWords": []
}

n = 2000
sentences_2000 = random.sample(sentences, n)
print(len(sentences_2000))

db = commons.get_database('clinicalTrialCorpus_v1')
collection = db['2000methodSentencesMedicalArticles']

word_label_tuple = []
for i, sent in enumerate(sentences_2000):
    # print(sent.text)
    sent_dictionary['_id'] = ObjectId()
    sent_dictionary['sentNumber'] = i + 1
    for w in sent.tokens:
        word_label_tuple.append(w.text)
        word_label_tuple.append('none')
        sent_dictionary['sentWords'].append(word_label_tuple)
        word_label_tuple = []
    collection.insert_one(sent_dictionary)
    sent_dictionary['sentWords'] = []
