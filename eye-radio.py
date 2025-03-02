import json
import requests
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

url = 'https://www.eyeradio.org/category/news/'

def get_article_data(article_url):
    
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1', class_='title-it').get_text(strip=True)
        date = soup.find('span', class_='posts-date').get_text(strip=True)
        category = soup.find('a', rel='category tag').get_text(strip=True)
        content = soup.find('div', class_='entry-content')
        converter = MarkdownConverter()
        content_md = converter.convert_soup(content)
        
        return {
            'title': title,
            'content': content_md,
            'date': date,
            'category': category
        }
    
    else:
        return "Error: Unable to retrieve article data"

def get_articles(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='more-cat')
        
        for article in articles:
            article_url = article.find('div', class_='more-cat-title').find('a')['href']
            title = article.find('h1', class_='cat-title-4').get_text(strip=True)
            image = article.find('div', class_='more-cat-pic').find('img').get_attribute_list('src')[0]
            description = article.find('p', class_='more-cat-copy').get_text(strip=True)

            the_article = {
                'title': title,
                'author': '',
                'url': article_url,
                'imageUrl': image,
                'description': description,
                'content': '',
                'publishedAt': '',
                'category': '',
                'source': 'eyeradio.org'
            }

            print(the_article)
        
    else:
        return "Error: Unable to retrieve article links"
    
get_articles(url)