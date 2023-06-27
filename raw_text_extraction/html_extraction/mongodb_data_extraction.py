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
collection = db['methodSentencesMedicalArticles']


#############Pulling Data From MongoDb#############


sentneces_objects = list(collection.find())
print(len(sentneces_objects))


dataset = {}
sentences = []
words = []
labels = []


for i, sent in enumerate(sentneces_objects):
    label = sent.get('semanticLabel')
    if label:
        labels.append(label)
    else:
        labels.append('missed')

    for w in sent['sentWords']:
        words.append(w[0])
    sentences.append(words)
    words = []

dataset ['sentences'] = sentences
dataset['labels'] = labels

with open('H:/nlp_crap/Articles/datasetTest.json', 'w') as f:
    json.dump(dataset, f)





