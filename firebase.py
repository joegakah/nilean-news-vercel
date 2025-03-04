import firebase_admin
import random

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('buai-92c2a-160af8a5b9d7.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

articles_ref = db.collection('articles')

def add_article(article: dict):
  doc_ref = articles_ref.document()
  doc_ref.set(article)

def check_article(article_url: str):
  articles = articles_ref.stream()
  for doc in articles:
    if doc.to_dict()['url'] == article_url:
      return True
  return False

def add_to_breaking_news():
  articles = articles_ref.stream()
  random_articles = random.sample(list(articles), 5)
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

add_to_breaking_news()