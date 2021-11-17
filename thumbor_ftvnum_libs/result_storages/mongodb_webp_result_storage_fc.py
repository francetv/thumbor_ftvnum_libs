# -*- coding: utf-8 -*-
# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2019 HZ HZ@blackhand.org

import time
import urllib
import bson
import re
from datetime import datetime, timedelta
from cStringIO import StringIO
from pymongo import MongoClient
from thumbor.result_storages import BaseStorage
from thumbor.utils import logger
from sys import getsizeof
from bson.binary import Binary


class Storage(BaseStorage):
    @property
    def is_auto_webp(self):
        return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

    def __conn__(self):
        password = urllib.quote_plus(self.context.config.MONGO_RESULT_STORAGE_SERVER_PASSWORD)
        user = urllib.quote_plus(self.context.config.MONGO_RESULT_STORAGE_SERVER_USER)
        if not self.context.config.MONGO_RESULT_STORAGE_SERVER_REPLICASET:
          uri = 'mongodb://'+ user +':' + password + '@' + self.context.config.MONGO_RESULT_STORAGE_SERVER_HOST + '/?authSource=' + self.context.config.MONGO_RESULT_STORAGE_SERVER_DB
        else:
          uri = 'mongodb://'+ user +':' + password + '@' + self.context.config.MONGO_RESULT_STORAGE_SERVER_HOST + '/?authSource=' + self.context.config.MONGO_RESULT_STORAGE_SERVER_DB + "&replicaSet=" + self.context.config.MONGO_RESULT_STORAGE_SERVER_REPLICASET + "&readPreference=" + self.context.config.MONGO_RESULT_STORAGE_SERVER_READ_PREFERENCE + "&maxStalenessSeconds=120"
        client = MongoClient(uri)
        db = client[self.context.config.MONGO_RESULT_STORAGE_SERVER_DB]
        storage = db[self.context.config.MONGO_RESULT_STORAGE_SERVER_COLLECTION]
        return client, db, storage

    def get_max_age(self):
        '''Return the TTL of the current request.
        :returns: The TTL value for the current request.
        :rtype: int
        '''

        default_ttl = self.context.config.RESULT_STORAGE_EXPIRATION_SECONDS
        if self.context.request.max_age == 0:
            return self.context.request.max_age

        return default_ttl


    def get_key_from_request(self):
        '''Return a key for the current request url.
        :return: The storage key for the current url
        :rettype: string
        '''
        path = "result:%s" % self.context.request.url

        return path


    def put(self, bytes):
        connection, db, storage = self.__conn__()
        key = self.get_key_from_request()
        max_age = self.get_max_age()
        ref_img = ''
        ref_img = re.findall(r'/[a-zA-Z0-9]{24}(?:$|/)', key)
        if ref_img:
            ref_img2 = ref_img[0].replace('/','')
        else:
            ref_img2 = 'undef'
        if self.is_auto_webp:
            content_t = 'webp'
        else:
            content_t = 'default'
        doc = {
            'path': key,
            'created_at': datetime.utcnow(),
            'data': Binary(bytes),
            'content-type': content_t,
            'ref_id': ref_img2,
            'expire': datetime.utcnow() + timedelta(seconds=max_age)
            }
        doc_cpm = dict(doc)
        
        try:
            self.context.config.MONGO_RESULT_STORAGE_MAXCACHESIZE
            maxs = self.context.config.MONGO_RESULT_STORAGE_MAXCACHESIZE
        except:
            maxs = 16000000

        amd = getsizeof(bytes)
        if  amd > maxs:
            logger.warning(u"OVERSIZE %s: %s > %s pas de mise en cache possible", key, amd, maxs)
            return None
        else:
            storage.insert(doc_cpm)
            return key


    def get(self):
        '''Get the item .'''
        connection, db, storage = self.__conn__()
        key = self.get_key_from_request()
        if self.is_auto_webp:
            result = storage.find_one({"path": key, "content-type": "webp"})
        else:
            result = storage.find_one({"path": key, "content-type": "default"})
        if not result:
            return None

        tosend = result['data']
        return tosend