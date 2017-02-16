#Rappler news site scraper

from bs4 import BeautifulSoup
import feedparser
import urllib
import re
import html.parser as htmlparser
import simplejson as json




#gets the rss feeds of GMA News only the current news are taken (you can change the '/nation' into other type of news)
rssfeed = feedparser.parse('http://feeds.feedburner.com/rappler/');

#to get the count of the entries of the feed
#len(rssfeed.entries)
limit = 10
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

			





