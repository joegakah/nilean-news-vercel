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
        
        articles = soup.find_all('div', class_='spotlight-post-1')
        
        for article in articles:
            article_url = article.find('a', class_='em-figure-link')['href']
            title = article.find('h3', class_='cat-title-4').get_text(strip=True)
            image = article.find('div', class_='featured-pic').get_attribute_list('src')[0]
            description = article.find('div', class_='featured-content').get_text(strip=True)

            article_data = get_article_data(article_url)

            the_article = {
                'title': title,
                'author': '',
                'url': article_url,
                'imageUrl': image,
                'description': description,
                'content': article_data['content'],
                'publishedAt': date,
                'category': article_data['category'],
                'source': 'eyeradio.org'
            }
            all_articles = []

            for article in articles:
                article_url = article.find('a', class_='em-figure-link')['href']
                title = article.find('h3', class_='article-title-2').get_text(strip=True)
                image = article.find('img', class_='wp-post-image')['src']
                date = article.find('span', class_='posts-date').get_text(strip=True)

                article_data = get_article_data(article_url)

                the_article = {
                'title': title,
                'author': '',
                'url': article_url,
                'imageUrl': image,
                'description': '',
                'content': article_data['content'],
                'publishedAt': date,
                'category': article_data['category'],
                'source': 'radiotamazuj.org'
                }

                all_articles.append(the_article)

            with open('all_articles.json', 'w') as f:
                json.dump(all_articles, f, indent=4)
        
    else:
        return "Error: Unable to retrieve article links"
    
get_articles(url)