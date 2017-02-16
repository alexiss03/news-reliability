#general news site scraper

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json



#gets the rss feeds of GMA News only the current news are taken
rssfeed = feedparser.parse('http://www.gmanetwork.com/news/rss/news/nation');

#to get the count of the entries of the feed
#len(rssfeed.entries)
for feed in rssfeed.entries:
	summary = feed.summary #gets the news summary
	title = feed.title #gets the news title
	pubdate = feed.published #gets the date published
	link = feed.links[0].href #gets the link

	with urllib.request.urlopen(link) as url:
		read = url.read()

	#this is the pattern of GMA news, news contents are stored into a variable initialData
	pattern = re.compile('var initialData = ({.*?});')

	soup = BeautifulSoup(read, "html.parser")
	parser = htmlparser.HTMLParser()
	parser.unescape(soup)

	script = soup.find('script', text = pattern)
	if script:
		match = pattern.search(script.text);
		if match:
			x = json.loads(match.group(1))
			#print(x["title"]);  #title of the news article
			newscontent = BeautifulSoup(x["story"]["main"], "html.parser").text #gets all the text excluding the html tags
			print newscontent

			





