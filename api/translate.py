import requests

def translate_to_ssl(text):
  url = 'https://translate.neurollect.africa/api/translate'
  to_nuer_data = {
    'engine': 'YOUR_DEEPL_API_KEY',
    'text': text,
    'from': 'en',
    'to': 'nus'
  }

  to_dinka_data = {
    'engine': 'YOUR_DEEPL_API_KEY',
    'text': text,
    'from': 'en',
    'to': 'din'
  }

  nuer = requests.post(url, data=to_nuer_data)
  din = requests.post(url, data=to_dinka_data)
  
  return {
    'en': text,
    'nus': nuer.json()['translated_text'],
    'din': din.json()['translated_text']
  }