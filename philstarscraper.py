from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json

#gets the rss feeds of Philstar only the current news are taken
rssfeed = feedparser.parse('http://www.philstar.com/rss/nation');

#to get the count of the entries of the feed
#len(rssfeed.entries)
limit = 10
for index, feed in enumerate(rssfeed.entries):
    if index == limit:
        break
    
    summary = feed.summary #gets the news summary
    title = feed.title #gets the news title
    pubdate = feed.published #gets the date published
    link = feed.links[0].href #gets the link
    print(link)
    
    with urllib.request.urlopen(link) as url:
        read = url.read()
        
    soup = BeautifulSoup(read, "html.parser")
    
    if soup.find_all(["div", "p"], {"class":"field-item even"}):
        paragraphs = soup.find(["div", "p"], {"class":"field-item even"}).findAll('p')
        paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
        print(paragraphs)