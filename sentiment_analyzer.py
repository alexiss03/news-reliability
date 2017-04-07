from create_db import News, Word, Topic

sentiment_dictionary = {}

class SentimentAnalyzer:

    def __init__(self):
        for line in open('resources/word_sentiments_2.txt'):
            word, score = line.split(' ')
            sentiment_dictionary[word] = int(score)



    def identify_reliability(self, news):

        variance_topic =  self.compute_variance_per_topic(news.topic)
        if news.topic == None or variance_topic < 0.01:
            return -1

        news_sentiment = self.compute_sentiment_news(news)
        topic_sentiment = self.compute_sentiment_per_topic(news.topic)

        print("average topic sentiment" + str(topic_sentiment))
        print("input news sentiment" + str(news_sentiment))

        score_reliability =  abs(topic_sentiment - news_sentiment) * 100

        print("reliability score:" + str(score_reliability))
        return score_reliability


    def compute_sentiment_news(self, news):
        sum = 0
        count = 0

        for news_word in news.news_words:
            word_sentiment = sentiment_dictionary.get(news_word.word.word,0)
            sum = sum + word_sentiment
            count += 1

        mean = 0
        if count != 0:
            mean = sum / count
        return mean


    def compute_sentiment_per_topic(self, topic):
        sum = 0
        count = 0
        topic_newslist = topic.newslist.all()

        for news in topic_newslist:
            sum = sum + self.compute_sentiment_news(news)
            count += 1

        mean = 0
        if count != 0:
            mean = sum / count
        return mean


    def compute_variance_per_topic(self, topic):
        score = 0
        scores = []
        news_count = len(topic.newslist.all())

        for news in topic.newslist:
            score = score + self.compute_sentiment_news(news)
            scores.append(score)

        mean = score / len(topic.newslist.all())


        for score in scores:
            variance = int((score - mean))^2

        variance = variance/news_count
        return variance