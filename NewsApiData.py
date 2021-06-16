import csv
import re
import requests

# fetch News Api data from Assignment3 NewsApi data file and store in new separate newsArticle_ .txt files

# FILE PATH AND LIST OF WORDS TO SEARCH
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\News_Data\NewArticles\ '
search_words = "Canada OR University OR Dalhousie University OR Halifax OR Canada Education OR Moncton OR Toronto"

# API KEY AND AUTHENTICATION
api_key = '7dac0178d3c148e4953c5df8fcc7f62d'
headers = {'Authorization': api_key}

# ENDPOINT URL AND PARAMETERS FOR EXTRACTING THE DATA [9]
everything_news_url = 'https://newsapi.org/v2/everything'
everything_payload = {'q': search_words, 'language': 'en', 'sortBy': 'popularity', 'pageSize': 100}
response = requests.get(url=everything_news_url, headers=headers, params=everything_payload).json()


newsNumber = 0
for i in response['articles']:
    name = file_path + "newsArticle_" + str(newsNumber) + ".txt"
    with open(name, 'w+', encoding='utf-8') as file:
        j = i['content']
        # CLEANING THE NEWS ARTICLES
        j = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', str(j))
        j = j.strip()
        newsarticledata = "Title : " + str(i['title']) + " Content : " + j + " Description : " + str(i['description'])
        file.write(newsarticledata)
    newsNumber = newsNumber + 1




