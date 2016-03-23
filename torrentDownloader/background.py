#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the MIT license.

import click
import  datetime 
from helper import showSeasonAll,show
from transmission_control import Transmission
from kickass import Kickass


def maintaince():
    click.echo('Starting Maintainence %s'%(datetime.datetime.now()))
    Transmission().removeCompletedTorrent()
    Kickass(None,None,None).scrap()
    Kickass(None,None,None).backUpdateRecord()
    click.echo('Ending Maintainence %s'%(datetime.datetime.now()))
maintaince()


