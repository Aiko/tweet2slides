from tqdm import tqdm
import gslides, twitter

presentation = gslides.init()
tweets = twitter.get_tweets()
i = 0

for tweet in tqdm(tweets):
    _, i = gslides.new_slide(presentation, tweet, i)