#############Importing Libraries#############
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

#############mongoDB_connection#############
def get_database(db_name):
    """ Establish connection to local Mongo DB.

        Args:
            arg_1: db name.

        Return: Connection to database.
        :param collection db_name: """

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient('localhost', 27017)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[db_name]

db = get_database('clinicalTrialCorpus_v1')
print([coll_name for coll_name in db.list_collection_names()])


collection = db['method200SentencesMedicalArticles']


####################################################
#############Pulling Data From MongoDb#############
####################################################
sentneces_objects = list(collection.find())
print(len(sentneces_objects))


sentence_set = []
sentence = []

for sent in sentneces_objects:
    for wlp in sent['sentWords']:
        sentence.append(wlp)
    sentence_set.append(sentence)
    sentence = []

print(len(sentence_set))

print(list(set([wlp[1] for s in sentence_set for wlp in s])))

l2i = {i:k  for i, k in enumerate(list(set([wlp[1] for s in sentence_set for wlp in s])))}
i2l = {k:i for i,k in l2i.items()}
print(i2l)

s = sentence_set[19]
current_label = 'none'
extracted_chunk_list = []
extracted_chunk_set = []
for wlp in s:
    if wlp[1] not in ['none','ENDPHRASE','BORDER'] :
        current_label = wlp[1]

    elif wlp[1] == 'ENDPHRASE':
        extracted_chunk.append(wlp[0])

        extracted_chunk_set.append({current_label:extracted_chunk})
        extracted_chunk = ''
        current_label = 'none'
    elif current_label != 'none' and wlp[1] != 'ENDPHRASE':
        extracted_chunk = extracted_chunk +" "+wlp[0]
print(extracted_chunk_set)
print(' '.join([wlp[0] for wlp in s]))
####################################################
#############Pushing data into files################
####################################################


dataset = {}
dataset ['sentences'] = sentence_set
# dataset['labels'] = labels

with open('H:/nlp_crap/Articles/dataset400_3_sents.json', 'w') as f:
    json.dump(dataset, f)





