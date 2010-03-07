#!/usr/bin/env python

import gzip
import cPickle as pickle

f = gzip.open('/home/www/workaround.org/stuff/all.pickle.gz', 'rb')
unp = pickle.Unpickler(f)
while True:
    print unp.load()
    print "-----------"
