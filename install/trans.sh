#! /bin/sh
#
# build.sh
# Copyright (C) 2016 tejas <tejas@Bazinga>
#
# Distributed under terms of the BSD license.
#
echo -n "Enter your name and press [ENTER]: "
read name
sudo chgrp debian-transmission /home/$name/Downloads/torrent
sudo chmod 777 /home/$name/Downloads/torrent
sudo service  transmission-daemon start








