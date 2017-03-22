from createdb import db, News, Word

class DB:
	def updateworddb(wordfrequencies):
		#print(wordfrequencies)
		for word in wordfrequencies:
			#the word --> word
			#the count of that word --> wordfrequencies[word]
			if(Word.query.filter_by(word = word).first() is None):
				addedword = Word(word, wordfrequencies[word])
				db.session.add(addedword)
			else:
				updatedword = Word.query.filter_by(word = word).first()
				updatedword.count += wordfrequencies[word]

			db.session.commit()
			print("Word database successfully updated")


	@staticmethod
	def updatenewsdb(channel, title, pubdate, link, wordfrequencies):
		newslink = News(channel, title, pubdate, link, wordfrequencies)
		db.session.add(newslink)
		db.session.commit()
		print("News database successfully updated")
