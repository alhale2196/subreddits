import argparse
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException, Timeout, HTTPError


BASE_URL = 'https://reddstats.com/ranking/relative'
PERIODS = ['daily', 'weekly']
SUBSCRIBER_BINS = ['10001-50000', '50001-100000', '100001-1000000']
REQUEST_TIMEOUT = 90

def generate_trending(period: str, limit: int, over18: bool = False) -> None:
    if period not in PERIODS:
        raise ValueError(f"Invalid period type. Must be one of {PERIODS}")

    subreddits = []
    for bin in SUBSCRIBER_BINS:
        url = f'{BASE_URL}?over18={str(over18)}&period={period}&subscriber_classification={bin}'
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
        except Timeout:
            raise Timeout(f"Request timed out for period type {period}. Try again later.")
        except HTTPError as e:
            raise HTTPError(f"Request HTTP error for period type {period}. {e}")
        except RequestException as e:
            raise RequestException(f"Request Exception for period type {period}. Exception Message: {e}")
        except Exception as e:
            raise Exception(f"Exception for period type {period}. Exception Message: {e}")

        soup = BeautifulSoup(response.content, 'html.parser')
        subreddit_elements = soup.select('div.item a[href^="/subreddit/"]')
        for element in subreddit_elements[:limit]:
            subreddits.append(element.text.strip())
    
    for subreddit in subreddits:
        print(subreddit)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate trending subreddits.')
    parser.add_argument('period', type=str, help='The period type (\'daily\' or \'weekly\')')
    parser.add_argument("--nsfw", help="Whether to include NSFW subreddits", action="store_true")
    parser.add_argument("--limit", help="Number of subreddits to return per bin", type=int, default=7)
    args = parser.parse_args()
    if args.nsfw:
        generate_trending(args.period, limit=args.limit, over18=args.nsfw)
    else:
        generate_trending(args.period, limit=args.limit)