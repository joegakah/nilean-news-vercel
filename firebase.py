import firebase_admin
import random

from firebase_admin import credentials, firestore, messaging

cred = credentials.Certificate('buai-92c2a-160af8a5b9d7.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

articles_ref = db.collection('articles')

def list_articles():
  articles = articles_ref.stream()
  articles = list(articles)

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

def delete_article(article_id: str):
  doc_ref = articles_ref.document(article_id)
  doc_ref.delete()

def delete_duplicates():
  print("Deleting duplicate articles from Firestore...")

  articles = articles_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(25)
  articles = list(articles.stream())

  unique_urls = set()
    
  for article in articles:
    url = article.to_dict()['url']
    
    if url in unique_urls:
      delete_article(article.id)
      print(f'Deleted Duplicate article: {url}')
    else:
      unique_urls.add(url)


def get_last_article_id():
    articles_ref = db.collection('articles')
    query = articles_ref.order_by('publishedAt', direction=firestore.Query.DESCENDING).limit(1)
    results = query.get()
    if results:
        return results[0].to_dict()
    else:
        return None

def send_notification():
    article_data = get_last_article_id()

    print(article_data['title']['en'])

    notification = messaging.Notification(
      title=article_data['title']['en'],
      body=article_data['description'],
    )
    data = {
      'articleId': article_data['imageUrl'],
      'url': article_data['url'],
    }
    message = messaging.Message(
        notification=notification,
        data=data,
        topic='new-articles',
    )
    try:
        response = messaging.send(message)
        print('Notification sent successfully:', response)
    except Exception as e:
        print('Error sending notification:', e)
