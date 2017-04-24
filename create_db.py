from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///words.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


# Table for many-to-many relationship (PARANG BALIKTAD YUNG topic_id AND word_id?)
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
    newscontent = db.Column(db.String(100000))
    link = db.Column(db.String(200)) #link of the news site
    news_words = db.relationship("NewsWord", backref="news", lazy='dynamic')
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'))
    sentiment = db.Column(db.Float)
    
    def __init__(self, channel, title, pubdate, link, news_words, newscontent):
        self.channel = channel
        self.title = title
        self.pubdate = pubdate
        self.link = link
        if news_words:
            self.news_words = news_words
        self.newscontent = newscontent
    
    def __repr__(self):
        return '<Newslink: %r>' % self.title


# TODO: Create a class InputNews that is subclass of News with an initializer of raw input string only; channel, pubdate, link, topic_id can be null but news_words must be populated by this initializer
class InputNews(db.Model):
    __tablename__ = "inputnews" 
    
    id = db.Column('input_news_id', db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.topic_id'))
    sentiment = db.Column(db.Float)
    content = db.Column(db.String(1000))

    def __init__(self, content, news_words):
        News.__init__(self, "channel", "title", "pubdate", "link", news_words, content)
        self.content = content

    def __repr__(self):
        return '<InputNews: %r>' % self.raw_input_string


class Topic(db.Model):
    __tablename__ = "topic"
    id = db.Column('topic_id', db.Integer, primary_key=True)
    newslist = db.relationship("News", backref="topic", lazy='dynamic')
    word = db.relationship('Word', secondary=WordTopic, backref='topics')
    
    def __init__(self, words):
        self.word = words
        
    def __repr__(self):
        return '<Topic: %r>' % list(self.words)

#print(Newslink.query.all())			
#db.drop_all(bind=None)
db.create_all()