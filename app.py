import firebase
import radio_tamazuj
import eye_radio

def app():
  articles =  radio_tamazuj.get_articles() + eye_radio.get_articles()

  for article in articles:
    if not firebase.check_article(article['url']):
      firebase.add_article(article)
      print(f"Added {article['title'] + ' - ' + article['source']} to Firestore")
    else:
      print(f"{article['title'] + ' - ' + article['source']} already exists in Firestore")

app()