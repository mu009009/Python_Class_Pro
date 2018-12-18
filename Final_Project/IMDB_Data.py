from imdb import IMDb
import csv
import requests
from requests.exceptions import HTTPError

# def get_status(url):
# 	r = requests.get(url, allow_redirects=False)
# 	return r.status_code

# create an instance of the IMDb class
ia = IMDb()

def transIndex(index):
	return '%007d'%index


def getMovieInfo(indexNo):
	index = transIndex(indexNo)
	# get a movie
	r = requests.get('https://www.imdb.com/title/tt'+index+'/plotsummary', allow_redirects=False)
	status = r.status_code
	# print(status)
	if(status != 404):
		movie = ia.get_movie(index)
	else:
		print('404 Found')
		movie = None
	return movie

# indexNo = 133093 // The Martix
# indexNo = 9392988 // The Max ID
indexNo = 220000
accteptableMovie = []
temporyMovie = None

while indexNo < 240000:

	if ((indexNo%1000)==0):
		indexReport = transIndex(indexNo)
		print('Current Number: '+ indexReport)

	try:
		temporyMovie = getMovieInfo(indexNo)
		if(temporyMovie!= None):
			if((temporyMovie['rating'] != None) and (temporyMovie['year'] != None) and (temporyMovie['actors'] != None)):
				accteptableMovie.append(temporyMovie)
	except Exception:
		pass
	indexNo += 1

# print(temporyMovie['genres'])

with open('movie_data.csv','a') as csvfile:
	fieldnames = ['movie_name','genres','rating','year']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)

	writer.writeheader()
	for current in accteptableMovie:
		# actors = ''
		genres = ''
		# directors = ''

		# for actor in current['actors']:
		# 	actors = actors + actor + ','
		for genre in current['genres']:
			genres = genres + genre + ','
		# for director in current['directors']:
		# 	directors = directors + director + ','

		# actors = actors.Remove(actors.Length-1)
		genres = genres[:-1]
		# directors = directors.Remove(directors.Length-1)
		# actors = current['actors']
		# directors = current['directors']
		# genres = current['genres']
		rating = current['rating']
		year = current['year']

		writer.writerow({'movie_name': current, 'genres': genres, 'rating': rating, 'year': year})
