import csv
import re

# fetch twitter text from Assignment3 twitter data file and store in new separate twitter_text.csv file

input_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\Twitter\twitter_data.csv'
output_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\Twitter_text\twitter_text1.csv'


with open(input_file, 'r', encoding='utf-8') as fileOpen:
    with open(output_file, 'w', newline='', encoding='utf-8')as file:
        readCsv = csv.DictReader(fileOpen)
        writeCsv = csv.DictWriter(file, fieldnames=["Id", "Text"])
        Id = 0
        writeCsv.writeheader()
        for row in readCsv:
            # REMOVE 'RT' FROM TWEETS
            text = re.sub('RT', '', row["Text"])
            Id = Id + 1
            t = {'Id': Id, 'Text': text}
            writeCsv.writerow(t)

