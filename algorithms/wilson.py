import json
import sys
from math import sqrt
import requests
import ast


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
                m_title=movies[movieid]
                prefs.setdefault(m_title,{})
		prefs[m_title][user]=float(rating)
	#print prefs
        return prefs

def jsondata(rankings):
	dic={}
	jsonrankingmovie=[]
	comma=","
	for item in rankings:
		m_title, rhs = item[1].split("(", 1)
		if comma in m_title:
			m_titlenew=m_title
			m_title,title_after_comma=m_titlenew.split(",",1)
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


def wilson():
	prefs=loadMovieLens()
	#userRatings=prefs[user]
	totalrating={}
	ratingcount={}
	wilsonscore={}
	#score={}
	z=1.96 #for 95% confidence
	zsqbytwo=z*z/2
	zsqbyfour=z*z/4
	zsq=z*z
	for (movie,ratelist) in prefs.items( ):
		for (user,rating) in prefs[movie].items():
			totalrating.setdefault(movie,0)
			ratingcount.setdefault(movie,0)			
			totalrating[movie]+=float(prefs[movie][user])
			ratingcount[movie]+=1.00
	#calculating average rating for each movie
	average=[(total/ratingcount[movie],movie) for movie,total in totalrating.items()]
	#net positive value
	#average is a list with =['avgrating':'movie']
	pos=[((float((item[0])-1)/4),item[1]) for item in average]
	#pos is a list with =['pos':'movie']
	for item in pos:
		wilsonscore.setdefault(item[1],0.0)
		n=totalrating[item[1]]
		#taking lower bound of wilsoln score
		score=(item[0]+(zsqbytwo/n)-(z*sqrt(((item[0]*(1-item[0])/n) + (zsqbyfour/(n*n))))))/(1+zsq/n)
		wilsonscore[item[1]]=1.0+4.0*score
	rankings=[(score,item) for item,score in wilsonscore.items( )]
	# Return the rankings from highest to lowest
	rankings.sort( )
	rankings.reverse( )
	return rankings

rankings=wilson()
getjson=jsondata(rankings[0:int(sys.argv[1])])
print getjson

