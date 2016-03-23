#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.


from helper import  executeCommand
import click
class Transmission:

    def listTorrent(self):
        cmd = 'transmission-remote --auth transmission:transmission -l'
        return executeCommand(cmd)

    def addTorrent(self,magnet):
        cmd = 'transmission-remote --auth transmission:transmission -a \'%s\' ' %(magnet)
        click.echo(executeCommand(cmd))

    def removeAndDeleteTorrent(self,index):
        cmd ='transmission-remote --auth transmission:transmission -t %d --remove-and-delete' %(index)
        executeCommand(cmd)

    def removeTorrent(self,index):
        cmd ='transmission-remote --auth transmission:transmission -t %d --remove' %(index)
        click.echo(executeCommand(cmd))


    def removeCompletedTorrent(self):
        curStatus=str(self.listTorrent())
        curStatus=curStatus.split('\n')
        for x in curStatus:
            x=x.split()
            if len(x) >= 9 and x[1]=='100%'  :
                self.removeTorrent(int(x[0]))
                cmd='/usr/bin/notify-send Download-Complete -t 20 \"%s\"' %(x[-1])
                executeCommand(cmd)



