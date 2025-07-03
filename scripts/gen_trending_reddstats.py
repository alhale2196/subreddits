import argparse
from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://reddstats.com/ranking/relative'
PERIODS = ['daily', 'weekly']
SUBSCRIBER_BINS = ['10001-50000', '50001-100000', '100001-1000000']
LIMIT_PER_BIN = 7

def generate_trending(period: str) -> None:
    if period not in PERIODS:
        raise ValueError(f"Invalid period type. Must be one of {PERIODS}")

    subreddits = []
    for bin in SUBSCRIBER_BINS:
        url = f'{BASE_URL}?over18=False&period={period}&subscriber_classification={bin}'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        subreddit_elements = soup.select('div.item a[href^="/subreddit/"]')
        for element in subreddit_elements[:LIMIT_PER_BIN]:
            subreddits.append(element.text.strip())
    
    for subreddit in subreddits:
        print(subreddit)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate trending subreddits.')
    parser.add_argument('period', type=str, help='The period type (\'daily\' or \'weekly\')')
    args = parser.parse_args()
    generate_trending(args.period)