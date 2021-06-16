import requests
import csv
import re


# API KEY OF THE OMDB MOVIE DATABASE [4]
api = 'http://www.omdbapi.com/?i=tt3896198&apikey=a7e42c3'
api_key = 'a7e42c3'


# LIST OF KEYWORDS AND FILE PATH
search_words = ["Canada", "University", "Halifax", "Moncton", "Toronto", "Vancouver", "Alberta", "Niagara"]
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\OMDB_API\OmdbApi_data.csv'
t = {}
a = []


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


# SEARCH WORDS IN DATABASE AND STORE JASON RESPONSE
for i in search_words:
    url = " http://www.omdbapi.com/?t=" + i + "+&apikey=a7e42c3&"
    response = requests.get(url)   # [5]
    data = response.json()

    # STORE ALL FIELDS
    t = {'Title': data['Title'], 'Year': data['Year'], 'Rated': data['Rated'], 'Released': data['Released'],
         'Genre': data['Genre'], 'Director': data['Director'], 'Writer': data['Writer'], 'Actors': data['Actors'],
         'Plot': data['Plot'], 'Language': data['Language'], 'Country': data['Country'], 'Awards': data['Awards'],
         'imdbRating': data['imdbRating'], 'imdbVotes': data['imdbVotes'], 'imdbID': data['imdbID'],
         'Type': data['Type'],
         }
    a.append(t)

    # WRITE FETCHED DATA INTO FILE
    with open(file_path, 'w', encoding='utf-8', newline='') as omdb_data:
        writer = csv.DictWriter(omdb_data,
                                fieldnames=["Title", "Year", "Rated", "Released", "Genre", "Director", "Writer",
                                            "Actors", "Plot", "Language", "Country", "Awards", "imdbRating",
                                            "imdbVotes", "imdbID", "Type"])
        writer.writeheader()
        writer.writerows(a)
