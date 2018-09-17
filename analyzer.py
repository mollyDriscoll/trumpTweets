import csv
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
import datetime
from dateutil import parser
#nltk.download('stopwords')

#top words, given time period

def getTweetsInDateRange(date1, date2):
	words = [[]]
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


#make list of words
#read in from csv file
words = getTweetsInDateRange("9/10/2018  5:53:11 PM","9/12/2018  5:53:11 PM")

#cleaning data
customStopwords = ['https', 'http']
stopWords = stopwords.words('english')
stopWords.extend(customStopwords)



words = [word for word in words if len(word) > 1]
words = [word for word in words if not word.isnumeric()]
words = [word.lower() for word in words]
words = [word for word in words if not word in stopWords]

topWords = nltk.FreqDist(words)

for word, frequency in topWords.most_common(50):
    print(u'{};{}'.format(word, frequency))




	


#we have the tweets, what now?
#set up website?
#analyze
	#top words in a given time period?
	#top topics
	#nicknames
	#emotion
	#capitilization
	#tweet popularity
		#popular in which groups