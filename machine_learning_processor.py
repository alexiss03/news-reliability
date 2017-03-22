import uuid

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from createdb import News, Topic

class MachineLearningProcessor:
    def identify_topics(self, newslist):
        topics = []
        
        for news in newslist:
            for topic in topics:
                if self.news_belongs_to_topic(topic,news):
                    break
            
            if news.topic is None:
                topic_word = []
                for news_word in sorted(news.news_words)[:5]:
                    topic_word.append(news_word.word)

                new_topic = Topic(topic_word)
                topics.append(new_topic)

        print("topic:" + str(topics))
        return topics
                

    def news_belongs_to_topic(self,topic, news):
        topic_count = len(topic.words)
        match_words = 0
        
        for news_word in sorted(news.news_words)[:5]:
            if news_word.word in topic.words:
                match_words +=1
                
        if match_words/topic_count > 0.8:
            news.topic = topic
            return True
        else:
            return False


#dummy data

#word1 = Word("the")
#word2 = Word("quick")
#word3 = Word("brown")
#word4 = Word("fox")
#word5 = Word("jump")
#word6 = Word("over")
#word7 = Word("the")

#newsword1 = NewsWord(word1, 1)
#newsword2 = NewsWord(word2, 2)
#newsword3 = NewsWord(word3, 3)
#newsword4 = NewsWord(word4, 4)
#newsword5 = NewsWord(word5, 5)
#newsword6 = NewsWord(word6, 6)
#newsword7 = NewsWord(word1, 4)
#newsword8 = NewsWord(word2, 4)


#news1 = News("abscbn", "The quick brown fox jumps over the lazy", "01-01-01", "http://www.google.com",[newsword1, newsword2, newsword3, newsword4, newsword5, newsword6])
#news2 = News("abscbn", "The quick brown fox jumps over the lazy", "01-01-01", "http://www.google.com",[newsword4, newsword3, newsword5, newsword6])
            
ml = MachineLearningProcessor()
allnews = News.query.all()
print(allnews)
#print(news1.first())
ml.identify_topics(allnews)
#ml.identify_topics([news1, news2])
