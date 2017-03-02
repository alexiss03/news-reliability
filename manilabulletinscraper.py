from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json
from createdb import db, Newslink
from functions import *

def manilabulletinscraper():
    #gets the rss feeds of Manila Bulletin only the current news are taken
    rssfeed = feedparser.parse('http://mb.com.ph/mb-feed/');

    #to get the count of the entries of the feed
    #len(rssfeed.entries)
    limit = 1
    for index, feed in enumerate(rssfeed.entries):
        if index == limit:
            break
        
        summary = feed.summary #gets the news summary
        title = feed.title #gets the news title
        pubdate = feed.published #gets the date published
        link = feed.links[0].href #gets the link
        print(link)

        #checks if the newslink is already found in the database
        #if there is same entry in the db, then proceed to the next iteration
        if(Newslink.query.filter_by(link = link).first() is not None): 
            print("News article is already found in the DB")
            continue;

        #Adding to News database
        updatenewsdb('MANILABULLETIN', title, pubdate, link)

        
        with urllib.request.urlopen(link) as url:
            read = url.read()
            
        soup = BeautifulSoup(read, "html.parser")
        
        if soup.find_all(["div", "p"], {"class":"tm-main"}):
            paragraphs = soup.find(["div", "p"], {"class":"tm-main"}).findAll('p')
            paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
            print(paragraphs)

            countoccurrence(paragraphs) #count occurrence of words