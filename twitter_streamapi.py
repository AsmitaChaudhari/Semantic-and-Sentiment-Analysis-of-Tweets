import re
import sys
import tweepy as tw
import csv

count = 0
max_count = 3000
all_tweets = []
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\Twitter\twitter_data_streamingApi.csv'


# FUNCTION TO REMOVE EMOJIS,URLS AND SPECIAL CHARACTERS FROM TEXT [1]
def clean_text(input_string):
    EMOJI_PATTERN = re.compile(
        '['
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
        ']+', flags=re.UNICODE
            )

    string = EMOJI_PATTERN.sub(r' ', input_string)
    string = re.sub(r"[^a-zA-Z0-9]+", ' ', input_string) # remove Urls from text [2]
    # remove special characters [3]
    string = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', input_string, flags=re.MULTILINE)
    return string


# STREAMLISTENER CLASS [6]
class StreamListener(tw.StreamListener):
    def on_status(self, status):
        global count
        global max_count

        # CHECK THE STATUS OF RETWEETED AND QUOTED TWEETS
        is_retweeted = hasattr(status, "retweeted_status")
        is_quoted = hasattr(status, "quoted_status")
        t = {}
        if is_retweeted is True:
            re_text = status.retweeted_status.text
            text = status.text

            # CLEAN TWEET TEXT USING CLEANING FUNCTION
            result = clean_text(text)
            retweeted_result = clean_text(re_text)

            t = {'ID': status.user.id, 'Text': result, 'UserName': status.user.screen_name,
                 'Retweet_text': retweeted_result,
                 'Retweet_username': status.retweeted_status.user.screen_name,
                 'Location': status.user.location, 'Time': status.created_at}
            all_tweets.append(t)

        elif is_quoted is True:
            quoted_text = ""
            # check if qutoted text is extended or not
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

            # REMOVE CHARACTERS
            r = [",", "\n"]
            for a in r:
                quoted_text.replace(a, " ")

            q_text = quoted_text
            text = status.text

            # CLEAN TWEET TEXT
            result = clean_text(text)
            quoted_result = clean_text(q_text)

            t = {'ID': status.user.id, 'Text': result, 'UserName': status.user.screen_name,
                 'Quoted_text': quoted_result, 'Quoted_username': status.quoted_status.user.screen_name,
                 'Location': status.user.location, 'Time': status.created_at}
            all_tweets.append(t)

        else:
            text = status.text

            # CLEAN TWEET TEXT
            result = clean_text(text)

            t = {'ID': status.user.id, 'Text': result, 'UserName': status.user.screen_name,
                 'Location': status.user.location, 'Time': status.created_at}
            all_tweets.append(t)

        # WRITE INTO FILE
        with open(file_path, 'a',
                  encoding='utf-8',
                  newline='') as tweet_data:
            writer = csv.DictWriter(tweet_data,
                                    fieldnames=["ID", "Text", "UserName", "Retweet_text", "Retweet_username",
                                                "Quoted_text",
                                                "Quoted_username", "Location", "Time"])
            if count == 0:
                writer.writeheader()
            count += 1
            if count > max_count:
                sys.exit()

            writer.writerow(t)

    # FUNCTION TO IDENTIFY ANY ERROR DURING EXTRACTION OF DATA [6]
    def on_error(self, status_code):
        print("Encountered streaming error(", status_code, ")")
        sys.exit()


# MAIN METHOD
if __name__ == "__main__":

    # API KEYS OF TWITTER APPLICATION
    consumer_key = "vpM3Pa0mfneYPerTYdGoXmiy6"
    consumer_secret = "10LbKBMaZwfpZCf4Ixvhk74c9wRcgQ7PSnmMug7skn3O7JiZl2"
    access_token = "1232330657872961536-0ZDd1oPvJMFqYSu7TbfepbseqcyrmI"
    access_token_secret = "duQF9ENYaJPdNWUFxgQjAcb1c3AF55L1Ydu7olzcUx5LB"

    # Authorization and initialize API endpoint
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    # LIST OF KEYWORDS TO SEARCH
    search_words = "Canada OR University OR Dalhousie University OR Halifax OR Canada Education"
    lang = ["en"]

    # INITIALIZE STREAM [6]
    streamListener = StreamListener()
    stream = tw.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')
    stream.filter(track=search_words, languages=lang)
