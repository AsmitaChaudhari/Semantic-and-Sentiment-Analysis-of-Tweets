import csv
import re
import heapq
import nltk

# FILE PATH OF INPUT FILE AND OUTPUT FILES
input_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\twitter_text1.csv'
output_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\Tweet_Polarity.csv'
Word_occurance = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\word_occurance.csv'

# PATH FOR POSITIVE AND NEGATIVE WORDS FILE
Positive_words = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\positive-words.txt'
Negative_words = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\negative-words.txt'


# FUNCTION TO CALCULATING WORD OCCURRENCES
def count_word(tokens, d=None):
    if d is None:
        d = {}
    for t in tokens:
        if t not in d.keys():
            d[t] = 1
        else:
            d[t] = d[t] + 1
    return d


count_positive = {}
count_negative = {}


# FUNCTION TO FIND POLARITY OF TWEET
def tweet_polarity(polarity):
    p_count = 0
    n_count = 0
    count = 0
    match_word_positive = []
    match_word_negative = []

    for b in polarity:
        if b in positive_words:
            p_count = +1
            match_word_positive.append(b)
        elif b in negative_words:
            n_count = +1
            match_word_negative.append(b)
        else:
            count = +1

    count_word(match_word_positive, count_positive)
    count_word(match_word_negative, count_negative)
    if p_count >= n_count:
        if p_count >= count:
            p = {'Match': match_word_positive, 'Polarity': "Positive"}
        else:
            p = {'Match': "N/A", 'Polarity': "Neutral"}
    else:
        if n_count >= count:
            p = {'Match': match_word_negative, 'Polarity': "Negative"}
        else:
            p = {'Match': "N/A", 'Polarity': "Neutral"}
    return p


positive_words = []
negative_words = []

# CREATE LIST OF POSITIVE AND NEGATIVE WORDS FROM FILE
with open(Positive_words, 'r') as fileOpen:
    readCsv = csv.reader(fileOpen)
    for i in readCsv:
        positive_words.append(i[0])

with open(Negative_words, 'r') as fileOpen:
    readCsv = csv.reader(fileOpen)
    for i in readCsv:
        negative_words.append(i[0])

tweet_list = []

with open(input_file, 'r', encoding='utf-8') as fileOpen:
    with open(output_file, 'w', newline='', encoding='utf-8')as file:
        readCsv = csv.reader(fileOpen)
        writeCsv = csv.DictWriter(file, fieldnames=["Id", "Tweet", "Match", "Polarity"])
        writeCsv.writeheader()
        for i in readCsv:
            tweet_list.append(i[1])

        # TOKENIZE THE WORDS IN TWEET
        corpus = nltk.sent_tokenize(str(tweet_list))

        # CLEAN THE TWEET
        for row in range(len(corpus)):
            corpus[row] = corpus[row].lower()
            corpus[row] = re.sub(r'\W', ' ', corpus[row])
            corpus[row] = re.sub(r'\s+', ' ', corpus[row])

        a = {}

        count_positive = {}
        # WRITE DATA TO FILE WITH TWEET, MATCH WORDS AND ITS POLARITY
        for sentence in range(len(corpus)):
            tokens = nltk.word_tokenize(corpus[sentence])
            d = count_word(tokens)
            polarity = tweet_polarity(d)

            a = {'Id': sentence, 'Tweet': corpus[sentence], 'Match': polarity['Match'],
                 'Polarity': polarity['Polarity']}
            writeCsv.writerow(a)

# WRITE DATA OF MATCH WORDS, ITS COUNT AND POLARITY IN NEW FILE FOR VISUALIZATION
with open(Word_occurance, 'w', newline='', encoding='utf-8')as file:
    writefile = csv.writer(file)
    writefile.writerow(['Words', 'Count', 'Polarity'])
    for keys in count_positive.keys():
        writefile.writerow([keys, count_positive[keys], 'Positive'])
    for keys in count_negative.keys():
        writefile.writerow([keys, count_negative[keys], 'Negative'])