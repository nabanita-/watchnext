#!/usr/bin/python
import sys
import requests
import json
import ast


def loadMovieLens(path='../../algorithms/ml-100k'):
	#print "Loading data...\n"
        # Get movie titles
        movies={}
        for line in open(path+'/u.item'):
                (id,title)=line.split('|')[0:2]
                movies[id]=title
        # Load data
        prefs={}
        for line in open(path+'/u.data'):
                (user,movieid,rating,ts)=line.split('\t')
                prefs.setdefault(user,{})
                prefs[user][movies[movieid]]=float(rating)
        return prefs

def myRatings(given_user):
	prefs=loadMovieLens()
	myRatings={}
	for user,list in prefs.items():
		if given_user==user:
			myRatings=[(rating,movie) for movie,rating in prefs[user].items()]
			break
	return myRatings
			
def findmovieid(str):
	#print "Loading data...\n"
	# Get movie titles
	movies={}
	reqid=0
        for line in open('../../algorithms/ml-100k/u.item'):
                (id,title)=line.split('|')[0:2]
 		if title==str:
			reqid=id
			break
	return reqid
def jsondata(ratings):
	dic={}
	jsonrankingmovie=[]
	comma=","
	brk="("
	for item in ratings:
		m_title, rhs = item[1].split("(", 1)
		if comma in m_title:
			m_titlenew=m_title
			m_title,title_after_comma=m_titlenew.split(",",1)
		if brk in rhs:
			word1,word2=rhs.split(")", 1)
			m_date,bracket=rhs.split(")", 1)
		else:
			m_date,bracket=rhs.split(")", 1)
		#print m_title
		#print m_date 
		r = requests.get("http://www.omdbapi.com/?t="+m_title+"&y="+m_date+"&plot=short&r=json")
		dic["movie"]=ast.literal_eval(r.content)
		dic["rating"]=item[0]
		dic["id"]=findmovieid(item[1])
		error="Movie not found!"
		if error in r.content:
			continue
		jsonrankingmovie.append(dic.copy())
	newd=json.dumps(jsonrankingmovie,separators=(',', ': '))
	return newd

myratings=myRatings(sys.argv[1])
getjson=jsondata(myratings)
print getjson
#print "Ranking: %s" % rankings[0:int(sys.argv[3])]
#print sys.argv
