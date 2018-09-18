import analyzer
import csv


date1 = "9/12/2018  5:53:11 AM"
date2 = "9/13/2018  5:53:11 PM"


a = analyzer
# tweetsInRange = a.getTweetsInDateRange(date1, date2)
# separatedTweetsInRange = a.getSeparatedTweetsInDateRange(date1, date2)
# row0 = "0,".join(tweetsInRange)
# with open('testAnswers.csv', 'w') as csvFile:
#     writer = csv.writer(csvFile)
#     writer.writerows(row0)




#record and check answer

def testTopXWords():
	top5Words = a.getXTopWords(date1, date2, 5)
	assert (top5Words[0][0] == 'florence')
	assert (top5Words[1][0] == 'hurricaneflorence')
	assert (top5Words[2][0] == 'hurricane')
	assert (top5Words[3][0] == 'carolina')
	assert (top5Words[4][0] == 'south')


def testXTopNgrams():
	top53grams = a.getXTopNgrams(date1, date2, 5, 3)
	assert(top53grams[0][0][0] == 'senate')
	assert(top53grams[0][0][1] == 'intelligence')
	assert(top53grams[0][0][2] == 'committee')
	assert(top53grams[0][1]) == 4
	assert(top53grams[1][0][0] == 'google')
	assert(top53grams[1][0][1] == 'play')
	assert(top53grams[1][0][2] == 'http')
	assert(top53grams[1][1]) == 3
	assert(top53grams[3][0][0] == 'for')
	assert(top53grams[3][0][1] == 'hurricane')
	assert(top53grams[3][0][2] == 'florence')
	assert(top53grams[3][1]) == 2
	# print(top53grams)

def testXTopUppercaseNgrams():
	get5TopUppercase2grams = a.getXTopUppercaseNgrams(date1, date2, 5, 2)
	assert get5TopUppercase2grams[0][0][0] == 'Hurricane'
	assert get5TopUppercase2grams[0][0][1] == 'Florence'
	assert get5TopUppercase2grams[0][1] == 6
	assert get5TopUppercase2grams[1][0][0] == 'South'
	assert get5TopUppercase2grams[1][0][1] == 'Carolina'
	assert get5TopUppercase2grams[1][1] == 4
	#print(get5TopUppercase2grams)

def testXTopCapitals():
	top5Capitals = a.getXTopCapitals(date1, date2, 5)
	assert top5Capitals[0][0] == 'Florence'
	assert top5Capitals[0][1] == 11
	assert top5Capitals[1][0] == 'HurricaneFlorence'
	assert top5Capitals[1][1] == 8
	assert top5Capitals[2][0] == 'Carolina'
	assert top5Capitals[2][1] == 7
	# print(top5Capitals)



testTopXWords()
testXTopNgrams()
testXTopUppercaseNgrams()
testXTopCapitals()
