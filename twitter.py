import tweepy
import engagement_api
from datetime import datetime, timedelta

with open('app_secret', 'r') as f:
    consumer_key, consumer_secret = [line.strip()
                                     for line in f.readlines()[:2]]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
try:
    with open('token_secret', 'r') as f:
        access_token, access_token_secret = [
            line.strip() for line in f.readlines()[:2]]
        auth.set_access_token(access_token, access_token_secret)
except:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input('Verifier: ')
    try:
        auth.get_access_token(verifier)
    except:
        print('Failed to retrieve access token.')
    with open('token_secret', 'w') as f:
        f.write(auth.access_token)
        f.write('\n')
        f.write(auth.access_token_secret)

API = tweepy.API(auth)
try:
    API.engagement
except:
    API.engagement = engagement_api.EngagementAPI(auth=auth)
    print("Plugging in our own engagement API")
me = API.me()


def get_tweets():
    cursor = API.user_timeline(id=me.id, count=50)
    min = datetime.today() - timedelta(days=7)
    tweets = []
    for tweet in cursor:
        if tweet.created_at < min:
            break
        tweets.append({
            'text': tweet.text,
            'time': tweet.created_at,
            'retweets': tweet.retweet_count,
            'favorites': tweet.favorite_count,
            'id': tweet.id_str
        })
    return tweets


def get_tweets_plus():
    cursor = API.user_timeline(id=me.id, count=50)
    min = datetime.today() - timedelta(days=7)
    tweets = []
    for tweet in cursor:
        if tweet.created_at < min:
            break
        tweets.append({
            'text': tweet.text,
            'time': tweet.created_at,
            'retweets': tweet.retweet_count,
            'favorites': tweet.favorite_count,
            'id': tweet.id_str
        })
    e = API.engagement.totals(tweet_ids=[
        t['id'] for t in tweets
    ],
        engagement_types=[
            'impressions',
            'engagements',
            'replies'
    ],
        groupings={
        '_': {
            'group_by': [
                'tweet.id',
                'engagement.type'
            ]
        }
    })
    for i, tweet in enumerate(tweets):
        tweets[i]['impressions'] = e['_'][tweet['id']]['impressions']
        tweets[i]['engagements'] = e['_'][tweet['id']]['engagements']
        tweets[i]['replies'] = e['_'][tweet['id']]['replies']
    return tweets
