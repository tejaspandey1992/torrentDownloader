#! /bin/sh
#
# build.sh
# Copyright (C) 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.
#
mkdir /home/$USER/Downloads/torrent
install="/usr/local/lib/python2.7/dist-packages/torrentDownloader"
crontab -l | { cat; echo "*/30 * * * *  /usr/bin/python $install/background.py >> /home/$USER/Desktop/log 2>&1 "; } | crontab -
cwd=$(pwd)
python $cwd/edit.py 

