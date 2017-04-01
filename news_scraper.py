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
import datetime

class NewsScraper:

	@staticmethod
	def scrape(channel, rssurl, from_date, to_date):
		rssfeed = feedparser.parse(rssurl);
		#print(rssfeed)

		try:
			from_date = parser.parse(from_date).date()
			to_date = parser.parse(to_date).date()
		except ValueError: #if the date is either empty or not valid date format
			from_date = datetime.datetime.today().date()
			to_date = datetime.datetime.today().date()

		#print('limit' + str(limit))
		print("ENTRIES LENGTH: " + str(len(rssfeed.entries)))
		#print(rssfeed)
		#return;
		for index, feed in enumerate(rssfeed.entries):
			if(len(feed) == 0):  
				continue;
			try:
				summary = feed.summary #gets the news summary
				title = feed.title #gets the news title
				pubdate = feed.published #gets the date published
				link = feed.links[0].href #gets the link
			except:
				continue;

			pubdate = parser.parse(pubdate).date()
			print('pubdate' + str(pubdate))

			# if pubdate < limit:
			# 	print("LIMIT DATE REACHED")
			# 	break;

			print(channel + " Scraping ...")

			#checks if the newslink is already found in the database, if there is same entry in the db, then proceed to the next iteration
			if(News.query.filter_by(link = link).first() is not None): 
				print("News article is already found in the DB")
				continue;

			print("Is there a news of the same link in the DB?")
			print(News.query.filter_by(link = link).first())
			try:
				with urllib.request.urlopen(link) as url:
					read = url.read()
			except:
				continue;

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
		rssurl = {'GMA': ['http://www.gmanetwork.com/news/rss/news/nation',
					'http://www.gmanetwork.com/news/rss/money',
					'http://www.gmanetwork.com/news/rss/publicaffairs',
					'http://www.gmanetwork.com/news/rss/newstv',
					'http://www.gmanetwork.com/news/rss/sports',
					'http://www.gmanetwork.com/news/rss/scitech'],
				'RAPPLER': ['http://feeds.feedburner.com/rappler/'],
				'CNN': ['http://rss.cnn.com/rss/edition_asia.rss',
						'http://rss.cnn.com/rss/cnn_latest.rss',
						'http://rss.cnn.com/rss/money_news_international.rss',
						'http://rss.cnn.com/rss/edition_technology.rss',
						'http://rss.cnn.com/rss/edition_sport.rss',
						'http://rss.cnn.com/rss/edition_us.rss',
						'http://rss.cnn.com/rss/edition_meast.rss',
						'http://rss.cnn.com/rss/edition_europe.rss',
						'http://rss.cnn.com/rss/edition_americas.rss',
						'http://rss.cnn.com/rss/edition_world.rss',
						'http://rss.cnn.com/rss/edition_africa.rss'],
				'MANILABULLETIN': ['http://mb.com.ph/mb-feed/'], 
				'PHILSTAR' : ['http://www.philstar.com/rss/nation',
						'http://www.philstar.com/rss/breakingnews',
						'http://www.philstar.com/rss/headlines',
						'http://www.philstar.com/rss/opinion',
						'http://www.philstar.com/rss/world',
						'http://www.philstar.com/rss/business']}

		earliest_news = db.session.query(News).order_by(News.pubdate.desc()).first()
		latest_news = db.session.query(News).order_by(News.pubdate.asc()).first()
        
		earliest_date = earliest_news.pubdate
		latest_date = latest_news.pubdate

		#scrape news from 6 months ago
		six_months_before = str(date.today() - relativedelta(months =+ 6))
		for i in range(0,5): 
			print(len(rssurl[channels[i]]))
			for j in range(0, len(rssurl[channels[i]])):
				#print(rssurl[channels[i]][j])
				NewsScraper.scrape(channels[i], rssurl[channels[i]][j], six_months_before, earliest_date);
				NewsScraper.scrape(channels[i], rssurl[channels[i]][j], latest_date, str(date.today));

       

# channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
# rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
# 	'RAPPLER': 'http://feeds.feedburner.com/rappler/',
#    'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
#    'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
#    'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

# NewsScraper.scrape(channels[0], rssurl[channels[0]], '', '')
#DB.update_news_db()