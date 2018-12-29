import tweepy
from twilio.rest import Client
import time
import sys


class ElonAlert:

    def __init__(self):
        self.twitter_client = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.twitter_client.set_access_token(access_token, access_secret)
        self.twitter_api = tweepy.API(self.twitter_client, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
        self.elon_tweets = []

    def get_tweets(self):
        tweets = self.twitter_api.user_timeline(id="elonmusk", count=15, include_rts=False, exclude_replies= True )
        for tweet in tweets:
            text = tweet.text.encode('utf-8')
		if 'Tesla' in text:
            self.elon_tweets.append(text)

    def check_latest_tweets(self):
        latest_tweets = self.twitter_api.user_timeline(id="elonmusk", count=15, include_rts=False, exclude_replies= True )
        arr = []
        for tweet in latest_tweets:
            text = tweet.text.encode('utf-8')
            arr.append(text)
        if arr == self.elon_tweets:
            return True
        else:
            self.elon_tweets = arr
            return False

    def send_message(self):
        message = self.twilio_client.messages.create(
            to = "", # your number as 11111111111
            from_= "", # your twilio number
            body= "Elon Musk just tweeted: " + self.elon_tweets[0])

if __name__ == "__main__":
    alert = ElonAlert()
    alert.get_tweets()
    while True:
        if not alert.check_latest_tweets():
            alert.send_message()
            time.sleep(300)
