
from create_db import db,News, Topic, InputNews
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta

class MachineLearningProcessor:

    sentiment_analyzer = SentimentAnalyzer()

    def compute_for_reliability_score(self, input_string):
        # TODO: create News instance from input string
        input_news = News()

        # TODO: Replace this with the filtered no topic news query
        self.generate_topics_from_newlist(News.query.all())

        if self.identify_topic_for_news(input_news) != None:
            self.sentiment_analyzer.identify_reliability(input_news)

        else:
            return None


    def identify_topic_for_news(self, news):
        topic = Topic.query.all()
        if self.news_belongs_to_any_topic():
            news.topic_id
        else:
            return None


    def generate_topics_from_newlist(self, newslist):
        topics = []
        
        for news in newslist:

            if not news.topic is None: #if may topic na yung news na yun, break the loop
                break

            self.news_belongs_to_any_topic(news, topics) #will return true if news belongs to a topic

            if news.topic is None: #if wala pang topic si news
                new_topic = self.create_new_topic_for_news(news)
                topics.append(new_topic)

        print("topic count " + str(len(topics)))

        for topic in topics:
            # The minimum newslist count will be adjusted accordingly
            if len(topic.newslist) < 5:
                topics.remove(topic)


        return topics
                

    def news_belongs_to_topic(self, news, topic):
        topic_count = len(topic.words)
        match_words = 0
        
        for news_word in sorted(news.news_words)[:10]:
            if news_word.word in topic.words:
                match_words +=1
                
        if match_words/topic_count > 0.8:
            news.topic = topic
            return True
        else:
            return False


    def news_belongs_to_any_topic(self, news, topics):
        for topic in topics:
            if self.news_belongs_to_topic(news,topic):
                return True

        return False


    def create_new_topic_for_news(self, news):
        topic_word = []
        for news_word in sorted(news.news_words)[:10]: 
            topic_word.append(news_word.word)

        new_topic = Topic(topic_word)
        return new_topic


    def get_news_without_topic(self):
        #get the date of the newest article in the DB. From now to that date, scrape it. 

        self.scrape_news_starting_from('20170327')

        return News.query.filter_by(topic = None).all()
            

    def scrape_news_starting_from(self,date):
        channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
        rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
            'RAPPLER': 'http://feeds.feedburner.com/rappler/',
            'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
            'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
            'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

        #scrape news from 6 months ago
        for i in range(0,5): 
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date);


    def update_news_db(self):
        channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
        rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
            'RAPPLER': 'http://feeds.feedburner.com/rappler/',
            'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
            'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
            'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

        #scrape news from 6 months ago
        for i in range(0,5): 
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date);
        earliest_news = db.session.query(News).order_by(News.pubdate.desc()).first()
        latest_news = db.session.query(News).order_by(News.pubdate.asc()).first()
        #news = News.query.order_by('pubdate').first()
        earliest_date = earliest_news.pubdate
        latest_date = latest_news.pubdate

        #scrape_news_starting_from(earliest_date)
        six_months_before = date.today() - relativedelta(months =+ 6)
        print(six_months_before)



# ml = MachineLearningProcessor()
# allnews = News.query.all()
# print(allnews)
# #print(news1.first())
# ml.generate_topics_from_newlist(allnews)
# #ml.identify_topics([news1, news2])

ml = MachineLearningProcessor()
#ml.get_news_without_topic()
#ml.get_date_of_latest_news_in_db()
ml.update_news_db()