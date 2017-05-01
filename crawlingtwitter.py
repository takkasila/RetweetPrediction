#Import the necessary methods from tweepy library
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import datetime, time
import json
import collections

consumer_key = 'B2belwJ2uBpWB8LJYdxkeLHH4'
consumer_secret = 'bbHVcfTpxaV78fGXPWLnfi3vkbi3CTqqmhL9B1CeHWjTdrFE2r'
access_token = '858235205471141888-WyasLMlGkn10yGNAYKNj9SQwL2YHdrm'
access_token_secret = 'fviwd7yotvuDpGazFHj4W7Blbmv6zsJdamOGjJ8d54uN8'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

dict = collections.OrderedDict()

api = API(auth)
queue = []
search_count = 0
max_search_node = 2
total_node_count = 0 

def readTweet(seed):
	tweets = api.user_timeline(seed, count = 40, include_rts = True)
	dict[seed] = collections.OrderedDict()
	dict[seed]['uid'] = seed
	dict[seed]['edge'] = collections.OrderedDict()
	for tweet in tweets:
		try:
			epochTime = int((tweet.retweeted_status.created_at -  datetime.datetime(1970,1,1)).total_seconds())
			# Already pushed in dictt
			if tweet.retweeted_status.user.id in dict[seed]['edge']:
				dict[seed]['edge'][tweet.retweeted_status.user.id]['count'] += 1
				dict[seed]['edge'][tweet.retweeted_status.user.id]['time_stamp'][
					dict[seed]['edge'][tweet.retweeted_status.user.id]['count']-1
				] = epochTime
			# Newly insert
			else:
				dict[seed]['edge'][tweet.retweeted_status.user.id] = collections.OrderedDict()
				dict[seed]['edge'][tweet.retweeted_status.user.id]['uid'] = tweet.retweeted_status.user.id
				dict[seed]['edge'][tweet.retweeted_status.user.id]['count'] = 1
				dict[seed]['edge'][tweet.retweeted_status.user.id]['time_stamp'] = collections.OrderedDict()
				dict[seed]['edge'][tweet.retweeted_status.user.id]['time_stamp']['0'] = epochTime
				queue.append(tweet.retweeted_status.user.id)
				global total_node_count
				total_node_count += 1
		except Exception as e:
			pass
	print "Done crawling: ", seed

if __name__ == '__main__':
	seed_user = api.get_user('waiiwall')
	queue.append(seed_user.id)
	while search_count < max_search_node:
		print("{}/{}".format(search_count, max_search_node))
		try:
			print "Try reading."
			seed = queue.pop(0)
			total_node_count += 1
			readTweet(seed)
		except tweepy.TweepError:
			print "Waiting 15 mins..."
			time.sleep(60 * 15)
			readTweet(seed)
		except Exception as e:
			print "Error"
			print e
		
		search_count+=1
		print("Total node: {}".format(total_node_count))
	with open("retweet3.json", "w") as fp:
		json.dump(dict, fp)