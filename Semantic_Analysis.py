import csv, math

Canada_doc = 0
University_doc = 0
Halifax_doc = 0
Business_doc = 0
DU_doc = 0
document_array_canada = []

# TOTAL NEWS ARTICLES TO PROCESS
total_doc = 100

# FILE PATHS OF OUTPUT FILES
output_file = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\News_Data\semantic_analysis1.csv'
output_file1 = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\News_Data\semantic_analysis2.csv'
file_path = r'F:\Dalhousie\winter semester\data m & w\assignments\Assignment 4\News_Data\NewArticles\ '


# SEARCH WORDS HALIFAX, CANADA, UNIVERSITY, DALHOUSIE UNIVERSITY AND BUSINESS AND GET COUNT OF WORDS
for i in range(100):
    Canada_count = 0
    University_count = 0
    Halifax_count = 0
    Business_count = 0
    DU_count = 0
    filename = file_path + "newsArticle_" + str(i) + ".txt"
    with open(filename, 'r', encoding='utf-8') as news_data:
        news = news_data.readline()
        news_words = news.split(" ")
        news_words = [x.lower() for x in news_words]
        for j in range(len(news_words)):
            if news_words[j] == 'canada':
                Canada_count = Canada_count + 1
            if news_words[j] == 'university':
                University_count = University_count + 1
            if news_words[j] == 'halifax':
                Halifax_count = Halifax_count + 1
            if news_words[j] == 'business':
                Business_count = Business_count + 1
            if j < len(news_words) and news_words[j] == 'dalhousie' and news_words[j + 1] == 'university':
                DU_count = DU_count + 1
        if Canada_count > 0:
            Canada_doc = Canada_doc + 1
            canada_details = str(len(news_words)) + "," + str(i) + "," + str(Canada_count)
            document_array_canada.append(canada_details)
        if University_count > 0:
            University_doc = University_doc + 1
        if Halifax_count > 0:
            Halifax_doc = Halifax_doc + 1
        if Business_count > 0:
            Business_doc = Business_doc + 1
        if DU_count > 0:
            DU_doc = DU_doc + 1

# CALCULATE OCCURRENCE OF EACH WORD DOCUMENT
canada_occurences = total_doc / Canada_doc
university_occurences = total_doc / University_doc
business_occurences = total_doc / Business_doc
if Halifax_doc == 0:
    halifax_occurences = 0
else:
    halifax_occurences = total_doc / Halifax_doc
if DU_doc == 0:
    DU_occurences = 0
else:
    DU_occurences = total_doc / DU_doc


# WRITE DATA OF PART 1 IN FILE
with open(output_file, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Total documents', total_doc])
    writer.writerow(
        ['Search Query', 'Document Containing Term(df)', 'Total documents(N)/number of  documents  term  appeared (df)',
         'Log10(N/df)'])
    ndf_canada = str(total_doc) + "/" + str(Canada_doc)
    ndf_university = str(total_doc) + "/" + str(University_doc)
    ndf_halifax = str(total_doc) + "/" + str(Halifax_doc)
    ndf_business = str(total_doc) + "/" + str(Business_doc)
    ndf_du = str(total_doc) + "/" + str(DU_doc)

    writer.writerow(['Canada', Canada_doc, ndf_canada, str(round(math.log10(canada_occurences), 2))])
    writer.writerow(['University', University_doc, ndf_university, str(round(math.log10(university_occurences), 2))])
    if halifax_occurences == 0:
        writer.writerow(['Halifax', Halifax_doc, ndf_halifax, '0'])
    else:
        writer.writerow(['Halifax', Halifax_doc, ndf_halifax, str(round(math.log10(halifax_occurences), 2))])
    writer.writerow(['Business', Business_doc, ndf_business, str(round(math.log10(business_occurences), 2))])

    if DU_occurences == 0:
        writer.writerow(['Dalhousie University', DU_doc, ndf_du, '0'])
    else:
        writer.writerow(['Dalhousie University', DU_doc, ndf_du, str(round(math.log10(DU_occurences), 2))])

maximum_frequency = 0
article_no = ''

# GET FREQUENCY OF CANADA TERM IN ALL DOCUMENTS AND PRINT THE DATA OF HIGHEST RELATIVE FREQUENCY ARTICLE
with open(output_file1, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Term', 'Canada'])
    writer.writerow(['Canada appeared in ' + str(Canada_doc) + ' documents', 'Total words(m)', 'Frequency(f)'])
    for i in range(Canada_doc):
        article_details = document_array_canada[i].split(",")
        writer.writerow(["Article_" + article_details[1], article_details[0], article_details[2]])

        relative_frequency = int(article_details[2]) / int(article_details[0])

        if relative_frequency > maximum_frequency:
            maximum_frequency = relative_frequency
            article_no = article_details[1]

            article_filename = file_path + "newsArticle_" + str(article_no) + ".txt"

            # PRINT THE CONTENT OF ARTICLE WITH MAX FREQUENCY
            with open(article_filename, 'r', encoding="utf-8") as articledata:
                article_content = articledata.readline()
                print("article_", article_no, " ", article_content)
                print("\n")