import json
corpora=[]
with open("4000_g1_articles.json") as data_file:
    articles = json.load(data_file, encoding='utf-8')
    for article in articles:        
				print article["URL"]
				news= article["URL"].split('/')[-1]
				news= news.split('.html')[0]
				corpora.append(news)
        # print news 
        #print article["TEXT"]
    print 'articles', len(articles)
    print 'unique news', len(set(corpora))
