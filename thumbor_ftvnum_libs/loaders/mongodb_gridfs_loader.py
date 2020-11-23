#!/usr/bin/python
# -*- coding: utf-8 -*-
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
from tornado.concurrent import return_future
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
import urllib
from thumbor.loaders import LoaderResult

def __conn__(self):
    the_database = self.config.MONGO_ORIGIN_SERVER_DB
    if urllib.quote_plus(self.config.MONGO_ORIGIN_SERVER_USER):
        password = urllib.quote_plus(self.config.MONGO_ORIGIN_SERVER_PASSWORD)
        user = urllib.quote_plus(self.config.MONGO_ORIGIN_SERVER_USER)
        uri = 'mongodb://'+ user +':' + password + '@' + self.config.MONGO_ORIGIN_SERVER_HOST + '/?authSource=' + self.config.MONGO_ORIGIN_SERVER_DB
    else:
        uri = 'mongodb://'+ self.config.MONGO_ORIGIN_SERVER_HOST
    client = MongoClient(uri)
    #database
    db = client[self.config.MONGO_ORIGIN_SERVER_DB]
    return db

@return_future
def load(self, path, callback):
    db = __conn__(self)
    words2 = path.split("/")
    storage = self.config.MONGO_ORIGIN_SERVER_COLLECTION
    images = gridfs.GridFS(db, collection=storage)
    result = LoaderResult()
    if ObjectId.is_valid(words2[0]):
        if images.exists(ObjectId(words2[0])):
            contents = images.get(ObjectId(words2[0])).read()
            result.successful = True
            result.buffer = contents
        else:
            result.error = LoaderResult.ERROR_NOT_FOUND
            result.successful = False
    else:
        result.error = LoaderResult.ERROR_NOT_FOUND
        result.successful = False
    callback(result)