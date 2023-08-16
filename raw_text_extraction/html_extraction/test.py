from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['clinicalTrialCorpus_v1']

# coll_names = [coll_name for coll_name in db.list_collection_names()]
# print(coll_names)
collection = db['method200SentencesMedicalArticles']

sentences_list = list(collection.find())


def find_sent(filter, updated):
    update = { '$set': { "sentWords" : updated} }
    filter = {'_id':filter}
    collection.update_one(filter, update)
    return


sentence_label_set= [s['sentWords']for s in sentences_list]


l2i = {i:k  for i, k in enumerate(list(set([wlp[1] for s in sentence_label_set for wlp in s])))}
i2l = {k:i for i,k in l2i.items()}
print(i2l)
def sent_split_by_border_tag(word_label_list):
    sentences_split_by_border = []
    s_split =  []
    for s in word_label_list:
        for wlp in s:
            if wlp[1] == 'BORDER':
                s_split.append(wlp)
                sentences_split_by_border.append(s_split)
                s_split = []
            else:
                s_split.append(wlp)
        sentences_split_by_border.append(s_split)
        s_split = []
    return sentences_split_by_border

sentences_split = sent_split_by_border_tag(sentence_label_set)

def chunk_reconstruction(sentence):
    phrase_list = []
    chunked_phrase = []
    label = 'none'
    for wlp in sentence:
        if wlp[1] not in ['none','ENDPHRASE'] and label == 'none':
            label = wlp[1]
            chunked_phrase.append(wlp[0])
        elif wlp[1] not in ['none', 'ENDPHRASE'] and label != 'none':
            # chunked_phrase.append(wlp[0])
            phrase_list.append({wlp[1]: chunked_phrase[0]})
            chunked_phrase = []
            chunked_phrase.append(wlp[0])
            label = wlp[1]
        elif wlp[1] == 'ENDPHRASE':
            chunked_phrase.append(wlp[0])
            phrase_list.append({label:chunked_phrase})
            label = 'none'
            chunked_phrase = []
        elif wlp[1] == 'none' and label != 'none':
            chunked_phrase.append(wlp[0])
    return phrase_list


label_set = list(set([wlp[1] for s in sentence_label_set for wlp in s]))
print(label_set)


secondary_labels = ['DESCRIPTION','BORDER','ACTOR', 'DEFINITION','LOCATION','TOOL']
ignore_labels = ['BORDER']

# print(chunk_reconstruction(sentences_split[17]))
chunk_set = [chunk_reconstruction(s) for s in sentences_split if chunk_reconstruction(s)!= [] ]
print(chunk_set[27])


chunk_set_to_publish = []
chunk_to_publish = []
# label = 'none'
for ch in chunk_set[27]:
    for k, v in ch.items():
        if k not in secondary_labels and chunk_set_to_publish != []:
            chunk_to_publish.append(ch)
       
        chunk_to_publish.append(ch)



# def sort_chunks(chunk_phrase):
#     return chunk_phrase[1]
# sorted_chunk_list = sorted(chunked_phrase_list, key=sort_chunks)



with open('H:/nlp_crap/Articles/sortedChunksTest.txt', 'w', encoding='utf-8') as f:
    for sent in labelled_sentence:
        # f.write(str(chunk[0])+'\t'+chunk[1]+'\t'+chunk[2]+'\n')
        line = ""
        for i, phrase in enumerate(sent)
        #     if i == 0:
        #         line = line + str(phrase[i][0])+'\t'
        #     else:
        #         line = line + str(phrase[i][0])+'\t'+str(phrase[i][1])
        # f.write(line + '\n')

print(labelled_sentence[17])

for i in range(20):
    for i, phrase in enumerate(labelled_sentence[i]):
        print(phrase)


for i , s in enumerate(sentences):
    for wlp in s['sentWords']:
        if wlp[1] == "":
            print(s['sentNumber'])