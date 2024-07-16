#!/usr/bin/env python3
'''
Python function that returns the list of school having a specific topic
'''


def schools_by_topic(mongo_collection, topic):
    '''
    topic (string) will be topic searched
    '''
    documents = mongo_collection.find({"topics": topic})
    document = [doc for doc in documents]
    return document
