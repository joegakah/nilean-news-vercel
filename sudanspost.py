import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from datetime import datetime, timedelta

import news_db
import translate

response = requests.get('https://www.sudanspost.com/category/news/')

def get_article(article_url: str, category:str):
  response = requests.get(article_url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='jeg_post_title').get_text(strip=True)
    description = soup.find('h2', class_='jeg_post_subtitle').get_text(strip=True)
    author = soup.find('div', class_='jeg_meta_author').find('a').get_text(strip=True)
    image = soup.find('img', class_='size-full').get_attribute_list('src')[0]

    date =  soup.find('div', class_='jeg_meta_date').get_text(strip=True)
    date_object = datetime.strptime(date, "%B %d, %Y")
    timestamp = date_object.strftime("%Y-%m-%d %H:%M:%S.%f")

    translated_title = translate.translate_to_ssl(title)

    the_article = {
      'title_en': translated_title['en'],
      'title_nus': translated_title['nus'],
      'title_din': translated_title['din'],
      'url': article_url,
      'imageUrl': image,
      'author': author,
      'category': category,
      'description': description,
      'source': 'sudanspost.com',
      'publishedAt': timestamp
    }
    
    news_id = news_db.add_news(the_article)

    content = soup.find('div', class_='content-inner').contents
    content.remove(soup.find('div', class_='sharedaddy'))

    content_soup = BeautifulSoup(''.join(str(item) for item in content[2:]), 'html.parser')
  
    converter = MarkdownConverter()
    content_md = converter.convert_soup(content_soup)

    translated_content = translate.translate_to_ssl(content_md)

    the_article_content = {
      'news_id': news_id,
      'content_en': translated_content['en'],        
      'content_nus': translated_content['nus'],
      'content_din': translated_content['din'],
      'publishedAt': timestamp
    }

    news_db.add_news_content(the_article_content)

    print(f"Added to Firestore")

def get_articles():
  if(response.status_code == 200):
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='jeg_post')

    print('Getting articles from Sudan Post...')

    for article in articles:
      article_link = article.find('h3', class_='jeg_post_title').find('a')['href']

      print(f'Article:{article_link}...')

      try:
        if not news_db.check_article(article_link):
          category = soup.find('div', class_='jeg_post_category').get_text(strip=True)
          get_article(article_link, category)

        else:
          print(f"Article already exists in Firestore")

      except Exception as e:
        print(f"Error processing article: {article_link}. Error: {e}")
  
    else:
      return "Error: Unable to retrieve article links"
