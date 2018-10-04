import csv
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk import bigrams, ngrams
import datetime
#dont forget -- pipenv install py-dateutil
from dateutil import parser
from itertools import chain
import re
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



#Get tokenized tweet word but separated by tweet
def getSeparatedTweetsInDateRange2(date1, date2):
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

def getSeparatedTweetsInDateRange(date1, date2):
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
# remove empty spaces, numbers, stopwords, and extrasymbols (if we want to, and makes all lowercase)
def cleanWords(words, extraSymbols, excludeStopWords, makeAllLowerCase):
	customStopwords = ['https', 'http']
	customStopwords.extend(extraSymbols)
	stopWords = stopwords.words('english')
	stopWords.extend(customStopwords)

	words = [word for word in words if len(word) > 1]
	words = [word for word in words if not word.isnumeric()]
	if makeAllLowerCase:
		words = [word.lower() for word in words]
	if excludeStopWords:
		words = [word for word in words if not word in stopWords]
	#remove punctuation at the end?
	#this removes all words with a symbol in extraSymbols


	
	if len(extraSymbols) > 0:
		keepWords = []
		for word in words:
			hasABadSymbol = False
			for c in word:
				if c in extraSymbols:
					hasABadSymbol = True
				if hasABadSymbol:
					break
			if not hasABadSymbol:
				keepWords.append(word)
		keepWords = []
	return words

#this returns the X top words in a date range
def getXTopWords(date1, date2, x):
	words = cleanWords(getTweetsInDateRange(date1, date2), [], True, True)
	topWords = nltk.FreqDist(words)
	retWords = []
	for word, frequency in topWords.most_common(x):
   		retWords.append((word, frequency))
	return retWords


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
def getXTopNgrams(date1, date2, x,  n):
	extraSymbols = ['/', "'", '.', '`', '-', "\\"]
	#get the tweets
	tweets = getSeparatedTweetsInDateRange(date1, date2)
	newTweets = [[]]

	#clean each tweet
	for tweets in tweets:
		newTweets.append(cleanWords(tweets, extraSymbols, False, True))
	tweets = newTweets
	
	#make the ngrams
	phrases = []
	for tweet in tweets:
		ngrams = findngrams(tweet, n)
		phrases.extend(ngrams)

	#get and return the most common
	topPhrases = nltk.FreqDist(phrases)
	ret = []
	for phrase, frequency in topPhrases.most_common(x):
   		ret.append((phrase, frequency))

	return ret

#lets get the top uppercase phrases
def getXTopUppercaseNgrams(date1, date2, x,  n):
	extraSymbols = ['/', "'", '.', '`', '-']
	#get the tweets
	tweets = getSeparatedTweetsInDateRange(date1, date2)
	newTweets = [[]]

	#clean each tweet
	for tweets in tweets:
		newTweets.append(cleanWords(tweets, extraSymbols, False, False))
	tweets = newTweets
	
	#make the ngrams
	phrases = []
	for tweet in tweets:
		ngrams = findngrams(tweet, n)
		phrases.extend(ngrams)

	#eliminate non uppercase phrases
	uppercasePhrases = []
	for phrase in phrases:
		isTitle = True
		for word in phrase:
			isTitle = isTitle and word[0].isupper()
		if isTitle:
			uppercasePhrases.append(phrase)

	#find teh topphrases
	topPhrases = nltk.FreqDist(uppercasePhrases)
	ret = []
	for word, frequency in topPhrases.most_common(x):
   		ret.append((word, frequency))

	return ret


#returns a tuple, (capitals not at the start of a sentence, capitals at the start)
def getCapitals(date1, date2):
	tweets = getSeparatedTweetsInDateRange(date1, date2)
	sentenceEnders = [",", ".", "?", "!"]
	#get capitals, ignoring first of sentence
	capitals = ([],[])
	for tweet in tweets:
		previousWasEndOfSentence = True
		for word in tweet:
			if word[0].isupper():
				if previousWasEndOfSentence:
					capitals[1].append(word)
				else:
					capitals[0].append(word)
			if word[len(word) -1].endswith("."):
				previousWasEndOfSentence = True
			else:
				previousWasEndOfSentence = False
	capitals = ((cleanWords(capitals[0], [], True, False)), (cleanWords(capitals[1], [], True, False)))
	return capitals

#get the most popular capital words
#need to clean things that should be capitalized, as in countries, names, I, The
def getXTopCapitals(date1, date2, x):
	capitals = getCapitals(date1, date2)
	topRandomCapitals = nltk.FreqDist(capitals[0])
	topFirstCapitals = nltk.FreqDist(capitals[1])
	retValue = []
	for word, frequency in topRandomCapitals.most_common(x):
		if word in capitals[1]:
			frequency = frequency + topFirstCapitals.get(word)
		retValue.append((word, frequency))
	return retValue




#make sure not a retweet
def XMostLikedTweets(date1, date2, x):
	lowerDate = parser.parse(date1)
	upperDate = parser.parse(date2)
	tweetsAndLikes = []
	with open('tweets.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		i = 0
		for row in csv_reader:
			if( i != 0):
				date = parser.parse(row[1])
				if (lowerDate < date) and (date < upperDate) and len(row[0]) > 0:
					entry = (row[2], row[0])
					tweetsAndLikes.extend(entry)
			i = i + 1
	print(tweetsAndLikes[0][0])
	tweetsAndLikes = sorted(tweetsAndLikes, key=lambda tup: tup[0])
	print(tweetsAndLikes[1][0])
	return tweetsAndLikes[0:x]

# def test():
	#print(getXTopWords("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM"))
	# print(getXTopNgrams("9/12/2018  5:53:11 AM","9/13/2018  5:53:11 PM", 5, 3))
	#print(getXTopCapitals("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM", 30))
	#print(getXTopUppercaseNgrams("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM", 15, 2))
	#XMostLikedTweets("9/12/2018  5:53:11 AM","9/18/2018  11:53:11 PM", 1)
	#print(getXTopWords("10/3/2018  5:53:11 AM","/2018  11:53:11 PM", 2))



# test()


#todo:
#link words to the tweets they come from
#from getXTopNgrams get rid of backslashes
#dealing wiht hashtags
#deal with contractions

#we have the tweets, what now?
#set up website?
#analyze
	#top words in a given time period!
	#top phrases!
	#top topics
	#find frequency of word
	#nicknames
	#emotion
	#capitilization
	#tweet popularity
		#popular in which groups
	#write tweets on a certain subject
	#filter out retweets
	#filter by containing a word
	