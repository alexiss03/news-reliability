import re
from createdb import db, Word, Newslink
from bs4 import BeautifulSoup
import html.parser as htmlparser


import feedparser
import urllib
import simplejson as json

def countoccurrence(paragraph):
	print("2")
	#the problem of this, it will remove also the apostrophe on possessive words
	#paragraph = "I was was and and dutertes' duterte's Helo helo Ha"
	paragraph = re.sub('[^\w]+', ' ', paragraph).lower()
	#print("PARAGRAPH" + paragraph)
	
	unique_words = set(paragraph.split()); #gets only the unique words
	#print("UNIQUE WORDS" + unique_words)

	wordcount = []
	for word in unique_words:
		count = sum(1 for _ in re.finditer(word, paragraph))
		#print(str(count) + " " + word)
		wordcount.append(count)

	#transform into a dictionary where the key is the word, and value is the frequency
	wordfrequencies = dict(zip(unique_words, wordcount))

	updateworddb(wordfrequencies)  #update the word database


def updateworddb(wordfrequencies):
	#print(wordfrequencies)
	for word in wordfrequencies:
		#the word --> word
		#the count of that word --> wordfrequencies[word]
		if(Word.query.filter_by(word = word).first() is None):
			addedword = Word(word, wordfrequencies[word])
			db.session.add(addedword)
		else:
			updatedword = Word.query.filter_by(word = word).first()
			updatedword.count += wordfrequencies[word]

		db.session.commit()
		print("Word database successfully updated")


def updatenewsdb(channel, title, pubdate, link):
	newslink = Newslink(channel, title, pubdate, link)
	db.session.add(newslink)
	db.session.commit()
	print("News database successfully updated")

#TESTING

# countoccurrence("h")
# print(Word.query.all())

def gmascraper(read):
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


def rapplerscraper(read):
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


def cnnscraper(read):
	soup = BeautifulSoup(read, "html.parser")
	if soup.find_all(["div", "p"], {"class":"zn-body__paragraph"}):
		paragraphs = soup.find_all(["div", "p"], {"class":"zn-body__paragraph"})
		paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
		print(paragraphs)
		countoccurrence(paragraphs) #count occurrence of words

def manilabulletinscraper(read):
	soup = BeautifulSoup(read, "html.parser")

	if soup.find_all(["div", "p"], {"class":"tm-main"}):
		paragraphs = soup.find(["div", "p"], {"class":"tm-main"}).findAll('p')
		paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
		print(paragraphs)

		countoccurrence(paragraphs) #count occurrence of words

def philstarscraper(read):
	soup = BeautifulSoup(read, "html.parser")
        
	if soup.find_all(["div", "p"], {"class":"field-item even"}):
		paragraphs = soup.find(["div", "p"], {"class":"field-item even"}).findAll('p')
		paragraphs = BeautifulSoup(str.join(u'\n',map(str,paragraphs)), "html.parser").text
		print(paragraphs)

		countoccurrence(paragraphs) #count occurrence of words