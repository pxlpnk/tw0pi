#!/usr/bin/env python
import tweepy
import re
import time
from getpass import getpass
from textwrap import TextWrapper
import urlparse
from BeautifulSoup import BeautifulSoup as bs
import urllib
from random import choice
import os
import Image

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]


counter = 1

class AppURLopener(urllib.FancyURLopener):
    version =  choice(user_agents)
 

class StreamWatcherListener(tweepy.StreamListener):
    print 'Catching the fish'    
    status_wrapper = TextWrapper(width=60, initial_indent='    ', subsequent_indent='    ')
    def on_status(self, status): 
        global counter  
        try:   
            downloader = Downloader()
            out_folder = 'test/'
            
            mystring = self.status_wrapper.fill(status.text)
            myString = status.text
            myUrl = re.search("(?P<url>https?://[^\s]+)", myString).group("url")
            
            print '############ NR %d'% (counter,)
            #time.sleep(2)
            print '#WorkerStart'
            
            downloader.downloadWorker(myUrl,out_folder) 
            print '#WorkerDone Nr %d' % (counter,)
            print '############'
            counter +=1
        except Exception ,e:
            print e
                 
    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'

class Downloader:
    def downloadWorker(self,url,out_folder):
        print 'Downloading'
        print url
        soup = bs(urllib.urlopen(url))
        
        for image in soup.findAll('img', attrs={'class' : 'photo-large'}):
            filename = image["src"].split("/")[-1]
            outpath = os.path.join(out_folder, filename)
            urllib.urlretrieve(image["src"], outpath)   
            path = 'test'+image["src"]
             
                    

def main():
    # Prompt for login credentials and setup stream object
    username = raw_input('Twitter username: ')
    password = getpass('Twitter password: ')
        
    stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)    

    #track_list = raw_input('Keywords to track (comma seperated): ').strip()
    track_list ='twitpic'    
    

    if track_list:
        track_list = [k for k in track_list.split(',')]
        print track_list
    else:
        track_list = None

    stream.filter(None, track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye! ^^'
