import json

from tweepy.binder import bind_api
from tweepy.parsers import JSONParser


class EngagementAPI:
    def __init__(
        self,
        auth=None,
        host='data-api.twitter.com',
        api_root='/insights/engagement',
        cache=None,
        compression=True,
        parser=None,
        retry_count=0,
        retry_delay=0,
        retry_errors=None,
        timeout=60,
        wait_on_rate_limit=False,
        wait_on_rate_limit_notify=False,
        proxy='',
    ):
        self.auth = auth
        self.host = host
        self.api_root = api_root
        self.cache = cache
        self.compression = compression
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.timeout = timeout
        self.wait_on_rate_limit = wait_on_rate_limit
        self.wait_on_rate_limit_notify = wait_on_rate_limit_notify
        self.parser = parser or JSONParser()
        self.proxy = {}
        if proxy:
            self.proxy['https'] = proxy

    def _request(
        self,
        path,
        *,
        tweet_ids,
        engagement_types,
        groupings,
        start=None,
        end=None
    ):
        headers = {"Content-Type": "application/json", "Content-type": "application/json"}
        payload = {
            'tweet_ids': tweet_ids,
            'engagement_types': engagement_types,
            'groupings': groupings,
        }
        #if start:
        #    payload['start'] = start.isoformat()
        #if end:
        #    payload['end'] = end.isoformat()
        print(path)
        print(payload)
        return bind_api(
            api=self,
            method='POST',
            path=path,
            payload_type='json',
            require_auth=True,
        )(post_data=json.dumps(payload), headers=headers)

    def historical(
        self,
        *,
        tweet_ids,
        engagement_types,
        groupings,
        start=None,
        end=None
    ):
        return self._request(
            '/historical',
            tweet_ids=tweet_ids,
            engagement_types=engagement_types,
            groupings=groupings,
            start=start,
            end=end,
        )

    def twentyeighthour(
        self,
        *,
        tweet_ids,
        engagement_types,
        groupings
    ):
        return self._request(
            '/28hr',
            tweet_ids=tweet_ids,
            engagement_types=engagement_types,
            groupings=groupings,
        )

    def totals(
        self,
        *,
        tweet_ids,
        engagement_types,
        groupings
    ):
        return self._request(
            '/totals',
            tweet_ids=tweet_ids,
            engagement_types=engagement_types,
            groupings=groupings,
        )
