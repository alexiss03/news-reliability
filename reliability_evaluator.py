
from create_db import db,News, Topic, InputNews
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta

class ReliabilityEvaluator:

    sentiment_analyzer = SentimentAnalyzer()

    def compute_for_reliability_score(self, input_string):
        # TODO: create News instance from input string
        input_news = InputNews(input_string)

        # TODO: Replace this with the filtered no topic news query
        #self.generate_topics_from_newlist(News.query.all())

        if self.identify_topic_for_news(input_news) != None:
            self.sentiment_analyzer.identify_reliability(input_news)

        else:
            return None


    def identify_topic_for_news(self, news):
        topics = Topic.query.all()
        if self.news_belongs_to_any_topic(news, topics):
            news.topic_id
        else:
            return None


    def generate_topics_from_newlist(self, newslist):
        print ("newslist count "+ str(len(newslist)))

        topics = []
        count = 0

        for news in newslist:
            count += 1
            print("news count " + str(count))
            if not news.topic is None:
                break

            if not self.news_belongs_to_any_topic(news, topics):
                new_topic = self.create_new_topic_for_news(news)
                # print("new topic " + str(new_topic))
                if not new_topic == None:
                    topics.append(new_topic)

        #for topic in topics:
            # The minimum newslist count will be adjusted accordingly
            # if len(topic.newslist) < 2:
            #    topics.remove(topic)


        return topics
                

    def news_belongs_to_topic(self, news, topic):
        topic_count = len(topic.words)

        #if topic.words is None:
        # print("topic count" + str(topic_count))
        #if topic_count == 0:
        #    return False

        match_words = 0
        
        for news_word in sorted(news.news_words)[:20]:
            for topic_word in topic.words:
                if news_word.word.word == topic_word.word:
                    match_words +=1
        if match_words/topic_count > 0.05:
            news.topic = topic
            print("matched topic:" + str(topic))
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
        for news_word in sorted(news.news_words)[:20]:
            topic_word.append(news_word.word)

        if len(topic_word) == 0:
            return None


        new_topic = Topic(topic_word)
        return new_topic


    def get_news_without_topic(self):
        #get the date of the newest article in the DB. From now to that date, scrape it.
        self.scrape_news_starting_from('20170301')
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
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date, "20170301");


    def update_news_db(self):
        channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
        rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
            'RAPPLER': 'http://feeds.feedburner.com/rappler/',
            'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
            'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
            'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

        #scrape news from 6 months ago
        for i in range(0,5): 
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date, "20170301");
        earliest_news = db.session.query(News).order_by(News.pubdate.desc()).first()
        latest_news = db.session.query(News).order_by(News.pubdate.asc()).first()
        #news = News.query.order_by('pubdate').first()
        earliest_date = earliest_news.pubdate
        latest_date = latest_news.pubdate

        #scrape_news_starting_from(earliest_date)
        six_months_before = date.today() - relativedelta(months =+ 6)
        print(six_months_before)


re = ReliabilityEvaluator()
rel = re.compute_for_reliability_score("Duterte President")
print("rel" + str(rel))
#print(News.query.all())
#re.scrape_news_starting_from("20170301")
#allnews = News.query.all()
#print(len(allnews))
#print("before generate topics")
#topics = re.generate_topics_from_newlist(allnews)
#print("topics:" + str(len(topics)))

