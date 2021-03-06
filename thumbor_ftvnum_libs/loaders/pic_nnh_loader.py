#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com

#from thumbor.loaders import file_loader, http_loader
import urllib
from thumbor.loaders import http_loader
from thumbor_ftvnum_libs.loaders import pic_nn_loader
from tornado.concurrent import return_future
from thumbor.loaders import LoaderResult

@return_future
def load(context, path, callback):
    def callback_wrapper(result):
        if result.successful:
            callback(result)
        else:
            # If file_loader failed try http_loader
            if (path.find('http') != -1):
                http_loader.load(context, path, callback)
            else:
                result = LoaderResult()
                result.error = LoaderResult.ERROR_NOT_FOUND
                result.successful = False
                callback(result)

    # First attempt to load with file_loader
    pic_nn_loader.load(context, path, callback_wrapper)
