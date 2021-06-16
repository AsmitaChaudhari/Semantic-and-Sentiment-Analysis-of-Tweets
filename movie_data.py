import csv

# fetch movie title, movie rating, genre and plot from file and store in new separate Movie_data.csv file

input_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\OMDB_API\OmdbApi_data.csv'
output_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 3\OMDB_API\Movie_data.csv'

with open(input_file, 'r') as fileOpen:
    with open(output_file,'w', newline='')as file:
        readCsv = csv.reader(fileOpen)
        writeCsv = csv.writer(file)
        for row in readCsv:
            writeCsv.writerow([row[0], row[2], row[4], row[8], row[12]])
