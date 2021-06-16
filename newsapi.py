import requests
import csv
import re

# FILE PATH AND LIST OF WORDS TO SEARCH
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\NewsApi\NewsApi_data.csv'
search_words = "Canada OR University OR Dalhousie University OR Halifax OR Canada Education OR Moncton OR Toronto"

# API KEY AND AUTHENTICATION
api_key = '7dac0178d3c148e4953c5df8fcc7f62d'
headers = {'Authorization': api_key}

# ENDPOINT URL AND PARAMETERS FOR EXTRACTING THE DATA [9]
everything_news_url = 'https://newsapi.org/v2/everything'
everything_payload = {'q': search_words, 'language': 'en', 'sortBy': 'popularity', 'pageSize': 100}
response = requests.get(url=everything_news_url, headers=headers, params=everything_payload).json()


# FUNCTION TO REMOVE EMOJIS,URLS AND SPECIAL CHARACTERS FROM TEXT [1]
def clean_text(input_string):
    emoji_pattern = re.compile(
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
    string = emoji_pattern.sub(r' ', input_string)
    string = re.sub(r"[^a-zA-Z0-9]+", ' ', input_string)  # remove Urls from text [2]
    # remove special characters [3]
    string = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', input_string, flags=re.MULTILINE)
    return string


with open(file_path, 'w', encoding='utf-8', newline='') as NewsApi_Data:
    writer = csv.DictWriter(NewsApi_Data, fieldnames=["Id", "Name", "Author", "Title", "Description",
                                                      "Url", "UrlToImage", "PublishedAt", "Content"])
    writer.writeheader()

    content = clean_text(response['articles'])

    for a in response['articles']:
        dd = {
                'Id': a['source']['id'],
                'Name': a['source']['name'],
                'Author': a['author'],
                'Title': a['title'],
                'Description': a['description'],
                'Url': a['url'],
                'UrlToImage': a['urlToImage'],
                'PublishedAt': a['publishedAt'],
                'Content': a['content']
            }
        writer.writerow(dd)














