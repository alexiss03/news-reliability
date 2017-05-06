from create_db import News, Topic, InputNews, Word
from database_manager import DatabaseManager as db

number_of_top_words = 20
minimum_match_word = 2

class TopicGenerator:
    
    reliability_evaluator = None
    
    def __init__(self, reliability_evaluator):
        self.reliability_evaluator = reliability_evaluator
        print("Topic Generator Initialization")
        
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
                    db.add_topic_to_db(new_topic)

        db.commit_db()
        return topics

    def generate_topics_input_news(self):
        topics = []
        count = 0

        newslist = InputNews.query.all()

        for news in newslist:
            count += 1
            if not news.topic is None:
                continue
            print(self.find_news_a_topic(news, topics))

        db.commit_db()
        return topics
    
    def get_topics_of_input_news_content(self):
        input_news_list = InputNews.query.all()
        count = 0
        with_topic_count = 0
        with_positive_reliability = 0
        
        for input_news in input_news_list:
            count += 1
            if not self.identify_topic_for_news(input_news) == None:
                if self.reliability_evaluator.sentiment_analyzer.identify_reliability(input_news):
                    with_positive_reliability += 1
                with_topic_count += 1
        
        print("With topic count " + str(with_topic_count) + " of " + str(count))
        print("With positive topic count " + str(with_positive_reliability) + " of " + str(count))
        return
    
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
            db.commit_db()
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
                if self.sentiment_analyzer.identify_reliability(input_news):

                    with_positive_reliability += 1 
                with_topic_count += 1
        
        print("With topic count " + str(with_topic_count) + " of " + str(count))
        print("With positive topic count " + str(with_positive_reliability) + " of " + str(count))
        return
    
    def generate_news_word_for_input_news(self, input_news_id, newscontent):
        newswords = NLP.input_count_occurrence(newscontent)
        db.update_input_news_wordfrequencies(input_news_id, newswords)
        db.commit_db()
        return
