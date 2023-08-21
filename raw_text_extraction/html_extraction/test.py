from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['clinicalTrialCorpus_v1']

# coll_names = [coll_name for coll_name in db.list_collection_names()]
# print(coll_names)
collection = db['method200SentencesMedicalArticles']




def sent_split_by_border_tag(word_label_list):
    sentences_split_by_border = []
    s_split =  []
    for s in word_label_list:
        s_number = s[0]
        for wlp in s[1]:
            if wlp[1] == 'BORDER':
                # s_split.append(wlp)
                sentences_split_by_border.append((s_number,s_split))
                s_split = []
            else:
                s_split.append(wlp)
        sentences_split_by_border.append((s_number,s_split))
        s_split = []
    return sentences_split_by_border

def chunk_reconstruction(sentence):
    phrase_list = []
    chunked_phrase = []
    label = 'none'
    s_number = sentence[0]
    for wlp in sentence[1]:
        if wlp[1] not in ['none','ENDPHRASE'] and label == 'none':
            label = wlp[1]
            chunked_phrase.append(wlp[0])
        elif wlp[1] not in ['none', 'ENDPHRASE'] and label != 'none':
            # chunked_phrase.append(wlp[0])
            phrase_list.append((s_number,label,chunked_phrase[0]))
            chunked_phrase = []
            chunked_phrase.append(wlp[0])
            label = wlp[1]
        elif wlp[1] == 'ENDPHRASE':
            chunked_phrase.append(wlp[0])
            phrase_list.append((s_number,label,chunked_phrase))
            label = 'none'
            chunked_phrase = []
        elif wlp[1] == 'none' and label != 'none':
            chunked_phrase.append(wlp[0])
    return phrase_list

secondary_labels = ['DURATION', 'SECTOOL', 'LOCATION', 'TIME', 'TOOL', 'DESCRIPTION', 'ACTOR', 'DEFINITION']

def split_chunks(chunk_list):
    chunk_set_to_publish = []
    chunk_to_publish = []
    i = 0
    for ch in chunk_list:
        if ch[1] not in secondary_labels and i == 0:
           i = 1
        elif ch[1] not in secondary_labels and i != 0:
            chunk_set_to_publish.append(chunk_to_publish)
            chunk_to_publish = []
        chunk_to_publish.append(ch)
    chunk_set_to_publish.append(chunk_to_publish)
    return chunk_set_to_publish

def index_non_secondary_chunks(chunk_list):
    for i, ch in enumerate(chunk_list):
        if ch[1] not in secondary_labels:
           return i
    return None

sentences_objects = list(collection.find())
# print(sentences_objects[3])

sentence_label_set= [(s['sentNumber'],s['sentWords'])for s in sentences_objects]
# print(sentence_label_set[32])

sentences_split = sent_split_by_border_tag(sentence_label_set)
# print(sentences_split[32])

# label_set = list(set([wlp[1] for s in sentence_label_set for wlp in s]))
# print(label_set)

# print(chunk_reconstruction(sentences_split[17]))
chunk_set = [chunk_reconstruction(s) for s in sentences_split if chunk_reconstruction(s)!= [] ]


chunk_set_split = [split_chunks(s) for s in chunk_set ]
# print(chunk_set_split[33])

for chs in chunk_set_split:
    for ch in chs:
        index = index_non_secondary_chunks(ch)
        if index is not None:
            ch.insert(0,ch.pop(index))



with open('H:/nlp_crap/Articles/extracted.txt', 'w', encoding='utf-8') as f:
    for s in chunk_set_split:
        for chs in s:
            line = ''
            for i, ch in enumerate(chs):
                if i == 0:
                    line = str(ch[0])
                line = line+ '  ' + ch[1]
                if isinstance(ch[2], list):
                    line = line+ '  ' + ' '.join(ch[2])
                else:
                    line = line +'  '+ch[2]
            # print(line)
            f.write(line)
            f.write('\n')
            f.write('\n')
      # print(chs)




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