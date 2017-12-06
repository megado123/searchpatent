import httplib2
import json
import requests
import nltk
import urllib.request
import regex
from json import JSONEncoder
from datetime import datetime
from sqlalchemy import desc
from patentsearch import db
from flask_login import UserMixin
from werkzeug.security import  check_password_hash, generate_password_hash
import os
import sys
from os import path


basedir = os.path.abspath(os.path.dirname(__file__))

nltk_path = os.path.join(basedir, 'patentsearch', 'App_Data', 'nltk_data')
nltk.data.path.append(nltk_path)
#add path to support Azure
nltk.data.path.append('D:\\home\\python361x64\\nltk_data')
nltk.data.path.append('D://home//python361x64//nltk_data')


from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
#tabulate used to create tuples
import tabulate
from tabulate import tabulate
import numpy as np
import nltk.data
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import gensim
from gensim import corpora, models, similarities
import collections


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class textSize():
    def __init__(self, text, size):
        self.text = text
        self.size = size


class resultmodels():
    def __init__(self):
        self.words = []
        self.score = []


class SearchData():
    def __init__(self, textdata, jsonData, orgs):
        self.orgs = orgs
        self.text = ""
        self.text = textdata
        self.counts = []
        self.words = []
        self.jsonData = jsonData
        self.mytextSizelist = []
        self.frequency_list = []


        self.LDA_topic_words = []
        self.LDA_topic_scores = []
        self.LDA_topic_model = []

        self.HDP_topic_words = []
        self.HDP_topic_scores = []
        self.HDP_topic_model = []

        #collection to hold topic model information
        self.LDA_models = []
        self.HDP_models = []

      
        self.bow()
        self.GetTops()


    #function to create bag of words on text
    def bow(self):
    
        self.text = regex.sub(r'[^\w]', ' ', self.text)
        self.text = self.text.lower()
        tokens = [t for t in self.text.split()]
        clean_tokens = tokens[:]
    
        sw = stopwords.words('english')
        unique_stopwords = ['wherein', 'base', 'said', 'therewith', 'one', 'two', 'first', 'second', 'third', 'includes']

   
        for token in tokens:
            if token in (stopwords.words('english') or unique_stopwords):
                clean_tokens.remove(token)

        freq = nltk.FreqDist(clean_tokens)
        blah = freq.most_common()

        total = 0
        max = 0

        for key, val in freq.items():
            total = total + val
            if (val > max):
                max = val

           
        maxsize = 100
        minsize = 20
        for key, val in freq.items():
            self.mytextSizelist.append(textSize( key, ((val/max) * (maxsize - minsize) + minsize)))
            #self.mytextSizelist.append(textSize( key, (100/max) * val))
            
                                       
        self.frequency_list = MyEncoder().encode(self.mytextSizelist)

    #function to create topics
    def GetTops(self):

        documents = []
        results = []
        tokens = []
        filtered_tokens = []
        bag_of_words = []
        frequency = []

        ## setup stopwords
        #  NLTK's default stopwords
        default_stopwords = set(nltk.corpus.stopwords.words('english'))
        #  We're adding some on our own
        custom_stopwords = set((u'``', u'and', u'but'))  #these are just some temp words
        unusual_stopwords = set(('"\\"\\"\\"', '"a', '\"\"\""'))
        stop1 = set({'wherein','base','said','therewith','one','two','first','second','third'})
        stop2 = set({'includes','like','inolves','identifies','forming','main','combined','portion','especially'})
        stop3 = set({'central'})
        unique_stopwords =  stop1 | stop2 | stop3

        all_stopwords = default_stopwords | custom_stopwords | unusual_stopwords | unique_stopwords

        num_response = len(self.jsonData)

        self.text = regex.sub(r'[^\w]', ' ', self.text)
        self.text = self.text.lower()

        for i in range(0, num_response):
            documents.append(regex.sub(r'[^\w]', ' ',self.jsonData[i]['abstract'].replace('"', '').lower()))

        ##
        ## this section is for Gensim functions
        ## a lot of the code is from Gensim tutorial
        # remove common words and tokenize

        texts = [[word for word in document.lower().split() if word not in all_stopwords]
                   for document in documents]

        #remove words that appear only once
        from collections import defaultdict

        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        Rpmodel = models.RpModel(corpus, num_topics=500)

        Ldamodel = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=1, update_every=1, chunksize=100,
                                    passes=10, gamma_threshold=0.001)
        tab = Ldamodel.show_topics(num_words=5, formatted=False)

        model_length = len(tab)


        for i in range(0, model_length):
                x = resultmodels()
                for (key, val) in tab:
                    for (key, value) in val:
                        self.LDA_topic_model.append(i)
                        self.LDA_topic_words.append(key)
                        self.LDA_topic_scores.append(value)
                        x.words.append(key)
                        x.score.append(value)
                self.LDA_models.append(x)


        Hdpmodel = models.HdpModel(corpus, id2word=dictionary)
        tab = Hdpmodel.show_topics(num_topics=1, num_words=5, formatted=False)

        model_length = len(tab)

        for i in range(0, model_length):
                x = resultmodels()
                for (key, val) in tab:
                    for (key, value) in val:
                        self.HDP_topic_model.append(i)
                        self.HDP_topic_words.append(key)
                        self.HDP_topic_scores.append(value)
                        x.words.append(key)
                        x.score.append(value)
                self.HDP_models.append(x)


class SearchFields():
    def __init__(self, searchtext, country, organization, kind, patentnumber, sortby, skip, recordnumber):
        self.searchtext = searchtext
        self.country = country
        self.organization = organization
        self.kind = kind
        self.patentnumber = patentnumber
        self.sortby = sortby
        self.skip = skip
        self.recordnumber = recordnumber


class Search(db.Model):
    extend_existing = True
    id = db.Column(db.Integer, primary_key=True)
    searchtext = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    author = db.Column(db.Text, nullable=True)
    organization = db.Column(db.Text, nullable=True)
    cpcs = db.Column(db.Text, nullable=True)
    patentnumber = db.Column(db.Text, nullable=True)

    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        return Search.query.order_by(desc(Search.date)).limit(num)

    def __repr__(self):
        return "<Search '{}': '{}'>".format(self.searchtext)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    searches = db.relationship('Search', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)
    extend_existing = True

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)
