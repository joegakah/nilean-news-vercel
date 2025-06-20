import threading
from http.client import HTTPException
from flask import Flask
from . import notification
from . import radio_tamazuj
from . import eye_radio
from . import sudanspost

app = Flask(__name__)

def scrape_website():
  threads = []
  threads.append(threading.Thread(target=sudanspost.get_articles))
  threads.append(threading.Thread(target=eye_radio.get_articles))
  threads.append(threading.Thread(target=radio_tamazuj.get_articles))

  for thread in threads:
      thread.start()

  for thread in threads:
      thread.join()
   
@app.route("/")
def home():
  return {"message": "Welcome to the Web Scraping API"}

@app.route("/scrape")
def scrape():
  try:
    threading.Thread(target=scrape_website).start()
    return {"message": "Scraping completed successfully"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@app.get("/notify-today-news")
def notify_today_news():
  try:
    notification.send_today_news()
    return {"message": "Notification sent successfully"}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
