from matplotlib import pyplot as plt
import subprocess
import numpy as np

def daily_performance(tweets):
    buckets = dict()
    for tweet in tweets:
        day = tweet['time'].strftime('%m/%d')
        if day not in buckets:
            buckets[day] = {
                'retweets': 0,
                'favorites': 0
            }
        buckets[day]['retweets'] += tweet['retweets']
        buckets[day]['favorites'] += tweet['favorites']
    X, Y = zip(*(buckets.items()))
    ind = np.arange(len(X))
    retweets_Y = [y['retweets'] for y in Y]
    favorites_Y = [y['favorites'] for y in Y]
    p1 = plt.bar(ind, retweets_Y, width=0.4, color='#87575f')
    p2 = plt.bar(ind, favorites_Y, width=0.4, color='#4c3337', bottom=retweets_Y)
    plt.xlabel('Time')
    plt.xticks(ind, X)
    plt.ylabel('Engagement')
    plt.title('Engagement over 1 Week')
    plt.legend((p1[0], p2[0]), ('🔃', '❤️'))
    plt.savefig('engagement.png')
    url = (subprocess.check_output(['curl', '--upload-file', './engagement.png', 'https://transfer.sh/engagement.png']))
    if type(url) == list: url = url[0]
    url = url.strip()
    return url