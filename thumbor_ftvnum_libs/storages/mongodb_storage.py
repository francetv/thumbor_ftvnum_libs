# -*- coding: utf-8 -*-
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2015 Thumbor-Community
# Copyright (c) 2011 globo.com timehome@corp.globo.com
import gridfs
import urllib
import re
from datetime import datetime, timedelta
from cStringIO import StringIO
from pymongo import MongoClient
from thumbor.storages import BaseStorage
from tornado.concurrent import return_future

class Storage(BaseStorage):

    def __conn__(self):
        password = urllib.quote_plus(self.context.config.MONGO_STORAGE_SERVER_PASSWORD)
        user = self.context.config.MONGO_STORAGE_SERVER_USER
        if not self.context.config.MONGO_STORAGE_SERVER_REPLICASET:
          uri = 'mongodb://'+ user +':' + password + '@' + self.context.config.MONGO_STORAGE_SERVER_HOST + '/?authSource=' + self.context.config.MONGO_STORAGE_SERVER_DB
        else:
          uri = 'mongodb://'+ user +':' + password + '@' + self.context.config.MONGO_STORAGE_SERVER_HOST + '/?authSource=' + self.context.config.MONGO_STORAGE_SERVER_DB + "&replicaSet=" + self.context.config.MONGO_STORAGE_SERVER_REPLICASET + "&readPreference=" + self.context.config.MONGO_STORAGE_SERVER_READ_PREFERENCE + "&maxStalenessSeconds=120"
        client = MongoClient(uri)
        db = client[self.context.config.MONGO_STORAGE_SERVER_DB]
        storage = db[self.context.config.MONGO_STORAGE_SERVER_COLLECTION]
        return client, db, storage

    def put(self, path, bytes):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        doc = {
            'path': tpath,
            'created_at': datetime.utcnow()           
        }
        doc_with_crypto = dict(doc)

        if self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            if not self.context.server.security_key:
                raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")
            doc_with_crypto['crypto'] = self.context.server.security_key

        fs = gridfs.GridFS(db)
        file_data = fs.put(StringIO(bytes), **doc)
        doc_with_crypto['file_id'] = file_data
        storage.insert(doc_with_crypto)
        return  tpath

    def put_crypto(self, path):
        if not self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
            return
        tpath = self.truepath(path)
        connection, db, storage = self.__conn__()
        pasplit = path.split("/")
        if not self.context.server.security_key:
            raise RuntimeError("STORES_CRYPTO_KEY_FOR_EACH_IMAGE can't be True if no SECURITY_KEY specified")
        crypto = storage.find_one({'path': tpath})
        crypto['crypto'] = self.context.server.security_key
        storage.update({'path': tpath}, crypto)
        return pasplit[0]

    def put_detector_data(self, path, data):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        pasplit = path.split("/")
        storage.update({'path': tpath}, {"$set": {"detector_data": data}})
        return pasplit[0]

    def truepath(self, path):

        pasplit = path.split("/")
        # cas du // vide a gerer
        pasplitf = re.search('^[a-z0-9A-Z]+', pasplit[0]).group(0)
        fichier = open("/tmp/data.txt", "a")

        return pasplitf

    @return_future
    def get_crypto(self, path, callback):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        pasplit = path.split("/")
        crypto = storage.find_one({'path': tpath})
        callback(crypto.get('crypto') if crypto else None)

    @return_future
    def get_detector_data(self, path, callback):
        connection, db, storage = self.__conn__()
        pasplit = path.split("/")
        tpath = self.truepath(path)
        doc = storage.find_one({'path': tpath})
        callback(doc.get('detector_data') if doc else None)

    @return_future
    def get(self, path, callback):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        stored = storage.find_one({'path': tpath})

        if not stored:
            callback(None)
            return
        if self.__is_expired(stored):
            self.remove(path)
            callback(None)
            return

        fs = gridfs.GridFS(db)

        contents = fs.get(stored['file_id']).read()

        callback(str(contents))

    @return_future
    def exists(self, path, callback):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        stored = storage.find_one({'path': tpath})

        if not stored or self.__is_expired(stored):
            callback(False)
        else:
            callback(True)

    def remove(self, path):
        connection, db, storage = self.__conn__()
        tpath = self.truepath(path)
        if not self.exists(tpath):
            return

        fs = gridfs.GridFS(db)
        stored = storage.find_one({'path': tpath})
        try:
            fs.delete(stored['file_id'])
            storage.remove({'path': tpath })
        except:
            return

    def __is_expired(self, stored):
        timediff = datetime.utcnow() - stored.get('created_at')
        return timediff > timedelta(seconds=self.context.config.STORAGE_EXPIRATION_SECONDS)