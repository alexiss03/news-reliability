import nltk, re
from nltk.probability import FreqDist

class NLP:

	#customized counting occurrences of words
	def countoccurrence(self, paragraph):
		#the problem of this, it will remove also the apostrophe on possessive words
		#paragraph = re.sub('[^\w]+', ' ', paragraph).lower()
		paragraph = re.sub('[,.;/!]+', ' ', paragraph)
		
		unique_words = set(paragraph.split()); #gets only the unique words
		#print("UNIQUE WORDS" + unique_words)

		wordcount = []
		for word in unique_words:
			count = sum(1 for _ in re.finditer(word, paragraph))
			#print(str(count) + " " + word)
			wordcount.append(count)

		#transform into a dictionary where the key is the word, and value is the frequency
		wordfrequencies = dict(zip(unique_words, wordcount))
		print(wordfrequencies)
		
		#updateworddb(wordfrequencies)  #update the word database


nlp = NLP()
#nlp.countoccurrence("HIHIHIHIHH don;t cry 10$ , jejd; cried hello's HHHHI")
nlp.countoccurrence("The Ateneo Lady Eagles saw their 2-0 lead disappear, before hanging on to defeat the FEU Lady Tamaraws on Saturday, 25-20 25-22 17-25 21-25 15-8.")