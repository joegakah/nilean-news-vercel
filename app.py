import firebase
import radio_tamazuj
import eye_radio
import threading
import schedule
import time
from fastapi import FastAPI, HTTPException

app = FastAPI()

def scrape_website():
  radio_tamazuj.get_articles()
  eye_radio.get_articles()
   
def schedule_scraping():
  schedule.every(30).minutes.do(scrape_website)
  print("Scheduled scraping every 10 minutes")
  while True:
      schedule.run_pending()
      scrape_website()
      time.sleep(1)

threading.Thread(target=schedule_scraping, daemon=True).start()

@app.get("/")
def home():
  scrape_website()
  return {"message": "Welcome to the Web Scraping API"}

@app.get("/scrape")
def scrape():
  try:
      scrape_website()
      return {"message": "Scraping completed successfully"}
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

