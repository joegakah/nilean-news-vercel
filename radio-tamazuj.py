import requests
from bs4 import BeautifulSoup

url = 'https://www.radiotamazuj.org/en/news'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.find_all('div', class_='spotlight-post-1')

    for article in articles:
        title = article.find('h3', class_='article-title-2').get_text()
        link = article.find('a', class_='em-figure-link')['href'] 
        print(f'Title: {title}\nLink: {link}\n')
else:
    print("Failed to retrieve the webpage.")