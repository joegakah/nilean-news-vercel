import firebase_admin

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
    if doc.to_dict()['article_url'] == article_url:
      return True
  return False