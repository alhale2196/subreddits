import os
import praw
from typing import List

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
MIN_LIMIT = 1000

def generate_popular_subreddits() -> None:
    # Replace these with your own credentials
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')

    # Authenticate with Reddit
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=USER_AGENT)

    # Get popular subreddits
    popular_subreddits: List[praw.models.Subreddit] = list(reddit.subreddits.popular(limit=None, params={'show': 'all'}))

    # Sanity check
    if len(popular_subreddits) < MIN_LIMIT:
        raise ValueError(f'Warning: Only {len(popular_subreddits)} subreddits found, expected more than {MIN_LIMIT}.')

    for subreddit in popular_subreddits:
        print(subreddit.display_name)

if __name__ == '__main__':
    generate_popular_subreddits()