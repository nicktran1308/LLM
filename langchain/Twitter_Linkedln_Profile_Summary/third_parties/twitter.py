# ------------------------------- Import Libraries -------------------------------
import os
import logging
import tweepy

# ------------------------------- Logger Configuration -------------------------------
logger = logging.getLogger("twitter")

# ------------------------------- Twitter Client Initialization -------------------------------
twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
)

# ------------------------------- Scrape User Tweets -------------------------------
def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (excluding retweets or replies).
    Returns a list of dictionaries with fields: "text" and "url".
    """
    # Fetching user ID using the given username
    user_id = twitter_client.get_user(username=username).data.id
    
    # Fetching tweets for the user based on the given conditions
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    # Processing the tweets to desired format
    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {
            "text": tweet["text"],
            "url": f"https://twitter.com/{username}/status/{tweet.id}"
        }
        tweet_list.append(tweet_dict)

    return tweet_list

# ------------------------------- Main Execution -------------------------------
if __name__ == "__main__":
    print(scrape_user_tweets(username="hwchase17"))

