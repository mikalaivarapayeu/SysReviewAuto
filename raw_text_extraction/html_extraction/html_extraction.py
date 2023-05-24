#############Importing Libraries#############
#import os
from bs4 import BeautifulSoup
import re
# import requests
# import scispacy
# import spacy
# nlp = spacy.load("en_core_sci_md")
#import itertools
import glob
import json
import stanza
from pymongo import MongoClient
from bson.objectid import ObjectId


# stanza.download('en', package='genia')
#####################################################
#####Getting Text from Articles#######################
######################################################


def get_database(collection_name):
    """ Establish connection to local Mongo DB.

        Args:
            arg_1: collection name.

        Return: Connection to database.
        :param collection name: """

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    # CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient('localhost', 27017)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[collection_name]


def article2soup(html_article):
    """ Extracts text from HTML documents with BeautifulSoup lib.

    Args:
        arg_1: Path to HTML documents.

    Return: BeautifulSoup object.
    :param html_article:
    """
    with open(html_article, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    return soup


def tags_from_soup(tag):
    """ Return necessary tags form the Beautiful soup objects.

        Args:
            arg_1: tag.

        Return:
            Necessary tags.

        Note:
            This is filter for the RE library.
            :param tag:
        """
    tag_names_list = ['h2', 'h3', 'p']
    if tag.name in tag_names_list and re.compile('title|sectitle|_p|P|').search(str(tag.get('id'))):
        return tag


def full_text_extraction(soup):
    """ Return necessary tag names and tag  text form the Beautiful soup objects.

           Args:
               arg_1: Beautiful soup object

           Return:
               List of necessary tag names and texts.
               :param soup:
    """
    raw_data = soup.find_all(tags_from_soup)
    required_data = [(tag.name, tag.text) for tag in raw_data]
    return required_data


def selection_section_sents(node_name_text_tuples):
    """ Select sentences from necessary sections.

             Args:
                 arg_1:List of texts and its titles

             Return:
                 List of sentences from necessary sections.
                 :param node_name_text_tuples:
      """
    # need_sections = ['methods and findings', 'abstract', 'participants', 'randomization and interventions',
    # 'statistical analyses', 'secondary outcomes', 'materials and methods', 'setting and participants',
    # 'randomization and interventions', 'outcomes and follow-up', 'primary outcomes', 'methods', 'study design',
    # 'clinical failure', 'study setting, population and design', 'exclusion criteria', 'indeterminate',
    # 'clinical outcome', 'statistics', 'clinical cure', 'objective']  # 'results']

    need_sections = ['results']
    section_sentences = []
    section_title = 'off'
    for item in node_name_text_tuples:
        if item[0] in ['h2', 'h3'] and item[1].lower().strip() in need_sections:
            section_title = item[1].lower().strip()
        elif item[0] == 'p' and section_title != 'off':
            section_sentences.append(item[1])
            section_title = 'off'
        else:
            section_title = 'off'
    # print(section_sentences)
    return section_sentences


def flatten(list_of_lists):
    """ Select sentences from necessary sections.

                 Args:
                     arg_1:List of list

                 Return:
                     Flatten list.
                     :param list_of_lists:"""
    return [item for sublist in list_of_lists for item in sublist]


# def text_titles_tples(tags_lst):
#     ''' Combine in list section and subsection titles and paragraphs.
#
#                 Args:
#                     arg_1:List of tag names and their texts
#
#                 Return:
#                     List of lists of section titles and subtitles and their paragraphs.
#          '''
#     # context = ['abstract','methods','results','discussion','conclusion']
#     section_sents = []
#     current_chunk = []
#     for item in tags_lst:
#         current_chunk.append(item[1])
#         if item[0] not in ['h2', 'h3']:
#             section_sents.append(cur_chunk)
#             cur_chunk = []
#     return section_sents


# article_path = 'H:\\nlp_crap\\Articles\\amox.html'
# article = article2soup(article_path)
# article = full_text_extraction(article)
# sentence_list = selection_section_sents(article)
# print(sentence_list)

articles_list = glob.glob('H:\\nlp_crap\\Articles\\*.html')

list_of_articles = []
for i in range(6):
    article = article2soup(articles_list[i])
    article = full_text_extraction(article)
    sentence_list = selection_section_sents(article)
    list_of_articles.append(sentence_list)

flatten_list_of_articles = flatten(list_of_articles)
print(flatten_list_of_articles)
# dictionary = {'data': flatten_list_of_articles}
# json_object = json.dumps(dictionary)
# with open("H:\\nlp_crap\\Articles\\articles.json", "w") as outfile:
#     outfile.write(json_object)

nlp = stanza.Pipeline('en', processors='tokenize', package='genia')
segmented_sents = []
for sents in flatten_list_of_articles:
    nlp_article = nlp(sents)
    for sent in nlp_article.sentences:
        segmented_sents.append(sent)

# sent = segmented_sents[0]
print(len(segmented_sents))

sent_dictionary = {
    "sentNumber": 1,
    "labelName": None,
    "isExtractable": "false",
    "isSelfContanined": "false",
    "words": []
}


db = get_database('clinicalTrialCorpus_v1')
# collection = db['methodSentencesMedicalArticles']
collection = db['resultsSentencesMedicalArticles']


word_label_tuple = []
for i, sent in enumerate(segmented_sents):
    # print(sent.text)
    sent_dictionary['_id'] = ObjectId()
    sent_dictionary['sentNumber'] = i+1
    for w in sent.tokens:
        word_label_tuple.append(w.text)
        word_label_tuple.append('none')
        sent_dictionary['words'].append(word_label_tuple)
        word_label_tuple = []
    collection.insert_one(sent_dictionary)
    sent_dictionary['words'] = []


# sent_dictionary.words = wrds
# print(sent_dictionary['words'])
# {
#     sentNumber: 2,
#     labelName: 'recruitmentDetails',
#     isExtractable: true,
#     isSelfContanined: true,
#     words: [
#         ['We', 'none'], ['recruited', 'none'], ['premenopausal', 'none'], ['women', 'none'], ['aged', 'none'],
#         ['18–40', 'none'],
#         ['years', 'none'], ['with', 'none'], ['current', 'none'], [',', 'none'], ['symptomatic', 'none'], [',', 'none'],
#         ['uncomplicated', 'none'],
#         ['cystitis', 'none'], ['from', 'rborder'], ['the', 'none'], ['student', 'none'],
#         ['health', 'none'], ['center', 'none'], ['at', 'none'], ['the', 'none'], ['University', 'none'], ['of', 'none'],
#         ['Washington', 'none'], ['(', 'none'], ['Seattle', 'none'], [',', 'none'], ['WA', 'none'], [')', 'none'],
#         ['from', 'none'],
#         ['February', 'none'], ['2006', 'none'], ['through', 'none'], ['February', 'none'], ['2009', 'none'],
#         ['.', 'none']
#
#     ]
#
# }

# const sentenceSchema = new Schema({
#     sentNumber: Number,
#     semanticLabel: String,
#     isExtractable: Boolean,
#     isSelfContanined: Boolean,
#     sentWords: [
#         [String]
#     ],
#
# })
