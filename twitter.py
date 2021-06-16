import re
import tweepy as tw
import csv

# LIST OF KEYWORDS TO SEARCH AND FILE PATH
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\Twitter\twitter_data.csv'
search_words = "Canada OR University OR Dalhousie University OR Halifax OR Canada Education"

# API KEYS OF TWITTER APPLICATION
consumer_key = "vpM3Pa0mfneYPerTYdGoXmiy6"
consumer_secret = "10LbKBMaZwfpZCf4Ixvhk74c9wRcgQ7PSnmMug7skn3O7JiZl2"
access_token = "1232330657872961536-0ZDd1oPvJMFqYSu7TbfepbseqcyrmI"
access_token_secret = "duQF9ENYaJPdNWUFxgQjAcb1c3AF55L1Ydu7olzcUx5LB"

# AUTHORIZATION AND INITIALIZE API ENDPOINT [7]
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

all_tweets = []


# FUNCTION TO REMOVE EMOJIS,URLS AND SPECIAL CHARACTERS FROM TEXT [1]
def clean_text(input_string):
    emoji_pattern = re.compile('['
                               '\U0001F1E0-\U0001F1FF'  # flags (iOS)
                               '\U0001F300-\U0001F5FF'  # symbols & pictographs
                               '\U0001F600-\U0001F64F'  # emoticons
                               '\U0001F680-\U0001F6FF'  # transport & map symbols
                               '\U0001F700-\U0001F77F'  # alchemical symbols
                               '\U0001F780-\U0001F7FF'  # Geometric Shapes Extended
                               '\U0001F800-\U0001F8FF'  # Supplemental Arrows-C
                               '\U0001F900-\U0001F9FF'  # Supplemental Symbols and Pictographs
                               '\U0001FA00-\U0001FA6F'  # Chess Symbols
                               '\U0001FA70-\U0001FAFF'  # Symbols and Pictographs Extended-A
                               '\U00002702-\U000027B0'  # Dingbats
                               '\U000024C2-\U0001F251'
                               ']+', flags=re.UNICODE)
    string = emoji_pattern.sub(r'', input_string)
    string = re.sub(r"[^a-zA-Z0-9]+", ' ', input_string)  # remove Urls from text [2]
    # remove special characters [3]
    string = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', input_string, flags=re.MULTILINE)
    return string


# COLLECT TWEETS [7]
tweets = tw.Cursor(api.search,
                   q=search_words,
                   lang="en").items(3000)
for tweet in tweets:
    # CHECK THE STATUS OF RETWEETED AND QUOTED TWEETS
    is_retweeted = hasattr(tweet, "retweeted_status")
    is_quoted = hasattr(tweet, "quoted_status")

    if is_retweeted is True:
        re_text = tweet.retweeted_status.text
        text = tweet.text

        # clean tweet text, remove urls, special charatecrs and emoticons
        result = clean_text(text)
        retweeted_result = clean_text(re_text)

        t = {'ID': tweet.user.id, 'Text': result, 'UserName': tweet.user.screen_name,
             'Retweeted_text': retweeted_result,
             'Retweeted_username': tweet.retweeted_status.user.screen_name,
             'Location': tweet.user.location, 'Time': tweet.created_at}
        all_tweets.append(t)

    elif is_quoted is True:
        quoted_text = tweet.quoted_status.text
        text = tweet.text

        # clean tweets
        result = clean_text(text)
        quoted_result = clean_text(quoted_text)

        t = {'ID': tweet.user.id, 'Text': result, 'UserName': tweet.user.screen_name,
             'Quoted_text': quoted_result, 'Quoted_username': tweet.quoted_status.user.screen_name,
             'Location': tweet.user.location, 'Time': tweet.created_at}
        all_tweets.append(t)

    else:
        text = tweet.text

        # clean Tweets
        result = clean_text(text)

        t = {'ID': tweet.user.id, 'Text': result, 'UserName': tweet.user.screen_name,
             'Location': tweet.user.location, 'Time': tweet.created_at}
        all_tweets.append(t)

# WRITE DATA INTO CSV FILE
with open(file_path, 'w', encoding='utf-8', newline='') as tweet_data:
    writer = csv.DictWriter(tweet_data, fieldnames=["ID", "Text", "UserName", "Retweeted_text", "Retweeted_username",
                                                    "Quoted_text", "Quoted_username", "Location", "Time"])
    writer.writeheader()
    # collect a list of tweets
    writer.writerows(all_tweets)
