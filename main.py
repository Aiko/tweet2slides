from tqdm import tqdm
import gslides, twitter
import sys

enterprise = '--enterprise' in sys.argv

presentation = gslides.init()
tweets = twitter.get_tweets_plus() if enterprise else twitter.get_tweets()
i = 0

for tweet in tqdm(tweets):
    _, i = gslides.new_slide_plus(presentation, tweet, i) if enterprise else gslides.new_slide(presentation, tweet, i)