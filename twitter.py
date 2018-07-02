import tweepy
import engagement_api
from datetime import datetime, timedelta

auth = tweepy.OAuthHandler(secret.consumer_key, secret.consumer_secret)
try:
    with open('secret','r') as f:
        access_token, access_token_secret = [line.strip() for line in f.readlines()[:2]]
        auth.set_access_token(access_token, access_token_secret)
except:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input('Verifier: ')
    try:
        auth.get_access_token(verifier)
    except:
        print('Failed to retrieve access token.')
    with open('secret','w') as f:
        f.write(auth.access_token)
        f.write('\n')
        f.write(auth.access_token_secret)

API = tweepy.API(auth)
try: API.engagement
except:
    API.engagement = engagement_api.EngagementAPI(auth=auth)
    print("Plugging in our own engagement API")
me = API.me()

def get_tweets():
    cursor = API.user_timeline(id=me.id, count=50)
    min = datetime.today() - timedelta(days=7)
    tweets = []
    for tweet in cursor:
        if tweet.created_at < min: break
        tweets.append({
            'text': tweet.text,
            'time': tweet.created_at,
            'retweets': tweet.retweet_count,
            'favorites': tweet.favorite_count,
            'id': tweet.id_str
        })
    return tweets
