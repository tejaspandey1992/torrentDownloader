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
import httplib2
from email.mime.text import MIMEText
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

basePath='/usr/local/lib/python2.7/dist-packages/torrentDownloader/'

with open(basePath+'config.yaml','r') as f:
        doc=yaml.load(f)
        emailId=doc['emailId']

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
    

def sendEmail(msg): 
    # Path to the client_secret.json file downloaded from the Developer Console
    CLIENT_SECRET_FILE = basePath+'client_secret.json'

    # Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

    # Location of the credentials storage file
    STORAGE = Storage(basePath + 'gmail.storage')

    # Start the OAuth flow to retrieve credentials
    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()

    # Try to retrieve credentials from storage or run the flow to generate them
    credentials = STORAGE.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, STORAGE, http=http)

    # Authorize the httplib2.Http object with our credentials
    http = credentials.authorize(http)

    # Build the Gmail service from discovery
    gmail_service = build('gmail', 'v1', http=http)

    # create a message to send
    message = MIMEText(msg,"plain", "utf-8")
    message['to'] = emailId
    message['to'] = emailId
    message['subject'] = u"Torrent Downloader Status"
    body = {'raw': base64.b64encode(message.as_string())}
    try:
          message = (gmail_service.users().messages().send(userId="me", body=body).execute())
          print('Message Id: %s' % message['id'])
          print(message)
    except Exception as error:
          print('An error occurred: %s' % error)

