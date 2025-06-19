import radio_tamazuj
import eye_radio
import threading
from fastapi import FastAPI, HTTPException

import sudanspost

app = FastAPI()

def scrape_website():
  threads = []
  threads.append(threading.Thread(target=sudanspost.get_articles))
  threads.append(threading.Thread(target=eye_radio.get_articles))
  threads.append(threading.Thread(target=radio_tamazuj.get_articles))

  for thread in threads:
      thread.start()

  for thread in threads:
      thread.join()
   

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

