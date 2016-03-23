#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.

import simplejson


basePath='/etc/transmission-daemon/'
print ('Enter your name and press [ENTER]:')
username=raw_input()
downloadPath='/home/%s/Downloads/torrent'%(username)
with open (basePath + 'settings.json') as f:
    jsonData=simplejson.load(f)
    jsonData['umask']=0
    jsonData['download-dir']=downloadPath
    print jsonData['umask'],jsonData['download-dir']


with open(basePath+'settings.json', 'w') as outfile:
    simplejson.dump(jsonData, outfile, sort_keys = True, indent = 4,
                        ensure_ascii=False)

