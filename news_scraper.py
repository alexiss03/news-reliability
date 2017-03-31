#!usr/bin/python

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json
from create_db import db, News
from database_manager import DatabaseManager as DB
#from functions import countoccurrence
from functions import *
from dateutil import parser
from datetime import date
from dateutil.relativedelta import relativedelta

class NewsScraper:

	@staticmethod
	def scrape(channel, rssurl, from_date, to_date):
		rssfeed = feedparser.parse(rssurl);
		#print(rssfeed)

		try:
			limit = parser.parse(from_date).date()
		except ValueError: #if the date is either empty or not valid date format
			limit = datetime.datetime.today().date()

		#print('limit' + str(limit))
		#print(len(rssfeed.entries))
		#print(rssfeed)
		#return;
		for index, feed in enumerate(rssfeed.entries):

			summary = feed.summary #gets the news summary
			title = feed.title #gets the news title
			pubdate = feed.published #gets the date published
			link = feed.links[0].href #gets the link

			pubdate = parser.parse(pubdate).date()
			print('pubdate' + str(pubdate))

			if pubdate < limit:
				print("LIMIT DATE REACHED")
				break;

			print("Scraping ...")

			#checks if the newslink is already found in the database, if there is same entry in the db, then proceed to the next iteration
			if(News.query.filter_by(link = link).first() is not None): 
				print("News article is already found in the DB")
				continue;

			print("Is there a news of the same link in the DB?")
			print(News.query.filter_by(link = link).first())
			with urllib.request.urlopen(link) as url:
				read = url.read()

			print("Ready to scrape")
			if(channel == 'GMA'):
				wordfrequencies = gma_scraper(read)
			elif(channel == 'RAPPLER'):
				wordfrequencies = rappler_scraper(read)
			elif(channel == 'CNN'):
				wordfrequencies = cnn_scraper(read)
			elif(channel == 'MANILABULLETIN'):
				wordfrequencies = manilabulletin_scraper(read)
			elif(channel == 'PHILSTAR'):
				wordfrequencies = philstar_scraper(read)


			#Adding to News database
			DB.add_news_to_db(channel, title, pubdate, link, wordfrequencies)


	@staticmethod
	def update_news_db():
		channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
		rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
			'RAPPLER': 'http://feeds.feedburner.com/rappler/',
			'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
			'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
			'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

		earliest_news = db.session.query(News).order_by(News.pubdate.desc()).first()
		latest_news = db.session.query(News).order_by(News.pubdate.asc()).first()
        
		earliest_date = earliest_news.pubdate
		latest_date = latest_news.pubdate

		#scrape news from 6 months ago
		six_months_before = str(date.today() - relativedelta(months =+ 6))
		for i in range(0,5): 
			print(1)
			NewsScraper.scrape(channels[i], rssurl[channels[i]], six_months_before, earliest_date);
			NewsScraper.scrape(channels[i], rssurl[channels[i]], latest_date, date.today);

       

# channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
# rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
# 	'RAPPLER': 'http://feeds.feedburner.com/rappler/',
#    'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
#    'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
#    'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

# NewsScraper.scrape(channels[0], rssurl[channels[0]], '', '')
#DB.update_news_db()