from tqdm import tqdm
import gslides, twitter, analytics
import sys

enterprise = '--enterprise' in sys.argv

presentation = gslides.init()
tweets = twitter.get_tweets_plus() if enterprise else twitter.get_tweets()
i = 0
qs=[]

for tweet in tqdm(tweets):
    q, i = gslides.new_slide_plus(presentation, tweet, i) if enterprise else gslides.new_slide(presentation, tweet, i)
    qs += q

# TODO: add more detailed analytics for enterprise users
q, i = gslides.new_image_slide(presentation, analytics.daily_performance(tweets).decode('utf-8'), i)
qs += q

gslides.execute(presentation, qs)