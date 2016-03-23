#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.

import requests
import simplejson
import sys
import subprocess
import base64
import yaml
basePath='/usr/local/lib/python2.7/dist-packages/torrentDownloader/'


def executeCommand(cmd):        
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
    output = p.communicate()[0].decode('utf-8')
    if p.returncode != 0: 
        print "Error in Execution of %s Error Code: %d " % (cmd,p.returncode)
    else: 
        return output

def detailImdb(p):
    url ="http://www.omdbapi.com/"
    try:
        x=requests.get(url,params=p)
    except requests.exceptions.Timeout:
            print 'Timeout has occured'
            sys.exit(1)
    except requests.exceptions.RequestException as e:
            print e
            sys.exit(1)
    return x.json()


def showSeasonAll(showName,season):
    p={'t':showName,'Season':season}
    return detailImdb(p)

def showEpisode (showName,season,episode):
    p={'t':showName,'Season':season,'Episode':episode}
    return detailImdb(p)
def show(showName):
    p={'t':showName};
    return detailImdb(p)
    


