from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///words.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


#class of words
class Word(db.Model):
	id = db.Column('word_id', db.Integer, primary_key=True)
	word = db.Column(db.String(100))
	count = db.Column(db.Integer)

	def __init__(self, word, count):
		self.word = word
		self.count = count

	def __repr__(self):
		return '<Word-> %r: %r>' % (self.word, self.count)


#class of the newslinks
class Newslink(db.Model):
	id = db.Column('news_id', db.Integer, primary_key=True)
	channel = db.Column(db.String(100)) #either GMA, ABS, RAPPLER, INQUIRER
	title = db.Column(db.String(100))
	pubdate = db.Column(db.String(100))
	link = db.Column(db.String(200)) #link of the news site


	def __init__(self, channel, title, pubdate, link):
			self.channel = channel
			self.title = title
			self.pubdate = pubdate
			self.link = link

	def __repr__(self):
			return '<Newslink: %r>' % self.title



#print(Newslink.query.all())			
#db.drop_all(bind=None)
db.create_all()