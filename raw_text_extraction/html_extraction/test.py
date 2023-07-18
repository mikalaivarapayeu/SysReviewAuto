from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['clinicalTrialCorpus_v1']

# coll_names = [coll_name for coll_name in db.list_collection_names()]
collection = db['method200SentencesMedicalArticles']

sentences = collection.find()

chunked_sentence_list = []
for i in range(10):
    chunked_sentence = {'sent_number': sentences[i]['sentNumber']}
    chunked_sentence_list.append(chunked_sentence)



chunked_phrase_list = []
for s in sentences:
    chunked_phrase = []
    for wlpain in s['sentWords']:
        chunked_phrase.append(wlpain[0])
        if wlpain[1] != 'none':
            chunked_phrase_text = ' '.join(chunked_phrase)
            chunked_phrase_label = (s['sentNumber'], wlpain[1].lower(), chunked_phrase_text)
            chunked_phrase_list.append(chunked_phrase_label)
            chunked_phrase = []

print(len(chunked_phrase_list))


def sort_chunks(chunk_phrase):
    return chunk_phrase[1]


sorted_chunk_list = sorted(chunked_phrase_list, key=sort_chunks)

with open('H:/nlp_crap/Articles/sortedChunksTest.txt', 'w', encoding='utf-8') as f:
    for chunk in sorted_chunk_list:
        f.write(str(chunk[0])+'\t'+chunk[1]+'\t'+chunk[2]+'\n')


