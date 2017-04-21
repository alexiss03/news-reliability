import re
from create_db import db, Word, News
from bs4 import BeautifulSoup
import html.parser as htmlparser
import feedparser
import urllib
import simplejson as json
from natural_language_processor import NaturalLanguageProcessor as NLP


def gma_scraper(read):
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
			print(newscontent)
			newswords = NLP.count_occurrence(newscontent) #count occurrence of words
			return newswords;

	return []

def rappler_scraper(read):
	soup = BeautifulSoup(read, "html.parser")
	if soup.find("div", {"class":"storypage-divider desktop"}):
		newscontent = soup.find("div", {"class":"storypage-divider desktop"}).findAll('p')
		newscontent = BeautifulSoup(str.join(u'\n',map(str,newscontent)), "html.parser").text
		print("newscontent A")
		newswords = NLP.count_occurrence(newscontent)
		return newswords
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
				print("newscontent B")

				newswords = NLP.count_occurrence(newscontent) #count occurrence of words
				return newswords;
	return []

def cnn_scraper(read):
	soup = BeautifulSoup(read, "html.parser")
	if soup.find_all(["div", "p"], {"class":"zn-body__paragraph"}):
		newscontent = soup.find_all(["div", "p"], {"class":"zn-body__paragraph"})
		newscontent = BeautifulSoup(str.join(u'\n',map(str,newscontent)), "html.parser").text
		print(newscontent)
		newswords = NLP.count_occurrence(newscontent) #count occurrence of words
		return newswords
	else:
		return []


def manilabulletin_scraper(read):
	soup = BeautifulSoup(read, "html.parser")

	if soup.find_all(["div", "p"], {"class":"tm-main"}):
		newscontent = soup.find(["div", "p"], {"class":"tm-main"}).findAll('p')
		newscontent = BeautifulSoup(str.join(u'\n',map(str,newscontent)), "html.parser").text
		print(newscontent)
		newswords = NLP.count_occurrence(newscontent) #count occurrence of words
		return newswords

	return []

def philstar_scraper(read):
	soup = BeautifulSoup(read, "html.parser")
        
	if soup.find_all(["div", "p"], {"class":"field-item even"}):
		newscontent = soup.find(["div", "p"], {"class":"field-item even"}).findAll('p')
		newscontent = BeautifulSoup(str.join(u'\n',map(str,newscontent)), "html.parser").text
		print(newscontent)

		newswords = NLP.count_occurrence(newscontent) #count occurrence of words	
		return newswords

	return []