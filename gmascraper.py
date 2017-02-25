#GMA news site scraper

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json
from createdb import db, Newslink
#from functions import countoccurrence
from functions import *

def gmascraper():
	#gets the rss feeds of GMA News only the current news are taken (you can change the '/nation' into other type of news)
	rssfeed = feedparser.parse('http://www.gmanetwork.com/news/rss/news/nation');

	#print(Newslink.query.all())

	#to get the count of the entries of the feed
	#len(rssfeed.entries)
	limit = 1
	for index, feed in enumerate(rssfeed.entries):
		if index == limit:
			break;

		summary = feed.summary #gets the news summary
		title = feed.title #gets the news title
		pubdate = feed.published #gets the date published
		link = feed.links[0].href #gets the link

		#checks if the newslink is already found in the database
		#if there is same entry in the db, then proceed to the next iteration
		if(Newslink.query.filter_by(link = link).first() is not None): 
			print("News article is already found in the DB")
			continue;

		#Adding to News database
		updatenewsdb('GMA', title, pubdate, link)

		#print(Newslink.query.all())	
		print(Newslink.query.filter_by(link = link).first())
		with urllib.request.urlopen(link) as url:
			read = url.read()

		#this is the pattern of GMA news, news contents are stored into a variable initialData
		pattern = re.compile('var initialData = ({.*?});') #({.*?});

		soup = BeautifulSoup(read, "html.parser")
		parser = htmlparser.HTMLParser()
		parser.unescape(soup)

		script = soup.find('script', text = pattern)
		if script:
			match = pattern.search(script.text);
			if match:
				#print(match.group(1))
				x = json.loads(match.group(1))
				#print(x["title"]);  #title of the news article
				newscontent = BeautifulSoup(x["story"]["main"], "html.parser").text #gets all the text excluding the html tags
				
				countoccurrence(newscontent) #count occurrence of words
				
				

			





