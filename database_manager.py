from create_db import db, News, Word, InputNews
#from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta
from natural_language_processor import NaturalLanguageProcessor as NLP

class DatabaseManager:
	def update_word_db(wordfrequencies):
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


	@staticmethod
	def add_news_to_db(channel, title, pubdate, link, wordfrequencies, newscontent):
		if newscontent is None:
		    return
		newslink = News(channel, title, pubdate, link, wordfrequencies, newscontent)
		db.session.add(newslink)
		db.session.commit()
		print("News database successfully updated")


	@staticmethod
	def add_input_news_to_db(pubdate, link, newscontent):
		if newscontent is None:
			return
		inputnews = InputNews(pubdate, link, newscontent, NLP.count_occurrence(newscontent));
		db.session.add(inputnews)
		db.session.commit()
		print("Input News database successfully updated")

	@staticmethod
	def add_topic_to_db(topic):
		db.session.add(topic)
		db.session.commit()
		print("Topic database successfully updated")



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
		six_months_before = date.today() - relativedelta(months =+ 6)
		for i in range(0,5): 
			print(1)
			#NewsScraper.scrape(channels[i], rssurl[channels[i]], six_months_before, earliest_date);
			#NewsScraper.scrape(channels[i], rssurl[channels[i]], latest_date, date.today);

	@staticmethod
	def commit_db():
		db.session.commit()
       