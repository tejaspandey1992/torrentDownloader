#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.
import requests
import click
import simplejson
import ast
import yaml
from datetime import date
from helper import showSeasonAll,show
from bs4 import BeautifulSoup
from transmission_control import Transmission
from time import sleep
import certifi


class Kickass:
    def __init__(self,showName,seasonNumber,episodeNumber):
        self.showName=showName
        self.seasonNumber=seasonNumber
        self.episodeNumber=episodeNumber

        self.isValidEpisode=True
        self.isValidSeasonNumber=True
        self.isValidShowName=True
        self.isValidShowSeasonEpisode=True

        self.maxSeason=0
        self.maxEpisode=0
        self.showEpisodeNumber=''

        self.torrentFound=False
        self.torrentPage=''
        self.recordPresent=False
        self.basePath='/usr/local/lib/python2.7/dist-packages/torrentDownloader/'
        with open(self.basePath + 'config.yaml','r') as f:
            config=yaml.load(f)
            self.baseUrl=config['baseUrl']
            self.quality=config['quality']
            self.depth=config['scrapDepth']

    def genNumber(self,x):
        genNumber=""
        if x<10:
            genNumber+='0'+str(x)
        else:
            genNumber=str(x)
        return genNumber


    def genShowSeasonEpisodeNumber(self):
        self.showEpisodeNumber+=self.showName+' '+'S'+self.genNumber(self.seasonNumber)+'E'+self.genNumber(self.episodeNumber)
        return self.showEpisodeNumber

    def validateShowName(self):
        imdbResponse = showSeasonAll(self.showName,1)
        self.isValidShowName=ast.literal_eval(imdbResponse['Response'])
    
        if self.isValidShowName == False:
            click.echo('Show Name Is Not Valid %s\n' %(self.showName))
        else:
            self.showName=imdbResponse['Title']
        self.isValidShowSeasonEpisode = self.isValidShowSeasonEpisode and self.isValidShowName
        return self.isValidShowName

    def numberPositive(self): 
        if self.seasonNumber < 0 :
            click.echo('Negative Season Number Not Possible %d\n' %(self.seasonNumber))
            self.isValidShowSeasonEpisode=False
        if self.episodeNumber < 0:
            click.echo ('Negative Episode Number Not Possible %d\n' %(self.episodeNumber))
            self.isValidShowSeasonEpisode=False

    def setMaxSeason(self): 
        if self.isValidShowSeasonEpisode:
            year=show(self.showName)['Year'].split(u'\u2013')
            if  year[1] == '' :
                self.maxSeason=date.today().year-int(year[0])+1
            else:
                year=map(int,show(self.showName)['Year'].split(u'\u2013'))
                self.maxSeason=year[1]-year[0]+1
   
    def validateSeasonNumber(self):
        if self.seasonNumber > self.maxSeason and self.isValidShowSeasonEpisode:
            click.echo ('Exceeding Maximum Available Season %d\n' %(self.maxSeason))
            self.isValidSeasonNumber=False

        self.isValidShowSeasonEpisode = self.isValidShowSeasonEpisode and self.isValidSeasonNumber

    def validateEpisodeNumber(self):
        if self.isValidShowSeasonEpisode:
            imdbResponse=showSeasonAll(self.showName,self.seasonNumber)    
            self.maxEpisode=len(imdbResponse['Episodes'])
            if self.episodeNumber > self.maxEpisode:
                click.echo ('Exceeding Maximum Available Episodes %d\n' %(self.maxEpisode))
                self.isValidEpisode=False

        self.isValidShowSeasonEpisode = self.isValidShowSeasonEpisode and self.isValidSeasonNumber


    def validateShowSeasonEpisode(self):
        self.validateShowName()
        self.numberPositive()
        self.setMaxSeason()
        self.validateSeasonNumber()
        self.validateEpisodeNumber()
        return self.isValidShowSeasonEpisode

    def getTorrentPage(self,url):
        url = self.baseUrl + url
        r=requests.get(url,verify=False)
        self.torrentPage=BeautifulSoup(r.text,'html.parser')

    def getMagnetLink(self,url):
        return self.torrentPage.find('a',{'title':'Magnet link'})['href']

    def getTorrentSize(self,url):
        x=self.torrentPage.find('div',{'class':'widgetSize'}).text.split()
        size=float(x[0])
        if x[1]=='GB':
            size*=1024
        elif x[1]=='KB':
            size/=1024
        return size
        

    def search(self):
        availabeTorrent=[]
        query=self.showEpisodeNumber.split()
        with open(self.basePath + 'data.txt', 'r') as f:
            jsonData=simplejson.load(f)
        for key,value in jsonData.iteritems():
            found = True
            k=key.split()
            for q in query:
                if q not in k:
                    found=False
                    break
            if found:
                self.getTorrentPage(value)
                self.torrentFound=True
                availabeTorrent.append([value,self.getTorrentSize(value),self.getMagnetLink(value)])
        availabeTorrent.sort(key=lambda x:float(x[1]))
        if self.torrentFound:
                if self.quality=='High':
                        Transmission().addTorrent(availabeTorrent[-1][2])
                else:
                        Transmission().addTorrent(availabeTorrent[0][2])

    def addRecord(self):
        with open(self.basePath + 'record.txt','r') as f:
            save=simplejson.load(f)
        if self.showName in  save:
            click.echo('Show already exists')           
            self.recordPresent=True
        else:
            save[self.showName]=[[self.seasonNumber,self.episodeNumber]]
        with open(self.basePath + 'record.txt','w') as f:
            simplejson.dump(save,f, sort_keys = True, indent = 4,
            ensure_ascii=False)

    def deleteAllRecord(self):
        with open(self.basePath + 'record.txt','w') as f:
            f.write('{ }')

    def deleteRecord(self):
        with open(self.basePath + 'record.txt','r') as f:
            save=simplejson.load(f)
        if self.showName in  save:
            del save[self.showName]
            click.echo('Record Deleted Successfully')
            print save
        else:
            click.echo('Show does not Exist')
        with open(self.basePath + 'record.txt','w') as f:
            simplejson.dump(save,f, sort_keys = True, indent = 4,
            ensure_ascii=False)

    def displayRecord(self):
        with open(self.basePath + 'record.txt','r') as f:
            save=simplejson.load(f)
        for key,value in save.iteritems():
            click.echo('Show Name : %s'%(key))
            click.echo('Season Number : %s'%(value[0][0]))
            click.echo('Episode Number : %s'%(value[0][1]))
            print

    def incrementRecord(self):
        with open(self.basePath + 'record.txt','r') as f:
            save=simplejson.load(f)
        if self.showName in  save:
            if save[self.showName][0][1]+1 > self.maxEpisode:
                self.deleteRecord()
                return
            else:
                save[self.showName][0][1]+=1
        with open(self.basePath + 'record.txt','w') as f:
            simplejson.dump(save,f, sort_keys = True, indent = 4,
            ensure_ascii=False)

    def scrap(self):
        print 'Starting Scrapping'
        with open(self.basePath+'data.txt','r') as f:
            jsonData=simplejson.load(f)
        for i in range(1,self.depth+1):
            try:
                url=self.baseUrl+'/user/ettv/uploads'
                r=requests.get(url,params={'page':i},verify = certifi.where())
            except requests.exceptions.Timeout:
                print 'Timeout has occured'
            except requests.exceptions.RequestException as e:
                print e
            soup=BeautifulSoup(r.text,'html.parser')
            for x in soup.findAll('a',{'class':'cellMainLink'}):
                    jsonData[x.string]=x['href']
            print 'End of Page',i
            with open(self.basePath + 'data.txt', 'w') as outfile:
                    simplejson.dump(jsonData, outfile, sort_keys = True, indent = 4,
                        ensure_ascii=False)
            sleep(5)
        print 'End Scrapping'


    def backUpdateRecord(self):
        print 'Start Back Updating Record'
        with open(self.basePath + 'record.txt','r') as f:
            save=simplejson.load(f)
        for key,value in save.iteritems():
            click.echo('Show Name : %s'%(key))
            click.echo('Season Number : %s'%(value[0][0]))
            click.echo('Episode Number : %s'%(value[0][1]))
            print
            cur=Kickass(key,value[0][0],value[0][1])
            if  cur.validateShowSeasonEpisode()  :
                cur.genShowSeasonEpisodeNumber()
                cur.search()
                if cur.torrentFound:
                    cur.incrementRecord()
                else:
                    click.echo('Torrent not Found')
        print 'End Back Updating Record'



