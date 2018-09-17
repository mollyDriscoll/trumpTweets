import urllib
from bs4 import BeautifulSoup
import csv

#to run: pipenv run python trumptweet.py
from twitter_scraper import get_tweets
tweets = [[]]
for tweet in get_tweets('realDonaldTrump', pages=25):
    #print(tweet['text'], tweet['time'])
    row = [tweet['text'], tweet['time']]
    tweets.append(row)



#write info to the csv file
with open('tweets.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(tweets)

csvFile.close()






#get the archived tweets
# archivePage = 'http://www.trumptwitterarchive.com/archive/loser'
# page = urllib.request.urlopen(archivePage)
# soup = BeautifulSoup(page, 'html.parser')

# print(soup)



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
