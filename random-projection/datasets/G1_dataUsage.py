import json

with open("4000_g1_articles.json") as data_file:
    articles = json.load(data_file, encoding='utf-8')
    for article in articles:
        print article["URL"]
        #print article["TEXT"]
    print len(articles)
