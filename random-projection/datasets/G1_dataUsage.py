'''
  author: Daniel Menezes
  modified: Guilherme Varela
  
  motivation: iterates "4000_g1_articles.json", printing only the articles that conform to the pattern
'''
import json
import re 


corpora=[]


def print_corpus_stats():
  with open("4000_g1_articles.json") as data_file:
    articles= json.load(data_file, encoding='utf-8')  

  n_articles= len(articles)
  vocabulary=set([])
  approx_word_count=0 # doesnt take into account hyperlinks
  for a, article in enumerate(articles):        
    print('processing %d of %d\tarticle_url: ' % (a, n_articles), article["URL"])
    sentences= article['TEXT'].split('. ')
    words=[] 
    for sentence in sentences:
      sentence_words= sentence.split(' ')
      words+= sentence_words
      approx_word_count+= len(sentence_words)

    vocabulary= vocabulary.union(set(words))


  print('#articles: ', n_articles)
  print('#approx vocabulary: ', len(vocabulary))
  print('#approx word_count: ', approx_word_count)

def print_article(pattern= 'acre-decreta-expediente-corrido-nas-vesperas-de-natal-e-reveillon'):
  prog = re.compile(pattern)
  with open("4000_g1_articles.json") as data_file:
    articles= json.load(data_file, encoding='utf-8')  
    
  for article in articles:        
    if prog.search(article['URL']):    
      print(article['TEXT'])

      sentences= article['TEXT'].split('. ')
      words=[] 
      approx_word_count=0
      vocabulary=set([])
      for sentence in sentences:
        sentence_words= sentence.split(' ')
        words+= sentence_words
        approx_word_count+= len(sentence_words)

        vocabulary= vocabulary.union(set(words))    
  print('#article: ', pattern)
  print('#approx vocabulary: ', len(vocabulary))
  print('#approx word_count: ', approx_word_count)
# pattern= 'acre-decreta-expediente-corrido-nas-vesperas-de-natal-e-reveillon'
# prog = re.compile(pattern)

# with open("4000_g1_articles.json") as data_file:
#   articles = json.load(data_file, encoding='utf-8')  
#   for article in articles:        
#     if prog.search(article["URL"]):    
    
# 		print article["URL"]
# 		news= article["URL"].split('/')[-1]
# 		news= news.split('.html')[0]
# 		corpora.append(news)
#     # print news 
#     #print article["TEXT"]
#   print 'articles', len(articles)
#   print 'unique news', len(set(corpora))

def main():
  # print_corpus_stats()
  pattern='darcy-e-nogueira-cumprem-agenda-em-ribeirao-preto-neste-domingo'
  print_article(pattern=pattern)

if __name__ == '__main__':
  main()