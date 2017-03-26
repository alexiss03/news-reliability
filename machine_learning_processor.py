
from createdb import News, Topic
from sentiment_analyzer import SentimentAnalyzer

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

            if not news.topic is None:
                break

            self.news_belongs_to_any_topic(news, topics)

            if news.topic is None:
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


ml = MachineLearningProcessor()
allnews = News.query.all()
print(allnews)
#print(news1.first())
ml.generate_topics_from_newlist(allnews)
#ml.identify_topics([news1, news2])
