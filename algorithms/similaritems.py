from math import sqrt
import pickle

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


# Returns a distance-based similarity score for person1 and person2
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

#recommendation using item item similarities
def transformPrefs(prefs):
	print "Generating Item centric matrix for item item cf\n"
        result={}
        for person in prefs:
                for item in prefs[person]:
                        result.setdefault(item,{})
                        #Flip item and person
                        result[item][person]=prefs[person][item]
        return result

# Create a dictionary of items showing which other items they
# are most similar to.
def calculateSimilarItems(n=10):
	print "Creating item similarity matrix\n"
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
	pickle.dump( result, open( "similaritems.txt", "wb" ) )
	return result
	
def loadMovieLens(path='../../algorithms/ml-100k'):
	print "Loading data...\n"
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

result=calculateSimilarItems()
print "Success\n"
