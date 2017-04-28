
from create_db import db,News, Topic, InputNews, NewsWord, Word
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta
from natural_language_processor import NaturalLanguageProcessor as NLP
from database_manager import DatabaseManager as DB


number_of_top_words = 20
minimum_match_word = 2

class ReliabilityEvaluator:

    sentiment_analyzer = SentimentAnalyzer()

    def compute_for_reliability_score(self, input_string):
        input_news = InputNews("pubdate", "link", input_string, NLP.count_occurrence(input_string))

        if not self.identify_topic_for_news(input_news) == None:
            reliability = self.sentiment_analyzer.identify_reliability(input_news)
            return reliability
        else:
            print("No topic")
            return None


    def identify_topic_for_news(self, news):
        topics = Topic.query.all()
        news_topic = self.find_news_a_topic(news, topics)

        if news_topic:
            return news.topic
        else:
            return None


    def assert_news_belong_to_topic(self, news, topic):
        match_words = 0

        if not news.topic_id is None:
            return True
        
        for news_word in sorted(news.news_words)[:number_of_top_words]:
            for topic_word in topic.words:
                if news_word.word.word.lower() == topic_word.word.lower():
                    match_words +=1

        if match_words >= minimum_match_word:
            news.topic = topic
            DB.commit_db()
            return True
        else:
            return False

        
    def find_news_a_topic(self, news, topics):
        for topic in topics:
            if self.assert_news_belong_to_topic(news,topic):
                return news.topic

        return None


    def create_new_topic_for_news(self, news):
        topic_word = []
        for news_word in sorted(news.news_words)[:number_of_top_words]:
            topic_word.append(news_word.word)

        if len(topic_word) == 0:
            return None

        new_topic = Topic(topic_word)
        return new_topic


    #only called when news list data is to be updated
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

    #only called when generating data set
    def generate_topics(self):
        topics = []
        count = 0

        newslist = News.query.all()

        for news in newslist:
            count += 1
            if not news.topic is None:
                continue

            if not self.find_news_a_topic(news, topics):
                new_topic = self.create_new_topic_for_news(news)
                news.topic = new_topic
                if not new_topic == None:
                    topics.append(new_topic)
                    DB.add_topic_to_db(new_topic)

        DB.commit_db()
        return topics

    def get_news_without_topic(self):
        return News.query.filter_by(topic = None).all()
    
    def get_topics_of_news_content(self):
        input_news_list = News.query.all()
        count = 0
        with_topic_count = 0
        with_positive_reliability = 0
        
        for input_news in input_news_list:
            count += 1
            if not self.identify_topic_for_news(input_news) == None:
                if self.sentiment_analyzer.identify_higher_than_topic_sentiment(input_news):

                    with_positive_reliability += 1 
                with_topic_count += 1
        
        print("With topic count " + str(with_topic_count) + " of " + str(count))
        print("With positive topic count " + str(with_positive_reliability) + " of " + str(count))
        return

re = ReliabilityEvaluator()
rel = re.compute_for_reliability_score("A federal form of government may be the last chance for the Philippines to resolve the decades-long conflict in Mindanao, former Chief Justice Reynato S. Puno said Monday.  Hindi masosolve 'yan if we have a unitary form of government, dahil ang dinedemand ng Muslims self rule, hindi delegated rule. Mabibigay mo lang 'yan under a federal form of government, Puno told reporters on the sidelines of a meeting of business groups in Makati City.  Part of the meeting was the Employers Confederation of the Philippines, Management Association of the Philippines, Makati Business Club and Philippine Chamber of Commerce and Industry.  A federal government may be the last chance to address concerns, or risk having a siege in Mindanao, according to the former chief justice.  Kung hindi pa natin mabigay 'yan – hindi pa nabibigay ng past Presidents natin – baka tuloy-tuloy na silang umalis. And that is a big, big problem, he said.  'Yan talagang maapektuhan tayong lahat niyan. Politically, economically, socially, he added.  President Rodrigo R. Duterte in December urged House Speaker Pantaleon Alvarez to speed up a Charter Change that would lead to a federal form of government. — VDS, GMA News")
#rel = re.compute_for_reliability_score("government government government government government government government government government government government government government  Philippines Duterte Manila Philippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte ManilaPhilippines Duterte Manila")
#print("word" + str(WordTopic.query.all()))

#Topic.query.delete()
#db.session.commit()
#News.query.delete()
#print("topics" + str(Topic.query.all()))
#re.generate_topics()
re.get_topics_of_news_content()
#re.get_topics_of_news_content()


#re.scrape_news_starting_from("01-01-2017")
