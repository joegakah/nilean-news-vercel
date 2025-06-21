import firebase_admin
from firebase_admin import credentials, firestore
import random
import json
import os
from dotenv import load_dotenv

load_dotenv()

json_str = os.getenv("FIREBASE_SERVER_KEY")

if not json_str:
  raise ValueError("Environment variable FIRBASE_SERVER_KEY not found.")

credentials_dict = json.loads(json_str)
credentials_dict["private_key"] = credentials_dict["private_key"].replace("\\n", "\n")
cred = credentials.Certificate(credentials_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()

articles_ref = db.collection('news_titles')
news_ref = db.collection('news')
news_content_ref = db.collection("news_content")

def list_articles():
  articles = articles_ref.stream()
  articles = list(articles)

def add_article(article: dict):
  doc_ref = articles_ref.document()
  doc_ref.set(article)

def add_news(news: dict):
  doc_ref = news_ref.document()
  doc_ref.set(news)
  print(doc_ref.id)
  return doc_ref.id

def check_article(article_url: str):
  print("Checking News Article ...")
  news = news_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(25)
  news = list(news.stream())

  for doc in news:
    if doc.to_dict()['url'] == article_url:
      print(f'News Article Already Exists')
      return True
    
  print("Article Not Found")
  return False

def add_to_breaking_news():
  articles = articles_ref.stream()
  random_articles = random.sample(list(articles), 5)
  breaking_news = db.collection('breaking_news')
  breaking_news.delete()
  
  for doc in random_articles:
    db.collection('breaking_news').document(doc.id).set(doc.to_dict())

def delete_articles():
  articles = articles_ref.stream()
  for doc in articles:
    doc.reference.delete()

def delete_breaking_news():
  breaking_news = db.collection('breaking_news').stream()
  for doc in breaking_news:
    doc.reference.delete()

def delete_article(article_id: str):
  doc_ref = articles_ref.document(article_id)
  doc_ref.delete()

  doc_ref = news_content_ref.document(article_id)
  doc_ref.delete()

def delete_duplicates():
  print("Deleting duplicate articles from Firestore...")

  articles = articles_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(30)
  articles = list(articles.stream())

  unique_urls = set()
    
  for article in articles:
    url = article.to_dict()['url']
    print(f'Article: {url}...')
    
    if url in unique_urls:
      delete_article(article.id)
      print(f'Deleted Duplicate article: {url}')
    else:
      unique_urls.add(url)


def delete_duplicate_news_content():
  print("Deleting duplicate articles from Firestore...")

  articles = db.collection('news_content').order_by('publishedAt', direction=firestore.Query.DESCENDING)
  articles = list(articles.stream())

  unique_id = set()
    
  for article in articles:
    news = article.to_dict()['content_en'][0:30]
    print(f'Article: {article.id}')
    
    if news in unique_id:
      doc_ref = news_content_ref.document(article.id)
      doc_ref.delete()
      print(f'Deleted Duplicate article: {article.id}')
    else:
      unique_id.add(news)


def get_last_article_id():
    articles_ref = db.collection('articles')
    query = articles_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(1)
    results = query.get()
    if results:
        return results[0].to_dict()
    else:
        return None
    