from create_db import News, Word, Topic

sentiment_dictionary = {}

class SentimentAnalyzer:

    def __init__(self):
        for line in open('resources/word_sentiment_value.txt'):
            word, score = line.split('\t')
            sentiment_dictionary[word] = int(score)


    def identify_reliability(self, news):

        if news.topic == None or self.compute_variance_per_topic(news.topic) < 3:
            return -1

        news_sentiment = self.compute_sentiment(news)
        topic_sentiment = self.compute_sentiment_per_topic(news.topic)
        score_reliabiltiy = 10 - (abs(news_sentiment-topic_sentiment) * 2)
        return score_reliabiltiy


    def compute_sentiment(self, news):
        sum = 0

        for word in news.news_words:
            sum = sum + sentiment_dictionary.get(word.word,0)

        mean = sum / len(news.news_words)
        print("news" + news.news_id + "sentiment" + str(mean))
        return mean



    def compute_sentiment_per_topic(self, topic):

        sum = 0
        for news in topic.newslist:
            sum = sum + self.compute_sentiment(news)

        mean = sum / len(topic.newslist)
        return mean



    def compute_variance_per_topic(self, topic):

        score = 0
        scores = []

        for news in topic.newslist:
            score = score + self.compute_sentiment(news)
            scores.append(score)

        mean = score / len(topic.newslist)


        for score in scores:
            variance = (score - mean)^2

        variance = variance/len(topic.newslist)
        return variance
