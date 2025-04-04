import firebase
import re
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

import translate

def extract_info(text):
    pattern = r"Author: (.*) \|  Published: (.*)"
    match = re.match(pattern, text)
    
    if match:
        author = match.group(1).strip()
        publishedAt = match.group(2).strip()
        return author, publishedAt
    else:
        return None, None

def convert_to_timestamp(publishedAt):
    now = datetime.now()
    if "hour" in publishedAt:
        hours = int(publishedAt.split(" hour")[0])
        timestamp = now - timedelta(hours=hours)

    elif "min" in publishedAt:
        minutes = int(publishedAt.split(" min")[0])
        timestamp = now - timedelta(minutes=minutes)

    elif "day" in publishedAt:
        days = int(publishedAt.split(" day")[0])
        timestamp = now - timedelta(days=days)

    else:
        date_object = datetime.strptime(publishedAt, "%B %d, %Y")
        timestamp = date_object.strftime("%Y-%m-%d %H:%M:%S.%f")

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
        content.remove(soup.find('div', class_='social-share-3'))
        content.remove(soup.find('div', class_='previous-post'))
        
        content_soup = BeautifulSoup(''.join(str(item) for item in content), 'html.parser')

        converter = MarkdownConverter()
        content_md = converter.convert_soup(content_soup)

        translated_content = translate.translate_to_ssl(content_md)
        
        return {
            'title': title,
            'content': translated_content,
            'date': str(date),
            'category': category,
            'author': author,
        }
    
    else:
        return "Error: Unable to retrieve article data"
    
def get_article(article):
    article_url = article.find('div', class_='more-cat-title').find('a')['href']
    title = article.find('h1', class_='cat-title-4').get_text(strip=True)
    image = article.find('div', class_='more-cat-pic').find('img').get_attribute_list('src')[0]
    description = article.find('p', class_='more-cat-copy').get_text(strip=True)

    print(f'Getting article:{title} data from {article_url}...')

    translated_title = translate.translate_to_ssl(title)
    
    article_data = get_article_data(article_url)

    return {
        'title': translated_title,
        'author': article_data['author'],
        'url': article_url,
        'imageUrl': image,
        'description': description,
        'content': article_data['content'],
        'publishedAt': article_data['date'],
        'category': article_data['category'],
        'source': 'eyeradio.org'
    }

def get_articles(): 
    url = 'https://www.eyeradio.org/category/news/'
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='more-cat')
        
        all_articles = []
        print('Getting articles from Eye Radio...')
        
        for article in articles:
            try:
                article_url = article.find('div', class_='more-cat-title').find('a')['href']
                if not firebase.check_article(article_url):
                    the_article = get_article(article)
                    firebase.add_article(the_article)
                    print(f"Added {article['title']['en'] + ' - ' + article['source']} to Firestore")
                else:
                    print(f"{article['title']['en'] + ' - ' + article['source']} already exists in Firestore")
            except:
                print('Error')
            all_articles.append(the_article)
        
    else:
        return "Error: Unable to retrieve article links"


def addlatestArtcle():
    url = 'https://www.eyeradio.org/category/news/'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        print('Getting latest article from Eye Radio...')
        
        articles = soup.find_all('div', class_='more-cat')
        article = get_article(articles[0])

        if not firebase.check_article(article['url']):
            print(f"Adding {article['title']['en'] + ' - ' + article['source']} to Firestore")
            firebase.add_article(article)