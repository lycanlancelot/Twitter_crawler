import tweepy
import token_key
import codecs
import pickle
import os.path
import time

def AuthTwitter():
	auth = tweepy.OAuthHandler(token_key.consumer_key, token_key.consumer_secret)
	auth.set_access_token(token_key.access_token, token_key.access_token_secret)
	api = tweepy.API(auth)
	return api

def ConvertTime(timea):
	yeara = timea.split('-')[0][-4:]
	montha = timea.split('-')[1]
	day = timea.split('-')[2][:2]
	# print day
	return yeara, montha, day

def FindTweetsOfUser(user_id):
	res = api.user_timeline(id = user_id, count = 100)
	for tweet in res:
		tw=tweet.text.encode('ascii', 'ignore')
		print '-----------------------------'
		timestr = str(tweet.created_at)
		# print 'Name: ', tweet.user.name.encode('ascii', 'ignore')
		print 'User: ', user_id
		print 'Tweet: ', tw
		print 'Time: ', timestr 
		print 'Geo: ', tweet.geo

def FindUsersInRT(OfficialAccount):
	interest_user=[]
	tastour = api.user_timeline(id = OfficialAccount, count = 400)
	# results = api.search(q=['Launceston'],show_user=True, lan='en',result_type='recent')
	for tweet in tastour:
		# print str(tweet).encode('ascii', 'ignore')
		
		tw=tweet.text.encode('ascii', 'ignore')
		timestr = str(tweet.created_at)
		if 'RT' in tw:
			# print 'Name: ', tweet.user.name.encode('ascii', 'ignore')
			# print 'Tweet: ', tw
			# print 'Time: ', timestr
			# ConvertTime(timestr)

			user = tw.split('@')[1].split(':')[0]
			# print user
			interest_user.append(user)
	return interest_user

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

def PrintUsers(Users, filename):
	f = open(filename+'_users.txt', 'w')
	for user in Users:
		# print'--------------------------------------'
		# print 'USER_ID: ',user
		FindTweetsOfUser(user)
		f.write(user+'\n')
		# print ' '
	f.close()


def Deduplicate(lista):
	listb = set(lista)
	return list(listb)

def FindTweetsFromOfficialAccount():
	users = FindUsersInRT('tasmania')
	users = Deduplicate(users)
	PrintUsers(users,"tasoffRT")



def FindTweetsFromUserPost(keywords):
	pool = []
	for keyword in keywords:
		results = api.search(q=keyword,lan='en',count=100)
		for tweet in results:
			nm = tweet.user.name.encode('ascii', errors='ignore')
			date = ConvertTime(str(tweet.created_at))
			tw = tweet.text.encode('ascii', 'ignore')
			tw_id = tweet.id
			print nm, tw_id
			pool.append((keyword, nm, tw_id, tw, date))
	return pool


def FindTweets(count):
	count = str(count)
	if not os.path.isfile("tweets"+count+".pickle"):
		place_file = codecs.open('POI_places.txt',encoding='utf-8', mode='r')
		keywords = place_file.read().encode('ascii', errors='ignore').split(',')
		print len(keywords)
		pool = FindTweetsFromUserPost(keywords)
		pool.sort(key=lambda tup: tup[0])

		pickle_file = open("tweets"+count+".pickle","wb")
		pickle.dump(pool, pickle_file)
		pickle_file.close()
		print "Saved"

	pickle_file = open("tweets"+count+".pickle",'rb')
	pool = pickle.load(pickle_file)
	pickle_file.close()
	return pool

if __name__ == '__main__':
	api  = AuthTwitter()
	# FindTweetsFromOfficialAccount()
	pool = FindTweets(300)
 	# keyword, Tweet_user, Tweet_ID, Tweet, Tweet_Date in pool 
	# print tweets
	pre = "none"
	ex_id = 0
	target = []
	flag = 0
	head = 1e100
	for keyword,people,tw,tweet,date in pool:
		print "keyword: ",keyword
		print "Tweet: ",tweet,"\nDate: ", date
		tw = int(tw)
		if people!=pre:
			if flag ==1:
				target.append((pre, head, ex_id))
			flag = 0
			head = 1e100
			ex_id = 0
		else :
			flag = 1
			if tw < head:
				head = tw
			if tw > ex_id:
				ex_id = tw
		pre = people
	if flag==1:
		target.append(ex_id)

	print len(target)
	res = []
	if not os.path.isfile('tourist_tweets.pickle'):
		res = []
	else:
		f = open('tourist_tweets.pickle','rb')
		res = pickle.load(f)
		f.close()
	ct = 0
	for user_id, ida, idb in target:
		try:
			tweets = api.user_timeline(id = user_id)
			res.append((user_id, tweets))
		except:
			ct = ct
		ct = ct + 1
		print ct
		
	f = open('tourist_tweets.pickle','wb')
	pickle.dump(res, f)
	f.close()
	print "Saved Tourist Tweets"
