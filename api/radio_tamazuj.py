import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from datetime import datetime, timedelta
from . import translate
from . import news_db

def get_article(article_url):
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.find('meta', property='og:title')['content']

        author_tag = soup.find('meta', attrs={'name': 'author'})
        author = author_tag['content'] if author_tag else None

        publishedAt_tag = soup.find('meta', property='article:published_time')
        publishedAt = publishedAt_tag['content'] if publishedAt_tag else None

        description_tag = soup.find('meta', property='og:description')
        description = description_tag['content'] if description_tag else None

        image_tag = soup.find('meta', property='og:image')
        image = image_tag['content'] if image_tag else None

        category = soup.find('a', rel='category tag').get_text(strip=True)

        print('Translating Article')
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
            'publishedAt': publishedAt
        }
        
        news_id = news_db.add_news(the_article)
        
        content = soup.find('div', class_='entry-content')
        converter = MarkdownConverter()
        content_md = converter.convert_soup(content)
        
        translated_content = translate.translate_to_ssl(content_md)
        
        the_article_content = {
            'news_id': news_id,
            'content_en': translated_content['en'],
            'content_nus': translated_content['nus'],
            'content_din': translated_content['din'],
            'publishedAt': publishedAt
        }

        news_db.add_news_content(the_article_content)
    
    else:
        return "Error: Unable to retrieve article data"

def get_articles():
    url = 'https://www.radiotamazuj.org/en/news'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='spotlight-post-1')
        
        print('Getting articles from Radio Tamazuj...')

        radio_tamazuj_articles = news_db.get_articles_per_source('radiotamazuj.org')
        existing_urls = {article.to_dict()['url'] for article in radio_tamazuj_articles}

        for article in articles:
            article_url = article.find('a', class_='em-figure-link')['href']

            print(f'Article:{article_link}...')
            
            try:
                if not existing_urls or article_url not in existing_urls:
                    get_article(article)
                    print(f"Added Article to Firestore")

                    existing_urls.add(article_url)

                else:
                    print(f"Article already exists in Firestore")

            except Exception as e:
                print(f"Error processing article: {article_url}. Error: {e}")
        
    else:
        return "Error: Unable to retrieve article links"