#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import json

consumer_key = 'B2belwJ2uBpWB8LJYdxkeLHH4'
consumer_secret = 'bbHVcfTpxaV78fGXPWLnfi3vkbi3CTqqmhL9B1CeHWjTdrFE2r'
access_token = '858235205471141888-WyasLMlGkn10yGNAYKNj9SQwL2YHdrm'
access_token_secret = 'fviwd7yotvuDpGazFHj4W7Blbmv6zsJdamOGjJ8d54uN8'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

dic = {}

api = API(auth)
queue = []
count = 0

def readTweet(seed):
	tweets = api.user_timeline(seed, count = 40, include_rts = True)
	dic[seed] = {}
	for tweet in tweets:
		try:
			if tweet.retweeted_status.user.id in dic[seed]:
				dic[seed][tweet.retweeted_status.user.id] += 1
			else:
				dic[seed][tweet.retweeted_status.user.id] = 1
		except:
			pass


if __name__ == '__main__':
	seed_user = api.get_user('waiiwall')

	queue.append(seed_user.id)
	while count < 2000:
		print("{}/2000".format(count))
		seed = queue.pop(0)
		try:
			readTweet(seed)
		except tweepy.TweepError:
			time.sleep(60 * 15)
			readTweet(seed)
		except:
			pass
		new_seed = [int(k) for k in dic[seed]]
		queue = queue+new_seed
		count+=1
	with open("retweet.json", "w") as fp:
		json.dump(dic, fp)