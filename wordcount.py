import csv

# read Twitter Data from twitter_csv_file and write into tweet_text_file
# read News Data from news_csv_file and write into news_text_file

twitter_csv_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\Twitter\twitter_data.csv'
tweet_text_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\spark_wordcount\tweet_count.txt'
news_csv_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\NewsApi\NewsApi_data.csv'
news_text_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\spark_wordcount\news_count.txt'

# GET TWEET TEXT FROM TWITTER DATA AND SAVE INTO .TXT FILE [8]
with open(tweet_text_file, "w", encoding="utf8") as my_output_file:
    with open(twitter_csv_file, "r", encoding="utf8") as my_input_file:
        # write in file with lowercase
        [my_output_file.write("".join(row[1]).lower() + '\n') for row in csv.reader(my_input_file)]
    my_output_file.close()

# GET NEWS CONTENT FROM TWITTER DATA AND SAVE INTO .TXT FILE [8]
with open(news_text_file, "w", encoding="utf8") as my_output_file:
    with open(news_csv_file, "r", encoding="utf8") as my_input_file:
        # write in file with lowercase
        [my_output_file.write("".join(row[8]).lower() + '\n') for row in csv.reader(my_input_file)]
    my_output_file.close()
