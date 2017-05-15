#!/usr/bin/python
import sys
from math import sqrt
import requests
import json
import ast
import pickle



# Returns a distance-based        similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
# Get the list of shared_items
#	print "Calculating distance based similarity score\n"
	si={}
	for item in prefs[person1]:
		if item in prefs[person2]:
			si[item]=1
	# if they have no ratings in common, return 0
	if len(si)==0: return 0
# Add up the squares of all the differences
	sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
		for item in prefs[person1] if item in prefs[person2]])
	return 1/(1+sum_of_squares)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs,p1,p2):
#	print "Calculating distance based on Pearson correlation coefficient score\n"
# Get the list of mutually rated items
	si={}
	for item in prefs[p1]:
		if item in prefs[p2]: si[item]=1
	# Find the number of elements
	n=len(si)
	# if they are no ratings in common, return 0
	if n==0: return 0
	# Add up all the preferences
	sum1=sum([prefs[p1][it] for it in si])
	sum2=sum([prefs[p2][it] for it in si])
	# Sum up the squares
	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
	# Sum up the products
	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
# Calculate Pearson score
	num=pSum-(sum1*sum2/n)
	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
	if den==0: return 0
	r=num/den
	return r

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_pearson):
#	print "Calculating best matches for a person from preference matrix\n"
	scores=[(similarity(prefs,person,other),other)
	for other in prefs if other!=person]
# Sort the list so the highest scores appear at the top
	scores.sort( )
	scores.reverse( )
	return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
#method 1 of user user cf algo, P[user,item]=Sum over n(rating[other user,item]*similarityscore[user,other user])/sum over n(similarityscore[user,other user] 
def getRecommendations(person,similarity=sim_pearson):
	#print "Generating Recommendation based on user user cf\n"
	#person=int(strperson)
	totals={}
	simSums={}
	prefs=loadMovieLens()
	for other in prefs:
		# don't compare me to myself
		if other==person: continue
		sim=similarity(prefs,person,other)
		# ignore scores of zero or lower
		if sim<=0: continue
		for item in prefs[other]:
			# only score movies I haven't seen yet
			if item not in prefs[person] or prefs[person][item]==0:
				# Similarity * Score
				#totals.setdefault(item,0)
				totals[item]=prefs[other][item]*sim
				# Sum of similarities
				simSums.setdefault(item,0)
				simSums[item]+=sim
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items( )]
	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings

#recommendation using item item similarities
def transformPrefs(prefs):
	#print "Generating Item centric matrix for item item cf\n"
        result={}
        for person in prefs:
                for item in prefs[person]:
                        result.setdefault(item,{})
                        #Flip item and person
                        result[item][person]=prefs[person][item]
        return result

# Create a dictionary of items showing which other items they
# are most similar to.
def calculateSimilarItems(prefs,n=10):
	#print "Creating item similarity matrix\n"
	prefs=loadMovieLens()
	result={}
	# Invert the preference matrix to be item-centric
	itemPrefs=transformPrefs(prefs)
	c=0
	for item in itemPrefs:
		# Status updates for large datasets
		c+=1
		if c%100==0: print "%d / %d" % (c,len(itemPrefs))
		# Find the most similar items to this one
		scores=topMatches(itemPrefs,item,n=n,similarity=sim_distance)
		result[item]=scores
	return result

def getRecommendedItems(user):
	#print "Generating Recommendations based on item item cf\n"
	#user=int(struser)
	prefs=loadMovieLens()	
	userRatings=prefs[user]
	scores={}
	totalSim={}
	itemMatch=pickle.load( open( "../bin/similaritems.txt", "rb" ) )
	# Loop over items rated by this user
	for (item,rating) in userRatings.items( ):
		# Loop over items similar to this one
		for (similarity,item2) in itemMatch[item]:
			# Ignore if this user has already rated this item
			if item2 in userRatings: continue
			# Weighted sum of rating times similarity
			scores.setdefault(item2,0)
			scores[item2]+=similarity*rating
			# Sum of all the similarities
			totalSim.setdefault(item2,0)
			totalSim[item2]+=similarity
	# Divide each total score by total weighting to get an average
	rankings=[(score/totalSim[item],item) for item,score in scores.items( )]
	# Return the rankings from highest to lowest
	rankings.sort( )
	rankings.reverse( )
	return rankings 

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
		


#print sys.argv[2]
rankings=[]
if sys.argv[1]=='usercf':
	rankings=getRecommendations(sys.argv[2])
if sys.argv[1]=='itemcf':
	rankings=getRecommendedItems(sys.argv[2])


getjson=jsondata(rankings[0:int(sys.argv[3])])
print getjson
#print "Ranking: %s" % rankings[0:int(sys.argv[3])]
#print sys.argv
