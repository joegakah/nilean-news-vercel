import random
import firebase_admin
from firebase_admin import credentials, firestore, messaging

cred = credentials.Certificate('buai-92c2a-160af8a5b9d7.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

news_ref = db.collection('news_titles')
news_content_ref = db.collection('news_content')

def add_news(news: dict):
  doc_ref = news_ref.document()
  doc_ref.set(news)
  print(doc_ref.id)
  return doc_ref.id

def add_news_content(content: dict):
  doc_ref = news_content_ref.document(content['news_id'])
  doc_ref.set(content)

def check_article(article_url: str):
  news = news_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(20)
  news = list(news.stream())

  for doc in news:
    if doc.to_dict()['url'] == article_url:
      return True
    
  return False

def delete_news(news_id: str):
  doc = news_ref.document(news_id)
  doc_content = news_content_ref.document(news_id)
  doc.delete()
  doc_content.delete()

def delete_all_news():
  news = news_ref.stream()
  for doc in news:
    doc.reference.delete()
  
  news_content = news_content_ref.stream()
  for doc in news_content:
    doc.reference.delete()

def add_articles_to_breaking_news():
    articles = news_ref.stream()
    random_articles = random.sample(list(articles), 5)
    for doc in random_articles:
        db.collection('breaking_news').document(doc.id).set(doc.to_dict())