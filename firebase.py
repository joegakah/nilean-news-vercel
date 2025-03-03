import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('buai-92c2a-160af8a5b9d7.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection('users')
docs = users_ref.stream()

for doc in docs:
  print(f'{doc.id} => {doc.to_dict()}')
