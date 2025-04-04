import firebase
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
import translate
from datetime import datetime, timedelta

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

        for article in articles:
            article_url = article.find('div', class_='more-cat-title').find('a')['href']
            
            try:
                print(f'Getting article:{article_url}...')

                if not firebase.check_article(article_url):
                    title = article.find('h3', class_='article-title-2').get_text(strip=True)
                    image = article.find('img', class_='wp-post-image')['src']
                    date = article.find('span', class_='posts-date').get_text(strip=True)
                    date_object = datetime.strptime(date, "%B %d, %Y")
                    timestamp = date_object.strftime("%Y-%m-%d %H:%M:%S.%f")

                    article_data = get_article_data(article_url)
                    translated_title = translate.translate_to_ssl(title)
        
                    the_article = {
                        'title': translated_title,
                        'author': 'chief editor',
                        'url': article_url,
                        'imageUrl': image,
                        'description': '',
                        'content': article_data['content'],
                        'publishedAt': timestamp,
                        'category': article_data['category'],
                        'source': 'radiotamazuj.org'
                    }

                    firebase.add_article(the_article)
                    print(f"Added {article['title']['en'] + ' - ' + article['source']} to Firestore")
                else:
                    print(f"{article['title']['en'] + ' - ' + article['source']} already exists in Firestore")
            except:
                print(f"Error getting article data from {article_url}")

            
            all_articles.append(the_article)

        return all_articles
        
    else:
        return "Error: Unable to retrieve article links"
    