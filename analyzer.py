import csv
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk import bigrams, ngrams
import datetime
#dont forget -- pipenv install py-dateutil
from dateutil import parser
from itertools import chain
#nltk.download('stopwords')


#this function returns one list with all of the tokenized words in a date range
def getTweetsInDateRange(date1, date2):
	words = []
	lowerDate = parser.parse(date1)
	upperDate = parser.parse(date2)
	with open('tweets.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		i = 0
		for row in csv_reader:
			if( i != 0):
				date = parser.parse(row[1])
				if (lowerDate < date) and (date < upperDate):
					text = row[0]
					words.extend(nltk.word_tokenize(text))
			i = i + 1
	return words

#this function returns a list of list where each list contains a list of all the words in a given tweet
def getSeperatedTweetsInDateRange(date1, date2):
	tweets = [[]]  #so the structure is [tweet, tweet, tweet], where each tweet is a list of words
	lowerDate = parser.parse(date1)
	upperDate = parser.parse(date2)
	with open('tweets.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		i = 0
		for row in csv_reader:
			if( i != 0):
				date = parser.parse(row[1])
				if (lowerDate < date) and (date < upperDate) and len(row[0]) > 0:
					text = row[0]
					tweets.append(nltk.word_tokenize(text))
			i = i + 1
	return tweets

#to clean our words up
def cleanWords(words, extraSymbols, excludeStopWords):
	customStopwords = ['https', 'http']
	customStopwords.extend(extraSymbols)
	stopWords = stopwords.words('english')
	stopWords.extend(customStopwords)

	words = [word for word in words if len(word) > 1]
	words = [word for word in words if not word.isnumeric()]
	words = [word.lower() for word in words]
	if excludeStopWords:
		words = [word for word in words if not word in stopWords]

	#remove punctuation at the end?
	#this removes all words with a symbol in extraSymbols
	keepWords = []
	if len(extraSymbols) > 0:
		for word in words:
			hasABadSymbol = False
			for c in word:
				if c in extraSymbols:
					hasABadSymbol = True
				if hasABadSymbol:
					break
			if not hasABadSymbol:
				keepWords.append(word)
	words = keepWords
					
	return words

#this returns the top words in a date range
def getTopWordsInRange(date1, date2):
	words = cleanWords(getTweetsInDateRange(date1, date2), [], True)
	topWords = nltk.FreqDist(words)
	for word, frequency in topWords.most_common(50):
   		print(u'{};{}'.format(word, frequency))


#http://locallyoptimal.com/blog/2013/01/20/elegant-n-gram-generation-in-python/
#returns ngrams from an input lize
def findngrams(inputList, n):
	#define our stopwords
	customStopwords = ['https', 'http']
	stopWords = stopwords.words('english')
	stopWords.extend(customStopwords)

	#create the ngrams
	ngrams = list(zip(*[inputList[i:] for i in range(n)]))

	#remove ngrams made entirely of stopwords
	newgrams = []
	for ngram in ngrams:
		hasANonStopWord = False
		for word in ngram:
			if word not in stopWords:
				hasANonStopWord = True
		if hasANonStopWord == True:
			newgrams.append(ngram)
			
	return newgrams

#this gets our top 
def getTopNgrams(date1, date2, n):
	extraSymbols = ['/', "'", '.', '`', '-']
	#get the tweets
	tweets = getSeperatedTweetsInDateRange(date1, date2)
	newTweets = [[]]

	#clean each tweet
	for tweets in tweets:
		newTweets.append(cleanWords(tweets, extraSymbols, False))
	tweets = newTweets
	
	#make the ngrams
	phrases = []
	for tweet in tweets:
		ngrams = findngrams(tweet, n)
		phrases.extend(ngrams)

	#get and print the most common
	topPhrases = nltk.FreqDist(phrases)
	for word, frequency in topPhrases.most_common(50):
   		print(u'{};{}'.format(word, frequency))


def test():
	#return 5
	#return getTopWordsInRange("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM")
	return getTopNgrams("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM", 2)


test()


#we have the tweets, what now?
#set up website?
#analyze
	#top words in a given time period!
	#top phrases
	#top topics
	#nicknames
	#emotion
	#capitilization
	#tweet popularity
		#popular in which groups