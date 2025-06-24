import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from . import news_db
from . import translate

def get_article(article_url):    
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('meta', property='og:title')['content']
        author_tag = soup.find('meta', attrs={'name': 'author'})
        author = author_tag['content'] if author_tag else None

        publishedAt_tag = soup.find('meta', property='article:published_time')
        publishedAt = publishedAt_tag['content'] if publishedAt_tag else None

        category_tag = soup.find('a', rel='category tag')
        category = category_tag.get_text(strip=True) if category_tag else None

        description_tag = soup.find('meta', property='og:description')
        description = description_tag['content'] if description_tag else None

        image_tag = soup.find('meta', property='og:image')
        image = image_tag['content'] if image_tag else None

        content = soup.find('div', class_='article-pic').contents
        content.remove(soup.find('div', class_='top-article-pic'))
        content.remove(soup.find('div', class_='social-share-3'))
        content.remove(soup.find('div', class_='previous-post'))
        
        content_soup = BeautifulSoup(''.join(str(item) for item in content), 'html.parser')

        converter = MarkdownConverter()
        content_md = converter.convert_soup(content_soup)

        print('Translating Article')
        translated_title = translate.translate_to_ssl(title)
        
        the_article = {
            'title_en': translated_title['en'],
            'title_nus': translated_title['nus'],
            'title_din': translated_title['din'],
            'author': author,
            'url': article_url,
            'imageUrl': image,
            'description': description,
            'publishedAt': publishedAt,
            'category': category,
            'source': 'eyeradio.org'
        }

        news_id = news_db.add_news(the_article)

        translated_content = translate.translate_to_ssl(content_md)

        the_article_content = {
            'news_id': news_id,
            'content_en': translated_content['en'],
            'content_nus': translated_content['nus'],
            'content_din': translated_content['din'],
            'publishedAt': publishedAt,
        }

        news_db.add_news_content(the_article_content)

        
        return {
            'title': title,
            'content': content_md,
            'date': str(publishedAt),
            'category': category,
            'author': author,
        }
    
    else:
        return "Error: Unable to retrieve article data"
                    
def get_articles(): 
    url = 'https://www.eyeradio.org/category/news/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='more-cat')
        
        print('Getting articles from Eye Radio...')

        eye_radio_articles = news_db.get_articles_per_source('eyeradio.org')
        existing_urls = {article.to_dict()['url'] for article in eye_radio_articles}
        
        for article in articles:
            article_url = article.find('div', class_='more-cat-title').find('a')['href']
            
            print(f'Article:{article_url}...')

            try:
                if not existing_urls or article_url not in existing_urls:
                    get_article(article_url)
                    print(f"Added Article to Firestore")

                    existing_urls.add(article_url)

                else:
                    print(f"Article already exists in Firestore")

            except Exception as e:
                print(f"Error processing article: {article_url}. Error: {e}")
        
    else:
        return "Error: Unable to retrieve article links"
