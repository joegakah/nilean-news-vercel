import requests

def get_news(api_key, country='us', category='general', page_size=10):
    """
    Fetch news articles from News API
    Parameters:
    - api_key: Your News API key
    - country: 2-letter ISO country code (default: 'us')
    - category: News category (general, business, technology, etc.)
    - page_size: Number of results to return (1-100)
    """
    endpoint = 'https://newsapi.org/v2/top-headlines'
    headers = {'X-Api-Key': api_key}
    params = {
        'country': country,
        'category': category,
        'pageSize': page_size
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        
        if data['status'] == 'ok':
            return data['articles']
        else:
            print(f"Error: {data.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


if __name__ == "__main__":
    API_KEY = '8242808826a04102ac592826689bdbbe'
    
    articles = get_news(API_KEY, country='us', category='technology', page_size=5)
    
    if articles:
        for idx, article in enumerate(articles, 1):
            print(f"\nArticle {idx}:")
            print(f"Title: {article['title']}")
            print(f"Source: {article['source']['name']}")
            print(f"Description: {article['description']}")
            print(f"URL: {article['url']}")
            print(f"Published at: {article['publishedAt']}")
    else:
        print("No articles found about South Sudan.")