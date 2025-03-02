import json
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

url = 'https://www.eyeradio.org/category/news/'

def extract_info(text):
    pattern = r"Author: (.*) \|  Published: (.*)"
    match = re.match(pattern, text)
    
    if match:
        author = match.group(1).strip()
        publishedAt = match.group(2).strip()
        return author, publishedAt
    else:
        return None, None


def convert_to_timestamp(published):
    now = datetime.now()
    if "hours" in published:
        hours = int(published.split(" hours")[0])
        timestamp = now - timedelta(hours=hours)

    elif "minutes" in published:
        minutes = int(published.split(" minutes")[0])
        timestamp = now - timedelta(minutes=minutes)

    elif "days" in published:
        days = int(published.split(" days")[0])
        timestamp = now - timedelta(days=days)

    else:
        date_object = datetime.strptime(published, "%B %d, %Y")
        timestamp = date_object.timestamp()
   
    return timestamp


def get_article_data(article_url):    
    response = requests.get(article_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('h1', class_='article-title').get_text(strip=True)
        author_date = soup.find('p', class_='made').get_text(strip=True)
        author, publishedAt = extract_info(author_date)
        date = convert_to_timestamp(publishedAt) if publishedAt else ''
        category = soup.find('a', rel='category tag').get_text(strip=True)

        content = soup.find('div', class_='article-pic').contents
        content.remove(soup.find('div', class_='top-article-pic'))
        content.remove(soup.find('p', class_='caption'))
        content.remove(soup.find('div', class_='social-share-3'))
        content.remove(soup.find('div', class_='previous-post'))
        
        content_soup = BeautifulSoup(''.join(str(item) for item in content), 'html.parser')

        converter = MarkdownConverter()
        content_md = converter.convert_soup(content_soup)
        
        return {
            'title': title,
            'content': content_md,
            'date': str(date),
            'category': category,
            'author': author,
        }
    
    else:
        return "Error: Unable to retrieve article data"

def get_articles(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='more-cat')
        
        all_articles = []
        
        for article in articles:
            article_url = article.find('div', class_='more-cat-title').find('a')['href']
            title = article.find('h1', class_='cat-title-4').get_text(strip=True)
            image = article.find('div', class_='more-cat-pic').find('img').get_attribute_list('src')[0]
            description = article.find('p', class_='more-cat-copy').get_text(strip=True)

            article_data = get_article_data(article_url)

            the_article = {
                'title': title,
                'author': article_data['author'],
                'url': article_url,
                'imageUrl': image,
                'description': description,
                'content': article_data['content'],
                'publishedAt': article_data['date'],
                'category': article_data['category'],
                'source': 'eyeradio.org'
            }
            
            all_articles.append(the_article)

        with open('eyeradio_articles.json', 'w') as f:
            json.dump(all_articles, f, indent=4)
        
    else:
        return "Error: Unable to retrieve article links"
    
get_articles(url)