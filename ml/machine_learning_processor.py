import uuid

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///words.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

# Table for many-to-many relationship
WordTopic = db.Table('WordTopic',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('topic_id', db.Integer, db.ForeignKey('word.word_id')),
    db.Column('word_id', db.Integer, db.ForeignKey('topic.topic_id')))

class Word(db.Model):
    __tablename__ = "word"
    id = db.Column("word_id", db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(100))
    #news_word_id = db.Column(db.Integer, db.ForeignKey('news_word.news_word_id'))
    news_word = db.relationship('NewsWord', backref="word", lazy = 'dynamic')
    #topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'))
    topic = db.relationship('Topic', secondary=WordTopic, backref='words')
    def __init__(self, word):
        self.word = word

    def __repr__(self):
        return '<Word %r>' % (self.word)


class NewsWord(db.Model):
    __tablename__ = "news_word"
    id = db.Column('news_word_id', db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.word_id'))
    word_count = db.Column(db.Integer)
    news_id = db.Column(db.Integer, db.ForeignKey('news.news_id'))
    
    def __init__(self, word, count):
        word.news_word.append(self)
        self.word_count = count
        
    def __repr__(self):
        return '<News Word %r: %r>' % (self.word.word, self.word_count)

    def __lt__(self, other):
        return self.word_count < other.word_count
    
    
class News(db.Model):
    __tablename__ = "news"
    id = db.Column('news_id', db.Integer, primary_key=True)
    channel = db.Column(db.String(100)) #either GMA, ABS, RAPPLER, INQUIRER
    title = db.Column(db.String(100))
    pubdate = db.Column(db.String(100))
    link = db.Column(db.String(200)) #link of the news site
    news_words = db.relationship("NewsWord", backref="news", lazy='dynamic')
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'))
    
    def __init__(self, channel, title, pubdate, link, news_words):
        self.channel = channel
        self.title = title
        self.pubdate = pubdate
        self.link = link
        self.news_words = news_words
    
    def __repr__(self):
        return '<Newslink: %r>' % self.title
    
    
class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column('topic_id', db.Integer, primary_key=True)
    news = db.relationship("News", backref="topic", lazy='dynamic')
    word = db.relationship('Word', secondary=WordTopic, backref='topics')
    
    def __init__(self, words):
        self.words = words
        
    def __repr__(self):
        return '<Topic: %r>' % list(self.words)
    

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

word1 = Word("the")
word2 = Word("quick")
word3 = Word("brown")
word4 = Word("fox")
word5 = Word("jump")
word6 = Word("over")
word7 = Word("the")

newsword1 = NewsWord(word1, 1)
newsword2 = NewsWord(word2, 2)
newsword3 = NewsWord(word3, 3)
newsword4 = NewsWord(word4, 4)
newsword5 = NewsWord(word5, 5)
newsword6 = NewsWord(word6, 6)
newsword7 = NewsWord(word1, 4)
newsword8 = NewsWord(word2, 4)


news1 = News("abscbn", "The quick brown fox jumps over the lazy", "01-01-01", "http://www.google.com",[newsword1, newsword2, newsword3, newsword4, newsword5, newsword6])
news2 = News("abscbn", "The quick brown fox jumps over the lazy", "01-01-01", "http://www.google.com",[newsword4, newsword3, newsword5, newsword6])
            
ml = MachineLearningProcessor()
ml.identify_topics([news1, news2])
