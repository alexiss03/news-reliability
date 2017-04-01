import nltk, re
from nltk.probability import FreqDist
from create_db import db, News, Word, NewsWord
from collections import Counter
import enchant

def clean_data(paragraph):
		#strips the stray characters or non-alphanumeric characters
		paragraph = re.sub('[^0-9a-zA-Z\' ]+', '', paragraph) 

		#removes the articles (the, a) and other noise words
		paragraph = re.sub('(?i)(the|a|an|in|of|at|it|for|about|be|on|in)+\s+', ' ', paragraph)
		#print(paragraph.split())
		return paragraph


class NaturalLanguageProcessor:
	#customized counting occurrences of words
	@staticmethod
	def count_occurrence(paragraph): #no self in the parameter since this is a static method
		#clean/remove the stray characters in the text
		paragraph = clean_data(paragraph)

		dictionary = enchant.Dict('en_US');
		wordfrequencies = []
		occurrence = Counter(paragraph.split())
		for i in occurrence.items():
			#if English or a Proper Noun (capitalized)
			if(dictionary.check(i[0]) or i[0].istitle() or i[0].isupper()): 
				thisword = Word(i[0]);
				newsword = NewsWord(thisword, i[1])
				wordfrequencies.append(newsword)

		return wordfrequencies

	

#NLP.countoccurrence("HIHIHIHIHH hello the The A a philippines ; hello; he;llo don't I'm hello wor;ld world don't cry 10$ , jejd; cried hello's HHHHI")
#nlp.countoccurrence("The Ateneo Lady Eagles saw their 2-0 lead disappear, before hanging on to defeat the FEU Lady Tamaraws on Saturday, 25-20 25-22 17-25 21-25 15-8.")
#clean_data("The red brown fox jups over the lazy dog a an then philippines");