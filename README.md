torrentDownloader
===============================

Version Number: 1.0  
Author: Tejas Pandey

Overview
-------------

To automate process of downloading TV Shows

Installation / Usage
---------------------------

Pre-Install
--------------

 - Run command `crontab -e` and select nano as a editor , this will happen only when crontab is never has been used 
  in the system.
  
 - Following steps to activate GMAIL API.
 - Use this [wizard](https://console.developers.google.com/start/api?id=gmail) to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue, then Go to credentials. 
 - At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button. 
 - Select the Credentials tab, click the Add credentials button and select OAuth 2.0 client ID. 
 - Select the application type Other, enter the name "Gmail API Quickstart", and click the Create button. 
 - Click OK to dismiss the resulting dialog.
 - Click the  (Download JSON) button to the right of the client ID.
 - Rename it to client_secret.json .
 

> Don't share client_secret.json to anyone . This will be used in later stages of installation.

 
 
Install
-----------
 - Extract the Source code (tar.gz) from Release.
 - Go to install folder and copy all the files and paste it where Source code (tar.gz)  is present   These scripts and Source code (tar.gz) must be in same folder .
 - Follow the command excatly without trying to become super using su    .
 - `sudo ./install.sh` 
 - `./cron.sh`   
 - `sudo ./trans.sh`
 - Copy as a  sudo  user **client_secret.json** to `/usr/local/lib/python2.7/dist-packages/torrentDownloader/ `
 - `sudo chmod 777 /usr/local/lib/python2.7/dist-packages/torrentDownloader/client_secret.json`.

> A folder will be created in Downloads folder with name "torrent" ,
> this is where  all torrents will be downloaded.
> Log of the software running will be present at the **log** file at the **Desktop** 

Issues
------------

 - It is possible transmission-daemon does not starts properly   
  Then we should try to use following command. 
  ` sudo service transmission-daemon start   
  sudo service transmission-daemon stop`

Example
------------

 - To see the help and commands available   

     **tc - -help**

 - To addshow to the currently watching.
 
     **tc addshow** 
        
     At a time only one season of a show can be downloaded . It will     increment   the episode number once season is completely downloaded it will be removed. 
  
 - Graphical user interface is also available for transmission-daemon   
  Default address - [Web Interface](http://127.0.0.1:9091/)   
  **Username - transmission**   
  **Password - transmission**
  

 - **tc lt** 
   List all the torrent that are currently running in the system .
   

 - **tc generalsearch**
     To add torrent without adding to the list of currently watching   show.   

 - **tc aftercare**
     To remove completed torrent without deleting the data.   

  
Configuration
----------------

Config.yaml
-----------------
**Location :- /usr/local/lib/python2.7/dist-packages/torrentDownloader/config.yaml**   

 - **baseUrl: https://kat.cr**
   Since there is possibility of kat.cr changes its domain , user can configure it form here . 
   
 - **scrapDepth : 10**
 Higher the number it will search for more pages for the torrent. In most cases does not require to change.
 
 - **quality : 'High'**
  By default it is set to High , can be changed to Low , for saving data or space. Valid values are - High or Low (case sensitive)
  
 - **emailId: 'example@gmail.com'**
  Set this to your gmail id to get the email when torrent download is complete.

crontab -e 
-----------

    */30 * * * *  /usr/bin/python /usr/local/lib/python2.7/dist-packages/torrentDownloader/background.py >> /home/tejas/Desktop/log   2>&1

  
Not exactly this entry will differ from system to system.   
  
***/30** - Tells about the minutes at which scrapping and maintaince routine should run   
  
This time can be changed depending upon the need by default it is 30 minutes , can be changed depending upon need  

