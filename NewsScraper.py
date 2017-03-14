#!usr/bin/python

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json
from createdb import db, Newslink
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
			if(Newslink.query.filter_by(link = link).first() is not None): 
				print("News article is already found in the DB")
				continue;

			#Adding to News database
			updatenewsdb(channel, title, pubdate, link)

			print(Newslink.query.filter_by(link = link).first())
			with urllib.request.urlopen(link) as url:
				read = url.read()

			if(channel == 'GMA'):
				gmascraper()
			elif(channel == 'RAPPLER'):
				rapperscraper()
			elif(channel == 'CNN'):
				cnnscraper()
			elif(channel == 'MANILABULLETIN'):
				manilabulletinscraper()
			elif(channel == 'PHILSTAR'):
				philstarscraper()


	def gmascraper():
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


	def rapplerscraper():
		soup = BeautifulSoup(read, "html.parser")
		if soup.find("div", {"class":"storypage-divider desktop"}):
			paragraphs = soup.find("div", {"class":"storypage-divider desktop"}).findAll('p')
			paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
			print(paragraphs)
		else:
			pattern = re.compile('var r4articleData = (.*?)$')
			parser = htmlparser.HTMLParser()
			parser.unescape(soup)

			script = soup.find('script', text = pattern)
			if script:
				match = pattern.search(script.text);
				if match:
		            #print(x["title"]);  #title of the news article
					print(script.text)
					x = json.loads(match.group(1))
					newscontent = BeautifulSoup(x["fulltext"], "html.parser").text #gets all the text excluding the html tags
					print(newscontent)

					countoccurrence(newscontent) #count occurrence of words

	def cnnscraper():
		soup = BeautifulSoup(read, "html.parser")
		if soup.find_all(["div", "p"], {"class":"zn-body__paragraph"}):
			paragraphs = soup.find_all(["div", "p"], {"class":"zn-body__paragraph"})
			paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
			print(paragraphs)

			countoccurrence(paragraphs) #count occurrence of words

	def manilabulletinscraper():
		soup = BeautifulSoup(read, "html.parser")

		if soup.find_all(["div", "p"], {"class":"tm-main"}):
			paragraphs = soup.find(["div", "p"], {"class":"tm-main"}).findAll('p')
			paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
			print(paragraphs)

			countoccurrence(paragraphs) #count occurrence of words

	def philstarscraper():
		soup = BeautifulSoup(read, "html.parser")
        
		if soup.find_all(["div", "p"], {"class":"field-item even"}):
			paragraphs = soup.find(["div", "p"], {"class":"field-item even"}).findAll('p')
			paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
			print(paragraphs)

			countoccurrence(paragraphs) #count occurrence of words