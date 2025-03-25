import firebase
import radio_tamazuj
import eye_radio
import threading
import schedule
import time
from fastapi import FastAPI, HTTPException

app = FastAPI()

def scrape_website():
  articles =  radio_tamazuj.get_articles() + eye_radio.get_articles()

  for article in articles:
    if not firebase.check_article(article['url']):
      firebase.add_article(article)
      print(f"Added {article['title']['en'] + ' - ' + article['source']} to Firestore")
    else:
      print(f"{article['title']['en'] + ' - ' + article['source']} already exists in Firestore")
   
def schedule_scraping():
  schedule.every(10).seconds.do(scrape_website)
  print("Scheduled scraping every 10 seconds")
  while True:
      schedule.run_pending()
      time.sleep(1)

threading.Thread(target=schedule_scraping, daemon=True).start()

@app.get("/")
def home():
  return {"message": "Welcome to the Web Scraping API"}

@app.get("/scrape")
def scrape():
  try:
      scrape_website()
      return {"message": "Scraping completed successfully"}
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

