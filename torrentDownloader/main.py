#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.

import click
from transmission_control import Transmission
from kickass import Kickass 

@click.group()
def cli():
    pass


@click.command()
def lt():
    ''' List The Torrent '''
    click.echo(Transmission().listTorrent())
cli.add_command(lt)


@click.command()
@click.option('-n',prompt='Enter Show Name')
@click.option('-s',prompt='Enter Season Number',type = int)
@click.option('-e',prompt='Enter Episode Number',type = int)
def addShow(n,s,e):
    '''To Add Show With Season Number And Episode Number'''
    cur=Kickass(n,s,e)
    if  cur.validateShowSeasonEpisode()  :
        cur.genShowSeasonEpisodeNumber()
        cur.addRecord()
        if cur.recordPresent==False:
            cur.search()
            if cur.torrentFound:
                cur.incrementRecord()
            else:
                click.echo('Torrent not Found')
                cur.deleteRecord()

cli.add_command(addShow)

@click.command()
@click.option('-n',prompt='Enter Show Name')
def removeShow(n):
    '''To Remove Show From Currently Watching'''
    cur=Kickass(n,None,None)
    cur.validateShowName()
    cur.deleteRecord() 
cli.add_command(removeShow)


@click.command()
def currentWatching():
    '''List of Currently Watching Shows'''
    cur=Kickass(None,None,None)
    cur.displayRecord()
cli.add_command(currentWatching)

@click.command()
def afterCare():
    '''To Remove Completed Torrent From The List'''
    Transmission().removeCompletedTorrent()
cli.add_command(afterCare)
    
@click.command()
def removeallshow():
    '''To Remove All Show From The Record'''
    Kickass(None,None,None).deleteAllRecord()
cli.add_command(removeallshow)

@click.command()
@click.option('-n',prompt='Enter Show Name')
@click.option('-s',prompt='Enter Season Number',type = int)
@click.option('-e',prompt='Enter Episode Number',type = int)
def generalSearch(n,s,e):
    '''To Add Torrent Without Adding It To Record'''
    cur=Kickass(n,s,e)
    if  cur.validateShowSeasonEpisode():
        cur.genShowSeasonEpisodeNumber()
        cur.search()
        if cur.torrentFound == False:
            click.echo('Torrent not Found')
cli.add_command(generalSearch)
