#!usr/bin/python

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json
from createdb import db, News
from DB import DB
#from functions import countoccurrence
from functions import *


class NewsScraper:

	def __init__(self, channel):
		self.channel = channel;

	def scrape(self, channel, rssurl):
		rssfeed = feedparser.parse(rssurl);

		limit = 1
		for index, feed in enumerate(rssfeed.entries):
			if index == limit:
				break;

			summary = feed.summary #gets the news summary
			title = feed.title #gets the news title
			pubdate = feed.published #gets the date published
			link = feed.links[0].href #gets the link

			#checks if the newslink is already found in the database, if there is same entry in the db, then proceed to the next iteration
			if(News.query.filter_by(link = link).first() is not None): 
				print("News article is already found in the DB")
				continue;

			print(News.query.filter_by(link = link).first())
			with urllib.request.urlopen(link) as url:
				read = url.read()

			print("Ready to scrape")
			if(channel == 'GMA'):
				wordfrequencies = gmascraper(read)
			elif(channel == 'RAPPLER'):
				wordfrequencies = rapplerscraper(read)
			elif(channel == 'CNN'):
				wordfrequencies = cnnscraper(read)
			elif(channel == 'MANILABULLETIN'):
				wordfrequencies = manilabulletinscraper(read)
			elif(channel == 'PHILSTAR'):
				wordfrequencies = philstarscraper(read)


			#Adding to News database
			DB.updatenewsdb(channel, title, pubdate, link, wordfrequencies)
	

	