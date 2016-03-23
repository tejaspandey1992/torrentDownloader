#! /bin/sh
#
# build.sh
# Copyright (C) 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.
#

install="/usr/local/lib/python2.7/dist-packages/torrentDownloader"
#sudo apt-get update
sudo apt-get -y install python-pip
sudo apt-get -y install transmission-daemon
#sudo apt-get -y install vim
sudo pip install torrentDownloader-0.0.1.tar.gz
sudo chmod 777 $install/*.txt $install/*.yaml  $install/*.py
sudo service  transmission-daemon stop
sudo chmod 777 /etc/transmission-daemon/settings.json








