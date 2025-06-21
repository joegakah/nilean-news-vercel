import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from datetime import datetime, timedelta
from . import translate
from . import news_db


def get_article_data(article_url):
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1', class_='entry-title').get_text(strip=True)
        date = soup.find('span', class_='posts-date').get_text(strip=True)
        category = soup.find('a', rel='category tag').get_text(strip=True)
        content = soup.find('div', class_='entry-content')
        converter = MarkdownConverter()
        content_md = converter.convert_soup(content)
        
        translated_content = translate.translate_to_ssl(content_md)
        
        return {
            'title': title,
            'content': translated_content,
            'date': date,
            'category': category
        }
    
    else:
        return "Error: Unable to retrieve article data"

def get_articles():
    url = 'https://www.radiotamazuj.org/en/news'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='spotlight-post-1')
        
        all_articles = []
        print('Getting articles from Radio Tamazuj...')

        radio_tamazuj_articles = news_db.get_articles_per_source('radiotamazuj.org')
        existing_urls = {article.to_dict()['url'] for article in radio_tamazuj_articles}

        for article in articles:
            article_url = article.find('a', class_='em-figure-link')['href']

            try:
                print(f'Article:{article_url}...')

                if not existing_urls or article_url not in existing_urls:
                    title = article.find('h3', class_='article-title-2').get_text(strip=True)
                    image = article.find('img', class_='wp-post-image')['src']
                    date = article.find('span', class_='posts-date').get_text(strip=True)
                    date_object = datetime.strptime(date, "%B %d, %Y")
                    timestamp = date_object.strftime("%Y-%m-%d %H:%M:%S.%f")

                    article_data = get_article_data(article_url)

                    translated_title = translate.translate_to_ssl(title)
        
                    the_article = {
                        'title_en': translated_title['en'],
                        'title_nus': translated_title['nus'],
                        'title_din': translated_title['din'],
                        'author': 'chief editor',
                        'url': article_url,
                        'imageUrl': image,
                        'description': '',
                        'publishedAt': timestamp,
                        'category': article_data['category'],
                        'source': 'radiotamazuj.org'
                    }

                    news_id = news_db.add_news(the_article)

                    the_article_content = {
                        'news_id': news_id,
                        'content_en': article_data['content']['en'],
                        'content_nus': article_data['content']['nus'],
                        'content_din': article_data['content']['din'],
                        'publishedAt': timestamp
                    }

                    news_db.add_news_content(the_article_content)

                    print(f"Added to Firestore")
                    
                else:
                    print(f"Article already exists in Firestore")

            except Exception as e:
                print(e)
                print(f"Error processing article {article_url}: {e}")


        return all_articles
        
    else:
        return "Error: Unable to retrieve article links"
    