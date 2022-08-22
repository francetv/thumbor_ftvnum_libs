#!/usr/bin/python
# -*- coding: utf-8 -*-

# thumbor imaging service
# https://github.com/thumbor/thumbor/wiki

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2011 globo.com thumbor@googlegroups.com
#import re
#from thumbor.loaders import file_loader, http_loader
from thumbor.loaders import http_loader
from thumbor_ftvnum_libs.loaders import pic_nn_loader
from tornado.concurrent import return_future

import re
import urllib

@return_future
def load(context, path, callback):
    strclean=urllib.unquote(path)
    if re.search('^http[s]?://', strclean):
        http_loader.load(context, path, callback)
    else:
        pic_nn_loader.load(context, path, callback)
