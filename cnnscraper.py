#Rappler news site scraper

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json




#gets the rss feeds of CNN News only the current news are taken
rssfeed = feedparser.parse('http://rss.cnn.com/rss/edition_asia.rss');

#to get the count of the entries of the feed
#len(rssfeed.entries)
limit = 5
for index, feed in enumerate(rssfeed.entries):
	print(index)
	if index == limit:
		break;

	summary = feed.summary #gets the news summary
	title = feed.title #gets the news title
	pubdate = feed.published #gets the date published
	link = feed.links[0].href #gets the link

	with urllib.request.urlopen(link) as url:
		read = url.read()

	soup = BeautifulSoup(read, "html.parser")
	if soup.find_all(["div", "p"], {"class":"zn-body__paragraph"}):
		paragraphs = soup.find_all(["div", "p"], {"class":"zn-body__paragraph"})
		paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
		print(paragraphs)
	





