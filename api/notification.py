import requests
import random
from . import news_db
import json

def send_notification(title, body, image_url):
  try:
    print('Sending Notification')

    url = "https://api.neurollect.africa/api/send-notification"

    payload = json.dumps({
      "topic": "news_titles",
      "title": title,
      "body": body,
      "image": image_url
    })
    
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response

  except Exception as e:
    print(e)

def send_today_news():
  try:
    todays_news = news_db.get_todays_news()
    
    news = random.choice(todays_news)

    print(news.id)

    news = news.to_dict()
    title = news['title_en']
    body = news['description']
    image_url = news['imageUrl']

    send_notification(title, body, image_url)

  except Exception as e:
    print(e)
    raise Exception(status_code=500, detail=str(e))
  